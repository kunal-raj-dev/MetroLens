# MEMBER 1 — PHASE B AUDIT BASELINE SNAPSHOT

**Role**: Independent Principal Engineer  
**Timestamp**: 2026-09-05T16:08:00+05:30  
**Phase**: Phase B Forensic Audit, Validation, Debugging & Freeze Gate  
**Monorepo**: MetroLens AI™ (SIH26034)  
**Target Subsystem**: Member 1 — Core Multilingual OCR Subsystem (`packages/ocr`)  

---

## 1. Version Control & Working Tree State
- **Current Branch**: `kunal-member-1-work` (tracking `origin/kunal-member-1-work`)
- **Current Git HEAD**: `f25d15a` (`feat(ocr): deliver Member 1 core OCR engine, pipeline integration, and benchmarks`)
- **Working Tree State**: Uncommitted modifications present from previous Phase A delivery (`apps/api/main.py`, `packages/ocr/src/nirikshak_ocr/service.py`, `packages/shared/src/nirikshak_shared/models/contracts.py`, `tests/integration/test_ocr_service_integration.py`, etc.) and untracked files (`tests/integration/test_vertical_slice_0.py`, `docs/audit/`, `benchmarks/ocr/final/`, `benchmarks/vertical_slice_0/`).
- **Git Safety Invariant**: **NO GIT COMMIT, NO GIT PUSH, NO GIT HISTORY MODIFICATION**. All work in Phase B is strictly read/write in working tree without creating Git commits or pushing upstream.

---

## 2. Hardware & Host Operating Environment
- **Operating System**: Windows 11 Home Single Language (10.0.26200-SP0)
- **Architecture**: AMD64 (x86_64)
- **CPU**: AMD Ryzen Processor (8 physical cores, 16 logical cores, AMD64 Family 25 Model 117 Stepping 2)
- **Total RAM**: 15.31 GB physical RAM
- **Python Version**: 3.14.3 (`tags/v3.14.3:323c59a`, Feb 3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)]
- **Executable**: Active Python 3.14 interpreter environment
- **Working Directory**: `c:\Users\kunal\Desktop\MetroLens`

---

## 3. Inference Runtime & Package Dependencies
- **ONNX Runtime**: `1.29.0`
- **Available Providers**: `['AzureExecutionProvider', 'CPUExecutionProvider']`
- **Active Execution Provider**: `CPUExecutionProvider` (configured intra-op: 4, inter-op: 1)
- **Direct Dependencies**:
  - `numpy`: `2.5.2`
  - `opencv-python`: `5.0.0.93`
  - `pydantic`: `2.13.4`
  - `shapely`: `2.1.2`
  - `pyclipper`: `1.4.0`
  - `onnxruntime`: `1.29.0`
  - `pyyaml`: `6.0.3`
  - `pytest`: `9.1.1`
- **Legacy / Wrapper Packages**:
  - `rapidocr-onnxruntime`: `1.2.3` (Installed in environment, but strictly NOT imported in production `nirikshak_ocr` execution; verified via forensic code audit).
  - `paddlepaddle`: ABSENT (Zero Paddle runtime).
  - `torch` / `tensorflow`: ABSENT (Zero heavy deep learning framework dependencies).
  - Cloud OCR SDKs: ABSENT (Zero AWS Textract, Google Cloud Vision, Azure AI Vision).

---

## 4. Model Asset Provenance & Integrity
All active models reside locally under `models/weights/ocr/` and were independently hashed via SHA-256:

| Model ID | File Path | Size (Bytes) | SHA-256 Hash | Status vs Manifest |
| :--- | :--- | :--- | :--- | :--- |
| `ch_PP-OCRv3_det_infer` | `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx` | 2,432,880 | `3439588c030faea393a54515f51e983d8e155b19a2e8aba7891934c1cf0de526` | MATCH (100%) |
| `ch_PP-OCRv3_rec_infer` | `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx` | 10,690,752 | `897a3ededb38fee0dae2c1ccee38241f37df202c9509e3abca02e9217c5ee615` | MATCH (100%) |
| `hindi_PP-OCRv3_rec_infer` | `models/weights/ocr/rec_hi/rec.onnx` | 8,980,224 | `43df175fa3c877fbf7bcc4e5bd1e203e24ec450cd3ea96c9e802c86e39a4d4cf` | MATCH (100%) |
| `hindi_dict` | `models/weights/ocr/rec_hi/dict.txt` | 508 | `b5f1be6d8bbff1a19fb96c5d4ca96a423380234bb7d2ce0e07b5838adb4d18ea` | MATCH (100%) |

---

## 5. Test Suite & Benchmark Baseline
- **Collected Test Count**: 101 tests across the monorepo.
- **Test Results**: 101 PASSED, 0 FAILED, 1 warning (`StarletteDeprecationWarning` regarding httpx in fastapi testclient).
- **Execution Time**: 24.31 seconds.
- **Dedicated OCR Unit & Integration Tests**: 63 tests directly exercising `nirikshak_ocr` and `nirikshak_shared`.
- **Existing Benchmark Suites**:
  - `benchmarks/ocr/chunk2/`: Legacy RapidOCR baseline.
  - `benchmarks/ocr/chunk3/`: Direct ONNX Runtime & Preprocessing benchmarks.
  - `benchmarks/ocr/chunk4/`: OCRService integration benchmarks.
  - `benchmarks/ocr/final/`: Phase A final benchmark draft.
  - `benchmarks/vertical_slice_0/`: Cross-member pipeline benchmark.

---

## 6. Dataset Provenance & Real Data Count
- **Physical Real Packaging Images on Disk**: **0 (ZERO)**.
- **Synthetic Packaging Test Images**: 8 synthetic specimens (`SYNTH-01` to `SYNTH-08`) located at `data/synthetic/regression/` and mirrored in `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET/images/`.
- **Real-Data Audit Verdict**: **REAL DATA VALIDATION = NOT VERIFIED / PENDING**.
- **Audit Rule**: Zero fabrication of real-world retail numbers. All measured metrics strictly reflect synthetic regression fixtures.
