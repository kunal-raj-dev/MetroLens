# Inter-Member Handoff: Member 1 (OCR) to Member 5 (Frontend Canvas) — Chunk 4
**Document:** `AI_CONTEXT/HANDOFFS/M1_TO_M5_CHUNK4.md`  
**From:** Member 1 (AI & Multilingual OCR Lead)  
**To:** Member 5 (Frontend, Inspector UX & Verification Canvas Lead)  
**Date:** 2026-09-05T05:35:00+05:30  
**Phase:** Chunk 4 Delivery  
**Status:** READY FOR FRONTEND VERIFICATION CANVAS CONSUMPTION  

---

## 1. Handoff Summary
Member 1 has verified that `OCRService` outputs tokens and observations strictly aligned with frontend rendering requirements for interactive visual verification.

---

## 2. Data Contract for Frontend Rendering

Each extracted observation delivered in the API response adheres to the `OCRObservation` schema:
```json
{
  "text": "MRP Rs. 250.00 (Incl. of all taxes)",
  "confidence": 0.942,
  "bounding_box": [
    [120.0, 340.0],
    [580.0, 340.0],
    [580.0, 385.0],
    [120.0, 385.0]
  ]
}
```

### 2.1 Coordinate Space Guarantees
- **Un-normalized Pixel Space:** Coordinates `[x, y]` are expressed in absolute pixel dimensions matching the **original uploaded image** ($W \times H$).
- **Polygon Ordering:** Vertices are strictly ordered **clockwise** starting from the top-left vertex:
  - Vertex 0: Top-Left `[x_tl, y_tl]`
  - Vertex 1: Top-Right `[x_tr, y_tr]`
  - Vertex 2: Bottom-Right `[x_br, y_br]`
  - Vertex 3: Bottom-Left `[x_bl, y_bl]`
- **Rotated Text:** For angled text lines, the 4-point quadrilateral accurately follows the text orientation. Canvas rendering should draw an SVG `<polygon points="..."/>` or HTML5 canvas path rather than an axis-aligned bounding box.

### 2.2 Confidence & Styling Recommendations
- `confidence >= 0.85`: High confidence (render green outline `#10b981`).
- `0.60 <= confidence < 0.85`: Moderate confidence (render yellow/amber outline `#f59e0b`).
- `confidence < 0.60`: Low confidence requiring human verification (render red outline `#ef4444` with alert badge).

### 2.3 Unicode & Multilingual Rendering
- Text strings contain verbatim UTF-8 characters including Devanagari script (`अ-ह`, conjuncts) and the Indian Rupee symbol (`₹`). Ensure frontend canvas fonts include Noto Sans Devanagari or equivalent fallbacks to prevent font-rendering squares (`□`).
