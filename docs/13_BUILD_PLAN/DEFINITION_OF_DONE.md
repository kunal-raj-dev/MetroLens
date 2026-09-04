# Definition of Done (DoD)

## Purpose
Establishes the mandatory quality, security, documentation, and verification standards that must be satisfied before any feature, pull request, or task is marked complete.

## Scope
Universal across code, documentation, rules, and benchmarks.

## Authoritative Inputs
- Project Anti-Hallucination Policy.
- CI/CD quality gates.

## Assumptions
- No work is "done" merely because the code compiles on a developer's machine.

## Dependencies
- `.github/workflows/ci.yml`
- `scripts/verification/`

## Verification Requirements
- Every PR checklist must verify all DoD criteria before merging to `main`.

---

## The 7-Point Definition of Done Checklist

A task or feature is considered **DONE** if and only if:

1. **Code Quality & Style:**
   - Code is clean, modular, and passes `ruff check .` with zero lint errors.
   - Pydantic models enforce strict typing; zero `Any` types in public interfaces.

2. **Automated Test Coverage:**
   - Dedicated unit tests implemented in `tests/unit/` or `tests/rules/`.
   - All tests pass via `pytest tests/` with zero regressions.

3. **Anti-Hallucination & Legal Check:**
   - Any new rule references an authentic entry in `regulations/source_registry.yaml` with valid `source_location`.
   - No unverified rules placed in `rules/current/` (must reside in `rules/proposed/`).
   - `python scripts/verification/verify_legal_sources.py` passes.
   - `python scripts/verification/verify_rule_registry.py` passes.

4. **Claims & Benchmark Integrity:**
   - No unsupported performance or accuracy numbers introduced.
   - Unmeasured metrics explicitly marked `TBD — MEASURE`.
   - `python scripts/verification/verify_claims.py` passes.

5. **Data & License Hygiene:**
   - Any new image batch has an entry in `data/manifests/manifest.yaml` with license, source, and date.
   - `python scripts/verification/verify_dataset_manifest.py` passes.

6. **Documentation Updated:**
   - Associated documentation files in `docs/` updated to reflect changes.
   - Traceability matrix updated in `docs/01_PROBLEM_STATEMENT/PS_REQUIREMENTS_MATRIX.md`.

7. **Peer Review & Sign-Off:**
   - At least one code review approval by the designated subsystem owner.
