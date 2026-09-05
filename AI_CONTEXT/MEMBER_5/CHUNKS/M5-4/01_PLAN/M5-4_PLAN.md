# CHUNK M5-4 ENGINEERING PLAN
**Subsystem:** Member 5 (Web Frontend & User Experience)  
**Chunk:** M5-4 — Declaration Table, Evidence Linking & Inspector Review Workflow  
**Timestamp:** 2026-09-05T17:56:30+05:30  

---

## 1. Objectives & Scope
1. **Declaration Table (`DeclarationTable.tsx`):**
   - Clean, professional table of mandatory and detected declarations.
   - Distinct columns: Field Name, Value (with raw OCR distinction), Status badge, Extraction Confidence, Measurement status, Evidence link action, Review action.
   - Responsive design: Transforms to stacked declaration cards on viewport < 768px.
   - Keyboard accessible navigation (Arrow keys, Enter, Space).
2. **Evidence Linking & Canvas Synchronization:**
   - Explicit identifier linking (`declaration.sourceTokenIds` -> `ocrToken.id`).
   - Support for both single token and multiple token declarations.
   - Coordinated highlight states on canvas (selected token vs declaration-linked tokens vs low-confidence tokens).
   - Smooth viewport centering / zoom-to-fit for linked tokens.
   - Graceful handling when evidence tokens are absent.
3. **Inspector Review Modal (`InspectorReviewModal.tsx`):**
   - Accessible dialog reusing M5-1 `Dialog` primitive.
   - Displays clear context: Field, Statutory rule citation, Verdict, Rationale, OCR evidence vs normalized value.
   - Review states: `IDLE`, `SUBMITTING`, `SUCCESS`, `ERROR`.
   - Actions: Confirm verification, Flag statutory deficit, Reviewer notes (bounded length).
   - Strict state isolation (no stale notes/actions when switching declarations).
4. **Manual Reference Points (Two-Point Caliper Tool):**
   - Interactive reference point placement on canvas (`Point A`, `Point B`).
   - Transformation pipeline: screen coordinates -> canvas coordinates -> original unscaled image pixel coordinates.
   - Coordinate validation: Disallows identical points, < 2px distance, out-of-image bounds.
   - Displays optical pixel distance only. Strictly NO client-side physical mm or legal compliance calculation.
5. **Service Layer Integration:**
   - Extended `IInspectionClient` with `submitReview(...)`.
   - `MockInspectionAdapter`: Simulates synthetic review workflow, labeled `SYNTHETIC DEMO`.
   - `LiveApiAdapter`: Defensively identifies review submission as pending Member 4 backend deployment.
6. **Automated Verification:**
   - Unit tests covering 20 distinct verification scenarios.
   - TypeScript compile check & Next.js production build check.
   - Chrome DevTools MCP browser verification.
