# INDIVIDUAL WORK PLAN: MEMBER 5
# Frontend & Web User Experience Lead
### Project: MetroLens AI (SIH26034) | Sponsoring Ministry: Ministry of Consumer Affairs
**Document Status:** Authoritative Personal Work Package & Accountability Contract | **Version:** 1.0.0 (Web MVP Edition)  
**Sprint Window:** 8–9 Days | **Primary Package:** `apps/web/` | **Secondary Role:** Demo Stagecraft & UI Polish

---

## 1. Member Role
**Member 5 — Frontend Engineering, Web Application & User Experience Lead**

---

## 2. Mission
Deliver an intuitive, responsive, highly polished web application that makes complex Legal Metrology compliance crystal clear to non-technical judges and regulatory officers. Member 5 is personally responsible for building the React 19 + Vite web interface, implementing a seamless drag-and-drop upload zone with client-side image validation, rendering the executive 5-State statutory compliance dashboard, developing the interactive bounding-box verification canvas with synchronized high-resolution evidence crops, providing an inspector review panel with manual 2-point caliper scale overrides, and embedding the 10-SKU pre-loaded sample package selector for fail-safe live demo execution.

---

## 3. Ownership

### Primary Ownership:
- `apps/web/`: Complete React 19 + TypeScript + Vite + Tailwind CSS Single-Page Application.
- `apps/web/src/components/ImageUploadZone.tsx`: Drag-and-drop upload dropzone with progress bar and client validation.
- `apps/web/src/components/ComplianceDashboard.tsx`: Executive 5-State status badge and summary cards.
- `apps/web/src/components/EvidenceCanvas.tsx`: Interactive image viewer rendering color-coded bounding boxes.
- `apps/web/src/components/DeclarationTable.tsx`: Side-by-side table comparing detected values with statutory minimums.
- `apps/web/src/components/InspectorReviewModal.tsx`: Inspector manual review panel with 2-point caliper scale override.
- `apps/web/src/components/SamplePackageSelector.tsx`: Persistent demo dropdown with 10 pre-loaded benchmark packages.
- `tests/unit/test_frontend_components.tsx`: Component unit tests and accessibility audits.

### Secondary Support:
- Support **Member 6 (DevOps Lead)** in staging the web application and testing mobile browser viewports.
- Support the presenter during live demo rehearsals with screen layout and font legibility for stage projection.

---

## 4. Concrete Responsibilities
1. Scaffold the web frontend using React 19, TypeScript, Vite, and Tailwind CSS; configure proxy to `http://127.0.0.1:8000`.
2. Implement client-side pre-flight validation in `ImageUploadZone.tsx`:
   - Enforce file extension whitelist (`.jpg`, `.jpeg`, `.png`, `.webp`) and $15.0\text{MB}$ size ceiling before network transmission.
   - Display animated upload progress bar and instant image thumbnail preview.
3. Construct the Executive 5-State Compliance Banner:
   - Green: `NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED` (Pass).
   - Red: `POTENTIAL_NON_COMPLIANCE` (Improvement Notice Recommended).
   - Amber: `MANUAL_REVIEW_REQUIRED` (Borderline / Non-Planar).
   - Blue: `STATUTORY_EXEMPTION_APPLIED` (Rule 26 / Wholesale).
   - Gray: `NOT_IMAGE_VERIFIABLE` (Net Weight / Scale Absent).
4. Build `EvidenceCanvas.tsx` for visual explainability:
   - Render packaging image on HTML5 canvas with normalized bounding boxes.
   - Color-code bounding boxes: Green for compliant declarations, Red for deficits/omissions, Amber for borderline.
   - Enable pan and zoom; clicking any box highlights the corresponding declaration card.
5. Build `DeclarationTable.tsx` displaying:
   - Mandatory field name, extracted text, measured height ($h_{\text{mm}}$), statutory minimum, and pass/fail status.
   - Dedicated Unit Sale Price (USP) arithmetic breakdown card displaying $\frac{\text{MRP}}{\text{NetQty}}$.
6. Implement Inspector Review & Manual Override Panel:
   - 1-tap confirmation toggle allowing an inspecting officer to verify cropped visual evidence.
   - Manual 2-point caliper tool: click two opposite edges of a coin or card on canvas to manually lock scale factor ($S$).
7. Implement Layer 2 Demo Failover:
   - "Load Sample Package" dropdown in the navbar pre-loaded with 10 pristine benchmark packaging images (5 compliant, 5 synthetic defects) that immediately trigger inspection without requiring live camera hardware.
8. Wire the frontend to the backend:
   - Use Axios / Fetch to call `POST /api/v1/inspect` via `multipart/form-data`.
   - Wire "Download Assessment Report" button to trigger `POST /api/v1/report/pdf` and download binary PDF.

---

## 5. What Member 5 Must NOT Own ("Not My Job")
- **NOT MY JOB:** Writing Python code or running OpenCV / PaddleOCR pipelines (owned by M1/M2/M4).
- **NOT MY JOB:** Codifying statutory compliance rules or USP math formulas in TypeScript (owned strictly by Member 3).
- **NOT MY JOB:** Modifying the backend API request/response contracts (governed by `docs/API_CONTRACT.md`).
- **NOT MY JOB:** Curating the physical 35-SKU benchmark dataset or measuring 1200 DPI scans (owned strictly by Member 6).
- **NOT MY JOB:** Configuring Docker multi-stage builds or CI/CD pipelines (owned strictly by Member 6).

---

## 6. Inputs Received
- **From Member 4 (Backend):** OpenAPI specification (`docs/API_CONTRACT.md`) and mock JSON responses.
- **From Member 3 (Rules):** 5-State classification definitions and statutory legal citation texts.
- **From Member 6 (QA):** 10 high-resolution demo sample packaging images for Layer 2 failover.
- **Specification:** `docs/PRODUCT_BLUEPRINT.md` (User Journey & UI Requirements).

---

## 7. Concrete Outputs Delivered
- `apps/web/`: Complete, responsive web frontend application.
- Drag-and-drop packaging upload interface.
- 5-State compliance result dashboard with side-by-side evidence crops.
- Interactive HTML5 bounding-box canvas.
- Layer 2 Demo "Load Sample Package" failover selector.
- Component test suite passing in CI.

---

## 8. Dependencies & Fallbacks

| Dependency | From Whom | Why Needed | When Needed | Fallback Strategy if Delayed |
| :--- | :--- | :--- | :--- | :--- |
| **API Contract & Mock JSON** | Member 3 / M4 | Schema definitions to build UI components | Day 1, 12:00 PM | Use mock JSON fixtures in `apps/web/src/mocks/sample_response.json`. |
| **Live FastAPI Endpoint** | Member 4 | Real HTTP upload and inspection results | Day 4, 12:00 PM | Toggle UI into `MOCK_MODE=true` to demonstrate full UI with canned JSON. |
| **10 Demo Sample Images** | Member 6 | High-res images for persistent demo dropdown | Day 5, 2:00 PM | Use 5 synthetic packaging samples from `tests/fixtures/sample_packages/`. |

---

## 9. Day-by-Day Execution Plan

### DAY 1: Risk Spike — Frontend Scaffold & Mock Data Wiring
- **Goal:** Stand up React 19 + Vite app and render 5-State result card using mock JSON.
- **Tasks:** Initialize `apps/web/` with Vite and Tailwind CSS; create TypeScript types matching `docs/API_CONTRACT.md`; build basic layout with header, dropzone placeholder, and mock result card.
- **Deliverables:** Working frontend application running on `http://localhost:5173`.
- **Expected Time:** 6 hours.
- **Dependencies:** None (develop against mock schema).
- **Checkpoint (Gate 1 - T+24h):** Frontend runs locally; renders Green/Red/Amber compliance cards from mock JSON.
- **Risk:** TypeScript compilation errors on complex Pydantic schema unions.
- **Fallback:** Use `quicktype` to automatically generate TypeScript interfaces from `docs/API_CONTRACT.md`.

### DAY 2: Packaging Image Upload Dropzone Component
- **Goal:** Deliver production-ready drag-and-drop upload zone with client validation.
- **Tasks:** Implement `ImageUploadZone.tsx`: drag-over visual feedback, file picker, file type checks (`.jpg`, `.png`, `.webp`), size check ($< 15\text{MB}$); render instant client-side thumbnail preview.
- **Deliverables:** Reusable upload component with error handling for oversized files.
- **Expected Time:** 7 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 2 - T+48h):** Upload zone accepts valid images, shows thumbnail, and rejects files $> 15\text{MB}$.
- **Risk:** Drag-and-drop event bubbling issues in modern browsers.
- **Fallback:** Ensure standard `<input type="file">` button is always prominently visible.

### DAY 3: Interactive Evidence Canvas & Bounding Box Overlays
- **Goal:** Build interactive bounding-box viewer over uploaded packaging image.
- **Tasks:** Implement `EvidenceCanvas.tsx`: render uploaded image onto HTML5 `<canvas>`; draw color-coded bounding boxes using coordinates from OCR tokens; add hover tooltips showing detected text and confidence.
- **Deliverables:** Interactive canvas with responsive coordinate scaling.
- **Expected Time:** 7 hours.
- **Dependencies:** Bounding box coordinates from mock JSON.
- **Checkpoint (Gate 3 - Day 3):** Bounding boxes scale accurately when resizing browser window.
- **Risk:** Canvas pixel scaling mismatch on high-DPI (Retina) screens.
- **Fallback:** Multiply canvas dimensions by `window.devicePixelRatio`.

### DAY 4: Live API Integration & End-to-End Upload Loop
- **Goal:** Connect React frontend to Member 4's live FastAPI backend.
- **Tasks:** Configure Axios upload client; call `POST /api/v1/inspect` with `multipart/form-data`; display animated processing spinner with stage messages; render live compliance result from API.
- **Deliverables:** Fully connected frontend-to-backend inspection loop.
- **Expected Time:** 7 hours.
- **Dependencies:** Live FastAPI backend from Member 4.
- **Checkpoint (Gate 4 - Day 4):** Dragging an image on frontend triggers live inspection and renders live cards in $< 2.5\text{s}$.
- **Risk:** CORS errors or payload serialization mismatches.
- **Fallback:** Pair directly with Member 4 to adjust FastAPI CORS middleware.

### DAY 5: Side-by-Side Crop Viewer & Statutory Declaration Cards
- **Goal:** Deliver detailed declaration breakdown and synchronized visual evidence crops.
- **Tasks:** Implement `DeclarationTable.tsx`: display MRP, Net Qty, Mfg Date, Address cards; clicking a card zooms the canvas to that declaration crop; display Unit Sale Price arithmetic breakdown card.
- **Deliverables:** Side-by-side evidence inspection dashboard.
- **Expected Time:** 6 hours.
- **Dependencies:** Crop metadata in API response.
- **Checkpoint (Gate 5 - Day 5):** Clicking "Rule 6(1)(c) Net Quantity" smoothly centers and zooms canvas onto numeral crop.
- **Risk:** Image crop coordinates out of bounds.
- **Fallback:** Clamp crop coordinates to image width/height bounds in UI helper.

### DAY 6: Inspector Review Modal & Manual Scale Override Tool
- **Goal:** Implement inspector review controls and 2-point manual caliper tool.
- **Tasks:** Build `InspectorReviewModal.tsx`: add 1-tap confirmation toggle for borderline fields; build manual 2-point caliper tool on canvas: user clicks two points on coin/card $\rightarrow$ calculates pixel distance $\rightarrow$ overrides scale factor.
- **Deliverables:** Inspector governance panel with manual calibration fallback.
- **Expected Time:** 6 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 6):** User can manually click 2 points on a coin and recalculate font heights dynamically.
- **Risk:** Manual click accuracy poor on touchscreens.
- **Fallback:** Add magnifying loupe reticle near touch point.

### DAY 7: Layer 2 Demo Dropdown, PDF Download & Responsive Polish
- **Goal:** Embed failover sample selector and wire PDF download trigger.
- **Tasks:** Build `SamplePackageSelector.tsx` in navigation bar: pre-load 10 benchmark packaging samples; clicking a sample immediately runs inspection; wire "Download Report" button to `POST /api/v1/report/pdf`.
- **Deliverables:** Fail-safe demo selector and report download integration.
- **Expected Time:** 6 hours.
- **Dependencies:** Sample images from Member 6, PDF route from Member 4.
- **Checkpoint (Gate 7):** Demo operates flawlessly using pre-loaded dropdown with zero external camera needed.
- **Risk:** PDF binary download blocked by browser popup blocker.
- **Fallback:** Trigger direct browser download using synthetic `<a download>` anchor.

### DAY 8: UI Freeze, Stagecraft Legibility & Mobile Viewport Audit
- **Goal:** Lock frontend code; optimize contrast and font sizes for auditorium projectors.
- **Tasks:** Freeze `apps/web/`; audit UI with Chrome DevTools on $1920\times1080$ projector resolution; increase status badge font sizes; test responsive layout on iPad/Android tablet viewports.
- **Deliverables:** Frozen frontend code and stage-ready presentation UI.
- **Expected Time:** 4 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 8):** Code locked; zero open UI bugs; high contrast verified for stage projection.

### DAY 9: Buffer Day & Live Demo Stagecraft Support
- **Goal:** Support presenter during live stage presentation.
- **Tasks:** Ensure demonstrator laptop browser is running in full-screen kiosk mode (`F11`); clear browser cache; stand by to trigger Layer 2 failover sample selector if camera glitches.
- **Expected Time:** As needed.

---

## 10. Checkpoints & Verification Gates

| Checkpoint | Timing | What Must Exist | How We Know It Works | What Happens if It Fails |
| :--- | :--- | :--- | :--- | :--- |
| **CP-0** | Hour 0 | Node.js v20+ & Vite installed | `npm run dev` starts dev server | Install Node dependencies |
| **CP-1** | T+24h | UI scaffold with mock JSON | Dashboard renders 5-State cards locally | Use static mock JSON file |
| **CP-2** | T+48h | Upload dropzone component works | Accepts image, validates size, shows preview | Fix HTML5 drag events |
| **CP-3** | Day 3 | Canvas renders bounding boxes | BBoxes align with text tokens | Debug coordinate scaling |
| **CP-4** | Day 4 | Live API integration complete | Upload triggers FastAPI and renders response | Pair with Member 4 on CORS |
| **CP-5** | Day 5 | Side-by-side crop viewer ready | Clicking card zooms into text crop | Fix crop boundary clamping |
| **CP-6** | Day 7 | Layer 2 failover dropdown ready | Tapping sample pack runs full audit instantly | Hardcode canned responses |
| **CP-7** | Day 8 | Final UI freeze | Zero open bugs; legible on stage projector | Lock master branch |

---

## 11. Acceptance Criteria & Test Evidence

| Deliverable | Acceptance Criteria | Test Command | Concrete Evidence |
| :--- | :--- | :--- | :--- |
| **Upload Dropzone** | Rejects files $>15\text{MB}$ with clear error message | `npm run test` (Component test) | Screencast showing red error toast on oversized file |
| **5-State Cards** | Renders appropriate color badge for each state | Visual component test | Screenshot gallery of all 5 state badges |
| **Interactive Canvas**| Bounding boxes scale accurately under resize | Manual viewport resize test | Screencast showing canvas coordinate invariance |
| **PDF Download** | Clicking download button saves valid PDF file | Browser integration test | Downloaded PDF verified in local file manager |
| **Load Time** | Initial web application load $< 1.0\text{s}$ locally | Lighthouse audit | Lighthouse Performance score $\ge 95$ |

---

## 12. Testing Responsibility
- **Component Tests:** `npm run test` (Upload dropzone, Result cards, Table rendering).
- **Accessibility Tests:** Lighthouse accessibility audit verifying WCAG 2.1 AA color contrast.
- **Cross-Browser Verification:** Test on Google Chrome, Mozilla Firefox, Apple Safari, and Mobile Chrome.
- **Failure Cases:** Network disconnection during upload (shows retry button), server 500 error (shows friendly error card instead of blank screen).

---

## 13. Handoff Protocol & Checklist

### Handoff to Member 6 (DevOps) & Presenter:
1. **Working Application:** `apps/web/` builds clean with `npm run build`.
2. **Production Bundle:** Static assets generated in `apps/web/dist/`.
3. **Usage Documentation:**
   ```bash
   cd apps/web
   npm install
   npm run dev  # Starts UI on http://localhost:5173
   ```
4. **Test Evidence:** Passing test logs and clean Lighthouse audit report.
5. **Known Limitations:** Safari requires user interaction before playing MediaStream video; manual caliper override requires mouse or stylus for sub-millimeter precision.

---

## 14. Escalation Conditions
- **Blocked for 30 minutes:** Node.js package dependency conflict $\rightarrow$ Ask Member 6 for clean `package-lock.json`.
- **Blocked for 2 hours:** Cannot parse backend API response $\rightarrow$ Escalate to Member 4 to check Pydantic serialization.
- **Blocked for half-day:** HTML5 canvas performance sluggish on large images $\rightarrow$ Downsample canvas render resolution while preserving high-res crop zooms.

---

## 15. Risk Table

| Risk | Prob | Impact | Trigger | Mitigation | Fallback |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **Camera Feed Glitches on Stage** | Med | High | Video freezes or black frame | Implement Layer 2: "Load Sample Package" dropdown | Click pre-loaded sample package |
| **CORS Policy Blocks Upload** | Med | High | Browser console CORS error | Configure FastAPI `CORSMiddleware` with `allow_origins` | Use Vite dev server reverse proxy |
| **Canvas Coordinates Misaligned** | Med | Med | BBox offset from text | Normalize coordinates as $0.0\text{--}1.0$ percentages | Scale boxes using natural image dimensions |
| **Small Projector Text Unreadable** | Low | High | Judge cannot read numbers | Increase card typography to $\ge 18\text{px}$; high-contrast colors | Full-screen zoom modal on evidence crops |

---

## 16. Daily Report Format (< 5 Minutes)
```text
MEMBER 5 DAILY STATUS (DATE: ________)
• DONE: [Components built and tested today]
• BLOCKED: [Any frontend or API blockers > 30 mins]
• TESTED: [Browsers and viewports verified]
• NEXT: [Tomorrow's UI/UX milestone]
• RISK: [Any stage legibility or integration concern]
```

---

## 17. Definition of Done (DoD)
A task is DONE when:
1. TypeScript code is written with zero compiler errors in `apps/web/`.
2. Component renders responsively across desktop, tablet, and mobile viewports.
3. Live upload triggers FastAPI backend and displays real inspection results.
4. Layer 2 failover sample selector operates with 10 benchmark packages.
5. Handshake is verified with Member 4 (Backend) and Member 6 (DevOps).

---

## 18. AI Coding Workflow
$$\text{PLAN (Sketch UI Layout)} \longrightarrow \text{PROMPT AI (Tailwind / React)} \longrightarrow \text{REVIEW (Accessibility \& Clean DOM)} \longrightarrow \text{RUN \& TEST} \longrightarrow \text{VERIFY} \longrightarrow \text{HANDOFF}$$
- **AI CAN DO:** Generate Tailwind component layouts, TypeScript interface boilerplate, and SVG icons.
- **MEMBER MUST DECIDE:** Visual hierarchy, state badge color taxonomy, user journey flow, and failover trigger locations.

---

## 19. Buffer Work
- **Primary:** Upload dropzone, 5-State dashboard, Evidence canvas, Inspector review modal, Sample package selector.
- **Buffer Task 1:** Implement HTML5 MediaStream live camera viewfinder option for mobile browsers.
- **Buffer Task 2:** Add dark mode / high-contrast regulatory inspection theme.
