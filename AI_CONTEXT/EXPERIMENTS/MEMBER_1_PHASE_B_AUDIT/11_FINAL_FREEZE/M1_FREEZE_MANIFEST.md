# MEMBER 1 — FINAL FREEZE MANIFEST

**Subsystem**: Member 1 — AI & Multilingual OCR (`packages/ocr`)  
**Lead**: Member 1 Lead  
**Auditor**: Independent Principal Engineer  
**Date**: 2026-09-05  
**Freeze Status**: `M1 FINAL — READY WITH KNOWN LIMITATIONS`  

---

## 1. Final Architecture
- **Engine**: `PP-OCRv3-ROUTED` (DBNet++ text line detection + SVTR script-routed recognition)
- **Routing**: Heuristic confidence gate between SVTR-EN (Latin) and SVTR-HI (Devanagari)
- **Service**: `nirikshak_ocr.OCRService` (thread-safe singleton lifespan adapter)
- **Package**: `nirikshak_ocr` (installed in editable mode, zero `sys.path` hacks)

## 2. Final Runtime
- **Inference Engine**: Direct `onnxruntime==1.29.0`
- **Execution Provider**: `CPUExecutionProvider` (intra-op threads: 4, inter-op threads: 1)
- **Framework Overhead**: Zero PyTorch, zero TensorFlow, zero Paddle runtime, zero RapidOCR wrapper in production inference path.
- **Offline Enforcement**: 100% local, air-gapped, zero network calls.

## 3. Final Models & Verified SHA-256 Hashes
All assets reside locally under `models/weights/ocr/` matching `models/manifest.yaml` 100%:

| Model Identifier | File Path | Size (Bytes) | SHA-256 Hash | License |
| :--- | :--- | :--- | :--- | :--- |
| `ch_PP-OCRv3_det_infer` | `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx` | 2,432,880 | `3439588c030faea393a54515f51e983d8e155b19a2e8aba7891934c1cf0de526` | Apache-2.0 |
| `ch_PP-OCRv3_rec_infer` | `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx` | 10,690,752 | `897a3ededb38fee0dae2c1ccee38241f37df202c9509e3abca02e9217c5ee615` | Apache-2.0 |
| `hindi_PP-OCRv3_rec_infer` | `models/weights/ocr/rec_hi/rec.onnx` | 8,980,224 | `43df175fa3c877fbf7bcc4e5bd1e203e24ec450cd3ea96c9e802c86e39a4d4cf` | Apache-2.0 |
| `hindi_dict` | `models/weights/ocr/rec_hi/dict.txt` | 508 | `b5f1be6d8bbff1a19fb96c5d4ca96a423380234bb7d2ce0e07b5838adb4d18ea` | Apache-2.0 |

## 4. Final Contract
- **Token Model**: `nirikshak_ocr.types.OCRToken`
  - `token_id: str` (e.g. `tok_001`)
  - `text: str` (transcribed characters, Unicode NFC normalized)
  - `confidence: float` (CTC mean probability in `[0.0, 1.0]`)
  - `polygon: List[List[float]]` (4-point clockwise quad in unnormalized image pixels)
  - `bbox: List[float]` (derived `[xmin, ymin, xmax, ymax]`)
  - `script: ScriptType` (`latin`, `devanagari`, `unknown`)
  - `line_id: int` (sequential reading-order line index)
  - `raw_pixel_height: float` (quadrilateral average height in pixels; NOT physical mm)
- **Canonical Inter-Package DTO**: `nirikshak_shared.models.contracts.OCRObservation`
- **API/UI Payload**: `OCRService.extract_dict()` returning tokens, observations, and telemetry.

## 5. Final Default Configuration
```python
OCRConfig(
    runtime_provider="CPUExecutionProvider",
    intra_op_num_threads=4,
    inter_op_num_threads=1,
    enable_warmup=False,
    max_side_len=960,
    det_db_thresh=0.3,
    det_db_box_thresh=0.5,
    det_db_unclip_ratio=1.6,
    det_use_dilation=True,
    confidence_review_threshold=0.60,
    preprocessing_mode="raw",
    preprocess_target="crop"
)
```

## 6. Final Test & Benchmark Commands
- **Test Command**: `python -m pytest` (108 passed in 33.62s)
- **Benchmark Command**: `python benchmarks/ocr/final/run_final_benchmark.py`

## 7. Final Measured Performance (AMD Ryzen CPU)
- **Cold Engine Load**: 358.28 ms | **Cold Service Load**: 350.02 ms
- **Service Warmup**: 15.55 ms
- **English Specimen Median**: 124.19 ms (Engine) / 184.78 ms (Service Obs)
- **Hindi Specimen Median**: 144.22 ms (Engine) / 152.37 ms (Service Obs)
- **Bilingual Specimen Median**: 167.07 ms (Engine) / 175.21 ms (Service Obs)
- **Blank Control Frame Median**: 47.45 ms (Engine) / 46.44 ms (Service Obs)
- **Throughput**: ~5.25 - 5.63 req/s on CPU
- **Decompression Bomb Rejection**: 0.029 ms

## 8. Final Limitations
1. Real packaging validation is PENDING field dataset collection (Path B active).
2. Script router is a heuristic confidence gate, not a deep neural classifier.
3. Concurrency is thread-safe via serialization lock; throughput does not scale linearly on CPU.
4. Confidence scores represent raw model CTC probability, not legal certitude.

## 9. Final External Dependencies
- **Member 2 (Vision/Calibration)**: Must provide unwarped, glare-free 2D images and apply optical scale factor (mm/px) to convert raw pixel geometry to physical dimensions.
- **Member 3 (Rule Engine)**: Consumes canonical `OCRObservation` list to extract statutory entities (MRP, Net Qty) and evaluate Legal Metrology Rules.
- **Member 4 (API/Worker)**: Consumes `OCRService.get_instance()` within FastAPI lifespan.
- **Member 5 (Web UI)**: Consumes `tokens` from `extract_dict()` to render interactive bounding boxes on React Canvas.
- **Member 6 (Validation & Datasets)**: Collects physical retail packaging imagery to conduct real-world retail accuracy benchmarks.

## 10. Final Release Status
**`M1 FINAL — READY WITH KNOWN LIMITATIONS`**
