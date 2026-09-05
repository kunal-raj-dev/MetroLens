# MEMBER 1 TO MEMBER 2 HANDOFF: CHUNK 3
**Document:** `AI_CONTEXT/HANDOFFS/M1_TO_M2_CHUNK3.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 2 (Computer Vision & Spatial Calibration Lead)  
**Date:** 2026-09-05T05:04:00+05:30  

---

## 1. Geometric Outputs Guaranteed
Member 1 confirms the following geometric guarantees:
1. **Coordinate System:** Original input image pixel space. Origin `(0.0, 0.0)` at top-left.
2. **Polygon Coordinates:** 4-point convex quadrilaterals `[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]` ordered clockwise starting from top-left.
3. **Bounding Envelope:** Axis-aligned bounding box `[xmin, ymin, xmax, ymax]`.
4. **Raw Pixel Height:** `raw_pixel_height` is strictly a quadrilateral stroke height primitive in pixels. Member 1 performs **zero physical mm conversion**.
5. **Coordinate Invariance Under Preprocessing:** Crop-level preprocessing operates strictly on text crops; original image polygons and bboxes suffer **0.0px distortion**.

## 2. Interface Needs from Member 2
1. **Cylindrical / Curved Packaging:** Curved surfaces on cans and bottles produce non-planar text perspective. When Member 2 provides an unwarped/rectified crop, Member 1's recognizer can transcribe it without model retraining.
2. **Optical Homography Rectification:** Extreme camera angle skew (>30°) degrades DBNet++ detection. Upstream homography rectification ensures orthogonal perspective for OCR.
3. **Ingestion Quality Gate:** Blur (Laplacian variance < 100) and severe specular glare obliterate text beyond classical restoration; Member 2's quality gate should reject such frames with an instructional retake prompt.
