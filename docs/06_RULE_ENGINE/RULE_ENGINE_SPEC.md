# Rule Engine Specification

## Purpose
Defines the functional architecture, evaluation algorithm, input/output schemas, and state machine of the Nirikshak Deterministic Rule Engine.

## Scope
Executes compliance checks against normalized package observations using machine-readable rules in `rules/`.

## Authoritative Inputs
- `rules/schema/rule.schema.json`
- `rules/schema/evidence.schema.json`

## Assumptions
- Rules are pure declarative functions mapping an `ObservationSet` and `RegulatorySnapshot` to an `EvaluationReport`.

## Open Questions
- Departmental guidelines regarding multi-pack commodities containing distinct sub-products with separate MRPs [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `packages/rules-engine/`
- `rules/`

## Verification Requirements
- Target: Engine must achieve 100% branch coverage across all rule unit tests in `tests/rules/` upon implementation (Status: SPECIFIED — PENDING_IMPLEMENTATION).

---

## Evaluation Algorithm

```python
def evaluate_package(observations: ObservationSet, inspection_date: Date) -> EvaluationReport:
    # Step 1: Resolve statutory epoch
    epoch = resolve_regulatory_epoch(observations.manufacturing_date or inspection_date)
    
    # Step 2: Load active rules for epoch
    active_rules = load_active_rules(epoch)
    
    report = EvaluationReport(inspection_id=observations.inspection_id, epoch=epoch)
    
    # Step 3: Check overall statutory applicability & exemptions
    if is_exempt(observations, active_rules):
        report.set_status("NOT_APPLICABLE", reason="Package qualifies for statutory exemption")
        return report
        
    # Step 4: Iterate over active rules
    for rule in active_rules:
        # Check rule-level applicability
        if not rule.applies_to(observations.commodity_type, observations.package_type):
            report.add_rule_result(rule.rule_id, "NOT_APPLICABLE")
            continue
            
        # Execute deterministic evaluator
        verdict = rule.evaluator(observations)
        report.add_rule_result(rule.rule_id, verdict)
        
    return report
```
