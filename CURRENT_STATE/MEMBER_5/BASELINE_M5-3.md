# BASELINE: MEMBER 5 — CHUNK M5-3
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering & Web UX Lead  
**Timestamp:** 2026-09-05T17:50:30+05:30  
**Phase:** Starting Chunk M5-3 (Compliance Dashboard + Evidence Canvas + Evidence Interaction)  
**Previous Milestones:**  
- M5-0: Audit Complete  
- M5-1: Foundation & Mastercard Design System Verified  
- M5-2: Image Ingestion, Validation, & Inspection Client Verified (34/34 tests passed, Exit Code 0 build)

---

## 1. Initial State Prior to M5-3
- `apps/web/` has working `ImageUploadZone.tsx` capable of handling drag-and-drop, 15 MiB ceiling check, magic byte sniffing, and browser raster decode.
- `apps/web/src/services/inspectionClient.ts` provides `IInspectionClient` with `MockInspectionAdapter` and `LiveApiAdapter`.
- `apps/web/src/types/frontend.ts` has `FrontendInspectionModel` with declarations, quality gate, calibration, and errors.
- `apps/web/src/mocks/fixtures.ts` has synthetic regression fixtures (`SYNTH-01`, `SYNTH-04`, `SYNTH-08`).
- The Right Column of the Officer Workstation currently displays an Evidence Canvas placeholder awaiting Chunk M5-3.
- Member 1 OCR coordinate contract is **frozen** in original input image pixel space with origin $(0,0)$ at top-left.

## 2. Invariants for M5-3
1. **Zero Client Legal Logic**: Frontend does not compute font heights ($h_{\text{mm}}$), physical dimensions, or Rule 6/7 evaluations in React. Backend is authoritative.
2. **No Reinterpretation of Legal Explanations**: Display backend explanations without generating legal text in the client.
3. **Synthetic Transparency**: Synthetic demo assets are visibly badged with clear disclaimers; mock mode must never look like real-world validation.
4. **No Silent Mock Fallback**: If live API is down, show failure and prompt the officer with a manual choice to switch to synthetic demo mode.
5. **Frozen OCR Coordinates**: Polygons and bounding boxes are stored and transformed in original image pixel space. No permanent percentage mutations.
6. **Git Safety**: Zero git commits, zero git pushes.
