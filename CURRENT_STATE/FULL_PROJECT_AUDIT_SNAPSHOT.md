# CURRENT STATE: FULL PROJECT AUDIT SNAPSHOT
**Snapshot Timestamp:** 2026-09-05T15:42:00+05:30  
**Audit Baseline Commit:** `f25d15a` on branch `kunal-member-1-work`  
**Governing Status:** Verified Ground Truth (Senior-Level Audit Baseline)

---

## 1. Repository Status
- **Monorepo Layout:** Configured and active via `pytest.ini` and editable pip installs (`nirikshak-shared`, `nirikshak-ocr`).
- **Execution Architecture:** In-process direct ONNX execution on local CPU (ADR-011). Celery and Redis are formally superseded.
- **Current Chunk:** **Chunk 4 COMPLETED & VERIFIED** (OCR Monorepo Integration, Service Adapter & Contracts).
- **Next Chunk:** **Chunk 5 READY TO START** (Inspection Pipeline Orchestration, Route Mounting & Deployment Hardening).

---

## 2. Subsystem Implementation Reality
- **OCR Perception (`packages/ocr`):** **IMPLEMENTED & TESTED**. Direct ONNX PP-OCRv3 engine (DBNet++ detector, SVTR-EN & SVTR-HI recognizers, script router, preprocessing filter suite, and `OCRService` thread-safe singleton adapter).
- **Shared Contracts (`packages/shared`):** **IMPLEMENTED & TESTED**. Canonical Pydantic DTOs and geometric primitives.
- **Vision Quality Gate (`packages/vision`):** **SCAFFOLD** (71 lines; basic numpy variance stub).
- **Optical Calibration (`packages/calibration`):** **SCAFFOLD** (67 lines; basic division math stub; zero coin detection from images).
- **Physical Measurement (`packages/measurement`):** **SCAFFOLD** (44 lines; float multiplication stub).
- **Semantic Extraction (`packages/extraction`):** **SCAFFOLD** (47 lines; single regex for MRP; 5 mandatory fields unparsed).
- **Legal Rules Engine (`packages/rules-engine`):** **SCAFFOLD** (39 lines; evaluates only MRP presence).
- **Evidence Graph (`packages/evidence`):** **SCAFFOLD** (43 lines; SHA-256 helper and DTO factory).
- **Reporting (`packages/reporting`):** **SCAFFOLD** (41 lines; 5-line ReportLab canvas).
- **Backend API Gateway (`apps/api`):** **SCAFFOLD (MOCK)** (FastAPI endpoints return static mock JSON).
- **Frontend Web UI (`apps/web`):** **SCAFFOLD (STATIC)** (40 lines static text; `node_modules` not installed).
- **Worker Service (`apps/worker`):** **SCAFFOLD** (62 lines stub worker).

---

## 3. Test & Verification Status
- **Automated Tests:** **89 passed / 89 total (100% pass rate in ~21.5s)** on Python 3.14.3 Windows AMD64.
  - 67 tests cover OCR engine, types, preprocessing, evaluation, and service integration.
  - 5 tests execute repository verification scripts (`scripts/verification/`).
  - 17 tests are package/app smoke tests for scaffolds.

---

## 4. Data & Dataset Status
- **Real Physical Packaging Images:** **0 images on disk** (`data/raw/real/` is empty).
- **Real Ground-Truth Annotations:** **0 files on disk** (`data/annotations/ocr/` is empty).
- **Synthetic Test Images:** **8 valid PNG specimens** (`data/synthetic/regression/`) with verified ground truth.
- **Data Gate:** Formally **BLOCKED under Path B Gate** awaiting Member 6 collection of 35 authentic retail packages.

---

## 5. Active ML Models
- `ch_PP-OCRv3_det_infer.onnx` (2.43 MB, SHA-256: `3439588c...`) — DBNet++ detector.
- `ch_PP-OCRv3_rec_infer.onnx` (10.69 MB, SHA-256: `897a3ede...`) — SVTR Latin recognizer.
- `rec.onnx` (8.98 MB, SHA-256: `43df175f...`) — SVTR Devanagari Hindi recognizer.
- `dict.txt` (167 characters, SHA-256: `b5f1be6d...`) — Devanagari dictionary.
- All models verified present in `models/weights/ocr/` and governed by `models/manifest.yaml`.

---

## 6. Active Blockers
1. **Critical Blocker 1 (Data):** Member 6 must collect 35 physical FMCG packaging photos with reference coin targets.
2. **Critical Blocker 2 (CV):** Member 2 must implement ₹10 coin anchor detection in `packages/calibration/`.
3. **Critical Blocker 3 (Rules):** Member 3 must implement regex field extraction and rule state machine in `packages/rules-engine/`.
4. **High Blocker 4 (API):** Member 4 must mount `nirikshak_ocr.OCRService` in `apps/api/main.py`.
5. **High Blocker 5 (Web):** Member 5 must run `npm install` and build interactive upload/overlay components in `apps/web/`.

---

## 7. Immediate Next Task
- **Member 4:** Wire `OCRService.get_instance().extract_observations()` into `apps/api/main.py` so that `POST /api/v1/inspections` returns live OCR bounding boxes and text from uploaded images.
