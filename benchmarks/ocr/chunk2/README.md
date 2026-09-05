# CHUNK 2 OCR BENCHMARK RESULTS & REPRODUCIBILITY GUIDE
**Directory:** `benchmarks/ocr/chunk2/`  
**Execution Timestamp:** 2026-09-05T04:16:28+05:30  
**Hardware Target:** AMD Ryzen 8C/16T, 15.31 GB RAM, Windows 11 (CPU-only)  
**Runtime:** Direct ONNX Runtime (`onnxruntime==1.29.0`) on Python 3.14.3  
**Architecture:** `PP-OCRv3-ROUTED` (DBNet++ det + Script-Routed SVTR-EN / SVTR-HI)

---

## 1. Thread Count Sweep (Latency vs CPU Saturation)

| Intra-op Threads | Cold Load (ms) | Median Latency (ms) | P95 Latency (ms) | Memory RSS (MB) | Engineering Verdict |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | 240.45 | 176.18 | 182.19 | 188.94 | Single-threaded; high latency. |
| **2** | 281.59 | 118.03 | 130.33 | 199.31 | Substantial 33% latency improvement. |
| **4** | **291.38** | **110.47** | **115.79** | **200.98** | **OPTIMAL:** Best median latency and tight P95 spread on 8-core CPU. |
| **8** | 292.12 | 151.18 | 175.49 | 205.00 | Thread contention and context-switching penalty. |

*Selected Default Setting:* `intra_op_num_threads = 4`.

---

## 2. Memory Stability Over 25 Repeated Inferences

```text
Step 0  (Post-Load):    231.80 MB
Step 1  (Inference #1):  275.73 MB (+43.93 MB initial buffer allocation)
Step 5  (Inference #5):  305.23 MB
Step 10 (Inference #10): 305.23 MB (0.00 MB delta)
Step 15 (Inference #15): 305.23 MB (0.00 MB delta)
Step 20 (Inference #20): 305.23 MB (0.00 MB delta)
Step 25 (Inference #25): 305.30 MB (+0.07 MB delta)
```

**Finding:** Memory usage strictly plateaus at ~305 MB RSS with zero unbounded leakage. Well within the 400 MB server process limit.

---

## 3. Specimen Sweep (8 Controlled Synthetic Specimens)

| Specimen Filename | Resolution | Median Latency (ms) | Token Count | Script Routing Breakdown |
| :--- | :---: | :---: | :---: | :--- |
| `SYNTH-01-ENG-FMCG.png` | 640x360 | 107.64 | 6 | Latin: 4, Devanagari: 2, Unknown: 0 |
| `SYNTH-02-HIN-FMCG.png` | 640x360 | 91.24 | 5 | Latin: 4, Devanagari: 1, Unknown: 0 |
| `SYNTH-03-MIXED-BILINGUAL.png` | 640x380 | 100.47 | 6 | Latin: 5, Devanagari: 1, Unknown: 0 |
| `SYNTH-04-MICRO-FONT.png` | 640x320 | 76.56 | 5 | Latin: 5, Devanagari: 0, Unknown: 0 |
| `SYNTH-05-LIQUID-VOLUME.png` | 640x360 | 88.15 | 6 | Latin: 6, Devanagari: 0, Unknown: 0 |
| `SYNTH-06-PROHIBITED-UNITS.png`| 640x320 | 72.06 | 5 | Latin: 5, Devanagari: 0, Unknown: 0 |
| `SYNTH-07-BLANK-FRAME.png` | 640x320 | 24.63 | 0 | Latin: 0, Devanagari: 0, Unknown: 0 |
| `SYNTH-08-LOW-CONTRAST-FADED.png`| 640x320| 66.89 | 4 | Latin: 4, Devanagari: 0, Unknown: 0 |

---

## 4. How to Reproduce

```bash
# Run benchmark harness
python benchmarks/ocr/chunk2/run_chunk2_benchmark.py

# Run unit and integration tests
python -m pytest tests/unit/test_ocr_types_config.py tests/unit/test_ocr_engine_comprehensive.py tests/unit/test_ocr_offline.py
```
