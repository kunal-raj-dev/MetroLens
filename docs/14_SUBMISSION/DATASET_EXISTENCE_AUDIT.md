# NIRIKSHAK — DATASET EXISTENCE & PHANTOM DATA FORENSIC AUDIT

**Audit Standard:** Forensic Verification of Physical Dataset Files on Disk (Truth > Appearance)  
**Audit Execution Date:** 2026-09-04  
**Integrity Standard:** Anti-Hallucination & Manifest Truthfulness Standard  
**Governing Rule:** A manifest entry records intent or schema; it NEVER constitutes proof of physical existence.

---

## 1. Executive Summary

A critical failure mode in machine learning and computer vision projects is the registration of "phantom datasets"—datasets declared in manifests or architecture documents with elaborate descriptions of annotators, sample sizes, and ground-truth measurement instruments, but with **zero physical images or annotation files committed to disk**.

This audit performs a forensic, byte-level verification of all datasets declared in `data/manifests/manifest.yaml` against the physical contents of the `data/` directory tree.

### Core Audit Finding:
> **Zero Physical Datasets Currently Exist on Disk:**  
> All data subdirectories (`data/raw/`, `data/processed/`, `data/annotations/`, `data/synthetic/`, `data/benchmark/`) contain **strictly `.gitkeep` files (0 bytes)**.  
> Every previous description implying that datasets were already "collected on 2026-09-04" or "measured with vernier calipers" has been downgraded to **`PLANNED`** with explicit artifact flags **`NOT_GENERATED`** and **`DECLARED_BUT_MISSING`**.

---

## 2. Dataset Manifest vs. Physical Reality Audit

| Dataset ID | Declared Title | Manifest Status | Artifact Status on Disk | Claimed Size | Actual Files on Disk | Physical Images | Annotations Present? | Caliper Data Present? | Final Forensic Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`DS-SYNTH-001`** | Synthetic FMCG Packaging Benchmark Vector Set | `PLANNED` | **`NOT_GENERATED`** | 1,000 synthetic vector configurations | **0 files** (only `.gitkeep`) | **0** | **NO** (0 files) | N/A (Vector ground truth) | **`PLANNED — NOT YET GENERATED`** |
| **`DS-RETAIL-PILOT-001`** | Field Retail Packaged Commodities Ground-Truth Pilot | `PLANNED` | **`DECLARED_BUT_MISSING`** | 50 retail SKU samples | **0 files** (only `.gitkeep`) | **0** | **NO** (0 files) | **NO** (0 measurement logs) | **`DECLARED_BUT_MISSING`** |

---

## 3. Special Forensic Deep-Dive: DS-SYNTH-001

- **Dataset Identifier:** `DS-SYNTH-001`
- **Declared Title:** Synthetic FMCG Packaging Benchmark Vector Set
- **Claimed Source:** Nirikshak Procedural Packaging Generator
- **Claimed License:** CC0-1.0 (Public Domain)
- **Claimed Annotation Method:** Programmatic bounding box and text ground truth export
- **Claimed Ground Truth Method:** Vector geometry rendering ground truth
- **Physical Disk Audit of `data/synthetic/`:**
  - Files Found: `data/synthetic/.gitkeep` (1 file, 0 bytes).
  - Image Files (`.png`, `.jpg`): **0**.
  - Annotation Files (`.json`, `.xml`, `.csv`): **0**.
- **Forensic Assessment:**  
  The procedural generation algorithm and mathematical model for synthetic label rendering are specified in documentation, but the execution script has not yet been triggered to produce image files on disk.
- **Corrective Action Taken:**
  - `data/manifests/manifest.yaml` updated: `status: PLANNED`, `artifact_status: NOT_GENERATED`, `collection_date: PLANNED — STAGE 2`.
  - Zero synthetic files were fabricated during this audit to simulate completeness.

---

## 4. Special Forensic Deep-Dive: DS-RETAIL-PILOT-001

- **Dataset Identifier:** `DS-RETAIL-PILOT-001`
- **Declared Title:** Field Retail Packaged Commodities Ground-Truth Pilot
- **Declared Geography:** National Capital Region (NCR), India
- **Claim-by-Claim Forensic Matrix:**

| Claimed Feature | Claim Description in Documentation | Physical Reality on Disk | Forensic Finding |
| :--- | :--- | :--- | :--- |
| **50 Retail SKUs** | "Limited to initial 50 retail SKU samples across dry food and personal care categories" | 0 image files in `data/raw/` or `data/processed/` | **CLAIMED BUT PHYSICALLY MISSING** |
| **Dual Annotation** | "Dual-annotator cross-validated manual labeling" | 0 annotation files in `data/annotations/` | **CLAIMED BUT PHYSICALLY MISSING** |
| **Cross-Validation**| "Cross-validated inter-annotator agreement" | 0 verification logs or annotator ID records | **CLAIMED BUT PHYSICALLY MISSING** |
| **Vernier Caliper Measurements** | "Physical vernier caliper measurement for font heights and calibrated ruler reference" | 0 physical measurement sheets, 0 caliper log files | **CLAIMED BUT PHYSICALLY MISSING** |
| **Physical Ground Truth** | "Calibrated physical ground truth millimeter measurements" | 0 ground truth calibration tables on disk | **CLAIMED BUT PHYSICALLY MISSING** |
| **Capture Metadata**| "Smartphone camera lens profile, focal length, lux illumination" | 0 EXIF metadata catalogs or capture logs | **CLAIMED BUT PHYSICALLY MISSING** |
| **Rights Clearance**| "CC BY-NC-SA 4.0; brand trade dress: RIGHTS_VERIFICATION_REQUIRED" | Stated in manifest; no formal legal counsel memo | **RIGHTS VERIFICATION PENDING** |

### List of Missing Physical Artifacts for DS-RETAIL-PILOT-001:
1. `data/raw/*.jpg` — 50 raw multi-panel smartphone packaging image sets (front, back, sides).
2. `data/processed/*.png` — Rectified, glare-filtered, and perspective-corrected planar crops.
3. `data/annotations/*.json` — Bounding polygon coordinates, transcribed string tokens, and Table-I class labels.
4. `data/benchmark/caliper_measurements.csv` — Certified digital vernier caliper physical measurement logsheets ($\pm 0.02	ext{ mm}$).
5. `data/manifests/sku_inventory.yaml` — Commercial SKU inventory with barcode GTINs, commodity classes, and retail purchase receipts.

- **Corrective Action Taken:**
  - `data/manifests/manifest.yaml` updated: `status: PLANNED`, `artifact_status: DECLARED_BUT_MISSING`, `collection_date: PLANNED — STAGE 2`.
  - The dataset is designated as **`CRITICAL BLOCKER: BLOCKER-DATA-01`** for Stage 2 empirical benchmarking.

---

## 5. Dataset Audit Conclusion & Stage Gate Status

| Forensic Check | Result | Detail |
| :--- | :---: | :--- |
| Does any active dataset physically exist on disk today? | **NO** | 0 datasets exist; all directories contain strictly `.gitkeep`. |
| Does the manifest accurately declare dataset status? | **YES** | Manifest updated to reflect `PLANNED`, `NOT_GENERATED`, and `DECLARED_BUT_MISSING`. |
| Were any fake dataset samples created to pass this audit? | **NO** | Strictly prohibited by the Anti-Hallucination Policy. |
| Is physical dataset acquisition documented as an explicit Stage 2 blocker? | **YES** | Formally cataloged in `docs/14_SUBMISSION/RESEARCH_GAPS.md` and `FINAL_ARTIFACT_AUDIT.md`. |

**Dataset Existence Audit Result:** **`PASS_WITH_BLOCKERS`**  
*(Blocker: Physical procurement and synthetic generation must occur prior to Stage 2 benchmark execution).*
