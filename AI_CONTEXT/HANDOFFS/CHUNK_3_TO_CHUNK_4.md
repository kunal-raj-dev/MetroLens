# ENGINEERING HANDOFF: CHUNK 3 TO CHUNK 4
**Document:** `AI_CONTEXT/HANDOFFS/CHUNK_3_TO_CHUNK_4.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 1 (Chunk 4 — Integration & API Services) & Downstream Monorepo Leads  
**Date:** 2026-09-05T05:04:00+05:30  
**Status:** FROZEN & READY FOR CHUNK 4  

---

## 1. Final OCR Configuration
- **Model Engine:** `PP-OCRv3-ROUTED`
- **Detector:** Direct ONNX Runtime DBNet++ (`models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx`, 2.43 MB)
- **Latin Recognizer:** Direct ONNX Runtime SVTR-EN (`models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx`, 10.69 MB)
- **Devanagari Recognizer:** Direct ONNX Runtime SVTR-HI (`models/weights/ocr/rec_hi/rec.onnx`, 8.98 MB) + Dictionary (`dict.txt`)
- **Default Threading:** 4 CPU intra-op threads
- **Execution Provider:** `CPUExecutionProvider` (100% offline, zero network reliance)

## 2. Preprocessing Policy
- **Canonical Production Default:** `B0_BASELINE_RAW` (`preprocessing_mode="raw"`). Raw identity passthrough ensures zero risk of character degradation on normal retail packaging and achieved superior aggregate Macro CER (0.2124) and WER (0.6038).
- **Provisional Experimental Candidate:** `P_ADAPTIVE_CROP` (`preprocessing_mode="adaptive"`). Retained for low-contrast or faded packaging (triggers CLAHE when crop luminance standard deviation $\sigma_{\text{luma}} < 35.0$).
- **Coordinate Invariance:** Crop-level processing guarantees 0.0px distortion of detector polygon coordinates and bounding envelopes (`atol=0.01`).
- **Rejected Methods:** Blanket whole-image filtering (`P_IMAGE_CLAHE`) and unconditional morphological dilation (`P6_COMBO_CLAHE_DILATE`) are strictly rejected for default inference.


## 3. Real-Data Results & Blocker Status
- **Disk Audit:** `data/raw/` contains **0 real physical packaging images** on disk.
- **Status:** **REAL-DATA VALIDATION BLOCKED** (Path B Gate).
- **Synthetic Regression Baseline:** Evaluated against 8 controlled synthetic packaging specimens (`SYNTH-01` through `SYNTH-08`).
- **Macro CER:** 0.2124 (B0 Raw) / 0.2184 (P-Adaptive).
- **Macro WER:** 0.6038 (B0 Raw) / 0.6446 (P-Adaptive).
- **Statutory Field Accuracy:** 75.9% across evaluated declarations.

## 4. Baseline vs Improved
- **Clean Packaging:** Baseline B0 preserves pristine text. P-Adaptive detects high contrast and leaves text untouched, preventing edge blur.
- **Low-Contrast Faded Print:** Adaptive CLAHE enhances local edge separation on faded metallic foil packaging (`SYNTH-08`).
- **Latency Tradeoff:** Minimal overhead (+3.5 ms median latency delta) compared to +5.2 ms for whole-image CLAHE.

## 5. Known Failure Modes
1. **CTC Numeric Confusions:** Visual confusion of `0`/`O`, `1`/`I`/`l`, and `5`/`S`. Requires downstream regex parsing with digit preference in currency/weight fields.
2. **Cylindrical Distortion:** Curved text on bottles/cans degrades OCR without geometric rectification. Member 2 unwarping is required.
3. **Severe Specular Glare:** Completely white overexposed regions cannot be reconstructed; upstream vision quality gate must request retake.

## 6. Recommended Regression Set
- Unit tests: `tests/unit/test_ocr_preprocessing.py`, `tests/unit/test_ocr_evaluation.py`, `tests/unit/test_ocr_chunk3_regression.py`.
- Benchmark harness: `benchmarks/ocr/chunk3/run_chunk3_benchmark.py`.
- Dataset manifest validator: `tools/validate_dataset_manifest.py`.

## 7. Performance
- **Cold Load Latency:** 283.66 ms
- **Warm Inference Latency:** Median **90.76 ms** (P95: 115.51 ms) on 4 CPU threads.
- Sub-200ms CPU budget easily satisfied.

## 8. Memory
- Starting RSS: 70.77 MB
- Post-Benchmark RSS: 99.11 MB (+28.34 MB across 72 continuous inference passes).
- Bounded memory footprint; comfortably stays under the 400 MB worker budget.


## 9. Hindi Status
- Pure Hindi packaging (`SYNTH-02`) achieved **0.3125 CER**.
- Critical declarations extracted: `"अधिकतम खुदरा मूल्य: ₹ 245.00"`, `"निवल मात्रा: 5 किग्रा"`, `"पैकिंग तिथि: 05/2026"`.
- Script router accurately directs Devanagari crops to SVTR-HI session.

## 10. Numeric OCR Status
- Digits and decimal points captured across all statutory fields.
- CTC decoder character ambiguity requires Member 3 rule parser context.

## 11. Integration Notes
Chunk 4 and downstream services can consume the engine via:
```python
from nirikshak_ocr import OCREngine, OCRConfig, OCRResult

config = OCRConfig(
    preprocessing_mode="adaptive",
    preprocess_target="crop",
    intra_op_num_threads=4
).resolve_paths()

engine = OCREngine(config)
result: OCRResult = engine.extract(image, image_id="sample_001")
```

## 12. What Chunk 4 Should Build
1. Service layer endpoints in `apps/api` (`POST /api/v1/inspect/ocr`).
2. Celery worker pipeline tasks in `apps/worker` for bulk background audits.
3. End-to-end integration tests between OCR, Calibration (Member 2), and Rules Engine (Member 3).

## 13. What Chunk 4 MUST NOT Rebuild
- ❌ **DO NOT** replace or rebuild the direct ONNX Runtime OCR subsystem.
- ❌ **DO NOT** modify DBNet++ or SVTR inference loops.
- ❌ **DO NOT** introduce external third-party OCR wrappers (`rapidocr-onnxruntime`).
- ❌ **DO NOT** hardcode legal compliance rules or physical mm conversions inside the OCR engine.
