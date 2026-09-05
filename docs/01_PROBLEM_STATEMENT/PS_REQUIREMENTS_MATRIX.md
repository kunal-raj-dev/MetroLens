# Problem Statement Requirements Matrix & Lifecycle Traceability

## Purpose
Establishes the master engineering matrix mapping every functional expectation in PS 26034 to its concrete software feature, underlying architectural module, automated test case, and live demonstration scenario.

## Multi-Dimensional Governance Notice
> [!IMPORTANT]
> In accordance with the Anti-Hallucination Policy, this matrix explicitly separates three dimensions:
> 1. **Legal Basis Status:** `VERIFIED_PRIMARY` | `VERIFIED_SECONDARY` | `PRIMARY_SOURCE_REQUIRED` | `NOT_APPLICABLE`
> 2. **Implementation Status:** `PLANNED` | `IMPLEMENTED` | `TESTED` | `BENCHMARKED`
> 3. **Evidence Status:** `NONE` | `EXPERIMENT_REQUIRED` | `VERIFIED` | `PARTIALLY_VERIFIED` | `REJECTED`

---

| Req ID | Problem Statement Requirement | Feature Specified | Core Module | Legal Basis Status | Implementation Status | Evidence Status | Planned Test / Verification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Multi-face package capture & acquisition | Guided Multi-Panel Capture UI & Quality Gate | `apps/web`, `packages/vision` | VERIFIED_SECONDARY | PLANNED | NONE | `tests/e2e/test_capture.py` (Planned) |
| **REQ-02** | Text detection & multilingual OCR | Bounding box text detection & OCR engine | `packages/ocr` | VERIFIED_SECONDARY | PLANNED | EXPERIMENT_REQUIRED | `tests/vision/test_ocr.py` (Planned) |
| **REQ-03** | Extraction of mandatory declarations | Structured field parsing (7 statutory declarations) | `packages/extraction` | PRIMARY_SOURCE_REQUIRED | PLANNED | NONE | `tests/unit/test_extraction.py` (Planned) |
| **REQ-04** | Detection of Principal Display Panel (PDP) | PDP polygon segmentation & surface area calculation | `packages/vision` | PRIMARY_SOURCE_REQUIRED | PLANNED | EXPERIMENT_REQUIRED | `tests/vision/test_pdp.py` (Planned) |
| **REQ-05** | Physical scale & font height measurement | Reference target calibration & measurement in mm | `packages/calibration`, `packages/measurement` | PRIMARY_SOURCE_REQUIRED | PLANNED | EXPERIMENT_REQUIRED | `tests/unit/test_calibration.py` (Planned) |
| **REQ-06** | Statutory compliance checking | Deterministic rule evaluator with snapshot versioning | `packages/rules-engine` | VERIFIED_SECONDARY | PLANNED | NONE | `tests/rules/test_evaluator.py` (Planned) |
| **REQ-07** | Auditable report generation | Cryptographic PDF & JSON inspection dossier | `packages/reporting`, `packages/evidence` | VERIFIED_SECONDARY | PLANNED | NONE | `tests/unit/test_dossier.py` (Planned) |
| **REQ-08** | Fully offline operation | Local inference & offline database storage | `apps/api`, `infra/db` | NOT_APPLICABLE | PLANNED | NONE | `tests/e2e/test_offline.py` (Planned) |
| **REQ-09** | Legal Source & Claims Verification | Automated Anti-Hallucination CI Verification | `scripts/verification/` | NOT_APPLICABLE | TESTED | VERIFIED | `tests/unit/test_verification_pipeline.py` (Passing) |
