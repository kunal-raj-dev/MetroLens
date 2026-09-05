# MEMBER 5: RE-ARCHITECTED 7-CHUNK WORK PLAN
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering & Web UX Lead  
**Document Version:** 2.0.0 (Post-Audit Re-Architected Edition)  
**Target Package:** `apps/web/`  

---

## 1. Architectural Strategy & Phasing Rationales

The original 9-day plan in `docs/team/MEMBER_5_WORK_PLAN.md` was directionally sound in identifying user journeys (`Upload -> Inspection -> Compliance -> Evidence -> Declarations -> Review -> Report`), but suffered from 8 boundary defects and assumed an uncoordinated timeline.

With **Member 1 (OCR) permanently frozen and certified**, and **Members 2, 3, and 4 actively developing**, Member 5 executes independently without blocking by using an **Adapter-based Inspection Client** architecture and realistic synthetic packaging fixtures.

```text
M5-0: Repository & Contract Audit
  │
  ▼
M5-1: Frontend Foundation & Design System
  │
  ▼
M5-2: Upload Zone & Inspection Client (Mock + Live Adapters)
  │
  ▼
M5-3: Results Dashboard & Evidence Canvas (Image-Space Transform)
  │
  ▼
M5-4: Declarations Table & Inspector Review (2-Point Caliper Dispatch)
  │
  ▼
M5-5: Live API Integration, Real-Asset Demo Failover & PDF Report
  │
  ▼
M5-6: QA, Accessibility, Responsive Viewports & MVP Freeze
```

---

## 2. Chunk-by-Chunk Detailed Specifications

### Chunk M5-0: Repository & Contract Audit
- **Status:** **COMPLETE**
- **Objective:** Establish the ground truth of the repository before writing UI components.
- **Audited Realities:**
  1. Framework is Next.js 14 App Router (`apps/web/package.json`), not Vite SPA.
  2. Tailwind CSS and PostCSS are listed as dependencies but lack configuration files and `globals.css`.
  3. `apps/api/main.py` has an active `POST /api/v1/inspect` endpoint that consumes `multipart/form-data` with a strict 15MB ceiling and magic bytes check.
  4. Backend returns `InspectionResult` (`nirikshak_shared.models.contracts`), which differs in field organization from the provisional `docs/API_CONTRACT.md`.
  5. Member 1 outputs unnormalized original image pixel coordinates in `OCRToken.polygon` (`[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]`) and `OCRToken.bbox` (`[xmin, ymin, xmax, ymax]`).
  6. `data/synthetic/regression/` provides 8 real packaging image assets (`SYNTH-01` to `SYNTH-08`) with complete ground truth metadata.

---

### Chunk M5-1: Frontend Foundation & Design System
- **Objective:** Create the stable visual foundation, styling tokens, and reusable UI primitives.
- **Scope & Files to Create/Configure:**
  - `apps/web/postcss.config.js`
  - `apps/web/tailwind.config.ts`
  - `apps/web/src/app/globals.css` (defining dark theme, accessible slate palette, high-contrast status tokens)
  - `apps/web/src/components/ui/`
    - `Button.tsx` (primary, secondary, danger, outline, ghost)
    - `Card.tsx` (header, content, footer, border styling)
    - `Badge.tsx` (semantic status badges with icons)
    - `Dialog.tsx` (accessible modal primitive with focus trap)
    - `Tooltip.tsx` (for OCR token annotations)
    - `Skeleton.tsx` (loading state pulse animations)
  - Initial layout update in `apps/web/src/app/layout.tsx` and `page.tsx`
- **Design Tokens:**
  - Background: `slate-950` / `slate-900`
  - Cards: `slate-900/60` border `slate-800`
  - Compliant: `emerald-400` / `emerald-950/80`
  - Non-Compliant: `rose-400` / `rose-950/80`
  - Manual Review: `amber-400` / `amber-950/80`
  - Exemption: `sky-400` / `sky-950/80`
  - Inconclusive: `slate-400` / `slate-800`
- **Verification Gate:** `apps/web` builds and runs cleanly; shows officer workstation layout, clean typography, and UI primitive catalog.

---

### Chunk M5-2: Image Upload Zone & Inspection Client
- **Objective:** Ingest packaging images safely, provide visual feedback, and establish the decoupled client interface.
- **Scope & Files to Create:**
  - `apps/web/src/components/ImageUploadZone.tsx`
  - `apps/web/src/types/inspection.ts` (defining `FrontendInspectionModel`)
  - `apps/web/src/services/inspectionClient.ts` (facade)
  - `apps/web/src/services/adapters/mockAdapter.ts`
  - `apps/web/src/services/adapters/liveApiAdapter.ts`
  - `apps/web/src/mocks/fixtures.ts` (populated with realistic `InspectionResult` payloads)
- **Validation Rules:**
  - Max size: `15 * 1024 * 1024` bytes (15.0 MB)
  - File types: `image/jpeg`, `image/png`, `image/webp`
  - Image decoding verification in browser prior to submission
  - Visual states: idle, drag-over, file selected with preview thumbnail, uploading with progress animation, error toast
- **Verification Gate:** A user can drop an image, see the thumbnail with file size and dimension metadata, clear/replace image, and trigger inspection against `MockInspectionAdapter`.

---

### Chunk M5-3: Results Dashboard & Evidence Canvas
- **Objective:** Present the macro statutory verdict and provide an interactive, pixel-accurate visual evidence viewer.
- **Scope & Files to Create:**
  - `apps/web/src/components/ComplianceDashboard.tsx`
  - `apps/web/src/components/EvidenceCanvas.tsx`
  - `apps/web/src/utils/canvasTransform.ts`
- **Dashboard Requirements:**
  - Multi-modal status banner: Color + Icon + Label + Plain English Summary + Telemetry timing chips.
  - Sub-cards for Quality Gate status (`Laplacian variance`, `glare ratio`), Calibration state (`Calibrated` vs `Uncalibrated`), and Stage latencies.
- **Canvas Requirements:**
  - HTML5 `<canvas>` rendering original image without loss of fidelity.
  - Coordinate system: Unnormalized input image pixel coordinates from M1.
  - Affine transformation: Scale and translation matrix handling fit-to-screen, mouse wheel / pinch zoom, pan by dragging.
  - High-DPI handling via `window.devicePixelRatio`.
  - Color-coded bounding box and polygon rendering (Green = compliant declaration, Red = non-compliant/deficit, Amber = review needed).
  - Hover tooltip displaying token text, confidence score, and script type.
- **Verification Gate:** Bounding boxes remain locked to underlying package text across browser resize, DPI changes, and full pan/zoom interaction.

---

### Chunk M5-4: Declaration Table & Inspector Review
- **Objective:** Deliver line-item statutory evidence breakdown and empower the inspecting officer with review controls and caliper override.
- **Scope & Files to Create:**
  - `apps/web/src/components/DeclarationTable.tsx`
  - `apps/web/src/components/InspectorReviewModal.tsx`
  - `apps/web/src/components/CaliperTool.tsx`
- **Declaration Table Features:**
  - Side-by-side list: MRP, Net Quantity, Unit Sale Price (USP), Mfg Date, Manufacturer Details, Consumer Care.
  - Displays detected text, normalized value, measured height (mm), statutory requirement, and verdict badge.
  - **Cross-Component Sync:** Clicking any declaration row smooth-zooms the `EvidenceCanvas` directly onto that declaration's bounding box.
- **Inspector Review Modal Features:**
  - Zoomed evidence crop viewer with SHA-256 parent image fingerprint.
  - 1-tap officer confirmation or dispute toggle with written justification notes.
  - **2-Point Caliper Tool:** Officer clicks two points on canvas (e.g. coin diameter). UI computes Euclidean pixel distance $d_{\text{px}}$ and dispatches `manualScaleOverride` to backend. React does **not** recalculate legal font millimeter heights.
- **Verification Gate:** Officer can inspect individual declaration evidence, review crops, and trigger caliper override dispatch.

---

### Chunk M5-5: Live Backend, Real Demo Samples & PDF
- **Objective:** Connect the live FastAPI backend, embed genuine pre-loaded sample packages, and wire PDF dossier downloads.
- **Scope & Files to Create:**
  - `apps/web/src/components/SamplePackageSelector.tsx`
  - `apps/web/src/services/adapters/responseNormalizer.ts`
  - Wire `LiveApiAdapter` to `http://127.0.0.1:8000/api/v1/inspect`.
  - Wire "Download Assessment Report" button to `/api/v1/report/pdf`.
- **Sample Package Selector Features:**
  - Quick-switch selector loaded with real synthetic package images from `data/synthetic/regression/` (`SYNTH-01` to `SYNTH-08`).
  - Selecting a package retrieves the real image asset and feeds it directly into `InspectionClient.inspect()`.
  - Ensures live presentation demo runs identically whether using live file upload or sample selector.
- **PDF Report Handling:**
  - Triggers report download.
  - If Member 4 reporting endpoint is in progress, renders an informative "Dossier Generator In Staging" status modal rather than breaking or faking data.
- **Verification Gate:** System executes live inspection end-to-end against local FastAPI backend and completes sample inspection within $<2.5\text{s}$.

---

### Chunk M5-6: Final QA, Accessibility, Responsive Polish & Freeze
- **Objective:** Comprehensive testing, accessibility audit, multi-device verification, and official MVP freeze.
- **Scope:**
  - **Cross-Browser:** Chrome, Firefox, Edge, Mobile Chrome.
  - **Responsive Matrix:** $1920 \times 1080$ (projector), $1440 \times 900$, $1280 \times 720$, $1024 \times 768$ (tablet), $390 \times 844$ (mobile).
  - **Accessibility (a11y):** WCAG 2.1 AA color contrast, full keyboard navigation (`Tab`, `Enter`, `Escape`), ARIA roles and labels, screen-reader readable status announcements.
  - **Hostile Error Handling:** Server 500, network drop, timeout, corrupted file, 0-declaration image.
- **Deliverable:** `docs/audit/MEMBER_5_FINAL_STATUS.md` certifying **M5 RELEASE CANDIDATE — PERMANENTLY FROZEN FOR MVP**.

---

## 3. Strict Microstep Execution Rhythm
Each chunk follows this inviolable engineering loop:

$$\text{PLAN} \longrightarrow \text{IMPLEMENT} \longrightarrow \text{RUN APP} \longrightarrow \text{TEST} \longrightarrow \text{BROWSER VERIFY} \longrightarrow \text{DOCUMENT} \longrightarrow \text{CHECKPOINT}$$

No commits or branches are touched without explicit authorization.
