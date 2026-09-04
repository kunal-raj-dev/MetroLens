# Test Matrix & Verification Cross-Reference

## Purpose
Provides an exhaustive cross-reference mapping functional modules, statutory provisions, test vectors, and execution commands.

## Scope
Covers all unit, integration, and rule test suites.

## Authoritative Inputs
- `docs/01_PROBLEM_STATEMENT/REQUIREMENT_TRACEABILITY.md`

## Assumptions
- Automated tests run against static synthetic fixtures to ensure deterministic repeatability.

## Open Questions
- None.

## Dependencies
- `tests/`

## Verification Requirements
- All tests listed below must be executed by `pytest tests/`.

---

| Test ID | Target Component | Statutory / Functional Focus | Test Implementation | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TEST-LEG-01** | Legal Sources | Checksum & Provenance Verification | `scripts/verification/verify_legal_sources.py` | 0 errors |
| **TEST-RUL-01** | Rule Registry | Schema & Lifecycle Verification | `scripts/verification/verify_rule_registry.py` | 0 errors |
| **TEST-CLM-01** | Claims Registry| Anti-Hallucination Claims Audit | `scripts/verification/verify_claims.py` | 0 unbacked claims |
| **TEST-DAT-01** | Data Manifest | Dataset Provenance & Licenses | `scripts/verification/verify_dataset_manifest.py`| 0 errors |
| **TEST-VIS-01** | Quality Gate | Laplacian Variance Blur Rejection | `tests/vision/test_quality_gate.py` | Rejects blurry frame |
| **TEST-VIS-02** | Calibration | Reference Scale Detection ($\text{mm/px}$) | `tests/vision/test_calibration.py` | Error $\le 0.2\text{ mm}$ |
| **TEST-EXT-01** | Field Extractor| Rule 6(1) Mandatory 7 Declarations | `tests/unit/test_extraction.py` | Normalizes fields |
| **TEST-ENG-01** | Rule Engine | Deterministic Rule Evaluation | `tests/rules/test_evaluator.py` | PASS/FAIL/REVIEW/N/A |
| **TEST-E2E-01** | Offline Mode | Network Disconnected Inspection | `tests/e2e/test_offline.py` | Generates valid PDF |
