# INTER-PHASE HANDOFF CONTRACT: PHASE 4 ──► PHASE 5
**Project:** MetroLens AI / Nirikshak (SIH26034)
**Workstream:** Member 2 — Computer Vision, Optical Calibration & Physical Measurement
**Handoff Point:** Phase 4 (Metric Anchor Detection) ──► Phase 5 (Planar Homography & Perspective Rectification)
**Date:** 2026-09-05

---

## 1. Executive Purpose

This handoff contract establishes the exact mathematical, programmatic, and behavioral interface exported by Phase 4 (`packages/calibration/src/nirikshak_calibration/anchor_detector.py`) and ingested by Phase 5 (`packages/calibration/src/nirikshak_calibration/homography.py`).

Phase 5 relies exclusively on the typed structures delivered by Phase 4 and must not re-implement contour extraction, ellipse fitting, or corner detection.

---

## 2. Ingested Data Transfer Objects (DTOs)

Phase 5 imports its inputs directly from `nirikshak_calibration`:

```python
from nirikshak_calibration import (
    AnchorDetectionResult,
    AnchorType,
    DetectionStatus,
    CircleGeometry,
    CardGeometry,
    Point2D,
    ConcentricRingInfo,
)
```

### Schema Guarantees:

#### A. When `result.status == DetectionStatus.SUCCESS` and `result.anchor_type == AnchorType.ID1_CARD`:
- `result.geometry` is guaranteed to be an instance of `CardGeometry`.
- `geometry.corners` is strictly a 4-element tuple of `Point2D(x, y)` ordered as:
  1. `corners[0]`: Top-Left ($x_{\text{tl}}, y_{\text{tl}}$)
  2. `corners[1]`: Top-Right ($x_{\text{tr}}, y_{\text{tr}}$)
  3. `corners[2]`: Bottom-Right ($x_{\text{br}}, y_{\text{br}}$)
  4. `corners[3]`: Bottom-Left ($x_{\text{bl}}, y_{\text{bl}}$)
- `geometry.aspect_ratio` matches the card's bounding quadrilateral ratio ($85.60 / 53.98 \approx 1.5858 \pm 0.30$).
- **Phase 5 Target Destination Coordinates:**
  Standard ISO/IEC 7810 ID-1 card dimensions ($85.60\text{ mm} \times 53.98\text{ mm}$). For an unwarped image at resolution scale $K\text{ px/mm}$:
  $$\text{Dst}_{\text{corners}} = [(0, 0), (K \cdot 85.60, 0), (K \cdot 85.60, K \cdot 53.98), (0, K \cdot 53.98)]$$

#### B. When `result.status == DetectionStatus.SUCCESS` and `result.anchor_type == AnchorType.COIN_INR_10`:
- `result.geometry` is guaranteed to be an instance of `CircleGeometry`.
- `geometry.center` is `Point2D(x, y)` representing the ellipse centroid in pixel coordinates.
- `geometry.major_axis_px >= geometry.minor_axis_px` is mathematically guaranteed by Phase 4 normalization.
- `geometry.angle_deg` strictly specifies the orientation angle of the **major axis** ($\theta \in [0^\circ, 180^\circ)$).
- `ring_information` contains `ConcentricRingInfo(inner_major_axis_px, inner_minor_axis_px, inner_ratio)` if bimetallic core was detected.
- **Phase 5 Physical Scale Recovery:**
  $$S = \frac{27.0\text{ mm}}{d_{\text{major}}\text{ px}} \quad (\text{accurate to } < 5.0\% \text{ for tilt } \le 15^\circ)$$

#### C. When `result.status != DetectionStatus.SUCCESS`:
- `result.detected` is `False`.
- `result.geometry` is `None`.
- Phase 5 must handle failure gracefully: emit `is_calibrated: false`, bypass perspective unwarping, and provide the unrectified image with diagnostic status to downstream consumers.

---

## 3. Phase 5 Scope Boundaries

### Concrete Phase 5 Responsibilities:
1. Compute $3 \times 3$ planar homography transformation matrix $H$ via `cv2.getPerspectiveTransform()` (card) or circle-to-circle projective correspondence.
2. Apply `cv2.warpPerspective()` to generate orthorectified, top-down packaging panel crops.
3. Compute reprojection residual error to quantify homography geometric stability.
4. Calculate perspective-corrected physical scale factor $S = \text{mm/px}$.

### Explicit Phase 5 Non-Goals:
- **NO OCR text recognition** (owned by Member 1).
- **NO numeral font height measurement** ($h_{\text{mm}} = h_{\text{px}} \times S$) &rarr; reserved for Phase 6 (`font_measurer.py`).
- **NO cylindrical surface distortion compensation** &rarr; reserved for Phase 7 (`cylinder.py`).
- **NO legal metrology compliance rules or penalty evaluations** (owned by Member 3).
- **NO FastAPI routes or web endpoints** (owned by Member 4).
