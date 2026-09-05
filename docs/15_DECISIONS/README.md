# Architecture Decision Records (ADR) Repository

## Purpose
Preserves the context, architectural justifications, considered alternatives, and long-term consequences of significant design decisions made throughout the Nirikshak lifecycle.

## Governance Policy
- **Canonical Authority**: This directory (`docs/15_DECISIONS/`) is the sole canonical repository for all Architecture Decision Records across the Nirikshak project.
- ADRs are authored only when a substantive architectural decision is deliberately analyzed, tested, and adopted.
- Avoid authoring premature ADRs before experimental or practical justification is established.
- Every new decision must adhere strictly to `ADR_TEMPLATE.md`.

---

## Canonical Decision Record Index

| ADR ID | Decision Title | Status | Date | Decision Summary |
| :--- | :--- | :--- | :--- | :--- |
| [**ADR-000**](ADR_TEMPLATE.md) | Architecture Decision Record Process Adoption | ACCEPTED | 2026-09-04 | Standardizing lightweight Markdown ADRs for project governance. |
| [**ADR-001**](ADR-001-deterministic-rule-engine.md) | Deterministic Rule Engine vs. Generative LLM | ACCEPTED | 2026-09-04 | Deterministic code execution over stochastic LLMs to ensure 0% hallucination in compliance verdicts. |
| [**ADR-002**](ADR-002-optical-reference-calibration.md) | Optical Reference Calibration vs. Uncalibrated Heuristics | ACCEPTED | 2026-09-04 | Mandating optical reference markers with explicit uncertainty intervals for physical font-height conversion. |
| [**ADR-003**](ADR-003-modular-monolith-deployment.md) | Modular Monolith vs. Distributed Microservices | ACCEPTED | 2026-09-04 | Deploying modular Python packages via API and async worker containers to eliminate inter-service latency. |
| [**ADR-004**](ADR-004-dag-evidence-chain-of-custody.md) | Cryptographic DAG Evidence Chain of Custody | ACCEPTED | 2026-09-04 | Structuring evidence as an immutable directed acyclic graph linked by SHA-256 digests. |
| [**ADR-005**](ADR-005-temporal-regulatory-snapshotting.md) | Date-of-Manufacture Temporal Regulatory Snapshotting | ACCEPTED | 2026-09-04 | Resolving and executing rules based on packaging date to prevent unlawful retroactive penalty assessment. |
| [**ADR-006**](ADR-006-quality-gate-pre-inference.md) | Pre-Inference Image Quality Gate (Blur & Glare) | ACCEPTED | 2026-09-04 | Enforcing Laplacian variance and glare filtering prior to heavy OCR inference to prevent false alarms. |
