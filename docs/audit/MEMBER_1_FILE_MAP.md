# Member 1 File Map & Asset Inventory

**Project**: MetroLens AI (SIH26034)  
**Phase**: Combined Chunk 6 + Chunk 7 (Final Implementation, Forensic Audit & Freeze)  
**Date**: September 2026  
**Status**: COMPLETE ASSET AUDIT

---

## 1. Core OCR Package (`packages/ocr/`)

| File Path | Role / Responsibility | Status | Dependencies |
| :--- | :--- | :--- | :--- |
| `packages/ocr/pyproject.toml` | Build configuration & dependency definitions | FROZEN | `setuptools`, `wheel` |
| `packages/ocr/README.md` | Architecture, installation, and usage documentation | FROZEN | None |
| `packages/ocr/src/nirikshak_ocr/__init__.py` | Public API surface exports (`OCREngine`, `OCRService`, `OCRConfig`) | FROZEN | Internal modules |
| `packages/ocr/src/nirikshak_ocr/config.py` | Configuration dataclass & CWD-independent model path resolution | FROZEN | `pathlib`, `dataclasses` |
| `packages/ocr/src/nirikshak_ocr/detector.py` | DBNet++ ONNX text detection and polygon contour extraction | FROZEN | `onnxruntime`, `cv2`, `numpy` |
| `packages/ocr/src/nirikshak_ocr/recognizer.py` | Latin & Indic CTC recognition models and dictionary decoder | FROZEN | `onnxruntime`, `cv2`, `numpy` |
| `packages/ocr/src/nirikshak_ocr/pipeline.py` | Dual-recognizer script routing and observation assembly | FROZEN | `detector`, `recognizer` |
| `packages/ocr/src/nirikshak_ocr/engine.py` | Core OCREngine orchestrating detection and recognition | FROZEN | `detector`, `recognizer`, `pipeline` |
| `packages/ocr/src/nirikshak_ocr/service.py` | Thread-safe service adapter, input conversions, DoS guards | FROZEN | `engine`, `nirikshak_shared` |

---

## 2. Shared Data Contracts (`packages/shared/`)

| File Path | Role / Responsibility | Status | Dependencies |
| :--- | :--- | :--- | :--- |
| `packages/shared/pyproject.toml` | Shared package packaging configuration | FROZEN | `setuptools` |
| `packages/shared/src/nirikshak_shared/ocr_contract.py` | Canonical optical observation dataclasses (`OCRObservation`, `OCRResult`, `BoundingPolygon`) | FROZEN | `dataclasses`, `typing` |

---

## 3. Model Assets (`models/`)

| File Path | Role / Responsibility | Size (Bytes) | SHA-256 Checksum |
| :--- | :--- | :--- | :--- |
| `models/manifest.yaml` | Cryptographic SHA-256 verification manifest | 1,460 | Manifest definition |
| `models/ch_PP-OCRv3_det_infer.onnx` | DBNet++ text detection model | 2,432,880 | `3439588c27cfc7a72d3ce6f3c1a26d7088b9ddaa87eb8f16723226dbab3737b5` |
| `models/ch_PP-OCRv3_rec_infer.onnx` | Latin recognition model | 10,690,752 | `897a3ede72ea00e6205e4fb066c0d0c3bfcbfe40b3c662ef4f1db12be3cb80b3` |
| `models/rec.onnx` | Indic Devanagari recognition model | 8,980,224 | `43df175f3a02bbfa254ff92723c34ffc9ce32ff769d2d0b57e7eb3be2bfaf582` |
| `models/dict.txt` | 708-token Hindi dictionary including ₹ | 708 | `b5f1be6d62a259c76e279262fca6f04d7d91df241ba2665e75ab663e6ef68478` |

---

## 4. Test Suite Assets (`tests/`)

| File Path | Role / Responsibility | Test Count | Status |
| :--- | :--- | :--- | :--- |
| `tests/smoke/test_ocr_smoke.py` | Basic engine smoke test & model presence | 4 | PASS |
| `tests/unit/test_ocr_engine.py` | Unit tests for detection, recognition, manifest verification | 8 | PASS |
| `tests/integration/test_ocr_service_integration.py` | Service integration, contracts, bomb guards, threading | 17 | PASS |
| `tests/regression/test_ocr_evaluation.py` | Dataset evaluation & character accuracy regression | 3 | PASS |
| `tests/offline/test_ocr_offline.py` | Network isolation & socket guard verification | 2 | PASS |

---

## 5. Final Benchmark Assets (`benchmarks/ocr/final/`)

| File Path | Role / Responsibility | Status |
| :--- | :--- | :--- |
| `benchmarks/ocr/final/config.json` | Benchmark execution configuration & specimen list | FROZEN |
| `benchmarks/ocr/final/environment.json` | Host platform, runtime, and model environment specification | FROZEN |
| `benchmarks/ocr/final/run_final_benchmark.py` | Benchmark runner measuring cold load, warm latency, concurrency, memory | FROZEN |
| `benchmarks/ocr/final/results.json` | Machine-readable benchmark telemetry and metrics | GENERATED |
| `benchmarks/ocr/final/README.md` | Human-readable markdown summary and performance tables | GENERATED |

---

## 6. Audit & Verification Documentation (`docs/audit/` and `AI_CONTEXT/`)

| File Path | Role / Responsibility | Status |
| :--- | :--- | :--- |
| `docs/audit/MEMBER_1_FINAL_SOURCE_OF_TRUTH.md` | Comprehensive 22-section definitive reference | FROZEN |
| `docs/audit/MEMBER_1_FILE_MAP.md` | This file map | FROZEN |
| `docs/audit/MEMBER_1_REPRODUCIBILITY.md` | Step-by-step developer reproduction guide | FROZEN |
| `docs/audit/MEMBER_1_TRUTH_MATRIX.md` | Claims vs code/test/benchmark evidence | FROZEN |
| `docs/audit/MEMBER_1_FINAL_SCORECARD.md` | Verification status scorecard | FROZEN |
| `docs/audit/MEMBER_1_DO_NOT_REBUILD.md` | Frozen components registry | FROZEN |
| `AI_CONTEXT/EXPERIMENTS/CHUNK_6_7_MEMBER_1_FINAL/06_AUDIT/INDEPENDENT_AUDIT_REPORT.md` | 35-question adversarial audit report | FROZEN |
| `AI_CONTEXT/EXPERIMENTS/CHUNK_6_7_MEMBER_1_FINAL/05_TESTS/M1_FINAL_TEST_MATRIX.md` | Comprehensive M1-001–M1-018 test matrix | FROZEN |
| `AI_CONTEXT/EXPERIMENTS/CHUNK_6_7_MEMBER_1_FINAL/07_DEBUG/M1_FINAL_BUG_REGISTER.md` | Defect history and resolution log | FROZEN |
| `AI_CONTEXT/EXPERIMENTS/CHUNK_6_7_MEMBER_1_FINAL/08_VALIDATION/M1_FINAL_LIMITATIONS.md` | Boundaries and Path B specification | FROZEN |
| `AI_CONTEXT/EXPERIMENTS/CHUNK_6_7_MEMBER_1_FINAL/08_VALIDATION/M1_FINAL_VALIDATION_MATRIX.md` | Requirements validation mapping | FROZEN |
| `AI_CONTEXT/EXPERIMENTS/CHUNK_6_7_MEMBER_1_FINAL/09_DOCUMENTATION/FINAL_M1_ARCHITECTURE.md` | Architecture specification & diagrams | FROZEN |
| `AI_CONTEXT/EXPERIMENTS/CHUNK_6_7_MEMBER_1_FINAL/11_FREEZE/M1_FINAL_CHANGELOG.md` | Historical changelog (Chunks 1–7) | FROZEN |
| `AI_CONTEXT/EXPERIMENTS/CHUNK_6_7_MEMBER_1_FINAL/11_FREEZE/M1_FREEZE_MANIFEST.md` | Cryptographic freeze manifest | FROZEN |
| `AI_CONTEXT/EXPERIMENTS/CHUNK_6_7_MEMBER_1_FINAL/11_FREEZE/MEMBER_1_FINAL_ENGINEERING_REPORT.md` | Complete 31-section engineering report | FROZEN |
