"""
Integration Tests for New API Routes & Middleware
=================================================
Tests GET /metrics, POST /api/v1/auth/token, GET /api/v1/auth/verify,
POST /api/v1/audit/affidavit, and AuditTelemetryMiddleware tracing headers.
"""

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.middleware.rate_limit import rate_limiter


@pytest.fixture(autouse=True)
def reset_rate_limits():
    """Reset rate limiter and bypass limits for tests."""
    rate_limiter.reset_all()


def test_metrics_endpoint():
    """Verify GET /metrics returns Prometheus formatted exposition."""
    with TestClient(app) as client:
        resp = client.get("/metrics")
        assert resp.status_code == 200
        assert "text/plain" in resp.headers["content-type"]
        body = resp.text
        assert "metrolens_inspections_total" in body
        assert "metrolens_inspection_duration_seconds" in body


def test_auth_token_issuance_and_verification():
    """Verify login, token issuance, and Bearer token verification."""
    with TestClient(app) as client:
        # 1. Obtain token
        login_payload = {
            "officer_id": "OFF-1001",
            "officer_name": "Smt. Priya Sundaram",
            "badge_number": "KA-LM-4402",
            "jurisdiction_code": "IN-KA-BLR-URBAN",
            "role": "LEGAL_METROLOGY_OFFICER",
        }
        res_login = client.post("/api/v1/auth/token", json=login_payload)
        assert res_login.status_code == 200
        data = res_login.json()
        assert "access_token" in data
        token = data["access_token"]
        assert "inspection:read" in data["permissions"]

        # 2. Verify valid token
        res_verify = client.get(
            "/api/v1/auth/verify",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res_verify.status_code == 200
        v_data = res_verify.json()
        assert v_data["status"] == "VALID"
        assert v_data["officer_name"] == "Smt. Priya Sundaram"
        assert "Bengaluru Urban Inspectorate" in v_data["jurisdiction_name"]

        # 3. Reject missing or forged token
        res_fail_missing = client.get("/api/v1/auth/verify")
        assert res_fail_missing.status_code == 401

        res_fail_forged = client.get(
            "/api/v1/auth/verify",
            headers={"Authorization": "Bearer bad.forgedtoken"},
        )
        assert res_fail_forged.status_code == 401


def test_audit_affidavit_generation():
    """Verify Section 63 BSA 2023 affidavit generation route."""
    with TestClient(app) as client:
        payload = {
            "inspection_id": "INS-AFF-2026-001",
            "raw_image_sha256": "4b5d6a7e8f901234567890abcdef1234567890abcdef1234567890abcdef1234",
            "raw_image_filename": "sample_spice_box.jpg",
            "raw_image_size_bytes": 450020,
            "officer_name": "Inspector R. K. Sharma",
            "badge_number": "DL-LM-0991",
            "district": "South Delhi",
            "state": "Delhi",
            "statutory_violations_count": 2,
            "overall_verdict": "NON_COMPLIANT",
        }
        resp = client.post(
            "/api/v1/audit/affidavit",
            json=payload,
            headers={"X-Bypass-Rate-Limit": "true"},
        )
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "application/pdf"
        assert "Affidavit_BSA_Sec63" in resp.headers["content-disposition"]
        assert resp.content.startswith(b"%PDF-")


def test_audit_telemetry_headers_injected():
    """Verify that AuditTelemetryMiddleware injects X-Request-ID, X-Trace-ID, and traceparent."""
    with TestClient(app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert "X-Request-ID" in resp.headers
        assert "X-Trace-ID" in resp.headers
        assert "traceparent" in resp.headers
        assert "X-Response-Time-MS" in resp.headers
