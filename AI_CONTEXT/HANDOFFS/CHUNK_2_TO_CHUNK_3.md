# ENGINEERING HANDOFF: CHUNK 2 TO CHUNK 3
**Document:** `AI_CONTEXT/HANDOFFS/CHUNK_2_TO_CHUNK_3.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 1 (Chunk 3 — Packaging Dataset & Robustness) & Downstream Monorepo Leads  
**Date:** 2026-09-05T04:34:00+05:30  
**Status:** COMPLETE & FROZEN  

---

## 1. What is Stable
- **Direct ONNX Runtime Subsystem:** Native `onnxruntime==1.29.0` with `CPUExecutionProvider` on Python 3.14.3.
- **Model Loading & Session Management:** Load once, reuse across all requests. No runtime model downloads.
- **Geometry & Coordinate Contracts:** Original input image pixel space. Origin `(0.0, 0.0)` top-left. Clockwise 4-point quadrilateral polygons `[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]`. Derived axis-aligned bounding boxes `[xmin, ymin, xmax, ymax]`.
- **Seam Separation:** Zero physical mm measurement in OCR. Zero semantic legal rule logic in OCR. `raw_pixel_height` is strictly a geometric quad height primitive.
- **Offline Guarantee:** 100% offline execution verified with local weights and dictionaries. Zero network requests.
- **Input Validation:** Safe handling of `None`, 0-byte arrays, and small images without crashing.
- **Reading Order Sorting:** Deterministic top-to-bottom, left-to-right line clustering.

---

## 2. What is Provisional
- **Provisional Architecture:** `PP-OCRv3-ROUTED` is the provisional selection for the Web MVP.
- **Script Router:** Current `ScriptRouter` is an **ENGINEERING HEURISTIC** (confidence gating), not a trained neural script classifier.
- **Preprocessing Hook:** `ImagePreprocessHook` is currently a passthrough. Domain-specific enhancements are intentionally deferred to Chunk 3.
- **Performance & Accuracy Baseline:** Current benchmarks are evaluated on 8 synthetic packaging fixtures. Formal production accuracy is pending Member 6's 35-SKU physical retail packaging dataset.

---

## 3. OCR API
```python
from nirikshak_ocr import OCREngine, OCRConfig, OCRResult

config = OCRConfig(intra_op_num_threads=4).resolve_paths()
engine = OCREngine(config)

# Accepts BGR numpy array, image path string, or Path object
result: OCRResult = engine.extract(image, image_id="sample_01", language_hint="auto")
```

---

## 4. OCRToken
```python
class OCRToken(BaseModel):
    token_id: str                      # Deterministic identifier e.g. "tok_001"
    text: str                          # Transcribed character sequence
    confidence: float                  # CTC decoder confidence [0.0, 1.0]
    polygon: List[List[float]]         # Clockwise 4-point quad in original image pixels
    bbox: List[float]                  # Derived envelope [xmin, ymin, xmax, ymax]
    script: ScriptType                 # 'latin' | 'devanagari' | 'unknown'
    line_id: int                       # Reading-order line index
    raw_pixel_height: Optional[float]  # Raw geometry only (NOT legal font height)
    model_name: str                    # "SVTR-EN" or "SVTR-HI"
```

---

## 5. OCRResult
```python
class OCRResult(BaseModel):
    image_id: str
    image_width: int
    image_height: int
    tokens: List[OCRToken]             # Sorted in reading order
    engine: str = "PP-OCRv3-ROUTED"
    detector_model: str                # e.g. "ch_PP-OCRv3_det_infer.onnx"
    recognizer_models: Dict[str, str]  # {"latin": "...", "devanagari": "..."}
    processing_time_ms: float          # Total wall-clock time
    stage_timings: Dict[str, float]    # Breakdown (prep, det, rec, sort)
    warnings: List[str]                # Diagnostic notices (e.g. low confidence)
    routing_summary: Dict[str, int]    # {"latin": N, "devanagari": M, "unknown": K}
```

---

## 6. Model Assets
| Model ID | File Location | Task | Format / Size | SHA-256 Checksum |
| :--- | :--- | :---: | :---: | :--- |
| `ch_PP-OCRv3_det_infer` | `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx` | Text Detection | ONNX (2.43 MB) | `3439588c030faea393a54515f51e983d8e155b19a2e8aba7891934c1cf0de526` |
| `ch_PP-OCRv3_rec_infer` | `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx` | Latin Recognition | ONNX (10.69 MB) | `897a3ededb38fee0dae2c1ccee38241f37df202c9509e3abca02e9217c5ee615` |
| `hindi_PP-OCRv3_rec_infer`| `models/weights/ocr/rec_hi/rec.onnx` | Devanagari Recognition | ONNX (8.98 MB) | `43df175fa3c877fbf7bcc4e5bd1e203e24ec450cd3ea96c9e802c86e39a4d4cf` |
| `dict.txt` | `models/weights/ocr/rec_hi/dict.txt` | Hindi Dictionary | Plain text (508 B) | `b5f1be6d8bbff1a19fb96c5d4ca96a423380234bb7d2ce0e07b5838adb4d18ea` |

---

## 7. Performance
- **Hardware Profile:** AMD Ryzen CPU (8 physical / 16 logical cores), 15.31 GB RAM, Windows 11, Python 3.14.3.
- **Cold Load Latency:** 283.66 ms.
- **Optimal Threading:** 4 threads (empirically confirmed; 1 thread: 168 ms; 8 threads: 168 ms due to context switching).
- **Warm Inference:** Median **107.29 ms** (P95: 113.91 ms) on 640x360 image.
- **Process Memory RSS:** Bounded at ~305 MB plateau across 25 repeated calls (+0.02 MB delta).

---

## 8. Offline
- 100% offline execution verified in `tests/unit/test_ocr_offline.py` with zero network access.

---

## 9. Real Data Gap
- **`data/raw/` Status:** Contains **0 real physical packaging images** (`DATA INSUFFICIENT`).
- **Validation State:** Evaluated against controlled synthetic fixtures labeled `SYNTHETIC TEST — NOT REAL PACKAGING`.
- Formal accuracy is strictly marked **PENDING**.

---

## 10. Known Failure Modes
1. Fragmented dot-matrix inkjet dates on packaging crimps.
2. Low contrast text on metallic/reflective pouches.
3. Curved text on cylindrical cans/bottles (requires Member 2 homography/unwarping).
4. Ambiguous script crops triggering fallback in heuristic router.

---

## 11. What Chunk 3 Should Build
1. Ingest Member 6's 35-SKU authentic Indian retail packaging dataset in `data/raw/`.
2. Implement domain-specific filters in `ImagePreprocessHook`:
   - Contrast Limited Adaptive Histogram Equalization (CLAHE) for low-contrast foil pouches.
   - Morphological dilation filter for connecting fragmented dot-matrix inkjet characters.
3. Compute field-level Character Error Rate (CER) and Word Error Rate (WER) across ground-truth annotations.

---

## 12. What Chunk 3 MUST NOT Rebuild
- ❌ **DO NOT** replace the Direct ONNX Runtime architecture (`onnxruntime==1.29.0`).
- ❌ **DO NOT** reintroduce `rapidocr-onnxruntime` or other unsupported third-party wrappers.
- ❌ **DO NOT** rebuild DBNet detection or SVTR recognition inference loops.
- ❌ **DO NOT** implement legal metrology rules or mm scale measurement inside OCR.
