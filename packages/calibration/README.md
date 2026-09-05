# Nirikshak Calibration Package (`nirikshak-calibration`)

**Package:** `packages/calibration/`
**Namespace:** `nirikshak_calibration`
**Role:** Member 2 — Computer Vision, Optical Calibration & Physical Measurement
**Standard Compliance:** SIH26034 / Nirikshak Anti-Hallucination Architectural Framework
**Status:** Phases 4, 5, 6, and 7 **COMPLETED & VERIFIED** (83 calibration unit tests passing)

---

## 1. Package Purpose & Architecture Seams

The `nirikshak-calibration` package provides deterministic, mathematically rigorous computer vision and optical calibration primitives for the Nirikshak / MetroLens AI platform. It converts 2D camera image coordinates into physical SI metric units (millimeters) for legal metrology compliance enforcement under the Legal Metrology (Packaged Commodities) Rules, 2011 (Rule 7 font height requirements).

### Architecture Alignment
- **AI PERCEIVES**: Downstream OCR models detect candidate text tokens.
- **MATH VALIDATES**: `nirikshak-calibration` deterministically fits ellipses, computes homography $H$, evaluates reprojection residuals, extracts vertical ink profiles, and computes cylindrical foreshortening.
- **RULES DECIDE**: Member 3's legal engine evaluates compliance against statutory tables.
- **HUMANS GOVERN**: Inspectors review ambiguous, uncalibrated, or flagged packaging scans.

### Scope Boundaries ("Not My Job")
- **NO OCR neural networks** (owned strictly by Member 1).
- **NO legal rule evaluations or penalty calculations** (owned strictly by Member 3).
- **NO web API endpoints or PDF reports** (owned strictly by Member 4).
- **NO React UI components** (owned strictly by Member 5).
- **NO CI/CD deployment pipelines** (owned strictly by Member 6).

---

## 2. Supported Metric Reference Anchors

The detector supports two physical reference targets:

### A. RBI Standard ₹10 Bimetallic Coin (`AnchorType.COIN_INR_10`)
- **Outer Diameter ($D_{\text{outer}}$):** $27.0\text{ mm}$ (circular outer brass ring).
- **Inner Core Diameter ($D_{\text{inner}}$):** $19.6\text{ mm}$ (circular inner nickel core).
- **Concentric Diameter Ratio ($D_{\text{inner}} / D_{\text{outer}}$):** $\approx 0.726 \pm 0.08$.
- **Geometric Model:** 2D perspective-projected ellipse characterized by centroid $(c_x, c_y)$, normalized major axis diameter ($d_{\text{major}}$), minor axis diameter ($d_{\text{minor}}$), and major-axis orientation angle ($\theta \in [0^\circ, 180^\circ)$).
- **Concentric Core Pairing:** When both outer brass rim and inner nickel core are detected, the inner core is absorbed into `ring_info` with a $+0.10$ concentricity bonus, preventing concentric circles from self-triggering ambiguity.

### B. ISO/IEC 7810 ID-1 Standard Card (`AnchorType.ID1_CARD`)
- **Physical Dimensions:** $85.60\text{ mm} \times 53.98\text{ mm}$.
- **Standard Aspect Ratio:** $85.60 / 53.98 \approx 1.5858$.
- **Geometric Model:** Planar quadrilateral characterized by strictly 4 ordered corner coordinates `(tl, tr, br, bl)` (top-left clockwise ordering) and width/height aspect ratio.

---

## 3. Public API & Usage

```python
import cv2
from nirikshak_calibration import (
    AnchorType,
    DetectionMode,
    DetectionStatus,
    detect_anchor,
)

# Load image (BGR numpy array)
image = cv2.imread("tests/fixtures/package_with_coin.jpg")

# 1. Automatic detection mode (evaluates both anchors, selects top candidate)
result = detect_anchor(image, anchor_type=DetectionMode.AUTO)

if result.detected and result.status == DetectionStatus.SUCCESS:
    print(f"Detected anchor: {result.anchor_type.value}")
    print(f"Confidence score: {result.confidence:.3f}")
    if result.anchor_type == AnchorType.COIN_INR_10:
        geom = result.geometry
        print(f"Coin center: ({geom.center.x:.1f}, {geom.center.y:.1f})")
        print(f"Major axis: {geom.major_axis_px:.1f} px, Minor axis: {geom.minor_axis_px:.1f} px")
        print(f"Orientation: {geom.angle_deg:.1f} deg")
    elif result.anchor_type == AnchorType.ID1_CARD:
        geom = result.geometry
        print(f"Card corners (TL, TR, BR, BL): {geom.corners}")
elif result.status == DetectionStatus.AMBIGUOUS_ANCHOR:
    print("Multiple competing anchors detected with indistinguishable scores.")
elif result.status == DetectionStatus.LOW_CONFIDENCE:
    print("Candidates found but failed the 0.50 confidence threshold.")
else:
    print(f"Detection failed: {result.status.value}")
```

---

## 4. Architectural Contracts & DTOs (`types.py`)

All data structures in `packages/calibration/src/nirikshak_calibration/types.py` are minimal, immutable, strongly typed, and free of untyped dictionary dumping grounds:

- **`Point2D`**: Immutable named tuple `(x: float, y: float)`.
- **`CircleGeometry`**: `center: Point2D`, `major_axis_px: float`, `minor_axis_px: float`, `angle_deg: float`.
  - *Invariant:* `major_axis_px >= minor_axis_px` is strictly guaranteed.
  - *Invariant:* `angle_deg` strictly corresponds to the orientation of the major axis.
- **`CardGeometry`**: `corners: Tuple[Point2D, Point2D, Point2D, Point2D]`, `aspect_ratio: float`.
  - *Invariant:* Ordered top-left, top-right, bottom-right, bottom-left.
- **`ConcentricRingInfo`**: `inner_major_axis_px: float`, `inner_minor_axis_px: float`, `inner_ratio: float`.
- **`AnchorDetectionResult`**:
  - `detected: bool`
  - `anchor_type: Optional[AnchorType]`
  - `status: DetectionStatus`
  - `confidence: float` (bounded to $[0.0, 1.0]$)
  - `geometry: Optional[Union[CircleGeometry, CardGeometry]]`
  - `fit_quality: float` (ellipse/polygon residual metric)
  - `ring_information: Optional[ConcentricRingInfo]`

---

## 5. Mathematical Algorithms & Implementation Details

### A. Normalized Algebraic Ellipse Residual
Given contour points $(x_i, y_i)$ and fitted ellipse parameters $(c_x, c_y, a, b, \theta)$ where $a = \frac{d_{\text{major}}}{2}$ and $b = \frac{d_{\text{minor}}}{2}$, points are translated to centroid and rotated into ellipse-aligned coordinates:
$$x'_i = (x_i - c_x)\cos\theta + (y_i - c_y)\sin\theta$$
$$y'_i = -(x_i - c_x)\sin\theta + (y_i - c_y)\cos\theta$$
The mean algebraic residual measures shape fidelity:
$$\epsilon_{\text{ellipse}} = \frac{1}{N}\sum_{i=1}^N \left| \left(\frac{x'_i}{a}\right)^2 + \left(\frac{y'_i}{b}\right)^2 - 1 \right|$$
Contours with $\epsilon_{\text{ellipse}} > 0.15$ are rejected as non-elliptical.

### B. Ellipse Axis & Angle Canonical Normalization
OpenCV's `cv2.fitEllipse()` returns axis lengths $(d_1, d_2)$ where $d_1$ aligns with `raw_angle`, but $d_1$ may be the minor axis. To ensure downstream consumers always receive canonical geometry:
$$\text{If } d_1 < d_2: \quad d_{\text{major}} = d_2, \quad d_{\text{minor}} = d_1, \quad \theta = (\text{raw\_angle} + 90^\circ) \pmod{180^\circ}$$
$$\text{Else}: \quad d_{\text{major}} = d_1, \quad d_{\text{minor}} = d_2, \quad \theta = \text{raw\_angle}$$

### C. Spatial Non-Maximum Suppression (NMS)
To prevent dual edge detections (e.g., inner and outer stroke contours of a coin boundary) from competing against each other and triggering false ambiguity, candidates with centroid distance $\Delta_{\text{center}} \le 0.25 \times d_{\text{major}}$ are deduplicated, preserving the highest-scoring candidate.

### D. Evidence Scoring & AUTO Ranking Semantics
Candidate detector scores use a structured tripartite evidence breakdown:
- **Shape Fidelity (45%):** Residual fit quality.
- **Boundary Gradient (30%):** Sobel edge magnitude along the perimeter.
- **Planar Regularity (25%):** Area solidity (coin) or corner angle orthogonality (card).

> [!NOTE]
> Candidate scores are **normalized heuristic evidence indices** on $[0.0, 1.0]$ designed for deterministic candidate ranking within a scene, not calibrated Bayesian probabilities. All scores are strictly clamped to $[0.0, 1.0]$ after ring bonuses ($+0.10$) and tilt penalties.

### E. Confidence Gating & Ambiguity Margin
- **Confidence Gate:** Top candidate must achieve $\text{score} \ge 0.50$; otherwise returns `LOW_CONFIDENCE`.
- **Ambiguity Margin:** If two distinct spatial candidates both exceed $0.50$ and satisfy $|S_1 - S_2| < 0.08$, the detector flags `AMBIGUOUS_ANCHOR`. Noise blobs $< 0.50$ are never allowed to trigger ambiguity.

---

## 6. Phase 5: Planar Homography & Perspective Rectification

Computes the $3 \times 3$ projective homography matrix $H$ and warps planar quadrilateral crops into top-down orthorectified coordinates (`homography.py`):
- **Geometric Validation**: Verifies 4 points, finite coordinates (no NaN/Inf), no duplicates ($> 2\text{px}$), non-degenerate area ($> 400\text{px}^2$), non-collinearity, strict convexity (Shoelace cross product sign consistency), and image domain boundary containment.
- **Canonical Destination Mapping**:
  $$TL \to (0, 0), \quad TR \to (W-1, 0), \quad BR \to (W-1, H-1), \quad BL \to (0, H-1)$$
- **Numerical Reprojection Error**:
  $$\epsilon_{\text{reproj}} = \frac{1}{4} \sum_{i=1}^4 \|\tilde{p}'_i - p_{\text{dst}, i}\|$$
  Enforces `mean_reproj_err <= cfg.max_reprojection_error_px` (default $5.0\text{px}$), rejecting unstable transformations with `TRANSFORMATION_FAILED`.
- **Derived Dimensions**: If explicit dimensions are omitted, deterministically derives width from the average of top and bottom edge lengths, and height from the average of left and right edge lengths.

---

## 7. Phase 6: Physical Font Height Measurement

Converts OCR bounding box observations into physical metric millimeters for Rule 7 verification (`font_measurer.py`):
- **Critical Conceptual Distinction**:
  - `BOUNDING_BOX_HEIGHT`: Measures raw bounding box pixel height $(y_{\max} - y_{\min}) \times S$.
  - `INK_PROFILE_HEIGHT`: Isolates true foreground printed glyph height via Otsu binarization and vertical projection profiling $P(y) = \sum_x M(y, x)$. Demonstrates that $h_{\text{bbox}} \neq h_{\text{ink}}$ when whitespace padding exists.
- **Zero Scale Fabrication**: Returns `UNCALIBRATED` status if optical calibration is missing, non-finite, $\le 0$, or marked uncalibrated. Never fabricates scale.
- **Zero Manufactured Uncertainty**: Uncertainty is propagated ($\Delta h_{\text{mm}} = h_{\text{px}} \times \Delta S$) ONLY when explicitly provided by `CalibrationOutcome.uncertainty_mm_per_pixel`; returns `None` when unavailable.
- **Coordinate Validation & Clipping**: Rejects inverted coordinates ($y_{\min} \ge y_{\max}$), safely clips out-of-bounds crops while flagging `is_clipped=True` and preserving `original_bounding_box`.
- **Contract Bridge**: Provides `.to_measurement_result()` producing canonical `nirikshak_shared.models.contracts.MeasurementResult`.

---

## 8. Phase 7: Constrained Cylindrical Packaging Measurement

Provides geometric correction for curved packaging surfaces (cans, jars, bottles) in `cylinder.py`:
- **Surface Geometry State Machine**:
  - `PLANAR`: No correction applied (`PLANAR_NO_CORRECTION`, factor = 1.0).
  - `CYLINDRICAL`: Permitted constrained vertical-generator measurement.
  - `UNSUPPORTED_TAPERED`: Rejected routing to `MANUAL_REVIEW_REQUIRED`.
  - `UNKNOWN`: Rejected routing to `MANUAL_REVIEW_REQUIRED`.
- **Right-Cylinder Vertical Generator Invariance**:
  - For a right circular cylinder whose axis is aligned with the measurement coordinate system (`is_axis_aligned=True`) and for a locally applicable calibrated scale, axial distance along the generator is preserved:
    $$h_{\text{axial\_mm}} = h_{\text{vertical\_px}} \times S$$
- **Circumferential Foreshortening**:
  - Horizontal dimensions along the curved circumference are foreshortened by $\cos\phi$:
    $$w_{\text{true\_px}} \approx \frac{w_{\text{measured\_px}}}{\cos\phi}$$
- **Mathematical Classification of Foreshortening**:
  - $\frac{1}{\cos\phi} - 1 = \sec\phi - 1$ is an analytical **mathematical property** whose derivative $\sec\phi\tan\phi > 0$ guarantees strictly monotonic increasing distortion with $|\phi| \in (0, \pi/2)$. Verified via automated unit tests.
- **Central Vertical Strip Constraint**:
  - Proposed heuristic boundary: $|\phi| \le 20.0^\circ$ ($\cos\phi \ge 0.9397$).
  - At $20^\circ$, foreshortening correction reaches approximately $6.42\%$.
  - Exceeding $20^\circ$ flags `EXCEEDS_ANGULAR_THRESHOLD`.
- **Contract Bridge**: Provides `.to_measurement_result()` producing canonical `nirikshak_shared.models.contracts.MeasurementResult`.

---

## 9. Public API Quick Reference

```python
from nirikshak_calibration import (
    # Phase 4: Anchor Detection
    detect_anchor,
    DetectionMode,
    AnchorType,
    DetectionStatus,
    AnchorDetectionResult,
    # Phase 5: Homography & Rectification
    rectify_planar_quadrilateral,
    RectificationStatus,
    RectificationResult,
    HomographyConfig,
    # Phase 6: Font Measurement
    measure_font_height,
    batch_measure_font_height,
    FontMeasurementType,
    FontMeasurementStatus,
    FontMeasurementResult,
    # Phase 7: Cylindrical Measurement
    measure_cylindrical_feature,
    CylinderGeometryState,
    CylinderMeasurementStatus,
    CylinderMeasurementResult,
    CylinderModelConfig,
    # Core Scale Model
    compute_scale_factor,
    CalibrationOutcome,
)
```

---

## 10. Verification Suite & Test Evidence

The package includes **83 automated unit tests** across 5 test suites:

```bash
# Execute complete calibration package test suite (83 tests)
pytest packages/calibration/tests -v

# Execute monorepo regression suite (168 tests)
pytest -q
```

| Test Suite | File | Tests | Coverage Scope |
|:---|:---|:---:|:---|
| **Phase 4 Anchor Detector** | `test_anchor_detector.py` | 32 | ₹10 coin, ID-1 card, ellipse fit, NMS, concentric bonus, glare, clutter, ambiguity. |
| **Phase 5 Homography** | `test_homography.py` | 19 | Identity, warp, card geometry, collinearity, non-convex, reprojection tolerance. |
| **Phase 6 Font Measurer** | `test_font_measurer.py` | 14 | Scale conversion, ink profiling vs bbox, clipping, uncalibrated scale, uncertainty. |
| **Phase 7 Cylinder** | `test_cylinder.py` | 16 | Central strip, 20° heuristic, generator invariance, planar, tapered/unknown, contracts bridge. |
| **Calibration Baseline Smoke** | `test_calibration_smoke.py` | 2 | Fiducial reference scale computation baseline. |
| **Total** | | **83** | **100% passing** |

---

## 11. Scientific Evidentiary Standard Notice

> [!IMPORTANT]
> **Anti-Hallucination Architectural Policy**:
> - The 83 automated unit tests verify software correctness, numerical stability, coordinate geometry transforms, and error-handling paths against controlled synthetic geometries and mathematical specifications.
> - They do **NOT** certify real-world physical calibration accuracy under uncontrolled smartphone optical distortion.
> - Real-world physical accuracy remains strictly **PENDING** until Member 6 (QA Lead) acquires physical packaging specimens and 1200 DPI flatbed optical scans for ground-truth verification.
