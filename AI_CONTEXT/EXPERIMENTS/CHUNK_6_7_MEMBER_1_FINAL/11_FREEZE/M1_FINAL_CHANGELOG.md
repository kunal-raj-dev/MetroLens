# Member 1 Final Changelog: Evolution from Feasibility to Freeze (Chunks 1–7)

**Project**: MetroLens AI (SIH26034)  
**Subsystem**: Member 1 — AI & Multilingual OCR Lead  
**Status**: **FROZEN & COMPLETED**

---

## Chunk 1: Architecture Inception & Model Selection Spike
- **Status**: Completed
- **Key Deliverables**:
  - Investigated PaddleOCR, EasyOCR, Tesseract, and standalone ONNX models.
  - Identified severe Python 3.14 C-extension build failures and dependency bloat in upstream PaddlePaddle.
  - Architectural Decision: Migrated entirely to pure, direct ONNX Runtime on CPU (`PP-OCRv3-ROUTED`).
  - Created initial benchmark harnesses and synthetic specimen dataset (`SYNTH-01` through `SYNTH-08`).

---

## Chunk 2: Engine Foundation & Multilingual Hardening
- **Status**: Completed
- **Key Deliverables**:
  - Implemented `nirikshak_ocr` direct engine (`detector.py`, `recognizer.py`, `engine.py`, `pipeline.py`).
  - Created dual-route recognition architecture to simultaneously support Latin and Devanagari text.
  - Sourced and validated `models/ch_PP-OCRv3_det_infer.onnx`, `models/ch_PP-OCRv3_rec_infer.onnx`, and `models/rec.onnx`.
  - Added 708-token Hindi dictionary `models/dict.txt` containing Hindi conjuncts and official Rupee symbol (`₹`).
  - Added cryptographic `models/manifest.yaml` with SHA-256 verification.

---

## Chunk 3: Real-Data Assessment & Path B Adoption
- **Status**: Completed
- **Key Deliverables**:
  - Assessed physical retail dataset availability on local disk.
  - Enacted **Path B**: Transparently documented that 0 physical retail packaging images exist on disk.
  - Benchmarked synthetic FMCG packaging specimens across English, Hindi, and bilingual labels.
  - Established scientific honesty rules: strictly disclaiming real-world >95% retail accuracy until physical images are gathered.
  - Hardened CWD-independent path discovery (`_default_root()` in `config.py`) to support arbitrary execution contexts.

---

## Chunk 4: Monorepo Integration & Service Adapter Layer
- **Status**: Completed
- **Key Deliverables**:
  - Integrated `packages/ocr` into the MetroLens monorepo.
  - Implemented `nirikshak_ocr.service.OCRService` providing 3 ingress modalities (file paths, raw bytes, canonical observations).
  - Integrated shared data contracts from `packages/shared/src/nirikshak_shared/ocr_contract.py` (`OCRObservation`, `OCRResult`, `BoundingPolygon`).
  - Implemented input immutability guard (`image.copy()`) preventing memory mutation.
  - Implemented thread safety lock (`_engine_lock`) and session warmup (`service.warmup()`).
  - Eliminated all lingering references to RapidOCR in documentation and test stubs.

---

## Chunk 5: Vertical Slice 0 Core Inspection Pipeline Integration
- **Status**: Completed
- **Key Deliverables**:
  - Validated end-to-end integration between Member 1 OCR, Member 2 Legal Rules, and Member 3 Physical Calibration in Vertical Slice 0.
  - Verified seamless data flow: Packaging Image -> `OCRService` -> `OCRObservation` -> Rule Engine -> Verdict.
  - Confirmed 100% test pass rate across all monorepo components.

---

## Combined Chunk 6 + Chunk 7: Hardening, Forensic Audit & Final Freeze
- **Status**: **FROZEN & CERTIFIED**
- **Key Deliverables**:
  - Hardened DoS defense: Implemented 64 Megapixel Decompression Bomb Guard (ADR-014) in `service.py`, rejecting oversize images in < 0.04 ms.
  - Added `test_decompression_bomb_guard()` bringing dedicated M1 tests to 64/64 (100% pass) and monorepo tests to 101/101 (100% pass).
  - Executed Final Release-Candidate Benchmark (`benchmarks/ocr/final/`):
    - Cold Engine Load: 481.14 ms | Cold Service Load: 451.38 ms | Warmup: 14.93 ms.
    - Warm Inference: English 139.18 ms, Hindi 115.79 ms, Bilingual 188.62 ms, Blank 49.68 ms.
    - Concurrency Sweep: 5.87 req/sec at 4 workers with 100% token consistency.
    - Memory RSS: Bounded at 406 MB after 250+ runs.
  - Conducted 35-question Independent Forensic Audit (`INDEPENDENT_AUDIT_REPORT.md`) with 100% satisfaction.
  - Published 22-section Final Source of Truth (`MEMBER_1_FINAL_SOURCE_OF_TRUTH.md`).
  - Published Frozen Components Registry (`MEMBER_1_DO_NOT_REBUILD.md`).
  - Delivered comprehensive handoffs to Members 2, 3, 4, 5, 6, and Project Lead.
  - Final Release Candidate Verdict: **`M1 RELEASE CANDIDATE — READY WITH KNOWN LIMITATIONS`**.
