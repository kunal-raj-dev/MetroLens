# Nirikshak Claims Register

## Purpose
Establishes the anti-hallucination tracking registry for all public, technical, legal, and performance assertions made by the Nirikshak system. Prevents unsubstantiated assertions during SIH evaluations.

## Scope
Governs all slides, READMEs, technical documentation, demos, and verbal representations to hackathon judges.

## Authoritative Inputs
- Actual benchmark outputs located in `benchmarks/results/`.
- Authenticated primary source records located in `regulations/source_registry.yaml`.
- Verified architectural implementations in `packages/`.

## Assumptions
- No performance figure may be cited unless produced by a reproducible test run recorded under `benchmarks/runs/`.

## Verification Taxonomy
- `VERIFIED`: Backed by an existing empirical report or verified primary source.
- `PARTIALLY_VERIFIED`: Structurally sound and partially tested, but lacking full multi-condition data.
- `TBD_MEASURE` / `EXPERIMENT_REQUIRED`: Awaiting empirical benchmark execution.
- `PRIMARY_SOURCE_REQUIRED`: Legal assertion awaiting Gazette retrieval.
- `REJECTED`: Disproven, unsupported, or removed from project claims.

---

## Claim Registry

## Claim: CLM-TECH-001
- **Claim:** "Nirikshak measures physical font height and PDP area in millimetres using reference-target calibration."
- **Type:** TECHNICAL
- **Status:** EXPERIMENT_REQUIRED
- **Evidence:** experiments/calibration/
- **verified_date:** null
- **last_reviewed:** 2026-09-04
- **Owner:** Computer Vision Lead
- **Limitations:** Requires an unoccluded physical reference target in the camera plane. Without reference calibration, system status defaults strictly to REVIEW.

## Claim: CLM-PERF-001
- **Claim:** "OCR character detection accuracy exceeds baseline on curved cylindrical packaging surfaces."
- **Type:** PERFORMANCE
- **Status:** TBD_MEASURE
- **Evidence:** benchmarks/results/
- **verified_date:** null
- **last_reviewed:** 2026-09-04
- **Owner:** AI Lead
- **Limitations:** TBD — MEASURE. No empirical number may be claimed until benchmark protocol PROTO-OCR-001 is executed on DS-RETAIL-PILOT-001.

## Claim: CLM-LEGAL-001
- **Claim:** "Rule evaluation is fully deterministic and avoids statistical AI for legal compliance verdicts."
- **Type:** LEGAL
- **Status:** EXPERIMENT_REQUIRED
- **Evidence:** rules/tests/
- **verified_date:** null
- **last_reviewed:** 2026-09-04
- **Owner:** Legal Engineering Lead
- **Limitations:** AI outputs are treated as observations; deterministic engine maps observations to statutory PASS/FAIL/REVIEW states.

## Claim: CLM-COMP-001
- **Claim:** "In reviewed systems listed in PRIOR_ART_REGISTER.md, we did not identify solutions combining multi-panel correlation and regulatory time-machine versioning for Indian Legal Metrology."
- **Type:** COMPETITIVE
- **Status:** EXPERIMENT_REQUIRED
- **Evidence:** docs/12_PRIOR_ART/DIFFERENTIATION.md
- **verified_date:** null
- **last_reviewed:** 2026-09-04
- **Owner:** Architecture Lead
- **Limitations:** Based exclusively on reviewed systems documented in PRIOR_ART_REGISTER.md; requires multi-panel capture sequence (minimum front PDP + back declarations).
