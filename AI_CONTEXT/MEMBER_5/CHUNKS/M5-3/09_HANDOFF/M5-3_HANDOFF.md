# CHUNK M5-3 HANDOFF SPECIFICATION

**Subsystem:** Member 5 — Web Frontend & User Experience  
**Chunk:** M5-3: Compliance Dashboard + Evidence Canvas + Evidence Interaction  
**Timestamp:** 2026-09-05T18:25:00+05:30  
**Target Recipient:** Chunk M5-4 (Declarations Table + Inspector Review Modal / 2-Point Caliper Override Dispatch)  
**Status:** **100% COMPLETE & FROZEN**  

---

## 1. Executive Summary & Accomplishments

Chunk M5-3 establishes the visual evidence and compliance observation foundation for the MetroLens AI™ Inspector Workstation. It connects Member 1's frozen multilingual OCR engine with interactive canvas graphics and a multi-modal statutory compliance dashboard.

All display transformations are strictly affine and executed at render-time, preserving the exact original image pixel space without distortion, rounding error, or premature legal adjudication.

---

## 2. Frozen Interfaces & Data Contracts

### 2.1 OCR Token Contract (`src/types/frontend.ts`)
```typescript
export interface OCRTokenModel {
  id: string;
  text: string;
  confidence: number;
  /**
   * 4-point polygon in ORIGINAL INPUT IMAGE PIXEL COORDINATES:
   * [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]
   * Order: [top-left, top-right, bottom-right, bottom-left]
   * Coordinate space: [0, imageWidth] x [0, imageHeight]
   * INVARIANT: Never normalize to permanent [0, 1] floats.
   */
  polygon: [number, number][];
  bbox: [number, number, number, number]; // [ymin, xmin, ymax, xmax] in original pixels
  script?: 'latin' | 'devanagari' | 'bilingual' | 'unknown';
  associatedField?: string;
  isSuspect?: boolean;
}
```

### 2.2 Transform Engine Contract (`src/features/inspection/canvasTransform.ts`)
The pure transform engine provides the following frozen mathematical primitives:
- `imageToCanvas(pt, transform): [number, number]` — Forward affine mapping ($s \cdot [x, y] + [p_x, p_y]$)
- `canvasToImage(pt, transform): [number, number]` — Inverted affine mapping ($([x, y] - [p_x, p_y]) / s$)
- `fitToScreen(imgW, imgH, canvasW, canvasH, padding): CanvasTransform` — Preserves aspect ratio with symmetric letterboxing
- `zoomAt(transform, focalPt, zoomFactor, minZoom, maxZoom): CanvasTransform` — Cursor-anchored focal zoom
- `pointInPolygon(point, polygon): boolean` — Ray-casting hit-testing in original image pixel space
- `pointInBBox(point, bbox): boolean` — Axis-aligned bounding box pre-filter

---

## 3. Implemented Components Ready for Chunk M5-4

1. **`ComplianceDashboard.tsx` (`src/features/inspection/ComplianceDashboard.tsx`)**:
   - 4-State statutory verdict banner (`COMPLIANT`, `NON_COMPLIANT`, `SUSPECT_REVIEW`, `INCONCLUSIVE`).
   - Synthetic disclosure warning banner for demo/regression fixtures (`SYNTH-01` to `SYNTH-08`).
   - Quality gate metrics (Sharpness $>50.0$, Calibration factor in mm/px, Pipeline latency in ms).
   - Interactive selected token callout with verbatim text, confidence, script badge, and declaration linkage.

2. **`EvidenceCanvas.tsx` (`src/features/inspection/EvidenceCanvas.tsx`)**:
   - High-DPI HTML5 canvas handling `devicePixelRatio` ($2\times$, $3\times$).
   - Cursor-anchored wheel zooming with non-passive event listeners (0 page scroll).
   - Drag-to-pan with boundary clamping.
   - Click-to-select with inverse ray-casting point-in-polygon algorithm.
   - Hover tooltips showing token ID, text, confidence, and mapped field.
   - Synchronized accessible listbox (`role="listbox"`, `role="option"`, `aria-selected`).

3. **`page.tsx` (`src/app/page.tsx`)**:
   - Master workstation state orchestrator connecting upload zone, canvas, dashboard, and declaration table.
   - Synchronized `selectedTokenId` state across all components.

---

## 4. Test Evidence & Quality Floor

- **Total Unit & Regression Tests:** 60/60 Passed (100%)
  - `apps/web/src/__tests__/canvas_transform.test.ts`: 20/20 Passed (Round-trip error $< 10^{-5}$)
  - `apps/web/src/__tests__/m5_2_verification.test.ts`: 34/34 Passed
  - `apps/web/src/__tests__/m5_3_integration.test.ts`: 6/6 Passed (Member 1 pixel coordinate invariance, Devanagari Unicode, client non-adjudication)
- **Next.js Production Build:** Exit Code 0 (`npm run build` completed cleanly, 4/4 static pages generated)
- **Browser Runtime Audit:** Verified with Chrome DevTools at $1920 \times 1080$, $1280 \times 720$, and $390 \times 844$. 0 console errors, 0 hydration warnings.

---

## 5. Handoff Directives for Chunk M5-4

1. **Declarations Table Enhancement**:
   - Connect the declaration table rows to `selectedTokenId`. Clicking a row must highlight the associated OCR polygon in `EvidenceCanvas` and center/zoom if appropriate.
   - Clicking an OCR polygon in `EvidenceCanvas` must highlight the corresponding declaration row in `DeclarationTable`.

2. **Inspector Review Modal (2-Point Caliper Override)**:
   - When an officer triggers manual review/override on a declaration, open the `InspectorReviewModal`.
   - Implement the 2-point digital caliper tool allowing the officer to mark the top and bottom of a character glyph on the canvas.
   - The caliper distance in pixels is multiplied by the backend-provided calibration factor ($mm/px$) to calculate the manual height $h_{\text{override\_mm}}$.
   - Dispatch the override payload (`override_height_mm`, `officer_notes`, `timestamp`) back to the parent state.

3. **Inviolate Invariants to Maintain**:
   - Never modify Member 1's OCR coordinates into percentages or viewport-relative values.
   - Never perform legal rule adjudication (Rule 6/7 verdicts) in the client; all legal conclusions remain backend-driven.
   - Never suppress synthetic disclosures when displaying synthetic regression assets.
   - Never execute git mutating commands.
