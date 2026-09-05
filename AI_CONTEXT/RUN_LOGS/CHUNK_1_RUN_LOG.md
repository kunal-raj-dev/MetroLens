# CHUNK 1: RUN LOG
**Project:** MetroLens AI (SIH26034)  
**Chunk:** Chunk 1 — OCR Model Feasibility Spike  
**Start Timestamp:** 2026-09-05T03:00:42+05:30

| Timestamp (UTC/IST) | Action | Tool / Subsystem | Purpose | Result / Artifact Created |
| :--- | :--- | :--- | :--- | :--- |
| **03:00:53** | Python Environment & Pip Audit | `run_command` (`python`, `pip list`) | Determine installed packages & Python version | Python 3.14.3 active; Pillow, psutil, fastapi installed; zero OCR packages installed. |
| **03:01:07** | Hardware & System Audit | `run_command` (`platform`, `psutil`) | Measure CPU cores, RAM, OS | Windows 11, AMD Ryzen 8C/16T, 15.31 GB RAM. |
| **03:01:19** | GPU Query Attempt | `run_command` (`nvidia-smi`) | Check GPU compute availability | Permission restricted; CPU-only execution confirmed mandatory. |
| **03:01:27** | Git State Inspection | `run_command` (`git log`, `git status`) | Check branch and working tree | Branch `main`, Commit `46a2a69`; working tree clean of commits. |
| **03:01:33** | Dataset Discovery | `find_by_name` in `data/`, `tests/` | Search for existing packaging images | Exactly 0 images found on disk in repository. |
| **03:02:10** | Context Structure Initialization | `write_to_file` | Establish `CURRENT_STATE/` and `AI_CONTEXT/` | Created `ENVIRONMENT_SNAPSHOT.md`, `GIT_STATE.md`, `DEPENDENCY_SNAPSHOT.md`, `PROJECT_SNAPSHOT.md`, `REPOSITORY_SNAPSHOT.md`, `CHUNK_1_STATUS.md`. |
| **03:02:48** | Pip Dependency Dry-Run | `run_command` (`pip install --dry-run`) | Evaluate wheel availability on Python 3.14 | Discovered `rapidocr-onnxruntime==1.2.3` provides native ONNX runtime without heavy PaddlePaddle dependencies. |
| **03:03:16** | RapidOCR Package Installation | `run_command` (`pip install rapidocr-onnxruntime`) | Install isolated lightweight OCR runner | Installed `rapidocr-onnxruntime`, `onnxruntime==1.29.0`, `opencv-python==5.0.0.93`, `shapely==2.1.2`, `numpy==2.5.2` in 8 seconds. |
| **03:08:27** | Monolingual English Test | Python inline test | Verify detection & recognition on synthetic sample | 792ms cold-start; recognized MRP, Net Qty, USP, Date with exact 4-point bounding boxes. |
| **03:09:04** | Hindi Script Isolation Test | Python inline test with `Nirmala.ttc` | Test if English/Chinese model recognizes Devanagari | **Discovery:** Default `ch_PP-OCR` model detected text region but failed to decode Devanagari characters due to dictionary limitation. |
| **03:09:39** | Devanagari ONNX Discovery | `search_web` & Hugging Face API | Locate official Devanagari ONNX model weights | Discovered `languages/hindi/rec.onnx` (8.56MB) and `dict.txt` (167 chars) in `monkt/paddleocr-onnx`. |
| **03:09:52** | Devanagari ONNX Download | `urllib.request` | Cache Hindi model locally | Downloaded to `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/models/hindi/`. |
| **03:13:01** | Hindi UTF-8 Recognition Test | Python inline execution | Verify Devanagari decoding with custom dict | **Confirmed:** Model correctly decoded Hindi text `अधिकतम` (MRP keyword) in $< 80\text{ms}$ recognition time. |
| **03:13:21** | Test Dataset Generation | `generate_synthetic_data.py` | Create 8 standardized FMCG test labels | Generated 8 specimens in `03_DATASET/images/` and `manifest.json` labeled `SYNTHETIC TEST — NOT REAL PACKAGING`. |
| **03:13:36** | Automated Benchmark Execution | `run_benchmark.py` | Run 120 inference passes across 3 candidates | Measuring latency, memory RSS, and field accuracy across EN, HI, and DUAL engines. |
| **03:14:15** | Benchmark Data Synthesis | Script extraction to `05_RESULTS/` | Generate CSV and JSON summaries | Created `summary.json` and `model_comparison.csv`. |
| **03:15:00** | Decision & Handoff Formalization | Document generation | Record provisional decision and Chunk 2 interface contract | Created `07_DECISION/OCR_MODEL_DECISION.md` and `HANDOFFS/CHUNK_1_TO_CHUNK_2.md`. |
| **03:16:35** | Analysis & Comparison Reports | Document generation | Complete detailed engineering spike analysis | Created `05_RESULTS/MODEL_COMPARISON.md` and `06_ANALYSIS/FINAL_SPIKE_REPORT.md`. |
| **03:16:53** | State & Status Finalization | Snapshot update | Mark Chunk 1 complete with empirical numbers | Updated `CURRENT_STATE/CHUNK_1_STATUS.md`. |
