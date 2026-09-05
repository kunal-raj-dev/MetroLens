# Project Milestones & Critical Path

## Purpose
Defines key delivery milestones, target dates, hard deadlines, and gating conditions for the hackathon lifecycle.

## Scope
Universal across development, staging, dry runs, and final submission.

## Authoritative Inputs
- SIH 2026 Hackathon schedule.

## Assumptions
- Critical path focuses on completing an end-to-end defensible inspection workflow before adding secondary UI enhancements.

## Dependencies
- `docs/13_BUILD_PLAN/ROADMAP.md`

## Verification Requirements
- Milestone sign-off requires meeting all exit criteria.

---

## Milestone Timeline

```
┌────────────────────────────────────────────────────────┐
│ M1: GOVERNANCE & SKELETON FREEZE (COMPLETED)           │
│ • Directory layout, anti-hallucination scripts, schemas│
│ • Exit Gate: make verify passes 100%                   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ M2: CORE VISION & CALIBRATION PIPELINE                 │
│ • Blur gate, target detector, scale estimator in mm    │
│ • Exit Gate: Calibration error bounded (TARGET — TBD)  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ M3: OCR, EXTRACTION & DETERMINISTIC RULE ENGINE        │
│ • Multilingual OCR, 7 mandatory fields, time-machine   │
│ • Exit Gate: 100% pass on tests/rules/ unit test suite │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ M4: INTEGRATION & DOSSIER GENERATION                   │
│ • Web guided capture + FastAPI + PDF dossier export    │
│ • Exit Gate: End-to-end latency benchmarked (TBD)      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ M5: LIVE DEMO REHEARSAL & SUBMISSION                   │
│ • Live demo executed under 4:30; judge Q&A dry runs    │
│ • Exit Gate: Final quality gate audit passes           │
└────────────────────────────────────────────────────────┘
```
