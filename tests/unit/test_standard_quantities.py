"""
Unit Tests for Second Schedule Standard Quantities & First Schedule MPE
=======================================================================
Verifies discrete and continuous step-size rules for baby food, biscuits,
bread, tea, edible oils, grains, and Rule 26 statutory exemptions.
"""

import pytest

from apps.api.verification.standard_quantities import (
    StandardQuantitiesValidator,
    StandardQuantityResult,
)


def test_standard_quantities_baby_food():
    """Verify baby food discrete packaging rules (100g, 200g, 400g, 500g, 1kg)."""
    val = StandardQuantitiesValidator()

    # Valid sizes
    assert val.validate("baby_food", 100, "g").is_compliant is True
    assert val.validate("baby_food", 400, "g").is_compliant is True
    assert val.validate("baby_food", 1, "kg").is_compliant is True

    # Invalid non-standard size (e.g. 350g, 250g)
    res_invalid = val.validate("baby_food", 350, "g")
    assert res_invalid.is_compliant is False
    assert "not a permitted standard size" in res_invalid.defect_reason.lower()


def test_standard_quantities_biscuits_discrete_and_steps():
    """Verify biscuits discrete sizes and 100g multiples between 300g and 1kg."""
    val = StandardQuantitiesValidator()

    # Discrete sizes
    assert val.validate("biscuits", 75, "g").is_compliant is True
    assert val.validate("biscuits", 150, "g").is_compliant is True
    assert val.validate("biscuits", 300, "g").is_compliant is True

    # 100g step multiples between 300g and 1000g: 400g, 500g, 600g
    assert val.validate("biscuits", 400, "g").is_compliant is True
    assert val.validate("biscuits", 700, "g").is_compliant is True

    # Invalid non-step size (e.g. 450g)
    assert val.validate("biscuits", 450, "g").is_compliant is False


def test_standard_quantities_edible_oil():
    """Verify edible oil permitted volumes and masses."""
    val = StandardQuantitiesValidator()

    # 1L, 500ml, 5L
    assert val.validate("edible_oil", 500, "ml").is_compliant is True
    assert val.validate("edible_oil", 1, "L").is_compliant is True
    assert val.validate("edible_oil", 5, "L").is_compliant is True

    # Non-standard 850ml
    assert val.validate("edible_oil", 850, "ml").is_compliant is False


def test_rule_26_statutory_exemptions():
    """Verify small packages (<=10g), bulk (>50kg), and institutional exemptions."""
    val = StandardQuantitiesValidator()

    # Small package <= 10g
    r_small = val.validate("biscuits", 8, "g")
    assert r_small.is_compliant is True
    assert r_small.is_exempt_under_rule_26 is True
    assert "Rule 26(a)" in r_small.statutory_citation

    # Institutional consumer
    r_inst = val.validate("biscuits", 435, "g", is_institutional_consumer=True)
    assert r_inst.is_compliant is True
    assert r_inst.is_exempt_under_rule_26 is True
    assert "Rule 26(d)" in r_inst.statutory_citation

    # Bulk agricultural > 50kg
    r_bulk = val.validate("grains", 55, "kg")
    assert r_bulk.is_compliant is True
    assert r_bulk.is_exempt_under_rule_26 is True


def test_maximum_permissible_error_mpe_calculation():
    """Verify First Schedule Table I MPE tolerance calculations."""
    val = StandardQuantitiesValidator()

    # <= 50g -> 9%
    v1, p1 = val.calculate_maximum_permissible_error(50.0, "g")
    assert p1 == 9.0
    assert v1 == 4.5

    # 500g -> 3%
    v2, p2 = val.calculate_maximum_permissible_error(500.0, "g")
    assert p2 == 3.0
    assert v2 == 15.0

    # 1000g -> 1.5%
    v3, p3 = val.calculate_maximum_permissible_error(1000.0, "g")
    assert p3 == 1.5
    assert v3 == 15.0
