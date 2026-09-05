# MetroLens AI — Actionable Next-Steps Map
**Audit Baseline Date:** 2026-09-05  
**Guiding Principle:** Practical, evidence-based engineering tasks directly addressing current blockers. No theoretical roadmaps.

---

## 1. Concrete Engineering Execution Sequence

### Step 1: Wire Member 1's OCRService into the FastAPI Backend
- **Current Blocker:** `apps/api/main.py` returns hardcoded dummy JSON and ignores uploaded images (Blocker 4).
- **Next Task:** Update `apps/api/main.py` to import `OCRService.get_instance()` from `nirikshak_ocr.service`. In the `submit_inspection` route, accept an uploaded image file (via `UploadFile`), pass raw image bytes to `OCRService.extract_observations(bytes)`, and populate the `InspectionResult` with genuine `OCRObservation` tokens and image SHA-256 digest.
- **Owner:** **Member 4 (Backend)**.
- **Dependencies:** `packages/ocr/` (Already complete and verified).
- **Expected Result:** Calling `curl -F "image=@sample.png" http://localhost:8000/api/v1/inspections` returns real OCR bounding boxes and recognized text tokens in $<200$ms.

---

### Step 2: Unblock Real Packaging Data Collection (Path B Gate)
- **Current Blocker:** Zero real physical packaging images exist on disk (`data/raw/real/` is empty) (Blocker 1).
- **Next Task:** Physically purchase 35 packaged FMCG commodity items (e.g. Haldiram snacks, Tata Salt, Maggi noodles, shampoo sachet, Parle-G biscuits, Dabur honey, soft drink can). Place each item on a flat surface with a standard ₹10 coin adjacent to the declaration panel. Photograph each item in good lighting with a smartphone (1080p/12MP). Deposit photos into `data/raw/real/` and update `data/manifests/real_packaging_manifest.json`.
- **Owner:** **Member 6 (Data & QA)** with support from Member 2.
- **Dependencies:** Physical store visit and camera.
- **Expected Result:** 35 authentic packaging images present in `data/raw/real/`, unlocking real-world OCR accuracy benchmarking and optical coin calibration testing.

---

### Step 3: Implement Computer Vision ₹10 Coin Anchor Detection
- **Current Blocker:** Calibration package has only a division math stub and cannot compute scale from an image (Blocker 2).
- **Next Task:** Create `packages/calibration/src/nirikshak_calibration/anchor_detector.py`. Implement circular Hough transform (`cv2.HoughCircles`) or color/contour thresholding and ellipse fitting (`cv2.fitEllipse`) to locate the standard RBI ₹10 coin (known diameter $27.0\text{mm}$). Compute the metric scale factor:
  $$S = \frac{27.0\text{ mm}}{\text{measured major diameter in pixels}}$$
- **Owner:** **Member 2 (Computer Vision & Calibration)**.
- **Dependencies:** OpenCV (`cv2`), sample images with ₹10 coin (from Step 2).
- **Expected Result:** Calling `detect_coin_scale(image)` returns calibrated millimeters-per-pixel scale factor with status `CALIBRATED`.

---

### Step 4: Implement Mandatory Field Normalizer & Rule 6 Evaluations
- **Current Blocker:** Extraction package parses only MRP; rule engine evaluates only 1 rule (Blocker 3).
- **Next Task:**
  1. Expand `packages/extraction/src/nirikshak_extraction/__init__.py` to parse Net Quantity (e.g., `Net Wt: 200g`, `500 ml`), Manufacturing Date (`Mfg: MM/YYYY`), and Consumer Care contact details using deterministic regexes.
  2. Expand `packages/rules-engine/src/nirikshak_rules_engine/__init__.py` to evaluate presence of all extracted fields against Rule 6(1)(a)-(h), compute Unit Sale Price ($\text{MRP} / \text{NetQty}$), and return a composite `COMPLIANT` or `NON_COMPLIANT` verdict.
- **Owner:** **Member 3 (Legal Rules Engine)**.
- **Dependencies:** `OCRObservation` tokens from Member 1.
- **Expected Result:** Passing OCR tokens to `NirikshakRulesEngine.evaluate()` produces structured evaluations for MRP, Net Qty, and Unit Sale Price.

---

### Step 5: Build Interactive Upload & Bounding-Box Overlay in Frontend
- **Current Blocker:** `apps/web/` is a static placeholder page with zero interactivity and no dependencies installed (Blocker 5).
- **Next Task:**
  1. Run `npm install` in `apps/web/`.
  2. Implement an image drag-and-drop component on `page.tsx` that uploads the selected image to `http://localhost:8000/api/v1/inspections`.
  3. Render the uploaded image on an HTML `<canvas>` and draw green/red bounding-box rectangles around the detected text tokens using coordinates returned by the API.
  4. Display an executive badge showing the overall compliance verdict.
- **Owner:** **Member 5 (Frontend Engineering)**.
- **Dependencies:** Member 4's working API (from Step 1).
- **Expected Result:** A user can open `http://localhost:3000`, drag-and-drop an image of a package, see text boxes highlighted over the photo, and see an instant compliance verdict.

---

### Step 6: Create Automated GitHub Actions CI Workflow
- **Current Blocker:** `.github/workflows/` does not exist; pull requests are untested in GitHub (Blocker 6).
- **Next Task:** Create `.github/workflows/ci.yml` configuring a workflow on `ubuntu-latest` running Python 3.11/3.12, installing dependencies from `requirements.txt`, and executing `pytest tests/ packages/ apps/`.
- **Owner:** **Member 6 (Release & CI)**.
- **Dependencies:** None.
- **Expected Result:** Automated CI check runs and passes on every Git push and pull request.
