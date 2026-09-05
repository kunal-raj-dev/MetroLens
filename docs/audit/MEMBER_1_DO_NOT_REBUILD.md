# MEMBER 1 — DO NOT REBUILD: FROZEN SUBSYSTEM MANIFEST

**Subsystem**: Member 1 — AI & Multilingual OCR (`packages/ocr`)  
**Auditor**: Independent Principal Engineer  
**Status**: AUDITED, HARDENED & FROZEN  
**Notice to Team**: The components specified in this document are **FROZEN**. Downstream members (Member 2, Member 3, Member 4, Member 5, Member 6) must consume these interfaces as-is and **MUST NOT** rewrite, redesign, or refactor them.

---

## 1. Frozen Components (DO NOT REBUILD)

### A. Core OCR Engine (`nirikshak_ocr.OCREngine`)
- **Location**: `packages/ocr/src/nirikshak_ocr/engine.py`
- **What it does**: Executes direct ONNX Runtime DBNet++ text line detection and SVTR script-routed recognition on CPU.
- **Why it is frozen**: Audited with 108 automated tests, zero dependencies on RapidOCR/Paddle runtime, and verified bounded memory.
- **Rules**: Do NOT wrap with alternative engines. Do NOT reintroduce Tesseract, EasyOCR, or cloud APIs.

### B. Production Service Adapter (`nirikshak_ocr.OCRService`)
- **Location**: `packages/ocr/src/nirikshak_ocr/service.py`
- **What it does**: Thread-safe singleton lifecycle management (`OCRService.get_instance()`), input normalization (paths, bytes, numpy arrays), caller memory protection (immutability), and exception translation.
- **Why it is frozen**: Already consumed by `apps/api/main.py` and `apps/worker/main.py`.
- **Rules**: Consume `OCRService.get_instance().extract()`, `extract_observations()`, or `extract_dict()`. Do NOT create redundant engine wrapper classes.

### C. Neural Runtime & Execution Provider
- **Runtime**: Direct `onnxruntime==1.29.0`
- **Provider**: `CPUExecutionProvider` (intra-op threads: 4, inter-op threads: 1)
- **Why it is frozen**: Verified 100% offline, air-gapped, zero remote telemetry, zero GPU dependencies.
- **Rules**: Do NOT switch execution providers without formal profiling and GPU compatibility checks.

### D. Model Weights & Manifest
- **Detector**: `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx` (SHA-256: `3439588c030faea393a54515f51e983d8e155b19a2e8aba7891934c1cf0de526`)
- **Latin Recognizer**: `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx` (SHA-256: `897a3ededb38fee0dae2c1ccee38241f37df202c9509e3abca02e9217c5ee615`)
- **Devanagari Recognizer**: `models/weights/ocr/rec_hi/rec.onnx` (SHA-256: `43df175fa3c877fbf7bcc4e5bd1e203e24ec450cd3ea96c9e802c86e39a4d4cf`)
- **Hindi Dictionary**: `models/weights/ocr/rec_hi/dict.txt` (SHA-256: `b5f1be6d8bbff1a19fb96c5d4ca96a423380234bb7d2ce0e07b5838adb4d18ea`)
- **Manifest**: `models/manifest.yaml`
- **Rules**: Do NOT replace or modify model weights without updating `manifest.yaml` and re-running the full test and benchmark suite.

### E. Coordinate Convention & Geometry Contract
- **Space**: Original input image pixel coordinates (unnormalized).
- **Origin**: Top-left corner `(0.0, 0.0)`.
- **Polygon**: 4-point quadrilateral `[[x1,y1], [x2,y2], [x3,y3], [x4,y4]]` ordered clockwise: `[top-left, top-right, bottom-right, bottom-left]`.
- **Bounding Box**: Derived axis-aligned envelope `[xmin, ymin, xmax, ymax]`.
- **Raw Height**: Average side-edge height in original image pixels.
- **Rules**: Member 2 MUST consume these coordinates directly for metric calibration. Do NOT re-normalize or invert axes.

### F. Canonical Seam Contracts
- **`OCRObservation`**: `nirikshak_shared.models.contracts.OCRObservation`
- **`OCRToken`**: `nirikshak_ocr.types.OCRToken`
- **`OCRResult`**: `nirikshak_ocr.types.OCRResult`
- **Rules**: Downstream members (Member 3 Rule Engine, Member 4 API/Dossier, Member 5 Canvas) must consume these typed DTOs.

### G. Standard Verification & Benchmark Commands
- **Full Test Suite**: `python -m pytest` (108 tests)
- **Benchmark Suite**: `python benchmarks/ocr/final/run_final_benchmark.py`

---

## 2. Changes Requiring Deliberate Architecture Review

Any of the following changes **CANNOT** be made arbitrarily and require formal multi-member RFC approval:
1. Adding a new OCR engine or third-party OCR library.
2. Modifying the coordinate space, vertex ordering, or polygon contract.
3. Introducing network calls, telemetry, or remote API dependencies into Member 1.
4. Altering the default preprocessing mode from `B0_BASELINE_RAW`.
5. Modifying ONNX execution provider settings or thread counts in production configs.
6. Introducing legal rule evaluation or metric physical millimeter conversions into `nirikshak_ocr`.
