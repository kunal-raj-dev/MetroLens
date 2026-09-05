# CURRENT STATE: CHUNK 5 BASELINE
**Document:** `CURRENT_STATE/CHUNK_5_BASELINE.md`  
**Generated:** 2026-09-05T15:38:00+05:30  
**Phase:** Member 1/Lead — Chunk 5 (Vertical Slice 0 Core Inspection Pipeline Integration)  
**Status:** BASELINE FROZEN  

---

## 1. Environment & Host Runtime
- **Operating System:** Windows 11 Home Single Language (10.0.26200 AMD64)
- **Python Runtime:** Python 3.14.3 (`C:\Python314\python.exe`)
- **Direct ONNX Runtime:** `onnxruntime==1.29.0` (CPUExecutionProvider, 4 intra-op threads)
- **Pytest:** `pytest-9.1.1`, `pluggy-1.6.0`
- **Total Test Suite:** **89 tests passing (100% pass rate in 12.93s–21.30s)**
- **Git State:** Working tree modified/untracked files only; HEAD `4681c47`; **Zero git commits created, zero git push performed**.

---

## 2. Monorepo Subsystem State Assessment

| Subsystem | Monorepo Path | Actual Code State | Actual Test Count | Reality Assessment |
| :--- | :--- | :--- | :--- | :--- |
| **OCR Perception** | `packages/ocr` | **IMPLEMENTED & HARDENED** (`nirikshak_ocr`) | 81 tests | Direct ONNX Runtime PP-OCRv3-ROUTED engine, B0 raw baseline default, P-Adaptive crop experimental, thread-safe `OCRService` adapter. |
| **Shared Contracts**| `packages/shared`| **IMPLEMENTED** (`nirikshak_shared.models`) | 5 tests | Pydantic DTOs: `OCRObservation`, `DeclarationField`, `MeasurementResult`, `RuleEvaluation`, `EvidenceItem`, `InspectionResult`. |
| **Image Quality** | `packages/vision`| **SCAFFOLDED** (`nirikshak_vision`) | 1 test (`test_vision_smoke.py`) | Basic `check_image_quality` with variance and high-luminance thresholding. |
| **Calibration** | `packages/calibration`| **SCAFFOLDED** (`nirikshak_calibration`) | 2 tests (`test_calibration_smoke.py`) | Basic `compute_scale_factor` math; no automated fiducial/coin detector. |
| **Measurement** | `packages/measurement`| **SCAFFOLDED** (`nirikshak_measurement`) | 3 tests (`test_measurement_smoke.py`) | Basic `calculate_font_height_mm` and `calculate_pdp_area_cm2`. |
| **Extraction** | `packages/extraction`| **SCAFFOLDED** (`nirikshak_extraction`) | 1 test (`test_extraction_smoke.py`) | Single regex searching for MRP only. Other Rule 6 fields absent. |
| **Rules Engine** | `packages/rules-engine`| **SCAFFOLDED** (`nirikshak_rules_engine`) | 2 tests (`test_rules_engine_smoke.py`) | Single rule evaluated: `LMPC-R06-MRP-001`. Net qty, date, font height rules un-evaluated. |
| **Evidence** | `packages/evidence`| **SCAFFOLDED** (`nirikshak_evidence`) | 2 tests (`test_evidence_smoke.py`) | Basic SHA-256 calculation and `EvidenceItem` factory. |
| **Reporting** | `packages/reporting`| **SCAFFOLDED** (`nirikshak_reporting`) | 1 test (`test_reporting_smoke.py`) | Minimal JSON/PDF stub. |
| **Backend API** | `apps/api` | **SCAFFOLDED / MOCKED** (`apps/api/main.py`) | 2 tests (`test_api_smoke.py`) | `POST /api/v1/inspections` returns hardcoded `COMPLIANT` dummy object. Real pipeline disconnected. |
| **Pipeline Worker**| `apps/worker` | **SCAFFOLDED** (`apps/worker/main.py`) | 2 tests (`test_worker_smoke.py`) | Calls quality gate and rules with `{}`; OCR and extraction completely bypassed. |
| **Frontend UI** | `apps/web` | **SCAFFOLDED** | 0 tests | Static landing page; disconnected from backend. |

---

## 3. Dataset & Ground Truth Status
- **Real Physical Dataset:** **0 physical retail packaging images on disk** under `data/raw/`.
- **Active Real-Data Gate:** **PATH B ENFORCED (REAL DATA BLOCKED)**.
- **Evaluation Specimens:** 8 synthetic regression specimens under `data/synthetic/regression/`.

---

## 4. Immediate Chunk 5 Challenge: The Integration Chasm
The repository possesses a fully working, production-grade OCR engine on one side, and detailed architecture specifications on the other. But the pipeline connecting `IMAGE → QUALITY → CALIBRATION → OCR → EXTRACTION → RULES → API RESULT` does not actually execute.

**Chunk 5 Mandate:** Build **Vertical Slice 0** — bridge this chasm with real, deterministic, testable code without mocks on the primary path.
