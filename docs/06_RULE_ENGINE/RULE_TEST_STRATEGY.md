# Rule Engine Testing Strategy

## Purpose
Defines the verification methodology, test vector schemas, edge case coverage, and regression suites for all machine-readable compliance rules in `rules/`.

## Scope
Governs unit testing of rule schemas, evaluators, applicability matrices, and exemption logic.

## Authoritative Inputs
- `rules/schema/rule.schema.json`
- `tests/rules/`

## Assumptions
- Every rule in `rules/current/` must have at least one positive test vector (`PASS`), one negative test vector (`FAIL`), one borderline/uncertain test vector (`REVIEW`), and one exempt test vector (`NOT_APPLICABLE`).

## Open Questions
- None.

## Dependencies
- `pytest`
- `rules/fixtures/`

## Verification Requirements
- 100% of rule tests must pass before any new rule file is promoted to `rules/current/`.

---

## 4-Vector Rule Test Matrix Template

Every rule test suite must implement four standard test vectors:

```python
# tests/rules/test_template.py

def test_rule_evaluates_pass():
    # Vector 1: Fully compliant observation
    obs = create_mock_observation(field_value="Compliant", measured_mm=2.5, pdp_area=80.0, calibrated=True)
    assert evaluate_rule(obs) == "PASS"

def test_rule_evaluates_fail():
    # Vector 2: Clear non-compliance
    obs = create_mock_observation(field_value="Missing", measured_mm=0.8, pdp_area=80.0, calibrated=True)
    assert evaluate_rule(obs) == "FAIL"

def test_rule_evaluates_review_on_borderline_or_uncalibrated():
    # Vector 3: Uncertainty (Uncalibrated or borderline measurement)
    obs = create_mock_observation(field_value="Compliant", measured_mm=1.51, pdp_area=80.0, calibrated=False)
    assert evaluate_rule(obs) == "REVIEW"

def test_rule_evaluates_not_applicable_when_exempt():
    # Vector 4: Exemption condition satisfied
    obs = create_mock_observation(net_quantity=5.0, unit="g") # Under 10g exemption
    assert evaluate_rule(obs) == "NOT_APPLICABLE"
```
