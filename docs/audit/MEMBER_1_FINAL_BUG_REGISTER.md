# MEMBER 1 — FINAL BUG REGISTER

**Subsystem**: Member 1 — Multilingual OCR Engine & Service  
**Auditor**: Independent Principal Engineer  
**Date**: 2026-09-05  
**Freeze Status**: AUDITED & CLOSED  

---

| Field | Value |
| :--- | :--- |
| **Bug ID** | `BUG-001` |
| **Description** | Devanagari SVTR-HI Recognizer Logit Dimension / Character Dictionary Count Discrepancy |
| **Root Cause** | In `models/weights/ocr/rec_hi/dict.txt`, line 1 is an explicit space character (`' '`). `CTCLabelDecoder.__init__` evaluated `if " " not in self.character_list:` to `False`, skipping trailing space appending. The ONNX model `rec.onnx` has output dimension 169 classes, but `self.character_list` had 168 items. Any CTC argmax predicting class 168 was silently dropped without decoding or recording confidence. |
| **Severity** | HIGH |
| **Owner** | Member 1 (AI & OCR Lead) |
| **Fix Applied** | Modified `SVTRRecognizer.__init__` to inspect `session.get_outputs()[0].shape[-1]` and pass `expected_classes` to `CTCLabelDecoder`. Updated `CTCLabelDecoder.__init__` to dynamically pad trailing space tokens until `len(self.character_list) == expected_classes`. Both Latin (6625) and Devanagari (169) class counts now match ONNX outputs 100%. |
| **Regression Test** | `tests/unit/test_ocr_phase_b_independent_audit.py::test_devanagari_dictionary_dimension_alignment` |
| **Status** | RESOLVED & VERIFIED |
| **Residual Risk** | LOW. Synthetic tests and Hindi packaging specimens confirm stable decoding; full phonetic coverage on complex conjuncts requires future physical retail dataset evaluation. |

---

| Field | Value |
| :--- | :--- |
| **Bug ID** | `BUG-002` |
| **Description** | Inaccurate Benchmark Environment Metadata (Truncated SHA-256 Hashes and Incorrect Core Count) |
| **Root Cause** | In `benchmarks/ocr/final/environment.json`, Phase A hardcoded model filenames without directory prefixes (`models/ch_PP-OCRv3_det_infer.onnx`), truncated SHA-256 hash suffixes (`...27cf...` instead of actual `...030f...`), and recorded `cpu_count_logical: 12` (actual host has 16 logical cores). |
| **Severity** | MEDIUM |
| **Owner** | Member 1 / Benchmark Infrastructure |
| **Fix Applied** | Replaced `benchmarks/ocr/final/environment.json` with machine-verified hardware specs (16 logical cores, AMD Ryzen, Windows 11 Build 26200) and byte-calculated SHA-256 hashes matching disk files and `models/manifest.yaml` 100%. |
| **Regression Test** | `tests/unit/test_verification_pipeline.py::test_verify_dataset_manifest` |
| **Status** | RESOLVED & VERIFIED |
| **Residual Risk** | NONE. |

---

| Field | Value |
| :--- | :--- |
| **Bug ID** | `BUG-003` |
| **Description** | Unbounded "Zero Memory Leak" Claim in Phase A Documentation |
| **Root Cause** | Phase A documentation claimed "Zero memory leak" without qualifying that ONNX Runtime allocates internal scratch execution workspaces on initial inferences that cause RSS to rise from ~116 MB (post-warmup) to ~189 MB before stabilizing. |
| **Severity** | LOW |
| **Owner** | Member 1 / Architecture & Docs |
| **Fix Applied** | Corrected all performance and memory documentation to state exact measured reality: memory increases to ~189 MB during initial repeated inferences as ONNX Runtime thread pools and execution memory stabilize, after which memory remains bounded (+0.48 MB over 70 concurrent requests). |
| **Regression Test** | `AI_CONTEXT/EXPERIMENTS/MEMBER_1_PHASE_B_AUDIT/06_PERFORMANCE_AUDIT/test_memory_and_concurrency.py` |
| **Status** | RESOLVED & VERIFIED |
| **Residual Risk** | NONE. Host systems with >= 1 GB free RAM will experience zero OOM risk. |
