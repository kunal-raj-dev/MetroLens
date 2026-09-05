# MetroLens AI — Active Project Blockers
**Audit Baseline Date:** 2026-09-05  
**Evaluation Standard:** Objective Verification of Current Pipeline State  
**Rule:** Only real blockers supported by repository evidence are listed.

---

## 1. Active Blocker Registry

### Blocker 1: Path B Data Blocker (Zero Real Packaging Images on Disk)
- **Evidence:** `data/raw/real/` contains 0 files. `data/manifests/real_packaging_manifest.json` line 8 specifies `"status": "BLOCKED_AWAITING_PHYSICAL_DATA_COLLECTION"`.
- **Owner:** Member 6 (Product, Benchmark & Release Lead).
- **Dependent Work:**
  - Member 1 cannot evaluate real-world packaging Character Error Rate (CER) or test dot-matrix font degradation.
  - Member 2 cannot validate optical coin detection, tilt angles, or glare filtering on physical retail packages.
  - Member 6 cannot run the official 35-SKU empirical benchmark.
  - Live hackathon demo lacks authentic Indian retail packaging specimens.
- **Severity:** **CRITICAL**.
- **Can It Be Removed?** YES.
- **What Is Required?** Member 6 must physically acquire 35 packaged commodity items across target FMCG categories (food snacks, beverages, personal care, staples), photograph them with a smartphone alongside a standard ₹10 coin or ruler, and deposit them into `data/raw/real/`.

---

### Blocker 2: Optical Calibration Anchor Detection Missing (No Coin / Card Finding)
- **Evidence:** `packages/calibration/src/nirikshak_calibration/__init__.py` contains only a 67-line stub (`compute_scale_factor`) that divides two float numbers. Planned module `anchor_detector.py` does not exist.
- **Owner:** Member 2 (Computer Vision, Calibration & Measurement Lead).
- **Dependent Work:**
  - System cannot compute the physical scale factor ($S$ in mm/pixel) directly from an uploaded camera photo.
  - Member 2 cannot supply calibrated font heights ($h_{\text{mm}}$) to Member 3.
  - Member 3 cannot evaluate Rule 7 font-to-area minimum height compliance.
- **Severity:** **CRITICAL**.
- **Can It Be Removed?** YES.
- **What Is Required?** Member 2 must implement computer vision contour detection and ellipse fitting (e.g., using `cv2.findContours` and `cv2.fitEllipse`) to detect the circular ₹10 coin ($27.0\text{mm}$) in the input image and return the calibrated scale factor in millimeters per pixel.

---

### Blocker 3: Legal Rule Engine & Field Normalizer Missing
- **Evidence:** `packages/rules-engine/src/nirikshak_rules_engine/__init__.py` (39 lines) evaluates only one rule (`LMPC-R06-MRP-001`). `packages/extraction/` (47 lines) parses only MRP amount.
- **Owner:** Member 3 (Legal Rules, Domain Logic & Compliance Engine Lead).
- **Dependent Work:**
  - System cannot parse net quantity, dates, manufacturer, or consumer care details.
  - System cannot evaluate mandatory declaration presence under Rule 6(1)(a)-(d),(f)-(h).
  - System cannot calculate Unit Sale Price (USP) arithmetic under Rule 6(11).
  - System cannot produce a composite 5-State compliance verdict.
  - Member 4 cannot return a real statutory compliance outcome from the API.
- **Severity:** **CRITICAL**.
- **Can It Be Removed?** YES.
- **What Is Required?** Member 3 must implement regex entity normalizers for the remaining 5 mandatory declarations in `packages/extraction/` and encode the statutory evaluation rules and composite verdict state machine in `packages/rules-engine/`.

---

### Blocker 4: Backend API Disconnected from OCR & Processing Pipeline
- **Evidence:** `apps/api/main.py` lines 39–51 return a hardcoded `InspectionResult` without importing or invoking `nirikshak_ocr.OCRService`, `nirikshak_vision`, or `nirikshak_rules_engine`.
- **Owner:** Member 4 (Backend API Gateway & PDF Reporting Lead).
- **Dependent Work:**
  - Frontend uploads receive static mock data regardless of what image is uploaded.
  - End-to-end integration cannot function.
  - The working OCR engine cannot be exercised through HTTP.
- **Severity:** **HIGH**.
- **Can It Be Removed?** YES (Immediately).
- **What Is Required?** Member 4 must import `OCRService.get_instance()` from `nirikshak_ocr.service` in `apps/api/main.py`, decode the incoming image payload, call `extract_observations()`, pass observations to `nirikshak_rules_engine`, and return the populated `InspectionResult`.

---

### Blocker 5: Frontend Web UI Lacks Interactive Components & Dependencies
- **Evidence:** `apps/web/src/app/page.tsx` is a 40-line static text page. Planned components (`ImageUploadZone.tsx`, `EvidenceCanvas.tsx`, `ComplianceDashboard.tsx`) do not exist. `node_modules` does not exist on disk.
- **Owner:** Member 5 (Frontend Engineering & Web User Experience Lead).
- **Dependent Work:**
  - No graphical user interface exists for testing or presenting the application to evaluators.
  - Uploading packaging photos requires raw curl commands or Python scripts.
- **Severity:** **HIGH**.
- **Can It Be Removed?** YES.
- **What Is Required?** Member 5 must run `npm install` in `apps/web/`, implement a drag-and-drop file upload component that sends a `POST` request to `http://localhost:8000/api/v1/inspections`, and render an image overlay displaying the returned bounding boxes and compliance status.

---

### Blocker 6: CI Pipeline Unimplemented
- **Evidence:** `.github/workflows/` directory does not exist on disk.
- **Owner:** Member 6 (Product Integration, QA & Release Lead).
- **Dependent Work:**
  - Pull requests and commits are not automatically tested or linted in GitHub.
  - Risk of regression breaks when members merge code.
- **Severity:** **MEDIUM**.
- **Can It Be Removed?** YES.
- **What Is Required?** Member 6 must create `.github/workflows/ci.yml` running `python -m pytest` and code linting on pushes.
