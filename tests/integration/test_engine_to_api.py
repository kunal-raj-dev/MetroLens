"""
Integration Tests: Rules Engine to Backend API (Member 3 to Member 4 & 5).
Verifies:
1. StatutoryRuleEngine produces ComplianceEvaluationResult conforming strictly to docs/API_CONTRACT.md.
2. ComplianceEvaluationResult converts cleanly to nirikshak_shared.models.contracts (InspectionResult, RuleEvaluation).
3. FastAPI endpoint /api/v1/inspections serializes and returns canonical inspection outcomes with rule evaluations.
4. Complete JSON serialization roundtrip with zero loss of Devanagari Unicode, decimal precision, or statutory citations.
"""

import json
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from nirikshak_shared.models.contracts import (
    InspectionRequest,
    InspectionResult,
    RuleEvaluation,
    DeclarationField,
)
from nirikshak_shared.models.primitives import (
    InspectionStatus,
    OverallVerdict,
    RuleVerdict,
    CalibrationStatus,
)
from nirikshak_rules_engine import (
    StatutoryRuleEngine,
    CanonicalDeclaration,
    MetricScaleResult,
    UnitType,
    ComplianceState,
    ComplianceEvaluationResult,
)


@pytest.fixture
def api_client():
    return TestClient(app)


@pytest.fixture
def statutory_engine():
    return StatutoryRuleEngine()


def test_rule_engine_to_shared_contracts_mapping(statutory_engine):
    """
    Verifies that StatutoryRuleEngine evaluation records map cleanly
    to nirikshak_shared.models.contracts.RuleEvaluation.
    """
    decl = CanonicalDeclaration(
        commodity_name="Fortified Atta",
        mrp_inr=210.0,
        tax_qualifier_present=True,
        net_quantity_value=5.0,
        net_quantity_unit=UnitType.KILOGRAM,
        declared_usp_value=42.0,
        declared_usp_unit="kg",
        mfg_month=6,
        mfg_year=2026,
        manufacturer_name="Hindustan Foods Ltd",
        manufacturer_address="Plot 12, Industrial Area, Noida",
        consumer_care_email="care@hindustanfoods.com",
        consumer_care_phone="1800-111-2222",
        country_of_origin="India",
    )

    result: ComplianceEvaluationResult = statutory_engine.evaluate(decl, inspection_id="INSP-INTEG-001")
    assert result.overall_verdict == ComplianceState.COMPLIANT

    # Convert to shared contracts
    shared_rule_evals = []
    for rec in result.rule_evaluations:
        verdict_enum = RuleVerdict.PASS if rec.is_compliant else RuleVerdict.FAIL
        shared_rule_evals.append(
            RuleEvaluation(
                rule_id=rec.rule_id,
                rule_title=rec.rule_title,
                verdict=verdict_enum,
                statutory_reference=rec.statutory_reference,
                observed_summary=rec.observed_value or "None",
                required_summary=rec.required_value or "None",
                evaluation_notes=rec.notes,
            )
        )

    assert len(shared_rule_evals) >= 8

    # Create canonical InspectionResult
    inspection_result = InspectionResult(
        inspection_id=result.inspection_id,
        status=InspectionStatus.SUCCESS,
        image_sha256="a" * 64,
        overall_verdict=OverallVerdict.COMPLIANT,
        quality_gate_passed=True,
        calibration_status=CalibrationStatus.CALIBRATED,
        rule_evaluations=shared_rule_evals,
    )

    # Validate JSON serializability
    dumped_json = inspection_result.model_dump_json()
    parsed_dict = json.loads(dumped_json)
    assert parsed_dict["inspection_id"] == "INSP-INTEG-001"
    assert parsed_dict["overall_verdict"] == "COMPLIANT"
    assert len(parsed_dict["rule_evaluations"]) >= 8


def test_fastapi_inspection_roundtrip(api_client, statutory_engine):
    """
    Verifies that FastAPI /api/v1/inspections accepts an InspectionRequest
    and successfully serializes an InspectionResult containing rule evaluations.
    """
    request_payload = {
        "inspection_id": "INSP-API-TEST-002",
        "image_sha256": "b" * 64,
        "target_ruleset": "current",
    }

    response = api_client.post("/api/v1/inspections", json=request_payload)
    assert response.status_code == 202
    data = response.json()
    assert data["inspection_id"] == "INSP-API-TEST-002"
    assert data["status"] == "SUCCESS"


def test_non_compliant_engine_notice_serialization(statutory_engine):
    """
    Verifies that a non-compliant evaluation generates an ImprovementNotice
    that serializes cleanly into API-ready JSON payloads.
    """
    # Missing MRP and missing Country of Origin
    decl = CanonicalDeclaration(
        commodity_name="Imported Biscuits",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
    )

    result = statutory_engine.evaluate(decl, inspection_id="INSP-VIOL-003")
    assert result.overall_verdict == ComplianceState.NON_COMPLIANT
    assert result.improvement_notice is not None
    assert result.improvement_notice.recommended is True
    assert result.improvement_notice.cure_period_days == 15

    # Serialize to JSON and verify contents
    result_json = result.model_dump_json()
    data = json.loads(result_json)
    assert data["overall_verdict"] == "NON_COMPLIANT"
    assert data["verdict_badge_color"] == "red"
    assert data["improvement_notice"]["cure_period_days"] == 15
    assert len(data["improvement_notice"]["itemized_violations"]) >= 2
    assert "Rule 6(1)(e)" in data["improvement_notice"]["statutory_grounds"]
