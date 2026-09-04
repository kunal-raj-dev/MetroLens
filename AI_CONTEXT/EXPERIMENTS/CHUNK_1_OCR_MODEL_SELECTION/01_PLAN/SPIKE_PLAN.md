# CHUNK 1: OCR MODEL FEASIBILITY SPIKE PLAN
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/01_PLAN/SPIKE_PLAN.md`  
**Author:** Senior ML & Performance Engineer | **Sprint Window:** 8–9 Days  
**Objective:** Empirically evaluate and select the primary local OCR foundation for MetroLens under real hardware constraints, dual-project time limits, and Indian packaged commodity requirements.

---

## 1. Core Hypothesis & Questions
1. **Hypothesis:** A lightweight, quantized ONNX scene text detection and recognition pipeline can run entirely on server/laptop CPU within $< 800\text{ms}$ latency and $< 400\text{MB}$ RAM while providing character bounding boxes and high critical-field recognition accuracy.
2. **Primary Investigation Questions:**
   - Does a single monolingual model suffice for Indian packaging declarations, or is dual-script routing (English + Hindi) mandatory?
   - What is the empirical latency breakdown between Text Detection (DBNet) and Text Recognition (SVTR)?
   - Can the engine run 100% offline with zero network connectivity?
   - How does the engine behave on edge failure cases (blank images, low contrast, microscopic fonts)?

---

## 2. Experimental Constraints
- **Hardware Target:** Standard commodity CPU (AMD Ryzen 8 cores / 16 threads, 15GB RAM). Zero reliance on GPU acceleration.
- **Runtime Target:** Local ONNX Runtime (`onnxruntime==1.29.0`) on Python 3.14.3.
- **Evaluation Dataset:** Standardized suite of 8 packaging test specimens covering English, Hindi, Bilingual, Shrinkflation font deficits, Liquid volumes, Prohibited units, Blank frame, and Faded contrast.
- **Metrics Measured:** Cold-start load time, Warm latency (median, P90, P95), Memory RSS, Bounding box count, and Critical-field recognition accuracy (MRP, Net Quantity, USP, Dates).
- **Rule of Integrity:** Zero fabricated metrics. If real data is missing or a candidate is uninstalled, it is recorded as `DATA INSUFFICIENT` or `DISQUALIFIED`.
