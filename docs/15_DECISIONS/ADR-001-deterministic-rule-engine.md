# ADR-001: Deterministic Rule Engine vs. Generative LLM for Compliance Evaluation

## Status
ACCEPTED

## Date
2026-09-04

## Deciders
Principal Software Architect, Legal Engineering Lead, Rule Engine Lead

---

## Context & Problem Statement
Legal metrology enforcement under the Legal Metrology Act, 2009 and the Legal Metrology (Packaged Commodities) Rules, 2011 requires exact, statutory compliance determination. If an automated system issues an erroneous violation notice, penalty recommendation, or inspection dossier based on hallucinated regulations or non-deterministic reasoning, the inspection is legally invalid in a court of law.

We must decide whether to evaluate statutory compliance using generative AI / Large Language Models (prompting an LLM with OCR text and statutory text) or deterministic executable rule code and schemas.

---

## Decision Drivers
- **Zero Hallucination Policy**: Legal metrology cannot tolerate stochastic or hallucinated compliance verdicts.
- **Mathematical Determinism**: Identical OCR inputs and physical measurements must produce 100% reproducible verdicts every time.
- **Statutory Auditability**: Every evaluation must trace to exact Gazette rule numbers, subrules, and tables.
- **Offline Field Execution**: Enforcement officers in remote wholesale markets or basements operate without cloud LLM connectivity.

---

## Considered Options
1. **Option 1: Deterministic Code & Schema-Driven Rule Engine** (Chosen)
2. **Option 2: Generative LLM Prompting (e.g. Gemini / GPT-4)**
3. **Option 3: Hybrid LLM Classifier with post-filtering**

---

## Decision Outcome
**Chosen Option:** Option 1: Deterministic Code & Schema-Driven Rule Engine.
Compliance logic is encoded as deterministic Python evaluator functions validated against strict JSON and YAML schemas (`rules/schema/rule.schema.json`).

### Positive Consequences
- Guarantees 0% hallucination rate in compliance decisions.
- Completely reproducible and auditable in judicial proceedings.
- Capable of running locally on edge devices without internet access or GPU cloud dependencies.
- Sub-millisecond evaluation latency per rule.

### Negative Consequences / Trade-offs
- Requires upfront manual encoding and legal verification of statutory rules into machine-readable schemas.
- Less forgiving of minor linguistic syntax variations in OCR text compared to semantic embeddings (mitigated by specialized regex and normalization parsers in `packages/extraction`).

---

## References & Statutory Linkages
- Legal Metrology (Packaged Commodities) Rules, 2011 (Rule 6, Rule 9, Rule 18).
- Anti-Hallucination Architectural Mandate (`docs/04_ARCHITECTURE/`).
