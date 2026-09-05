# INTER-MEMBER HANDOFF SPECIFICATION: M1 ──► M5
### Optical Character Recognition (M1) to Frontend Verification Canvas (M5)
**Document:** `AI_CONTEXT/HANDOFFS/M1_TO_M5_CHUNK2.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 5 (Frontend Architecture, Inspector UX & Canvas Lead)  
**Status:** FROZEN CONTRACT (Chunk 2 Complete)  
**Timestamp:** 2026-09-05T04:33:00+05:30  

---

## 1. Executive Contract Summary
Member 5 builds the interactive inspection verification canvas (HTML5 Canvas / SVG overlay / React) where human Legal Metrology Officers inspect detected packaging declarations.

This document defines the exact geometric coordinates, bounding box envelopes, and token metadata emitted by Member 1 for frontend rendering without requiring Member 5 to understand machine learning or ONNX internals.

---

## 2. Coordinate System Specification

```text
(0, 0) Top-Left ────────────────────────────────► +X (Width in original pixels)
  │
  │     [x1, y1] (Top-Left) ─────────── [x2, y2] (Top-Right)
  │           │                               │
  │           │      Detected Text Line       │
  │           │                               │
  │     [x4, y4] (Bottom-Left) ──────── [x3, y3] (Bottom-Right)
  ▼
 +Y (Height in original pixels)
```

1. **Pixel Space:** All coordinates refer strictly to the **original uploaded image pixel dimensions** (`image_width` $\times$ `image_height`).
2. **Origin:** Top-left corner `(0.0, 0.0)`.
3. **Polygon Format (`polygon`):**
   - 4-point quadrilateral array: `[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]`.
   - **Order:** Clockwise: `[top-left, top-right, bottom-right, bottom-left]`.
   - Use `polygon` for drawing oriented polygon bounding overlays or tilted highlight boxes.
4. **Bounding Box (`bbox`):**
   - Axis-aligned rectangular envelope: `[xmin, ymin, xmax, ymax]`.
   - `width = xmax - xmin`
   - `height = ymax - ymin`
   - Use `bbox` for simple rectangular canvas highlights or CSS absolute positioning.

---

## 3. Token Metadata for UI Visualization

Each token in `result.tokens` provides rich metadata for inspector interactions:

```typescript
// Frontend TypeScript interface matching Member 1's OCRToken
interface OCRToken {
  token_id: string;             // e.g. "tok_001" (use as unique React key)
  text: string;                 // Transcribed string (e.g. "MRP Rs. 20")
  confidence: number;           // 0.0 to 1.0 (Render green >= 0.80, yellow 0.60-0.79, red < 0.60)
  polygon: [number, number][];  // 4 vertices [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
  bbox: [number, number, number, number]; // [xmin, ymin, xmax, ymax]
  script: "latin" | "devanagari" | "unknown"; // Display badge (e.g. "EN" or "HI")
  line_id: number;              // Reading order sequence index
  raw_pixel_height: number;     // Quad height in pixels (NOT legal font height in mm)
  model_name: string;           // "SVTR-EN" or "SVTR-HI" (Provenance tooltip)
}
```

---

## 4. UI Rendering Guidelines for Member 5

1. **Canvas Zoom & Scale:**
   Because all coordinates are in original image pixels, when scaling the image on the responsive canvas:
   $$\text{scale\_x} = \frac{\text{canvas\_rendered\_width}}{\text{image\_width}}, \quad \text{scale\_y} = \frac{\text{canvas\_rendered\_height}}{\text{image\_height}}$$
   Multiply all vertex coordinates by $(\text{scale\_x}, \text{scale\_y})$.
2. **Confidence Color Coding:**
   - $\text{confidence} \ge 0.80$: Green highlight (High confidence OCR).
   - $0.60 \le \text{confidence} < 0.80$: Amber highlight (Satisfactory).
   - $\text{confidence} < 0.60$: Red / Striped highlight with warning tooltip (`"Review Required: Low OCR Confidence"`).
3. **Inspector Manual Edit / Override:**
   Provide an inline editable text input bound to `token.text` so the inspecting officer can correct any character errors (e.g., in dot-matrix dates) before clicking "Confirm & Generate Notice".
