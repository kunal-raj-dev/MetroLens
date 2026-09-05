# Master Benchmark Protocol Specification

## Purpose
Establishes reproducible, standardized testing procedures to measure OCR accuracy, font measurement error, calibration precision, and end-to-end latency without fabricating performance metrics.

## Scope
Governs all benchmark runs under `benchmarks/protocols/` and results logged in `benchmarks/results/`.

## Authoritative Inputs
- Anti-Hallucination Policy: No empirical number may appear without an actual experiment run.
- ICDAR and COCO evaluation standards.

## Assumptions
- Benchmark tests are executed on standardized reference hardware: 8-core CPU, 16 GB RAM, without external GPU acceleration (to simulate field laptop limits).

## Open Questions
- Establishing statistical significance sample size across varied packaging sheen [TBD — MEASURE].

## Dependencies
- `benchmarks/datasets/`
- `scripts/benchmark/`

## Verification Requirements
- All reported metrics in `docs/17_CLAIMS/PERFORMANCE_CLAIMS.md` must link to completed runs following these protocols.

---

## 1. Protocol PROTO-OCR-001: Multilingual Text Recognition

- **Objective:** Quantify Character Error Rate (CER) and Word Error Rate (WER) across flat and curved retail packaging.
- **Dataset:** `data/benchmark/ocr_test_set/` (Minimum 100 annotated package panels).
- **Execution Command:**
  ```bash
  python scripts/benchmark/run_ocr_benchmark.py --dataset data/benchmark/ocr_test_set/ --out benchmarks/results/ocr_run_latest.json
  ```
- **Metric Definitions:**
  $$\text{CER} = \frac{S + D + I}{N} \times 100\%$$
- **Current Result:** `TBD — MEASURE`

---

## 2. Protocol PROTO-CALIB-001: Physical Scale Calibration Accuracy

- **Objective:** Measure calibration error of estimated scale factor $S$ against laser-measured optical calibration patterns.
- **Metric:** Mean Absolute Error (MAE) in millimetres per pixel:
  $$\text{MAE}_S = \frac{1}{M} \sum_{i=1}^M |S_{\text{pred}, i} - S_{\text{true}, i}|$$
- **Current Result:** `TBD — MEASURE`

---

## 3. Protocol PROTO-FONT-001: Font Height Error Bound

- **Objective:** Evaluate deviation between optical font height measurement and physical caliper ground truth.
- **Tolerance Threshold:** Allowable error bound $\le \pm 0.2\text{ mm}$.
- **Metric:** Root Mean Squared Error (RMSE) in millimetres.
- **Current Result:** `TBD — MEASURE`

---

## 4. Protocol PROTO-LATENCY-001: End-to-End Pipeline Runtime

- **Objective:** Measure execution time from raw multi-panel image ingestion to final JSON/PDF dossier output on single-thread and multi-thread CPU.
- **Metric:** Latency percentiles ($p50, p90, p99$) in seconds.
- **Current Result:** `TBD — MEASURE`
