"""
Integration Tests for Chunk 5: Mock eMaap REST Adapter & Evidentiary PDF Export Route.
Verifies:
1. POST /api/v1/report/pdf returns valid binary PDF stream with attachment header.
2. PDF compilation executes within < 500ms latency budget.
3. Report caching in ephemeral spool session (X-Report-Cached header).
4. POST /api/v1/emaap/mock-sync assigns statutory reference numbers and validates SHA-256 integrity.
5. Tamper detection on modified or non-hex cryptographic hash digests.
6. GET /api/v1/health readiness probe telemetry, host memory, CPU, and rules engine versioning.
"""

import re
import time
import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.schemas import HealthResponse, EMaapSyncResponse


@pytest.fixture
def client():
    """Provides FastAPI test client with reset rate limiter."""
    from apps.api.middleware.rate_limit import rate_limiter
    rate_limiter.reset_all()
    with TestClient(app) as test_client:
        test_client.headers.update({"X-Bypass-Rate-Limit": "true"})
        yield test_client
    rate_limiter.reset_all()


# =========================================================================
# PDF Report Export Tests (POST /api/v1/report/pdf)
# =========================================================================

def test_download_pdf_report_binary_validity(client):
    """Verifies that PDF report endpoint compiles and returns valid binary PDF stream."""
    inspection_id = "INSP-20260905-9988"

    response = client.post(
        "/api/v1/report/pdf",
        json={
            "inspection_id": inspection_id,
            "officer_notes": "Surveillance audit in wholesale FMCG hub.",
            "include_raw_image": True,
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert f'filename="metrolens_report_{inspection_id}.pdf"' in response.headers["content-disposition"]

    # Binary PDF checks
    content = response.content
    assert content.startswith(b"%PDF-")
    assert b"%%EOF" in content[-1024:]
    assert len(content) > 3000


def test_pdf_report_compilation_latency_sub_500ms(client):
    """Verifies that PDF report compilation completes in < 500ms."""
    # Warmup
    _ = client.post(
        "/api/v1/report/pdf",
        json={"inspection_id": "INSP-WARMUP-001"},
    )

    # Benchmark run
    start = time.perf_counter()
    response = client.post(
        "/api/v1/report/pdf",
        json={"inspection_id": "INSP-BENCH-002"},
    )
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    assert response.status_code == 200
    assert elapsed_ms < 500.0, f"PDF generation exceeded 500ms threshold: {elapsed_ms:.2f}ms"


def test_pdf_report_session_caching(client):
    """Verifies that secondary requests for the same inspection ID are served from cache."""
    inspection_id = "INSP-CACHE-003"

    # First request: compiles fresh
    r1 = client.post(
        "/api/v1/report/pdf",
        json={"inspection_id": inspection_id},
    )
    assert r1.status_code == 200
    assert r1.headers.get("x-report-cached") == "false"

    # Second request: served from ephemeral spool cache
    r2 = client.post(
        "/api/v1/report/pdf",
        json={"inspection_id": inspection_id},
    )
    assert r2.status_code == 200
    assert r2.headers.get("x-report-cached") == "true"
    assert len(r1.content) == len(r2.content)


# =========================================================================
# eMaap National Portal Sync Tests (POST /api/v1/emaap/mock-sync)
# =========================================================================

def test_emaap_mock_sync_successful(client):
    """
    Verifies that a valid inspection dossier syncs with the national eMaap portal mock,
    receiving an official reference number and ACCEPTED_FOR_RECORD status.
    """
    valid_sha256 = "a" * 64

    response = client.post(
        "/api/v1/emaap/mock-sync",
        json={
            "inspection_id": "INSP-20260905-1234",
            "jurisdiction_code": "DL-01-CENTRAL",
            "officer_id": "LMO-DELHI-42",
            "compliance_state": "COMPLIANT",
            "improvement_notice_issued": False,
            "dossier_sha256": valid_sha256,
        },
    )

    assert response.status_code == 200
    data = response.json()

    # Validate against Pydantic schema
    parsed = EMaapSyncResponse.model_validate(data)
    assert parsed.sync_status == "ACCEPTED_FOR_RECORD"
    assert parsed.tamper_verification == "VERIFIED_VALID"
    assert re.match(r"^EMAAP-DL-\d{4}-\d{6}$", parsed.emaap_reference_no)
    assert len(parsed.received_at) > 10


def test_emaap_mock_sync_tamper_detection(client):
    """
    Verifies that an invalid non-hex hash triggers TAMPER_DETECTED and REJECTED status.
    """
    tampered_sha256 = "z" * 64  # 64 chars, but non-hexadecimal

    response = client.post(
        "/api/v1/emaap/mock-sync",
        json={
            "inspection_id": "INSP-20260905-TAMPER",
            "jurisdiction_code": "MH-02-MUMBAI",
            "officer_id": "LMO-MUMBAI-09",
            "compliance_state": "NON_COMPLIANT",
            "improvement_notice_issued": True,
            "dossier_sha256": tampered_sha256,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sync_status"] == "REJECTED"
    assert data["tamper_verification"] == "TAMPER_DETECTED"
    assert "EMAAP-MH-" in data["emaap_reference_no"]


# =========================================================================
# Health & Telemetry Probe Tests (GET /api/v1/health)
# =========================================================================

def test_health_readiness_probe(client):
    """
    Verifies GET /api/v1/health readiness probe schema, resource telemetry,
    and rules engine metadata conforming to API Contract Section 3.2.
    """
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()

    # Validate Pydantic schema
    health = HealthResponse.model_validate(data)
    assert health.status == "healthy"
    assert health.version == "1.0.0"
    assert health.environment == "production"
    assert health.uptime_seconds >= 0.0

    # System telemetry
    assert health.system.cpu_percent >= 0.0
    assert health.system.memory_used_mb > 0.0
    assert health.system.memory_total_mb > 0.0

    # Inference models readiness
    assert health.models.paddleocr_onnx_det == "loaded_cpu_int8"
    assert health.models.paddleocr_onnx_rec == "loaded_cpu_int8"
    assert health.models.scale_calibrator == "ready"

    # Rules engine status
    assert health.rules_engine.status == "active"
    assert "JanVishwas" in health.rules_engine.ruleset_version
    assert health.rules_engine.verified_rules_count >= 4
