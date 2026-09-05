# CHUNK 1 TO CHUNK 2 ENGINEERING HANDOFF
**Source:** Chunk 1 — OCR Model Feasibility Spike  
**Target:** Chunk 2 — OCR Production Module & Extraction Interface  
**Lead Engineer:** Member 1 (AI & OCR Lead)  
**Date:** 2026-09-05

---

## 1. Selected Primary OCR Foundation
- **Model Engine:** PP-OCRv3 via `rapidocr-onnxruntime` + custom Devanagari ONNX recognizer.
- **Model Files:**
  - Detection: `models/ch_PP-OCRv3_det_infer.onnx` (2.32 MB)
  - English Recognition: `models/ch_PP-OCRv3_rec_infer.onnx` (10.20 MB)
  - Hindi Recognition: `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/models/hindi/rec.onnx` (8.56 MB) + `dict.txt` (167 characters)
- **Runtime:** ONNX Runtime (`onnxruntime==1.29.0`) executed strictly on CPU.
- **Python Dependencies:** `rapidocr-onnxruntime==1.2.3`, `onnxruntime==1.29.0`, `opencv-python==5.0.0.93`, `shapely==2.1.2`, `numpy==2.5.2`.

---

## 2. Interface Contracts for Downstream Workstreams

### Interface for Member 2 (Computer Vision & Calibration):
- **Output Geometry:** For every detected line, the engine emits an exact 4-point polygon `[[x1,y1], [x2,y2], [x3,y3], [x4,y4]]`.
- **Character Stroke Height:** Calculated as vertical distance: $h_{\text{px}} = \frac{(y4 - y1) + (y3 - y2)}{2}$.
- **Input Accepted:** Preprocessed `numpy.ndarray` (BGR or RGB) or rectified planar crops.

### Interface for Member 3 (Rule Engine & Domain Logic):
- **Structured Tokens:** Emits `List[OCRToken]` where each token contains:
  ```python
  token_id: int
  text: str
  confidence: float  # Filter threshold: >= 0.60
  bbox: List[int]    # [x, y, width, height]
  char_height_px: float
  ```
- **Language Tags:** Tokens tagged with `lang: "en"` or `lang: "hi"`.

### Interface for Member 4 (Backend API):
- **Service Class:** `packages/ocr/engine.py` provides a single class `OCREngine` with warm-loaded ONNX sessions.
- **Thread Safety:** Single-session inference thread-safe for synchronous Uvicorn workers.

### Interface for Member 5 (Frontend Canvas):
- **Bounding Boxes:** Normalized bounding boxes ready for direct rendering on HTML5 canvas with hover tooltips.

### Interface for Member 6 (QA & Benchmark):
- **Benchmark Script:** `tests/benchmarks/test_ocr_benchmark.py` ready to ingest the 35-SKU ground-truth dataset once sourced.

---

## 3. What Chunk 2 Must Do
1. Implement `packages/ocr/engine.py` encapsulating the Dual-Recognizer pipeline.
2. Implement `packages/ocr/tokenizer.py` converting raw detections into `OCRToken` dataclasses.
3. Cache model weights locally in `models/` directory for zero-network execution.
4. Add morphological dilation filter for dot-matrix inkjet dates.
5. Write unit tests in `tests/unit/test_ocr_engine.py` achieving $> 90\%$ branch coverage.

---

## 4. What Chunk 2 Must NOT Redo
- Do NOT re-investigate EasyOCR or Tesseract (already disqualified).
- Do NOT attempt to train or fine-tune neural models from scratch.
- Do NOT install heavy frameworks like PyTorch or PaddlePaddle.
- Do NOT build statutory legal logic into the OCR module (owned by Member 3).
