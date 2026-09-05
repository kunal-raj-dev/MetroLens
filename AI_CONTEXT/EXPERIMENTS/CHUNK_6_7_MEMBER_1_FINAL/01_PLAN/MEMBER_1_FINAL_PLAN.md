# MEMBER 1 FINALIZATION & AUDIT PLAN (COMBINED CHUNK 6 + CHUNK 7)

**Lead**: Member 1 — AI & Multilingual OCR Lead  
**Scope**: Advanced OCR completion, robustness, performance hardening, forensic audit, documentation reconciliation, integration review, and subsystem freeze.  
**Date**: September 5, 2026  

---

## 1. Objective & Scope Boundaries
To take the Member 1 OCR subsystem from a working implementation to a finalized, verified, documented, reproducible, and integration-ready MVP subsystem, and freeze it.

### Inviolable Boundaries
- **Member 1 Produces**: Trustworthy optical text observations (`OCRObservation`), bounding boxes, polygons, confidence scores, script tags, image dimensions, and performance telemetry.
- **Member 1 Does NOT Produce**:
  - Legal Metrology rules (Member 3)
  - Semantic declaration field parsing (Member 3)
  - Metric measurement in mm or physical scaling (Member 2)
  - Scale calibration or reference detection (Member 2)
  - PDP segmentation or unwrapping (Member 2)
  - REST API gateway (Member 4)
  - Frontend UI (Member 5)
  - PDF reporting (Member 4/5)
  - eMaap sync (Member 4)

---

## 2. Microstep Execution Protocol

```
Step 1: Baseline & Asset Inventory
  ├── Capture system state in CURRENT_STATE/MEMBER_1_FINAL_BASELINE.md
  └── Create comprehensive asset inventory in M1_ASSET_INVENTORY.md

Step 2: Subsystem Code Hardening & Security Audit
  ├── Audit packages/ocr for memory safety, input guards, and decompression bomb protection (64MP)
  ├── Verify logging safety (no raw image/base64 logging)
  └── Verify thread safety & lifecycle guarantees

Step 3: Concurrency & Performance Benchmarking
  ├── Execute benchmarks/ocr/final/run_final_benchmark.py
  ├── Sweep 1, 2, 4, 8 threads for concurrency safety and memory stability
  └── Generate results.json, environment.json, config.json, README.md

Step 4: Forensic Independent Review & Verification
  ├── Evaluate 35 reviewer questions from Section 86
  ├── Build M1_TRUTH_MATRIX.md and M1_FINAL_SCORECARD.md
  ├── Build M1_FINAL_BUG_REGISTER.md and M1_FINAL_LIMITATIONS.md
  └── Compile M1_FINAL_VALIDATION_MATRIX.md

Step 5: Documentation & Downstream Handoffs
  ├── Create docs/audit/MEMBER_1_FINAL_SOURCE_OF_TRUTH.md
  ├── Create docs/audit/MEMBER_1_FILE_MAP.md & MEMBER_1_DO_NOT_REBUILD.md
  ├── Create docs/audit/MEMBER_1_REPRODUCIBILITY.md
  ├── Author inter-member handoffs (M1 to M2, M3, M4, M5, M6, Project)
  └── Author MEMBER_1_COMPLETE_TO_TEAM.md & MEMBER_1_EXIT_CHECKLIST.md

Step 6: Freeze & Master Recompilation
  ├── Formally freeze Member 1 via M1_FREEZE_MANIFEST.md & M1_FINAL_CHANGELOG.md
  ├── Write MEMBER_1_FINAL_ENGINEERING_REPORT.md (31 sections)
  ├── Update CURRENT_STATE/MEMBER_1_FINAL_STATUS.md
  ├── Recompile ALL-IN-ONE master context document
  └── Run full monorepo test suite & verify Git clean state
```
