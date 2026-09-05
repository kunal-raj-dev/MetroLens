# MetroLens AI — Complete Current-State Audit
**Document ID:** `docs/audit/METROLENS_COMPLETE_PROJECT_AUDIT.md`  
**Audit Baseline Date:** 2026-09-05  
**Audit Methodology:** Strict Ground-Truth Physical Code, Test Execution, and Filesystem Inspection  
**Audit Constraints:** NO Application Implementation, NO Git Commits, NO Git Pushes, NO File Deletions/Modifications  
**Git Baseline:** Commit `f25d15a` on branch `kunal-member-1-work` (Clean working tree prior to audit)  
**Host Environment:** Windows 11 Home (AMD Ryzen 7 250 w/ Radeon 780M, 8 Cores / 16 Threads, 15.31 GB RAM, NVIDIA RTX 5050 Laptop GPU), Python 3.14.3, Node v25.6.1, Docker 29.7.2

---

## 1. Executive Summary
The MetroLens AI repository represents an automated legal metrology inspection platform currently exhibiting an **extreme architectural imbalance**. The AI/Perception subsystem (`packages/ocr`), developed by Member 1 across Chunks 1 through 4, is fully implemented, packaged as a standard monorepo library, integrated via a thread-safe `OCRService` adapter, and validated against 89 passing automated tests on server CPU with sub-110ms latency. 

However, **virtually every other subsystem in the project exists purely as a hollow skeleton or static scaffold**:
1. **Computer Vision & Calibration (Member 2):** Consists of 30–70 line stubs that perform basic math division; zero coin detection, contour finding, homography unwarping, or image-based metric scale recovery exists.
2. **Legal Rules Engine & Extraction (Member 3):** Evaluates exactly one hardcoded rule (is MRP present?); 5 of 6 mandatory statutory fields are unparsed, and Unit Sale Price arithmetic, Rule 7 font matrices, and the 5-State compliance state machine are completely unbuilt.
3. **Backend API Gateway (Member 4):** The FastAPI application (`apps/api/main.py`) returns static mock JSON with hardcoded `COMPLIANT` verdicts without invoking OCR, computer vision, or legal rules.
4. **Frontend Web UI (Member 5):** The Next.js web application consists of a single 40-line static text page with zero upload functionality, zero API clients, zero canvas overlays, and uninstalled dependencies (`node_modules` does not exist).
5. **Data & Physical Packaging (Member 6):** Real physical packaging data is **entirely absent (0 real images on disk)**. All testing and benchmarks have been executed exclusively on 8 computer-generated synthetic images. Real-world retail packaging accuracy, glare resilience, and curved surface distortion remain completely unverified.

**Conclusion:** The project is not an end-to-end runnable web application. It is currently a high-performance, standalone Python OCR engine surrounded by extensive theoretical documentation and hollow application scaffolds. The immediate engineering imperative is to halt theoretical documentation, wire the working OCR engine into the FastAPI backend, physically collect 35 authentic retail packages, and implement the missing computer vision and legal rules logic.

---

## 2. Project in One Sentence
MetroLens AI is a planned automated compliance inspection web application for Indian packaged commodity labels where **currently only the OCR text extraction subsystem actually works**, while the computer vision calibration, legal rule logic, backend API gateway, and web interface remain as scaffolded skeletons.

---

## 3. Project in Simple Language
The team is attempting to build a tool for government inspectors. An inspector takes a smartphone photo of a product package (like a box of tea or a bag of chips) with a ₹10 coin resting next to it. The system is supposed to inspect the photo, use the coin to calculate the exact physical size of the text in millimeters, read all the printed text in English and Hindi, check if the label obeys Indian packaging laws (such as displaying the MRP, net weight, expiry date, and consumer care phone number in sufficiently large lettering), and generate a legal violation dossier.

In reality today:
- The computer can read the text very quickly and accurately from an image (Step 3 works).
- But the computer does NOT know how to find the coin to measure text size (Step 2 is missing).
- The computer does NOT know the actual rules of Indian packaging law beyond a single check for the word "MRP" (Step 4 is missing).
- There is NO working website or working API to upload the photo (Step 5 is missing).
- And the team has NOT tested the system on a single photograph of a real store-bought product—only on 8 fake test images drawn on a computer.

---

## 4. Actual Current State
- **OCR Subsystem:** `IMPLEMENTED & TESTED` (Chunk 4 complete; direct ONNX PP-OCRv3 engine; median latency 109.64 ms; 67 dedicated tests passing).
- **Shared Data Contracts:** `IMPLEMENTED & TESTED` (Pydantic DTOs and primitives in `packages/shared`; 5 contract tests passing).
- **Vision Quality Gate:** `SCAFFOLD` (Basic numpy variance and threshold stub; 71 lines; no OpenCV Laplacian or HSV glare masking).
- **Optical Calibration:** `SCAFFOLD` (Math division stub; 67 lines; no coin/card contour or ellipse detection from images).
- **Physical Measurement:** `SCAFFOLD` (Multiplies pixels by scale factor; 44 lines; no text-box-to-typographic-font conversion).
- **Semantic Extraction:** `SCAFFOLD` (Single regex for MRP; 47 lines; Net Qty, Dates, Mfr, Origin, and Contact unparsed).
- **Legal Rules Engine:** `SCAFFOLD` (Evaluates only Rule 6(1)(e) MRP presence; 39 lines; composite verdict state machine unbuilt).
- **Evidence Chain:** `SCAFFOLD` (SHA-256 helper and Pydantic factory; 43 lines; no DAG or database persistence).
- **PDF Reporting:** `SCAFFOLD` (Renders 5 plain text lines via ReportLab; 41 lines; no image crops, tables, or Section 36(1) notices).
- **Backend API:** `SCAFFOLD (MOCK)` (FastAPI server runs, but returns hardcoded mock JSON without invoking OCR or rules).
- **Web Frontend:** `SCAFFOLD (STATIC)` (Single 40-line static text landing page; `node_modules` missing).
- **Data (Real):** `0 REAL IMAGES (BLOCKED)` (`data/raw/real/` is empty; 0 annotations; 0 physical caliper sheets).
- **Data (Synthetic):** `8 SYNTHETIC IMAGES` (`data/synthetic/regression/` contains 8 specimens with ground truth).
- **Automated Tests:** `89 PASSING TESTS` (21.49s execution time on Python 3.14.3; 100% pass rate; heavily concentrated in OCR).
- **CI / CD:** `NOT IMPLEMENTED` (`.github/workflows/` does not exist).
- **Database:** `SCAFFOLD (DDL ONLY)` (`infra/db/init.sql` exists; 0 lines of Python ORM/driver code).

---

## 5. Repository Structure
The repository is structured as a Python and TypeScript monorepo:
- `apps/`: Houses the 3 runnable entrypoint applications (`api/`, `web/`, `worker/`). All 3 are currently scaffolds.
- `packages/`: Houses the 9 core modular packages (`ocr`, `shared`, `calibration`, `evidence`, `extraction`, `measurement`, `reporting`, `rules-engine`, `vision`). Only `ocr` and `shared` have functional code.
- `models/`: Version-controlled ONNX model weights (22.1 MB total) and machine-readable manifests (`models/manifest.yaml`).
- `data/`: Datasets and manifests. Contains 8 synthetic regression specimens in `synthetic/regression/`; `raw/real/` is empty.
- `METROLENS_LEGAL_SOURCE_PACK/`: 74 authentic Indian government Gazette and Act PDFs, indexed and hashed.
- `benchmarks/`: Empirical benchmark harnesses and results (Chunks 2, 3, and 4 in `benchmarks/ocr/`).
- `CURRENT_STATE/`: Authoritative execution snapshots and chunk baselines.
- `AI_CONTEXT/`: Granular execution run logs, experiment notes, and cross-member handoffs.
- `docs/`: 123+ markdown files detailing architecture, legal matrices, user personas, and individual work plans.
- `tests/`: Root integration and unit test suite containing 9 test files.
- `scripts/`: Integrity verification scripts (`scripts/verification/`).
- `tools/`: Utility CLI scripts for debugging, visualization, and context generation.
- `infra/`: PostgreSQL initialization DDL and Dockerfiles.

---

## 6. What Each Folder Does
*(Refer to [`docs/audit/FOLDER_EXPLANATION.md`](file:///c:/Users/kunal/Desktop/MetroLens/docs/audit/FOLDER_EXPLANATION.md) for the complete 21-folder catalog).*
- `packages/ocr/`: Contains the complete, working perception engine.
- `packages/shared/`: Contains canonical data transfer objects (`contracts.py`) and enums (`primitives.py`).
- `packages/vision/`, `calibration/`, `measurement/`, `extraction/`, `rules-engine/`, `evidence/`, `reporting/`: Scaffold stubs awaiting real implementation.
- `apps/api/`: FastAPI server returning mock JSON.
- `apps/web/`: Next.js static placeholder page.
- `data/raw/real/`: Intended home for 35 authentic packaging images (currently empty).
- `data/synthetic/regression/`: Houses the 8 synthetic test specimens.
- `METROLENS_LEGAL_SOURCE_PACK/`: Immutable archive of 74 sovereign legal PDFs.
- `docs/`: Master architectural and requirements library (describes target state).
- `CURRENT_STATE/`: Master status baseline directory.

---

## 7. What Each Important File Does
*(Refer to [`docs/audit/FILE_EXPLANATION.md`](file:///c:/Users/kunal/Desktop/MetroLens/docs/audit/FILE_EXPLANATION.md) for individual file analyses).*
- `packages/ocr/src/nirikshak_ocr/service.py`: High-level production service adapter (`OCRService`) providing thread-safe, contract-compliant text extraction.
- `packages/ocr/src/nirikshak_ocr/engine.py`: Internal facade orchestrating DBNet++ detection and SVTR recognition.
- `packages/shared/src/nirikshak_shared/models/contracts.py`: Master Pydantic DTOs governing data flow between subsystems.
- `apps/api/main.py`: FastAPI application entrypoint with mock endpoints.
- `apps/web/src/app/page.tsx`: Static landing page for the frontend.
- `models/manifest.yaml`: Machine-readable authority for model weights and hashes.
- `CURRENT_STATE/PROJECT_SNAPSHOT.md`: Authoritative single-page progress tracker.
- `pytest.ini`: Root pytest configuration enabling monorepo-wide test discovery.

---

## 8. Actual Architecture
The actual architecture currently functioning in the repository is an in-memory, single-process perception pipeline:
1. **Input:** An image file path, raw byte buffer, or numpy RGB array is provided to `nirikshak_ocr.OCRService`.
2. **Normalization:** Input is converted to a contiguous uint8 RGB numpy array (`convert_image_input` with defensive copy).
3. **Detection (DBNet++):** The image is resized to multiples of 32 (max side 960px) and normalized with ImageNet statistics. `ch_PP-OCRv3_det_infer.onnx` generates a probability map. Contours are extracted and expanded using Vatti clipping (`pyclipper`, unclip ratio 1.6) to produce rotated 4-point quadrilateral polygons.
4. **Perspective Crop:** Each text polygon is cropped and orthorectified via OpenCV `cv2.getPerspectiveTransform`.
5. **Script Routing:** Text crops are analyzed by character aspect ratio and Unicode block heuristics in `router.py` to route to Latin vs Devanagari models.
6. **Recognition (SVTR):** Latin crops are resized to $48 \times 320$ and evaluated by `ch_PP-OCRv3_rec_infer.onnx`. Devanagari crops are evaluated by `rec.onnx` with `dict.txt`. CTC greedy decoding transcribes character strings.
7. **Marshalling:** Results are filtered by confidence ($c \ge 0.60$) and packaged into canonical `OCRObservation` instances.
8. **Pipeline Block:** The pipeline terminates here. No downstream caller in `apps/api/` or `apps/worker/` invokes this service.

---

## 9. Actual End-to-End Flow
```
[User / Developer] (Invokes Python Script or Pytest)
       │
       ▼
[packages/ocr/src/nirikshak_ocr/service.py: OCRService]
       │
       ▼
[packages/ocr/src/nirikshak_ocr/detector.py: DBNet++]
       │  (Extracts 4-point bounding polygons)
       ▼
[packages/ocr/src/nirikshak_ocr/router.py: ScriptRouter]
       │  (Routes crops to Latin vs Devanagari)
       ▼
[packages/ocr/src/nirikshak_ocr/recognizer.py: SVTR]
       │  (Decodes Unicode text tokens)
       ▼
[List[OCRObservation] DTO Tokens]
       │
       ▼
════════════════════════════════════════════════════════════════
  PIPELINE BLOCKED HERE — ALL DOWNSTREAM SUBSYSTEMS ARE HOLLOW
  - apps/api/main.py DOES NOT call OCRService
  - packages/calibration/ DOES NOT detect coins from images
  - packages/rules-engine/ DOES NOT evaluate legal rules
  - apps/web/ DOES NOT communicate with backend
════════════════════════════════════════════════════════════════
```

---

## 10. Target / Planned Architecture
*(PLANNED / NOT CURRENT)*  
The planned architecture described in `docs/PRODUCT_BLUEPRINT.md` and `docs/ARCHITECTURE.md`:
1. Officer uploads front and back photos of packaging via React 19 web interface with drag-and-drop dropzone.
2. Ingestion security middleware validates magic bytes, strips EXIF metadata, and caps decompression bombs at 64MP.
3. Optical quality filter rejects blurred frames (Laplacian $<100$) and high specular glare ($>15\%$) in $<15$ms.
4. Optical calibration engine locates a coplanar ₹10 coin ($27.0\text{mm}$) and computes metric scale ($S$ in mm/px).
5. Planar homography unwarps tilted declaration panels into orthorectified viewports.
6. OCR engine extracts text tokens in English and Hindi.
7. Entity normalizer parses mandatory Rule 6 fields (MRP, Net Qty, Dates, Mfr, Origin, Contact).
8. Measurement module converts bounding boxes to calibrated physical millimeter heights ($h_{\text{mm}}$) and PDP area ($A_{\text{cm}^2}$).
9. Deterministic rules engine evaluates compliance against Rules 6, 6(11), 7, 8, and 26, computing Unit Sale Price and matching font height tables.
10. System generates a 5-State compliance verdict and signs an immutable PDF inspection dossier with Section 36(1) Notice in $<500$ms.
11. Mock eMaap adapter synchronizes findings with the National Legal Metrology portal.

---

## 11. Current vs Planned
*(Refer to [`docs/audit/ACTUAL_VS_PLANNED.md`](file:///c:/Users/kunal/Desktop/MetroLens/docs/audit/ACTUAL_VS_PLANNED.md) for the comprehensive comparison table).*  
- **Perception Layer:** 100% of planned capability delivered.
- **Vision & Calibration:** ~10% delivered (math division stubs; 0% image anchor detection).
- **Domain Logic & Rules:** ~10% delivered (1 of 7 statutory rules encoded).
- **Backend Gateway:** ~15% delivered (FastAPI server exists, but routes are static mocks).
- **Frontend Web UI:** ~5% delivered (static landing page; uninstalled dependencies).
- **Physical Packaging Data:** 0% delivered (0 of 35 real images exist on disk).

---

## 12. Subsystem Status
| Subsystem | Classification | Implementation Reality |
| :--- | :--- | :--- |
| **OCR Perception** | `IMPLEMENTED & TESTED` | Direct ONNX DBNet++ + SVTR-EN + SVTR-HI; 67 tests pass. |
| **Shared Contracts** | `IMPLEMENTED & TESTED` | Pydantic DTOs and primitives; 5 tests pass. |
| **Computer Vision** | `SCAFFOLD` | Raw gray variance stub; 1 smoke test passes. |
| **Calibration** | `SCAFFOLD` | Float division math stub; 2 smoke tests pass. |
| **Measurement** | `SCAFFOLD` | Float multiplication stub; 3 smoke tests pass. |
| **Extraction** | `SCAFFOLD` | Single MRP regex; 1 smoke test passes. |
| **Rules Engine** | `SCAFFOLD` | 1 rule evaluation (MRP presence); 2 smoke tests pass. |
| **Evidence** | `SCAFFOLD` | SHA-256 helper and DTO factory; 2 smoke tests pass. |
| **Reporting** | `SCAFFOLD` | 5-line ReportLab canvas; 1 smoke test passes. |
| **Backend API** | `SCAFFOLD (MOCK)` | FastAPI mock endpoints; 2 smoke tests pass. |
| **Frontend Web** | `SCAFFOLD (STATIC)` | Static Next.js page; 0 tests; `node_modules` missing. |
| **eMaap Sync** | `NOT_STARTED` | Documented only; 0 code. |
| **Database** | `SCAFFOLD (DDL ONLY)`| PostgreSQL SQL script; 0 Python connection code. |
| **CI / CD** | `NOT_STARTED` | `.github/workflows/` does not exist. |
| **Real Packaging Data**| `BLOCKED (0 IMAGES)` | Path B Gate enforced; 0 images in `data/raw/real/`. |
| **Synthetic Data** | `IMPLEMENTED` | 8 synthetic images in `data/synthetic/regression/`. |

---

## 13. Member 1 Status (AI & OCR Perception Lead)
- **Role:** Member 1.
- **Ownership:** `packages/ocr/`, `models/weights/ocr/`, `benchmarks/ocr/`.
- **Actual Work Completed:** Successfully delivered Chunks 1 through 4. Implemented direct ONNX engine, multilingual script router, preprocessing filter evaluation suite, typed Pydantic config, standardized error codes, and thread-safe `OCRService` adapter. Authored 67 passing tests and verified CPU latency (~109ms), concurrency (8.81 req/s), and bounded memory (296 MB peak RSS).
- **Handoffs Delivered:** Formally authored handoffs to Member 2, Member 3, Member 4, Member 5, and Chunk 5 (`AI_CONTEXT/HANDOFFS/`).
- **Remaining / Blocked Work:** Real-data benchmark validation remains **BLOCKED** awaiting physical packaging photographs from Member 6.
- **Verdict:** **COMPLETE & VERIFIED (Ahead of all other streams)**.

---

## 14. Member 2 Status (CV, Calibration & Measurement Lead)
- **Role:** Member 2.
- **Ownership:** `packages/vision/`, `packages/calibration/`, `packages/measurement/`.
- **Actual Work Completed:** Scaffolded 3 packages with minimal `__init__.py` files and 6 smoke tests. Implemented basic scale division formula and rectangular PDP area formula.
- **What Is Missing:** ₹10 coin contour detection, ellipse fitting, ISO card detection, planar homography unwarping ($3 \times 3$ $H$ matrix), cylindrical surface unwarping, and conversion of OCR token bounding boxes to typographic font heights.
- **Blockers:** Blocked on Member 6 for physical packaging photos containing reference coins; unblocked on synthetic math testing.
- **Verdict:** **SCAFFOLD ONLY (Implementation Pending)**.

---

## 15. Member 3 Status (Legal Rules & Compliance Engine Lead)
- **Role:** Member 3.
- **Ownership:** `packages/rules-engine/`, `packages/extraction/`, `packages/evidence/`.
- **Actual Work Completed:** Scaffolded 3 packages with 5 smoke tests. Implemented a regex parsing MRP amount and a rule evaluator checking MRP presence under Rule 6(1)(e).
- **What Is Missing:** Entity normalizers for Net Quantity, Dates, Manufacturer, Country of Origin, and Consumer Care. Rule evaluators for Rules 6(1)(a)-(d), 6(11) USP arithmetic, and Rule 7 font-to-area matrix. 5-State compliance state machine. 25-case statutory test suite.
- **Blockers:** None for regex and declaration rules (can develop against synthetic OCR tokens immediately); partially blocked on Member 2 for Rule 7 physical millimeter font heights.
- **Verdict:** **SCAFFOLD ONLY (Implementation Pending)**.

---

## 16. Member 4 Status (Backend API Gateway & PDF Reporting Lead)
- **Role:** Member 4.
- **Ownership:** `apps/api/`, `apps/worker/`, `packages/reporting/`, `infra/db/`.
- **Actual Work Completed:** Scaffolded FastAPI service with CORS middleware and 3 endpoints; created PostgreSQL 16 DDL script (`init.sql`); created basic ReportLab PDF canvas stub.
- **What Is Missing:** Real pipeline integration (importing and calling `OCRService`, Vision, and Rules Engine); upload security (magic bytes, 64MP cap, EXIF strip); ephemeral spool manager (60-min TTL); full PDF dossier compiler with Section 36(1) notices and image crops; database repository layer.
- **Blockers:** None for OCR integration (Member 1's `OCRService` is ready); partially blocked on Member 3 for real compliance results.
- **Verdict:** **SCAFFOLD ONLY (Implementation Pending)**.

---

## 17. Member 5 Status (Frontend Engineering & Web UX Lead)
- **Role:** Member 5.
- **Ownership:** `apps/web/`.
- **Actual Work Completed:** Scaffolded Next.js 14 App Router shell (`layout.tsx`) and static landing page (`page.tsx`).
- **What Is Missing:** Dependency installation (`npm install`); drag-and-drop image upload dropzone; API integration with FastAPI; interactive image canvas rendering color-coded bounding boxes; executive 5-state compliance dashboard; declaration comparison table; inspector caliper override modal; 10-SKU pre-loaded demo selector.
- **Blockers:** Partially blocked on Member 4 providing a live API that returns real image observations; can develop against mock JSON immediately.
- **Verdict:** **SCAFFOLD ONLY (Implementation Pending)**.

---

## 18. Member 6 Status (Product Integration, QA & Release Lead)
- **Role:** Member 6.
- **Ownership:** `data/`, `infra/`, `.github/`, `benchmarks/`.
- **Actual Work Completed:** Created synthetic regression dataset (8 PNGs + manifest); authored master dataset manifests; authored 6 repository integrity verification scripts; created Dockerfiles.
- **What Is Missing:** Curating the 35-SKU authentic physical retail packaging dataset; conducting 1200 DPI flatbed optical scans and digital caliper ground-truth measurements; executing empirical benchmarks on real packaging; creating automated GitHub Actions CI workflow (`.github/workflows/ci.yml`).
- **Blockers:** Blocked on physical specimen acquisition and photography.
- **Verdict:** **BLOCKED ON PHYSICAL DATA / SCAFFOLD**.

---

## 19. Cross-Member Dependencies
*(Refer to [`docs/audit/CROSS_MEMBER_DEPENDENCIES.md`](file:///c:/Users/kunal/Desktop/MetroLens/docs/audit/CROSS_MEMBER_DEPENDENCIES.md)).*  
- **M4 $\rightarrow$ M1:** UNBLOCKED. `OCRService` is complete and verified. Member 4 has simply not wired it into `apps/api/main.py`.
- **M3 $\rightarrow$ M1:** UNBLOCKED. `OCRObservation` tokens are standardized and ready for regex parsing.
- **M5 $\rightarrow$ M4:** BLOCKED BY MOCK. Member 5 cannot build live upload/overlay workflows until Member 4 makes the API functional.
- **M3 $\rightarrow$ M2:** PARTIALLY BLOCKED. Member 3 cannot test Rule 7 font-to-area matrix until Member 2 provides millimeter scale factors.
- **M1 & M2 $\rightarrow$ M6:** CRITICALLY BLOCKED. Neither Member 1 nor Member 2 can validate real-world packaging performance because Member 6 has not collected physical photos.

---

## 20. Current Critical Path
1. **Critical Step 1 (Internal):** Member 4 wires `OCRService` into `apps/api/main.py` (Unlocks HTTP OCR).
2. **Critical Step 2 (External):** Member 6 collects 35 authentic retail packages with ₹10 coin reference targets (Unblocks Real Data Gate).
3. **Critical Step 3 (Domain):** Member 2 implements ₹10 coin anchor detection in `packages/calibration/` (Unlocks Physical Scale).
4. **Critical Step 4 (Domain):** Member 3 implements regex extraction and statutory rules in `packages/rules-engine/` (Unlocks Legal Compliance).
5. **Critical Step 5 (Client):** Member 5 builds interactive upload and bounding box canvas in `apps/web/` (Unlocks Live Demo).

---

## 21. Tests
- **Execution Command:** `python -m pytest`
- **Result:** **89 passed, 1 warning in 21.49s** (100% pass rate).
- **Warning:** `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead.`
- **Distribution:**
  - `tests/integration/test_ocr_service_integration.py`: 16 tests.
  - `tests/unit/test_ocr_*.py`: 46 tests.
  - `tests/unit/test_verification_pipeline.py`: 5 tests (executes subordinate verification scripts).
  - `packages/*/tests/`: 18 tests (5 in `shared`, 1 in `ocr`, 12 smoke tests across 7 scaffold packages).
  - `apps/*/tests/`: 4 tests (2 in `api`, 2 in `worker`).
- **Test Quality Assessment:** The 67 OCR and shared tests are comprehensive, asserting on mock images, synthetic fixtures, socket isolation, thread safety, memory boundaries, and contract schemas. The remaining 22 tests are hollow smoke tests that assert `True` or check that an empty class instantiates without crashing.

---

## 22. Benchmarks
- **Harnesses:** Located in `benchmarks/ocr/` (Chunks 2, 3, and 4).
- **Chunk 4 Integration Benchmark Results (`integration_results.json`):**
  - Bare `OCREngine` Latency: Median **106.60 ms** (Mean 108.66 ms, P95 121.11 ms).
  - `OCRService` Latency (Path): Median **109.64 ms** (Mean 112.74 ms, P95 132.18 ms).
  - `OCRService` Latency (Bytes): Median **108.84 ms** (Mean 108.10 ms, P95 113.40 ms).
  - `OCRService` Latency (`to_observations`): Median **113.27 ms** (Mean 114.29 ms, P95 121.83 ms).
  - Adapter Overhead: **3.04 ms**.
  - Concurrency Throughput: **8.81 req/sec** (4 worker threads, 8 concurrent requests, 908.18 ms total).
  - Memory Footprint: 71.11 MB start $\rightarrow$ 150.17 MB warm $\rightarrow$ 296.85 MB peak concurrency.
- **Reproducibility:** **VERIFIED (Synthetic)**. The benchmark script runs deterministically on CPU.
- **Limitation:** All benchmark numbers reflect performance on computer-generated synthetic specimens; real-world packaging latency and accuracy are unmeasured.

---

## 23. Data
- **Real Packaging Images:** **0 images** on disk (`data/raw/real/` is completely empty).
- **Real Packaging Annotations:** **0 files** on disk (`data/annotations/ocr/` is completely empty).
- **Physical Caliper Measurement Sheets:** **0 sheets** on disk.
- **Synthetic Packaging Specimens:** **8 images** (`SYNTH-01-ENG-FMCG.png` through `SYNTH-08-LOW-CONTRAST-FADED.png`) in `data/synthetic/regression/`.
- **Manifests:** `data/manifests/real_packaging_manifest.json` correctly declares the status as `BLOCKED_AWAITING_PHYSICAL_DATA_COLLECTION`.

---

## 24. Models
- **Model Weights Inventory:**
  1. `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx` (2,432,880 bytes, SHA-256: `3439588c030faea393a54515f51e983d8e155b19a2e8aba7891934c1cf0de526`) — DBNet++ text detector.
  2. `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx` (10,690,752 bytes, SHA-256: `897a3ededb38fee0dae2c1ccee38241f37df202c9509e3abca02e9217c5ee615`) — SVTR Latin/English recognizer.
  3. `models/weights/ocr/rec_hi/rec.onnx` (8,980,224 bytes, SHA-256: `43df175fa3c877fbf7bcc4e5bd1e203e24ec450cd3ea96c9e802c86e39a4d4cf`) — SVTR Devanagari Hindi recognizer.
  4. `models/weights/ocr/rec_hi/dict.txt` (SHA-256: `b5f1be6d8bbff1a19fb96c5d4ca96a423380234bb7d2ce0e07b5838adb4d18ea`) — 167-character dictionary.
- **Model Provenance:** Official PaddleOCR / RapidOCR model hub and Hugging Face port (`monkt/paddleocr-onnx`). Licensed under Apache-2.0.
- **Runtime:** `onnxruntime==1.29.0` with `CPUExecutionProvider`.
- **Status:** **ALL 3 MODELS PRESENT, HASH-VERIFIED, AND ACTIVE**.

---

## 25. API
- **Entrypoint:** `apps/api/main.py`.
- **Routes Implemented:**
  - `GET /health` $\rightarrow$ returns `{"status": "ok", "service": "nirikshak-api", "version": "0.1.0"}`.
  - `POST /api/v1/inspections` $\rightarrow$ returns hardcoded `InspectionResult` with `COMPLIANT` verdict.
  - `GET /api/v1/inspections/{id}` $\rightarrow$ returns hardcoded `InspectionResult`.
- **Actual Status:** **SCAFFOLD MOCK ONLY**. Endpoints exist and pass basic smoke tests, but do NOT execute OCR, computer vision, or rules logic.

---

## 26. Frontend
- **Framework:** Next.js 14.2.5 (React 18.3.1) App Router in `apps/web/`.
- **Actual Status:** **SCAFFOLD STATIC TEXT ONLY**.
- **Content:** `src/app/page.tsx` is a 40-line static text page.
- **Dependencies:** `node_modules` does not exist on disk (`npm install` has never been run).
- **Interactivity:** Zero upload dropzones, zero API fetch calls, zero canvas bounding box overlays.

---

## 27. Legal Components
- **Source Pack:** `METROLENS_LEGAL_SOURCE_PACK/` contains 74 authentic Indian government Gazette and Act PDFs.
- **Canonical Register:** `regulations/source_registry.yaml` lists primary acts and amendments with official DCA URLs.
- **Codified Rules:** Only Rule 6(1)(e) (MRP presence) is encoded in Python (`packages/rules-engine/`). Rules for Net Quantity, Dates, Manufacturer, Country of Origin, Consumer Care, Unit Sale Price arithmetic, and Rule 7 font-to-area matrices exist only as candidate YAML proposals in `rules/proposed/` or documentation tables in `docs/LEGAL_RULE_MATRIX.md`.

---

## 28. AI Context
- **Directory:** `AI_CONTEXT/`.
- **Health Assessment:** Excellent structure. Detailed run logs exist for Chunks 1 through 4 (`AI_CONTEXT/RUN_LOGS/`). Experiment records (`AI_CONTEXT/EXPERIMENTS/`) document why RapidOCR was abandoned and why `B0_BASELINE_RAW` was chosen over CLAHE. Formal handoffs (`AI_CONTEXT/HANDOFFS/`) define precise inter-chunk and inter-member boundaries.
- **Usability for Future Agents:** **HIGH**. An incoming AI agent can read `CURRENT_STATE/PROJECT_SNAPSHOT.md` and `AI_CONTEXT/HANDOFFS/CHUNK_4_TO_CHUNK_5.md` to resume work seamlessly without hallucinating project state.

---

## 29. Current State
- **Current Chunk:** **Chunk 4 is COMPLETE & VERIFIED**.
- **Next Chunk:** **Chunk 5 is READY TO START** (focused on Pipeline Orchestration and API mounting).
- **Baselines:** Validated baselines exist on disk up to `CHUNK_4_BASELINE.md`.

---

## 30. Documentation Health
- **Total Documents:** 150+ markdown files across `docs/`, `research/`, and `problem statement #1/`.
- **Diagnosis:** **OVER-DOCUMENTED AND PARTIALLY DIVERGENT**. The team has written extensive, high-quality specifications for a mature, court-admissible regulatory system. However, the documentation frequently speaks in the present tense about features that do not exist in code (such as Celery workers, React 19 UIs, eMaap synchronization, and physical font height measurement).
- **Remedy:** Add status disclaimers to blueprint documents and align endpoint paths.

---

## 31. Clutter
*(Refer to [`docs/audit/CLUTTER_CLEANUP_PLAN.md`](file:///c:/Users/kunal/Desktop/MetroLens/docs/audit/CLUTTER_CLEANUP_PLAN.md)).*  
- `ALL-IN-ONE context/METROLENS_AI_ALL_IN_ONE_DOCS.md` (720 KB redundant dump).
- `problem statement #1/` (~1 MB historical dossier, superseded by `docs/01_PROBLEM_STATEMENT/`).
- 25+ empty scaffold directories containing only `.gitkeep`.
- No clutter should be deleted during this audit; a formal cleanup pass should occur post-audit.

---

## 32. Duplicate / Stale Content
*(Refer to [`docs/audit/DOCUMENTATION_CONTRADICTIONS.md`](file:///c:/Users/kunal/Desktop/MetroLens/docs/audit/DOCUMENTATION_CONTRADICTIONS.md)).*  
- Duplicate architecture descriptions across `PRODUCT_BLUEPRINT.md` and `ARCHITECTURE.md`.
- Stale references to Celery/Redis in architecture docs.
- Stale references to React 19 + Vite in Member 5 plan vs Next.js 14 in `package.json`.
- Inconsistent endpoint paths (`/api/v1/inspect` vs `/api/v1/inspections`).

---

## 33. Technical Debt
*(Refer to [`docs/audit/TECHNICAL_DEBT.md`](file:///c:/Users/kunal/Desktop/MetroLens/docs/audit/TECHNICAL_DEBT.md)).*  
- **Critical:** Mock return in core API ingestion route (`apps/api/main.py`).
- **High:** Subsystem integration debt across Members 2, 3, 4, and 5.
- **High:** Incomplete OpenCV Laplacian and glare filter in `packages/vision/`.
- **Medium:** Uninstalled frontend dependencies in `apps/web/`.
- **Medium:** Absence of automated CI workflow in `.github/workflows/`.

---

## 34. Current Blockers
*(Refer to [`docs/audit/CURRENT_BLOCKERS.md`](file:///c:/Users/kunal/Desktop/MetroLens/docs/audit/CURRENT_BLOCKERS.md)).*  
1. **Blocker 1 (Critical):** Zero physical retail package images on disk (Member 6).
2. **Blocker 2 (Critical):** Optical coin calibration anchor detection missing (Member 2).
3. **Blocker 3 (Critical):** Legal rule engine and field normalizers unbuilt (Member 3).
4. **Blocker 4 (High):** Backend API disconnected from `OCRService` (Member 4).
5. **Blocker 5 (High):** Frontend Web UI lacks interactive components (Member 5).
6. **Blocker 6 (Medium):** CI pipeline unimplemented (Member 6).

---

## 35. Demo Readiness
- **Can the repository run end-to-end today?** **NO**.
- **Why?** The web UI is static, the API returns hardcoded fake JSON, and the backend is not wired to the OCR or rules engine.
- **What can be demonstrated independently?**
  - **Standalone OCR Script:** Member 1's `OCRService` can be executed from a Python script or CLI, taking any image and outputting bounding boxes, text strings, and script routing decisions in ~109ms.
  - **Test Suite:** Pytest can be run to prove that 89 tests pass cleanly.

---

## 36. Reproducibility
- **OCR Synthetic Latency & Memory:** **REPRODUCIBLE (100%)**. Benchmarks run locally on CPU and produce consistent latency (~109ms) and memory bounds (296 MB).
- **Repository Integrity Tests:** **REPRODUCIBLE (100%)**. All 5 verification scripts execute and pass.
- **Real-World Packaging Accuracy:** **NON-REPRODUCIBLE / UNVERIFIED**. Zero real-world datasets exist on disk.

---

## 37. Security Observations
- **CORS Configuration:** `apps/api/main.py` line 20 specifies `allow_origins=["*"]`. Acceptable for local development/hackathon, but must be restricted to specific frontend origins prior to public deployment.
- **Upload Hardening:** Ingestion security (magic-byte header validation, Pillow decompression bomb caps, EXIF sanitization) is documented in architecture plans but **completely absent in code**.
- **Secrets Audit:** No committed API keys, private tokens, or secret credentials were found. `.env.example` contains only non-sensitive placeholder names.

---

## 38. What Has Actually Been Completed
- Core Multilingual Perception Engine (`packages/ocr`) running DBNet++ and SVTR ONNX models.
- English and Hindi script router based on Unicode block analysis.
- Domain preprocessing filter suite (CLAHE, bilateral, unsharp, dilation).
- Monorepo package architecture with editable `pip` installations.
- Production `OCRService` singleton adapter with thread-safe execution serialization.
- Canonical domain primitives and contracts (`packages/shared`).
- Synthetic FMCG test dataset (8 specimens) and ground-truth manifests.
- 89 automated tests passing with 100% pass rate.
- Collection and indexing of 74 sovereign Indian government legal PDFs.

---

## 39. What Has NOT Been Completed
- Real physical packaging dataset collection and annotation (0 images).
- Computer vision ₹10 coin anchor detection from photos.
- Planar homography perspective unwarping.
- Conversion of OCR bounding boxes to typographic font heights in millimeters.
- Regex normalizers for Net Quantity, Dates, Manufacturer, and Consumer Care.
- Deterministic statutory rule engine evaluating Rules 6, 6(11), 7, and 26.
- Real pipeline integration inside FastAPI routes.
- Interactive Next.js web application with image upload and bounding box canvas.
- Court-admissible signed PDF dossier compiler.
- Automated GitHub Actions CI workflow.

---

## 40. What Is Only Planned
- Integration with National Legal Metrology eMaap portal.
- 5-layer demo failover architecture.
- PostgreSQL persistence repository layer.
- Right-cylinder unwarping for curved beverage cans.
- Dedicated fine-tuned dot-matrix recognition model.

---

## 41. What Is Historical
- Exploratory spikes evaluating RapidOCR and Tesseract (Chunk 1).
- Blanket full-image CLAHE preprocessing (rejected in Chunk 3).
- Distributed Celery/Redis task worker architecture (superseded by ADR-011).
- Historical 50-SKU dataset targets in early draft manifests (standardized to 35).
- Problem Statement #1 inception dossier scripts.

---

## 42. What Should Be Ignored
- Any claim in documentation stating that MetroLens AI is currently "court admissible", "officially compliant", or "fully integrated end-to-end".
- Celery and Redis deployment guides in older architecture docs.
- The 720KB concatenated file in `ALL-IN-ONE context/`.

---

## 43. Immediate Next Steps
1. **Member 4:** Wire `OCRService.get_instance()` into `apps/api/main.py` so `POST /api/v1/inspections` processes real uploaded images.
2. **Member 6:** Physically purchase and photograph 35 FMCG items with a ₹10 coin and populate `data/raw/real/`.
3. **Member 2:** Implement circular contour detection and ellipse fitting in `packages/calibration/` to detect ₹10 coins and calculate millimeters per pixel.
4. **Member 3:** Write regex normalizers for Net Quantity and Dates, and implement Rule 6 and Rule 6(11) evaluations in `packages/rules-engine/`.
5. **Member 5:** Run `npm install` in `apps/web/` and build the upload dropzone and canvas bounding box overlay.
6. **Member 6:** Add `.github/workflows/ci.yml` to automate pytest on GitHub.

---

## 44. Overall Assessment
The MetroLens AI project has built a **world-class, production-quality OCR perception foundation** that runs locally, executes in ~109ms on CPU, and passes 89 rigorous tests. However, the project has suffered from **severe documentation-implementation divergence**: the team has written specifications for a completed, multi-tiered enterprise legal compliance system while leaving 5 out of 6 functional application subsystems as 40-line stubs. 

The project is **not failing**, but it is **drastically lopsided**. If the team shifts its focus immediately from writing documentation to wiring Member 1's working OCR engine into the API, collecting 35 real product photos, and implementing the core computer vision and legal rules logic, the system can achieve full end-to-end demo readiness well within the remaining sprint window.
