# MetroLens AI — Cross-Member Dependency Graph & Bottleneck Audit
**Audit Baseline Date:** 2026-09-05  
**Core Standard:** Hard Evidence from Monorepo Contracts and Disk Assets

---

## 1. Dependency Status Registry

| Consumer (A) | Producer (B) | Required Artifact / Contract | B Complete? | B Integrated? | B Documented? | B Blocked? | Real State & Impact |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Member 4 (Backend)** | **Member 1 (OCR)** | `nirikshak_ocr.OCRService` in-process API (`extract_observations`, `extract_dict`) | **YES** | **YES** (Unit & Integration tests pass) | **YES** (`AI_CONTEXT/HANDOFFS/M1_TO_M4_CHUNK4.md`) | **NO** | **UNBLOCKED**. Member 4 can import and execute `OCRService` immediately. Member 4 has not yet wired it into `apps/api/main.py`. |
| **Member 3 (Rules)** | **Member 1 (OCR)** | Standardized `OCRObservation` DTO tokens with 4-point polygon coordinates | **YES** | **YES** (`nirikshak_shared.models.contracts`) | **YES** (`AI_CONTEXT/HANDOFFS/M1_TO_M3_CHUNK4.md`) | **NO** | **UNBLOCKED**. Member 3 can consume `OCRObservation` tokens immediately to build field regexes. |
| **Member 2 (CV)** | **Member 1 (OCR)** | Raw bounding boxes for numeral text lines to compute physical font heights | **YES** | **YES** (`OCRObservation.bounding_box`) | **YES** (`AI_CONTEXT/HANDOFFS/M1_TO_M2_CHUNK4.md`) | **NO** | **UNBLOCKED**. Member 1 emits pixel-height and rotated bounding boxes. |
| **Member 5 (Web UI)** | **Member 4 (Backend)** | Working `POST /api/v1/inspections` and `GET /api/v1/inspections/{id}` endpoints returning real data | **NO** (Mocked only) | **NO** | **YES** (`docs/API_CONTRACT.md`) | **NO** (Self-blocked) | **BLOCKED BY MOCK**. Member 5 can build UI against mocked JSON, but cannot test real image processing until Member 4 implements the pipeline. |
| **Member 3 (Rules)** | **Member 2 (CV)** | Metric physical measurements (`measured_mm`, `pdp_area_cm2`) for Rule 7 font-to-area matrix | **NO** (Scaffold only) | **NO** | **YES** (`MEMBER_2_WORK_PLAN.md`) | **NO** | **PARTIAL BLOCKER**. Member 3 can evaluate Rule 6 declarations (text presence), but CANNOT evaluate Rule 7 (font height vs PDP area) until Member 2 provides real millimeter measurements. |
| **Member 4 (Backend)** | **Member 3 (Rules)** | `NirikshakRulesEngine.evaluate()` returning 5-State compliance verdicts | **NO** (Only MRP check) | **NO** | **YES** (`MEMBER_3_WORK_PLAN.md`) | **NO** | **BLOCKED ON IMPLEMENTATION**. Member 4 cannot return a real statutory verdict until Member 3 writes the compliance state machine. |
| **Member 4 (Backend)** | **Member 2 (CV)** | `check_image_quality` and metric scale calibration output | **NO** (Scaffolds only) | **NO** | **YES** (`MEMBER_2_WORK_PLAN.md`) | **NO** | **BLOCKED ON IMPLEMENTATION**. Member 4 cannot run real image quality gate or physical calibration. |
| **Member 6 (QA/Bench)** | **Member 1 (OCR)** | Stable, offline, reproducible OCR engine with documented CLI / API | **YES** | **YES** | **YES** (`CHUNK_4_STATUS.md`) | **NO** | **UNBLOCKED**. Member 6 has everything needed from Member 1 to run OCR benchmarks. |
| **Member 1 (OCR)** | **Member 6 (Data)** | 35-SKU authentic physical retail packaging dataset (`data/raw/real/`) | **NO** (0 images) | **NO** | **YES** (`real_packaging_manifest.json`) | **YES (Path B Gate)** | **CRITICAL BLOCKER**. Member 1 cannot perform real-world OCR validation or fine-tuning because Member 6 has not provided physical photos. |
| **Member 2 (CV)** | **Member 6 (Data)** | Physical packaging photos containing reference coins/cards + flatbed scans | **NO** (0 images) | **NO** | **YES** (`MEMBER_6_WORK_PLAN.md`) | **YES (Path B Gate)** | **CRITICAL BLOCKER**. Member 2 cannot test coin detection, tilt invariance, or homography rectification without real camera photos containing coins. |
| **Member 6 (Release)** | **M2, M3, M4, M5** | Functional application modules to package into Docker and test in CI | **NO** (Scaffolds only) | **NO** | **YES** | **NO** | **BLOCKED BY REPO MATURITY**. Member 6 cannot run meaningful end-to-end integration tests because 4 of 6 members have only committed stubs. |

---

## 2. The Critical Dependency Bottlenecks

### Bottleneck 1: Member 6 Physical Data Collection (External Blocker)
- **Impacts:** Member 1 (OCR real validation), Member 2 (Calibration & homography), Member 6 (Empirical benchmarks).
- **Reality:** While development can continue on synthetic data, no real-world accuracy claim or demo on authentic Indian packaging can be verified until physical photos are acquired.

### Bottleneck 2: Member 4 Pipeline Wiring (Internal Architectural Blocker)
- **Impacts:** Member 5 (Web UI), End-to-End Demorun.
- **Reality:** Member 1's OCR engine is ready for consumption. Member 4 has not yet imported `OCRService` into `apps/api/main.py`. Wiring this single connection immediately turns the API from a 100% fake mock into a real OCR web service.

### Bottleneck 3: Member 2 and Member 3 Scaffolds (Domain Logic Blocker)
- **Impacts:** Legal compliance assessment, physical font measurement, Section 36(1) notices.
- **Reality:** Even if an image is uploaded and OCR reads the text, without Member 2's coin calibration and Member 3's rule engine, the system cannot verify font heights or legal compliance.
