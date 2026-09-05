# CHUNK 2: OCR ENGINE FOUNDATION PLAN
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_2_OCR_ENGINE/01_PLAN/CHUNK_2_PLAN.md`  
**Author:** Member 1 (AI & OCR Lead)  
**Objective:** Engineer a clean, reusable, testable, locally runnable OCR engine foundation (`packages/ocr/`) from the provisional Chunk 1 baseline.

---

## 1. Scope & Core Objectives
1. **Dependency & Runtime Compatibility Gate:**
   - Audit RapidOCR vs. Direct ONNX Runtime compatibility with Python 3.14.
   - Formally document runtime decision (Option A vs Option B vs Option C).
2. **Model Currency Sanity Check:**
   - Quick check of official PaddleOCR PP-OCRv5 mobile models without derailing the sprint.
3. **Data Contract Standardization:**
   - Define `OCRToken` and `OCRResult` with 4-point convex polygons, derived bounding boxes, model confidences, and script classifications.
   - Strictly decouple raw geometry from Member 2's physical font measurement and Member 3's legal semantic parsing.
   - Standardize canonical coordinate convention: Original input image pixel coordinates, origin at top-left `(0,0)`, clockwise quad `[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]`.
4. **Modular Package Implementation (`packages/ocr/`):**
   - `config.py`: Typed configuration (model paths, thread counts, thresholds).
   - `types.py`: Frozen data contracts (`OCRToken`, `OCRResult`, `ScriptType`).
   - `errors.py`: Typed error hierarchy.
   - `preprocessing.py`: Color conversion, aspect-ratio preserving resize, and coordinate unscaling.
   - `detector.py`: DBNet++ ONNX text detection and polygon extraction.
   - `recognizer.py`: SVTR-EN and SVTR-HI recognition sessions.
   - `router.py`: Lightweight script routing heuristic (detect -> route -> single recognizer).
   - `engine.py`: `OCREngine` facade exposing `extract(image) -> OCRResult`.
   - `utils.py`: Deterministic reading order sorting and geometry helpers.
5. **Rigorous Verification & Benchmarking:**
   - Input safety validation (None, blank, zero-size, malformed images).
   - Coordinate remapping accuracy tests (original -> resized -> original).
   - CPU thread count sweep (1, 2, 4, 8 threads).
   - Latency (median, P95) and RSS memory stability over 20+ repeated inferences.
   - 100% offline verification with network disconnected/mocked.
   - Local model manifest (`models/manifest.yaml`).
6. **Downstream Handoffs:**
   - Clean handoffs to Member 2 (geometry only), Member 3 (text only), Member 4 (engine facade), Member 5 (coordinates), Member 6 (benchmarking hooks).

---

## 2. Inviolable Constraints & Scope Boundaries
- **NO** legal rule evaluations (Rule 6, 7, 8, 9, 26).
- **NO** semantic entity extraction (MRP, Net Qty, USP, Dates).
- **NO** physical mm measurement, scale calibration ($S$), or PDP calculation.
- **NO** curved-surface unwarping or TPS rectification.
- **NO** fabricated accuracy or latency claims.
- **NO** git commits or pushes.
