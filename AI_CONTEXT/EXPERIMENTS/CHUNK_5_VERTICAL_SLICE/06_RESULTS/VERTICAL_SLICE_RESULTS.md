# Chunk 5 Vertical Slice 0 Experimental Results

## Executive Summary
Chunk 5 established the first working, end-to-end, deterministic vertical slice of the MetroLens AI (SIH26034) legal metrology inspection platform: **Vertical Slice 0**.
All 8 pipeline stages were transformed from mocked scaffolds into fully functional, synchronized components operating on real image bytes:
`Image Ingestion -> Quality Gate -> Metric Calibration -> Multilingual OCR -> Semantic Extraction -> Metrological Measurement -> Legal Rules Engine -> Evidence DAG Assembly`.

## Benchmark Performance & Latency Profile

Profiling conducted over 15 measured iterations on Windows 11 (AMD64, Python 3.14.3, Direct ONNX Runtime `CPUExecutionProvider` with 4 threads):

| Pipeline Stage | Mean Latency | Median (P50) | P90 Latency | P95 Latency | Min Latency | Max Latency | Std Dev | Share of Total |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1. Ingestion & Digest** | 5.79 ms | 5.90 ms | 6.09 ms | 6.13 ms | 5.08 ms | 6.16 ms | 0.31 ms | 2.7% |
| **2. Optical Quality Gate** | 22.42 ms | 22.41 ms | 25.30 ms | 25.91 ms | 19.95 ms | 26.23 ms | 1.80 ms | 10.5% |
| **3. Metric Scale Calibration** | 16.05 ms | 15.92 ms | 17.79 ms | 18.00 ms | 14.33 ms | 18.02 ms | 1.15 ms | 7.5% |
| **4. Multilingual OCR Perception** | 169.55 ms | 168.60 ms | 179.96 | 182.69 ms | 155.13 ms | 188.14 ms | 9.00 ms | 79.2% |
| **5. Semantic Extraction** | 0.20 ms | 0.19 ms | 0.24 ms | 0.26 ms | 0.14 ms | 0.30 ms | 0.04 ms | < 0.1% |
| **6. Physical Measurement** | 0.02 ms | 0.02 ms | 0.03 ms | 0.03 ms | 0.01 ms | 0.04 ms | 0.01 ms | < 0.1% |
| **7. Legal Rules Engine** | 0.05 ms | 0.04 ms | 0.06 ms | 0.07 ms | 0.03 ms | 0.08 ms | 0.01 ms | < 0.1% |
| **8. Evidence DAG Assembly** | 0.06 ms | 0.06 ms | 0.10 ms | 0.10 ms | 0.04 ms | 0.10 ms | 0.02 ms | < 0.1% |
| **TOTAL END-TO-END PIPELINE** | **214.19 ms** | **211.49 ms** | **228.37 ms** | **230.26 ms** | **197.30 ms** | **232.54 ms** | **10.00 ms** | **100.0%** |

### SLA Conformance
- **Target SLA for Synchronous Web MVP**: **<= 2000.0 ms** (2.0 seconds) per packaging frame.
- **Measured P95 Latency**: **230.26 ms**.
- **SLA Margin**: 8.7x faster than the maximum allowable SLA threshold.
- **Verdict**: **COMPLIANT / SLA PASSED**.

## Resource Footprint & Stability
- **Starting Memory RSS**: 72.86 MB (baseline Python process).
- **Post-Warmup Memory RSS**: 257.63 MB (ONNX Runtime sessions loaded: Det + Rec-En + Rec-Dev).
- **Final Memory RSS after 15 Iterations**: 260.59 MB.
- **Leak Audit**: Delta between post-warmup and run 15 is +2.96 MB (attributable to in-memory FastAPI result cache), confirming zero unbounded memory leaks in vision, OCR, or metrology loops.

## Verified End-to-End Capabilities
1. **Perimeter Security Gate**: Successfully rejects corrupted images, invalid headers, and oversized payloads (> 15MB) with HTTP 400/413.
2. **Deterministic Pre-flight Quality**: Rapidly evaluates Laplacian edge variance and specular glare (< 25 ms), returning `REJECTED_QUALITY` on unreadable inputs to save OCR compute.
3. **Truthful Metrology**:
   - In uncalibrated mode: returns `CalibrationStatus.UNCALIBRATED`, `measured_mm=None`, and flags Rule 7 font height as `REVIEW` with `uncertainty_flag=True`.
   - In calibrated mode: detects reference coin (INR coin via HoughCircles) or ArUco markers, calculates metric scale factor (mm/px), computes actual font height in mm, and evaluates compliance against Table-I.
4. **Statutory Legal Logic**: Evaluates mandatory Rule 6 presence (MRP, Net Quantity, Mfg Date, Consumer Care, Country of Origin) and Rule 7 minimum numeral font heights without hallucinated verdicts.
5. **Cryptographic Chain of Custody**: Links every verdict and extracted declaration to an `EvidenceItem` containing pixel coordinates, OCR confidence, and image SHA-256 digest.
6. **Air-Gapped Offline Execution**: Fully verified to operate with zero network dependencies under socket-level monkeypatch isolation.
