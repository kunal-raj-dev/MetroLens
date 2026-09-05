# ACTUAL VS CLAIMED: CHUNK M5-5
**Project:** MetroLens AI™ (SIH26034)  
**Subsystem:** Member 5 (Frontend Engineering)  

---

## 1. Audit Table: Claimed vs Verified Reality

| Specification Claim | Claimed Behavior | Verified Reality | Evidence | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Benchmark Packages Catalog** | Support 8 statutory test cases from `manifest.json` | All 8 packages modeled with genuine resolutions, language tags, statutory condition descriptions, and static PNG assets in `public/fixtures/` | `fixtures.ts`, `SamplePackageSelector.tsx` | **VERIFIED** |
| **Prominent Synthetic Disclosure** | Always disclose synthetic fixtures to prevent false claims | `SYNTHETIC DEMO` badges, warning banners, and review dispatch indicators visible across UI | `page.tsx`, `SamplePackageSelector.tsx`, `InspectorReviewModal.tsx` | **VERIFIED** |
| **Shared Standard UI** | Synthetic demo uses same UI components as live inspection | Identical `ImageUploadZone`, `ComplianceDashboard`, `EvidenceCanvas`, and `DeclarationTable` components used for both modes | `page.tsx` | **VERIFIED** |
| **Strict Mode Separation** | Switching modes resets state; network failures never fallback to mock | Mode toggle purges active inspection and file state. Live adapter failure produces actionable error with manual switch button | `page.tsx:handleModeToggle`, `liveApiAdapter.ts` | **VERIFIED** |
| **Report PDF Integration** | Request PDF from `POST /api/v1/report/pdf` | Implemented `ReportClient` with `%PDF-` magic byte check, filename sanitization, anti-double-click lock, and honest error handling | `reportClient.ts` | **VERIFIED** |
| **Zero Client PDF Fabrication** | Frontend must NEVER generate fake client PDF | When backend report endpoint is offline, UI truthfully displays warning alert without generating local PDF | `reportClient.ts`, browser test | **VERIFIED** |
| **Bidirectional Evidence Linking** | Clicking declaration highlights token on canvas | Declaration table rows and Canvas buttons zoom and center canvas onto matching token quad | `page.tsx`, `EvidenceCanvas.tsx` | **VERIFIED** |
| **Inspector Review Dialog** | Officer review with confirm/flag and character-counted notes | Fully functional accessible dialog with 500-character audit notes counter and audit trail update | `InspectorReviewModal.tsx` | **VERIFIED** |
| **Complete Session Reset** | "New Inspection" purges all state | Cleans file, preview URL, dimensions, tokens, declarations, review dialog, and report notifications | `page.tsx:handleStartNewInspection` | **VERIFIED** |
| **Zero Legal Calculation Invariant** | Client never computes font height or Rule 6/7/12 legality | Verified across codebase that font minimums and verdicts are read purely from DTOs | Unit tests `m5_5_verification.test.ts` | **VERIFIED** |
| **Zero Metric Calibration Invariant** | Client never calculates homography or metric scale | Homography matrix and mm/px ratios computed exclusively by backend engine | Architecture audit | **VERIFIED** |
| **Zero Git Commands Invariant** | No git commands executed | Zero git commits, zero git pushes, zero working tree modifications | Run log audit | **VERIFIED** |
