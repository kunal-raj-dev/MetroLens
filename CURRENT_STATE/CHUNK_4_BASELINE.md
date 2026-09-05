# CURRENT STATE: CHUNK 4 BASELINE
**Document:** `CURRENT_STATE/CHUNK_4_BASELINE.md`  
**Generated:** 2026-09-05T05:28:00+05:30  
**Phase:** Member 1 — Chunk 4 (OCR Monorepo Integration, Service Adapter, Contract Verification & End-to-End Readiness)  
**Role:** Senior ML / Computer Vision / Systems Engineer (Member 1 Lead)  

---

## 1. Git & Environment Reality
- **Git Branch:** `main`
- **Git HEAD Commit:** `4681c476ff9d2b6ba549de792a39258b9d570bcb`
- **Working Tree State:** Clean working branch with unstaged/untracked local experiment, model, and documentation artifacts.
- **Git Operations Policy:** **STRICTLY ENFORCED: NO GIT COMMITS, NO GIT PUSH.**
- **Host OS:** Windows 11 (AMD64)
- **Python Runtime:** Python `3.14.3`
- **Core Library Versions:**
  - `onnxruntime`: `1.29.0` (Direct ONNX Runtime CPUExecutionProvider)
  - `opencv-python`: `5.0.0.93`
  - `numpy`: `2.5.2`
  - `shapely`: `2.1.2`
  - `pyclipper`: `1.4.0`
  - `pydantic`: `2.13.4`
  - `fastapi`: `0.141.1`
  - `pytest`: `9.1.1`

---

## 2. Monorepo Packaging & Subsystem Status
- **`packages/ocr/` (`nirikshak-ocr` v0.1.0):**
  - Fully implemented standalone direct ONNX Runtime OCR engine (`PP-OCRv3-ROUTED`).
  - Native package discovery verified: installed as editable package in local environment; importable via `import nirikshak_ocr` from repository root, `apps/api/`, and test runners without manual `sys.path` injection.
  - Canonical Default Configuration: `B0_BASELINE_RAW` (`preprocessing_mode="raw"`).
  - Provisional Experimental Configuration: `P_ADAPTIVE_CROP` (`preprocessing_mode="adaptive"`).
- **`packages/shared/` (`nirikshak-shared` v0.1.0):**
  - Shared domain primitives and canonical seam contracts defined in `nirikshak_shared.models.contracts` (`OCRObservation`, `BoundingBox`, `InspectionResult`, etc.).
  - Editable install verified and active.
- **`apps/api/` (Member 4 Gateway):**
  - FastAPI application scaffold in `apps/api/main.py`.
  - Owned by Member 4.
  - Exposes `/health` and `/api/v1/inspections`.
  - Synchronous MVP architecture (no Celery, no Redis, no message brokers).
- **`apps/worker/` (Pipeline Scaffold):**
  - Synchronous `InspectionPipelineWorker` class in `apps/worker/main.py`.
  - No background queue infrastructure (Celery/Redis explicitly excluded from MVP scope).

---

## 3. Test Suite & Verification Baseline
- **Passing Tests:** **73 passed / 73 total (100% pass rate in 6.36s)**.
- **Coverage Areas:**
  - OCR Engine comprehensive tests (detection, recognition, ordering, invalid inputs): 15 tests.
  - Preprocessing filters (CLAHE, bilateral, unsharp, dilation, adaptive, safety guards): 9 tests.
  - Precision evaluation (CER, WER, Hindi Unicode, numeric confusions): 6 tests.
  - Chunk 3 regression (polygon invariance, clean text, blank frame, determinism): 4 tests.
  - Chunk 3 hardening (B0 default, routing accuracy isolation, manifest validation, 8-config matrix): 5 tests.
  - Offline isolation verification: 1 test.
  - Shared contracts and downstream smoke tests: 33 tests.

---

## 4. Model Path Resolution & Assets Baseline
- **Detector Weights:** `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx` (2.43 MB)
- **Latin Recognizer Weights:** `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx` (10.69 MB)
- **Devanagari Recognizer Weights:** `models/weights/ocr/rec_hi/rec.onnx` (8.98 MB)
- **Devanagari Dictionary:** `models/weights/ocr/rec_hi/dict.txt` (4,364 lines)
- **Cryptographic Hash Manifest:** `models/manifest.yaml` (verified SHA-256 integrity).
- **Resolution Strategy:** `PROJECT_ROOT` auto-detected by ascending directory hierarchy until `models/` is found, with environment variable override (`METROLENS_ROOT`, `METROLENS_MODELS_DIR`). CWD-independent.

---

## 5. Known Integration Challenges & Objectives for Chunk 4
1. **Service Adapter Boundary:** Deliver a robust `OCRService` interface in `packages/ocr` that encapsulates engine lifecycle, session reuse, input array validation, and timing instrumentation, so that Member 4 can call OCR synchronously without touching ONNX Runtime internals.
2. **Contract Compatibility:** Ensure seamless conversion between `OCRResult`/`OCRToken` and `nirikshak_shared.models.contracts.OCRObservation`, preserving 4-point pixel polygons and verbatim UTF-8 Devanagari Unicode.
3. **Engine Reusability:** Guarantee singleton / long-lived session reuse across multiple HTTP requests (preventing per-request model reload).
4. **Structured Error Translation:** Map internal engine errors (`ModelLoadError`, `InvalidImageError`, `InferenceError`) to clear service errors that Member 4 can map to HTTP status codes.
5. **Preserve Synchronous MVP Architecture:** Exclude all Celery, Redis, and RabbitMQ scaffolding. Maintain zero legal metrology logic and zero physical mm calibration in OCR.
