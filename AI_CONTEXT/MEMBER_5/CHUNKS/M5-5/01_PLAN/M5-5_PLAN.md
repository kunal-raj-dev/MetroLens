# CHUNK M5-5 ENGINEERING PLAN
**Subsystem:** Member 5 (Web Frontend & User Experience)  
**Chunk:** M5-5 — Sample Package Workflow + Demo Mode + Report/PDF Integration + Workflow Hardening  
**Date:** 2026-09-05  

---

## 1. Objectives & Scope
1. **Sample Package Selector (`SamplePackageSelector.tsx`):**
   - Provide a carousel/grid selector of benchmark package fixtures backed by real static assets in `public/fixtures/`.
   - Display source-backed metadata: sample ID, language, package category, test characteristics.
   - Distinct, prominent disclosure: `SYNTHETIC DEMO`.
   - Dispatches through standard `InspectionClient` pipeline, producing normalized `FrontendInspectionModel`.
2. **Demo Mode vs Live Mode Separation:**
   - Visual mode indicators in header and result views.
   - Strict mode boundary: switching modes triggers complete inspection state reset.
   - Zero silent degradation: live network failure reports real error rather than falling back to mock.
3. **Declarations & Review Integration (M5-4 completion & workflow hardening):**
   - `DeclarationTable.tsx`: Tabular display of mandatory and detected declarations with confidence, values, status, and canvas focus actions.
   - `InspectorReviewModal.tsx`: Officer review modal to confirm compliance or flag deficits with optional notes.
   - Fix `LiveApiAdapter` missing `submitReview` implementation.
4. **Report / PDF Integration (`reportClient.ts`):**
   - Implements `POST /api/v1/report/pdf` per `docs/API_CONTRACT.md`.
   - Honest availability check: if backend endpoint is unavailable, display pending notice. No fake PDF generation in frontend.
   - Stale report protection, debounce guard, AbortController support, object URL lifecycle management.
5. **Session Reset Workflow:**
   - "Start New Inspection" button clearing all state (file, preview URL, inspection, tokens, review, report).
6. **Automated Verification & Browser Testing:**
   - End-to-end regression tests and Chrome DevTools MCP verification across responsive viewports.
