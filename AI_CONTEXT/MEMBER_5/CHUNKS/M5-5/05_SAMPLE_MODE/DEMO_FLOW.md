# DEMONSTRATION WORKFLOW: BENCHMARK PACKAGES & DEMO MODE
**Project:** MetroLens AI™ (SIH26034)  
**Subsystem:** Member 5 (Frontend Engineering)  
**Chunk:** M5-5  

---

## 1. Executive Purpose
The Benchmark Demonstration Mode enables hackathon judges, state enforcement officials, and legal metrology auditors to experience and verify the complete MetroLens inspection pipeline using 8 verified statutory benchmark packages without requiring physical packaging cameras or an active GPU cluster.

---

## 2. Inviolable Governance Principles
1. **Prominent Synthetic Disclosure**: Every demonstration package, evidence canvas, and review modal prominently displays the `SYNTHETIC DEMO` / `SYNTHETIC REGRESSION ASSET` notice.
2. **Normalized Shared UI**: Synthetic demonstration packages pass through the exact same ingestion dropzone, validation pipeline, normalized data model, compliance dashboard, evidence canvas, and declaration table as live field inspections.
3. **Strict Separation of State**: Switching between `SYNTHETIC DEMO` and `LIVE INSPECTION` resets the workstation to prevent cross-contamination of custody logs.
4. **Honest Network Transparency**: If live mode fails due to an offline backend, the workstation displays an actionable connection alert and a manual button to switch to demo mode—never a silent fake success.

---

## 3. The 8 Benchmark Packages Catalog

| ID | Title | Packaging Category | Script / Language | Key Statutory Test Condition | Expected Rule Adjudication |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `SYNTH-01` | English Biscuit Pouch | Biscuit Pouch ($640 \times 360$) | English (Latin) | Standard FMCG declarations with USP calculation | **COMPLIANT** (Rule 6 Pass) |
| `SYNTH-02` | Pure Hindi Atta Bag | Atta Bag ($640 \times 360$) | Hindi (Devanagari) | Non-Latin OCR & ₹ currency symbol verification | **COMPLIANT** (Devanagari ₹ Pass) |
| `SYNTH-03` | Bilingual Snack Carton | Snack Carton ($640 \times 380$) | English + Hindi | Bilingual statutory labeling compliance | **COMPLIANT** (Bilingual Pass) |
| `SYNTH-04` | Shrinkflation Micro-Font | Confectionery Pouch ($640 \times 320$) | English | Net wt 35g with 1.2mm font height (< 2.0mm min) | **NON_COMPLIANT** (Rule 7 Font Deficit) |
| `SYNTH-05` | Handwash Liquid Volume | Handwash Bottle ($640 \times 360$) | English | Liquid volume in milliliters (250 ml) with USP | **COMPLIANT** (Volume Metric Pass) |
| `SYNTH-06` | Detergent Pluralized Units | Detergent Pouch ($640 \times 320$) | English | Non-standard unit 'gms' prohibited by Rule 12 | **NON_COMPLIANT** (Rule 12 Prohibited Unit) |
| `SYNTH-07` | Blank / Texture Frame | Blank Cardboard ($640 \times 320$) | None | Low Laplacian variance sharpness ($<50.0$) | **INCONCLUSIVE** (Quality Gate Reject) |
| `SYNTH-08` | Faded Thermal Stamp | Foil Crimp ($640 \times 320$) | English | Degraded thermal expiry date near certainty threshold | **SUSPECT_REVIEW** (Review Required) |

---

## 4. End-to-End User Journey Walkthrough
1. **Officer Landing**: Officer arrives at `http://localhost:3000/`. Workstation defaults to `SYNTHETIC DEMO` mode.
2. **Select Sample**: Officer clicks `SYNTH-04-MICRO-FONT` in the carousel. The static PNG asset is fetched, converted to a `File`, and ingested into `ImageUploadZone`.
3. **Ingestion & Validation**: Client-side image validation checks size, magic bytes, and raster dimensions ($640 \times 320$ px). Dropzone transitions to `READY`.
4. **Inspect Package**: Officer clicks "Inspect Package". `InspectionClient` processes the request via `MockInspectionAdapter` with simulated 1200ms processing delay.
5. **Dashboard & Evidence Canvas**: Macro verdict displays `NON_COMPLIANT (Rule 7 Deficit)`. Evidence Canvas renders original image pixel quads.
6. **Declarations Table Audit**: Net Quantity declaration shows `1.2mm` observed vs `2.0mm` statutory minimum.
7. **Canvas Evidence Linking**: Clicking the declaration row zooms and centers the Evidence Canvas directly onto the micro-font token.
8. **Officer Review**: Officer clicks "Review", opens `InspectorReviewModal`, selects "Flag Deficit", enters audit notes, and submits. Review status updates in the table.
9. **Report Generation**: Officer clicks "Download Report". `ReportClient` attempts to compile report from `POST /api/v1/report/pdf`. If offline, clear notice is shown with zero client-fabricated fake PDF.
10. **Session Reset**: Officer clicks "New Inspection". The workstation purges all session state, returning to clean standby.
