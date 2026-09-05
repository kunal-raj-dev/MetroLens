# RESEARCH EVIDENCE PACK E — DATASETS & ACQUISITION REGISTRY

**Research Scope:** Public Datasets for Indic OCR, Scene Text, Packaging Labels, Curved Text, and Synthetic Procedural Datasets  
**Audit Execution Date:** 2026-09-04  
**Integrity Standard:** Strict Provenance & License Verification (Policy: Unclear rights = `RIGHTS_VERIFICATION_REQUIRED`)  
**Pack Status:** 🔴 CRITICAL (Verified Primary & Secondary)

---

## 1. Executive Summary & Data Governance Rules

In Legal Metrology inspection, computer vision models face unique challenges: high-contrast background clutter, metallic foil reflections, cylindrical label curvature, multilingual packaging (English, Hindi, and regional scripts), and tiny font sizes.

### Non-Negotiable Data Rules:
1. **Web Scraping Prohibition:** Mass scraping of commercial e-commerce websites is strictly **`REJECTED — PROHIBITED BY POLICY`**.
2. **Trade Dress & Copyright:** Physical commercial product packaging labels purchased at retail represent public statutory disclosures under Section 18 of the Legal Metrology Act; packaging graphic artwork and logos are classified as **`RIGHTS_VERIFICATION_REQUIRED`** for public distribution outside fair-dealing evaluation.
3. **Synthetic Ground Truth:** Nirikshak utilizes a deterministic procedural label generator (`SRC-SYNTH-PROC-01`) to empirically validate font measurement math with absolute sub-pixel ground truth before testing on physical camera captures.

---

## 2. Public Dataset Registry

### 2.1 Bharat Scene Text Dataset (BSTD)
- **Official URL:** `https://github.com/AI4Bharat/BharatSceneText` / `https://arxiv.org/abs/2109.06004`
- **Owner:** AI4Bharat / IIT Bombay / IIIT Hyderabad
- **License:** MIT License / CC BY-NC 4.0 (Research use)
- **Download Availability:** Publicly available on GitHub / Hugging Face.
- **Commercial Use:** Restricted for NC partitions; Permissive for open benchmarks.
- **Redistribution:** Allowed with attribution under academic license.
- **Language:** Multilingual (11 Indian languages: Hindi, Bengali, Tamil, Telugu, Gujarati, Marathi, etc., plus English).
- **Country Relevance:** India (High - native Indian signage, packaging, and street text).
- **Image Type:** In-the-wild scene text photos (natural lighting, perspective distortion, diverse fonts).
- **Annotation Type:** Word-level bounding polygons and ground-truth text transcriptions.
- **Dataset Size:** 100,000+ annotated word instances.
- **Date / Version:** 2021 (v1.0).
- **Limitations:** Predominantly street scenes and signboards; packaging labels form a subset, requiring transfer learning.
- **Governance Status:** `VERIFIED_SECONDARY`

---

### 2.2 IndicSTR12 (Indic Scene Text Recognition 12)
- **Official URL:** `https://www.kaggle.com/datasets/indicstr12` / `https://arxiv.org/abs/2203.15340`
- **Owner:** Academic consortium (CVPR / ICDAR benchmark contributors)
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Download Availability:** Public download on Kaggle and academic mirrors.
- **Commercial Use:** Allowed with attribution.
- **Redistribution:** Allowed.
- **Language:** 12 major Indian languages (Devanagari, Gurmukhi, Gujarati, Odia, Bengali, Assamese, Telugu, Kannada, Tamil, Malayalam, Urdu, English).
- **Country Relevance:** India (High).
- **Image Type:** Cropped real-world word images exhibiting blur, occlusion, motion, and perspective distortion.
- **Annotation Type:** Word image with text label.
- **Dataset Size:** 27,000+ cropped word images.
- **Date / Version:** 2022.
- **Limitations:** Word-level recognition benchmark; does not provide full-document layout or bounding coordinates for PDP area calculation.
- **Governance Status:** `VERIFIED_SECONDARY`

---

### 2.3 IIIT-ILST (Indic Language Scene Text)
- **Official URL:** `http://cvit.iiit.ac.in/research/projects/cvit-projects/ilst`
- **Owner:** Centre for Visual Information Technology (CVIT), IIIT Hyderabad
- **License:** Academic Research Non-Commercial License
- **Download Availability:** Available upon request / open academic download.
- **Commercial Use:** Prohibited without institutional license.
- **Redistribution:** Prohibited.
- **Language:** Hindi, Telugu, Malayalam, English.
- **Country Relevance:** India (High).
- **Image Type:** Focused scene text images across Indian urban environments.
- **Annotation Type:** Word-level bounding boxes and transcriptions.
- **Dataset Size:** ~1,000 images, 15,000 text instances.
- **Date / Version:** 2014–2016.
- **Limitations:** Older benchmark; smaller size than BSTD; non-commercial restriction.
- **Governance Status:** `VERIFIED_SECONDARY`

---

### 2.4 OpenFoodFacts India Product Image Database
- **Official URL:** `https://world.openfoodfacts.org/country/india`
- **Owner:** Open Food Facts Non-Profit Association
- **License:** Open Database License (ODbL) v1.0; Images under CC BY-SA 3.0
- **Download Availability:** Direct download via public AWS S3 dumps and REST API.
- **Commercial Use:** Permitted under ODbL share-alike conditions.
- **Redistribution:** Permitted with ODbL license notice.
- **Language:** English, Hindi, and regional scripts.
- **Country Relevance:** India (High — real Indian consumer FMCG packaging).
- **Image Type:** Uncurated smartphone photos taken by consumers under varied lighting.
- **Annotation Type:** Barcode GTIN, ingredient list, front/back/ingredients image URLs. No pixel bounding boxes for font heights.
- **Dataset Size:** 30,000+ Indian product entries with multi-panel photos.
- **Date / Version:** Daily updated (Current 2024–2026).
- **Limitations:** High variance in photo quality; lacks bounding box annotations for Table-I numerals and PDP area; requires team annotation.
- **Governance Status:** `VERIFIED_SECONDARY`

---

### 2.5 Total-Text (Curved & Arbitrary-Shaped Text Benchmark)
- **Official URL:** `https://github.com/cs-chan/Total-Text-Dataset`
- **Owner:** University of Malaya
- **License:** Academic Research License
- **Download Availability:** Public GitHub repository.
- **Commercial Use:** Non-commercial evaluation.
- **Redistribution:** Permitted for research.
- **Language:** English.
- **Country Relevance:** International benchmark.
- **Image Type:** Curved, horizontal, and multi-oriented text in real scenes.
- **Annotation Type:** Polygon bounding coordinates (up to 16 points per word) and text transcriptions.
- **Dataset Size:** 1,555 images, 11,459 text instances.
- **Date / Version:** 2017–2019.
- **Limitations:** English only; benchmark for validating dewarping and curved text detection algorithms on cylindrical bottles and cans.
- **Governance Status:** `VERIFIED_SECONDARY`

---

## 3. Project-Generated Datasets

### 3.1 Nirikshak Synthetic Procedural Label Dataset (`SRC-SYNTH-PROC-01` / `DS-SYNTH-001`)
- **Owner:** Project Nirikshak Team
- **License:** CC0-1.0 (Public Domain Dedication for generated procedural layouts)
- **Download Availability:** Procedural generation script planned (`scripts/data_prep/generate_synthetic_labels.py`).
- **Commercial Use:** Permissive (for generated geometries).
- **Redistribution:** Permissive (upon generation).
- **Language:** English, Hindi (Devanagari Unicode fonts).
- **Country Relevance:** India (Statutory Table-I and Rule 6 compliance testing).
- **Image Type:** Synthetic high-resolution renders ($300\text{ DPI}$) with known millimeter text heights ($1.0\text{ mm}$, $2.0\text{ mm}$, $2.5\text{ mm}$, $4.0\text{ mm}$, $6.0\text{ mm}$) overlaid on planar and simulated cylindrical surfaces with artificial glare, shadow, and blur.
- **Annotation Type:** Exact mathematical ground truth (pixel-perfect bounding boxes, cap-height, x-height, stroke width, text transcription, PDP area in $\text{cm}^2$).
- **Dataset Size:** 1,000 procedurally generated label configurations (`PLANNED TARGET ONLY — NOT GENERATED ON DISK: 0 files exist`).
- **Date / Version:** Stage 2 Planned Generation.
- **Limitations:** Synthetic; does not capture physical printing micro-defects or real-world paper textures.
- **Dataset Status:** `PLANNED`
- **Artifact Status:** `NOT_GENERATED`
- **Governance Status:** `PLANNED`

---

### 3.2 Nirikshak Retail Packaging Field Corpus (`SRC-TEAM-FIELD-01` / `DS-RETAIL-PILOT-001`)
- **Owner:** Physical retail procurement by Nirikshak Engineering Team (Delhi-NCR retail markets).
- **Rights Breakdown:**
  - **IMAGE RIGHTS:** `RIGHTS_VERIFICATION_REQUIRED` (Photographic reproduction of commercial packaging trade dress lacks binding statutory exemption; fair dealing opinion pending).
  - **ANNOTATION RIGHTS:** `RIGHTS_VERIFICATION_REQUIRED` (Bounding polygons, character heights, and text transcriptions pending formal project licensing dedication).
  - **TRADEMARK / TRADE DRESS:** Proprietary to respective trademark holders; not owned, licensed, or assignable by the Nirikshak team.
  - **REDISTRIBUTION RIGHTS:** `RESTRICTED` (Public redistribution prohibited pending legal rights clearance).
  - **PUBLICATION RIGHTS:** `RESTRICTED` (Restricted to internal research and confidential review).
  - **HACKATHON DEMONSTRATION RIGHTS:** `RIGHTS_VERIFICATION_REQUIRED` (Non-commercial academic evaluation defense pending formal sign-off).
- **Download Availability:** Stage 2 planned physical acquisition.
- **Commercial Use:** Prohibited without trademark holder clearance.
- **Language:** English, Hindi.
- **Country Relevance:** India (Ground truth consumer packaging).
- **Image Type:** Calibrated smartphone photos with ArUco fiducial target under controlled and uncontrolled lighting.
- **Annotation Type:** Digital caliper measurements ($\pm 0.02\text{ mm}$ physical ground truth), manual bounding polygons, statutory compliance ground truth labels.
- **Dataset Size:** 50 physical SKUs (`PLANNED TARGET: 20 rectangular cartons, 15 cylindrical cans/bottles, 15 stand-up pouches; currently 0 collected on disk`).
- **Date / Version:** Stage 2 Planned Acquisition.
- **Dataset Status:** `PLANNED`
- **Artifact Status:** `DECLARED_BUT_MISSING`
- **Governance Status:** `RIGHTS_VERIFICATION_REQUIRED`
