# M1 FINAL AUDITED HANDOFF TO MEMBER 5 (UI/UX & FRONTEND CANVAS)

**From**: Member 1 (AI & Multilingual OCR Lead)  
**To**: Member 5 (Frontend Engineering & Interactive Canvas Lead)  
**Date**: 2026-09-05  
**Freeze Status**: AUDITED & FROZEN  

---

## 1. Frontend Data Payload: `tokens`
Member 5's React Canvas and inspection UI consume the `tokens` array emitted by `OCRService.extract_dict()` or FastAPI `/api/v1/inspect`:

```json
{
  "token_id": "tok_001",
  "text": "MRP Rs. 250.00",
  "confidence": 0.985,
  "polygon": [
    [120.0, 45.0],
    [310.0, 45.0],
    [310.0, 75.0],
    [120.0, 75.0]
  ],
  "bbox": [120.0, 45.0, 310.0, 75.0],
  "script": "latin",
  "line_id": 0,
  "raw_pixel_height": 30.0,
  "model_name": "SVTR-EN"
}
```

## 2. Canvas Coordinate System & Rendering Rules
- **Coordinate Space**: Unnormalized pixel coordinates matching the native resolution of the uploaded image (`image_width` x `image_height`).
- **Origin**: Top-left corner `(0, 0)`.
- **Polygon Points**: 4 vertices ordered clockwise:
  1. `polygon[0]`: Top-Left `[x, y]`
  2. `polygon[1]`: Top-Right `[x, y]`
  3. `polygon[2]`: Bottom-Right `[x, y]`
  4. `polygon[3]`: Bottom-Left `[x, y]`
- **Derived Bounding Box**: `[xmin, ymin, xmax, ymax]`.
- **Canvas Scaling**: If the React Canvas scales down the image for display (e.g. from 1920x1080 down to 800x450 in the browser viewport), scale all polygon coordinates by the exact viewport scale factor `(viewport_width / image_width)` and `(viewport_height / image_height)`.

## 3. UI Status & Visual Warnings
- **Status Field**: `status == "SUCCESS"` even when 0 tokens are detected (e.g. blank package frame). Display an informational banner ("No text detected on selected panel") rather than an error modal.
- **Diagnostic Warnings**: If `confidence < 0.60`, M1 includes diagnostic messages in `warnings`. The UI can render amber bounding box outlines to prompt officer verification.
- **Script Badge**: `script` attribute (`"latin"`, `"devanagari"`, or `"unknown"`) can be displayed as a chip tag next to the transcribed text.
