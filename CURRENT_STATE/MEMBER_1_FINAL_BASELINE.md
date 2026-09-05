# MEMBER 1 FINAL BASELINE: STARTING ENVIRONMENT SNAPSHOT

**Project**: MetroLens AI™ (SIH26034)  
**Lead**: Member 1 — AI & Multilingual OCR Lead  
**Phase**: Combined Chunk 6 + Chunk 7 (Final Implementation, Forensic Audit & Freeze)  
**Snapshot Timestamp**: 2026-09-05T16:00:00+05:30  

---

## 1. Host Hardware & System Environment
- **Operating System**: Windows 11 Home Single Language (Build 26200.5670, SP0)
- **Architecture**: AMD64 (x86_64)
- **CPU**: AMD Ryzen Processor (8 Cores, 16 Threads)
- **Total Physical RAM**: 15.31 GB
- **Python Version**: 3.14.3 (tags/v3.14.3:323c59a, Feb 3 2026) [MSC v.1944 64 bit (AMD64)]
- **CWD**: `c:\Users\kunal\Desktop\MetroLens`

## 2. Git State & Version Control Invariants
- **Current Branch**: Active working branch
- **Git HEAD**: `f25d15a` (`feat(ocr): deliver Member 1 core OCR engine, pipeline integration, and benchmarks`)
- **Working Tree**: Modified/untracked working files from Chunk 5 integration
- **Git Safety Rule**: **ZERO COMMITS, ZERO PUSHES ENFORCED**. Working tree remains uncommitted until explicitly authorized by user.

## 3. Runtime & Neural Framework Verification
- **Inference Runtime**: Direct `onnxruntime==1.29.0`
- **Execution Provider**: `CPUExecutionProvider` (4 intra-op threads, 1 inter-op thread)
- **RapidOCR Wrapper**: **ABSENT** in production execution (verified via grep search; legacy mention in README only).
- **Paddle / PaddlePaddle Runtime**: **ABSENT** (zero runtime imports or dependencies).
- **Network Downloads**: **DISABLED / ABSENT** (all model weights and dictionaries are stored locally).

## 4. Model Weights & Asset Audit
All weights stored under `models/weights/ocr/` and verified against `models/manifest.yaml`:
1. **Detection Model**: `models/weights/ocr/det/ch_PP-OCRv3_det_infer.onnx`
   - Architecture: DBNet++ Mobile (Lightweight scene text detector)
   - Size: 2,432,880 bytes (2.32 MB)
   - SHA-256: `3439588c030faea393a54515f51e983d8e155b19a2e8aba7891934c1cf0de526` (MATCH CONFIRMED)
   - License: Apache-2.0
2. **Latin/English Recognizer**: `models/weights/ocr/rec_en/ch_PP-OCRv3_rec_infer.onnx`
   - Architecture: SVTR-LCNet alphanumeric CTC recognizer (embedded dictionary)
   - Size: 10,690,752 bytes (10.19 MB)
   - SHA-256: `897a3ededb38fee0dae2c1ccee38241f37df202c9509e3abca02e9217c5ee615` (MATCH CONFIRMED)
   - License: Apache-2.0
3. **Devanagari/Hindi Recognizer**: `models/weights/ocr/rec_hi/rec.onnx`
   - Architecture: SVTR Devanagari CTC recognizer
   - Size: 8,980,224 bytes (8.56 MB)
   - SHA-256: `43df175fa3c877fbf7bcc4e5bd1e203e24ec450cd3ea96c9e802c86e39a4d4cf` (MATCH CONFIRMED)
   - Dictionary: `models/weights/ocr/rec_hi/dict.txt` (167 characters)
   - Dict Size: 708 bytes | Dict SHA-256: `b5f1be6d8bbff1a19fb96c5d4ca96a423380234bb7d2ce0e07b5838adb4d18ea` (MATCH CONFIRMED)
   - License: Apache-2.0

## 5. Member 1 Package Status
- **Package Name**: `nirikshak_ocr`
- **Installation**: Installed in editable mode (`pip install -e packages/ocr --no-deps`)
- **Public Classes**: `OCREngine`, `OCRService`, `OCRConfig`, `OCRToken`, `OCRResult`, `ScriptType`, `ScriptRouter`, `DBNetDetector`, `SVTRRecognizer`
- **Import Verification**: Successfully imports from repo root, subdirectories, and external working directories with zero `sys.path` hacks.

## 6. Test Suite & Benchmark Baseline
- **Dedicated Member 1 OCR Tests**: 63 automated tests (100% passing in 21.53s).
- **Monorepo Integration Suite**: 100 automated tests passing across monorepo.
- **Offline Guard**: Verified via `test_ocr_strictly_offline` and `test_offline_execution_socket_guard` (zero network calls).
- **Current Default Preprocessing**: `B0_BASELINE_RAW` (`preprocessing_mode="raw"`).
- **Provisional Preprocessing**: `P_ADAPTIVE_CROP` (`preprocessing_mode="adaptive"`).

## 7. Real-Data Status: PATH B ENFORCED
- **Physical Retail Images on Disk**: 0 (ZERO).
- **Real Packaging Accuracy / CER / WER**: **PENDING / BLOCKED AWAITING MEMBER 6 PHYSICAL DATASET COLLECTION**.
- **Synthetic Packaging Status**: 7 synthetic packaging fixtures under `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET/images/` used exclusively for deterministic pipeline plumbing, geometric regression, and integration testing.
- **No-Fabrication Protocol**: No real-world accuracy claims are made based on synthetic specimens.
