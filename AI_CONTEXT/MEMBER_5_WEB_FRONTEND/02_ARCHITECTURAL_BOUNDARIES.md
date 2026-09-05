# MEMBER 5: ARCHITECTURAL BOUNDARIES & THE 8 CORRECTIONS
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering & Web UX Lead  
**Document Status:** Authoritative Seam Specification  

---

## 1. Overview & Architectural Motivation
To prevent frontend scope creep and preserve separation of concerns across the 6-member team, Member 5 operates within strictly defined architectural boundaries.

Below are the **8 core corrections** made to the original Member 5 plan, along with their mathematical and architectural justifications.

---

## 2. The 8 Core Boundary Corrections

### Correction 1: Member 5 Must Not Independently Define Legal States
- **Original Defect:** The plan implied that the frontend would determine whether a package is compliant or calculate whether a declaration violates the law.
- **Correction:** The legal and semantic meaning of compliance is owned **strictly by Member 3 (Rule Engine)** and returned by the backend. The frontend is a faithful visual representation layer.
- **Architectural Flow:**
  ```text
  Member 3 Rule Engine (Pydantic / Gazette Logic)
             │
             ▼
  FastAPI InspectionResult DTO
             │
             ▼
  Member 5 Visual Representation Layer (Dashboard & Badges)
  ```

---

### Correction 2: Manual Caliper Logic Boundary
- **Original Defect:** The plan stated that the frontend would click two points on canvas and "recalculate font heights dynamically."
- **Correction:** Frontend owns **interaction**, not physical measurement mathematics. Calculating scale factor ($S$) from reference objects (coins/cards) and converting pixel heights to physical millimeters belongs to **Member 2 (Calibration & Metrology)**.
- **Correct Interaction Flow:**
  ```text
  Inspector clicks Point A (x1, y1) and Point B (x2, y2) on Canvas
             │
             ▼
  Frontend computes Euclidean pixel distance: d_px = sqrt((x2 - x1)^2 + (y2 - y1)^2)
             │
             ▼
  Frontend dispatches manualScaleOverride payload to backend:
  {
    "inspection_id": "...",
    "pixel_distance": d_px,
    "reference_target": "INR_10_COIN",
    "known_dimension_mm": 27.0
  }
             │
             ▼
  Member 2 re-computes scale factor S (mm/px)
             │
             ▼
  Member 3 re-evaluates Rule 7 font heights
             │
             ▼
  Updated InspectionResult returned to Frontend
  ```

---

### Correction 3: Member 5 Must Not Modify API Contract
- **Original Defect:** Frontend developers often "fix" schema mismatches by inventing new response structures or forcing backend modifications.
- **Correction:** The API contract is governed by shared schemas (`packages/shared`). Frontend adapts to the approved contract via a dedicated client adapter. Any required contract evolution must be coordinated through shared schema channels with Member 4.

---

### Correction 4: Adapter-Based Inspection Client Layer
- **Original Defect:** Component code directly calling `fetch()` or `axios()` with hardcoded mock switches.
- **Correction:** Implement a clean abstraction:
  ```text
                   React UI Components
                           │
                           ▼
                   InspectionClient
                    ├── MockInspectionAdapter
                    └── LiveApiInspectionAdapter
                           │
                           ▼
                 FrontendInspectionModel
  ```
  The UI components consume a normalized `FrontendInspectionModel` and remain completely unaware of whether data originates from local mocks or a live FastAPI instance.

---

### Correction 5: Sample Failover Uses Real Local Assets, Not Canned JSON
- **Original Defect:** The original fallback proposal was to "hardcode canned responses" for the demo selector.
- **Correction:** Canned JSON creates fake demos that degrade under scrutiny. Instead:
  ```text
  User selects "SYNTH-01 English FMCG" from dropdown
             │
             ▼
  App loads local image blob from data/synthetic/regression/
             │
             ▼
  Passes real image through standard InspectionClient.inspect()
             │
             ▼
  Executes same inspection pipeline & identical UI rendering
  ```
  Even in offline demo failover, the system executes real visual workflows with zero fake rendering paths.

---

### Correction 6: Canvas Coordinate Strategy Aligned with Member 1
- **Original Defect:** Proposal to normalize OCR coordinates into $0.0\text{--}1.0$ percentages, risking rounding errors and coordinate drift.
- **Correction:** Member 1’s finalized contract provides **unnormalized original input image pixel coordinates**. The frontend preserves these exact coordinates and renders them via an affine transform matrix:
  ```text
  IMAGE SPACE (Original image pixels: w x h)
             │
             ▼ (fit-to-screen scale & pan offset)
  CANVAS SPACE (HTML5 Canvas display pixels)
             │
             ▼ (* window.devicePixelRatio)
  SCREEN SPACE (Physical monitor / projector pixels)
  ```
  The underlying OCR coordinates remain unaltered throughout the application lifecycle.

---

### Correction 7: 15 MB Ceiling Aligned with Backend Policy
- **Original Defect:** Treating 15MB as an arbitrary frontend validation rule.
- **Correction:** The frontend directly mirrors the backend limit established in `apps/api/main.py` (`MAX_FILE_SIZE = 15 * 1024 * 1024` bytes) and validates magic byte formats (`JPEG`, `PNG`, `WebP`) before transmission.

---

### Correction 8: Multi-Modal Status Communication
- **Original Defect:** Excessive reliance on color alone (Green/Red/Amber/Blue/Gray).
- **Correction:** For accessibility (WCAG 2.1 AA) and readability on washed-out auditorium projectors, every statutory state must convey information through four simultaneous signals:
  $$\text{Color Accent} + \text{Unique Lucide Icon} + \text{Text Status Label} + \text{Plain-Language Explanation}$$
  Example:
  - **Color:** Rose (`#f43f5e`)
  - **Icon:** `AlertTriangle`
  - **Label:** `POTENTIAL_NON_COMPLIANCE`
  - **Explanation:** *"Rule 6(11) Unit Sale Price arithmetic discrepancy detected: declared ₹1.20/gm exceeds statutory standard ₹0.31/g."*
