"""
Unit tests for nirikshak-shared contracts and models.
Verifies serialization, deserialization, and schema compliance with rules/schema/evidence.schema.json.
"""

import json
from pathlib import Path
import pytest
import jsonschema

from nirikshak_shared.models.primitives import (
    BoundingBox,
    CalibrationStatus,
    PanelName,
    RuleVerdict,
    OverallVerdict,
    InspectionStatus,
    ObservedValue,
)
from nirikshak_shared.models.contracts import (
    InspectionRequest,
    InspectionResult,
    OCRObservation,
    DeclarationField,
    MeasurementResult,
    RuleEvaluation,
    EvidenceItem,
    InspectionError,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
EVIDENCE_SCHEMA_PATH = REPO_ROOT / "rules" / "schema" / "evidence.schema.json"


def test_ocr_observation_roundtrip():
    obs = OCRObservation(
        token_id="tok_001",
        text="MRP Rs. 250.00",
        confidence=0.98,
        bounding_box=BoundingBox(x_min=10.0, y_min=20.0, x_max=150.0, y_max=45.0),
        language="en",
    )
    data = obs.model_dump()
    reconstructed = OCRObservation.model_validate(data)
    assert reconstructed.token_id == "tok_001"
    assert reconstructed.text == "MRP Rs. 250.00"
    assert reconstructed.confidence == 0.98


def test_declaration_field_mapping():
    decl = DeclarationField(
        field_name="mrp",
        raw_text="MRP Rs. 250.00 (incl. of all taxes)",
        normalized_value={"amount": 250.00, "currency": "INR"},
        confidence=0.96,
        source_token_ids=["tok_001", "tok_002"],
        is_mandatory=True,
        is_present=True,
    )
    assert decl.field_name == "mrp"
    assert decl.normalized_value["amount"] == 250.00


def test_measurement_result():
    meas = MeasurementResult(
        feature_name="numeral_height_mm",
        measured_pixels=48.0,
        scale_factor_mm_per_pixel=0.0625,
        measured_mm=3.0,
        uncertainty_mm=0.15,
        calibration_status=CalibrationStatus.CALIBRATED,
    )
    assert meas.measured_mm == 3.0
    assert meas.calibration_status == CalibrationStatus.CALIBRATED


def test_evidence_item_schema_conformance():
    """Validates that EvidenceItem produces JSON strictly valid against rules/schema/evidence.schema.json."""
    assert EVIDENCE_SCHEMA_PATH.exists(), f"Missing schema at {EVIDENCE_SCHEMA_PATH}"

    with open(EVIDENCE_SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    dummy_sha256 = "a" * 64
    evidence = EvidenceItem(
        evidence_id="ev_pdp_crop_001",
        image_sha256=dummy_sha256,
        panel_name=PanelName.PRINCIPAL_DISPLAY_PANEL,
        bounding_box=BoundingBox(x_min=100.0, y_min=100.0, x_max=600.0, y_max=800.0),
        calibration_status=CalibrationStatus.CALIBRATED,
        physical_scale_mm_per_pixel=0.05,
        observed_value=ObservedValue(
            raw_text="Net Qty: 500 g",
            normalized_value="500 g",
            measured_font_height_mm=2.5,
            measured_pdp_area_cm2=150.0,
            ocr_confidence=0.97,
        ),
    )

    ev_json = evidence.to_schema_dict()
    # This must not raise any ValidationError
    jsonschema.validate(instance=ev_json, schema=schema)


def test_inspection_result_composite():
    dummy_sha = "b" * 64
    result = InspectionResult(
        inspection_id="insp_20260905_001",
        status=InspectionStatus.SUCCESS,
        image_sha256=dummy_sha,
        overall_verdict=OverallVerdict.COMPLIANT,
        quality_gate_passed=True,
        calibration_status=CalibrationStatus.CALIBRATED,
        declarations={
            "mrp": DeclarationField(
                field_name="mrp",
                raw_text="MRP 100.00",
                confidence=0.99,
            )
        },
        measurements={
            "font_height": MeasurementResult(
                feature_name="font_height",
                measured_pixels=40.0,
                measured_mm=2.0,
                calibration_status=CalibrationStatus.CALIBRATED,
            )
        },
        rule_evaluations=[
            RuleEvaluation(
                rule_id="LMPC-R06-MRP-001",
                rule_title="MRP Declaration Present",
                verdict=RuleVerdict.PASS,
                statutory_reference="Rule 6(1)(e)",
                observed_summary="MRP Rs. 100 present",
                required_summary="MRP must be declared inclusive of all taxes",
            )
        ],
        evidence_chain=[
            EvidenceItem(
                evidence_id="ev_001",
                image_sha256=dummy_sha,
                panel_name=PanelName.PRINCIPAL_DISPLAY_PANEL,
                bounding_box=BoundingBox(x_min=10.0, y_min=10.0, x_max=100.0, y_max=50.0),
                calibration_status=CalibrationStatus.CALIBRATED,
                observed_value=ObservedValue(raw_text="MRP 100.00"),
            )
        ],
        errors=[],
    )

    data = result.model_dump()
    assert data["inspection_id"] == "insp_20260905_001"
    assert data["overall_verdict"] == "COMPLIANT"
    assert len(data["rule_evaluations"]) == 1
