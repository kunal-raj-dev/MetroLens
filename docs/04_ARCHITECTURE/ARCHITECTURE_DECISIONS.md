# Architecture Decisions Overview & Cross-Reference

## Purpose
Summarizes the key technical and structural decisions made across the Nirikshak architecture and links them to their formal, canonical Architecture Decision Records (ADRs).

## Canonical Authority Notice
> [!IMPORTANT]
> The single canonical source of truth for all formal Architecture Decision Records is **[`docs/15_DECISIONS/`](../15_DECISIONS/README.md)**.
> This document serves as a contextual architectural index and cross-reference. Teammates must author all new decisions in `docs/15_DECISIONS/` following `docs/15_DECISIONS/ADR_TEMPLATE.md`.

---

## Architectural Decision Cross-Reference Table

| Decision Area | Chosen Approach | Rejected Alternative | Canonical ADR Link |
| :--- | :--- | :--- | :--- |
| **Compliance Decision** | Deterministic Code & Schema | LLM / Generative AI Prompting | [ADR-001: Deterministic Rule Engine](../15_DECISIONS/ADR-001-deterministic-rule-engine.md) |
| **Physical Measurement** | Optical Reference Calibration | Uncalibrated pixel heuristics | [ADR-002: Optical Reference Calibration](../15_DECISIONS/ADR-002-optical-reference-calibration.md) |
| **Deployment Model** | Modular Monolith / Local Stack | Distributed 14-service microservices | [ADR-003: Modular Monolith Deployment](../15_DECISIONS/ADR-003-modular-monolith-deployment.md) |
| **Evidence Structure** | Directed Acyclic Graph (DAG) | Flat database row | [ADR-004: DAG Evidence Chain of Custody](../15_DECISIONS/ADR-004-dag-evidence-chain-of-custody.md) |
| **Rule Versioning** | Historical Regulatory Snapshots | Fixed latest ruleset | [ADR-005: Temporal Regulatory Snapshotting](../15_DECISIONS/ADR-005-temporal-regulatory-snapshotting.md) |
| **Image Quality Gate** | Pre-inference blur & glare check | Blind end-to-end processing | [ADR-006: Pre-Inference Quality Gate](../15_DECISIONS/ADR-006-quality-gate-pre-inference.md) |

---

## Governance Rules
1. Any architectural modification affecting package interfaces, models, or deployment topology requires an accepted ADR in `docs/15_DECISIONS/`.
2. Decisions must satisfy the Anti-Hallucination Policy and the Lean Architecture Mandate.
