# Regression Testing & Continuous Integrity Strategy

## Purpose
Establishes automated regression pipelines ensuring that new code commits or regulatory updates do not break existing rule evaluations, OCR benchmarks, or cryptographic invariants.

## Scope
Universal across all GitHub workflows and local development environments.

## Authoritative Inputs
- CI/CD workflow definitions (`.github/workflows/ci.yml`).

## Assumptions
- Every code change must run the full deterministic rule regression suite.

## Open Questions
- None.

## Dependencies
- `.github/workflows/`

## Verification Requirements
- PR merge is blocked if any existing regression test fails.

---

## Automated Regression Regimen

1. **Golden Dossier Regression:**
   - A suite of 10 golden synthetic packages with known expected outcomes (5 compliant, 3 non-compliant, 2 borderline) is evaluated on every build.
   - Assert exact character-level and verdict-level matching against stored golden JSON dossiers.

2. **Schema Invariant Regression:**
   - Any modification to `rules/schema/` triggers validation of all YAML files across `rules/current/`, `rules/verified/`, and `rules/proposed/`.

3. **Claims Invariant Regression:**
   - `scripts/verification/verify_claims.py` runs on every PR affecting docs or rules, preventing unbacked claims from creeping in.
