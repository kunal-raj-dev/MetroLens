# Nirikshak Calibration Package (`nirikshak-calibration`)

**Package:** `packages/calibration/`
**Namespace:** `nirikshak_calibration`
**Role:** Member 2 — Computer Vision, Optical Calibration & Physical Measurement
**Standard Compliance:** SIH26034 / Nirikshak Anti-Hallucination Architectural Framework
**Current Phase Status:** Phase 4 (Metric Anchor Detection) **COMPLETED** | Phase 5 (Planar Homography) **QUEUED**

---

## 1. Package Purpose & Scope

The `nirikshak-calibration` package solves the fundamental monocular scale ambiguity of consumer smartphone camera uploads. It delivers mathematically verifiable physical references required to convert 2D pixel measurements into physical SI metric units (millimeters) for legal metrology compliance enforcement under the Legal Metrology (Packaged Commodities) Rules, 2011 (Rule 7 font height requirements).

### Scope Boundary (Phase 4 vs Subsequent Phases)
- **Phase 4 Boundary (Current):** **METRIC ANCHOR DETECTION ONLY**. Detects and characterizes candidate physical calibration anchors (₹10 coin and ISO ID-1 card) in 2D image coordinates, filters noise blobs, resolves multi-candidate ambiguity, and outputs strongly typed geometric descriptions.
- **Explicit Phase 4 Non-Goals:** Does **NOT** compute metric scale factor ($S = \text{mm/px}$), does **NOT** compute planar homography matrices ($H$), does **NOT** perform cylinder unrolling, does **NOT** measure font heights, and does **NOT** evaluate statutory compliance rules.

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

## 6. Verification Suite & Test Evidence

The package includes 32 deterministic unit tests in `packages/calibration/tests/test_anchor_detector.py`:
- **Mathematical Invariants:** Algebraic residual formulas, corner ordering, ellipse axis/angle normalization.
- **Synthetic Geometry Tests:** Clean circles, perspective-tilted ellipses ($10^\circ, 20^\circ, 30^\circ$), concentric ring bonuses, clean cards, rotated cards.
- **Adversarial Noise & Robustness:** Circular glare spots (rejected by gradient), background clutter, low contrast, non-convex quadrilaterals, invalid aspect ratios.
- **Ranking & Ambiguity:** Multi-candidate determinism, identical coin ambiguity, low-confidence gating prior to ambiguity.
- **Dispatch Modes:** Forced `COIN` mode, forced `CARD` mode, automatic `AUTO` mode.
- **Input Sanitization:** `None`, empty arrays, non-array inputs, 1D/4D shapes, single-channel/multi-channel formats, non-finite floats (`NaN`, `+Inf`, `-Inf`).
- **Performance & Latency:** Execution latency strictly $< 50\text{ms}$ on CPU.
- **Score Range Guarantee:** Verified that all candidate scores remain strictly within $[0.0, 1.0]$ after all bonuses and penalties.

```bash
# Execute Phase 4 unit tests
pytest packages/calibration/tests/test_anchor_detector.py -v

# Execute monorepo regression suite
pytest -q
```

---

## 7. Evidentiary Standards & Next Phase

> [!IMPORTANT]
> **Evidentiary Boundary Notice**: The 32 deterministic automated tests verify software correctness, numerical stability, and algorithmic contracts under controlled synthetic geometries. They do **NOT** certify real-world physical calibration accuracy. Physical validation remains strictly **PENDING** until Member 6 (QA Lead) acquires physical packaging specimens and 1200 DPI flatbed optical scans.

**Next Milestone:** Phase 5 — Planar Homography & Perspective Rectification (`packages/calibration/homography.py`).
