# Inter-Member Final Handoff: Member 1 (OCR) -> Member 5 (Frontend & UX)

**From**: Member 1 — AI & Multilingual OCR Lead  
**To**: Member 5 — Frontend & User Experience Lead  
**Date**: September 2026  
**Status**: **FROZEN & PRODUCTION READY**

---

## 1. Executive Summary & UI Data Contract

Member 1 provides JSON-serializable optical detection structures optimized for rendering interactive bounding box overlays and text inspection sidebars in the MetroLens frontend application.

### JSON Schema Emitted by OCR Endpoint:
```json
{
  "image_id": "packaging_sample_01.jpg",
  "status": "SUCCESS",
  "token_count": 6,
  "tokens": [
    {
      "token_id": "tok_0",
      "text": "MRP Rs. 150.00",
      "confidence": 0.942,
      "language_script": "latin",
      "polygon": [[50.0, 120.0], [300.0, 120.0], [300.0, 160.0], [50.0, 160.0]],
      "bounding_box": [50.0, 120.0, 300.0, 160.0]
    },
    {
      "token_id": "tok_1",
      "text": "शुद्ध मात्रा: 500 ग्राम",
      "confidence": 0.915,
      "language_script": "devanagari",
      "polygon": [[50.0, 180.0], [350.0, 180.0], [350.0, 220.0], [50.0, 220.0]],
      "bounding_box": [50.0, 180.0, 350.0, 220.0]
    }
  ],
  "latency_ms": 139.18
}
```

---

## 2. Frontend Rendering Guidelines for Member 5

1. **Polygon Canvas / SVG Overlay**:
   - Render polygon contours using SVG `<polygon points="x1,y1 x2,y2 x3,y3 x4,y4" />` overlaid on top of the packaging image.
   - Scale factor formula: $S = \text{ClientImageWidth} / \text{OriginalImageWidth}$.
2. **Confidence Color Coding**:
   - **High Confidence ($\ge 0.85$)**: Green border (`#10B981`)
   - **Moderate Confidence ($0.60 \le C < 0.85$)**: Amber/Yellow border (`#F59E0B`)
   - **Low Confidence ($< 0.60$)**: Red border (`#EF4444`) with manual edit affordance
3. **Unicode & Font Typography**:
   - Ensure frontend typography bundles support Devanagari Unicode codepoints (Noto Sans Devanagari or Hind) and the Indian Rupee symbol (`₹`, U+20B9).

---

## 3. Strict Boundary Rules for Member 5

1. **Member 5 Owns**:
   - Web application layout, visual inspector, interactive polygon overlays, inspector sidebars, and responsive mobile/desktop UI.
2. **Member 5 Must NOT**:
   - Attempt client-side OCR in WebAssembly or browser canvas.
   - Modify or rebuild any code in `packages/ocr/` (permanently frozen per `MEMBER_1_DO_NOT_REBUILD.md`).
