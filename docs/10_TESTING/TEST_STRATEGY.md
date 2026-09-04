# Quality Assurance & Testing Strategy

## Purpose
Defines the multi-layered testing pyramid, automated verification gates, regression policies, and adversarial testing regimens for Nirikshak.

## Scope
Covers unit tests, rule tests, computer vision tests, API integration tests, and end-to-end user journey tests.

## Authoritative Inputs
- SIH 2026 Problem Statement 26034.
- Project Anti-Hallucination Policy.

## Assumptions
- No feature is complete until verified by automated unit tests and integration fixtures.

## Open Questions
- Establishing simulated optical noise generators for synthetic test sets [TBD — MEASURE].

## Dependencies
- `tests/`
- `scripts/verification/`

## Verification Requirements
- `make verify` and `pytest` must pass 100% in CI before pull requests are approved.

---

## The Nirikshak Testing Pyramid

```
                / \
               /   \      E2E Integration & UI Flows (tests/e2e/)
              /     \     - Guided capture to signed dossier export
             /-------\
            /         \   Vision, OCR & Calibration (tests/vision/)
           /           \  - Blur gate, dewarping, fiducial scale detection
          /-------------\
         /               \ Deterministic Rule Tests (tests/rules/)
        /                 \ - 4-state vectors: PASS, FAIL, REVIEW, N/A
       /-------------------\
      /                     \ Verification Scripts (scripts/verification/)
     /                       \ - Legal source provenance, rules schema, claims
    /-------------------------\
```

### Mandatory Verification Gates:
1. **Gate 1 (Anti-Hallucination):** `verify_legal_sources.py` ensures every rule links to an authentic primary source.
2. **Gate 2 (Rule Schema & Lifecycle):** `verify_rule_registry.py` enforces that `rules/current/` has only verified in-force rules.
3. **Gate 3 (Claims Integrity):** `verify_claims.py` fails CI if any claim is marked `VERIFIED` without an empirical report artifact.
4. **Gate 4 (Deterministic Correctness):** 100% pass rate on `tests/rules/`.
