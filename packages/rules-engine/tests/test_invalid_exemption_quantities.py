"""Invalid quantities must never establish a small-package exemption."""

import pytest

from nirikshak_rules_engine import CanonicalDeclaration, StatutoryRuleEngine, UnitType
from nirikshak_rules_engine.normalizer import TokenNormalizer


@pytest.mark.parametrize("quantity", [0.0, -1.0, float("-inf")])
@pytest.mark.parametrize("unit", [UnitType.GRAM, UnitType.MILLILITER])
def test_nonpositive_quantity_cannot_establish_small_package_exemption(quantity, unit):
    declaration = CanonicalDeclaration(net_quantity_value=quantity, net_quantity_unit=unit)
    is_exempt, record = StatutoryRuleEngine().evaluate_exemptions(declaration)
    assert is_exempt is False
    assert record is None


def test_zero_quantity_from_ocr_does_not_bypass_declaration_evaluation():
    declaration = TokenNormalizer().normalize("Soap\nNet Qty: 0 g")
    result = StatutoryRuleEngine().evaluate(declaration)
    assert result.overall_verdict != "EXEMPTED"
    assert any(record.rule_id.startswith("LMPC-R06-") for record in result.rule_evaluations)
