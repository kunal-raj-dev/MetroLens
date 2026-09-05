# MetroLens AI — Comprehensive Project Map (Actual vs Planned)
**Audit Baseline Date:** 2026-09-05  
**Core Purpose:** Visual structural map contrasting actual implemented components against the planned target architecture.

---

## 1. End-to-End Architectural Pipeline Map

```
PROJECT: MetroLens AI (SIH26034)
│
├── 1. INPUT SUBSYSTEM
│   ├── PLANNED: Multi-panel mobile camera upload (front PDP, back, sides) with client-side EXIF stripping & magic-byte validation.
│   └── ACTUAL:  Direct file path or raw numpy byte array passed in Python script. Web upload is a static placeholder.
│
├── 2. VISION SUBSYSTEM (Quality Gate & Panel Segmentation)
│   ├── PLANNED: Pre-flight quality filter calculating discrete 2D Laplacian blur variance (<100) and HSV specular glare (>15%); unwarping via planar homography (3x3 H matrix).
│   └── ACTUAL:  [SCAFFOLD] packages/vision/src/nirikshak_vision/__init__.py computes np.var(gray) and counts pixels >= 250. Zero homography or unwarping code.
│
├── 3. OCR PERCEPTION SUBSYSTEM (Scene Text Extraction)
│   ├── PLANNED: Ultra-fast local CPU multilingual scene text extraction (<800ms) with rotated bounding boxes and English/Devanagari script routing.
│   └── ACTUAL:  [IMPLEMENTED & TESTED] packages/ocr/src/nirikshak_ocr/ (11 modules). DBNet++ ONNX detector + SVTR Latin & Devanagari recognizers + script router + OCRService adapter. Median latency ~109ms. 67 passing tests.
│
├── 4. MEASUREMENT & CALIBRATION SUBSYSTEM
│   ├── PLANNED: Automatic detection of coplanar reference anchor (₹10 coin, 27.0mm, or ISO card) to recover metric scale factor S (mm/px); conversion of text boxes to physical font height (mm) with MAE < 0.15mm.
│   └── ACTUAL:  [SCAFFOLD] packages/calibration/ and packages/measurement/ contain math division and multiplication stubs taking pre-measured numbers. Zero computer vision coin detection from images.
│
├── 5. EXTRACTION SUBSYSTEM (Semantic Parsing)
│   ├── PLANNED: Deterministic regex and heuristic entity extractors parsing 6 mandatory Rule 6 declarations: MRP, Net Qty, Mfg Date, Mfr Name, Country of Origin, Consumer Care.
│   └── ACTUAL:  [SCAFFOLD] packages/extraction/src/nirikshak_extraction/__init__.py contains a single regex pattern extracting MRP. Other 5 fields are completely unparsed.
│
├── 6. RULES ENGINE SUBSYSTEM (Legal Compliance State Machine)
│   ├── PLANNED: 100% deterministic compliance engine evaluating PCR 2011 Rules 6(1)(a)-(h), 6(11) USP arithmetic, Rule 7 font-to-area matrix, and Jan Vishwas Act 2026 into 5-State taxonomy.
│   └── ACTUAL:  [SCAFFOLD] packages/rules-engine/src/nirikshak_rules_engine/__init__.py checks 1 single rule (MRP presence). Rules for Net Qty, dates, font heights, and USP arithmetic do not exist.
│
├── 7. EVIDENCE SUBSYSTEM (Cryptographic Chain of Custody)
│   ├── PLANNED: Immutable forensic Directed Acyclic Graph (DAG) linking raw image SHA-256 to cropped bounding boxes, metric calibrations, rule evaluations, and officer overrides.
│   └── ACTUAL:  [SCAFFOLD] packages/evidence/src/nirikshak_evidence/__init__.py provides a hashlib SHA-256 helper and an EvidenceItem Pydantic factory. No Merkle graph structure or database storage.
│
├── 8. REPORTING SUBSYSTEM (Inspection Dossier Generation)
│   ├── PLANNED: Court-admissible signed PDF inspection report embedding raw & calibrated images, Rule 6 compliance checklist, measurement logs, and Section 36(1) Improvement Notices in <500ms.
│   └── ACTUAL:  [SCAFFOLD] packages/reporting/src/nirikshak_reporting/__init__.py renders 5 lines of plain text via ReportLab. No image crops, tables, or statutory notices.
│
└── 9. USER INTERFACE SUBSYSTEM (Web & API Gateways)
    ├── PLANNED: Responsive web application with drag-and-drop upload, 5-state status badge, interactive bounding-box canvas, declaration comparison table, and live demo SKU selector; backed by FastAPI server.
    └── ACTUAL:  [SCAFFOLD] apps/api/main.py returns hardcoded mock JSON without calling OCR or rules. apps/web/src/app/page.tsx is a static 40-line landing page with no interactive components.
```

---

## 2. Actual Code Execution Boundary

```
[User Input] 
     │
     ▼
[packages/ocr/src/nirikshak_ocr/service.py]  <─── FUNCTIONAL BOUNDARY STARTS HERE
     │ (Normalizes image to RGB numpy array)
     ▼
[packages/ocr/src/nirikshak_ocr/detector.py] 
     │ (Executes DBNet++ ONNX, binarizes, unclips polygons)
     ▼
[packages/ocr/src/nirikshak_ocr/router.py] 
     │ (Routes text crops to Latin vs Devanagari)
     ▼
[packages/ocr/src/nirikshak_ocr/recognizer.py]
     │ (Executes SVTR ONNX, greedy CTC decoding)
     ▼
[OCRObservation Tokens]                      <─── FUNCTIONAL BOUNDARY ENDS HERE
     │
     ▼
[PIPELINE BLOCKED — ALL DOWNSTREAM SUBSYSTEMS ARE HOLLOW SCAFFOLDS]
```
