# Nirikshak Rules Engine Package (`nirikshak-rules-engine`)

## Purpose
Executes deterministic compliance checks against machine-readable legal metrology rules (`rules/current/`). Evaluates mandatory declaration completeness, date epoch validity, and font height threshold satisfaction with zero generative hallucination.

## Owner
Legal / Rules Lead

## Interface Seams
- **Input**: `Dict[str, DeclarationField]`, `Dict[str, MeasurementResult]`, active rule definitions.
- **Output**: `List[RuleEvaluation]` (verdicts: `PASS`, `FAIL`, `REVIEW`, `NOT_APPLICABLE`).
- **Error Codes**: `ERR_RULE_SCHEMA_INVALID`.
