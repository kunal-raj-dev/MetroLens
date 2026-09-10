"""API integration checks with test-only OCR and quality outputs.

The guarded_api fixture exercises the real upload validator, calibration,
normalizer, rules engine, evidence store, and PDF renderer. These tests do not
measure real OCR accuracy, camera behavior, or deployed/browser performance.
The explicitly named quality component test runs the actual blur detector.
"""

import hashlib
import importlib
from types import SimpleNamespace

import cv2
import numpy as np
import pytest


def _pipeline_module():
    return importlib.import_module("apps.api.services.pipeline_orchestrator")


def test_api_001_upload_retrieve_and_report(guarded_api):
    data = guarded_api.upload()
    assert data["inspection_id"].startswith("INSP-")
    assert data["image_metadata"]["sha256_hash"] == hashlib.sha256(guarded_api.image_bytes).hexdigest()
    retained = guarded_api.client.get(f'/api/v1/inspections/{data["inspection_id"]}')
    assert retained.status_code == 200 and retained.json() == data
    report = guarded_api.client.post("/api/v1/report/pdf", json={"inspection_id": data["inspection_id"]})
    assert report.status_code == 200, report.text
    assert report.headers["content-type"] == "application/pdf"
    assert report.content.startswith(b"%PDF-") and len(report.content) > 1000
    audit = guarded_api.client.get(f'/api/v1/audit/verify/{data["inspection_id"]}')
    assert audit.status_code == 200 and audit.json()["status"] == "LOCAL_HASHES_MATCH"


def test_api_002_invalid_image_has_no_assessment(guarded_api):
    response = guarded_api.client.post("/api/v1/inspect",
        files={"file": ("bad.jpg", b"NOT_A_REAL_IMAGE_DATA_HEADER", "image/jpeg")})
    assert response.status_code == 415
    assert "inspection_id" not in response.json()
    assert not list(guarded_api.spool.base_dir.iterdir())


def test_component_003_severe_blur_detector():
    from nirikshak_vision import evaluate_image_quality
    image = np.full((800, 1000, 3), 180, dtype=np.uint8)
    cv2.putText(image, "PACKAGING TEXT", (80, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
    blurred = cv2.GaussianBlur(image, (51, 51), 0)
    result = evaluate_image_quality(blurred)
    assert result.passed is False
    assert result.is_blurry is True


def test_api_003_quality_rejection_stops_before_ocr(guarded_api, monkeypatch):
    module = _pipeline_module()
    monkeypatch.setattr(module, "check_image_quality", lambda image: SimpleNamespace(
        passed=False, laplacian_variance=0.0, glare_ratio=0.0))
    monkeypatch.setattr(module.pipeline_orchestrator, "_get_ocr_service",
                        lambda: pytest.fail("Rejected image must not invoke OCR"))
    response = guarded_api.client.post("/api/v1/inspect",
        files={"file": ("blurred.png", guarded_api.image_bytes, "image/png")})
    assert response.status_code == 422
    assert not list(guarded_api.spool.base_dir.iterdir())


def test_api_004_uncalibrated_image_has_no_physical_measurements(guarded_api):
    data = guarded_api.upload()
    assert data["calibration"]["is_calibrated"] is False
    assert data["calibration"]["scale_mm_per_px"] is None
    assert data["calibration"]["pdp_area_cm2"] is None
    assert data["rule_evaluations"]["font_height_audit"]["measured_net_qty_height_mm"] is None


def test_api_005_injected_ocr_geometry_is_preserved(guarded_api):
    tokens = guarded_api.set_tokens()
    data = guarded_api.upload()
    observed = {item["token_id"]: item for item in data["ocr_observations"]}
    assert set(observed) == {token.token_id for token in tokens}
    for token in tokens:
        assert observed[token.token_id]["text"] == token.text
        box = observed[token.token_id]["bounding_box"]
        assert [box[key] for key in ("x_min", "y_min", "x_max", "y_max")] == token.bbox
    assert data["evidence_crops"]
    for crop in data["evidence_crops"]:
        assert crop["source_token_id"] in observed
        x, y, width, height = crop["bbox_px"]
        assert 0 <= x < x + width <= 800
        assert 0 <= y < y + height <= 600


def test_api_006_low_confidence_requires_review(guarded_api):
    tokens = guarded_api.set_tokens()
    tokens[0].confidence = 0.45
    data = guarded_api.upload()
    assert data["state"] == "MANUAL_REVIEW_REQUIRED"
    assert data["rule_evaluations"]["usp_audit"]["status"] == "REVIEW"
    assert data["improvement_notice"] is None


def test_api_007_declarations_come_from_injected_tokens(guarded_api):
    declarations = guarded_api.upload()["declarations"]
    assert declarations["commodity_name"] == "Premium Roasted Cashews"
    assert declarations["mrp_inr"] == 240.0
    assert declarations["net_quantity_value"] == 200.0
    assert declarations["net_quantity_unit"] == "g"
    assert declarations["tax_qualifier_present"] is True


def test_api_008_present_declarations_do_not_resolve_missing_metrology(guarded_api):
    data = guarded_api.upload()
    rules = data["rule_evaluations"]
    assert rules["rule6_mandatory_status"]["overall_status"] == "PASS"
    assert rules["font_height_audit"]["status"] == "REVIEW"
    assert data["state"] in {"UNCERTAIN", "MANUAL_REVIEW_REQUIRED"}


def test_api_009_single_panel_deficit_does_not_issue_notice(guarded_api):
    guarded_api.set_tokens("PKG-03-MISSING-TAX-QUALIFIER")
    data = guarded_api.upload()
    assert data["declarations"]["tax_qualifier_present"] is False
    assert data["state"] == "POTENTIAL_NON_COMPLIANCE"
    assert data["improvement_notice"] is None
    assert "panel" in data["summary_reason"].lower()


def test_component_010_known_scale_with_unknown_area_requires_review():
    from nirikshak_rules_engine import CanonicalDeclaration, MetricScaleResult, StatutoryRuleEngine, UnitType
    declaration = CanonicalDeclaration(
        commodity_name="Cookies", net_quantity_value=100.0, net_quantity_unit=UnitType.GRAM,
        mrp_inr=30.0, tax_qualifier_present=True, declared_usp_value=0.30, declared_usp_unit="g",
        mfg_month=6, mfg_year=2026, manufacturer_name="Bakery Ltd", country_of_origin="India",
        consumer_care_email="care@bakery.com")
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.1, pdp_area_sqcm=None)
    result = StatutoryRuleEngine().evaluate(decl=declaration, scale=scale,
        inspection_id="INSP-REVIEW", measured_font_height_mm=1.5)
    font = next(rule for rule in result.rule_evaluations if rule.rule_id == "LMPC-R07-FONT-001")
    assert font.status == "REVIEW"
    assert result.overall_verdict == "UNCERTAIN"


def test_api_011_hindi_observations_preserve_unicode(guarded_api):
    tokens = guarded_api.set_tokens("PKG-02-BILINGUAL-HINDI-ATTA")
    data = guarded_api.upload()
    expected = [token.text for token in tokens if any(0x900 <= ord(char) <= 0x97f for char in token.text)]
    assert expected
    observed = [item["text"] for item in data["ocr_observations"]]
    assert all(text in observed for text in expected)
    assert data["declarations"]["mrp_inr"] == 45.0
    assert data["rule_evaluations"]["font_height_audit"]["status"] == "REVIEW"


def test_api_012_unit_price_arithmetic_uses_observed_values(guarded_api):
    data = guarded_api.upload()
    assert data["declarations"]["mrp_inr"] == 240.0
    assert data["declarations"]["net_quantity_value"] == 200.0
    audit = data["rule_evaluations"]["usp_audit"]
    assert audit["declared_usp"] == audit["expected_usp"] == 1.2
    assert audit["status"] == "PASS"


def test_api_013_http_fixture_override_is_rejected(guarded_api):
    response = guarded_api.client.post("/api/v1/inspect",
        files={"file": ("sample.png", guarded_api.image_bytes, "image/png")},
        data={"mock_fixture_key": "PKG-01-COMPLIANT-FMCG-CASHEWS"})
    assert response.status_code == 400
    assert "inspection_id" not in response.json()
    assert not list(guarded_api.spool.base_dir.iterdir())


def test_api_014_successive_inspections_keep_independent_results(guarded_api):
    first = guarded_api.upload()
    guarded_api.set_tokens("PKG-02-BILINGUAL-HINDI-ATTA")
    second = guarded_api.upload()
    assert first["inspection_id"] != second["inspection_id"]
    assert first["declarations"]["mrp_inr"] == 240.0
    assert second["declarations"]["mrp_inr"] == 45.0
    for expected in (first, second):
        response = guarded_api.client.get(f'/api/v1/inspections/{expected["inspection_id"]}')
        assert response.status_code == 200 and response.json() == expected


def test_api_015_ocr_unavailable_is_technical_failure(guarded_api, monkeypatch):
    monkeypatch.setattr(_pipeline_module().pipeline_orchestrator, "_get_ocr_service", lambda: None)
    response = guarded_api.client.post("/api/v1/inspect",
        files={"file": ("sample.png", guarded_api.image_bytes, "image/png")})
    assert response.status_code == 503
    assert "inspection_id" not in response.json()
    assert "state" not in response.json()
    assert not list(guarded_api.spool.base_dir.iterdir())


def test_api_015_oversized_image_is_not_a_legal_verdict(guarded_api):
    response = guarded_api.client.post("/api/v1/inspect",
        files={"file": ("huge.jpg", b"x" * (15 * 1024 * 1024 + 1), "image/jpeg")})
    assert response.status_code == 413
    assert "inspection_id" not in response.json()
    assert "state" not in response.json()
    assert not list(guarded_api.spool.base_dir.iterdir())
