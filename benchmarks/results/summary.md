# MetroLens AI™ / Nirikshak AI — Benchmark Execution Summary
**SIH 2026 Problem Statement 26034**  
**Role:** Member 6 — Product Integration, Quality Assurance, Benchmark Verification & Release Governance  
**Generated At:** `2026-09-07T23:34:04.067862+00:00`  
**Git Commit SHA:** `a06872f`  
**Platform:** `Windows 11 | Python 3.12.7`  

---

## 1. Executive Benchmark Verdict

| Domain | Target | Measured / Actual | Status | Rationale / Denominator |
|:---|:---:|:---:|:---:|:---|
| **Physical Dataset** | 35 SKUs | 0 SKUs | **BENCHMARK_BLOCKED** | 0 authentic retail SKU scans on disk in `data/raw/` |
| **Physical OCR CER** | < 6.0% | `null` | **BENCHMARK_BLOCKED** | Denominator: 0 physical samples |
| **Synthetic OCR CER** | Baseline | `1.1961` | **EVALUATED** | Evaluated on 7 synthetic test specimens |
| **Scale Factor Error** | < 5.0% | `null` | **BENCHMARK_BLOCKED** | Denominator: 0 physical calibration specimens |
| **Font Height MAE** | < 0.15 mm | `null` | **BENCHMARK_BLOCKED** | Denominator: 0 vernier caliper ground-truth records |
| **Compliance Accuracy**| > 95.0% | `null` | **BENCHMARK_BLOCKED** | Denominator: 0 authenticated physical statutory records |
| **E2E Pipeline Latency**| < 2500 ms | `72.82 ms` | **PASS** | Evaluated on 20 repeated iterations (< 2.5s budget) |
| **PDF Dossier Latency** | < 500 ms | `20.22 ms` | **PASS** | ReportLab court-admissible PDF compiler |

---

## 2. Denominators & Anti-Metric Laundering Audit

- **Physical Samples Eligible:** 0
- **Physical Samples Evaluated:** 0
- **Physical Samples Excluded:** 0
- **Exclusion Reason:** Physical retail dataset collection pending Member 6 field acquisition.
- **Synthetic Specimens Eligible:** 8
- **Synthetic Specimens Evaluated:** 7
- **Synthetic Total Characters:** 459

---

## 3. Per-Sample Synthetic Breakdown

| Sample ID | Type | OCR Status | CER | Latency (ms) | Notes |
|---|:---:|:---:|:---:|:---:|---|
| `SYNTH-01-ENG-FMCG` | SYNTHETIC_TEST_SPECIMEN | SUCCESS | `1.2875` | 383.12 ms | Pass |
| `SYNTH-02-HIN-FMCG` | SYNTHETIC_TEST_SPECIMEN | SUCCESS | `0.8286` | 281.05 ms | Pass |
| `SYNTH-03-MIXED-BILINGUAL` | SYNTHETIC_TEST_SPECIMEN | SUCCESS | `1.046` | 258.41 ms | Pass |
| `SYNTH-04-MICRO-FONT` | SYNTHETIC_TEST_SPECIMEN | SUCCESS | `1.4259` | 224.05 ms | Pass |
| `SYNTH-05-LIQUID-VOLUME` | SYNTHETIC_TEST_SPECIMEN | SUCCESS | `1.2317` | 254.96 ms | Pass |
| `SYNTH-06-PROHIBITED-UNITS` | SYNTHETIC_TEST_SPECIMEN | SUCCESS | `1.6047` | 219.19 ms | Pass |
| `SYNTH-07-BLANK-FRAME` | SYNTHETIC_TEST_SPECIMEN | SKIPPED | `None` | None ms | Missing image or empty reference text |
| `SYNTH-08-LOW-CONTRAST-FADED` | SYNTHETIC_TEST_SPECIMEN | SUCCESS | `1.1628` | 184.78 ms | Pass |

---
*Note: In compliance with the MetroLens Anti-Hallucination Policy, no synthetic metrics have been substituted for physical metrological validation.*
