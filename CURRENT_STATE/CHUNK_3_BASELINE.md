# CURRENT STATE: CHUNK 3 BASELINE (B0)
**Document:** `CURRENT_STATE/CHUNK_3_BASELINE.md`  
**Generated:** 2026-09-05T05:04:00+05:30  
**Phase:** Member 1 — Chunk 3 (Baseline Measurement B0)  
**Author:** Senior OCR / Benchmark Engineer (Member 1 Lead)  

---

## 1. Baseline Configuration (B0)
- **Engine Architecture:** `PP-OCRv3-ROUTED`
- **Detector:** DBNet++ ONNX (`ch_PP-OCRv3_det_infer.onnx`, 2.43 MB)
- **Latin Recognizer:** SVTR-EN ONNX (`ch_PP-OCRv3_rec_infer.onnx`, 10.69 MB)
- **Devanagari Recognizer:** SVTR-HI ONNX (`rec.onnx`, 8.98 MB) + Hindi dictionary (`dict.txt`)
- **Preprocessing:** Raw / Identity pass-through (`ImagePreprocessHook`)
- **Runtime:** `onnxruntime==1.29.0`, `CPUExecutionProvider`, 4 intra-op threads
- **Platform:** Windows 11 (AMD64), Python 3.14.3

---

## 2. Real-Data Audit Status
- **Disk Images Present in `data/raw/`:** **0**
- **Real-Data Gate Activated:** **PATH B (REAL DATA NOT AVAILABLE)**
- **Blocker Reason:** Physical store collection of 35 FMCG retail SKUs pending Member 6 delivery.
- **Evaluation Dataset:** Synthetic FMCG Regression Harness (8 controlled test fixtures: English, Hindi, Bilingual, Micro-font, Liquid volume, Prohibited units, Blank frame, Low-contrast faded).

---

## 3. Empirical Baseline Metrics (B0)
*Measured via `benchmarks/ocr/chunk3/run_chunk3_benchmark.py` on host CPU:*

| Metric | Measured Baseline B0 | Target Requirement | Status |
| :--- | :---: | :---: | :---: |
| **Median Latency** | **97.30 ms** | $< 250\text{ ms}$ | PASSED (Well within budget) |
| **P95 Latency** | **110.25 ms** | $< 400\text{ ms}$ | PASSED |
| **Macro Character Error Rate (CER)** | **0.2124 (21.24%)** | Benchmark anchor | MEASURED |
| **Macro Word Error Rate (WER)** | **0.6038 (60.38%)** | Benchmark anchor | MEASURED |
| **Statutory Field Accuracy** | **75.9%** | $\ge 70\%$ | PASSED |
| **Numeric Exact Match Accuracy** | **42.9%** | Priority focus | MEASURED (Identified 0/O, 1/I/l confusions) |
| **Empty Result Rate (on non-empty)**| **0.0%** | $0.0\%$ | PASSED |
| **Blank Frame Specificity** | **100.0% (0 false tokens)** | $100\%$ | PASSED |
| **Process RSS Memory** | **70.36 MB $\rightarrow$ 101.11 MB** | $< 400\text{ MB}$ | PASSED (Bounded plateau) |

---

## 4. Script-Stratified Baseline Performance
- **English / Latin CER:** **0.1748 (17.48%)**
- **Devanagari / Hindi CER:** **0.3125 (31.25%)**
- **Mixed Bilingual CER:** **0.2462 (24.62%)**

---

## 5. Primary Baseline Failure Modes
1. **Numeric Confusions:** Digit `0` confused with `O`, digit `1` confused with `I`/`l`, digit `5` confused with `S`.
2. **Low-Contrast Faded Print:** Faded silver foil text (`SYNTH-08`) produces degraded confidence (0.8512) and character drops.
3. **Hindi Conjuncts:** Complex Devanagari ligatures require accurate script routing to prevent fallback to English character set.
