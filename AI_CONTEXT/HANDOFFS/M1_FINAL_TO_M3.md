# Inter-Member Final Handoff: Member 1 (OCR) -> Member 3 (Physical Vision & Calibration)

**From**: Member 1 — AI & Multilingual OCR Lead  
**To**: Member 3 — Computer Vision & Physical Calibration Lead  
**Date**: September 2026  
**Status**: **FROZEN & PRODUCTION READY**

---

## 1. Executive Summary & Interface Contract

Member 1 provides Member 3 with mathematically valid, clockwise 4-point bounding polygons and bounding boxes for every detected text line on packaging.

### Ingestion Interface:
```python
from nirikshak_ocr import OCRService
from nirikshak_shared.ocr_contract import OCRObservation

service = OCRService()
observations = service.extract_observations(image_bytes)

for obs in observations:
    # 4 clockwise polygon points: (x, y) in original frame pixel coordinates
    poly = obs.polygon.points
    # Bounding box: (xmin, ymin, xmax, ymax)
    xmin, ymin, xmax, ymax = obs.bounding_box
    pixel_height = ymax - ymin
```

---

## 2. Spatial Guarantees for Physical Calibration

1. **Clockwise Ordering**: All bounding polygons are guaranteed to have 4 vertices in clockwise order: Top-Left -> Top-Right -> Bottom-Right -> Bottom-Left.
2. **Original Frame Coordinate Alignment**: Coordinates correspond 1-to-1 with unscaled, unwarped input image dimensions $(W, H)$.
3. **Positive Area**: Every emitted polygon has a strictly positive area $>0$.

---

## 3. Strict Boundary Rules for Member 3

1. **Member 3 Owns**:
   - Reference target detection (e.g., ArUco markers, standard metric reference cards, coin fiducials).
   - Computing camera pixels-per-millimeter calibration scale factor ($S_{mm/px}$).
   - Computing Principal Display Area (PDA) in $\text{cm}^2$.
   - Converting text pixel height to physical millimeters ($H_{mm} = H_{px} \times S_{mm/px}$) to evaluate minimum font height compliance under Rule 5 & Schedule II.
2. **Member 3 Must NOT**:
   - Attempt to re-run OCR or modify OCR token strings.
   - Modify or rebuild any code in `packages/ocr/` (permanently frozen per `MEMBER_1_DO_NOT_REBUILD.md`).
