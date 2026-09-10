"""Operational access control and trace headers at the actual API boundary."""


def test_metrics_endpoint(guarded_api):
    client = guarded_api.client
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "metrolens_inspections_total" in response.text
    assert "metrolens_inspection_duration_seconds" in response.text
    client.headers.pop("Authorization")
    assert client.get("/metrics").status_code == 401


def test_auth_service_access_does_not_issue_officer_identity(guarded_api):
    client = guarded_api.client
    response = client.post("/api/v1/auth/token", json={
        "officer_id": "OFF-1001", "officer_name": "Self asserted officer",
        "badge_number": "made-up", "jurisdiction_code": "IN-KA-BLR-URBAN",
        "role": "DIRECTORATE_ADMIN",
    })
    assert response.status_code == 501
    assert "access_token" not in response.json()
    verified = client.get("/api/v1/auth/verify")
    assert verified.status_code == 200
    assert verified.json()["status"] == "VALID"
    assert verified.json()["officer_identity_verified"] is False
    client.headers.pop("Authorization")
    assert client.get("/api/v1/auth/verify").status_code == 401
    assert client.get("/api/v1/auth/verify", headers={
        "Authorization": "Bearer bad.forgedtoken"}).status_code == 401


def test_audit_affidavit_unavailable_until_identity_is_implemented(guarded_api):
    response = guarded_api.client.post("/api/v1/audit/affidavit", json={
        "inspection_id": "INS-AFF-2026-001", "raw_image_sha256": "4" * 64,
        "officer_name": "Self asserted officer", "overall_verdict": "NON_COMPLIANT",
    })
    assert response.status_code == 501
    assert "application/pdf" not in response.headers["content-type"]
    assert not response.content.startswith(b"%PDF-")


def test_audit_telemetry_headers_injected(guarded_api):
    response = guarded_api.client.get("/health")
    assert response.status_code == 200
    for name in ("X-Request-ID", "X-Trace-ID", "traceparent", "X-Response-Time-MS"):
        assert name in response.headers
