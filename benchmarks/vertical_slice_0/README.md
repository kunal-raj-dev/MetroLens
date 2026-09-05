# MetroLens AI — Vertical Slice 0 Integration Benchmark

## Overview
This directory contains the performance benchmark results for **Vertical Slice 0: Core Inspection Pipeline Integration** (Chunk 5).
The benchmark evaluates the end-to-end synchronous execution of the full 8-stage pipeline:
`Image Ingestion -> Quality Gate -> Calibration -> Multilingual OCR -> Semantic Extraction -> Font Measurement -> Rules Engine -> Evidence Assembly`.

## Hardware & Environment Baseline
- **Operating System**: Windows-11-10.0.26200-SP0
- **Architecture**: AMD64
- **Python Version**: 3.14.3
- **Execution Provider**: Direct ONNX Runtime (`CPUExecutionProvider`, 4 intra-op threads)
- **Synchronous MVP Target SLA**: **<= 2000 ms** per inspection

## Latency Breakdown Across 8 Stages (15 iterations)

| Pipeline Stage             |     Mean |   Median |      P90 |      P95 |      Min |      Max |    Std |
|----------------------------|----------|----------|----------|----------|----------|----------|--------|
| ingestion_ms               |     5.79 |     5.90 |     6.09 |     6.13 |     5.08 |     6.16 |   0.31 |
| quality_gate_ms            |    22.42 |    22.41 |    25.30 |    25.91 |    19.95 |    26.23 |   1.80 |
| calibration_ms             |    16.05 |    15.92 |    17.79 |    18.00 |    14.33 |    18.02 |   1.15 |
| ocr_perception_ms          |   169.55 |   168.60 |   179.96 |   182.69 |   155.13 |   188.14 |   9.00 |
| semantic_extraction_ms     |     0.20 |     0.19 |     0.24 |     0.26 |     0.14 |     0.30 |   0.04 |
| measurement_ms             |     0.02 |     0.02 |     0.03 |     0.03 |     0.01 |     0.04 |   0.01 |
| rules_engine_ms            |     0.05 |     0.04 |     0.06 |     0.07 |     0.03 |     0.08 |   0.01 |
| evidence_assembly_ms       |     0.06 |     0.06 |     0.10 |     0.10 |     0.04 |     0.10 |   0.02 |
| total_ms                   |   214.19 |   211.49 |   228.37 |   230.26 |   197.30 |   232.54 |  10.00 |

## Summary Findings
1. **End-to-End Latency**: Mean total pipeline latency is **214.19 ms** (P95: **230.26 ms**), well within the synchronous Web MVP SLA limit of 2000 ms.
2. **Dominant Stage**: Multilingual OCR perception accounts for ~79.2% of execution time on CPU, remaining consistent and deterministic.
3. **Microsecond Non-Vision Stages**: Legal rules engine (0.05 ms), semantic extraction (0.20 ms), and physical font measurement (0.02 ms) execute nearly instantaneously.
4. **Memory Stability**: Process memory RSS remained stable (Start: 72.9 MB, Final: 260.6 MB, Delta: +187.7 MB) with zero leaks detected over repeated iterations.
5. **SLA Verdict**: **COMPLIANT / PASSED**.
