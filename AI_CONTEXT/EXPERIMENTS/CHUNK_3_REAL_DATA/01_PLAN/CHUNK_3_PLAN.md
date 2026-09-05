# CHUNK 3 EXECUTION PLAN: REAL-DATA OCR VALIDATION, DOMAIN PREPROCESSING & ROBUSTNESS
**Run ID:** `C3-EXEC-01`  
**Date:** 2026-09-05T04:59:00+05:30  
**Phase:** Member 1 — Chunk 3  
**Status:** IN EXECUTION (PATH B: REAL DATA BLOCKED)  

---

## 1. Objective
Establish an evidence-based evaluation of the PP-OCRv3-ROUTED engine against packaging challenges, specifically:
- Low-contrast print on metallic/reflective pouches.
- Dot-matrix inkjet printed date and batch stamps.
- Micro-font statutory declarations (<1mm).
- Bilingual Latin and Devanagari script routing.

## 2. Inviolable Architectural Boundaries
- **No Engine Architecture Rebuild:** Keep direct ONNX Runtime (`onnxruntime==1.29.0`) CPU execution, DBNet++ detector, and SVTR recognizers.
- **No Physical Measurement in OCR:** Font heights remain in raw original pixels (`raw_pixel_height`); Member 2 owns mm calibration.
- **No Semantic Metrology Rules in OCR:** No Rule 6/7/8/9/11/26 logic; Member 3 owns legal compliance adjudication.
- **No Cloud AI / No External Generative LLMs:** All inference runs 100% locally and offline.
- **No Fabricated Data (Path B Gate):** Real physical dataset is absent (`data/raw/` = 0 images). Do NOT synthesize fake images or fake ground truth.

## 3. Preprocessing Hypotheses
- **H1 (CLAHE):** Contrast Limited Adaptive Histogram Equalization applied in LAB color space on low-contrast regions improves character contrast without color distortion.
- **H2 (Bilateral Filtering):** Edge-preserving denoising smooths high-frequency packaging texture noise without degrading stroke edges.
- **H3 (Unsharp Masking):** Controlled sharpening sharpens soft edges on slightly blurred packaging print.
- **H4 (Morphological Dilation):** Structural dilation with a small kernel bridges disconnected dot-matrix inkjet dots into continuous strokes for CTC recognizer decoding.
- **H5 (Crop-level vs Image-level):** Applying transformations strictly at the cropped text region level preserves original detector geometry and prevents degrading unrelated clean packaging regions.

## 4. Execution Matrix
- **B0:** Baseline (Raw / Identity)
- **P1:** Grayscale / Normalization
- **P2:** CLAHE (clip_limit: 2.0, 3.0; tile_grid: 8x8)
- **P3:** Bilateral Filter (d: 5, sigma: 50)
- **P4:** Unsharp Mask (amount: 1.5)
- **P5:** Morphological Dilation (kernel: 2x2, iterations: 1, 2)
- **P6:** Targeted Combinations (e.g. CLAHE + Dilation)
- **P-Adaptive:** Conditional crop-level preprocessing triggered on low-contrast crops.
