# CURRENT STATE: CHUNK 2 BASELINE
**Generated:** 2026-09-05T04:02:00+05:30  
**Phase:** Chunk 2 — OCR Engine Foundation  
**Role:** Member 1 (AI & OCR Lead)  
**Status:** BASELINE ESTABLISHED

---

## 1. Environment & Machine Profile
- **Date/Time:** 2026-09-05 04:02:00 IST
- **Operating System:** Windows 11 Home Single Language (64-bit, Build 26100)
- **CPU:** AMD Ryzen (8 Physical Cores / 16 Logical Threads)
- **RAM:** 15.31 GB Total Physical Memory
- **Python Version:** 3.14.3 (64-bit)
- **GPU Availability:** None / Restricted (`nvidia-smi` query restricted) $\rightarrow$ Strict CPU-only execution confirmed.

---

## 2. Git & Working Tree State
- **Branch:** `main`
- **HEAD Commit:** `4681c47` (*chore(test): configure root pytest settings and pythonpaths for monorepo*)
- **Working Tree State:** Clean tracking status; untracked context and compilation scripts present (`tools/build_all_in_one_context.py`). No files staged.

---

## 3. Installed OCR & CV Dependencies
- `onnxruntime==1.29.0`
- `rapidocr-onnxruntime==1.2.3`
- `opencv-python==5.0.0.93`
- `shapely==2.1.2`
- `numpy==2.5.2`
- `pillow==12.1.1`
- `psutil==7.2.2`

---

## 4. Current Model Assets on Disk
- **Devanagari SVTR Weights:** `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/models/hindi/rec.onnx` (8.56 MB)
- **Devanagari Character Dictionary:** `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/models/hindi/dict.txt` (167 lines / Unicode codepoints)
- **RapidOCR Default Assets (Local Cache):**
  - Detection: `ch_PP-OCRv3_det_infer.onnx` (2.32 MB)
  - Latin/CJK Recognition: `ch_PP-OCRv3_rec_infer.onnx` (10.20 MB)

---

## 5. Current Project Structure & Scaffolding
- Monorepo layout per `pytest.ini`:
  - `packages/shared/src/nirikshak_shared/models/contracts.py` (defines `OCRObservation`)
  - `packages/ocr/src/nirikshak_ocr/__init__.py` (minimal stub returning `[]`)
  - `apps/api/` (FastAPI service scaffold)
  - `apps/web/` (Next.js web application scaffold)
  - `apps/worker/` (Celery background worker scaffold)
- Data status:
  - `data/raw/`: 0 physical packaging images.
  - `AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET/images/`: 8 controlled synthetic specimens labeled `SYNTHETIC TEST — NOT REAL PACKAGING`.

---

## 6. Current API Contract (`docs/API_CONTRACT.md`)
- Downstream contracts reference `OCRObservation` with `token_id`, `text`, `confidence`, `bounding_box`, `polygon`, and `language`.
- Chunk 1 provisional handoff proposed `OCRToken` dataclass with `polygon` `[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]`.
- **Identified Defect to Correct:** Physical measurement ($h_{\text{mm}}$) and legal font compliance must NOT be mixed into OCR. Raw pixel height `raw_pixel_height` may be exposed as convenience geometry only, explicitly documented as NOT legal font height.

---

## 7. Chunk 1 Baseline Decision
- **Selected Architecture:** `PP-OCRv3-ROUTED` (provisional baseline).
- Shared DBNet++ detector + Script-Routed SVTR-EN and SVTR-HI ONNX sessions.
- Empirical benchmark on host CPU: cold load 632.61 ms, median warm latency ~710 ms (serial was 1227 ms), RSS 157–162 MB, 100% offline, Apache-2.0.
