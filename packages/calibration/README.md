# Nirikshak Calibration Package (`nirikshak-calibration`)

## Purpose
Detects physical optical reference fiducials (e.g. AruCo tags, reference calibration coin/strip) to compute the metric physical scale factor $S = \text{mm}/\text{pixel}$ and measurement uncertainty bounds.

## Owner
CV / Measurement Lead

## Interface Seams
- **Input**: Image frame array, known physical reference dimension (mm).
- **Output**: `CalibrationOutcome` with `scale_factor_mm_per_pixel`, `uncertainty_mm_per_pixel`, and `calibration_status`.
- **Error Codes**: `ERR_CALIBRATION_FAILED`.
