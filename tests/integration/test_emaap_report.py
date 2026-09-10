"""Genuine retained-evidence reports and truthful unavailable integrations."""

import time
import pytest


@pytest.fixture
def client(guarded_api):
    return guarded_api.client


@pytest.fixture
def inspection(guarded_api):
    return guarded_api.upload()


def test_download_pdf_report_binary_validity(client, inspection):
    inspection_id = inspection["inspection_id"]
    response = client.post("/api/v1/report/pdf", json={
        "inspection_id": inspection_id,
        "officer_notes": "Operator observation from local packaging screening.",
        "include_raw_image": True,
    })
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "application/pdf"
    assert f'filename="metrolens_report_{inspection_id}.pdf"' in response.headers["content-disposition"]
    assert response.headers["cache-control"] == "no-store"
    assert response.content.startswith(b"%PDF-")
    assert b"%%EOF" in response.content[-1024:]
    assert len(response.content) > 3000


def test_pdf_report_compilation_latency_sub_500ms(client, inspection):
    payload = {"inspection_id": inspection["inspection_id"]}
    assert client.post("/api/v1/report/pdf", json=payload).status_code == 200
    start = time.perf_counter()
    response = client.post("/api/v1/report/pdf", json=payload)
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    assert response.status_code == 200
    assert elapsed_ms < 500.0, f"PDF compilation took {elapsed_ms:.2f}ms"


def test_repeated_pdf_request_rechecks_retained_evidence(client, inspection, guarded_api):
    inspection_id = inspection["inspection_id"]
    payload = {"inspection_id": inspection_id}
    assert client.post("/api/v1/report/pdf", json=payload).status_code == 200
    assert client.post("/api/v1/report/pdf", json=payload).status_code == 200
    session = guarded_api.spool.get_session(inspection_id)
    session.raw_image_path.write_bytes(b"modified retained image")
    assert client.post("/api/v1/report/pdf", json=payload).status_code == 409
    audit = client.get(f"/api/v1/audit/verify/{inspection_id}").json()
    assert audit["status"] == "INTEGRITY_MISMATCH"
    assert audit["tamper_detected"] is True


def test_emaap_sync_cannot_assign_fictional_official_reference(client):
    response = client.post("/api/v1/emaap/mock-sync", json={
        "inspection_id": "INSP-UNOBSERVED", "dossier_sha256": "a" * 64,
        "compliance_state": "COMPLIANT", "officer_id": "made-up",
    })
    assert response.status_code == 501
    assert "emaap_reference_no" not in response.json()


def test_emaap_sync_cannot_claim_tamper_verification_from_caller_hash(client):
    response = client.post("/api/v1/emaap/mock-sync", json={
        "inspection_id": "INSP-UNOBSERVED", "dossier_sha256": "z" * 64,
    })
    assert response.status_code == 501
    assert "tamper_verification" not in response.json()


def test_health_is_public_liveness_only(client):
    client.headers.pop("Authorization")
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "metrolens-api"}
