# Product Development Roadmap

## Purpose
Establishes the sequential delivery phases, sprint targets, and milestone horizons from hackathon prototype to production field deployment.

## Scope
Universal across engineering, vision, legal systems, and presentation tracks.

## Authoritative Inputs
- SIH 2026 delivery timeline and technical requirements.

## Assumptions
- Development proceeds through distinct, verifiable phases with clear entry and exit gates.

## Open Questions
- Pilot trial schedule with designated state enforcement directorates [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `docs/13_BUILD_PLAN/TASK_BREAKDOWN.md`
- `docs/13_BUILD_PLAN/MILESTONES.md`

## Verification Requirements
- All phase exits require passing corresponding verification test suites.

---

## The 4 Development Horizons

```
┌────────────────────────────────────────────────────────┐
│ PHASE 1: REPOSITORY SKELETON & GOVERNANCE (CURRENT)    │
│ • Complete engineering documentation suite             │
│ • Tripartite directory structure frozen                │
│ • Automated verification scripts in CI                 │
│ • JSON schemas for rules, evidence, applicability      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ PHASE 2: HACKATHON MVP PROTOTYPE                       │
│ • Local FastAPI server + React guided capture UI       │
│ • Image quality gate (blur/glare detection)            │
│ • Optical calibration via reference marker             │
│ • OCR pipeline & Rule 6 mandatory field extractor      │
│ • Deterministic rule engine (Rule 6 + Rule 7 Table I)  │
│ • PDF inspection dossier export with SHA-256 hashes    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ PHASE 3: BENCHMARKING & FIELD STRENGTHENING            │
│ • Execution of master benchmark protocols on retail set│
│ • Parametric cylinder dewarping module                 │
│ • E-commerce product listing batch ingestion           │
│ • Enhanced Devanagari OCR accuracy tuning              │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ PHASE 4: STATE-LEVEL DEPLOYMENT & PRODUCTION           │
│ • Central server synchronization & telemetry           │
│ • Android native camera SDK integration                │
│ • Departmental PKI digital signature integration       │
│ • Regional language script support (Tamil, Bengali)   │
└────────────────────────────────────────────────────────┘
```
