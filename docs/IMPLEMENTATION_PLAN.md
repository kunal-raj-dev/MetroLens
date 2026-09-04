# MASTER 8–9 DAY EXECUTION PLAN & SIX-MEMBER ALLOCATION
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)

This document establishes the day-by-day engineering roadmap, multi-workstream parallelization strategy, and strict six-member task allocation for InnoHack 3.0 / SIH 2026.

---

## 1. Team Structure & Workstream Architecture

Because the team is simultaneously developing a second project for another Problem Statement, **ruthless scope discipline, zero duplication of effort, and decoupled parallel workstreams are mandatory**.

```
                           SIX-MEMBER WORKSTREAM TOPOLOGY
┌─────────────────────────────────────────────────────────────────────────────┐
│ MEMBER 1: AI & Computer Vision Lead (Workstream A)                          │
│ • Domain: Local PaddleOCR v4 integration, ONNX quantization, text detection │
│ • Non-Goal: Do NOT touch frontend UI or legal rule writing                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ MEMBER 2: Metric Calibration & Geometry Lead (Workstream B)                 │
│ • Domain: OpenCV coin contour detection, homography warping, font-height mm │
│ • Non-Goal: Do NOT write PDF report generators or e-commerce scrapers       │
├─────────────────────────────────────────────────────────────────────────────┤
│ MEMBER 3: Backend & Statutory Rule Architect (Workstream C)                 │
│ • Domain: FastAPI server, Pydantic schemas, 8 Rule 6 modules, USP math audit│
│ • Non-Goal: Do NOT touch computer vision homography math or mobile styling  │
├─────────────────────────────────────────────────────────────────────────────┤
│ MEMBER 4: Frontend & UX/UI Engineer (Workstream D)                          │
│ • Domain: Vite/React PWA, camera viewfinder, coin contour overlay, dashboard│
│ • Non-Goal: Do NOT write raw OCR algorithms or database schemas             │
├─────────────────────────────────────────────────────────────────────────────┤
│ MEMBER 5: Data, Benchmarking & Ground Truth Lead (Workstream E)              │
│ • Domain: 100 physical packages, caliper measurements, CER/WER/MAE benchmark│
│ • Non-Goal: Do NOT spend time writing complex backend API routes            │
├─────────────────────────────────────────────────────────────────────────────┤
│ MEMBER 6: Product, Demo Stagecraft & Reporting Lead (Workstream F)          │
│ • Domain: Form A PDF generator (SHA-256), eMaap mock, pitch script, Q&A deck│
│ • Non-Goal: Do NOT attempt to train machine learning models                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Master Dependency Graph & Critical Path

```
                    DEPENDENCY GRAPH & CRITICAL PATH
                    
[M5: 100 Physical SKUs + Calipers] ──┐
                                     │
[M1: PaddleOCR Local ONNX Engine] ───┼──> [Canonical Entity Parser] ──┐
                                     │                                │
[M2: Coin Homography Metric Scale] ──┘                                ▼
                                                       [M3: Python Statutory Rule Engine]
                                                                      │
                                                       ┌──────────────┴──────────────┐
                                                       ▼                             ▼
                                        [M4: Responsive PWA Dashboard]  [M6: Form A PDF Report]
                                                       │                             │
                                                       └──────────────┬──────────────┘
                                                                      ▼
                                                       [END-TO-END 2-SECOND DEMO]
```

### The Critical Path (The Bottleneck Spine):
`Day 1: Coin Homography Proof` $\rightarrow$ `Day 2: Local OCR Extraction` $\rightarrow$ `Day 3: Deterministic Rule Engine` $\rightarrow$ `Day 5: Viewfinder Integration` $\rightarrow$ `Day 7: Form A PDF & E2E Validation` $\rightarrow$ `Day 8: Caliper Benchmark Run`.

---

## 3. Day-by-Day Master Execution Schedule

### DAY 1: Foundations, Metric Calibration Proof & Data Sourcing
- **Primary Goal:** Prove the core mathematical moat (metric scale recovery) and collect initial physical packaging.
- **Deliverables by Member:**
  - *M1 (AI/CV):* Setup local Python virtual environment; run standalone PaddleOCR v4 on sample packaging image; verify text line and bounding box extraction.
  - *M2 (Calibration):* Implement `cv2.findContours` + ellipse fitting to detect 27.0mm Indian 10-Rupee coin; compute pixel-to-mm scale factor $S$; verify on flat surface.
  - *M3 (Backend):* Scaffold FastAPI repository structure; define Pydantic schemas: `CanonicalDeclarationSchema`, `ViolationResultSchema`, `InspectionSessionSchema`.
  - *M4 (Frontend):* Initialize Vite + React project; configure design tokens, layout shell, and mobile camera access via `getUserMedia`.
  - *M5 (Data):* Acquire 30 physical Indian FMCG packages (biscuits, shampoos, snacks); borrow digital vernier caliper (0.01mm resolution); measure true font heights.
  - *M6 (Product):* Review Jan Vishwas Act 2023 Gazette text; draft exact Form A inspection report template and statutory citation map.
- **End-of-Day Checkpoint / Demo:** Member 2 demonstrates Python script accurately measuring coin diameter to within $\pm 0.1\text{mm}$.

---

### DAY 2: Planar Homography & Rule Engine Codification
- **Primary Goal:** Overcome perspective tilt via homography matrix ($H^{-1}$) and implement core statutory rules.
- **Deliverables by Member:**
  - *M1 (AI/CV):* Quantize PaddleOCR to ONNX int8 format; evaluate CPU latency on laptop (target: $<1.0\text{s}$); build bounding box cropper.
  - *M2 (Calibration):* Implement Planar Homography matrix calculation ($H$) using 4 corners / coin orientation; generate orthorectified metric crops from tilted images ($25^\circ$ tilt).
  - *M3 (Backend):* Implement Rule 6(1)(c) (Net Qty SI units), Rule 6(1)(e) (MRP & tax qualifier), and Rule 6(11) (Unit Sale Price deterministic arithmetic auditor).
  - *M4 (Frontend):* Build camera viewfinder screen with visual coin alignment guide (circular targeting reticle) and live resolution indicator.
  - *M5 (Data):* Expand physical package count to 60 SKUs; record true physical PDP dimensions ($H \times W$) and caliper font heights into `data/ground_truth_benchmark.json`.
  - *M6 (Product):* Implement ReportLab / Weasyprint script generating initial static Form A PDF report with placeholder data.
- **End-of-Day Checkpoint / Demo:** **FIRST 48-HOUR KILL-SWITCH GATE.** Verify coin scale recovery error $<5\%$ on tilted surface and 100% pass on USP arithmetic unit tests.

---

### DAY 3: Entity Normalizer & Complete Rule Engine Suite
- **Primary Goal:** Bridge OCR text outputs into structured Pydantic schemas and complete all 8 statutory rule modules.
- **Deliverables by Member:**
  - *M1 (AI/CV):* Implement regex entity normalizer mapping raw OCR text lines to canonical schema keys; integrate CLAHE preprocessing for dot-matrix text.
  - *M2 (Calibration):* Integrate font stroke height measurement (measuring capital letter x-height in millimeters from rectified binary text crop).
  - *M3 (Backend):* Complete remaining rule modules: Rule 6(1)(a) (Address + PIN regex), Rule 6(1)(d) (Mfg date validator), Rule 6(1)(g) (Consumer care email/phone), Rule 26 (miniature package exemptions).
  - *M4 (Frontend):* Build Screen 4 (Extracted Declarations card) and Screen 5 (Compliance Result status card) with mock API payload.
  - *M5 (Data):* Reach 85 physical packages; add 10 intentional non-compliant test packages (missing USP, tiny fonts, "Gms" units).
  - *M6 (Product):* Implement SHA-256 cryptographic hashing module embedding raw image hash and inspection metadata into PDF generator.
- **End-of-Day Checkpoint / Demo:** Run end-to-end headless script: Raw image in $\rightarrow$ OCR $\rightarrow$ Calibrated font mm $\rightarrow$ Rule engine $\rightarrow$ Violations list.

---

### DAY 4: Pipeline Integration & Glare Pre-Check
- **Primary Goal:** Connect frontend camera stream to local FastAPI backend; implement glare rejection.
- **Deliverables by Member:**
  - *M1 (AI/CV):* Build HSV saturation glare-mask detector ($V > 250, S < 30$); expose `/api/v1/cv/glare-check` endpoint.
  - *M2 (Calibration):* Implement cylinder generator vertical height invariance logic: lock measurement strictly to vertical axis within central $60^\circ$ generator strip.
  - *M3 (Backend):* Expose primary inspection endpoint: `POST /api/v1/inspect/package-image`; wire together CV, OCR, entity parser, and rule engine.
  - *M4 (Frontend):* Connect camera capture button to FastAPI inspection endpoint; implement loading spinner and latency timer.
  - *M5 (Data):* Complete physical benchmark dataset to full **100 physical SKUs**; lock ground truth JSON file.
  - *M6 (Product):* Build eMaap REST API mock adapter (`POST /api/v1/emaap/sync-inspection`) and simulate national database sync.
- **End-of-Day Checkpoint / Demo:** Complete end-to-end scan from mobile web viewfinder to dashboard display in $<2.5\text{ seconds}$ on localhost.

---

### DAY 5: Cylindrical Handling & Full UI Polish
- **Primary Goal:** Polish mobile responsive inspection workflow; handle curved container edge cases.
- **Deliverables by Member:**
  - *M1 (AI/CV):* Multilingual Devanagari dictionary mapping for Hindi packaging text (`अधिकतम खुदरा मूल्य` $\rightarrow$ `mrp`).
  - *M2 (Calibration):* Refine contour sub-pixel edge detection (`cv2.cornerSubPix`) to achieve font measurement MAE $<0.12\text{mm}$.
  - *M3 (Backend):* Implement Rule 9 Table 1 lookup engine indexing calibrated PDP area $A$ to mandatory minimum font heights.
  - *M4 (Frontend):* Build Screen 6 (Violation Evidence view with side-by-side rectified crop) and Screen 7 (Inspector Manual Review toggle).
  - *M5 (Data):* Run benchmark pipeline across first 50 packages; calculate preliminary CER, WER, and font MAE.
  - *M6 (Product):* Add "Brand Pre-Flight Artwork Mode" tab on frontend dashboard allowing packaging designers to upload digital artwork PDFs.
- **End-of-Day Checkpoint / Demo:** Live scan of a curved beverage can proving vertical font height measurement invariance.

---

### DAY 6: Evidentiary Notice Generator & E-Commerce Module
- **Primary Goal:** Finalize tamper-evident PDF generation and implement e-commerce marketplace ingestion.
- **Deliverables by Member:**
  - *M1 (AI/CV):* Optimize ONNX inference thread allocation to reduce OCR latency to $<800\text{ms}$ on CPU.
  - *M2 (Calibration):* Add "Manual Reference Override" UI fallback (enables user to click 2 reference points if coin contour fails).
  - *M3 (Backend):* Build Playwright headless e-commerce scraper for Amazon/Blinkit listing URLs; extract packshot images and listing attributes under Rule 6(10).
  - *M4 (Frontend):* Integrate PDF viewer and download trigger directly inside the web UI; add e-commerce URL input field.
  - *M5 (Data):* Execute benchmark run across all 100 packages; generate confusion matrix (Precision, Recall, F1, FPR).
  - *M6 (Product):* Rehearse 3-minute live presentation pitch; finalize presentation slide deck following official SIH template.
- **End-of-Day Checkpoint / Demo:** One-click download of a cryptographic Form A PDF report from a live scan in under 3 seconds total session time.

---

### DAY 7: End-to-End Stress Testing & 5-Layer Redundancy Setup
- **Primary Goal:** Harden system against all venue failure modes and rehearse live stagecraft.
- **Deliverables by Member:**
  - *M1 (AI/CV):* Package all models, weights, and dependencies into an offline standalone directory (zero internet dependency).
  - *M2 (Calibration):* Verify measurement error bounds under variable lighting (bright sun, indoor fluorescent, dim room).
  - *M3 (Backend):* Write automated integration test suite (`pytest tests/test_e2e_pipeline.py`) testing 20 distinct package flows.
  - *M4 (Frontend):* Implement Layer 2 Pre-Captured Sample Suite dropdown in UI with 10 pristine test cases.
  - *M5 (Data):* Compile official Benchmark Report document (`docs/BENCHMARK_RESULTS.md`) with actual empirical metrics and charts.
  - *M6 (Product):* Prepare Layer 4 static HTML bundle and Layer 5 4K uncut demonstration video on backup USB drives.
- **End-of-Day Checkpoint / Demo:** Complete dry run of the 3-minute live pitch with airplane mode enabled on laptop.

---

### DAY 8: Final Code Freeze & Jury Defense Simulation
- **Primary Goal:** Freeze all codebase modifications; conduct intense adversarial jury defense drills.
- **Deliverables by Entire Team:**
  - **12:00 PM:** **STRICT CODE FREEZE.** Zero new feature additions permitted. Only critical UI bug fixes or typos.
  - **2:00 PM:** Conduct 5 mock jury defense sessions grilling the presenter with all 32 questions from `docs/JURY_QA.md`.
  - **4:00 PM:** Verify digital caliper, physical packages, 10-Rupee coins, and backup USB drives are packed into demo kit.
  - **6:00 PM:** Final presentation slide deck rehearsal with 3-minute stopwatch timer.

---

### DAY 9: Buffer, Presentation Readiness & Competition Day
- **Primary Goal:** Flawless live execution, calm jury defense, and victory.
- **Deliverables by Entire Team:**
  - Final hardware battery check (laptops, phones, mice, chargers).
  - Placement of physical biscuit pack, coin, and digital caliper on the table.
  - Deliver live 3-minute pitch, execute live 2-second scan, and win 1st place.
