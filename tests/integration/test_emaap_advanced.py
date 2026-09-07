"""
Integration Tests for National Legal Metrology (eMaap) Integration
==================================================================
Tests HMAC signing, circuit breaker behavior, stateful mock server,
and prosecution case lifecycle under Section 36(1) and Section 48.
"""

import pytest

from apps.api.integrations.emaap.emaap_client import (
    EMaapClient,
    EMaapClientConfig,
    CircuitBreakerState,
)
from apps.api.integrations.emaap.emaap_mock_server import (
    StatefulEMaapMockServer,
    EMaapCaseRecord,
)
from apps.api.integrations.emaap.case_filing import (
    ProsecutionCaseManager,
    CaseStage,
)


def test_emaap_hmac_header_generation_and_verification():
    """Verify cryptographic HMAC-SHA256 signature calculation and verification."""
    config = EMaapClientConfig(api_key="TEST_KEY", api_secret="SECRET_HMAC_123")
    client = EMaapClient(config=config)

    body = b'{"inspection_id": "INS-101", "verdict": "NON_COMPLIANT"}'
    headers = client.build_hmac_headers("POST", "/api/v1/inspections/sync", body)

    assert "X-EMaap-ApiKey" in headers
    assert "X-EMaap-Signature" in headers
    assert headers["X-EMaap-ApiKey"] == "TEST_KEY"

    # Verify incoming webhook signature check
    is_valid = client.verify_incoming_webhook_hmac(
        endpoint="/api/v1/inspections/sync",
        body_bytes=body,
        timestamp_str=headers["X-EMaap-Timestamp"],
        nonce_str=headers["X-EMaap-Nonce"],
        received_signature=headers["X-EMaap-Signature"],
    )
    assert is_valid is True

    # Tampered body should fail verification
    is_tampered_valid = client.verify_incoming_webhook_hmac(
        endpoint="/api/v1/inspections/sync",
        body_bytes=b'{"inspection_id": "TAMPERED"}',
        timestamp_str=headers["X-EMaap-Timestamp"],
        nonce_str=headers["X-EMaap-Nonce"],
        received_signature=headers["X-EMaap-Signature"],
    )
    assert is_tampered_valid is False


def test_emaap_circuit_breaker_behavior():
    """Verify circuit breaker trips to OPEN after threshold failures and denies attempts."""
    config = EMaapClientConfig(
        circuit_breaker_failure_threshold=2,
        circuit_breaker_cooldown_seconds=10.0,
    )

    def failing_transport(method, url, payload, headers):
        raise RuntimeError("Connection Refused by Gateway")

    client = EMaapClient(config=config, http_transport=failing_transport)

    # 1st failure
    r1 = client.sync_inspection({"id": 1})
    assert r1.is_success is False
    assert client.circuit_breaker.state == CircuitBreakerState.CLOSED

    # 2nd failure -> Trips to OPEN
    r2 = client.sync_inspection({"id": 2})
    assert r2.is_success is False
    assert client.circuit_breaker.state == CircuitBreakerState.OPEN

    # 3rd request should fail-fast with HTTP 503 without attempting transport
    r3 = client.sync_inspection({"id": 3})
    assert r3.status_code == 503
    assert "Circuit Breaker OPEN" in r3.error_message


def test_stateful_emaap_mock_server():
    """Verify case filing, 15-day cure calculation, and merchant cure recording."""
    server = StatefulEMaapMockServer(authorized_api_key="METROLENS_PROD_KEY")

    # File case with violations
    status_code, resp = server.file_inspection_case(
        api_key="METROLENS_PROD_KEY",
        inspection_id="INS-EXP-001",
        jurisdiction_code="MH-01",
        raw_image_sha256="abcdef123456",
        violations=[{"rule": "Rule 6(1)(e)", "defect": "Missing MRP"}],
        overall_verdict="NON_COMPLIANT",
    )

    assert status_code == 201
    assert resp["status"] == "SUCCESS"
    case_ref = resp["case_reference"]
    assert case_ref.startswith("EMAAP-MH-01-2026-")
    assert resp["lifecycle_status"] == "NOTICE_DISPATCHED"
    assert resp["cure_deadline"] is not None

    # Retrieve record
    case_record = server.get_case(case_ref)
    assert isinstance(case_record, EMaapCaseRecord)
    assert case_record.compounding_fee_inr == 25000

    # Merchant remedies packaging
    cured = server.record_merchant_cure(case_ref)
    assert cured is True
    assert server.get_case(case_ref).status == "CURED"


def test_prosecution_case_manager_lifecycle():
    """Verify end-to-end case escalation from evaluation to compounding ladder."""
    manager = ProsecutionCaseManager(default_cure_period_days=15)

    dossier = manager.create_case(
        inspection_id="INS-CASE-999",
        merchant_name="SuperMart Retail Pvt Ltd",
        manufacturer_name="Confectionery Works",
        commodity_name="Chocolate Wafer 50g",
        jurisdiction_code="DL-03",
        violation_rules=["Rule 6(1)(c)", "Rule 26"],
        offense_count=2,  # Repeat offender
    )

    assert dossier.stage == CaseStage.EVALUATED

    # Issue improvement notice
    manager.issue_improvement_notice(dossier.case_id)
    assert dossier.stage == CaseStage.NOTICE_SERVED
    assert dossier.cure_deadline_iso is not None

    # Re-inspection fails (merchant did not remedy)
    manager.verify_merchant_cure(dossier.case_id, is_rectified=False)
    assert dossier.stage == CaseStage.UNREMEDIED_EXPIRED
    # Second offense compounding fee: Rs. 50,000
    assert dossier.compounding_quantum_inr == 50000

    # Merchant compounds offense
    manager.compound_case(dossier.case_id, receipt_reference="RCPT-GOV-89421")
    assert dossier.stage == CaseStage.COMPOUNDED
    assert dossier.compounding_receipt_ref == "RCPT-GOV-89421"
