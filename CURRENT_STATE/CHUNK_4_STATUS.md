# CURRENT STATE: CHUNK 4 STATUS
**Document:** `CURRENT_STATE/CHUNK_4_STATUS.md`  
**Generated:** 2026-09-05T05:36:00+05:30  
**Phase:** Member 1 — Chunk 4 (OCR Monorepo Integration, Service Adapter & Contract Verification)  
**Role:** Senior ML/OCR Engineer (Member 1 Lead)  
**Status:** COMPLETE & VERIFIED  

---

## STATUS SUMMARY
- **STATUS:** COMPLETE & VERIFIED
- **CANONICAL DEFAULT:** `B0_BASELINE_RAW` (`preprocessing_mode="raw"`)
- **PROVISIONAL POLICY:** `P_ADAPTIVE_CROP` (`preprocessing_mode="adaptive"`, conditional CLAHE on low-contrast crops)
- **IMPLEMENTED:**
  - Standard monorepo packaging via editable install: `pip install -e packages/shared -e packages/ocr --no-deps`.
  - CWD-independent root directory resolution in `packages/ocr/src/nirikshak_ocr/config.py` using `METROLENS_ROOT` and `METROLENS_MODELS_DIR`.
  - Machine-readable `error_code` attributes across the entire `OCRError` hierarchy and introduced `OCRServiceError` with HTTP status code mapping in `packages/ocr/src/nirikshak_ocr/errors.py`.
  - High-level production service adapter `OCRService` in `packages/ocr/src/nirikshak_ocr/service.py` featuring thread-safe singleton lifecycle (`get_instance()`, `reset_instance()`), polymorphic input normalization (`convert_image_input` with defensive copy), pre-flight warmup (`warmup()`), concurrency execution serialization lock (`_engine_lock`), and shared contract marshalling (`extract_observations()`, `extract_dict()`).
  - Integration benchmark harness in `benchmarks/ocr/chunk4/run_chunk4_integration_benchmark.py`.
  - Comprehensive 16-test integration suite in `tests/integration/test_ocr_service_integration.py`.
- **MEASURED:**
  - Service Adapter Latency: Median **109.64 ms** (path input), **108.84 ms** (bytes input), **113.27 ms** (`to_observations`).
  - Adapter Overhead: **3.04 ms** compared to bare `OCREngine` (106.60 ms median).
  - Concurrency Throughput: **8.81 req/sec** across 4 worker threads (8 requests batch, 908.18 ms total).
  - Memory Footprint: Starts at 71.11 MB RSS, warms to 150.17 MB, plateaus at 296.85 MB under concurrency (bounded below 400 MB worker budget).
- **VALIDATED:**
  - Full repository test suite: **89 passed / 89 total (100% pass rate in 12.93s)**.
  - Contract compliance: Canonical `OCRObservation` instances conform to Pydantic schemas.
  - Geometric invariance: 4-point clockwise quadrilateral polygon coordinates in original image pixel space.
  - Multilingual Unicode: Devanagari text and Indian Rupee symbol (`₹`) survive JSON roundtrips without mojibake.
  - Offline isolation: 100% execution without network calls under socket monkeypatching.
  - Concurrency safety: Zero race conditions or ONNX session corruptions under multi-threaded execution.
- **NOT VALIDATED:** Real-world retail packaging accuracy on physical photographs (0 physical images on disk).
- **BLOCKED:** Real-data benchmark validation remains **BLOCKED (Path B Gate)** awaiting physical photography.
- **UNKNOWN:** Degree of optical specular reflection on metallic foil packaging in real retail environments.
- **NEXT CHUNK:** Chunk 5 (Inspection Pipeline Orchestration, Route Mounting & Deployment Hardening).

---

## 1. IMPLEMENTED
1. `packages/ocr/src/nirikshak_ocr/config.py`: Hardened CWD-independent path discovery (`METROLENS_ROOT`, `METROLENS_MODELS_DIR`), enforced `preprocessing_mode="raw"` as default.
2. `packages/ocr/src/nirikshak_ocr/errors.py`: Standardized `error_code` strings across all exceptions; implemented `OCRServiceError` with `status_code`.
3. `packages/ocr/src/nirikshak_ocr/service.py`: Implemented `OCRService` adapter with singleton pattern, input normalization, engine execution lock, and observation serializers.
4. `packages/ocr/src/nirikshak_ocr/__init__.py`: Exported `OCRService` and `OCRServiceError`.
5. Monorepo Editable Installation: Registered `nirikshak-shared` and `nirikshak-ocr` via `pip install -e`.
6. `benchmarks/ocr/chunk4/run_chunk4_integration_benchmark.py`: Performance and memory benchmark runner.
7. `benchmarks/ocr/chunk4/integration_results.json`: Machine-readable integration benchmark artifacts.
8. `benchmarks/ocr/chunk4/README.md`: Integration benchmark documentation.
9. `tests/integration/test_ocr_service_integration.py`: 16 comprehensive service integration tests.

---

## 2. MEASURED
- **Cold Load Time:** Bare Engine: **270.30 ms** | Service Adapter: **267.66 ms**.
- **Inference Latency (Windows 11 AMD64, 4 intra-op threads):**
  - Direct `OCREngine`: Mean 108.66 ms, Median **106.60 ms**, P95 121.11 ms.
  - `OCRService` (Path): Mean 112.74 ms, Median **109.64 ms**, P95 132.18 ms.
  - `OCRService` (Bytes): Mean 108.10 ms, Median **108.84 ms**, P95 113.40 ms.
  - `OCRService` (`to_observations`): Mean 114.29 ms, Median **113.27 ms**, P95 121.83 ms.
  - Adapter Overhead: **3.04 ms**.
- **Concurrency Throughput:** 8.81 req/sec (4 threads, 8 concurrent requests).
- **Process Memory:** 71.11 MB $\rightarrow$ 150.17 MB (warmed) $\rightarrow$ 296.85 MB (peak concurrency). Bounded inside 400 MB budget.

---

## 3. VALIDATED
- **Test Suite:** 89/89 tests passing (100% pass rate).
- **Input Polymorphism:** Raw bytes, file paths, and numpy arrays supported; defensive copy ensures array immutability.
- **Contract Adherence:** `OCRObservation` and `OCRResult` Pydantic schemas serialized to JSON cleanly.
- **Geometry Invariance:** 4-point clockwise polygon coordinates in original image pixel space.
- **Unicode Integrity:** Devanagari Hindi and Indian Rupee symbol (`₹`) preserved without corruption.
- **Thread Safety:** Serialized engine lock prevents race conditions.
- **Offline Readiness:** Confirmed 100% offline via socket isolation.

---

## 4. BLOCKED & UNVALIDATED
- **Real-Data Physical Packaging:** Path B Gate remains active; 0 real packaging images exist on disk.
- **Statutory Legal Compliance:** Handed off to Member 3; zero legal rules inside OCR.
- **Physical Scale Calibration:** Handed off to Member 2; zero mm calibration inside OCR.

---

## 5. GIT STATUS
- Modified/untracked working tree files only.
- **NO GIT COMMITS CREATED. NO GIT PUSH PERFORMED.**
