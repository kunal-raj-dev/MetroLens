# METROLENS AI — MEMBER 5 (CHUNK M5-4)
## Implementation Architecture & Code Structure

### 1. Component Architecture & File Map

```
apps/web/src/
├── types/
│   └── frontend.ts                     # Added CaliperPoint, ReviewDecision, ReviewSubmissionInput, ReviewSubmissionResult, DeclarationModel enhancements
├── services/
│   ├── client.ts                       # IInspectionClient interface with submitReview()
│   ├── errors.ts                       # Added REVIEW_API_NOT_IMPLEMENTED error code
│   └── adapters/
│       ├── mockAdapter.ts              # submitReview() implementation with synthetic audit persistence
│       ├── liveApiAdapter.ts          # submitReview() implementation with graceful API pending detection
│       └── responseNormalizer.ts      # imagePath mapping and enhanced declaration fields
├── features/inspection/
│   ├── DeclarationTable.tsx            # Responsive statutory declaration matrix (table & mobile cards)
│   ├── InspectorReviewModal.tsx        # Officer adjudication modal with 4 core inspection questions
│   ├── EvidenceCanvas.tsx              # Canvas with highlightedTokenIds, focusTokensUnion, & Manual Caliper Tool
│   ├── canvasTransform.ts              # Inverse coordinate mapping (canvasToImage)
│   └── index.ts                        # Re-exports DeclarationTable and InspectorReviewModal
└── app/
    └── page.tsx                        # Workstation integration with review handling & caliper state
```

### 2. Evidence Linking & Multi-Token Union
When an officer clicks "Canvas" on any declaration row in `DeclarationTable`:
1. The declaration's `sourceTokenIds` are extracted.
2. The primary token is selected via `onSelectToken(tokenIds[0])`.
3. All linked tokens are highlighted via `highlightedTokenIds` with a distinctive Royal Blue outline (`#2563EB`) and fill.
4. If multiple tokens belong to the declaration, `focusTokensUnion` computes the minimal bounding box containing all tokens and smoothly animates the viewport to fit the bounding region with 40px padding.

### 3. Manual Two-Point Reference Points (Caliper Tool)
1. **Activation**: Toggled via the Caliper button on the Evidence Canvas floating toolbar.
2. **Coordinate Mapping**: On mouse click, screen canvas coordinates `(canvasX, canvasY)` are converted to unscaled original image space via `canvasToImage(canvasPt, transform)`.
3. **Validation**:
   - Out-of-bounds clicks are clamped to image bounds `[0, width]` and `[0, height]`.
   - Clicks within 2.0 optical pixels of Point A are rejected to prevent duplicate/accidental double-clicks.
4. **Distance Computation**:
   \[
   \text{dist} = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}
   \]
   Computed strictly in optical image pixels. No physical mm conversion is performed on the frontend.
5. **Visual Rendering**:
   - Precision crosshair markers at Point A (emerald) and Point B (sky blue).
   - High-contrast dashed connecting line (`ctx.setLineDash([4, 4])`).
   - Pill tag displaying `X.X px (optical)` centered on the midpoint with a white backdrop.
