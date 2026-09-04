# Physical Measurement & Optical Calibration Limitations

## Purpose
Documents the optical physics constraints, sensor geometry limits, and uncertainty bounds governing physical millimetre measurements.

## Metrological Principles & Empirical Limitations

1. **Pixels Are Not Millimetres:** The system strictly refuses to calculate physical dimensions from an arbitrary, uncalibrated photograph. Without an authenticated physical reference target, dimensional calculations are blocked and routed to `REVIEW`.
2. **Co-Planarity Requirement:** Physical planar reference calibration assumes the calibration target is placed coplanar with the packaging surface. Depth offset between the target and package face introduces perspective homography error; the maximum acceptable coplanarity displacement tolerance cannot be assumed a priori and must be empirically determined via calibration benchmark PROTO-CALIB-001 (`status: EXPERIMENT_REQUIRED`).
3. **Borderline Uncertainty Policy:** In any measurement where the expanded uncertainty interval $[H_{\text{font}} - U(H), H_{\text{font}} + U(H)]$ overlaps with a statutory minimum height boundary (defined in Table-I for the corresponding PDP area), the system deliberately refuses to emit a binary `PASS` or `FAIL` verdict and outputs `REVIEW`. The numerical width of the uncertainty band $U(H)$ is not fixed in documentation and must be calculated dynamically from sensor resolution, calibration residuals, and optical modulation transfer function (`status: EXPERIMENT_REQUIRED`).
4. **Resolution & Optical Sampling Limits:** Character strokes require sufficient optical pixel density (Nyquist spatial sampling) across stroke widths to achieve valid contour measurement. Minimum acceptable pixels-per-millimetre (PPM) thresholds and camera working distance limits are sensor-dependent and must be established through empirical optical testing (`status: EXPERIMENT_REQUIRED`). If optical sampling falls below the calibrated threshold, the system triggers a `REQUEST_RETAKE` prompt rather than guessing.
