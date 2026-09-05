# M1 FINAL AUDITED HANDOFF TO MEMBER 2 (VISION & OPTICAL CALIBRATION)

**From**: Member 1 (AI & Multilingual OCR Lead)  
**To**: Member 2 (Computer Vision & Camera Calibration Lead)  
**Date**: 2026-09-05  
**Freeze Status**: AUDITED & FROZEN  

---

## 1. Coordinate System & Geometry Convention
Member 1 outputs raw optical geometry strictly referenced to the original input image:
- **Coordinate Space**: Unnormalized pixel coordinates `[0.0, W]` and `[0.0, H]`.
- **Origin**: `(0.0, 0.0)` at the top-left corner of the image.
- **Orientation**: X-axis increases horizontally to the right; Y-axis increases vertically downward.
- **Polygon Representation**: 4-point quadrilateral `[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]` ordered strictly clockwise:
  `[top-left, top-right, bottom-right, bottom-left]`.
- **Bounding Box**: Derived axis-aligned envelope `[xmin, ymin, xmax, ymax]`.
- **Raw Pixel Height (`raw_pixel_height`)**: Average length of side edges:
  `h_px = (||p3 - p0|| + ||p2 - p1||) / 2` in image pixels.

## 2. Inviolable Boundary between M1 and M2
- **M1 Role**: Detects text quads and extracts raw character strokes in pixel units.
- **M2 Role**: Computes metric scale factor (`scale_factor_mm_per_pixel`) via optical fiducial marker calibration (e.g. ArUco or reference coin) and converts `raw_pixel_height` into physical millimeters (`measured_mm`).
- **RULE**: M1 does NOT compute millimeters. M2 does NOT rerun OCR or alter polygon vertex ordering.

## 3. Input Image Quality Requirements for M1
To maximize OCR accuracy, upstream image processing by Member 2 should provide:
- **Planar Surface**: Dewarped 2D rectilinear image (cylindrical / perspective distortion corrected).
- **Glare Removal**: Diffuse lighting without clipped specular whiteouts on glossy foil surfaces.
- **Minimum Stroke Height**: Character stroke height >= 8 pixels in the uncropped frame.
- **Max Resolution**: Below 64 Megapixels (inputs exceeding 64 MP are rejected by M1 decompression bomb guard).

## 4. Known Limitations
- Cylindrical curvature degrades DBNet++ bounding polygons if uncorrected upstream.
- Extremely low contrast packaging requires upstream photometric normalization or M1's optional adaptive CLAHE hook.
