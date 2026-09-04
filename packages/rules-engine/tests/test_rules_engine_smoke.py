"""
Smoke test for nirikshak-rules-engine.
"""

from nirikshak_rules_engine import NirikshakRulesEngine, RuleVerdict
from nirikshak_shared.models.contracts import DeclarationField


def test_evaluate_mrp_present():
    engine = NirikshakRulesEngine()
    decls = {
        "mrp": DeclarationField(
            field_name="mrp",
            raw_text="MRP Rs. 99.00",
            confidence=0.98,
            is_present=True,
        )
    }
    evals = engine.evaluate_mandatory_declarations(decls)
    assert len(evals) == 1
    assert evals[0].rule_id == "LMPC-R06-MRP-001"
    assert evals[0].verdict == RuleVerdict.PASS


def test_evaluate_mrp_missing():
    engine = NirikshakRulesEngine()
    evals = engine.evaluate_mandatory_declarations({})
    assert len(evals) == 1
    assert evals[0].verdict == RuleVerdict.FAIL
