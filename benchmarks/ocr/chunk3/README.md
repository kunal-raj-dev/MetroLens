# Nirikshak OCR Chunk 3 Benchmark Suite

## Dataset Status
- **Status:** `REAL_PACKAGING_BLOCKED` (0 real images present on disk)
- **Harness:** Synthetic FMCG Regression Harness (8 controlled specimens)
- **Hardware Profile:** Windows (AMD64), Python 3.14.3
- **Evaluation Scope:** 8 configurations × 8 specimens = 64 evaluated inference passes (+ 8 warmup passes = 72 total passes)
- **Production Default Policy:** `B0_BASELINE_RAW` is the canonical production default. `P_ADAPTIVE_CROP` is a provisional experimental candidate.

## Summary of Results
| Configuration | Macro CER | Macro WER | Field Acc | Num Acc | Routing Acc | Median Latency | Decision Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **B0 (Baseline Raw)** | 0.2124 | 0.6038 | 75.9% | 42.9% | 83.8% | 88.7 ms | Canonical Production Default |
| **P2_CLAHE_CROP** | 0.2250 | 0.6504 | 75.9% | 42.9% | 83.8% | 101.0 ms | BENEFICIAL_FOR_LOW_CONTRAST |
| **P3_BILATERAL_CROP** | 0.2304 | 0.6446 | 75.9% | 42.9% | 86.5% | 101.8 ms | OPTIONAL_DOMAIN_FILTER |
| **P4_UNSHARP_CROP** | 0.2173 | 0.6089 | 75.9% | 42.9% | 83.8% | 94.4 ms | OPTIONAL_DOMAIN_FILTER |
| **P5_DILATION_CROP** | 0.2288 | 0.6446 | 75.9% | 42.9% | 86.5% | 94.3 ms | OPTIONAL_DOMAIN_FILTER |
| **P6_COMBO_CLAHE_DILATE** | 0.2443 | 0.6587 | 72.4% | 42.9% | 89.2% | 96.7 ms | OPTIONAL_DOMAIN_FILTER |
| **P_ADAPTIVE_CROP** | 0.2184 | 0.6446 | 75.9% | 42.9% | 83.8% | 90.1 ms | PROVISIONAL_EXPERIMENTAL |
| **P_IMAGE_CLAHE** | 0.2157 | 0.6242 | 75.9% | 42.9% | 83.8% | 101.0 ms | REJECTED_BLANKET_OVERHEAD |

## Reproduction Command
```powershell
python benchmarks/ocr/chunk3/run_chunk3_benchmark.py
```
