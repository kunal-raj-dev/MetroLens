# Architecture Decisions Overview

## Purpose
Summarizes the key technical and structural decisions made across the Nirikshak architecture, linking them to formal Architecture Decision Records (ADRs).

## Scope
Covers framework selection, vision pipeline design, rule engine execution, database choices, and offline capabilities.

## Authoritative Inputs
- `docs/15_DECISIONS/`
- SIH 2026 Problem Statement requirements.

## Assumptions
- Every significant architectural pivot or constraint must be formally justified in `docs/15_DECISIONS/`.

## Open Questions
- Long-term synchronization strategy for central departmental telemetry [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `docs/15_DECISIONS/`

## Verification Requirements
- Architectural choices must align with the Anti-Hallucination Policy and Lean Architecture Mandate.

---

## Architectural Decision Summary Table

| Decision Area | Chosen Approach | Rejected Alternative | Key Justification |
| :--- | :--- | :--- | :--- |
| **Compliance Decision** | Deterministic Code & Schema | LLM / Generative AI Prompting | Zero hallucination; mathematically deterministic & reproducible; legally auditable. |
| **Physical Measurement** | Optical Reference Calibration | Uncalibrated pixel heuristics | Pixels are not mm; arbitrary conversion produces fatal legal errors. |
| **Deployment Model** | Modular Monolith / Local Stack | Distributed 14-service microservices | Eliminates network failure in basements; hackathon-practical. |
| **Evidence Structure** | Directed Acyclic Graph (DAG) | Flat database row | Full chain of custody linking raw pixels to final verdict. |
| **Rule Versioning** | Historical Regulatory Snapshots | Fixed latest ruleset | Packages manufactured in 2018 cannot be penalized under 2022 rules. |
| **Image Quality Gate** | Pre-inference blur & glare check | Blind end-to-end processing | Saves compute; eliminates spurious OCR hallucinations on degraded frames. |
