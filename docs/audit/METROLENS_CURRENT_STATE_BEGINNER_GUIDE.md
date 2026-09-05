# MetroLens AI — Current State Beginner & Refresher Guide
**Audience:** A developer or teammate who has lost context, hasn't touched the repository for a few days, and needs to understand exactly where everything stands in 10 minutes.  
**Audit Baseline Date:** 2026-09-05

---

## 1. In One Sentence...
MetroLens AI is a planned automated compliance inspection web application for Indian packaged commodity labels where **currently only the OCR text extraction engine actually works**, while the computer vision calibration, legal rule logic, backend API, and web interface remain as scaffolded skeletons.

---

## 2. In Simple Terms...
The project’s goal is to let a regulatory officer take a smartphone photo of a product package (like a bag of chips or a bottle of oil) with a ₹10 coin placed next to it. The system is supposed to:
1. Check if the photo is sharp and glare-free.
2. Find the ₹10 coin to figure out the exact physical scale (how many millimeters per pixel).
3. Read all the printed text in English and Hindi.
4. Measure the physical height of the printed numbers (e.g. MRP and Net Weight) to ensure they meet the minimum legal height (e.g. at least 2mm or 4mm depending on package size).
5. Check if all required declarations (MRP, Net Qty, Dates, Manufacturer, Consumer Care) are present and legally formatted.
6. Generate a signed PDF legal dossier proving whether the package passed or failed.

**Right now, only Step 3 (reading the text) is actually built and working.** The rest of the steps are empty placeholder functions returning fake or hardcoded values. Furthermore, the system has only been tested on 8 computer-generated sample images; zero photos of real store-bought products have been uploaded or tested yet.

---

## 3. The System Currently Does...
- **Detects text boxes:** Takes an image and finds rotated text lines using a lightweight DBNet++ ONNX neural network in ~30 milliseconds.
- **Reads English and Hindi text:** Routes text crops to either an English SVTR model or a Hindi Devanagari SVTR model and transcribes characters accurately in ~80 milliseconds.
- **Runs 100% locally on CPU:** Uses Direct ONNX Runtime without requiring a GPU, Docker, external cloud APIs, or an internet connection.
- **Provides a clean Python Service:** You can call `OCRService.get_instance().extract_observations("path/to/image.png")` in Python and get structured tokens with bounding box coordinates.
- **Passes 89 automated tests:** The test suite runs in ~21 seconds via `python -m pytest` with 100% pass rate.

---

## 4. The System Currently Does NOT Do...
- **It does NOT detect coins or calibrate scale:** It cannot look at a coin in an image and calculate the millimeters per pixel.
- **It does NOT unwarp tilted packages:** There is no perspective correction code yet.
- **It does NOT measure legal font heights:** It cannot convert OCR bounding boxes into typographic millimeter heights.
- **It does NOT check Indian packaging law:** The rule engine only checks if an "MRP" string was found; it does not check Net Quantity, Dates, Manufacturer, Unit Sale Price arithmetic, or Rule 7 height tables.
- **It does NOT run through the web:** The FastAPI backend returns a hardcoded fake success JSON response without calling the OCR, and the Next.js frontend is a static page with no upload button.
- **It does NOT generate real legal PDF reports:** The PDF generator only writes 5 lines of plain text.
- **It has NOT been proven on real physical packaging:** There are 0 real packaging photos on disk.

---

## 5. Here Is What Each Folder Means...
- **`packages/ocr/`:** **The real engine.** This is where 90% of the actual working code lives. Contains models, detectors, recognizers, and the `OCRService`.
- **`packages/shared/`:** **The contracts.** Defines the standardized data formats (like `OCRObservation` and `InspectionResult`) that all packages use to talk to each other.
- **`packages/calibration/`, `vision/`, `measurement/`, `rules-engine/`, `reporting/`:** **The scaffolds.** Empty skeleton folders with 30-to-70-line placeholder files waiting for implementation.
- **`apps/api/`:** **The backend server.** FastAPI app. Currently returns hardcoded mock data.
- **`apps/web/`:** **The frontend website.** Next.js app. Currently a single page of static text.
- **`models/weights/ocr/`:** **The AI brains.** Real ONNX neural network weight files (22 MB total) used by the OCR engine.
- **`data/synthetic/`:** **The test data.** 8 computer-generated package images used for testing.
- **`data/raw/real/`:** **The missing data.** Currently completely empty. Real photos must be placed here.
- **`METROLENS_LEGAL_SOURCE_PACK/`:** **The sovereign legal authority.** 74 real Indian government Gazette and Act PDFs collected for legal reference.
- **`docs/`:** **The blueprint library.** 120+ markdown files describing the target vision. Very thorough, but describes what the project *wants to be*, not what it *currently is*.
- **`CURRENT_STATE/`:** **The progress tracker.** Check `PROJECT_SNAPSHOT.md` to see the latest verified chunk status.

---

## 6. Here Is What Each Member Currently Owns...
- **Member 1 (AI & OCR):** `packages/ocr/`. **Has completed Chunks 1 through 4.** Engine is built, fast (~109ms), and tested.
- **Member 2 (CV & Calibration):** `packages/vision/`, `packages/calibration/`, `packages/measurement/`. Needs to write the code that finds the ₹10 coin and calculates font heights in millimeters.
- **Member 3 (Legal Rules):** `packages/rules-engine/`, `packages/extraction/`. Needs to write the regexes that parse mandatory fields and the state machine that evaluates legal rules.
- **Member 4 (Backend API & PDF):** `apps/api/`, `packages/reporting/`. Needs to connect the FastAPI routes to Member 1's `OCRService` and Member 3's rules engine.
- **Member 5 (Frontend Web UX):** `apps/web/`. Needs to build the interactive upload page, bounding-box display canvas, and compliance dashboard.
- **Member 6 (Data, QA & CI):** `data/`, `infra/`, `.github/`. Needs to collect 35 real store-bought packaging items, photograph them, and put them in `data/raw/real/`.

---

## 7. Here Is How the Pieces Connect...

```
[User Image]
     │
     ▼
[Quality Gate (Member 2 - Scaffold)]  ──> Checks blur & glare
     │
     ▼
[Optical Calibration (Member 2 - Scaffold)]  ──> Finds ₹10 coin (mm/pixel)
     │
     ▼
[OCR Perception Engine (Member 1 - COMPLETE)]  ──> Reads English & Hindi text
     │
     ▼
[Semantic Extractor (Member 3 - Scaffold)]  ──> Extracts MRP, Net Qty, Dates
     │
     ▼
[Measurement Engine (Member 2 - Scaffold)]  ──> Computes font height in mm
     │
     ▼
[Legal Rules Engine (Member 3 - Scaffold)]  ──> Checks compliance vs Law
     │
     ▼
[Dossier Reporter (Member 4 - Scaffold)]  ──> Generates PDF Dossier
     │
     ▼
[FastAPI / Web UI (Members 4 & 5 - Scaffold)]  ──> Displays verdict to Officer
```
*Note: In the code today, only the OCR Perception box is fully operational.*

---

## 8. Here Is Where We Currently Are...
- **Chunk 4 was completed by Member 1.** The OCR engine was cleanly packaged into the monorepo, wrapped in a thread-safe service adapter, and verified with 89 passing tests.
- **We are ready for Chunk 5.** The immediate next step is for Member 4 to wire Member 1's `OCRService` into the FastAPI backend so that real images can be uploaded and processed, while Member 6 begins collecting physical packaging photos.
