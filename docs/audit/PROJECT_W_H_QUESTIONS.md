# MetroLens AI — Project W/H Questions Ground-Truth Guide
**Audit Baseline Date:** 2026-09-05  
**Core Purpose:** Answer all foundational engineering questions using strictly verified repository evidence.

---

## 1. Ground-Truth Answers

### WHAT: What is MetroLens AI?
MetroLens AI (also referenced historically in some documents as *MetroSetu* and code-named *Nirikshak*) is an automated, AI-assisted packaged commodity inspection and compliance assessment system designed to verify that consumer product labels in India conform to the *Legal Metrology (Packaged Commodities) Rules, 2011* and the *Legal Metrology Act, 2009* (incorporating the *Jan Vishwas Act, 2026*). In its current software reality, it is a Python monorepo featuring a high-speed, local CPU-based multilingual OCR perception engine with scaffolded outlines for computer vision calibration, legal rule evaluation, API services, and web UI.

### WHY: Why does this repository exist?
The repository was established to solve Problem Statement **SIH26034** for the Ministry of Consumer Affairs, Food and Public Distribution at the Smart India Hackathon (SIH). The objective is to replace slow, error-prone manual physical inspections by legal metrology officers with an automated tool that extracts mandatory declarations (MRP, net quantity, manufacturing dates, consumer care), converts pixel dimensions to physical millimeters using optical calibration, evaluates statutory compliance deterministically, and issues auditable inspection dossiers.

### WHO: Who uses it, and who owns each subsystem?
- **Intended End Users:** Legal Metrology Officers, consumer protection authorities, retail compliance auditors, and e-commerce marketplace compliance managers.
- **Engineering Team Ownership (6 Members):**
  - **Member 1:** AI & Multilingual OCR Lead (`packages/ocr/`).
  - **Member 2:** Computer Vision, Calibration & Physical Measurement Lead (`packages/vision/`, `packages/calibration/`, `packages/measurement/`).
  - **Member 3:** Legal Rules, Domain Logic & Compliance Engine Lead (`packages/rules-engine/`, `packages/extraction/`).
  - **Member 4:** Backend API Gateway, Upload Security & PDF Reporting Lead (`apps/api/`, `apps/worker/`, `packages/reporting/`).
  - **Member 5:** Frontend Engineering & Web UX Lead (`apps/web/`).
  - **Member 6:** Product Integration, QA, Benchmark & Release Lead (`data/`, `infra/`, `.github/`).

### WHERE: Where is each component?
- **Perception / OCR:** `packages/ocr/src/nirikshak_ocr/`
- **Shared Data Contracts:** `packages/shared/src/nirikshak_shared/models/`
- **Models & Weights:** `models/weights/ocr/`
- **Vision Quality Gate:** `packages/vision/src/nirikshak_vision/`
- **Optical Calibration:** `packages/calibration/src/nirikshak_calibration/`
- **Measurement Logic:** `packages/measurement/src/nirikshak_measurement/`
- **Entity Extraction:** `packages/extraction/src/nirikshak_extraction/`
- **Legal Rule Engine:** `packages/rules-engine/src/nirikshak_rules_engine/`
- **Inspection Dossier Reporting:** `packages/reporting/src/nirikshak_reporting/`
- **Backend API Server:** `apps/api/`
- **Frontend Web UI:** `apps/web/`
- **Authoritative Legal PDFs:** `METROLENS_LEGAL_SOURCE_PACK/`
- **Synthetic Test Data:** `data/synthetic/regression/`
- **Real Packaging Data:** `data/raw/real/` (currently 0 images)

### WHEN: What stage / chunk is actually complete?
- **Chunk 1 (OCR Model Selection):** COMPLETED. Evaluated model options; selected PP-OCRv3.
- **Chunk 2 (OCR Engine Core):** COMPLETED. Built Direct ONNX Runtime engine with DBNet++ and SVTR-EN / SVTR-HI.
- **Chunk 3 (Real Data Audit & Preprocessing):** COMPLETED. Documented real data provenance rules, evaluated 6 preprocessing filters on synthetic images, confirmed `B0_BASELINE_RAW` as production default.
- **Chunk 4 (Monorepo Integration & Service Adapter):** COMPLETED. Packaged monorepo via editable installs, implemented `OCRService` adapter, verified shared contract marshalling, and hardened concurrency safety.
- **Chunk 5 (Pipeline Orchestration & Mounting):** PLANNED / NOT STARTED.

### WHICH: Which files, models, and services are canonical?
- **Canonical Status Reference:** `CURRENT_STATE/PROJECT_SNAPSHOT.md` and `docs/audit/`.
- **Canonical OCR Models:** `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx`, `rec_en/ch_PP-OCRv3_rec_infer.onnx`, and `rec_hi/rec.onnx` (defined in `models/manifest.yaml`).
- **Canonical Legal Source Register:** `regulations/source_registry.yaml` and `METROLENS_LEGAL_SOURCE_PACK/`.
- **Canonical API Entrypoint:** `apps/api/main.py`.
- **Canonical Data Contract:** `packages/shared/src/nirikshak_shared/models/contracts.py`.

### HOW: How does the actual pipeline currently work?
In physical code reality today:
1. Input image (path, bytes, or ndarray) is provided to `nirikshak_ocr.OCRService`.
2. Image is normalized into an RGB numpy array.
3. DBNet++ detects rotated text polygons.
4. Cropped text regions are perspective-rectified.
5. The script router analyzes character glyph distributions and directs crops to either SVTR Latin or SVTR Devanagari.
6. The recognizers decode text strings via greedy CTC.
7. Results are packed into canonical `OCRObservation` DTO objects in ~109ms.
8. **The pipeline halts here.** The API returns mock data; computer vision calibration, full rule evaluations, and PDF dossier generation are unintegrated stubs.

### HOW MUCH: How much is actually implemented and tested?
- **OCR Subsystem:** ~95% implemented, passing 67 dedicated unit/integration tests.
- **Shared Data Models:** 100% implemented, passing 5 contract tests.
- **Test Suite:** 89 automated tests passing (100% repository pass rate).
- **Vision & Calibration:** ~10% implemented (simple math stubs).
- **Rule Engine:** ~10% implemented (1 of 7 core statutory rules).
- **Backend API:** ~15% implemented (scaffold mock routes).
- **Frontend Web UI:** ~5% implemented (static text page).
- **Real Packaging Data:** 0% (0 of 35 targeted real packaging images exist on disk).

### WHAT NEXT: What is the immediate next engineering task?
1. Member 4 must mount `nirikshak_ocr.OCRService` inside `apps/api/main.py` so that `POST /api/v1/inspections` returns genuine text observations from uploaded images.
2. Member 6 must collect authentic retail packaging photos under Path B Gate.
3. Member 2 must implement ₹10 coin anchor detection in `packages/calibration/`.
4. Member 3 must implement regex field extraction and rule logic in `packages/rules-engine/`.

### WHAT FAILED: What has failed or been disproven so far?
- **RapidOCR Third-Party Wrapper:** Failed in early development due to rigid dependencies and path issues; replaced with direct ONNX Runtime.
- **Blanket Full-Image Preprocessing:** Blanket CLAHE on full images degraded detection accuracy and added ~12ms overhead; formally rejected in Chunk 3.
- **Pre-filtering Glare via Blanket Filters:** Failed to improve OCR on synthetic test specimens; raw baseline (`B0_BASELINE_RAW`) proved superior.
- **Celery / Redis Distributed Architecture:** Deemed excessive overhead and latency liability for an 8-day sprint; superseded by in-process local execution.

### WHAT CHANGED: What changed from Chunk 1 to current state?
- Moved from exploratory evaluation of OCR engines to a production-ready, direct ONNX PP-OCRv3 engine.
- Packaged repository into a unified monorepo with `packages/shared` and `packages/ocr` installed via editable pip links.
- Introduced `OCRService` singleton adapter enforcing thread-safe serialized execution.
- Standardized target dataset from 50 SKUs down to a canonical 35-SKU target.

### WHAT REMAINS: What genuinely remains to be built?
- Optical reference coin detection from camera uploads.
- Planar homography perspective correction.
- Regex normalizers for Net Quantity, Dates, Manufacturer, Country of Origin, and Consumer Care.
- Deterministic rule evaluators for Rules 6(1)(a)-(d), 6(11) USP arithmetic, and Rule 7 font-to-area matrix.
- Real API pipeline orchestration.
- Interactive Next.js upload dropzone and bounding-box overlay canvas.
- Real 35-SKU retail packaging data collection and physical caliper measurements.

### WHAT IS DEAD: What is historical or obsolete?
- Distributed Celery/Redis architecture references in early docs.
- Early v0.3 audit notes (`docs/AUDIT_V0_3.md`).
- Historical 50-SKU target declarations in early drafts.
- Initial problem statement dossier scripts (`problem statement #1/scripts/generate_dossier.py`).
