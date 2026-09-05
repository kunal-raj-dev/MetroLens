# CURRENT STATE: CHUNK 3 CORRECTION BASELINE
**Document:** `CURRENT_STATE/CHUNK_3_CORRECTION_BASELINE.md`  
**Generated:** 2026-09-05T05:20:00+05:30  
**Phase:** Member 1 — Chunk 3 Correction & Engineering Hardening  
**Scope:** Technical Audit, Baseline Verification, Benchmark Integrity & Reconciliation  

---

## 1. Engine Configuration Baseline
The Nirikshak OCR engine (`packages/ocr`) is hard-coded with the following verified baseline:
- **Default Preprocessing:** `raw` (Identity hook, zero pixel mutation prior to detection and crop recognition).
- **Default Target:** `crop` (When non-raw preprocessing is selected, it operates exclusively on rotated bounding crops, leaving whole-image detector polygons invariant).
- **Configuration Defaults:**
  - `clahe_clip_limit`: 2.0
  - `clahe_tile_grid_size`: (8, 8)
  - `bilateral_d`: 5
  - `bilateral_sigma_color`: 50.0
  - `bilateral_sigma_space`: 50.0
  - `unsharp_amount`: 1.5
  - `dilation_kernel_size`: 2
  - `dilation_iterations`: 1
  - `adaptive_contrast_threshold`: 35.0

## 2. Benchmark Artifacts Summary
The benchmark harness (`benchmarks/ocr/chunk3/run_chunk3_benchmark.py`) systematically executes 8 configurations across 8 synthetic specimens (64 evaluated passes + 8 warmup passes = 72 total passes):
- **B0_BASELINE_RAW:** Macro CER 0.2124 | WER 0.6038 | Field Acc 75.9% | Num Acc 42.9% | Script Routing Acc 83.8% | Median Latency 88.7 ms (CANONICAL DEFAULT)
- **P2_CLAHE_CROP:** Macro CER 0.2250 | WER 0.6504 | Field Acc 75.9% | Num Acc 42.9% | Script Routing Acc 83.8% | Median Latency 101.0 ms (BENEFICIAL_FOR_LOW_CONTRAST)
- **P3_BILATERAL_CROP:** Macro CER 0.2304 | WER 0.6446 | Field Acc 75.9% | Num Acc 42.9% | Script Routing Acc 86.5% | Median Latency 101.8 ms (OPTIONAL_DOMAIN_FILTER)
- **P4_UNSHARP_CROP:** Macro CER 0.2173 | WER 0.6089 | Field Acc 75.9% | Num Acc 42.9% | Script Routing Acc 83.8% | Median Latency 94.4 ms (OPTIONAL_DOMAIN_FILTER)
- **P5_DILATION_CROP:** Macro CER 0.2288 | WER 0.6446 | Field Acc 75.9% | Num Acc 42.9% | Script Routing Acc 86.5% | Median Latency 94.3 ms (OPTIONAL_DOMAIN_FILTER)
- **P6_COMBO_CLAHE_DILATE:** Macro CER 0.2443 | WER 0.6587 | Field Acc 72.4% | Num Acc 42.9% | Script Routing Acc 89.2% | Median Latency 96.7 ms (OPTIONAL_DOMAIN_FILTER)
- **P_ADAPTIVE_CROP:** Macro CER 0.2184 | WER 0.6446 | Field Acc 75.9% | Num Acc 42.9% | Script Routing Acc 83.8% | Median Latency 90.1 ms (PROVISIONAL_EXPERIMENTAL)
- **P_IMAGE_CLAHE:** Macro CER 0.2157 | WER 0.6242 | Field Acc 75.9% | Num Acc 42.9% | Script Routing Acc 83.8% | Median Latency 101.0 ms (REJECTED_BLANKET_OVERHEAD)

## 3. Dataset Integrity
- **Real Data Status:** `BLOCKED_AWAITING_PHYSICAL_DATA_COLLECTION` (Path B Gate enforced).
- **Physical Images on Disk:** 0 real retail packaging images.
- **Canonical Dataset Target:** 35 FMCG retail SKUs (25 development / 10 holdout).
- **Leakage Prevention:** Strict SKU-disjoint partition enforced. Multiple photos of the same SKU are constrained to either dev or holdout.
- **Schema Validation:** `tools/validate_dataset_manifest.py` verifies manifest format and reports `PASS_EMPTY_BLOCKED` when 0 records are registered under a blocked status.
