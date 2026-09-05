# CURRENT STATE: CHUNK 3 STATUS
**Document:** `CURRENT_STATE/CHUNK_3_STATUS.md`  
**Generated:** 2026-09-05T05:21:00+05:30  
**Phase:** Member 1 — Chunk 3 (Real-Data OCR Validation, Domain Preprocessing & Robustness)  
**Role:** Senior ML/OCR Engineer (Member 1 Lead)  
**Status:** COMPLETE (PATH B: REAL DATA BLOCKED)  

---

## STATUS SUMMARY
- **STATUS:** COMPLETE (PATH B: REAL DATA BLOCKED)
- **CANONICAL DEFAULT:** `B0_BASELINE_RAW` (`preprocessing_mode="raw"`)
- **PROVISIONAL POLICY:** `P_ADAPTIVE_CROP` (`preprocessing_mode="adaptive"`, conditional CLAHE on low-contrast crops)
- **IMPLEMENTED:** Domain-specific preprocessing pipeline (`packages/ocr/src/nirikshak_ocr/preprocessing.py`) with CLAHE, bilateral filter, unsharp mask, morphological dilation, and adaptive crop contrast; precision evaluation engine (`packages/ocr/src/nirikshak_ocr/evaluation.py`) with CER, WER, numeric extraction, digit CER, script routing accuracy (`compute_routing_accuracy`), error taxonomy classifier; dataset schemas & manifest registry (`data/manifests/real_packaging_manifest.json`, `ground_truth_benchmark.json`); manifest validator (`tools/validate_dataset_manifest.py`); visual error overlay generator (`benchmarks/ocr/chunk3/visualize_errors.py`); benchmark harness (`benchmarks/ocr/chunk3/run_chunk3_benchmark.py`).
- **MEASURED:** Baseline B0 (88.70 ms median, 0.2124 CER, 0.6038 WER, 75.9% field accuracy, 83.8% routing accuracy), P2 CLAHE (100.97 ms median, 0.2250 CER), P-Adaptive (90.14 ms median, 0.2184 CER, 75.9% field accuracy, 83.8% routing accuracy), RSS memory (70.77 MB $\rightarrow$ 99.11 MB, +28.34 MB across 72 total passes, bounded memory footprint).
- **VALIDATED:** 73 repository tests passing (100%), coordinate and polygon invariance under crop preprocessing confirmed (0.0px distortion, `atol=0.01`), negative tests on clean & blank packaging passed, determinism verified across repeated runs, offline execution confirmed under socket isolation.
- **NOT VALIDATED:** Empirical accuracy on authentic physical retail packaging (0 real images exist on disk).
- **BLOCKED:** Real-world retail packaging benchmark validation is **BLOCKED** awaiting physical specimen collection by Member 6.
- **UNKNOWN:** Degree of font distortion, specular glare patterns, and non-standard Hindi typography across unconstrained regional Indian retail brands.
- **NEXT CHUNK:** Chunk 4 (Monorepo Integration & API Service Layer).

---

## 1. IMPLEMENTED
1. `packages/ocr/src/nirikshak_ocr/config.py`: Added typed preprocessing parameters (`preprocessing_mode`, `preprocess_target`, `clahe_clip_limit`, `clahe_tile_grid_size`, `bilateral_d`, `bilateral_sigma_color`, `bilateral_sigma_space`, `unsharp_amount`, `dilation_kernel_size`, `dilation_iterations`, `adaptive_contrast_threshold`). Default set to `raw`.
2. `packages/ocr/src/nirikshak_ocr/preprocessing.py`: Added `apply_clahe`, `apply_bilateral_filter`, `apply_unsharp_mask`, `apply_morphological_dilation`, `apply_adaptive_preprocessing`, and `DomainPreprocessPipeline`.
3. `packages/ocr/src/nirikshak_ocr/engine.py`: Integrated `crop_preprocessor_hook` and `preprocessor_hook` with clean configuration dispatch and polygon coordinate immutability.
4. `packages/ocr/src/nirikshak_ocr/evaluation.py`: Added `levenshtein_distance`, `compute_cer`, `compute_wer`, `evaluate_numeric_accuracy`, `classify_ocr_error`, and `compute_routing_accuracy`.
5. `packages/ocr/src/nirikshak_ocr/__init__.py`: Exported public preprocessing and evaluation symbols.
6. `data/manifests/real_packaging_manifest.json`: Machine-readable dataset registry schema for 35 canonical retail SKUs (25 dev / 10 holdout).
7. `data/manifests/ground_truth_benchmark.json`: Machine-readable ground truth annotation specification.
8. `tools/validate_dataset_manifest.py`: Automated manifest and SKU-disjoint partition verification tool distinguishing `PASS_EMPTY_BLOCKED` from `PASS_VALID_POPULATED`.
9. `benchmarks/ocr/chunk3/run_chunk3_benchmark.py`: Reproducible benchmark harness evaluating 8 configurations across 8 specimens (72 total passes).
10. `benchmarks/ocr/chunk3/visualize_errors.py`: Visual debug overlay generator rendering polygons, transcriptions, and error taxonomy labels.

---

## 2. MEASURED
- **Inference Latency (4 CPU threads, 72 passes):**
  - B0 Baseline Raw: Median **88.70 ms** (P95: 116.80 ms)
  - P-Adaptive Crop: Median **90.14 ms** (P95: 110.43 ms)
  - P5 Dilation Crop: Median **94.28 ms** (P95: 114.01 ms)
  - P4 Unsharp Crop: Median **94.40 ms** (P95: 121.14 ms)
  - P6 Combo Crop: Median **96.69 ms** (P95: 130.36 ms)
  - P2 CLAHE Crop: Median **100.97 ms** (P95: 134.28 ms)
  - P-Image CLAHE (Whole image): Median **100.99 ms** (P95: 117.47 ms)
  - P3 Bilateral Crop: Median **101.84 ms** (P95: 150.38 ms)
- **Error Rates (Synthetic Regression Harness):**
  - Baseline B0 CER: **0.2124** | WER: **0.6038** | Routing Acc: **83.8%**
  - P-Adaptive CER: **0.2184** | WER: **0.6446** | Routing Acc: **83.8%**
- **Statutory Field Accuracy:** **75.9%** (B0 and P-Adaptive tie)
- **Numeric Accuracy:** **42.9%** exact match (identified 0/O, 1/I/l confusions; allocated to Member 3 regex parser)
- **Memory Footprint:** 70.77 MB $\rightarrow$ 99.11 MB (+28.34 MB delta over 72 passes, stable plateau).

---

## 3. VALIDATED
- **Test Suite Pass Rate:** 73 passed / 73 total (100% pass across tests, packages, and apps).
- **Coordinate Invariance:** Verified in `test_polygon_invariance_under_crop_preprocessing` (0.0px distortion, `atol=0.01`).
- **Clean Specimen Safety:** Verified in `test_clean_packaging_negative_test_no_hallucination` (no hallucinated tokens).
- **Blank Frame Specificity:** Verified in `test_blank_frame_zero_tokens` (0 false tokens).
- **Determinism:** Verified across repeated identical runs.
- **Offline Guarantee:** Maintained 100% local execution with zero network egress.
- **Hardening Assertions:** Default B0 baseline, decoupled script routing accuracy, manifest validation states, and 8-configuration counts verified in `tests/unit/test_ocr_chunk3_hardening.py`.
