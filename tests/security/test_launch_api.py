"""Launch security regression checks using isolated temporary evidence storage."""

import importlib
import io
import hashlib
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient


API_KEY = "test-only-api-key-" + "a" * 48


@pytest.fixture
def api(monkeypatch, tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("launch")
    monkeypatch.setenv("METROLENS_API_KEY", API_KEY)
    monkeypatch.setenv("METROLENS_SPOOL_DIR", str(tmp_path / "spool"))
    main = importlib.import_module("apps.api.main")
    from apps.api.services.spool_service import SpoolService
    from apps.api.services import inspection_store as store_module
    from apps.api.routes import inspect as inspect_route, report, audit
    spool = SpoolService(base_dir=tmp_path / "isolated", auto_start_daemon=False)
    store = store_module.InspectionStore()
    monkeypatch.setattr(main, "spool_service", spool)
    monkeypatch.setattr(inspect_route.pipeline_orchestrator, "spooler", spool)
    monkeypatch.setattr(inspect_route, "inspection_store", store)
    monkeypatch.setattr(store_module, "inspection_store", store)
    monkeypatch.setattr(report, "spool_service", spool)
    monkeypatch.setattr(audit, "spool_service", spool)
    middleware = main.app.middleware_stack
    while middleware is not None:
        if hasattr(middleware, "limiter"):
            middleware.limiter.reset_all()
        middleware = getattr(middleware, "app", None)
    return main, TestClient(main.app, raise_server_exceptions=False)


@pytest.fixture
def authorized():
    return {"Authorization": f"Bearer {API_KEY}"}


@pytest.mark.parametrize("method,path,body", [
    ("GET", "/api/v1/inspections/INSP-NO-RECORD", None),
    ("POST", "/api/v1/report/pdf", {"inspection_id": "INSP-NO-RECORD"}),
    ("GET", "/api/v1/audit/verify/INSP-NO-RECORD", None),
    ("GET", "/metrics", None),
])
def test_operational_routes_require_access_key(api, method, path, body):
    _, client = api
    assert client.request(method, path, json=body).status_code == 401


def test_unimplemented_identity_and_certification_fail_closed(api, authorized):
    _, client = api
    assert client.post("/api/v1/auth/token", json={
        "officer_id": "made-up", "officer_name": "Made Up", "badge_number": "fake",
        "jurisdiction_code": "IN-CENTRAL", "role": "DIRECTORATE_ADMIN",
    }).status_code == 501
    assert client.post("/api/v1/audit/affidavit", headers=authorized, json={
        "inspection_id": "INSP-NO-RECORD", "raw_image_sha256": "0" * 64,
        "raw_image_filename": '<img src="http://invalid.example/image.png"/>',
        "raw_image_size_bytes": 10, "officer_name": "Made Up", "badge_number": "fake",
    }).status_code == 501


def test_unknown_reports_and_verification_never_fabricate_success(api, authorized):
    _, client = api
    assert client.post("/api/v1/report/pdf", headers=authorized,
                       json={"inspection_id": "INSP-NO-RECORD"}).status_code == 404
    assert client.get("/api/v1/audit/verify/INSP-NO-RECORD", headers=authorized).status_code == 404


def test_health_does_not_assert_unchecked_model_readiness(api):
    _, client = api
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "models" not in response.json()
    assert "system" not in response.json()


def test_rate_limit_cannot_be_bypassed_with_client_headers():
    from apps.api.middleware.rate_limit import InMemoryRateLimiter, RateLimitMiddleware
    from fastapi import FastAPI

    app = FastAPI()
    app.add_middleware(RateLimitMiddleware, rate_limiter=InMemoryRateLimiter(requests_per_window=1))

    @app.get("/work")
    def work():
        return {"ok": True}

    client = TestClient(app)
    assert client.get("/work", headers={"X-Forwarded-For": "first"}).status_code == 200
    assert client.get("/work", headers={
        "X-Bypass-Rate-Limit": "true", "X-Forwarded-For": "second",
    }).status_code == 429


@pytest.fixture
def image_bytes():
    from PIL import Image
    from PIL.PngImagePlugin import PngInfo
    image = Image.new("RGB", (800, 600), "gray")
    metadata = PngInfo()
    metadata.add_text("private-location", "must-not-appear-in-derivative")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", pnginfo=metadata)
    return buffer.getvalue()


@pytest.fixture
def controlled_pipeline(api, monkeypatch):
    from apps.api.routes.inspect import pipeline_orchestrator
    module = importlib.import_module("apps.api.services.pipeline_orchestrator")
    monkeypatch.setattr(module, "check_image_quality", lambda image: SimpleNamespace(
        passed=True, laplacian_variance=200.0, glare_ratio=0.0))
    return pipeline_orchestrator


def set_ocr(monkeypatch, pipeline, text="Net Quantity: 200 g", confidence=0.98):
    token = SimpleNamespace(token_id="observed-1", text=text, confidence=confidence,
                            bbox=[20, 30, 220, 80])
    monkeypatch.setattr(pipeline, "_get_ocr_service", lambda: SimpleNamespace(
        extract=lambda *args, **kwargs: SimpleNamespace(tokens=[token])))


def upload(client, authorized, image_bytes, **fields):
    return client.post("/api/v1/inspect", headers=authorized,
                       files={"file": ("packaging.png", image_bytes, "image/png")},
                       data={"anchor_type": "NONE", **fields})


def test_missing_api_configuration_fails_closed(api, authorized, monkeypatch):
    _, client = api
    monkeypatch.delenv("METROLENS_API_KEY")
    assert client.get("/api/v1/auth/verify", headers=authorized).status_code == 503
    assert client.get("/health").status_code == 200


def test_legacy_creation_and_public_fixture_switch_are_disabled(api, authorized, image_bytes):
    _, client = api
    assert client.post("/api/v1/inspections", headers=authorized, json={"inspection_id": "replace-me"}).status_code == 501
    assert upload(client, authorized, image_bytes, mock_fixture_key="compliant").status_code == 400
    assert upload(client, authorized, b"not an image").status_code == 415


@pytest.mark.parametrize("failure", ["missing", "empty", "exception"])
def test_ocr_failures_never_produce_synthetic_assessments(api, authorized, image_bytes,
                                                       controlled_pipeline, monkeypatch, failure):
    _, client = api
    if failure == "missing":
        service = None
    elif failure == "empty":
        service = SimpleNamespace(extract=lambda *args, **kwargs: SimpleNamespace(tokens=[]))
    else:
        def fail(*args, **kwargs):
            raise RuntimeError("private model path")
        service = SimpleNamespace(extract=fail)
    monkeypatch.setattr(controlled_pipeline, "_get_ocr_service", lambda: service)
    response = upload(client, authorized, image_bytes)
    assert response.status_code == (422 if failure == "empty" else 503)
    assert "COMPLIANT" not in response.text and "private model path" not in response.text
    assert not list(controlled_pipeline.spooler.base_dir.iterdir())


def test_quality_rejection_precedes_ocr(api, authorized, image_bytes, controlled_pipeline, monkeypatch):
    module = importlib.import_module("apps.api.services.pipeline_orchestrator")
    monkeypatch.setattr(module, "check_image_quality", lambda image: SimpleNamespace(
        passed=False, laplacian_variance=0.0, glare_ratio=0.0))
    monkeypatch.setattr(controlled_pipeline, "_get_ocr_service", lambda: pytest.fail("OCR must not run"))
    assert upload(api[1], authorized, image_bytes).status_code == 422


def test_low_confidence_cannot_grant_small_package_exemption(api, authorized, image_bytes,
                                                          controlled_pipeline, monkeypatch):
    set_ocr(monkeypatch, controlled_pipeline, text="Net Quantity: 5 g", confidence=0.20)
    response = upload(api[1], authorized, image_bytes)
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["state"] == "MANUAL_REVIEW_REQUIRED"
    assert not result["rule_evaluations"]["exemption_status"]["is_exempt"]
    assert "confidence" in result["summary_reason"].lower()
    assert result["improvement_notice"] is None


def test_single_panel_missing_fields_do_not_adjudicate_entire_package(api, authorized, image_bytes,
                                                                   controlled_pipeline, monkeypatch):
    set_ocr(monkeypatch, controlled_pipeline)
    response = upload(api[1], authorized, image_bytes)
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["state"] == "POTENTIAL_NON_COMPLIANCE"
    assert "panel" in result["summary_reason"].lower()
    assert result["improvement_notice"] is None
    assert result["rule_evaluations"]["font_height_audit"]["status"] == "REVIEW"
    assert result["calibration"]["pdp_area_cm2"] is None
    retrieved = api[1].get(f'/api/v1/inspections/{result["inspection_id"]}', headers=authorized)
    assert retrieved.json() == result


def test_original_evidence_report_binding_and_tamper_detection(api, authorized, image_bytes,
                                                             controlled_pipeline, monkeypatch):
    from apps.api.routes import report
    set_ocr(monkeypatch, controlled_pipeline)
    response = upload(api[1], authorized, image_bytes)
    assert response.status_code == 200, response.text
    result = response.json()
    identifier = result["inspection_id"]
    session = controlled_pipeline.spooler.get_session(identifier)
    assert session.raw_image_path.read_bytes() == image_bytes
    assert session.sanitized_image_path.read_bytes() != image_bytes
    assert result["image_metadata"]["sha256_hash"] == hashlib.sha256(image_bytes).hexdigest()
    verification = api[1].get(f"/api/v1/audit/verify/{identifier}", headers=authorized).json()
    assert verification["status"] == "LOCAL_HASHES_MATCH"
    assert verification["cryptographic_signature_verified"] is False
    observed = {}
    def compile_report(canonical, **kwargs):
        observed["result"] = canonical
        observed["options"] = kwargs
        return b"%PDF-test-only-renderer"
    monkeypatch.setattr(report.pdf_compiler, "compile_report_pdf", compile_report)
    pdf = api[1].post("/api/v1/report/pdf", headers=authorized, json={
        "inspection_id": identifier, "officer_notes": "Operator annotation", "include_raw_image": True})
    assert pdf.status_code == 200
    assert observed["result"].overall_verdict == result["state"]
    assert observed["result"].sha256_hash == hashlib.sha256(image_bytes).hexdigest()
    assert observed["options"]["officer_notes"] == "Operator annotation"
    assert observed["options"]["reference_image_bytes"] == session.sanitized_image_path.read_bytes()
    assert api[1].post("/api/v1/report/pdf", headers=authorized, json={
        "inspection_id": identifier, "include_raw_image": False}).status_code == 200
    assert observed["options"]["reference_image_bytes"] is None
    assert api[1].post("/api/v1/report/pdf", headers=authorized, json={
        "inspection_id": identifier, "officer_notes": "a" * 2001}).status_code == 400
    session.raw_image_path.write_bytes(b"altered")
    assert api[1].post("/api/v1/report/pdf", headers=authorized,
                       json={"inspection_id": identifier}).status_code == 409
    assert api[1].get(f"/api/v1/audit/verify/{identifier}", headers=authorized).json()["status"] == "INTEGRITY_MISMATCH"


def test_all_actual_ocr_observations_survive_response_and_lookup(api, authorized, image_bytes,
                                                              controlled_pipeline, monkeypatch):
    tokens = [SimpleNamespace(token_id="observed-quantity", text="Net Quantity: 200 g",
        confidence=0.57, bbox=[20, 30, 220, 80], script="latin",
        polygon=[[20, 30], [220, 30], [220, 80], [20, 80]]),
        SimpleNamespace(token_id="observed-other", text="Unclassified actual text",
            confidence=0.72, bbox=[50, 100, 300, 150], script="unknown")]
    monkeypatch.setattr(controlled_pipeline, "_get_ocr_service", lambda: SimpleNamespace(
        extract=lambda *args, **kwargs: SimpleNamespace(tokens=tokens)))
    response = upload(api[1], authorized, image_bytes)
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["ocr_observations"]) == 2
    first, second = data["ocr_observations"]
    assert first == {"token_id": "observed-quantity", "text": "Net Quantity: 200 g",
        "confidence": 0.57, "bounding_box": {"x_min": 20, "y_min": 30, "x_max": 220, "y_max": 80},
        "polygon": tokens[0].polygon, "script": "latin"}
    assert second["text"] == "Unclassified actual text" and second["confidence"] == 0.72
    assert data["evidence_crops"][0]["source_token_id"] == first["token_id"]
    lookup = api[1].get(f'/api/v1/inspections/{data["inspection_id"]}', headers=authorized)
    assert lookup.json()["ocr_observations"] == data["ocr_observations"]


def test_evidence_verifier_rejects_files_outside_the_inspection(api, authorized, image_bytes,
                                                            controlled_pipeline, monkeypatch, tmp_path):
    from apps.api.services.inspection_store import verify_retained_evidence, inspection_store
    set_ocr(monkeypatch, controlled_pipeline)
    result = upload(api[1], authorized, image_bytes).json()
    identifier = result["inspection_id"]
    session = controlled_pipeline.spooler.get_session(identifier)
    outside = tmp_path / "outside.png"
    outside.write_bytes(image_bytes)
    session.raw_image_path = outside
    record = inspection_store.get(identifier, hashlib.sha256(API_KEY.encode()).hexdigest())
    checks = verify_retained_evidence(record, controlled_pipeline.spooler)
    assert checks["raw_image_matches"] is False


def test_store_expiry_capacity_and_service_principal_binding(api, authorized, image_bytes,
                                                          controlled_pipeline, monkeypatch):
    from apps.api.services.inspection_store import InspectionStore, inspection_store
    set_ocr(monkeypatch, controlled_pipeline)
    result = upload(api[1], authorized, image_bytes).json()
    record = inspection_store.get(result["inspection_id"], hashlib.sha256(API_KEY.encode()).hexdigest())
    now = [0.0]
    store = InspectionStore(max_records=1, ttl_seconds=10, clock=lambda: now[0])
    def put(identifier):
        return store.put(record.response.model_copy(update={"inspection_id": identifier}),
                         record.compliance_result.model_copy(update={"inspection_id": identifier}),
                         "principal-one", record.raw_sha256, record.sanitized_sha256,
                         record.raw_size_bytes, record.sanitized_size_bytes)
    put("INSP-ONE")
    assert store.get("INSP-ONE", "principal-two") is None
    with pytest.raises(ValueError):
        put("INSP-ONE")
    put("INSP-TWO")
    assert store.get("INSP-ONE", "principal-one") is None
    now[0] = 10.0
    assert store.get("INSP-TWO", "principal-one") is None


@pytest.mark.asyncio
async def test_oversized_content_length_digits_cannot_trigger_integer_conversion_error():
    from apps.api.middleware.body_limit import BodyLimitMiddleware
    sent = []
    async def downstream(*args):
        pytest.fail("An oversized request must never reach multipart parsing")
    async def receive():
        pytest.fail("Declared oversized bodies must be rejected before receiving them")
    async def send(message):
        sent.append(message)
    await BodyLimitMiddleware(downstream)(
        {"type": "http", "headers": [(b"content-length", b"9" * 5000)]}, receive, send)
    assert sent[0]["status"] == 413


@pytest.mark.asyncio
async def test_streamed_body_limit_applies_without_content_length():
    from apps.api.middleware.body_limit import BodyLimitMiddleware
    messages = iter([
        {"type": "http.request", "body": b"123", "more_body": True},
        {"type": "http.request", "body": b"45", "more_body": False},
    ])
    sent = []
    async def receive():
        return next(messages)
    async def send(message):
        sent.append(message)
    async def downstream(*args):
        pytest.fail("Oversized body must not reach multipart parsing")
    await BodyLimitMiddleware(downstream, max_body_bytes=4)(
        {"type": "http", "headers": []}, receive, send)
    assert sent[0]["status"] == 413


def test_processing_capacity_rejects_another_upload_without_blocking_health(api, authorized, image_bytes):
    from apps.api.routes.inspect import processing_slot
    assert processing_slot.acquire(blocking=False)
    try:
        response = upload(api[1], authorized, image_bytes)
        assert response.status_code == 429 and response.headers["retry-after"] == "5"
        assert api[1].get("/health").status_code == 200
    finally:
        processing_slot.release()
