# MEMBER 1 ASSET INVENTORY

**Subsystem**: Member 1 — AI & Multilingual OCR  
**Phase**: Combined Chunk 6 + Chunk 7 Finalization  
**Date**: September 5, 2026  

---

## 1. Source Code Inventory (`packages/ocr/`)

| File Path | Primary Purpose | Active? | Used? | Tested? | Duplicated? | Historical? | Stale? | Keep? | Reason / Disposition |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `packages/ocr/pyproject.toml` | Packaging metadata and build config for `nirikshak-ocr` | YES | YES | YES | NO | NO | NO | **KEEP** | Essential for pip editable installation |
| `packages/ocr/README.md` | Package-level documentation | YES | YES | NO | NO | NO | NO | **KEEP** | Package documentation (remove legacy RapidOCR mention) |
| `packages/ocr/src/nirikshak_ocr/__init__.py` | Package root exports and `NirikshakOCREngine` adapter | YES | YES | YES | NO | NO | NO | **KEEP** | Public API exports and backward compatibility |
| `packages/ocr/src/nirikshak_ocr/config.py` | Typed `OCRConfig` Pydantic model with root resolution | YES | YES | YES | NO | NO | NO | **KEEP** | Central runtime & model path configuration |
| `packages/ocr/src/nirikshak_ocr/detector.py` | `DBNetDetector` using direct ONNX Runtime | YES | YES | YES | NO | NO | NO | **KEEP** | Core scene text line detector |
| `packages/ocr/src/nirikshak_ocr/engine.py` | `OCREngine` orchestrating detection, crop, routing, recognition | YES | YES | YES | NO | NO | NO | **KEEP** | Primary synchronous OCR inference engine |
| `packages/ocr/src/nirikshak_ocr/errors.py` | Typed OCR exception hierarchy (`OCRError`, `ModelLoadError`, etc.) | YES | YES | YES | NO | NO | NO | **KEEP** | Standardized error translation across monorepo |
| `packages/ocr/src/nirikshak_ocr/evaluation.py` | CER, WER, numeric evaluation, Levenshtein distance | YES | YES | YES | NO | NO | NO | **KEEP** | Evaluation & benchmark metrics engine |
| `packages/ocr/src/nirikshak_ocr/preprocessing.py` | Image & crop filters (CLAHE, bilateral, unsharp, dilation, adaptive) | YES | YES | YES | NO | NO | NO | **KEEP** | Domain preprocessing hooks for difficult packaging |
| `packages/ocr/src/nirikshak_ocr/recognizer.py` | `SVTRRecognizer` and `CTCLabelDecoder` | YES | YES | YES | NO | NO | NO | **KEEP** | Alphanumeric & Devanagari CTC text line recognizers |
| `packages/ocr/src/nirikshak_ocr/router.py` | `ScriptRouter` heuristic confidence gate | YES | YES | YES | NO | NO | NO | **KEEP** | Script routing between Latin and Devanagari |
| `packages/ocr/src/nirikshak_ocr/service.py` | `OCRService` thread-safe singleton adapter | YES | YES | YES | NO | NO | NO | **KEEP** | Monorepo service adapter for API & Worker consumption |
| `packages/ocr/src/nirikshak_ocr/types.py` | Pydantic data contracts (`OCRToken`, `OCRResult`, `ScriptType`) | YES | YES | YES | NO | NO | NO | **KEEP** | Internal typed data structures |
| `packages/ocr/src/nirikshak_ocr/utils.py` | Geometric transforms, clockwise ordering, reading order | YES | YES | YES | NO | NO | NO | **KEEP** | Spatial geometry & polygon coordinate utilities |
| `packages/ocr/tests/test_ocr_smoke.py` | Subsystem smoke test | YES | YES | YES | NO | NO | NO | **KEEP** | Package smoke verification |

---

## 2. Model Assets (`models/`)

| File Path | Primary Purpose | Active? | Used? | Tested? | Duplicated? | Historical? | Stale? | Keep? | Reason / Disposition |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `models/manifest.yaml` | Cryptographic model registry, checksums, and licensing metadata | YES | YES | YES | NO | NO | NO | **KEEP** | Canonical model metadata source of truth |
| `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx` | DBNet++ text detector weights (2.32 MB) | YES | YES | YES | NO | NO | NO | **KEEP** | Official PP-OCRv3 detector ONNX model |
| `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx` | SVTR-EN Latin/English recognizer weights (10.19 MB) | YES | YES | YES | NO | NO | NO | **KEEP** | Alphanumeric CTC recognizer with embedded dict |
| `models/weights/ocr/rec_hi/rec.onnx` | SVTR-HI Devanagari recognizer weights (8.56 MB) | YES | YES | YES | NO | NO | NO | **KEEP** | Devanagari Hindi CTC recognizer model |
| `models/weights/ocr/rec_hi/dict.txt` | Devanagari character dictionary (167 characters) | YES | YES | YES | NO | NO | NO | **KEEP** | Character mapping for Hindi CTC decoder |

---

## 3. Test Suites (`tests/`)

| File Path | Primary Purpose | Active? | Used? | Tested? | Duplicated? | Historical? | Stale? | Keep? | Reason / Disposition |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `tests/unit/test_ocr_chunk3_hardening.py` | Chunk 3 hardening tests (routing, baseline, manifests) | YES | YES | YES | NO | NO | NO | **KEEP** | Regression protection for B0 baseline |
| `tests/unit/test_ocr_chunk3_regression.py` | Polygon invariance, blank frames, determinism | YES | YES | YES | NO | NO | NO | **KEEP** | Regression protection for geometry |
| `tests/unit/test_ocr_engine_comprehensive.py` | Comprehensive unit tests for `OCREngine` & edge cases | YES | YES | YES | NO | NO | NO | **KEEP** | Core engine unit coverage |
| `tests/unit/test_ocr_evaluation.py` | CER, WER, Levenshtein, and numeric confusion tests | YES | YES | YES | NO | NO | NO | **KEEP** | Evaluation metric unit coverage |
| `tests/unit/test_ocr_offline.py` | Network isolation test for pure offline execution | YES | YES | YES | NO | NO | NO | **KEEP** | Air-gap verification |
| `tests/unit/test_ocr_preprocessing.py` | Preprocessing filters and adaptive dispatch tests | YES | YES | YES | NO | NO | NO | **KEEP** | Filter validation |
| `tests/unit/test_ocr_types_config.py` | OCRConfig, OCRToken, OCRResult schema tests | YES | YES | YES | NO | NO | NO | **KEEP** | Type safety validation |
| `tests/integration/test_ocr_service_integration.py` | OCRService adapter integration, thread safety, contracts | YES | YES | YES | NO | NO | NO | **KEEP** | Service integration validation |

---

## 4. Benchmark Suites (`benchmarks/ocr/`)

| File Path | Primary Purpose | Active? | Used? | Tested? | Duplicated? | Historical? | Stale? | Keep? | Reason / Disposition |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `benchmarks/ocr/chunk2/` | Chunk 2 thread sweep & CPU memory benchmark | NO | NO | YES | NO | YES | NO | **KEEP** | Historical audit record for Chunk 2 |
| `benchmarks/ocr/chunk3/` | Chunk 3 preprocessing benchmark (8 configs, 72 passes) | NO | NO | YES | NO | YES | NO | **KEEP** | Historical evidence for B0 vs Adaptive |
| `benchmarks/ocr/chunk4/` | Chunk 4 OCRService adapter overhead benchmark | NO | NO | YES | NO | YES | NO | **KEEP** | Historical evidence for service layer |
| `benchmarks/ocr/final/` | **Member 1 Final Benchmark Suite (Current)** | YES | YES | YES | NO | NO | NO | **KEEP** | Authoritative final benchmark record |
