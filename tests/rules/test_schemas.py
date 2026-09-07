"""
Tests for canonical Pydantic schemas in nirikshak_rules_engine.
Verifies Gate 1 / CP-1 schema freezing, field validation, and JSON serialization.
"""

import json
import pytest
from pydantic import ValidationError

from nirikshak_rules_engine.schemas import (
    ComplianceState,
    VerdictBadgeColor,
    UnitType,
    ScriptType,
    OCRToken,
    MetricScaleResult,
    CanonicalDeclaration,
    RuleEvaluationRecord,
    EvidenceCropMetadata,
    ImprovementNoticePayload,
    ComplianceEvaluationResult,
)


def test_compliance_state_values():
    """Verify that ComplianceState contains all frozen values from API_CONTRACT.md and 5-State taxonomy."""
    assert ComplianceState.GREEN == "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED"
    assert ComplianceState.RED == "POTENTIAL_NON_COMPLIANCE"
    assert ComplianceState.AMBER == "MANUAL_REVIEW_REQUIRED"
    assert ComplianceState.BLUE == "STATUTORY_EXEMPTION_APPLIED"
    assert ComplianceState.GRAY == "NOT_IMAGE_VERIFIABLE"
    
    # 5-State taxonomy aliases
    assert ComplianceState.COMPLIANT == "COMPLIANT"
    assert ComplianceState.NON_COMPLIANT == "NON_COMPLIANT"
    assert ComplianceState.DEVIATION_DETECTED == "DEVIATION_DETECTED"
    assert ComplianceState.UNCERTAIN == "UNCERTAIN"
    assert ComplianceState.EXEMPTED == "EXEMPTED"


def test_unit_type_normalization():
    """Verify UnitType standard statutory SI units and string normalization."""
    assert UnitType.GRAM == "g"
    assert UnitType.KILOGRAM == "kg"
    assert UnitType.MILLILITER == "ml"
    assert UnitType.LITER == "l"
    assert UnitType.METER == "m"
    assert UnitType.CENTIMETER == "cm"
    assert UnitType.NUMBER == "N"
    assert UnitType.PIECE == "piece"

    assert UnitType.from_string("g") == UnitType.GRAM
    assert UnitType.from_string("grams") == UnitType.GRAM
    assert UnitType.from_string("kg") == UnitType.KILOGRAM
    assert UnitType.from_string("ml") == UnitType.MILLILITER
    assert UnitType.from_string("L") == UnitType.LITER
    assert UnitType.from_string("pcs") == UnitType.PIECE
    assert UnitType.from_string("unknown_unit") is None


def test_ocr_token_model():
    """Verify OCRToken initialization, validation, and serialization."""
    token = OCRToken(
        token_id="tok_001",
        text="MRP ₹250.00",
        confidence=0.98,
        bbox=[100.0, 200.0, 350.0, 240.0],
        script=ScriptType.LATIN,
        char_height_px=22.5,
    )
    assert token.token_id == "tok_001"
    assert token.confidence == 0.98
    assert token.bbox == [100.0, 200.0, 350.0, 240.0]

    # Test confidence bounds
    with pytest.raises(ValidationError):
        OCRToken(
            token_id="tok_err",
            text="invalid",
            confidence=1.5,
            bbox=[0, 0, 10, 10],
        )


def test_metric_scale_result_defaults():
    """Verify MetricScaleResult default values."""
    res = MetricScaleResult()
    assert res.is_calibrated is False
    assert res.scale_factor_mm_per_px is None
    assert res.pdp_area_sqcm is None
    assert res.anchor_type_detected == "none"
    assert res.is_cylindrical is False


def test_canonical_declaration_serialization():
    """Verify CanonicalDeclaration serialization and field typing."""
    decl = CanonicalDeclaration(
        commodity_name="Premium Roasted Cashews",
        mrp_inr=240.0,
        tax_qualifier_present=True,
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        declared_usp_value=1.20,
        declared_usp_unit="g",
        mfg_month=8,
        mfg_year=2026,
        manufacturer_name="MetroLens Foods Pvt Ltd",
        manufacturer_pincode="110001",
        consumer_care_email="support@metrolens.in",
        consumer_care_phone="1800-11-4000",
        country_of_origin="India",
        is_pan_masala_or_tobacco=False,
        is_wholesale_or_bulk=False,
    )

    data = decl.model_dump(mode="json")
    assert data["commodity_name"] == "Premium Roasted Cashews"
    assert data["mrp_inr"] == 240.0
    assert data["net_quantity_unit"] == "g"
    assert data["mfg_month"] == 8
    assert data["mfg_year"] == 2026

    # Roundtrip validation
    reconstructed = CanonicalDeclaration.model_validate(data)
    assert reconstructed.commodity_name == decl.commodity_name
    assert reconstructed.net_quantity_unit == UnitType.GRAM


def test_rule_evaluation_record():
    """Verify RuleEvaluationRecord validation."""
    record = RuleEvaluationRecord(
        rule_id="LMPC-R06-MRP-001",
        rule_title="MRP Declaration Presence",
        statutory_reference="Rule 6(1)(e)",
        status="PASS",
        is_compliant=True,
        observed_value="MRP Rs. 240.00",
        required_value="MRP inclusive of all taxes",
        statutory_citation="Rule 6(1)(e) of Legal Metrology (Packaged Commodities) Rules, 2011",
        notes="Compliant MRP declaration detected.",
        benefit_of_doubt_applied=False,
    )
    assert record.is_compliant is True
    assert record.status == "PASS"


def test_improvement_notice_payload():
    """Verify ImprovementNoticePayload strictly adheres to Jan Vishwas Act 2026 and lacks criminal terms."""
    notice = ImprovementNoticePayload(
        recommended=True,
        act_provision="Section 36(1) read with Jan Vishwas (Amendment of Provisions) Act, 2026",
        cure_period_days=15,
        statutory_grounds="Violation of Rule 6(11): Discrepancy in declared Unit Sale Price.",
    )
    assert notice.recommended is True
    assert notice.cure_period_days == 15
    notice_str = json.dumps(notice.model_dump())
    assert "imprisonment" not in notice_str.lower()
    assert "jail" not in notice_str.lower()


def test_compliance_evaluation_result_roundtrip():
    """Verify full master ComplianceEvaluationResult object serialization and schema stability."""
    decl = CanonicalDeclaration(
        commodity_name="Roasted Almonds",
        mrp_inr=150.0,
        net_quantity_value=100.0,
        net_quantity_unit=UnitType.GRAM,
    )
    scale = MetricScaleResult(
        is_calibrated=True,
        scale_factor_mm_per_px=0.08,
        pdp_area_sqcm=120.0,
        anchor_type_detected="coin_10rs",
    )
    rec = RuleEvaluationRecord(
        rule_id="LMPC-R06-MRP-001",
        rule_title="MRP Declaration",
        statutory_reference="Rule 6(1)(e)",
        status="PASS",
        is_compliant=True,
        statutory_citation="PCR 2011 Rule 6(1)(e)",
    )
    crop = EvidenceCropMetadata(
        field_name="mrp",
        label="MRP Declaration Crop",
        bbox_px=[50, 100, 200, 40],
        measured_height_mm=2.4,
        confidence=0.96,
        crop_base64="data:image/jpeg;base64,samplebase64",
    )
    notice = ImprovementNoticePayload(recommended=False)

    result = ComplianceEvaluationResult(
        inspection_id="INSP-20260905-001",
        timestamp_utc="2026-09-05T09:30:00Z",
        overall_verdict="COMPLIANT",
        verdict_badge_color="green",
        primary_legal_summary="All image-verifiable mandatory declarations compliant with PCR 2011.",
        rule_evaluations=[rec],
        declarations=decl,
        calibrated_measurements=scale,
        evidence_crops=[crop],
        improvement_notice=notice,
        sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        pdf_report_url="/reports/INSP-20260905-001.pdf",
        telemetry_ms=8.5,
    )

    data = result.model_dump(mode="json")
    assert data["inspection_id"] == "INSP-20260905-001"
    assert data["overall_verdict"] == "COMPLIANT"
    assert data["calibrated_measurements"]["pdp_area_sqcm"] == 120.0
    assert len(data["evidence_crops"]) == 1
    assert data["telemetry_ms"] == 8.5

    # Test deserialization
    reconstructed = ComplianceEvaluationResult.model_validate(data)
    assert reconstructed.inspection_id == result.inspection_id
    assert reconstructed.declarations.commodity_name == "Roasted Almonds"
    assert reconstructed.calibrated_measurements.scale_factor_mm_per_px == 0.08
