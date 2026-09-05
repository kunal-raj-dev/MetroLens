# MetroLens AI — Feature Completion Matrix
**Audit Baseline Date:** 2026-09-05  
**Evaluation Standard:** Physical Code Reality & Test Evidence  
**Status Taxonomy:** `NOT_STARTED`, `SCAFFOLD`, `PARTIAL`, `IMPLEMENTED`, `TESTED`, `INTEGRATED`, `DEMO_READY`, `BLOCKED`, `UNKNOWN`

---

## 1. Subsystem & Feature Completion Table

| Feature / Capability | Planned? | Code exists? | Tests exist? | Integrated? | Demo-ready? | Real-data validated? | Status | Owner | Evidence / Code Location | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Multilingual Text Detection** | YES | YES | YES | YES | YES | NO (Synthetic only) | **INTEGRATED** | Member 1 | `packages/ocr/src/nirikshak_ocr/detector.py` | DBNet++ direct ONNX inference; 4-point polygon extraction. |
| **Latin/English Recognition** | YES | YES | YES | YES | YES | NO (Synthetic only) | **INTEGRATED** | Member 1 | `packages/ocr/src/nirikshak_ocr/recognizer.py` | SVTR alphanumeric model with greedy CTC decoding. |
| **Devanagari/Hindi Recognition**| YES | YES | YES | YES | YES | NO (Synthetic only) | **INTEGRATED** | Member 1 | `packages/ocr/src/nirikshak_ocr/recognizer.py` | Dedicated SVTR Devanagari model + 167-char dictionary. |
| **Script Routing (EN vs HI)** | YES | YES | YES | YES | YES | NO (Synthetic only) | **INTEGRATED** | Member 1 | `packages/ocr/src/nirikshak_ocr/router.py` | Unicode block density + aspect ratio routing. |
| **Domain Preprocessing Hooks** | YES | YES | YES | YES | YES | NO (Synthetic only) | **INTEGRATED** | Member 1 | `packages/ocr/src/nirikshak_ocr/preprocessing.py` | CLAHE, bilateral, unsharp, dilation; default is raw. |
| **OCR Service Adapter** | YES | YES | YES | YES | YES | NO (Synthetic only) | **INTEGRATED** | Member 1 | `packages/ocr/src/nirikshak_ocr/service.py` | Thread-safe singleton, input normalization, contract marshalling. |
| **Laplacian Blur Detection** | YES | PARTIAL | NO | NO | NO | NO | **SCAFFOLD** | Member 2 | `packages/vision/src/nirikshak_vision/__init__.py` | Calculates variance of raw gray array; no cv2.Laplacian. |
| **Specular Glare Detection** | YES | PARTIAL | NO | NO | NO | NO | **SCAFFOLD** | Member 2 | `packages/vision/src/nirikshak_vision/__init__.py` | Counts pixels >= 250; no HSV color space masking. |
| **₹10 Coin Anchor Detection** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 2 | Planned `packages/calibration/anchor_detector.py` | 0 lines of code on disk. |
| **ISO Card Anchor Detection** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 2 | Planned `packages/calibration/anchor_detector.py` | 0 lines of code on disk. |
| **Metric Scale Factor Math** | YES | YES | YES (Smoke) | NO | NO | NO | **SCAFFOLD** | Member 2 | `packages/calibration/src/nirikshak_calibration/__init__.py` | Simple division function; takes raw pixel input. |
| **Planar Homography (Rectify)**| YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 2 | Planned `packages/calibration/homography.py` | 0 lines of code on disk. |
| **Cylindrical Surface Unwarp** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 2 | Planned `packages/calibration/cylinder.py` | 0 lines of code on disk. |
| **Font Height Conversion (mm)**| YES | YES | YES (Smoke) | NO | NO | NO | **SCAFFOLD** | Member 2 | `packages/measurement/src/nirikshak_measurement/__init__.py` | Multiplies pixel height by scale factor. |
| **PDP Area Calculation ($cm^2$)**| YES | YES | YES (Smoke) | NO | NO | NO | **SCAFFOLD** | Member 2 | `packages/measurement/src/nirikshak_measurement/__init__.py` | Simple rectangle multiplication: $(W \times H) / 100$. |
| **MRP Field Extraction** | YES | YES | YES (Smoke) | NO | NO | NO | **SCAFFOLD** | Member 3 | `packages/extraction/src/nirikshak_extraction/__init__.py` | Single regex pattern searching for `MRP Rs. X`. |
| **Net Quantity Extraction** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 3 | `packages/extraction/` | Not implemented in extractor. |
| **Date of Packaging/Mfg Parse**| YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 3 | `packages/extraction/` | Not implemented in extractor. |
| **Manufacturer Details Parse** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 3 | `packages/extraction/` | Not implemented in extractor. |
| **Country of Origin Parse** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 3 | `packages/extraction/` | Not implemented in extractor. |
| **Consumer Care Contact Parse**| YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 3 | `packages/extraction/` | Not implemented in extractor. |
| **Rule 6(1)(e) MRP Presence** | YES | YES | YES (Smoke) | NO | NO | NO | **SCAFFOLD** | Member 3 | `packages/rules-engine/src/nirikshak_rules_engine/__init__.py` | Checks if `declarations["mrp"].is_present`. |
| **Rule 6(1)(a)-(d) Declarations**| YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 3 | `packages/rules-engine/` | Unimplemented in rules engine. |
| **Rule 6(11) Unit Sale Price** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 3 | `packages/rules-engine/` | Planned `usp_validator.py` does not exist. |
| **Rule 7 Table-I Font Height** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 3 | `packages/rules-engine/` | Planned `font_matrix.py` does not exist. |
| **5-State Compliance State Machine**| YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 3 | `packages/rules-engine/` | No composite verdict resolution code. |
| **Evidence SHA-256 Digest** | YES | YES | YES (Smoke) | NO | NO | NO | **SCAFFOLD** | Member 3 | `packages/evidence/src/nirikshak_evidence/__init__.py` | Computes standard hashlib SHA-256. |
| **Inspection Dossier PDF** | YES | YES | YES (Smoke) | NO | NO | NO | **SCAFFOLD** | Member 4 | `packages/reporting/src/nirikshak_reporting/__init__.py` | Renders 5 text lines to ReportLab canvas. |
| **Section 36(1) Notice Export** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 4 | `packages/reporting/` | Unimplemented. |
| **FastAPI Ingestion Endpoint** | YES | PARTIAL | YES (Smoke) | NO | NO | NO | **SCAFFOLD** | Member 4 | `apps/api/main.py` | `POST /api/v1/inspections` returns static dummy JSON. |
| **FastAPI Retrieval Endpoint** | YES | PARTIAL | YES (Smoke) | NO | NO | NO | **SCAFFOLD** | Member 4 | `apps/api/main.py` | `GET /api/v1/inspections/{id}` returns static dummy JSON. |
| **Upload Security Middleware** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 4 | `apps/api/` | Magic bytes, decompression bombs, EXIF stripping absent. |
| **Ephemeral Spool TTL Manager** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 4 | `apps/api/` | Planned `spool_service.py` does not exist. |
| **Background Worker Pipeline** | YES | PARTIAL | YES (Smoke) | NO | NO | NO | **SCAFFOLD** | Member 4 | `apps/worker/main.py` | Dummy worker class; synchronous mock calls. |
| **eMaap Sync REST Adapter** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 4 | `apps/api/` | 0 lines of code across repo. |
| **Database Persistence Layer** | YES | PARTIAL | NO | NO | NO | NO | **SCAFFOLD** | Member 4 | `infra/db/init.sql` | SQL schema exists; 0 lines of Python connection code. |
| **Web Image Upload Dropzone** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 5 | `apps/web/` | `ImageUploadZone.tsx` does not exist. |
| **Interactive Bounding Box Canvas**| YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 5 | `apps/web/` | `EvidenceCanvas.tsx` does not exist. |
| **5-State Compliance Badge UI** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 5 | `apps/web/` | `ComplianceDashboard.tsx` does not exist. |
| **Declaration Comparison Table**| YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 5 | `apps/web/` | `DeclarationTable.tsx` does not exist. |
| **Inspector Caliper Override Modal**| YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 5 | `apps/web/` | `InspectorReviewModal.tsx` does not exist. |
| **Pre-loaded Demo SKU Selector**| YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 5 | `apps/web/` | `SamplePackageSelector.tsx` does not exist. |
| **35-SKU Physical Packaging Data**| YES | NO | NO | NO | NO | NO | **BLOCKED** | Member 6 | `data/raw/real/` | 0 images on disk. Formally blocked under Path B Gate. |
| **Synthetic Regression Dataset** | YES | YES | YES | YES | YES | N/A | **IMPLEMENTED** | Member 6 / M1 | `data/synthetic/regression/` | 8 synthetic FMCG packaging PNG images with ground truth. |
| **Automated CI/CD Pipeline** | YES | NO | NO | NO | NO | NO | **NOT_STARTED** | Member 6 | `.github/` | `.github/workflows/` directory does not exist. |
| **Docker Multi-Stage Container**| YES | PARTIAL | NO | NO | NO | NO | **SCAFFOLD** | Member 6 | `infra/docker/` | Dockerfiles exist; container builds unverified. |
