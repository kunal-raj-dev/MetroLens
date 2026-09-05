# INTER-MEMBER HANDOFF SPECIFICATION: M1 ──► M2
### Optical Character Recognition (M1) to Calibration & Measurement Subsystem (M2)
**Document:** `AI_CONTEXT/HANDOFFS/M1_TO_M2_CHUNK2.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 2 (Computer Vision, Metric Calibration & Measurement Lead)  
**Status:** FROZEN CONTRACT (Chunk 2 Complete)  
**Timestamp:** 2026-09-05T04:33:00+05:30  

---

## 1. Executive Contract Summary
This document establishes the inviolable geometric and data boundary between Member 1's OCR Perception Engine and Member 2's Metric Scale & Calibration Pipeline.

```text
┌────────────────────────────────────────────────────────┐
│ MEMBER 1 (OCR PERCEPTION)                              │
│ • Detects text polygons in original image pixels       │
│ • Recognizes alphanumeric & Devanagari text sequences  │
│ • Computes raw quadrilateral pixel height (raw_pixel_h)│
└───────────────────────────┬────────────────────────────┘
                            │ Handed off via OCRToken / OCRObservation
                            ▼
┌────────────────────────────────────────────────────────┐
│ MEMBER 2 (CALIBRATION & PHYSICAL MEASUREMENT)          │
│ • Detects calibration reference fiducials (e.g. coin)  │
│ • Computes optical scale factor S (mm/pixel)           │
│ • Rectifies perspective distortion via homography H    │
│ • Computes physical font height: H_font = h_px * S mm  │
│ • Calculates Principal Display Panel (PDP) surface area│
└────────────────────────────────────────────────────────┘
```

---

## 2. What Member 1 PROVIDES to Member 2

Member 1 delivers raw optical observations strictly bounded to **original image pixel space**:

1. **Original Image Dimensions:**
   - `image_width: int` (pixels)
   - `image_height: int` (pixels)
2. **Clockwise 4-Point Quadrilateral Polygons:**
   - `polygon: List[List[float]]`: Exactly 4 vertices `[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]` ordered clockwise:
     `[top-left, top-right, bottom-right, bottom-left]`.
   - Coordinates refer to the unscaled, original input image pixel space. Origin `(0.0, 0.0)` is top-left.
3. **Axis-Aligned Bounding Box (Derived Envelope):**
   - `bbox: List[float]`: `[xmin, ymin, xmax, ymax]` in original image pixels.
4. **Transcribed Character Text:**
   - `text: str`: Raw character transcription (e.g., `"Net Qty: 65 g"`, `"अधिकतम खुदरा मूल्य"`).
5. **Token Confidence:**
   - `confidence: float`: Decoder confidence in range `[0.0, 1.0]`.
6. **Script Category:**
   - `script: ScriptType`: `'latin'`, `'devanagari'`, or `'unknown'`.
7. **Line & Region Identification:**
   - `line_id: int`: Assigned reading order sequence index.
8. **Raw Pixel Height (Geometry Primitive):**
   - `raw_pixel_height: float`: Average quadrilateral edge height in original image pixels:
     $$\text{raw\_pixel\_height} = \frac{\|p_3 - p_0\| + \|p_2 - p_1\|}{2}$$
     **NOTE:** THIS IS A RAW PIXEL MEASUREMENT ONLY. IT IS NOT STATUTORY OR LEGAL FONT HEIGHT.

---

## 3. What Member 1 DOES NOT Provide ("Not Member 1's Job")

Member 1 explicitly **does NOT compute or provide**:
- ❌ **Physical Scale Factor:** Member 1 does not know or compute $S$ ($\text{mm/px}$).
- ❌ **Physical Millimetre Dimensions:** Member 1 never outputs millimeters ($H_{\text{mm}}$).
- ❌ **Fiducial / Coin / Card Detection:** Reference standard detection is strictly owned by Member 2.
- ❌ **Perspective Rectification / Homography:** Homography matrix $H$ is computed and applied by Member 2.
- ❌ **Principal Display Panel (PDP) Area:** Area calculations ($A_{\text{PDP}}$ in $\text{cm}^2$) belong to Member 2.
- ❌ **Font Legality Evaluation:** Verifying whether numeral height satisfies Table-I of Rule 7 is strictly owned by Member 3.

---

## 4. Consumption Interface for Member 2

Member 2 can consume Member 1's output via either `OCRResult` or canonical `OCRObservation`:

```python
from nirikshak_ocr import OCREngine

engine = OCREngine()
result = engine.extract(image_bgr)

# Iterate through raw tokens for dimensional scaling:
for token in result.tokens:
    # 1. Access 4-point quadrilateral for homography remapping:
    poly_pts = token.polygon  # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    
    # 2. Access raw pixel height:
    h_px = token.raw_pixel_height
    
    # 3. Member 2 applies scale factor S (mm/px) recovered from calibration target:
    # H_mm = h_px * scale_factor_mm_per_px
```
