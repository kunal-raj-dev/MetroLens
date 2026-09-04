# INDIVIDUAL WORK PLAN: MEMBER 6
# Product, Integration, QA, Benchmark & Release Lead
### Project: MetroLens AI (SIH26034) | Sponsoring Ministry: Ministry of Consumer Affairs
**Document Status:** Authoritative Personal Work Package & Accountability Contract | **Version:** 1.0.0 (Web MVP Edition)  
**Sprint Window:** 8–9 Days | **Primary Packages:** `infra/`, `data/`, `tests/benchmarks/` | **Secondary Role:** Demo Stagecraft & Release Governance

---

## 1. Member Role
**Member 6 — Product Integration, Quality Assurance, Benchmark Verification & Release Lead**

---

## 2. Mission
Guarantee that MetroLens AI is a fully integrated, empirically proven, secure, containerized, and demo-hardened product. Member 6 is personally responsible for establishing the continuous integration pipeline, curating the 35-SKU physical packaging benchmark dataset with dual-instrument ground truth (1200 DPI flatbed optical scans + digital vernier calipers), executing automated regression benchmarks (proving CER $< 6.0\%$ and font height MAE $< 0.15\text{mm}$ with zero fabricated numbers), building production-ready multi-stage Docker containers booting in $< 10\text{s}$, and rehearsing the 5-Layer live demonstration failover architecture to ensure flawless stage execution.

---

## 3. Ownership

### Primary Ownership:
- `infra/Dockerfile` & `infra/docker-compose.yml`: Multi-stage container builds, non-root user execution, and production hosting configuration.
- `.github/workflows/ci.yml`: Automated CI pipeline (ruff linting, mypy typechecking, pytest test execution).
- `data/raw/` & `data/ground_truth/`: Curated 35-SKU physical retail packaging dataset across 5 FMCG categories.
- `data/manifests/manifest.yaml` & `ground_truth_benchmark.json`: Verified ground-truth coordinate and dimension manifests.
- `tests/benchmarks/test_benchmark_suite.py`: Automated empirical benchmark evaluation harness.
- `benchmarks/results/`: Definitive empirical measurement records (CER, WER, font MAE, latency).
- `docs/DEMO_PLAN.md`: Live demonstration script, stagecraft runbook, and 5-Layer failover management.

### Secondary Support:
- Architecture governance with Member 3 (Rule Engine) and Member 4 (Backend API).
- Live presentation coaching and technical Q&A defense preparation for the team presenter.

---

## 4. Concrete Responsibilities
1. Set up GitHub Actions CI/CD pipeline on Day 1:
   - Run automated linting (`ruff`), typechecking (`mypy`), and pytest suites on every pull request.
   - Block any PR that fails unit tests or introduces unverified claims.
2. Curate the 35-SKU Physical Packaging Ground-Truth Benchmark Dataset:
   - 10 Snacks & Dry Foods (Parle-G, Lay's, Kurkure, Haldiram, Tata Tea).
   - 8 Personal Care & Cosmetics (Dettol sanitizer, Nivea lotion, Colgate carton, Dove soap).
   - 6 Beverages (Coca-Cola aluminum can, Red Bull, Real juice Tetra Pak).
   - 5 Home Care & Detergents (Surf Excel bar, Harpic, Lizol).
   - 6 Controlled Synthetic Defect Mockups (clearly marked *"Synthetic Test Specimen — Not an Actual Violation"* representing font deficits, missing USP, arithmetic mismatches, and non-metric units).
3. Execute Dual-Instrument Ground-Truth Protocol:
   - Scan every benchmark packaging panel on a flatbed optical scanner at **1200 DPI resolution** ($1\text{ pixel} \equiv 0.02116\text{mm}$).
   - Measure outer packaging dimensions using a digital vernier caliper ($0.01\text{mm}$ resolution) to calculate true PDP area ($A \text{ cm}^2$).
   - Record dual-rater optical pixel heights for Net Quantity and MRP digits; verify inter-rater variance $< 0.04\text{mm}$.
4. Build Automated Benchmark Evaluation Harness:
   - Write `tests/benchmarks/test_benchmark_suite.py`: run the complete MetroLens pipeline across all 35 SKUs; compute Character Error Rate (CER), Word Error Rate (WER), scale factor error ($S$), font height MAE, and statutory compliance accuracy.
   - Record measured values in `benchmarks/results/summary.json`; strictly enforce: **Zero Invented Metrics**.
5. Build Multi-Stage Production Dockerfile:
   - Stage 1 (Builder): Compile dependencies, install ONNX Runtime CPU wheels.
   - Stage 2 (Runner): Lightweight Python slim image; run as non-root user (`appuser:10001`); verify container boots in $< 10\text{s}$.
6. Rehearse & Enforce the 5-Layer Live Demo Failover:
   - Layer 1: 100% offline localhost execution on `127.0.0.1:8000` with OS Wi-Fi toggled OFF.
   - Layer 2: Pre-captured 10-SKU demo sample dropdown in frontend navigation bar.
   - Layer 3: Manual 2-point caliper scale override on canvas.
   - Layer 4: Static pre-rendered HTML/JSON dashboard (canned mode).
   - Layer 5: 4K uncut backup video walkthrough stored on smartphone and USB drive.
7. Manage physical demonstration props: defective packaging specimen, compliant packaging specimen, RBI standard 10-Rupee coin, ISO ATM card, and physical digital vernier caliper.

---

## 5. What Member 6 Must NOT Own ("Not My Job")
- **NOT MY JOB:** Writing OCR neural model inference code (owned strictly by Member 1).
- **NOT MY JOB:** Implementing OpenCV contour or homography unwarping math (owned strictly by Member 2).
- **NOT MY JOB:** Codifying statutory legal rules or regex normalizers (owned strictly by Member 3).
- **NOT MY JOB:** Building React frontend components or CSS layouts (owned strictly by Member 5).
- **NOT MY JOB:** Becoming the default dumping ground for unfinished application code from other teammates.

---

## 6. Inputs Received
- **From Member 1 (OCR):** `packages/ocr/` engine and token extraction outputs.
- **From Member 2 (CV/Calib):** `packages/calibration/` and `packages/vision/` scale outputs.
- **From Member 3 (Rules):** `packages/rules-engine/` statutory state machine.
- **From Member 4 (Backend):** `apps/api/` FastAPI endpoints and Docker requirements.
- **From Member 5 (Web UI):** `apps/web/` production build bundle.

---

## 7. Concrete Outputs Delivered
- `infra/Dockerfile` & `docker-compose.yml`: Working containerized deployment.
- `.github/workflows/ci.yml`: Automated CI pipeline gating all PRs.
- `data/ground_truth/`: 35-SKU physical packaging dataset with 1200 DPI scans.
- `data/manifests/ground_truth_benchmark.json`: Machine-readable ground-truth database.
- `benchmarks/results/`: Formal empirical accuracy report (CER $<6.0\%$, Font MAE $<0.15\text{mm}$).
- Physical demo prop kit & 4K backup demonstration video.

---

## 8. Dependencies & Fallbacks

| Dependency | From Whom | Why Needed | When Needed | Fallback Strategy if Delayed |
| :--- | :--- | :--- | :--- | :--- |
| **Physical Packaging SKUs** | Local Stores | Sourcing 35 real retail commodities | Day 1–2 | Team members bring packaging from home kitchens/pantries. |
| **Flatbed Scanner Access** | University/Shop| 1200 DPI optical scanning for ground truth | Day 2, 4:00 PM | Use macro camera lens on stable tripod with printed millimeter grid. |
| **Integrated Pipeline** | Member 4 | Running end-to-end benchmark harness | Day 5, 2:00 PM | Run component benchmarks on OCR and Calibration in isolation. |

---

## 9. Day-by-Day Execution Plan

### DAY 1: CI/CD Pipeline Setup & Phase 1 Physical SKU Collection
- **Goal:** Establish automated CI/CD gating and acquire first 15 physical retail packages.
- **Tasks:** Author `.github/workflows/ci.yml` (linting, typechecking, pytest); verify CI passes on repository; purchase/source first 15 physical retail packages across snacks, personal care, and beverages; verify RBI standard ₹10 coin diameter ($27.0\text{mm}$) with digital caliper.
- **Deliverables:** Operational GitHub Actions CI pipeline and 15 physical packages on desk.
- **Expected Time:** 7 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 1 - T+24h):** CI pipeline automatically runs and reports green on sample PR; 15 packages ready.
- **Risk:** CI runner runs out of memory installing large packages.
- **Fallback:** Cache pip wheels and Node modules in GitHub Actions cache.

### DAY 2: 1200 DPI Optical Scanning & Ground-Truth Annotation
- **Goal:** Produce optical ground truth for Phase 1 smoke dataset (15 SKUs).
- **Tasks:** Scan packaging panels at 1200 DPI flatbed resolution; measure outer carton dimensions using digital caliper; calculate PDP area ($A \text{ cm}^2$); measure true numeral pixel heights with optical reticle; record values in `ground_truth_benchmark.json`.
- **Deliverables:** Phase 1 ground-truth dataset in `data/ground_truth/` and verified manifest.
- **Expected Time:** 7 hours.
- **Dependencies:** Flatbed scanner access.
- **Checkpoint (Gate 2 - T+48h):** Ground truth established for 15 SKUs with inter-rater variance $< 0.04\text{mm}$.
- **Risk:** Scanner glass glare on reflective foil pouches.
- **Fallback:** Place anti-reflective black matte card backing behind flexible pouches.

### DAY 3: Phase 2 SKU Collection (35 Total) & Synthetic Defect Production
- **Goal:** Complete sourcing of 35 physical SKUs and print 6 synthetic defect sleeves.
- **Tasks:** Source remaining 20 packaging SKUs (bringing total to 35); design and print 6 high-precision synthetic defect mockups (font deficit, missing USP, wrong units, missing tax qualifier) clearly labeled *"Synthetic Test Specimen"*; scan all 20 new SKUs at 1200 DPI.
- **Deliverables:** Complete 35-SKU physical collection and synthetic defect sleeves.
- **Expected Time:** 8 hours.
- **Dependencies:** Office laser printer for synthetic sleeves.
- **Checkpoint (Gate 3 - Day 3):** Full 35-SKU physical packaging collection cataloged in repository.
- **Risk:** Printing resolution on synthetic sleeves deviates from target numeral height.
- **Fallback:** Verify printed synthetic numerals with flatbed scan; record actual printed height in ground truth.

### DAY 4: Dual-Rater Measurement Protocol & Manifest Verification
- **Goal:** Complete dual-rater verification of font heights across all 35 SKUs.
- **Tasks:** Conduct independent optical measurements (Rater 1 and Rater 2) on all 35 packages; average measurements where variance $< 0.04\text{mm}$; finalize `data/manifests/ground_truth_benchmark.json`; write validation script `scripts/verification/verify_dataset_manifest.py`.
- **Deliverables:** Complete, auditable ground-truth database.
- **Expected Time:** 6 hours.
- **Dependencies:** Dual team member availability.
- **Checkpoint (Gate 4 - Day 4):** Manifest verification script passes with 100% integrity.
- **Risk:** Discrepancies between rater measurements on dot-matrix dates.
- **Fallback:** Average 5 independent character stroke measurements.

### DAY 5: Automated Empirical Benchmark Evaluation Harness
- **Goal:** Build automated test harness to evaluate full pipeline accuracy.
- **Tasks:** Write `tests/benchmarks/test_benchmark_suite.py`: execute pipeline against all 35 SKUs; compute Character Error Rate (Levenshtein distance), Word Error Rate, Scale Factor error, and Numeral Height MAE; format results in markdown and JSON.
- **Deliverables:** Working benchmark harness ready to execute on live system.
- **Expected Time:** 7 hours.
- **Dependencies:** Integrated pipeline from Member 4.
- **Checkpoint (Gate 5 - Day 5):** Benchmark suite executes end-to-end on test fixtures.
- **Risk:** Benchmark harness crashes on individual image parsing failure.
- **Fallback:** Wrap individual SKU executions in try/except; log failures and continue evaluation.

### DAY 6: Formal 35-SKU Benchmark Execution & Result Locking
- **Goal:** Execute formal benchmark on demonstrator laptop and lock results.
- **Tasks:** Run `python -m pytest tests/benchmarks/test_benchmark_suite.py` on target hardware; verify $\text{CER} < 6.0\%$, Scale Error $< 5.0\%$, Font MAE $< 0.15\text{mm}$, and Latency $< 2.5\text{s}$; generate `benchmarks/results/summary.json`; lock results.
- **Deliverables:** Official empirical benchmark report; zero fabricated numbers.
- **Expected Time:** 6 hours.
- **Dependencies:** Feature-complete software from M1–M5.
- **Checkpoint (Gate 6):** Formal benchmark passes all acceptance criteria on real hardware.
- **Risk:** Benchmark exposes accuracy deficit on small pouches.
- **Fallback:** Pair with M1 (OCR) and M2 (CV) to tune contrast filters before locking.

### DAY 7: Multi-Stage Docker Build & 5-Layer Demo Failover Rehearsal
- **Goal:** Deliver production Docker container and rehearse demo failovers.
- **Tasks:** Build multi-stage `infra/Dockerfile`; verify image boots clean in $< 10\text{s}$; test Layer 1 (100% offline localhost with Wi-Fi disabled in OS); test Layer 2 (Sample package dropdown); record Layer 5 (4K uncut backup video walkthrough).
- **Deliverables:** Production Docker image, passing offline drill, and 4K backup video.
- **Expected Time:** 7 hours.
- **Dependencies:** Frontend build from Member 5.
- **Checkpoint (Gate 7):** Full demonstration operates flawlessly with Wi-Fi switched off.
- **Risk:** Docker container image size exceeds 2GB.
- **Fallback:** Use Python Alpine/Slim base image and strip development dependencies.

### DAY 8: Final Presentation Freeze & Jury Q&A Drills
- **Goal:** Lock all systems; conduct rigorous jury evaluation drills.
- **Tasks:** Enforce absolute git branch freeze; pack physical props kit (defective pack, compliant pack, coin, card, caliper); conduct 5 full 3-minute pitch rehearsals with tough technical jury cross-examination.
- **Deliverables:** Frozen repository, packed demonstration kit, and presentation slides.
- **Expected Time:** 5 hours.
- **Dependencies:** None.
- **Checkpoint (Gate 8):** Entire team passes 10-question technical jury grill without hesitation.

### DAY 9: Buffer Day & Competition Stage Execution
- **Goal:** Execute winning demonstration on hackathon stage.
- **Tasks:** Set up demo hardware on jury table 15 minutes before pitch; place props in exact script positions; manage backup USB video; support presenter during technical Q&A.
- **Expected Time:** Competition day execution.

---

## 10. Checkpoints & Verification Gates

| Checkpoint | Timing | What Must Exist | How We Know It Works | What Happens if It Fails |
| :--- | :--- | :--- | :--- | :--- |
| **CP-0** | Hour 0 | Git repository & CI initialized | GitHub Actions workflow file created | Commit CI workflow |
| **CP-1** | T+24h | CI passes; 15 SKUs sourced | PR triggers automated test run | Fix CI runner environment |
| **CP-2** | T+48h | 15 SKUs scanned at 1200 DPI | High-res scan TIFF/PNG files in `data/` | Re-scan blurry panels |
| **CP-3** | Day 3 | 35 SKUs + synthetic defects ready | All 35 packages cataloged on desk | Print defect mockups |
| **CP-4** | Day 4 | Ground-truth manifest verified | `verify_dataset_manifest.py` passes | Re-measure outlier dimensions |
| **CP-5** | Day 5 | Benchmark harness operational | Runs across sample fixtures | Debug harness metrics code |
| **CP-6** | Day 6 | 35-SKU benchmark locked | $\text{CER} < 6\%$, $\text{MAE} < 0.15\text{mm}$ documented | Pair with M1/M2 to tune |
| **CP-7** | Day 7 | 5-Layer failover drill passes | Demo runs with Wi-Fi switched OFF | Fix offline asset bundling |
| **CP-8** | Day 8 | Final freeze & props packed | Caliper, coin, packs, video on USB ready | Final stage checklist sign-off |

---

## 11. Acceptance Criteria & Test Evidence

| Deliverable | Acceptance Criteria | Test Command | Concrete Evidence |
| :--- | :--- | :--- | :--- |
| **CI/CD Pipeline** | All PRs automatically linted, typechecked, tested | GitHub Actions CI run | Green checkmark badge on repository |
| **Ground Truth** | 35 SKUs annotated with dual-rater variance $<0.04\text{mm}$ | `python scripts/verification/verify_dataset_manifest.py`| Verification script terminal report: SUCCESS |
| **Benchmark Suite** | Measures CER $<6.0\%$, Font MAE $<0.15\text{mm}$ | `pytest tests/benchmarks/test_benchmark_suite.py` | Official `summary.json` with empirical metrics |
| **Docker Build** | Multi-stage container boots in $<10\text{s}$ on port 8000 | `docker-compose up -d` | Clean container startup log; health check returns 200 |
| **Offline Failover** | Full demo executes with OS network adapter disabled | Manual offline test | Screencast showing inspection executing with airplane mode active |

---

## 12. Testing Responsibility
- **CI Pipeline:** Automated execution of all unit, integration, and rule tests on GitHub Actions.
- **Benchmark Suite:** Automated execution of empirical accuracy metrics on target hardware.
- **Security Fuzzing:** Automated upload testing of malformed, huge, and non-image payloads with Member 4.
- **Demo Redundancy Testing:** Verification of all 5 failover layers under simulated hardware/network crashes.

---

## 13. Handoff Protocol & Checklist

### Handoff to Entire Team & Presenter:
1. **Benchmark Results:** Documented in `benchmarks/results/summary.json` and presentation slides.
2. **Container Artifact:** Production Docker image tag `metrolens-ai:v1.0.0`.
3. **Demo Props Kit:**
   - [ ] Defective synthetic biscuit package (Net Qty printed at 1.15mm).
   - [ ] Compliant Dettol / Colgate retail package.
   - [ ] Uncirculated RBI standard 10-Rupee coin (27.0mm).
   - [ ] Standard ISO ATM card (85.60 x 53.98mm).
   - [ ] Mitutoyo / calibrated digital vernier caliper ($0.01\text{mm}$ precision).
   - [ ] USB thumb drive containing 4K backup demonstration video.
4. **Usage Instructions:**
   ```bash
   # Run full benchmark evaluation
   python -m pytest tests/benchmarks/test_benchmark_suite.py -v
   ```
5. **Test Evidence:** Signed-off benchmark report and clean CI build history.

---

## 14. Escalation Conditions
- **Blocked for 30 minutes:** CI workflow failure on environment configuration $\rightarrow$ Fix Docker base image.
- **Blocked for 2 hours:** Cannot locate flatbed optical scanner $\rightarrow$ Use tripod DSLR/macro camera setup with calibration grid.
- **Blocked for half-day:** Benchmark Character Error Rate exceeds $10\%$ $\rightarrow$ Call urgent engineering sync with Member 1 (OCR) and Member 2 (CV) to adjust preprocessing parameters.

---

## 15. Risk Table

| Risk | Prob | Impact | Trigger | Mitigation | Fallback |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **Venue Wi-Fi Dead** | High | High | Network timeout on stage | 100% offline localhost architecture | Run demo with Wi-Fi switched OFF in OS |
| **Benchmark Metrics Challenged** | Low | High | Judge asks for proof of CER | Produce 1200 DPI scan ground-truth manifest | Invite judge to measure package with vernier caliper |
| **Docker Build Too Slow** | Med | Med | Build time $>10\text{ minutes}$ | Multi-stage caching; pre-download model weights | Run locally via native Python virtualenv |
| **Synthetic Label Challenged** | Low | Med | Brand defamation concern | Clearly label: "Synthetic Test Specimen — Not Actual Violation" | Display on-screen ethics disclaimer |

---

## 16. Daily Report Format (< 5 Minutes)
```text
MEMBER 6 DAILY STATUS (DATE: ________)
• DONE: [Data collected, benchmarks run, CI/Docker status]
• BLOCKED: [Any hardware, scanning, or deployment blockers]
• TESTED: [Benchmark numbers / CI pass status]
• NEXT: [Tomorrow's QA/integration milestone]
• RISK: [Any demo failover or hardware vulnerability]
```

---

## 17. Definition of Done (DoD)
A task is DONE when:
1. Docker container builds cleanly and boots in $< 10\text{s}$.
2. Automated CI passes on all PRs with zero test failures.
3. 35-SKU ground-truth dataset is curated, scanned at 1200 DPI, and documented.
4. Benchmark script measures and records empirical accuracy on real hardware.
5. All 5 demo failover layers are verified and physical props are packed.

---

## 18. AI Coding Workflow
$$\text{PLAN (Define Benchmark Schema)} \longrightarrow \text{PROMPT AI (Pytest Harness)} \longrightarrow \text{REVIEW (Zero Hardcoded Metrics)} \longrightarrow \text{RUN \& TEST} \longrightarrow \text{VERIFY} \longrightarrow \text{HANDOFF}$$
- **AI CAN DO:** Write pytest benchmark harnesses, Dockerfile multi-stage syntax, and GitHub Actions YAML.
- **MEMBER MUST DECIDE:** Physical measurement ground truth, accuracy acceptance thresholds, demo failover triggers, and stage props.

---

## 19. Buffer Work
- **Primary:** CI/CD pipeline, 35-SKU ground-truth dataset, benchmark harness, Docker container, 5-layer demo failover.
- **Buffer Task 1:** Expand benchmark dataset from 35 to 50 physical SKUs across secondary categories.
- **Buffer Task 2:** Build automated performance regression graph generator visualizing latency across commits.
