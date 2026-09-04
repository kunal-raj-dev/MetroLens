# MASTER 8–9 DAY EXECUTION PLAN & SIX-MEMBER ALLOCATION (V0.2)
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)
**Plan Status:** Authoritative Engineering Roadmap | **Version:** 0.2 (Post-Audit Edition)  
**Date:** 4 September 2026 | **Governing Constraint:** 6 Members Developing 2 SIH Projects in Parallel

---

## 1. Hackathon Engineering Strategy & Value Optimization

Because the team is simultaneously developing a second project, **every task must be ruthlessly evaluated on engineering time vs. jury mark contribution**:

```
                          VALUE VS. EFFORT MATRIX
┌──────────────────────────────────────┬──────────────────────────────────────┐
│ HIGH VALUE / LOW TIME (MUST BUILD)   │ HIGH VALUE / HIGH TIME (CAREFUL)     │
│ • Deterministic Python Rule Engine   │ • Optical Metric Calibration Spike   │
│ • Unit Sale Price (USP) Math Auditor │ • Local ONNX PaddleOCR Integration   │
│ • Tamper-Evident Assessment Report   │ • Responsive Viewfinder PWA          │
│ • 5-State Inspector UI Cards         │ • 35-SKU Ground-Truth Benchmark Set  │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ LOW VALUE / LOW TIME (BUFFER ONLY)   │ LOW VALUE / HIGH TIME (EXCISED / OUT)│
│ • eMaap Mock REST Endpoint & Sync    │ • Playwright E-Commerce Web Scraper  │
│ • Pre-captured Demo Sample Suite     │ • Production eMaap Gateway Auth      │
│ • Viewfinder Glare Warning Badge     │ • 100-Package Caliper Measurements   │
│                                      │ • Full 3D Curved Surface Unwarping   │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. Six-Member Ownership & Dual-Project Allocation

Tasks are assigned by **concrete outcome ownership**, pairing primary leads with cross-support secondaries:

| Member | Primary Role | Secondary Cross-Support | Day 1–2 Responsibility | Day 3–4 Responsibility | Day 5–6 Responsibility | Day 7–8 Responsibility |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | **AI & OCR Lead** | Backend API Support | Setup PaddleOCR ONNX; run 24h OCR latency spike. | Optimize CPU threads; build text bounding box cropper. | Multilingual Devanagari dictionary mapping. | Standalone offline packaging; model freezing. |
| **M2** | **Calibration & Geometry Lead** | Physical Data Collection | Run 24h Calibration Spike (coin vs card vs tilt). | Implement vertical cylinder generator invariance logic. | Calibrated font stroke measurement module. | Optical stress testing across variable lighting. |
| **M3** | **Backend & Rule Engine Lead** | Architecture Governance | Scaffold FastAPI; write Pydantic schemas & USP math. | Codify Rules 6(1)(a)-(h), 7, 8, 9 Table 1, 26. | Expose `/api/v1/inspect`; wire CV, OCR, and rules. | Automated end-to-end integration test suite. |
| **M4** | **Frontend & UX Lead** | Demo Stagecraft Support | Initialize Vite/React PWA; build camera viewfinder. | Build Extracted Declarations & 5-state result cards. | Visual evidence side-by-side crop viewer. | Offline PWA caching; Layer 2 sample dropdown. |
| **M5** | **Data & Benchmark Lead** | Calibration Support | Source Phase 1 packages (20 SKUs); 1200 DPI scan. | Build Phase 2 benchmark dataset (35–40 SKUs). | Run automated CER, WER, and font MAE benchmark. | Compile formal Benchmark Results document. |
| **M6** | **Product & Presentation Lead** | QA & Compliance Audit | Draft Assessment Report PDF schema; Jan Vishwas check. | Implement cryptographic SHA-256 PDF generator. | Build eMaap mock sync adapter; rehearse script. | Lead 5 adversarial jury drills; demo kit setup. |

---

## 3. Mandatory First 24-Hour Technical Validation Spike (Hours 0 to 24)

The riskiest architectural claims must be validated immediately. **Do not write application UI or complex backends until this spike passes**:

```
                      FIRST 24-HOUR VALIDATION SPIKE
                      
  [ Hour 0: Virtualenv Setup & Test Image Sourcing (15 Packages) ]
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
  [ Experiment A ]        [ Experiment B ]        [ Experiment C ]
  PaddleOCR ONNX CPU      Optical Metric Scale    Deterministic Rules
  Latency & CER Test      Coin vs Card vs Tilt    25 Unit Tests Pass
       │                       │                       │
       └───────────────────────┼───────────────────────┘
                               ▼
                        [ Experiment D ]
               End-to-End Headless CLI Pipeline
        (Image -> OCR -> Normalizer -> Rules -> Output)
                               │
                               ▼
                 [ HOUR 24 FORMAL MILESTONE ]
                 • GO: All 4 experiments pass
                 • GO WITH MODIFICATION: Calibration adjusted
                 • PIVOT: Trigger secondary problem statement
```

### The 4 Spike Experiments:
- **Experiment A (Local OCR Latency & Accuracy):** Run `ch_PP-OCRv4` ONNX int8 model on 15 package crops on demonstrator CPU. Target: Latency $< 1,200\text{ms}$, CER $< 8\%$.
- **Experiment B (Calibration Feasibility):** Measure Indian 10-Rupee coin diameter and scale factor $S$ at $0^\circ, 15^\circ, 30^\circ$ tilt against a millimeter grid. Target: Scale error $< 5\%$ at $<15^\circ$ tilt. Compare against ISO card corners.
- **Experiment C (Deterministic Rule Suite):** Run Python rule suite against 25 synthetic cases (including Rule 6(11) USP denominations and Rule 26 tobacco exceptions). Target: $100\%$ pass.
- **Experiment D (End-to-End Headless Pipeline):** Execute single Python CLI command taking an image path and printing structured JSON compliance results in $<2.5\text{s}$.

---

## 4. The 48-Hour Go / No-Go Decision Protocol

At **T+48 Hours**, the team conducts a formal binary review across **5 Hard Gates**:

| Gate | Description | Pass Threshold | Warning Condition | Failure Condition | Action upon Failure |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Gate A** | **Legal Rule Engine** | 100% tests pass on 25 synthetic test cases. | 1–2 edge cases fail on obscure rounding. | Fundamental logic flaw in USP or Rule 9. | Refactor rule logic; lock rule scope to core 6 clauses. |
| **Gate B** | **Scene Text OCR** | CER $< 8\%$, CPU latency $< 1,200\text{ms}$ on 15 packages. | CER $8\text{–}12\%$ or latency $1.2\text{–}1.8\text{s}$. | Model crashes or CER $> 15\%$ on clear print. | Add CLAHE contrast preprocessing; switch to ROI cropping. |
| **Gate C** | **Metric Calibration** | Scale error $< 5\%$ (MAE $< 0.15\text{mm}$) on planar packs. | Scale error $5\text{–}8\%$. | Scale error $> 10\%$; ellipse fit unstable. | **DROP AUTOMATIC FONT MEASUREMENT FROM MVP.** Pivot demo to declaration presence, SI units, and USP math. |
| **Gate D** | **Assessment Report** | PDF compiles with SHA-256 hash in $< 500\text{ms}$. | Styling or layout clipping on long text. | PDF compilation crashes backend. | Switch from ReportLab to clean HTML-to-PDF template. |
| **Gate E** | **Offline E2E Pipeline**| End-to-end flow executes locally in $< 3.0\text{s}$. | Latency between $3.0\text{s}$ and $4.5\text{s}$. | Pipeline requires active internet connection. | Remove cloud dependencies; enforce synchronous local calls. |

### Decision Outcomes at Hour 48:
1. **GREEN LIGHT (GO):** All 5 gates PASS $\rightarrow$ Proceed with full UI integration and benchmark execution.
2. **AMBER LIGHT (MODIFY):** Gate C exhibits $5\text{–}8\%$ error $\rightarrow$ Constrain font measurement to flat boxes with viewfinder plane guide; add manual reference calibration in UI.
3. **RED LIGHT (PROJECT PIVOT):** Gate B or Gate C catastrophically fails $\rightarrow$ **Trigger emergency pivot to the secondary problem statement (SIH26073: Weather Anomaly Detection)** with 7 full days remaining.

---

## 5. Master Day-by-Day Execution Roadmap

```
                               MASTER TIMELINE
  Day 1: 24h Technical Spike & Phase 1 Data (20 SKUs)
  Day 2: 48h Kill Switch Review, Homography & Core Rules
  Day 3: Entity Normalizer & Assessment Report PDF Generator
  Day 4: Pipeline Integration & Viewfinder Camera Wiring
  Day 5: Phase 2 Benchmark Run (35–40 SKUs) & Evidence UI
  Day 6: Cylindrical Mode Refinement & eMaap Mock Adapter
  Day 7: 5-Layer Redundancy Setup & 100% Offline Stress Testing
  Day 8: STRICT CODE FREEZE (12:00 PM) & 5 Adversarial Jury Drills
  Day 9: Final Battery/Prop Check & Competition Presentation
```

### Detailed Daily Breakdown:

#### DAY 1: The First 24-Hour Technical Validation Spike
- **Goal:** Prove the mathematical and optical viability of local OCR and metric scale recovery.
- **Milestones:**
  - M1: Local virtualenv with quantized PaddleOCR ONNX running on CPU.
  - M2: Calibration spike script testing coin vs ISO card vs tilt angles.
  - M3: FastAPI scaffolding and Pydantic canonical declaration schemas.
  - M4: Vite + React PWA shell with responsive viewport and camera stream access.
  - M5: Acquire 20 physical packages; scan 10 on 1200 DPI scanner for ground truth.
  - M6: Audit legal templates; codify Jan Vishwas Section 36(1) report schema.
- **Checkpoint:** Hour 24 CLI script running: `python spike_e2e.py test.jpg` $\rightarrow$ prints valid JSON.

#### DAY 2: 48-Hour Review, Calibration & Core Rules
- **Goal:** Complete the 48-hour kill switch review and implement deterministic statutory rules.
- **Milestones:**
  - M1: Implement text bounding-box cropper and adaptive CLAHE contrast pre-filter.
  - M2: Implement planar metric scale recovery with tilt angle validation.
  - M3: Implement Rule 6(1)(c) (SI units), Rule 6(1)(e) (MRP), and Rule 6(11) (USP math).
  - M4: Build Viewfinder screen with circular targeting guide and glare pre-check indicator.
  - M5: Expand physical package set to 30 SKUs; record outer dimensions and caliper heights.
  - M6: Implement initial Assessment Report PDF generator using ReportLab.
- **Checkpoint:** 48-Hour Kill Switch Review. Formal sign-off on Gates A through E.

#### DAY 3: Entity Normalizer & Cryptographic Reporting
- **Goal:** Connect OCR text outputs to canonical schemas and generate tamper-evident PDF reports.
- **Milestones:**
  - M1: Implement regex entity parser mapping raw text lines to `CanonicalDeclaration`.
  - M2: Build numeral stroke height measurement module from rectified binary crops.
  - M3: Complete remaining rule modules: Rules 6(1)(a), 6(1)(d), 6(1)(g), and Rule 26.
  - M4: Build Extracted Declarations card and Compliance Result status card in React.
  - M5: Add 8 synthetic defect packages with clearly marked mock labels.
  - M6: Integrate cryptographic SHA-256 hashing of raw image, crops, and metadata into PDF.
- **Checkpoint:** Headless pipeline producing a signed PDF report from a raw image file.

#### DAY 4: End-to-End Pipeline Integration
- **Goal:** Wire frontend web interface to local FastAPI backend; achieve sub-2.5s execution.
- **Milestones:**
  - M1: Expose `/api/v1/inspect/package-image` endpoint wiring all modules.
  - M2: Implement vertical cylinder generator invariance module for upright cans.
  - M3: Enforce 5-state compliance classification in rule engine responses.
  - M4: Connect mobile capture button to inspection endpoint with real-time latency bar.
  - M5: Finalize Phase 2 benchmark dataset (35–40 SKUs); lock `benchmark.json`.
  - M6: Implement mock eMaap adapter endpoint (`POST /api/v1/emaap/mock-sync`).
- **Checkpoint:** Live mobile web capture yielding on-screen verdict in $<2.5\text{s}$ on localhost.

#### DAY 5: Benchmark Execution & Evidence UI
- **Goal:** Run the formal empirical benchmark and build side-by-side evidence viewer.
- **Milestones:**
  - M1: Profile and optimize CPU inference threads to ensure consistent latency.
  - M2: Fine-tune contour edge detection to minimize stroke jitter.
  - M3: Implement Rule 9 Table 1 lookup engine indexing calibrated PDP area.
  - M4: Build Visual Evidence viewer with side-by-side rectified crop and deficit badge.
  - M5: Run automated benchmark script across all Phase 2 packages; record CER, WER, MAE.
  - M6: Add Inspector Manual Review toggle screen with 1-tap field confirmation.
- **Checkpoint:** Empirical metrics recorded into `docs/BENCHMARK_RESULTS.md`.

#### DAY 6: Cylindrical Testing & Presentation Rehearsal
- **Goal:** Validate curved packaging handling and rehearse live 3-minute pitch.
- **Milestones:**
  - M1: Add Devanagari keyword dictionary mapping for bilingual packaging.
  - M2: Verify vertical font height invariance on 5 cylindrical beverage cans.
  - M3: Add UI manual scale override mode (click 2 points) as a failsafe.
  - M4: Integrate PDF preview and 1-click download directly inside the web UI.
  - M5: Generate confusion matrix (Precision, Recall, F1, FPR) from benchmark data.
  - M6: Draft presentation slide deck following official SIH template; time 3-minute pitch.
- **Checkpoint:** Live scan of a cylindrical can proving vertical font height invariance.

#### DAY 7: 5-Layer Redundancy & Offline Hardening
- **Goal:** Eliminate every potential venue failure mode; achieve total offline resilience.
- **Milestones:**
  - M1: Verify all ONNX models and dependencies load with zero internet access.
  - M2: Test measurement stability under low ambient light and harsh glare.
  - M3: Write comprehensive automated integration test suite (`pytest tests/`).
  - M4: Implement Layer 2 Pre-Captured Sample Suite dropdown with 10 pristine test cases.
  - M5: Package physical demo kit: digital caliper, standard 10-Rupee coins, hero packages.
  - M6: Export Layer 4 static HTML bundle and Layer 5 4K backup demonstration video.
- **Checkpoint:** Full live dry-run executed with laptop Wi-Fi and Bluetooth disabled.

#### DAY 8: Strict Code Freeze & Adversarial Jury Drills
- **Goal:** Freeze all code modifications; prepare team for intense jury cross-examination.
- **Schedule:**
  - **12:00 PM:** **STRICT CODE FREEZE.** Zero new features or algorithmic changes.
  - **2:00 PM:** Mock Jury Drill 1: Technical CV and optical physics grilling (Q1–Q5).
  - **3:30 PM:** Mock Jury Drill 2: Legal Metrology and Jan Vishwas Act grilling (Q6–Q10).
  - **5:00 PM:** Mock Jury Drill 3: AI perception vs deterministic rules grilling (Q11–Q14).
  - **6:30 PM:** Final pitch rehearsal with 3-minute stopwatch timer.
- **Checkpoint:** All 6 team members fluent in answering adversarial questions from memory.

#### DAY 9: Competition Day & Presentation Execution
- **Goal:** Deliver a flawless live demonstration, project calm competence, and win.
- **Execution:**
  - Setup physical biscuit pack, 10-Rupee coin, and digital caliper on the jury table.
  - Deliver the 3-minute live pitch; execute the live 2-second scan.
  - Invite judges to physically verify optical font measurements with the caliper.
