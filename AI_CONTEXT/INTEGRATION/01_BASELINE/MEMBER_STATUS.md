# Member Baseline Status — M1 through M5

**Audit Date:** September 2026  
**Auditor:** MetroLens System Integration Lead  
**Monorepo:** `c:\Users\kunal\Desktop\MetroLens`  

---

## 1. Executive Status Summary

| Member Subsystem | Ownership Scope | Implementation State | Test Suite Status | Mock Status | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Member 1 (M1)** | OCR, Detection, Recognition, Post-Processing | Production-Ready (Local CPU) | 165+ Unit/Int Tests Pass | **100% Real ONNX Engine** | **FULLY FUNCTIONAL** |
| **Member 2 (M2)** | Optical Calibration, Reference Card, Coin | Functional Pipeline | 180+ Unit Tests Pass | **Functional algorithm; synthetic card fixtures** | **BLOCKED ON M6 REAL IMAGES** |
| **Member 3 (M3)** | Legal Metrology Rules Engine (PCR 2011) | Production-Ready Pure Logic | 210+ Unit Tests Pass | **Zero mocks; pure deterministic Python** | **FULLY FUNCTIONAL** |
| **Member 4 (M4)** | FastAPI Backend, PDF Reporting, Evidence | Production-Ready | 180+ Unit/Int Tests Pass | **Real ReportLab PDF; mock review endpoint** | **FUNCTIONAL WITH NOTED GAPS** |
| **Member 5 (M5)** | Next.js Web Frontend, Canvas, Dashboard | Production-Ready React 19 | 174 Vitest Tests Pass | **Dual Mode (Live API + Mock Synthetic)** | **FULLY FUNCTIONAL** |

---

## 2. Member 1: OCR & Perception Engine
- **Primary Package:** `packages/ocr`, `packages/extraction`, `packages/vision`
- **Models Present:**
  - `packages/ocr/src/nirikshak_ocr/models/det/ch_PP-OCRv3_det_infer.onnx` (2.4 MB)
  - `packages/ocr/src/nirikshak_ocr/models/rec_en/ch_PP-OCRv3_rec_infer.onnx` (10.7 MB)
  - `packages/ocr/src/nirikshak_ocr/models/rec_hi/rec.onnx` (8.9 MB) + `dict.txt` (74.7 KB)
- **Runtime Reality:**
  - Operates locally via `rapidocr-onnxruntime` using CPU inference.
  - Zero cloud API dependency (Tesseract / Cloud Vision NOT required).
  - Handles English and Devanagari Hindi text cleanly.
  - Generates bounding boxes, text strings, and character-level confidence scores.

## 3. Member 2: Computer Vision & Calibration
- **Primary Package:** `packages/calibration`, `packages/measurement`
- **Capabilities:**
  - Laplacian variance blur detection gate.
  - 27.0mm Indian 1-Rupee coin reference anchor detection.
  - Metric scale recovery in mm/pixel.
  - Principal Display Panel (PDP) bounding box estimation.
- **Runtime Reality:**
  - Code is mathematically sound and algorithmic.
  - Passes all synthetic test suites (SYNTH-01 to SYNTH-08).
  - **Limitation:** Fails to detect calibration anchors on uncurated consumer photos without reference targets (e.g. Dairy Milk Bubbly packet without a coin/card placed beside it). Correctly falls back to `UncalibratedModeResult`.

## 4. Member 3: Legal Metrology Rules Engine
- **Primary Package:** `packages/rules-engine` (`nirikshak-rules-engine`)
- **Statutory Scope:**
  - Legal Metrology Act, 2009 & Packaged Commodities Rules (PCR), 2011.
  - Jan Vishwas (Amendment) Act, 2023 / 2026 decriminalized compounding penalty schedules.
  - Rule 6(1): Mandatory Declarations (MRP, Net Qty, Mfg Date, Consumer Care, Packer/Importer).
  - Rule 6(11): Unit Sale Price (USP) arithmetic validation.
  - Schedule II: Font height compliance relative to PDP area.
  - Section 36(1): Non-compliance notice generation.
- **Runtime Reality:**
  - 100% deterministic Python rule trees.
  - No external service calls; instantaneous execution (< 1 ms per evaluation).

## 5. Member 4: Backend API & Evidentiary Reporting
- **Primary Package:** `apps/api`, `packages/reporting`, `packages/evidence`
- **Endpoints Verified:**
  - `GET /health` -> HTTP 200 `{"status": "ok"}`
  - `POST /api/v1/inspect` -> Full multipart/form-data analysis pipeline
  - `POST /api/v1/report/pdf` -> Binary ReportLab PDF generation (SHA-256 sealed)
- **Runtime Reality:**
  - End-to-end pipeline connects M1, M2, M3 into a single execution payload.
  - Security gates enforce image format, size, and minimum 800x600 resolution.
  - **Missing Endpoint:** `POST /api/v1/inspections/{id}/review` is not yet implemented (returns 404), causing M5 inspector review override to remain client-side only.

## 6. Member 5: Web Frontend Experience
- **Primary Package:** `apps/web` (Next.js 16.1.6, React 19.2.3, Tailwind CSS v4)
- **Key Features:**
  - Zero-conversion invariant: displays pure backend units, performs no frontend legal adjudication.
  - High-precision dual-layer HTML5 Canvas with pinch-zoom, pan, and millimeter overlay.
  - Dual Mode architecture: switches seamlessly between Live API (`/api/v1`) and Mock Synthetic mode.
  - WCAG AA compliant contrast and full keyboard navigation.
