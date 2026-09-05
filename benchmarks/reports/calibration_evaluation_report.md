# Optical Calibration Evaluation Report

**Overall Benchmark Status:** 🟡 `BENCHMARK_BLOCKED`  
**Diagnostic Message:** No explicit physical ground-truth dataset available.

## 1. Executive Summary

| Metric | Value | Target | Verdict |
| :--- | :---: | :---: | :---: |
| Total Samples | 0 | - | - |
| Successful Calibrations | 0 | - | - |
| Failed Calibrations | 0 | - | - |
| Calibration Success Rate | 0.0% | >= 90.0% | ⚠️ BLOCKED |
| Calibration Failure Rate | 0.0% | - | - |
| Scale Evaluated Samples (N) | 0 | - | - |
| Dimension Evaluated Samples (N) | 0 | - | - |
| Scale Mean Relative Error | N/A | <= 5.0% | ⚠️ BLOCKED |
| Feature Dimension MAE | N/A | <= 0.1500 mm | ⚠️ BLOCKED |

## 2. Scale Estimation Metrics (Units: mm/pixel or %)

*Denominator Note: Metrics computed strictly over N = 0 successfully calibrated samples with ground-truth scale. Dataset-level calibration reliability is independently captured by the Calibration Failure Rate (0.0% over all 0 samples).*  

| Metric | Value | Unit |
| :--- | :---: | :---: |
| Evaluated Sample Count (N) | 0 | samples |
| Mean Absolute Error (MAE) | N/A | mm/px |
| Median Absolute Error | N/A | mm/px |
| Root Mean Square Error (RMSE) | N/A | mm/px |
| 95th Percentile Error (P95) | N/A | mm/px |
| Mean Relative Error | N/A | % |
| Median Relative Error | N/A | % |

## 3. Physical Feature Dimension Metrics (Units: mm)

*Denominator Note: Metrics computed strictly over N = 0 samples with physical feature ground truth.*  

| Metric | Value | Unit |
| :--- | :---: | :---: |
| Evaluated Sample Count (N) | 0 | samples |
| Dimension MAE | N/A | mm |
| Dimension Median AE | N/A | mm |
| Dimension RMSE | N/A | mm |
| Dimension P95 AE | N/A | mm |

## 4. Failure Mode Breakdown

No failures recorded across evaluation dataset.

---
*Evidentiary Note: Physical ground-truth verification requires physical calibration specimens. In accordance with Nirikshak metrological integrity constraints, when no physical ground-truth dataset is present in the repository, status is reported as BENCHMARK_BLOCKED without fabricating synthetic accuracy claims.*