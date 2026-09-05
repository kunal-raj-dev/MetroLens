# Physical Scale Calibration & Fiducial Systems

## Purpose
Specifies the mathematical principles, calibration targets, homography estimations, error bounds, and failure modes used to establish physical millimetre scale from optical camera images.

## Scope
Applies to all dimensional calculations (font height, character width, PDP surface area).

## Authoritative Inputs
- Metrology principles: Pixels are not millimetres.
- ISO/IEC 17025 (Traceability in optical metrology).

## Assumptions
- The physical reference object is placed on or directly adjacent to the packaging panel in the same optical depth plane.

## Open Questions
- Evaluating camera sensor intrinsic calibration with smartphone autofocus variation [TBD — MEASURE].

## Dependencies
- `packages/calibration/`
- `experiments/calibration/`

## Verification Requirements
- Calibration error and uncertainty boundaries must be determined experimentally; acceptance threshold: `TBD — MEASURE` across test sets in `benchmarks/runs/` (`status: EXPERIMENT_REQUIRED`).

---

## 1. Supported Calibration Methods

### Method 1: Planar Reference Target (Primary Mode)
A standardized, high-contrast reference object of precisely verified physical dimensions is placed in the field of view:
- **Reference Standard:** Standardized physical calibration target (e.g. certified circular fiducial or precision checkerboard marker with dimension $D_{\text{calib}}$ verified via vernier caliper/micrometer).
- **Detection Algorithm:** Sub-pixel contour extraction and ellipse fitting.
- **Scale Factor Computation:**
  Let $d_{\text{px}}$ be the detected major axis in pixels.
  $$S = \frac{D_{\text{calib}}}{d_{\text{px}}} \quad (\text{mm/pixel})$$

### Method 2: Monocular Depth & Camera Intrinsics (Alternative Experimental Mode)
When camera intrinsic matrix $K$ and distance $Z$ to target are known via depth sensor/ArCore:
$$S(Z) = \frac{Z}{f_x}$$
*Note: Due to lens distortion and sensor variations, Method 2 is experimental and automatically applies wider uncertainty bounds ($\sigma_S$).*

### Method 3: Default Uncalibrated State (Mandatory Fallback)
If no reference marker is identified:
- Calibration status is set to: `UNCALIBRATED`.
- Physical scale factor $S$ is set to: `null`.
- **All dimensional rule evaluations route strictly to `REVIEW`.** The system NEVER invents a default pixel-to-mm ratio.

---

## 2. Perspective Rectification (Homography)

When the package face is tilted relative to the camera lens plane, perspective distortion alters apparent dimensions.
The system calculates a $3 \times 3$ planar homography matrix $H$:
$$\mathbf{p}_{\text{rectified}} = H \cdot \mathbf{p}_{\text{image}}$$

Homography $H$ is solved using 4 coplanar corner points of the detected package face or rectangular reference card. Measurements execute exclusively on the perspective-corrected rectified plane.
