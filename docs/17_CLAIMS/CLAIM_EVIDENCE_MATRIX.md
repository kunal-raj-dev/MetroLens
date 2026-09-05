# Claim Evidence Matrix

## Purpose
Maps every declared capability of Nirikshak to its underlying empirical verification artifact, experimental protocol, or statutory source.

## Scope
Enforces evidence completeness prior to submission and live judging.

## Authoritative Inputs
- `docs/17_CLAIMS/CLAIMS_REGISTER.md`
- `benchmarks/protocols/`
- `regulations/source_registry.yaml`

## Assumptions
- Any claim lacking a completed verification link will be defended as a design target or marked `EXPERIMENT_REQUIRED` rather than an accomplished fact.

---

| Claim ID | Category | Proposition | Evidence Dependency | Verification Status | Gate Requirement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CLM-TECH-001** | Technical | Millimetre-scale font & PDP measurement | `experiments/calibration/` | EXPERIMENT_REQUIRED | Pass error bound test $\le 0.2\text{ mm}$ |
| **CLM-PERF-001** | Performance | High-accuracy curved surface OCR | `benchmarks/results/` | TBD_MEASURE | Run PROTO-OCR-001 on cylindrical set |
| **CLM-LEGAL-001** | Legal | Deterministic compliance decision | `rules/tests/` | EXPERIMENT_REQUIRED | 100% pass on synthetic test suite |
| **CLM-COMP-001** | Competitive | Multi-panel & regulatory snapshot | `packages/rules-engine/` | EXPERIMENT_REQUIRED | Interactive demo with historical date |
