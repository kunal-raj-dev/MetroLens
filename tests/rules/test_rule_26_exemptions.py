"""
Tests for Rule 3 Wholesale Scope Exclusions and Rule 26 Small Package Exemptions.
Includes strict validation of the G.S.R. 881(E) Pan Masala and Tobacco non-exemption carve-out.
"""

import pytest
from nirikshak_rules_engine import (
    StatutoryRuleEngine,
    CanonicalDeclaration,
    ComplianceState,
    UnitType,
)


@pytest.fixture
def engine():
    return StatutoryRuleEngine()


def test_rule_26_a_small_package_exemption_hotel_soap(engine):
    """
    Verify that general packages containing <= 10g/ml (e.g. hotel guest soap)
    are granted statutory exemption under Rule 26(a).
    """
    decl = CanonicalDeclaration(
        commodity_name="Hotel Guest Soap",
        net_quantity_value=8.0,
        net_quantity_unit=UnitType.GRAM,
        is_pan_masala_or_tobacco=False,
    )
    is_exempt, rec = engine.evaluate_exemptions(decl)
    assert is_exempt is True
    assert rec is not None
    assert rec.rule_id == "LMPC-R26-SMALL-PACK-EXEMPTION"
    assert rec.status == "NOT_APPLICABLE"
    assert "Rule 26(a)" in rec.statutory_reference

    result = engine.evaluate(decl)
    assert result.overall_verdict == ComplianceState.EXEMPTED
    assert result.verdict_badge_color == "blue"


def test_rule_26_gsr_881e_pan_masala_strictly_non_exempt(engine):
    """
    CRITICAL STATUTORY REQUIREMENT (G.S.R. 881(E) effective Feb 1, 2026):
    Pan masala sachets (<= 10g) are STRICTLY REVOKED from Rule 26(a) exemptions.
    System must deny exemption and enforce all mandatory retail declarations.
    """
    # Pan masala sachet of 4g with missing manufacturer & tax qualifier
    decl = CanonicalDeclaration(
        commodity_name="Royal Pan Masala",
        net_quantity_value=4.0,
        net_quantity_unit=UnitType.GRAM,
        is_pan_masala_or_tobacco=True,  # TRIGGER
        mrp_inr=5.0,
        tax_qualifier_present=False,  # VIOLATION
        manufacturer_name=None,  # VIOLATION
    )
    is_exempt, rec = engine.evaluate_exemptions(decl)
    # Exemption MUST BE DENIED
    assert is_exempt is False
    assert rec is not None
    assert rec.rule_id == "LMPC-R26-GSR881E-CARVEOUT"
    assert "G.S.R. 881(E)" in rec.statutory_citation

    # When evaluated, overall verdict must be NON_COMPLIANT due to missing declarations
    result = engine.evaluate(decl)
    assert result.overall_verdict == ComplianceState.NON_COMPLIANT
    assert result.verdict_badge_color == "red"
    assert any(r.rule_id == "LMPC-R26-GSR881E-CARVEOUT" for r in result.rule_evaluations)


def test_rule_26_tobacco_strictly_non_exempt(engine):
    """Verify that tobacco products are strictly non-exempt under Rule 26(a) proviso."""
    decl = CanonicalDeclaration(
        commodity_name="Chewing Tobacco",
        net_quantity_value=5.0,
        net_quantity_unit=UnitType.GRAM,
        is_pan_masala_or_tobacco=True,
        mrp_inr=10.0,
        tax_qualifier_present=True,
        manufacturer_name="TobaccoCo Ltd, Patna 800001",
        country_of_origin="India",
        mfg_month=8,
        mfg_year=2026,
        consumer_care_phone="1800-33-4455",
    )
    is_exempt, rec = engine.evaluate_exemptions(decl)
    assert is_exempt is False
    assert rec.rule_id == "LMPC-R26-GSR881E-CARVEOUT"

    result = engine.evaluate(decl)
    # If all declarations are present, it is COMPLIANT, but NOT EXEMPTED
    assert result.overall_verdict == ComplianceState.COMPLIANT
    assert result.verdict_badge_color == "green"


def test_rule_3_wholesale_bulk_exclusion_over_25kg(engine):
    """Verify that wholesale bulk commodities (> 25kg or > 25L) are excluded under Rule 3."""
    decl = CanonicalDeclaration(
        commodity_name="Whole Grain Wheat",
        net_quantity_value=30.0,
        net_quantity_unit=UnitType.KILOGRAM,
        is_wholesale_or_bulk=True,
    )
    is_exempt, rec = engine.evaluate_exemptions(decl)
    assert is_exempt is True
    assert rec.rule_id == "LMPC-R03-WHOLESALE-EXCLUSION"
    assert rec.status == "NOT_APPLICABLE"

    result = engine.evaluate(decl)
    assert result.overall_verdict == ComplianceState.EXEMPTED
    assert result.verdict_badge_color == "blue"


def test_rule_3_cement_up_to_50kg_exception(engine):
    """Verify that cement up to 50kg is an exception to the wholesale exclusion and remains governed."""
    decl = CanonicalDeclaration(
        commodity_name="Portland Pozzolana Cement",
        net_quantity_value=50.0,
        net_quantity_unit=UnitType.KILOGRAM,
        is_wholesale_or_bulk=True,  # Would normally be excluded, but cement is exception
        manufacturer_name="UltraCement Ltd",
        country_of_origin="India",
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=380.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-22-9900",
    )
    is_exempt, rec = engine.evaluate_exemptions(decl)
    # Cement is an exception, NOT excluded from mandatory declarations
    assert is_exempt is False
    result = engine.evaluate(decl)
    assert result.overall_verdict == ComplianceState.COMPLIANT
