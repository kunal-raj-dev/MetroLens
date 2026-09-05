# INTER-WORKSTREAM HANDOFF CONTRACT: PHASES 8 & 9 COMPLETE
**Project:** MetroLens AI / Nirikshak (SIH26034)
**Workstream:** Member 2 — Computer Vision, Optical Calibration & Physical Measurement
**Handoff Recipients:** Member 1 (OCR Extraction), Member 3 (Rules Engine), Member 4 (Backend API), Member 6 (QA Lead)
**Status:** 🟢 Complete & Verified (180/180 calibration tests, 265/265 monorepo tests passing)

---

## 1. Executive Purpose

This handoff contract establishes the exact programmatic interfaces, mathematical invariants, robustness guarantees, and benchmark evaluation protocols delivered upon completion of:
- **Phase 8:** Vision Pipeline Robustness & Edge-Case Hardening (`packages/calibration/tests/test_vision_robustness.py`, 90 tests)
- **Phase 9:** Metric Calibration Evaluation Engine & Benchmarking Framework (`packages/calibration/src/nirikshak_calibration/evaluation.py`, `scripts/benchmark/run_calibration_evaluation.py`, 7 tests)

Together with the previous Phases 0–7, Member 2's core responsibilities for Computer Vision, Optical Calibration, Perspective Rectification, and Physical Measurement are fully implemented, defensively hardened, and benchmark-ready.

---

## 2. Phase 8: Robustness Hardening & Defensive Guarantees

Phase 8 guarantees that Member 2 entry points **never crash with unhandled exceptions** when presented with degenerate, adversarial, malformed, or out-of-distribution inputs.

### A. Defensive Seam Fixes
1. **String / Sequence Confusion in Coordinate Validation**: Coordinate sequences like `"1234"` (which satisfy `len(b) == 4` in Python) are rejected early via strict type validation (`isinstance(v, (int, float)) and not isinstance(v, bool)`).
2. **Channel Fallback in Grayscale Conversion**: Single-channel crops or intermediate arrays with shapes `(H, W, 1)` or `(H, W, 2)` are handled without crashing OpenCV `cv2.cvtColor`.
3. **Non-Numeric Cylinder Geometry Rejection**: Radii, centroids, and angular spans passed as strings, NaNs, or Infinities are caught and rejected with `CylinderMeasurementStatus.INVALID_CYLINDER_GEOMETRY`.
4. **Malformed Image Interception**: Micro-images, empty arrays `(0, 0, 3)`, 1D/4D shapes, and non-finite pixel values return structured failure statuses rather than raising unhandled exceptions.

### B. 9-Category Robustness Verification Matrix (90 Tests)
| Category | Scope | Behavior |
|:---|:---|:---|
| **1. Malformed Inputs** | `None`, non-arrays, non-numeric arrays, empty arrays, 1D/4D arrays | Graceful rejection with typed status |
| **2. Extreme Dimensions** | Micro-images `(1, 1, 3)`, `(2, 2, 3)`, extreme aspect ratios `(10, 4000, 3)` | Rejection with `IMAGE_TOO_SMALL` / status |
| **3. Channels & Dtypes** | Single-channel `(H, W)`, 2-channel, 4-channel RGBA, `float32`, `uint16`, `int32` | Automatic conversion or safe handling |
| **4. Degenerate Geometry** | Inverted bounding boxes ($y_{\min} \ge y_{\max}$), collinear quadrilateral points, non-convex polygons | Rejection with typed status; zero divide-by-zero crashes |
| **5. Degenerate Calibration** | Zero, negative, NaN, Inf scale factors, missing outcomes | Returns `UNCALIBRATED`; zero scale fabrication |
| **6. OCR Bounding Box Anomalies** | Large boxes exceeding image, negative coordinates, float coordinates | Safe clipping (`is_clipped=True`); original box preserved |
| **7. Noise, Contrast & Artifacts** | Pure black/white, pure Gaussian noise, heavy Gaussian blur | Safe handling without crash |
| **8. Caller Array Immutability** | Image arrays passed by callers to public functions | Deep verification that arrays are **never mutated in-place** |
| **9. Downstream Crash Prevention** | All public functions exercised with adversarial edge cases | 100% zero unhandled OpenCV exceptions |

---

## 3. Phase 9: Metric Calibration Evaluation Engine

The evaluation module provides a mathematically rigorous, reproducible framework for auditing the calibration pipeline against ground-truth datasets.

### A. Architectural Invariants
1. **Production Pipeline Execution**: Evaluates the real `detect_anchor()` and canonical `compute_scale_factor()` production routines.
2. **Ground Truth Isolation**: The reference ground truth scale ($S_{\text{gt}}$) and dimensions ($D_{\text{gt}}$) are used strictly as reference baselines and never leak into pipeline detection.
3. **Metric Units Separation**:
   - Scale factor error: strictly $\text{mm/px}$ (MAE, RMSE, P95) or $\%$ (Relative Error).
   - Packaging dimension error: strictly $\text{mm}$.
4. **Explicit Denominator Accounting**:
   - Scale MAE, RMSE, P95: denominator is strictly $N_{\text{scale}} = \text{scale\_evaluated\_samples}$.
   - Dimension MAE, RMSE, P95: denominator is strictly $N_{\text{dim}} = \text{dimension\_evaluated\_samples}$.
   - Calibration failure rate: denominator is $N_{\text{total}} = \text{total\_samples}$.
   - Failed calibrations cannot dilute or artificially alter scale error metrics.
5. **Scientifically Honest Evaluation State (`BENCHMARK_BLOCKED`)**:
   - No physical packaging ground-truth dataset currently exists in the repository.
   - The framework emits status **`BENCHMARK_BLOCKED`** and explicitly documents that real-world physical verification awaits physical specimens from Member 6.

### B. CLI Runner & Output Artifacts
```bash
# Execute evaluation engine across dataset
python scripts/benchmark/run_calibration_evaluation.py
```
Outputs:
- Machine-readable JSON: `benchmarks/results/calibration_evaluation_results.json`
- Human-readable report: `benchmarks/reports/calibration_evaluation_report.md`

---

## 4. Downstream Integration Guide

### A. For Member 1 (OCR Extraction)
- **Rectified Crops**: `rectify_planar_quadrilateral()` is safe to call on any detected card or planar panel corners.
- **Robustness**: Any token bounding boxes can be passed directly to `measure_font_height()`—negative coordinates, floating-point coordinates, and out-of-bound boxes are safely clipped without crashing.

### B. For Member 3 (Rules Engine)
- **Canonical Contracts**: All measurements emit standard `MeasurementResult` objects via `.to_measurement_result()`.
- **Zero Scale Fabrication**: If calibration is absent, status is `UNCALIBRATED` and physical values are `None`. Rules engine should route uncalibrated items to manual inspector review.
- **Zero Fabricated Uncertainty**: Uncertainty is populated only when propagated from an authenticated optical calibration outcome.

### C. For Member 6 (QA Lead)
- **Ground Truth Acquisition**: Member 6 can place packaging test images and corresponding ground-truth JSON metadata into `data/ground_truth/calibration/` and run `python scripts/benchmark/run_calibration_evaluation.py` to lift the `BENCHMARK_BLOCKED` status and generate certified physical calibration metrics.

---

## 5. Evidentiary Summary

- **Calibration Package Tests:** **180 / 180 PASSING** (100%)
- **Monorepo Tests:** **265 / 265 PASSING** (100% in 10.47s)
- **Git Working Tree:** Clean, verified, and synchronized through Phase 9.
