# Claim Verification Registry & Proof Catalog

## Purpose
Catalogues every public, technical, legal, and performance claim made by Nirikshak, providing explicit verification statuses, empirical proof links, and limitation boundaries.

## Verification Policy
- Any claim marked `VERIFIED` must link to an authenticated primary source or an existing empirical benchmark report on disk.
- If an empirical run has not yet been executed, the status is strictly logged as `EXPERIMENT_REQUIRED` or `TBD_MEASURE`.
- Unbacked claims fail CI automatically via `scripts/verification/verify_claims.py`.

---

## Controlled Claim Registry

| Claim ID | Claim Proposition | Category | Evidence / Source Link | Verification Status | verified_date | last_reviewed | Limitations & Context |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CLM-TECH-001** | "Measures font height in millimetres using optical calibration." | Technical | `experiments/calibration/` | EXPERIMENT_REQUIRED | null | 2026-09-04 | Requires planar reference target in camera plane; otherwise defaults to REVIEW. |
| **CLM-PERF-001** | "Character Error Rate exceeds baseline on curved packaging." | Performance | `benchmarks/results/` | TBD_MEASURE | null | 2026-09-04 | Awaiting PROTO-OCR-001 execution on cylindrical test set. |
| **CLM-LEGAL-001** | "Compliance evaluations are deterministic and avoid AI hallucination." | Legal | `rules/tests/` | EXPERIMENT_REQUIRED | null | 2026-09-04 | AI restricted to optical observation; deterministic code evaluates statutory thresholds. |
| **CLM-COMP-001** | "In reviewed systems, we did not identify solutions combining multi-panel correlation and regulatory versioning." | Competitive | `docs/12_PRIOR_ART/DIFFERENTIATION.md` | EXPERIMENT_REQUIRED | null | 2026-09-04 | Based on systems reviewed in PRIOR_ART_REGISTER.md; requires multi-panel capture sequence. |
