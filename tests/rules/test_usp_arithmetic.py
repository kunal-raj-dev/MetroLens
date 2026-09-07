"""
Tests for Unit Sale Price (USP) Arithmetic Precision & IEEE-754 Tolerance Bounds.
Verifies decimal.Decimal math, ROUND_HALF_UP rounding to two decimal places,
1.0% engineering comparison tolerance, division-by-zero robustness, and edge cases.
"""

import pytest
from decimal import Decimal
from nirikshak_rules_engine import (
    USPValidator,
    CanonicalDeclaration,
    UnitType,
)


@pytest.fixture
def validator():
    return USPValidator()


def test_usp_repeating_fractional_cent_round_half_up(validator):
    """
    Test repeating decimal rounding: MRP ₹10.00 for 300g.
    Exact math: 10 / 300 = 0.033333333333...
    Statutory rounding (2 decimal places, ROUND_HALF_UP): ₹0.03 / g.
    """
    decl = CanonicalDeclaration(
        net_quantity_value=300.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=10.0,
        declared_usp_value=0.03,
        declared_usp_unit="g",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.required_value == "₹ 0.03 / g"


def test_usp_half_cent_round_half_up(validator):
    """
    Test half-cent rounding boundary: MRP ₹1.25 for 50g.
    Exact math: 1.25 / 50 = 0.025.
    ROUND_HALF_UP rounds 0.025 to 0.03.
    """
    decl = CanonicalDeclaration(
        net_quantity_value=50.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=1.25,
        declared_usp_value=0.03,
        declared_usp_unit="g",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.required_value == "₹ 0.03 / g"


def test_usp_fractional_low_mrp_per_gram(validator):
    """Test low unit price edge case: MRP ₹5.00 for 100g = ₹0.05 / g."""
    decl = CanonicalDeclaration(
        net_quantity_value=100.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=5.0,
        declared_usp_value=0.05,
        declared_usp_unit="g",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.required_value == "₹ 0.05 / g"


def test_usp_high_value_commodity_per_kg(validator):
    """Test high price commodity: MRP ₹45000.00 for 25kg (25000g) = ₹1800.00 / kg."""
    decl = CanonicalDeclaration(
        net_quantity_value=25.0,
        net_quantity_unit=UnitType.KILOGRAM,
        mrp_inr=45000.0,
        declared_usp_value=1800.0,
        declared_usp_unit="kg",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.required_value == "₹ 1800.00 / kg"


def test_usp_tolerance_buffer_within_1_percent(validator):
    """
    Engineering tolerance buffer: If declared USP is within 1.0% of expected,
    minor packaging rounding discrepancies are accepted.
    MRP = 100, Net Qty = 300g -> Expected = 0.33.
    Declared = 0.333 or 0.33.
    """
    decl = CanonicalDeclaration(
        net_quantity_value=300.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=100.0,
        declared_usp_value=0.33,
        declared_usp_unit="g",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True


def test_usp_tolerance_buffer_exceeding_1_percent_fails(validator):
    """
    When declared USP deviates by > 1.0% (e.g. 5.0%),
    the engine must flag an arithmetic mismatch.
    MRP = 100, Net Qty = 300g -> Expected = 0.33.
    Declared = 0.36 (diff = 0.03 > 0.02 and rel_diff ~ 9%).
    """
    decl = CanonicalDeclaration(
        net_quantity_value=300.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=100.0,
        declared_usp_value=0.36,
        declared_usp_unit="g",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "FAIL"
    assert rec.is_compliant is False
    assert "arithmetic mismatch" in rec.notes.lower()


def test_usp_sub_cent_precision_quantization(validator):
    """
    Test sub-cent quantization: MRP ₹2.00 for 250g.
    Exact math: 2.0 / 250 = 0.008 -> quantizes to 0.01.
    """
    decl = CanonicalDeclaration(
        net_quantity_value=250.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=2.0,
        declared_usp_value=0.01,
        declared_usp_unit="g",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.required_value == "₹ 0.01 / g"


def test_usp_fractional_kilogram_normalization(validator):
    """
    Test fractional kilogram normalization: 2.5 kg at ₹500.00.
    Since net qty >= 1kg, denominator is kg.
    Expected: 500 / 2.5 = ₹200.00 / kg.
    """
    decl = CanonicalDeclaration(
        net_quantity_value=2.5,
        net_quantity_unit=UnitType.KILOGRAM,
        mrp_inr=500.0,
        declared_usp_value=200.0,
        declared_usp_unit="kg",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "PASS"
    assert rec.is_compliant is True
    assert rec.required_value == "₹ 200.00 / kg"


def test_usp_zero_quantity_division_safety(validator):
    """Verify that zero net quantity returns REVIEW cleanly without throwing ZeroDivisionError."""
    decl = CanonicalDeclaration(
        net_quantity_value=0.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=100.0,
        declared_usp_value=1.0,
        declared_usp_unit="g",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "REVIEW"
    assert rec.is_compliant is False


def test_usp_negative_mrp_safety(validator):
    """Verify that negative MRP returns REVIEW cleanly without throwing exceptions."""
    decl = CanonicalDeclaration(
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mrp_inr=-50.0,
        declared_usp_value=1.0,
        declared_usp_unit="g",
    )
    rec = validator.evaluate(decl)
    assert rec.status == "REVIEW"
    assert rec.is_compliant is False


def test_usp_none_inputs_safety(validator):
    """Verify that None inputs return REVIEW cleanly without throwing unhandled exceptions."""
    decl = CanonicalDeclaration(
        net_quantity_value=None,
        net_quantity_unit=None,
        mrp_inr=None,
        declared_usp_value=None,
        declared_usp_unit=None,
    )
    rec = validator.evaluate(decl)
    assert rec.status == "REVIEW"
    assert rec.is_compliant is False
