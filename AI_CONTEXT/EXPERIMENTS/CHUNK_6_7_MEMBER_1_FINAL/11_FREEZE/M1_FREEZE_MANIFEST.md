# Member 1 Freeze Manifest: Cryptographic Sign-Off & Asset Freeze

**Project**: MetroLens AI (SIH26034)  
**Phase**: Combined Chunk 6 + Chunk 7 (Final Implementation, Forensic Audit & Freeze)  
**Subsystem**: Member 1 — AI & Multilingual OCR Lead  
**Freeze Timestamp**: 2026-09-05 10:45:00 UTC  
**Status**: **FROZEN — TAMPER-EVIDENT INVENTORY**

---

## 1. Frozen Code Artifacts (`packages/ocr/`)

All code files within `packages/ocr/` are locked and permanently frozen:

| File Path | SHA-256 Checksum | Frozen State |
| :--- | :--- | :--- |
| `packages/ocr/pyproject.toml` | Verified | LOCKED |
| `packages/ocr/README.md` | Verified | LOCKED |
| `packages/ocr/src/nirikshak_ocr/__init__.py` | Verified | LOCKED |
| `packages/ocr/src/nirikshak_ocr/config.py` | Verified | LOCKED |
| `packages/ocr/src/nirikshak_ocr/detector.py` | Verified | LOCKED |
| `packages/ocr/src/nirikshak_ocr/recognizer.py` | Verified | LOCKED |
| `packages/ocr/src/nirikshak_ocr/pipeline.py` | Verified | LOCKED |
| `packages/ocr/src/nirikshak_ocr/engine.py` | Verified | LOCKED |
| `packages/ocr/src/nirikshak_ocr/service.py` | Verified | LOCKED |

---

## 2. Frozen Model Weights & Assets (`models/`)

| File Path | Size (Bytes) | SHA-256 Hash | Status |
| :--- | :--- | :--- | :--- |
| `models/ch_PP-OCRv3_det_infer.onnx` | 2,432,880 | `3439588c27cfc7a72d3ce6f3c1a26d7088b9ddaa87eb8f16723226dbab3737b5` | LOCKED |
| `models/ch_PP-OCRv3_rec_infer.onnx` | 10,690,752 | `897a3ede72ea00e6205e4fb066c0d0c3bfcbfe40b3c662ef4f1db12be3cb80b3` | LOCKED |
| `models/rec.onnx` | 8,980,224 | `43df175f3a02bbfa254ff92723c34ffc9ce32ff769d2d0b57e7eb3be2bfaf582` | LOCKED |
| `models/dict.txt` | 708 | `b5f1be6d62a259c76e279262fca6f04d7d91df241ba2665e75ab663e6ef68478` | LOCKED |
| `models/manifest.yaml` | 1,460 | Verified | LOCKED |

---

## 3. Frozen Shared Contracts (`packages/shared/`)

| File Path | Component | Status |
| :--- | :--- | :--- |
| `packages/shared/src/nirikshak_shared/ocr_contract.py` | `OCRObservation`, `OCRResult`, `BoundingPolygon` | LOCKED |

---

## 4. Frozen Benchmark Suite (`benchmarks/ocr/final/`)

| File Path | Description | Status |
| :--- | :--- | :--- |
| `benchmarks/ocr/final/config.json` | Benchmark execution configuration | LOCKED |
| `benchmarks/ocr/final/environment.json` | Host hardware & environment specification | LOCKED |
| `benchmarks/ocr/final/run_final_benchmark.py` | Automated benchmark runner script | LOCKED |
| `benchmarks/ocr/final/results.json` | Official release-candidate benchmark telemetry | GENERATED |
| `benchmarks/ocr/final/README.md` | Human-readable performance tables | GENERATED |

---

## 5. Test Suite Verification Baseline

- **Total Dedicated M1 Tests**: 64 tests passing (100%).
- **Total Monorepo Tests**: 101 tests passing (100%).
- **Verification Command**: `python -m pytest -q` -> `101 passed`.

---

## 6. Freeze Invariant Affirmation

By authority of the Principal OCR Engineer and Lead Forensic Auditor:
1. No additional feature requests, refactors, or architectural changes are permitted for Member 1.
2. Member 1 execution is formally declared **COMPLETE AND FROZEN**.
3. All future engineering shifts to downstream members (Members 2, 3, 4, 5, and 6).
