# RUNTIME & DEPENDENCY COMPATIBILITY DECISION
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_2_OCR_ENGINE/02_RESEARCH/RUNTIME_DECISION.md`  
**Date:** 2026-09-05  
**Author:** Member 1 (AI & OCR Lead)  
**Status:** VALIDATED & APPROVED

---

## 1. Context & Problem Statement
The project host environment runs **Python 3.14.3 (64-bit)** on Windows 11.
Chunk 1 utilized `rapidocr-onnxruntime==1.2.3` as a fast feasibility wrapper.
However, an audit of upstream package metadata on PyPI reveals:
- Upstream `rapidocr-onnxruntime>=1.3` (current version 1.4.4) explicitly specifies:
  ```text
  Requires-Python: <3.13, >=3.6
  ```
- While version 1.2.3 omitted the metadata boundary and executes locally, relying on an unmaintained version with an upstream Python `<3.13` restriction introduces severe supply-chain fragility, container build failure risk, and unvetted behavior on Python 3.14+.

---

## 2. Evaluation of Options

### Option A: Use RapidOCR with Python 3.14
- **Pros:** Minimal initial refactoring.
- **Cons:** Explicitly unsupported by upstream metadata (`Requires-Python: <3.13`). In a clean Docker build or CI environment, `pip install rapidocr-onnxruntime` will fail on Python 3.14 without `--ignore-requires-python`.
- **Verdict:** **REJECTED** as a production dependency.

### Option B: Direct ONNX Runtime Implementation (`onnxruntime==1.29.0`)
- **Pros:**
  1. `onnxruntime==1.29.0` officially supports Python 3.14 on Windows and Linux with native `CPUExecutionProvider`.
  2. Eliminates all third-party wrapper overhead and dependency bloat.
  3. Gives direct control over `onnxruntime.SessionOptions` (e.g. `intra_op_num_threads`, `execution_mode`, memory pattern optimization).
  4. Postprocessing algorithms (DBNet binarization via OpenCV + polygon dilation via `pyclipper` and CTC greedy decoding) require only ~250 lines of clean, maintainable, typed Python code.
  5. Native support for script routing (selective invocation of SVTR-EN vs SVTR-HI).
  6. Reversible coordinate transforms and deterministic 4-point polygon guarantees.
- **Cons:** Requires maintaining DBNet++ postprocessing and CTC decoding internally.
- **Verdict:** **SELECTED AS PRIMARY ARCHITECTURE**.

### Option C: Downgrade Host Python Environment to 3.12
- **Pros:** Allows using RapidOCR wrapper.
- **Cons:** High disruption risk across the existing workspace, host system, and other monorepo tools. Unnecessary since `onnxruntime` 1.29.0 already runs stably on Python 3.14.
- **Verdict:** **REJECTED**.

---

## 3. Decision
Adopt **Option B: Direct ONNX Runtime Implementation**.
The `packages/ocr/` package will interact directly with `onnxruntime.InferenceSession`, using `numpy`, `opencv-python`, `pyclipper`, and `shapely`. All models will be loaded once into memory with configured CPU session options.
