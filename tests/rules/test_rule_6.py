"""
Tests for Rule 6 mandatory declarations completeness under Legal Metrology (Packaged Commodities) Rules, 2011.
Verifies Gate 3 / CP-3 evaluation of Rules 6(1)(a)-(g).
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


def test_rule_6_all_mandatory_declarations_pass(engine):
    """Verify that a declaration containing all 8 mandatory declarations passes Rule 6."""
    decl = CanonicalDeclaration(
        commodity_name="Roasted Almonds",
        manufacturer_name="DryFruit Hub Ltd, Delhi 110001",
        manufacturer_pincode="110001",
        country_of_origin="India",
        net_quantity_value=250.0,
        net_quantity_unit=UnitType.GRAM,
        has_non_standard_unit=False,
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=300.0,
        tax_qualifier_present=True,
        consumer_care_email="support@dryfruit.com",
        consumer_care_phone="1800-11-2233",
        declared_usp_value=1.20,
        declared_usp_unit="g",
    )
    records = engine.evaluate_rule_6(decl)
    assert len(records) == 7
    assert all(r.is_compliant for r in records)
    assert all(r.status == "PASS" for r in records)

    result = engine.evaluate(decl)
    assert result.overall_verdict == ComplianceState.COMPLIANT
    assert result.verdict_badge_color == "green"


def test_rule_6_1_e_missing_tax_qualifier_fails(engine):
    """Verify that omitting 'inclusive of all taxes' causes Rule 6(1)(e) to fail."""
    decl = CanonicalDeclaration(
        commodity_name="Potato Chips",
        manufacturer_name="SnackCo Ltd",
        country_of_origin="India",
        net_quantity_value=50.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=5,
        mfg_year=2026,
        mrp_inr=20.0,
        tax_qualifier_present=False,  # VIOLATION
        consumer_care_phone="1800-00-1111",
    )
    records = engine.evaluate_rule_6(decl)
    mrp_rec = next(r for r in records if r.rule_id == "LMPC-R06-MRP-001")
    assert mrp_rec.is_compliant is False
    assert mrp_rec.status == "FAIL"
    assert "tax qualifier" in mrp_rec.notes.lower()

    result = engine.evaluate(decl)
    assert result.overall_verdict == ComplianceState.NON_COMPLIANT
    assert result.verdict_badge_color == "red"


def test_rule_6_1_c_non_standard_unit_symbol_fails(engine):
    """Verify that using non-standard unit symbols (e.g. Gms, Kgs, ML) triggers statutory failure."""
    decl = CanonicalDeclaration(
        commodity_name="Turmeric Powder",
        manufacturer_name="SpiceWorld Ltd",
        country_of_origin="India",
        net_quantity_value=500.0,
        net_quantity_unit=UnitType.GRAM,
        raw_net_quantity_unit="Gms",
        has_non_standard_unit=True,  # VIOLATION
        mfg_month=7,
        mfg_year=2026,
        mrp_inr=150.0,
        tax_qualifier_present=True,
        consumer_care_email="care@spiceworld.in",
    )
    records = engine.evaluate_rule_6(decl)
    qty_rec = next(r for r in records if r.rule_id == "LMPC-R06-QTY-001")
    assert qty_rec.is_compliant is False
    assert qty_rec.status == "FAIL"
    assert "Rule 13" in qty_rec.statutory_reference


def test_rule_6_1_a_missing_manufacturer_fails(engine):
    """Verify that omitting manufacturer name causes Rule 6(1)(a) failure."""
    decl = CanonicalDeclaration(
        commodity_name="Biscuits",
        manufacturer_name=None,  # VIOLATION
        country_of_origin="India",
        net_quantity_value=100.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=8,
        mfg_year=2026,
        mrp_inr=30.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-22-3344",
    )
    records = engine.evaluate_rule_6(decl)
    mfr_rec = next(r for r in records if r.rule_id == "LMPC-R06-MFR-001")
    assert mfr_rec.is_compliant is False
    assert mfr_rec.status == "FAIL"


def test_rule_6_1_aa_missing_country_of_origin_fails(engine):
    """Verify that omitting country of origin causes Rule 6(1)(aa) failure."""
    decl = CanonicalDeclaration(
        commodity_name="Dark Chocolate",
        manufacturer_name="ChocoCraft Ltd",
        country_of_origin=None,  # VIOLATION
        net_quantity_value=80.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=6,
        mfg_year=2026,
        mrp_inr=120.0,
        tax_qualifier_present=True,
        consumer_care_email="help@chococraft.in",
    )
    records = engine.evaluate_rule_6(decl)
    coo_rec = next(r for r in records if r.rule_id == "LMPC-R06-COO-001")
    assert coo_rec.is_compliant is False
    assert coo_rec.status == "FAIL"
    assert "G.S.R. 629(E)" in coo_rec.statutory_citation


def test_rule_6_1_d_missing_mfg_date_fails(engine):
    """Verify that omitting month and year of manufacture causes Rule 6(1)(d) failure."""
    decl = CanonicalDeclaration(
        commodity_name="Green Tea",
        manufacturer_name="TeaEstate Ltd",
        country_of_origin="India",
        net_quantity_value=100.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=None,  # VIOLATION
        mfg_year=None,
        mrp_inr=250.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-44-5566",
    )
    records = engine.evaluate_rule_6(decl)
    date_rec = next(r for r in records if r.rule_id == "LMPC-R06-DATE-001")
    assert date_rec.is_compliant is False
    assert date_rec.status == "FAIL"


def test_rule_6_1_g_missing_consumer_care_fails(engine):
    """Verify that omitting both email and telephone causes Rule 6(1)(g) failure."""
    decl = CanonicalDeclaration(
        commodity_name="Detergent Powder",
        manufacturer_name="CleanCo Ltd",
        country_of_origin="India",
        net_quantity_value=1.0,
        net_quantity_unit=UnitType.KILOGRAM,
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=90.0,
        tax_qualifier_present=True,
        consumer_care_phone=None,  # VIOLATION
        consumer_care_email=None,  # VIOLATION
    )
    records = engine.evaluate_rule_6(decl)
    care_rec = next(r for r in records if r.rule_id == "LMPC-R06-CARE-001")
    assert care_rec.is_compliant is False
    assert care_rec.status == "FAIL"
