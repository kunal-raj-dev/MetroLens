"""Unmeasured geometry and unverified historical applicability stay uncertain."""

import pytest

from nirikshak_rules_engine import CanonicalDeclaration, MetricScaleResult, StatutoryRuleEngine, UnitType


@pytest.fixture
def declaration():
    return CanonicalDeclaration(
        commodity_name="Cashews", manufacturer_name="Example Foods Ltd",
        country_of_origin="India", net_quantity_value=200, net_quantity_unit=UnitType.GRAM,
        mfg_month=6, mfg_year=2026, mrp_inr=240, tax_qualifier_present=True,
        consumer_care_phone="1800-11-2233", declared_usp_value=1.2, declared_usp_unit="g",
    )


@pytest.mark.parametrize("scale,height", [
    (None, None),
    (MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05), 1.6),
    (MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80), None),
])
def test_missing_measurement_never_produces_overall_compliant(declaration, scale, height):
    result = StatutoryRuleEngine().evaluate(declaration, scale=scale, measured_font_height_mm=height)
    font = next(record for record in result.rule_evaluations if record.rule_id == "LMPC-R07-FONT-001")
    assert font.status == "REVIEW"
    assert result.overall_verdict == "UNCERTAIN"
    assert result.verdict_badge_color == "amber"
    assert not result.improvement_notice.recommended


def test_established_failure_is_not_hidden_by_unmeasured_font(declaration):
    declaration.declared_usp_value = 2.0
    result = StatutoryRuleEngine().evaluate(declaration)
    assert result.overall_verdict == "NON_COMPLIANT"
    assert result.improvement_notice.recommended


@pytest.mark.parametrize("height,expected", [(1.3, "DEVIATION_DETECTED"), (1.6, "COMPLIANT")])
def test_measured_font_keeps_existing_deficit_and_pass_semantics(declaration, height, expected):
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80)
    result = StatutoryRuleEngine().evaluate(declaration, scale=scale, measured_font_height_mm=height)
    assert result.overall_verdict == expected


@pytest.mark.parametrize("year,month", [(2015, 6), (2021, 11), (2022, 11), (2022, None)])
def test_unverified_historical_usp_is_review_not_a_modern_violation(declaration, year, month):
    declaration.mfg_year = year
    declaration.mfg_month = month
    declaration.declared_usp_value = None
    declaration.declared_usp_unit = None
    record = StatutoryRuleEngine().evaluate_usp(declaration)
    assert record.status == "REVIEW"
    assert record.is_compliant is False
    assert "historical" in record.notes.lower()


def test_historical_usp_does_not_create_an_improvement_notice(declaration):
    declaration.mfg_year = 2015
    declaration.declared_usp_value = None
    declaration.declared_usp_unit = None
    result = StatutoryRuleEngine().evaluate(declaration)
    assert result.overall_verdict == "UNCERTAIN"
    assert not result.improvement_notice.recommended


def test_current_usp_check_is_still_evaluated(declaration):
    declaration.declared_usp_value = None
    declaration.declared_usp_unit = None
    assert StatutoryRuleEngine().evaluate_usp(declaration).status == "FAIL"
