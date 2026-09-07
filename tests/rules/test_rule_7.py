"""
Tests for Rule 7 Tables I & II Numeral/Letter Height Matrix and 5-State Taxonomy.
Verifies Gate 5 / CP-5 compliance under G.S.R. 629(E) and G.S.R. 1373(E).
Validates PDP area brackets, Table-I vs Table-II routing, 0.10mm benefit-of-doubt buffer,
and 5-State classification aggregator.
"""

import pytest
from nirikshak_rules_engine import (
    StatutoryRuleEngine,
    FontMatrixValidator,
    CanonicalDeclaration,
    MetricScaleResult,
    UnitType,
    ComplianceState,
)


@pytest.fixture
def engine():
    return StatutoryRuleEngine()


@pytest.fixture
def validator():
    return FontMatrixValidator()


# ---------------------------------------------------------------------------
# 1. Table-I (Weight / Volume) Area Brackets
# ---------------------------------------------------------------------------

def test_rule_7_table_1_tier_under_50_sqcm(validator):
    """PDP Area <= 50 cm²: Normal min 1.0mm, Blown min 1.5mm."""
    decl = CanonicalDeclaration(net_quantity_value=20.0, net_quantity_unit=UnitType.GRAM)
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=45.0)

    # Normal packaging: 1.1mm >= 1.0mm -> PASS
    rec_pass = validator.evaluate(decl, scale, measured_height_mm=1.1, is_blown_or_formed=False)
    assert rec_pass.status == "PASS"
    assert rec_pass.is_compliant is True
    assert "1.0 mm" in rec_pass.required_value

    # Blown packaging: 1.2mm < 1.5mm (fails even with 0.10mm buffer -> 1.30 < 1.50)
    rec_fail = validator.evaluate(decl, scale, measured_height_mm=1.2, is_blown_or_formed=True)
    assert rec_fail.is_compliant is False
    assert "1.5 mm" in rec_fail.required_value


def test_rule_7_table_1_tier_50_to_100_sqcm(validator):
    """50 < PDP Area <= 100 cm²: Normal min 1.5mm, Blown min 3.0mm."""
    decl = CanonicalDeclaration(net_quantity_value=200.0, net_quantity_unit=UnitType.GRAM)
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)

    rec = validator.evaluate(decl, scale, measured_height_mm=1.60, is_blown_or_formed=False)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert "1.5 mm" in rec.required_value


def test_rule_7_table_1_tier_100_to_500_sqcm(validator):
    """100 < PDP Area <= 500 cm²: Normal min 2.5mm, Blown min 4.0mm."""
    decl = CanonicalDeclaration(net_quantity_value=1.0, net_quantity_unit=UnitType.KILOGRAM)
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=250.0)

    rec = validator.evaluate(decl, scale, measured_height_mm=2.60, is_blown_or_formed=False)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert "2.5 mm" in rec.required_value


def test_rule_7_table_1_tier_500_to_2500_sqcm(validator):
    """500 < PDP Area <= 2500 cm²: Normal min 4.0mm, Blown min 6.0mm."""
    decl = CanonicalDeclaration(net_quantity_value=5.0, net_quantity_unit=UnitType.KILOGRAM)
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=800.0)

    rec = validator.evaluate(decl, scale, measured_height_mm=4.20, is_blown_or_formed=False)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert "4.0 mm" in rec.required_value


def test_rule_7_table_1_tier_over_2500_sqcm(validator):
    """PDP Area > 2500 cm²: Normal min 6.0mm, Blown min 6.0mm."""
    decl = CanonicalDeclaration(net_quantity_value=20.0, net_quantity_unit=UnitType.KILOGRAM)
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=3000.0)

    rec = validator.evaluate(decl, scale, measured_height_mm=6.20, is_blown_or_formed=False)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert "6.0 mm" in rec.required_value


# ---------------------------------------------------------------------------
# 2. Table-II (Length, Area, Count / Number) Area Brackets
# ---------------------------------------------------------------------------

def test_rule_7_table_2_count_under_100_sqcm(validator):
    """Table-II: PDP Area <= 100 cm²: Normal min 1.0mm, Blown min 2.0mm."""
    decl = CanonicalDeclaration(net_quantity_value=10.0, net_quantity_unit=UnitType.PIECE)
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=60.0)

    rec = validator.evaluate(decl, scale, measured_height_mm=1.20, is_blown_or_formed=False)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert "Table-II" in rec.notes
    assert "1.0 mm" in rec.required_value


def test_rule_7_table_2_length_100_to_500_sqcm(validator):
    """Table-II: 100 < PDP Area <= 500 cm²: Normal min 2.0mm, Blown min 4.0mm."""
    decl = CanonicalDeclaration(net_quantity_value=5.0, net_quantity_unit=UnitType.METER)
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=200.0)

    rec = validator.evaluate(decl, scale, measured_height_mm=2.10, is_blown_or_formed=False)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert "2.0 mm" in rec.required_value


# ---------------------------------------------------------------------------
# 3. Benefit-of-Doubt Tolerance Buffer (0.10 mm)
# ---------------------------------------------------------------------------

def test_benefit_of_doubt_applied_for_marginal_measurement(validator):
    """
    Required height is 1.5mm. Measured height is 1.42mm.
    1.42 < 1.50, but 1.42 + 0.10 = 1.52 >= 1.50.
    Must evaluate to PASS with benefit_of_doubt_applied=True.
    """
    decl = CanonicalDeclaration(net_quantity_value=200.0, net_quantity_unit=UnitType.GRAM)
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)

    rec = validator.evaluate(decl, scale, measured_height_mm=1.42, is_blown_or_formed=False)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.benefit_of_doubt_applied is True
    assert "benefit-of-doubt" in rec.notes.lower()


def test_deficit_exceeding_benefit_of_doubt_fails(validator):
    """
    Required height is 1.5mm. Measured height is 0.90mm.
    Deficit is 0.60mm (exceeds 0.10mm buffer and 0.25mm uncertainty band).
    Must evaluate to FAIL with is_compliant=False.
    """
    decl = CanonicalDeclaration(net_quantity_value=200.0, net_quantity_unit=UnitType.GRAM)
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)

    rec = validator.evaluate(decl, scale, measured_height_mm=0.90, is_blown_or_formed=False)
    assert rec.status == "FAIL"
    assert rec.is_compliant is False
    assert rec.deficit_mm == 0.60
    assert "deficit" in rec.notes.lower()


# ---------------------------------------------------------------------------
# 4. Uncertainty & Calibration Edge Cases
# ---------------------------------------------------------------------------

def test_uncalibrated_scale_returns_review(validator):
    """When scale is not calibrated, numeral height cannot be asserted; status is REVIEW."""
    decl = CanonicalDeclaration(net_quantity_value=200.0, net_quantity_unit=UnitType.GRAM)
    scale = MetricScaleResult(is_calibrated=False, scale_factor_mm_per_px=None, pdp_area_sqcm=80.0)

    rec = validator.evaluate(decl, scale, measured_height_mm=1.20)
    assert rec.status == "REVIEW"
    assert "uncalibrated" in rec.notes.lower()


def test_unknown_pdp_area_returns_review(validator):
    """When PDP area is None, table bracket cannot be indexed; status is REVIEW."""
    decl = CanonicalDeclaration(net_quantity_value=200.0, net_quantity_unit=UnitType.GRAM)
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=None)

    rec = validator.evaluate(decl, scale, measured_height_mm=1.20)
    assert rec.status == "REVIEW"
    assert "pdp area" in rec.notes.lower()


# ---------------------------------------------------------------------------
# 5. Composite 5-State Taxonomy Adjudication
# ---------------------------------------------------------------------------

def test_composite_5_state_compliant(engine):
    """Verify that a package with valid declarations and compliant font height receives COMPLIANT (Green)."""
    decl = CanonicalDeclaration(
        commodity_name="Cashews",
        manufacturer_name="DryFruit Hub Ltd",
        country_of_origin="India",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=240.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-11-2233",
        declared_usp_value=1.20,
        declared_usp_unit="g",
    )
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)
    res = engine.evaluate(decl, scale=scale, measured_font_height_mm=1.60)
    assert res.overall_verdict == ComplianceState.COMPLIANT
    assert res.verdict_badge_color == "green"


def test_composite_5_state_non_compliant(engine):
    """Verify that a package with font height deficit receives NON_COMPLIANT (Red)."""
    decl = CanonicalDeclaration(
        commodity_name="Cashews",
        manufacturer_name="DryFruit Hub Ltd",
        country_of_origin="India",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=240.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-11-2233",
        declared_usp_value=1.20,
        declared_usp_unit="g",
    )
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)
    # 0.80mm is severely below the 1.5mm requirement for 80 cm²
    res = engine.evaluate(decl, scale=scale, measured_font_height_mm=0.80)
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    assert res.verdict_badge_color == "red"


def test_composite_5_state_deviation_detected(engine):
    """Verify that a package with borderline font height receives DEVIATION_DETECTED (Amber)."""
    decl = CanonicalDeclaration(
        commodity_name="Cashews",
        manufacturer_name="DryFruit Hub Ltd",
        country_of_origin="India",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=240.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-11-2233",
        declared_usp_value=1.20,
        declared_usp_unit="g",
    )
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)
    # Required is 1.5mm. With 0.10mm buffer, 1.40mm passes.
    # At 1.30mm, deficit is 0.20mm (within uncertainty band of 0.25mm) -> REVIEW
    res = engine.evaluate(decl, scale=scale, measured_font_height_mm=1.30)
    assert res.overall_verdict == ComplianceState.DEVIATION_DETECTED
    assert res.verdict_badge_color == "amber"


def test_composite_5_state_exempted(engine):
    """Verify that a wholesale package (>25kg) receives EXEMPTED (Blue)."""
    decl = CanonicalDeclaration(
        is_wholesale_or_bulk=True,
        net_quantity_value=50.0,
        net_quantity_unit=UnitType.KILOGRAM,
        mrp_inr=3000.0,
    )
    res = engine.evaluate(decl)
    assert res.overall_verdict == ComplianceState.EXEMPTED
    assert res.verdict_badge_color == "blue"
