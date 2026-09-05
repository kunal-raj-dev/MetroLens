"""
Tests for Rule 6(11) Unit Sale Price (USP) Statutory Mandate.
Verifies Gate 4 / CP-4 compliance under G.S.R. 779(E) and G.S.R. 226(E).
Validates statutory denominators, rounding to two decimal places, and statutory exemptions.
"""

import pytest
from nirikshak_rules_engine import (
    StatutoryRuleEngine,
    USPValidator,
    CanonicalDeclaration,
    UnitType,
    ComplianceState,
)


@pytest.fixture
def engine():
    return StatutoryRuleEngine()


@pytest.fixture
def validator():
    return USPValidator()


# ---------------------------------------------------------------------------
# 1. Statutory Denominator Tests: Weight
# ---------------------------------------------------------------------------

def test_usp_weight_under_1kg_per_gram_pass(validator):
    """Under Rule 6(11)(i), package < 1kg must declare USP per gram (₹/g)."""
    decl = CanonicalDeclaration(
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=240.0,
        declared_usp_value=1.20,
        declared_usp_unit="g",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.required_value == "₹ 1.20 / g"
    assert "Rule 6(11)" in rec.statutory_reference


def test_usp_weight_over_or_equal_1kg_per_kg_pass(validator):
    """Under Rule 6(11)(ii), package >= 1kg must declare USP per kilogram (₹/kg)."""
    decl = CanonicalDeclaration(
        net_quantity_value=2.0,
        net_quantity_unit=UnitType.KILOGRAM,
        mrp_inr=900.0,
        declared_usp_value=450.0,
        declared_usp_unit="kg",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.required_value == "₹ 450.00 / kg"


def test_usp_weight_under_1kg_wrong_denominator_fails(validator):
    """Package of 500g declaring per kg instead of per g must fail denominator check."""
    decl = CanonicalDeclaration(
        net_quantity_value=500.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=100.0,
        declared_usp_value=200.0,
        declared_usp_unit="kg",  # VIOLATION: Must be per gram under Rule 6(11)(i)
    )
    rec = validator.evaluate(decl)
    assert rec.status == "FAIL"
    assert rec.is_compliant is False
    assert "denomination violation" in rec.notes.lower()


def test_usp_weight_prohibited_100g_denominator_fails(validator):
    """Declaring USP per 100g violates G.S.R. 226(E) amended statutory requirements."""
    decl = CanonicalDeclaration(
        net_quantity_value=500.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=120.0,
        declared_usp_value=24.0,
        declared_usp_unit="100g",  # PROHIBITED DENOMINATOR
    )
    rec = validator.evaluate(decl)
    assert rec.status == "FAIL"
    assert rec.is_compliant is False
    assert "prohibited" in rec.notes.lower()


# ---------------------------------------------------------------------------
# 2. Statutory Denominator Tests: Volume
# ---------------------------------------------------------------------------

def test_usp_volume_under_1l_per_ml_pass(validator):
    """Under Rule 6(11)(iii), package < 1L must declare USP per millilitre (₹/ml)."""
    decl = CanonicalDeclaration(
        net_quantity_value=750.0,
        net_quantity_unit=UnitType.MILLILITER,
        mrp_inr=30.0,
        declared_usp_value=0.04,
        declared_usp_unit="ml",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.required_value == "₹ 0.04 / ml"


def test_usp_volume_over_or_equal_1l_per_litre_pass(validator):
    """Under Rule 6(11)(iv), package >= 1L must declare USP per litre (₹/L)."""
    decl = CanonicalDeclaration(
        net_quantity_value=2.0,
        net_quantity_unit=UnitType.LITER,
        mrp_inr=160.0,
        declared_usp_value=80.0,
        declared_usp_unit="l",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.required_value == "₹ 80.00 / l"


# ---------------------------------------------------------------------------
# 3. Statutory Denominator Tests: Length & Count
# ---------------------------------------------------------------------------

def test_usp_length_under_1m_per_cm_pass(validator):
    """Under Rule 6(11)(v), length < 1m must declare USP per centimetre (₹/cm)."""
    decl = CanonicalDeclaration(
        net_quantity_value=50.0,
        net_quantity_unit=UnitType.CENTIMETER,
        mrp_inr=25.0,
        declared_usp_value=0.50,
        declared_usp_unit="cm",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True


def test_usp_length_over_1m_per_metre_pass(validator):
    """Under Rule 6(11)(vi), length >= 1m must declare USP per metre (₹/m)."""
    decl = CanonicalDeclaration(
        net_quantity_value=5.0,
        net_quantity_unit=UnitType.METER,
        mrp_inr=200.0,
        declared_usp_value=40.0,
        declared_usp_unit="m",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True


def test_usp_count_per_piece_pass(validator):
    """Under Rule 6(11)(viii), count packages declare per number or per piece."""
    decl = CanonicalDeclaration(
        net_quantity_value=10.0,
        net_quantity_unit=UnitType.PIECE,
        mrp_inr=150.0,
        declared_usp_value=15.0,
        declared_usp_unit="piece",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True


# ---------------------------------------------------------------------------
# 4. Statutory Provisos & Exemptions
# ---------------------------------------------------------------------------

def test_usp_exemption_mrp_equals_usp_pass(validator):
    """Under Rule 6(11) proviso (c), package where MRP equals USP is exempt from separate USP declaration."""
    # 1 kg package at ₹45 -> USP = 45 / 1 = ₹45/kg == MRP
    decl = CanonicalDeclaration(
        net_quantity_value=1.0,
        net_quantity_unit=UnitType.KILOGRAM,
        mrp_inr=45.0,
        declared_usp_value=None,  # Not declared
        declared_usp_unit=None,
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert "proviso (c)" in rec.notes.lower()


def test_usp_exemption_small_pack_under_10g(validator):
    """Under Rule 6(11) proviso (a), net quantity < 10g or < 10ml is exempt from USP."""
    decl = CanonicalDeclaration(
        net_quantity_value=5.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=5.0,
        declared_usp_value=None,
    )
    rec = validator.evaluate(decl)
    assert rec.status == "NOT_APPLICABLE"
    assert rec.is_compliant is True
    assert "proviso (a)" in rec.notes.lower()


def test_usp_exemption_wholesale_bulk(validator):
    """Under Rule 6(11) proviso (b), wholesale packages are exempt from USP."""
    decl = CanonicalDeclaration(
        is_wholesale_or_bulk=True,
        net_quantity_value=30.0,
        net_quantity_unit=UnitType.KILOGRAM,
        mrp_inr=2500.0,
    )
    rec = validator.evaluate(decl)
    assert rec.status == "NOT_APPLICABLE"
    assert rec.is_compliant is True
    assert "proviso (b)" in rec.notes.lower()


# ---------------------------------------------------------------------------
# 5. Non-Compliance Violations
# ---------------------------------------------------------------------------

def test_usp_missing_declaration_fails(validator):
    """When net quantity > 10g and MRP != USP, missing USP declaration triggers statutory failure."""
    decl = CanonicalDeclaration(
        net_quantity_value=500.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=100.0,
        declared_usp_value=None,  # VIOLATION: Mandatory USP missing
    )
    rec = validator.evaluate(decl)
    assert rec.status == "FAIL"
    assert rec.is_compliant is False
    assert "mandatory unit sale price (usp) declaration missing" in rec.notes.lower()


def test_usp_arithmetic_mismatch_fails(validator):
    """Declared USP differing by more than 1.0% tolerance buffer triggers failure."""
    decl = CanonicalDeclaration(
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=240.0,            # Expected USP = 240 / 200 = 1.20
        declared_usp_value=1.80,  # VIOLATION: Declared 1.80 instead of 1.20
        declared_usp_unit="g",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "FAIL"
    assert rec.is_compliant is False
    assert "arithmetic mismatch" in rec.notes.lower()


def test_usp_engine_integration(engine):
    """Verify StatutoryRuleEngine.evaluate integrates USP validation into overall verdict."""
    # Compliant declaration with valid USP
    decl_compliant = CanonicalDeclaration(
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
    res_compliant = engine.evaluate(decl_compliant)
    assert res_compliant.overall_verdict == ComplianceState.COMPLIANT
    usp_eval = next(r for r in res_compliant.rule_evaluations if r.rule_id == "LMPC-R06-USP-001")
    assert usp_eval.is_compliant is True

    # Non-compliant declaration with arithmetic mismatch on USP
    decl_mismatch = decl_compliant.model_copy(update={"declared_usp_value": 2.50})
    res_mismatch = engine.evaluate(decl_mismatch)
    assert res_mismatch.overall_verdict == ComplianceState.NON_COMPLIANT
    usp_eval_mismatch = next(r for r in res_mismatch.rule_evaluations if r.rule_id == "LMPC-R06-USP-001")
    assert usp_eval_mismatch.is_compliant is False
