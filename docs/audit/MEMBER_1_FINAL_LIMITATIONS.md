# MEMBER 1 — FINAL LIMITATIONS

**Subsystem**: Member 1 — Multilingual OCR Engine & Service  
**Auditor**: Independent Principal Engineer  
**Date**: 2026-09-05  
**Freeze Status**: AUDITED & FROZEN  

---

## 1. Real-Data Validation Status: PENDING
- **Physical Retail Images on Disk**: **0 (ZERO)**.
- **Verification Basis**: All current regression testing, latency measurements, and pipeline integration tests have been conducted on 8 synthetic packaging specimens (`SYNTH-01` through `SYNTH-08`).
- **Policy**: No real-world retail accuracy (CER, WER) claims are made or fabricated. Full real-data accuracy benchmarking is formally assigned to Member 6 upon physical dataset collection (Path B active).

## 2. Script Routing Architecture: HEURISTIC GATE
- **Current Implementation**: Heuristic confidence gate (`ScriptRouter.ROUTING_METHOD = "heuristic_confidence_gate"`).
- **Mechanism**: Evaluates Latin recognizer (SVTR-EN). If confidence is below threshold (0.70) or length < 2, evaluates Devanagari recognizer (SVTR-HI) and routes to Devanagari if Hindi confidence exceeds English by a margin (+0.15).
- **Limitation**: This is an engineering routing heuristic, NOT an independent deep neural script classifier. Mixed-script phrases within a single contiguous text line will be routed to the single model with higher overall confidence.

## 3. Dot-Matrix Inkjet Text: MORPHOLOGICAL HEURISTIC
- **Current Implementation**: Polar-aware morphological dilation (`apply_morphological_dilation`).
- **Limitation**: Enhances disconnected character dots on standard dot-matrix date/batch codes. However, severely degraded dot-matrix text with missing dots or extreme stroke fragmentation may fail detection or recognition.

## 4. Curved Surfaces & Specular Reflection
- **Boundary**: Member 1 operates on 2D planar image arrays.
- **Limitation**: Cylindrical perspective distortion (e.g. text wrapping around curved bottles or cans) and severe specular glare on metallic foil packaging degrade detection bounding polygons. Dewarping and photometric glare removal must be handled upstream by Member 2 (Vision & Calibration).

## 5. Micro-Font Text (< 8px Height)
- **Minimum Input Dimension**: Images with width or height < 8 pixels are rejected by `validate_input_image`.
- **Limitation**: Text lines with stroke height under 8 pixels in original image space exhibit reduced detection and recognition accuracy due to feature pyramid downsampling in DBNet++.

## 6. Concurrency & Multi-Threading: SERIALIZED
- **Execution Invariant**: Thread safety is achieved via a dedicated mutex lock (`OCRService._engine_lock`).
- **Limitation**: Concurrent calls from multiple threads (e.g. FastAPI worker threads) are safely serialized. CPU throughput does not scale linearly with thread count, and latency scales proportionally with concurrent request depth. True parallel scale requires multi-process workers (e.g. Uvicorn/Gunicorn processes with independent engine instances).

## 7. Model Confidence Semantics: MODEL CTC PROBABILITY
- **Definition**: The `confidence` attribute in `OCRToken` and `OCRObservation` represents the mean CTC softmax / logit probability output of the neural model for decoded characters.
- **Limitation**: It is NOT a calibrated statistical probability, and it is NOT a legal certitude score. Downstream legal metrology rule evaluation must never treat `confidence > 0.8` as legal proof of statutory compliance.
