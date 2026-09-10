# Test Matrix & Verification Cross-Reference

## Purpose
Maps selected requirements to existing verification scripts and test files, and identifies validation gaps. A file link establishes where a check is implemented; it does not establish that the check passed in a particular environment.

## Scope
Covers repository governance, quality gating, calibration, extraction, rule outcomes, and offline inspection. This is a requirement-oriented subset, not an exhaustive test inventory.

## Authoritative Inputs
- [Requirement traceability](../01_PROBLEM_STATEMENT/REQUIREMENT_TRACEABILITY.md)
- [Acceptance criteria](../03_PRODUCT_REQUIREMENTS/ACCEPTANCE_CRITERIA.md)
- [Benchmark protocol](../07_DATA/BENCHMARK_PROTOCOL.md)

## Assumptions
- Most linked unit tests use synthetic fixtures. Such checks do not establish representative real-package accuracy or physical measurement tolerances.
- OCR tests require the documented local runtime and model files.

## Open Questions
- Physical calibration accuracy and complete disconnected-network inspection-to-dossier acceptance remain unvalidated by the linked unit tests.

## Dependencies
- `tests/`, `packages/*/tests/`, and `scripts/verification/`

## Verification Requirements
- Run each governance script with `python scripts/verification/<script>.py`; these are not collected by pytest.
- Run pytest files with `python -m pytest <linked file or directory>`. `pytest tests/` does not include the package-local suites.
- Configure test spool and temporary storage beneath an isolated test directory before API/storage tests; do not use retained user inspections.
- Record actual commands and results separately. The expected results below are acceptance targets, not recorded execution results.

---

| Test ID | Target Component | Statutory / Functional Focus | Test Implementation | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TEST-LEG-01** | Legal sources | Source record/checksum consistency | [verify_legal_sources.py](../../scripts/verification/verify_legal_sources.py) | No structural/provenance errors. Declared partial or unverified sources may remain; exit 0 does not authenticate all law. |
| **TEST-RUL-01** | Rule registry | Schema and lifecycle | [verify_rule_registry.py](../../scripts/verification/verify_rule_registry.py) | No schema/lifecycle errors. Does not prove active engine use of a verified historical registry. |
| **TEST-CLM-01** | Claims registry | Evidence requirements for registered claims | [verify_claims.py](../../scripts/verification/verify_claims.py) | No registered `VERIFIED` claim without required evidence; not a scan of every repository statement. |
| **TEST-DAT-01** | Data manifest | Declared specimen/provenance consistency | [verify_dataset_manifest.py](../../scripts/verification/verify_dataset_manifest.py) | No manifest errors. Physical-data and benchmark blockers remain explicit. |
| **TEST-VIS-01** | Quality gate | Blur/glare checks on synthetic frames | [test_quality_gate.py](../../packages/vision/tests/test_quality_gate.py) | Rejects tested severe blur and evaluates synthetic glare. Real-camera acceptance needs separate validation. |
| **TEST-VIS-02** | Calibration | Scale formula and unavailable-reference handling | [test_calibration_smoke.py](../../packages/calibration/tests/test_calibration_smoke.py) | Checks scale conversion and uncertainty handling. **Gap:** physical error $\le 0.2\text{ mm}$ is not established by these smoke tests; follow the benchmark protocol. |
| **TEST-EXT-01** | Field extractor | Declaration normalization from OCR tokens | [test_normalizer.py](../../tests/rules/test_normalizer.py) | Normalizes declaration fixtures. Does not establish end-to-end OCR accuracy on real packaging. |
| **TEST-ENG-01** | Rule engine | Rule outcomes and unresolved measurements | [test_rules_engine.py](../../tests/rules/test_rules_engine.py), [test_rule_7.py](../../tests/rules/test_rule_7.py), [test_review_applicability.py](../../packages/rules-engine/tests/test_review_applicability.py) | Preserves `PASS`/`FAIL`/`REVIEW`/`NOT_APPLICABLE`; missing measurements remain uncertain. Passing fixtures do not verify statutory sources. |
| **TEST-E2E-01** | Offline mode | Complete inspection with network disconnected | **Gap:** no matching complete offline inspection-to-PDF test. Supporting OCR-only check: [test_ocr_offline.py](../../tests/unit/test_ocr_offline.py). | The supporting test guards `socket.socket.connect` while running local OCR. It does not prove camera-to-dossier operation, all network paths disabled, or a valid exported evidence graph. |
