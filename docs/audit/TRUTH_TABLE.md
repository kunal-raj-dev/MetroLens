# MetroLens AI — Repository Ground-Truth Table
**Audit Baseline Date:** 2026-09-05  
**Evaluation Principle:** Hard Repository Evidence Over Documentation Claims  
**Authoritative Rule:** If it cannot be proven with files and execution on disk, it is not verified.

---

## 1. Truth Table of Key System Claims

| Claim / Assertion | Where Claimed | Physical Repository Evidence | Actual Status | Confidence | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **"OCR perception engine exists and extracts text"** | `docs/PRODUCT_BLUEPRINT.md`, `README.md`, `MEMBER_1_WORK_PLAN.md` | `packages/ocr/src/nirikshak_ocr/engine.py`, 11 modules, passes 89 tests | **VERIFIED** | HIGH (100%) | Production-grade direct ONNX engine running DBNet++ and SVTR models. |
| **"OCR runs 100% offline with zero cloud API dependencies"** | `README.md`, `docs/04_ARCHITECTURE/OFFLINE_ARCHITECTURE.md` | `tests/unit/test_ocr_offline.py` passes under socket monkeypatching | **VERIFIED** | HIGH (100%) | Verified in automated tests. Zero outbound network sockets opened during inference. |
| **"OCR uses direct ONNX Runtime"** | `models/manifest.yaml`, `AI_CONTEXT/PROJECT_CONTEXT.md` | `packages/ocr/src/nirikshak_ocr/detector.py` imports `onnxruntime` | **VERIFIED** | HIGH (100%) | Uses `onnxruntime==1.29.0` with `CPUExecutionProvider`. |
| **"Multilingual Hindi / Devanagari OCR works"** | `docs/05_AI_VISION/OCR_STRATEGY.md` | `models/weights/ocr/rec_hi/rec.onnx`, `dict.txt` (167 chars), `router.py` | **VERIFIED** (Synthetic) | HIGH (100%) | Devanagari recognition verified on synthetic specimens; real packaging accuracy unmeasured. |
| **"OCR runs in under 800ms on server CPU"** | `docs/team/MEMBER_1_WORK_PLAN.md` | `benchmarks/ocr/chunk4/integration_results.json` | **VERIFIED** | HIGH (100%) | Empirically measured median latency is ~109.64 ms on AMD Ryzen 7 / Intel CPU (8 intra-op threads). |
| **"Real retail packaging dataset exists on disk"** | `docs/PRODUCT_BLUEPRINT.md`, `docs/DATA_AND_BENCHMARK_PLAN.md` | `data/raw/real/` contains 0 files | **UNSUPPORTED / 0 ON DISK** | HIGH (100%) | Exactly 0 physical packaging photos exist on disk. Formally blocked under Path B Gate. |
| **"35-SKU empirical benchmark has been conducted"** | `docs/07_DATA/`, `MEMBER_6_WORK_PLAN.md` | `benchmarks/results/` is empty (.gitkeep) | **PLANNED / NOT PERFORMED** | HIGH (100%) | The 35-SKU dataset does not exist; no real benchmark has been executed. |
| **"Synthetic regression test suite exists"** | `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/` | `data/synthetic/regression/` has 8 PNGs and `manifest.json` | **VERIFIED** | HIGH (100%) | 8 synthetic images exist and are used in unit and regression tests. |
| **"FastAPI backend API service exists"** | `apps/api/README.md`, `docs/API_CONTRACT.md` | `apps/api/main.py` exists (67 lines) | **IMPLEMENTED / SCAFFOLD ONLY** | HIGH (100%) | FastAPI server runs, but endpoints return hardcoded mock JSON without invoking OCR or rules. |
| **"Next.js web frontend application exists"** | `apps/web/README.md`, `MEMBER_5_WORK_PLAN.md` | `apps/web/src/app/page.tsx` exists (40 lines) | **SCAFFOLD ONLY / STATIC TEXT** | HIGH (100%) | Contains 40 lines of static placeholder HTML. No upload, no canvas, `node_modules` not installed. |
| **"Deterministic statutory rules engine exists"** | `docs/06_RULE_ENGINE/`, `MEMBER_3_WORK_PLAN.md` | `packages/rules-engine/src/nirikshak_rules_engine/__init__.py` | **SCAFFOLD ONLY (1 RULE)** | HIGH (100%) | Evaluates only 1 rule (MRP presence). Rules for Net Qty, dates, USP, and font heights are unbuilt. |
| **"Physical optical coin scale calibration works"** | `docs/05_AI_VISION/CALIBRATION.md`, `MEMBER_2_WORK_PLAN.md` | `packages/calibration/src/nirikshak_calibration/__init__.py` | **SCAFFOLD ONLY (MATH ONLY)** | HIGH (100%) | Has a function that divides two numbers; cannot detect coins or fiducial markers from an image. |
| **"Physical font height measurement works"** | `docs/05_AI_VISION/FONT_MEASUREMENT.md` | `packages/measurement/src/nirikshak_measurement/__init__.py` | **SCAFFOLD ONLY (MATH ONLY)** | HIGH (100%) | Multiplies pixels by scale factor; cannot convert OCR text bounding boxes to typographic font heights. |
| **"Image blur and specular glare quality gate works"** | `docs/05_AI_VISION/IMAGE_QUALITY_GATE.md` | `packages/vision/src/nirikshak_vision/__init__.py` | **SCAFFOLD ONLY** | HIGH (100%) | Uses basic numpy variance and thresholding; lacks OpenCV Laplacian and HSV glare mask logic. |
| **"Court-admissible PDF inspection dossier is generated"** | `docs/08_EVIDENCE/`, `MEMBER_4_WORK_PLAN.md` | `packages/reporting/src/nirikshak_reporting/__init__.py` | **SCAFFOLD ONLY (5 LINES TEXT)** | HIGH (100%) | Renders 5 lines of plain text via ReportLab; lacks image crops, Section 36(1) notices, and signatures. |
| **"System synchronizes with National eMaap portal"** | `docs/API_CONTRACT.md`, `docs/team/MEMBER_4_WORK_PLAN.md` | 0 occurrences in `packages/` or `apps/` | **PLANNED / NOT IMPLEMENTED** | HIGH (100%) | 0 lines of code exist across the entire repository. |
| **"System uses Celery and Redis for asynchronous task processing"** | `docs/ARCHITECTURE.md`, `docs/PRODUCT_BLUEPRINT.md` | 0 occurrences of `import celery` or `import redis` | **HISTORICAL / SUPERSEDED** | HIGH (100%) | Stale architecture design superseded by ADR-011 and direct in-memory synchronous execution. |
| **"PostgreSQL database persists inspections and evidence"** | `infra/db/init.sql`, `docker-compose.yml` | `infra/db/init.sql` exists; 0 Python DB code | **SCAFFOLD ONLY (DDL ONLY)** | HIGH (100%) | SQL table schema exists, but no ORM models or database drivers (`asyncpg`/`psycopg`) are used. |
| **"System can perform end-to-end inspection"** | `docs/PRODUCT_BLUEPRINT.md`, `MVP_UNIFIED_WORKFLOW_GRAPH.md` | `apps/api/main.py` does not invoke OCR or rules | **NOT IMPLEMENTED** | HIGH (100%) | Cannot run end-to-end. Pipeline halts at API mock and at OCR output. |
| **"89 automated tests pass in pytest"** | `CURRENT_STATE/CHUNK_4_STATUS.md` | `python -m pytest` outputs 89 passed in 21.49s | **VERIFIED** | HIGH (100%) | All 89 tests pass cleanly on Windows AMD64 Python 3.14.3. |

---

## 2. Summary Truth Assessment

- **What Truly Exists & Works:** The core OCR perception engine (`packages/ocr`) with direct ONNX models, multilingual routing, preprocessing filters, typed configuration, and the `OCRService` adapter, supported by 89 passing unit/integration tests and synthetic regression data.
- **What Is Scaffold / Stub Only:** Image quality gating, optical coin calibration, physical measurement, field extraction, legal rule engine, PDF dossier generation, backend API server, and web frontend.
- **What Is Completely Missing / 0 on Disk:** Authentic retail packaging photographs (0 real images), real packaging annotations, real-world accuracy benchmarks, automated CI workflows, eMaap sync, and database persistence.
