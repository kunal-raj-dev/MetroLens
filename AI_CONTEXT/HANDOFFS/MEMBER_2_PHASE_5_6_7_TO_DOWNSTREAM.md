# INTER-WORKSTREAM HANDOFF CONTRACT: PHASES 5, 6 & 7 COMPLETE
**Project:** MetroLens AI / Nirikshak (SIH26034)
**Workstream:** Member 2 — Computer Vision, Optical Calibration & Physical Measurement
**Handoff Recipients:** Member 1 (OCR Extraction) & Member 3 (Rules Engine)
**Status:** 🟢 Complete & Verified (83/83 calibration tests, 168/168 monorepo tests passing)

---

## 1. Executive Purpose

This handoff contract establishes the exact programmatic interfaces, mathematical guarantees, and behavioral contracts exported by Member 2 upon completion of:
- **Phase 5:** Planar Homography & Perspective Rectification (`packages/calibration/src/nirikshak_calibration/homography.py`)
- **Phase 6:** Physical Font Height Measurement (`packages/calibration/src/nirikshak_calibration/font_measurer.py`)
- **Phase 7:** Constrained Cylindrical Packaging Measurement (`packages/calibration/src/nirikshak_calibration/cylinder.py`)

---

## 2. Downstream Interface Contracts

### A. For Member 1 (OCR Extraction Pipeline)
Member 1 consumes rectified planar panel crops to maximize character recognition fidelity:

```python
from nirikshak_calibration import rectify_planar_quadrilateral, RectificationStatus

# Ingest quadrilateral coordinates from Member 2 CardGeometry or detector
rect_res = rectify_planar_quadrilateral(
    corners=card_geometry.corners,
    image=raw_image_bgr,
)

if rect_res.success and rect_res.status == RectificationStatus.SUCCESS:
    # Top-down orthorectified image ready for OCR inference:
    ocr_crop = rect_res.rectified_image
    reproj_err = rect_res.reprojection_error_px  # < 5.0 px guaranteed
else:
    # Graceful degradation fallback: use original unrectified image
    ocr_crop = raw_image_bgr
```

### B. For Member 3 (Statutory Rules Engine)
Member 3 consumes canonical `MeasurementResult` objects for evaluating Rule 7 minimum numeral height compliance:

```python
from nirikshak_calibration import measure_font_height, measure_cylindrical_feature, CylinderGeometryState
from nirikshak_shared.models.contracts import MeasurementResult

# 1. Planar package font height measurement:
font_res = measure_font_height(
    bounding_box=ocr_bounding_box,
    calibration=calibration_outcome,
    image=rectified_crop,  # Optional: enables Otsu vertical ink profiling
)
# Convert to canonical shared contract:
measurement: MeasurementResult = font_res.to_measurement_result(feature_name="numeral_height_mm")

# 2. Cylindrical package font height measurement:
cyl_res = measure_cylindrical_feature(
    feature_box=ocr_bounding_box,
    geometry_state=CylinderGeometryState.CYLINDRICAL,
    cylinder_center_x=cylinder_center_px,
    cylinder_radius_px=cylinder_radius_px,
    calibration=calibration_outcome,
    is_axis_aligned=True,
)
cyl_measurement: MeasurementResult = cyl_res.to_measurement_result(feature_name="numeral_height_mm")
```

---

## 3. Evidentiary Boundary & Anti-Hallucination Policy

> [!IMPORTANT]
> - All mathematical routines, coordinate transformations, and error handlings are verified via 83 automated unit tests against synthetic test geometries.
> - Real-world physical measurement accuracy remains strictly **PENDING** physical packaging specimen scans by Member 6 (QA Lead).
