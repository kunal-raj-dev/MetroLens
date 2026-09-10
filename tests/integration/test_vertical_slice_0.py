"""Current API vertical slice with isolated model outputs and real evidence storage."""

import hashlib
import importlib
import socket
from types import SimpleNamespace

import pytest


def test_vs0_valid_packaging_end_to_end(guarded_api):
    data = guarded_api.upload()
    assert data["image_metadata"]["is_quality_valid"] is True
    assert data["image_metadata"]["sha256_hash"] == hashlib.sha256(guarded_api.image_bytes).hexdigest()
    assert data["declarations"]["mrp_inr"] == 240.0
    assert data["rule_evaluations"]["font_height_audit"]["status"] == "REVIEW"
    result = guarded_api.client.get(f'/api/v1/inspections/{data["inspection_id"]}')
    assert result.status_code == 200 and result.json() == data


def test_vs0_upload_security_checks(guarded_api):
    for payload, expected in ((b"SOME_CORRUPTED_BINARY_DATA", 415), (b"", 400)):
        response = guarded_api.client.post("/api/v1/inspect",
            files={"file": ("bad.jpg", payload, "image/jpeg")})
        assert response.status_code == expected
    assert not list(guarded_api.spool.base_dir.iterdir())


def test_vs0_quality_gate_rejection(guarded_api, monkeypatch):
    module = importlib.import_module("apps.api.services.pipeline_orchestrator")
    monkeypatch.setattr(module, "check_image_quality", lambda image: SimpleNamespace(
        passed=False, laplacian_variance=0.0, glare_ratio=0.0))
    monkeypatch.setattr(module.pipeline_orchestrator, "_get_ocr_service",
                        lambda: pytest.fail("OCR must not follow a quality rejection"))
    response = guarded_api.client.post("/api/v1/inspect",
        files={"file": ("flat.png", guarded_api.image_bytes, "image/png")})
    assert response.status_code == 422
    assert not list(guarded_api.spool.base_dir.iterdir())


def test_vs0_uncalibrated_handling(guarded_api):
    data = guarded_api.upload()
    assert data["calibration"]["is_calibrated"] is False
    assert data["calibration"]["scale_mm_per_px"] is None
    font = data["rule_evaluations"]["font_height_audit"]
    assert font["measured_net_qty_height_mm"] is None
    assert font["status"] == "REVIEW"


def test_vs0_missing_mrp_requires_other_panel_review(guarded_api, monkeypatch):
    module = importlib.import_module("apps.api.services.pipeline_orchestrator")
    tokens = [token for token in guarded_api.set_tokens() if "MRP" not in token.text]
    monkeypatch.setattr(module.pipeline_orchestrator, "_get_ocr_service", lambda: SimpleNamespace(
        extract=lambda *args, **kwargs: SimpleNamespace(tokens=tokens)))
    data = guarded_api.upload()
    assert data["declarations"]["mrp_inr"] is None
    assert data["state"] == "POTENTIAL_NON_COMPLIANCE"
    assert data["rule_evaluations"]["rule6_mandatory_status"]["details"]["mrp"] == "REVIEW"
    assert data["improvement_notice"] is None


def test_vs0_calibrated_scale_does_not_invent_panel_dimensions(guarded_api, monkeypatch):
    module = importlib.import_module("apps.api.services.pipeline_orchestrator")
    from nirikshak_calibration import AnchorDetectionStatus
    monkeypatch.setattr(module, "detect_anchor", lambda *args, **kwargs: SimpleNamespace(
        status=AnchorDetectionStatus.SUCCESS, confidence=0.95,
        geometry=SimpleNamespace(major_axis_px=100.0, aspect_ratio=1.0)))
    response = guarded_api.client.post("/api/v1/inspect",
        files={"file": ("pack.png", guarded_api.image_bytes, "image/png")},
        data={"anchor_type": "INR_10_COIN"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["calibration"]["is_calibrated"] is True
    assert data["calibration"]["scale_mm_per_px"] == pytest.approx(0.27)
    assert data["calibration"]["pdp_area_cm2"] is None
    assert data["rule_evaluations"]["font_height_audit"]["status"] == "REVIEW"


def test_vs0_evidence_source_linkage_and_retained_hashes(guarded_api):
    data = guarded_api.upload()
    observations = {token["token_id"]: token for token in data["ocr_observations"]}
    assert observations and data["evidence_crops"]
    for crop in data["evidence_crops"]:
        assert crop["source_token_id"] in observations
        x, y, width, height = crop["bbox_px"]
        assert 0 <= x < x + width <= 800
        assert 0 <= y < y + height <= 600
    audit = guarded_api.client.get(f'/api/v1/audit/verify/{data["inspection_id"]}').json()
    assert audit["status"] == "LOCAL_HASHES_MATCH"
    assert audit["cryptographic_signature_verified"] is False


def test_vs0_offline_execution(guarded_api, monkeypatch):
    def block_network(*args, **kwargs):
        raise AssertionError("Outbound network call attempted during isolated inspection")
    monkeypatch.setattr(socket, "create_connection", block_network)
    monkeypatch.setattr(socket.socket, "connect", block_network)
    # Calling the synchronous pipeline avoids intercepting Windows asyncio's
    # own loopback socketpair when it constructs the in-process test transport.
    module = importlib.import_module("apps.api.services.pipeline_orchestrator")
    result = module.pipeline_orchestrator.orchestrate_inspection(
        image_bytes=guarded_api.image_bytes, filename="offline.png", anchor_type="NONE")
    assert result.ocr_observations
    assert guarded_api.spool.get_session(result.inspection_id) is not None


def test_vs0_stage_timings(guarded_api):
    data = guarded_api.upload()
    telemetry = data["telemetry"]
    assert telemetry["total_duration_ms"] >= 0
    assert set(telemetry["stages_ms"]) == {
        "quality_gate", "metric_calibration", "ocr_perception", "normalization",
        "rule_engine", "evidence_packaging",
    }
    assert all(value >= 0 for value in telemetry["stages_ms"].values())
