# Inter-Member Handoff: Member 1 (OCR) to Member 2 (Vision & Measurement) — Chunk 4
**Document:** `AI_CONTEXT/HANDOFFS/M1_TO_M2_CHUNK4.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 2 (Computer Vision, Metric Calibration & Measurement Lead)  
**Date:** 2026-09-05T05:35:00+05:30  
**Phase:** Chunk 4 Delivery  
**Status:** READY FOR OPTICAL MEASUREMENT & CALIBRATION INTEGRATION  

---

## 1. Handoff Summary
Member 1 provides strict geometric guarantees on OCR token bounding boxes and coordinates, enabling Member 2 to execute Table-I Rule 7 physical font height measurements in millimeters.

---

## 2. Geometric Guarantees & Coordinate Space

### 2.1 Coordinate Alignment
- All polygon vertices returned by `OCRService` are in **original image pixel coordinates** ($W \times H$).
- If Member 2 downsamples or crops an image prior to passing it to OCR, Member 2 must maintain the transformation affine matrix to map OCR coordinates back to physical millimeters.
- Alternatively, Member 2 can pass the full-resolution unrectified image directly to `OCRService` and apply calibration scale factors ($\text{mm}/\text{px}$) directly to the returned token polygons.

### 2.2 Vertex Ordering
Vertices are strictly ordered clockwise:
```text
(x0, y0) [Top-Left] -----------------> (x1, y1) [Top-Right]
       ^                                      |
       |                                      |
       |                                      v
(x3, y3) [Bottom-Left] <-------------- (x2, y2) [Bottom-Right]
```
For angled or sheared text lines:
$$\text{Line Height (px)} = \frac{\|(x_3, y_3) - (x_0, y_0)\| + \|(x_2, y_2) - (x_1, y_1)\|}{2}$$

### 2.3 Table-I Font Height Calculation
Member 2 applies the optical calibration ratio $K$ (mm per pixel, obtained from ArUco marker or reference coin):
$$\text{Physical Height (mm)} = \text{Line Height (px)} \times K$$
Member 2 then checks compliance against Table-I minimum height requirements (e.g. $\ge 1.0\text{ mm}$, $\ge 2.0\text{ mm}$, $\ge 4.0\text{ mm}$ depending on net quantity).

### 2.4 Input Immutability
`OCRService.convert_image_input()` performs a defensive copy on any input `np.ndarray`. Member 2 can safely reuse or pass image buffers without concern for in-place modifications by OCR.
