# Member 1 Final Bug Register: Historical & Forensic Resolution Log

**Project**: MetroLens AI (SIH26034)  
**Phase**: Combined Chunk 6 + Chunk 7 (Final Implementation, Forensic Audit & Freeze)  
**Date**: September 2026  
**Status**: 100% RESOLVED & CLOSED (Zero Open Bugs)

---

## 1. Overview & Forensic Summary

This register provides the definitive forensic record of all defects, architectural challenges, and edge cases encountered, triaged, and permanently resolved across the entire Member 1 lifecycle (Chunks 1 through 7).

| Bug ID | Severity | Phase Discovered | Component | Resolution State |
| :--- | :--- | :--- | :--- | :--- |
| **BUG-M1-001** | CRITICAL | Chunk 1 | Engine / Dependencies | RESOLVED (Direct ONNX Runtime) |
| **BUG-M1-002** | HIGH | Chunk 2 | Multilingual Recognition | RESOLVED (Dual-Route Rec + Dict) |
| **BUG-M1-003** | MEDIUM | Chunk 3 | Path Resolution | RESOLVED (CWD-Independent Traversal) |
| **BUG-M1-004** | MEDIUM | Chunk 4 | Documentation / Hygiene | RESOLVED (RapidOCR Excision) |
| **BUG-M1-005** | HIGH | Chunk 4 | Memory Safety | RESOLVED (Defensive Copy Guard) |
| **BUG-M1-006** | HIGH | Chunk 6 | Security / DoS Defense | RESOLVED (64MP Decompression Bomb Guard) |
| **BUG-M1-007** | LOW | Chunk 7 | Test Harness | RESOLVED (Specimen Key Synchronization) |

---

## 2. Detailed Bug Forensic Reports

### BUG-M1-001: PaddleOCR Upstream Build & Dependency Conflicts on Python 3.14
- **Date Discovered**: September 2026 (Chunk 1)
- **Component**: Core OCR Engine Engine Selection
- **Symptoms**: PaddleOCR and PaddlePaddle wheels failed to install on Windows 11 under Python 3.14 due to missing pre-built wheels and MSVC compilation errors.
- **Root Cause**: Heavy third-party framework dependencies tied to older Python C-extensions (Python 3.8-3.11).
- **Resolution**: Eliminated all dependencies on PaddlePaddle and RapidOCR. Re-architected Member 1 to use direct, official ONNX Runtime (`onnxruntime==1.29.0`) CPU execution with raw FP32 ONNX weights.
- **Verification**: Verified zero Paddle imports across codebase; 100% reproducible install via standard `pip`.
- **Status**: **CLOSED - PERMANENT FIX**

---

### BUG-M1-002: Devanagari Glyph Decoding Collisions on Hindi FMCG Packaging
- **Date Discovered**: September 2026 (Chunk 2)
- **Component**: Recognition Pipeline (`nirikshak_ocr.pipeline`)
- **Symptoms**: Hindi text tokens produced empty or garbled characters when passed through standard English PP-OCR recognition models.
- **Root Cause**: Latin recognition dictionary lacks Devanagari Unicode codepoints and complex conjunct tokens.
- **Resolution**: Designed the `PP-OCRv3-ROUTED` dual-recognizer architecture. Shared DBNet++ detector routes Latin crops to `ch_PP-OCRv3_rec_infer.onnx` and Indic crops to `rec.onnx` with a dedicated 708-token dictionary `dict.txt` containing full Hindi Unicode characters and the Indian Rupee symbol (`₹`).
- **Verification**: `test_extract_hindi_devanagari_and_currency_symbol()` passes 100% with exact token matches ("शुद्ध", "मात्रा:", "₹150").
- **Status**: **CLOSED - PERMANENT FIX**

---

### BUG-M1-003: Model & Specimen Path Resolution Fragility Across Working Directories
- **Date Discovered**: September 2026 (Chunk 3)
- **Component**: Configuration Layer (`nirikshak_ocr.config`)
- **Symptoms**: Invoking OCR CLI or pytest from non-root working directories (e.g., `packages/ocr/src` or outside the repo) triggered `FileNotFoundError` for models.
- **Root Cause**: Hardcoded relative paths assumed execution from repository root.
- **Resolution**: Implemented `_default_root()` in `config.py` using parent directory hierarchy traversal (up to 5 levels) searching for anchor markers (`models/manifest.yaml` and `packages/shared`).
- **Verification**: Tested execution from 3 distinct working directories; all paths resolve deterministically.
- **Status**: **CLOSED - PERMANENT FIX**

---

### BUG-M1-004: Lingering RapidOCR Mentions in Documentation and Test Stubs
- **Date Discovered**: September 2026 (Chunk 4)
- **Component**: Package Documentation & Source Hygiene
- **Symptoms**: `packages/ocr/README.md` and docstrings contained references to RapidOCR despite the complete migration to direct ONNX Runtime.
- **Root Cause**: Incomplete cleanup during rapid phase transitions.
- **Resolution**: Conducted comprehensive codebase audit. Cleaned `packages/ocr/README.md` and all docstrings to accurately document the pure direct ONNX Runtime architecture.
- **Verification**: Recursive grep confirms zero occurrences of `rapidocr` in all documentation and source code.
- **Status**: **CLOSED - PERMANENT FIX**

---

### BUG-M1-005: Potential In-Place Image Mutation by Downstream Components
- **Date Discovered**: September 2026 (Chunk 4)
- **Component**: Image Ingress Layer (`OCRService.convert_image_input`)
- **Symptoms**: When caller supplied a `numpy.ndarray`, subsequent preprocessing operations could mutate the caller's array buffer in place.
- **Root Cause**: Direct assignment without defensive cloning.
- **Resolution**: Added `image.copy()` in `convert_image_input()` ensuring caller's array is strictly immutable.
- **Verification**: Added `test_input_array_immutability()` in `test_ocr_service_integration.py` which verifies bit-exact SHA-256 hash preservation of the input array.
- **Status**: **CLOSED - PERMANENT FIX**

---

### BUG-M1-006: Denial-of-Service Risk via Massive Decompression Bombs
- **Date Discovered**: September 2026 (Chunk 6)
- **Component**: Service Ingress Guard (ADR-014)
- **Symptoms**: Extremely large images (e.g., >64 Megapixels) could cause memory exhaustion (OOM) or system instability on edge devices.
- **Root Cause**: Unbounded image dimension ingestion prior to memory allocation.
- **Resolution**: Implemented explicit 64 Megapixel threshold check (`width * height > 64,000,000`) across all input modalities (byte buffers, file paths, and numpy arrays) raising strongly typed `UnsupportedImageError`.
- **Verification**: Added `test_decompression_bomb_guard()` verifying immediate rejection in < 1 ms without memory leaks.
- **Status**: **CLOSED - PERMANENT FIX**

---

### BUG-M1-007: Specimen Key Discrepancy in Final Benchmark Test Harness
- **Date Discovered**: September 2026 (Chunk 7)
- **Component**: Benchmark Suite (`benchmarks/ocr/final/run_final_benchmark.py`)
- **Symptoms**: Benchmark script referenced non-existent filename `SYNTH-03-BILINGUAL-FMCG.png` instead of canonical `SYNTH-03-MIXED-BILINGUAL.png`.
- **Root Cause**: Typo in harness dictionary mapping.
- **Resolution**: Synchronized benchmark specimen definitions with canonical dataset files in `03_DATASET/images/`.
- **Verification**: Benchmark script runs to completion and processes all 4 specimens across 20 iterations each without errors.
- **Status**: **CLOSED - PERMANENT FIX**

---

## 3. Final Defect Metrics & Freeze Verdict

- **Total Defects Identified**: 7
- **Defects Resolved**: 7 (100%)
- **Open Defects**: 0
- **Regression Bugs**: 0
- **Freeze Status**: **CLEAN — ZERO DEFECT DEFENSE CERTIFIED**.
