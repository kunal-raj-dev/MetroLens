# Data Licenses & Image Provenance Framework

## Purpose
Specifies the copyright, data privacy, commercial permissions, and governmental re-use conditions governing all packaging images, synthetic renderings, OCR ground-truth annotations, and benchmarking datasets utilized in Nirikshak.

## Scope
Applies to all data stored, processed, or referenced in `data/`, `benchmarks/datasets/`, and `assets/`.

## Authoritative Inputs
- Indian Copyright Act, 1957 (Sections on fair dealing, non-commercial research, and artistic/commercial works on packaging labels).
- Digital Personal Data Protection (DPDP) Act, 2023 (redaction of consumer care personal phone numbers/emails).
- Open Government Data (OGD) Platform India terms of use.

## Assumptions & Legal Rights Notice
- Real packaging photographs collected from retail shelves capture commercial trade dress, logos, and statutory labels. The legal status of reproducing commercial packaging trade dress in computational vision datasets is not settled by binding statutory exemption; therefore, this repository does NOT make legal conclusions regarding "Fair Dealing". Third-party IP rights for field retail images are designated as `RIGHTS_VERIFICATION_REQUIRED`.
- Commercial brand trademarks must not be disparaged, misattributed, or used outside non-commercial evaluation.

## Open Questions
- Departmental data sharing agreement terms for official seizure photo datasets [TBD — PRIMARY SOURCE REQUIRED].
- Formal IP clearance protocol for public release of retail SKU photos [status: RIGHTS_VERIFICATION_REQUIRED].

## Dependencies
- Dataset manifests (`data/manifests/`).
- Dataset verification script (`scripts/verification/verify_dataset_manifest.py`).

## Verification Requirements
- Every image batch must have an explicit entry in `data/manifests/` detailing source, declared license, rights verification status, collector identity, collection date, and geographic jurisdiction.
- No scraped or unverified images from internet search engines may be committed to `data/raw/` without an approved manifest entry.

---

## Dataset Provenance & Rights Classification (6-Facet Rights Breakdown)

1. **Category A: Team-Collected Field Packaging (Physical Ground Truth: `DS-RETAIL-PILOT-001`)**
   - **Source:** Direct physical retail purchase and optical capture by the Nirikshak engineering team (Planned Stage 2).
   - **Status:** `PLANNED / DECLARED_BUT_MISSING` (0 physical image sets or measurement sheets on disk).
   - **Target Scope:** 50 physical SKUs across dry food and personal care categories.
   - **Rights Breakdown:**
     - **IMAGE RIGHTS:** `RIGHTS_VERIFICATION_REQUIRED` (Photographic reproduction of commercial packaging trade dress lacks binding statutory exemption; formal legal opinion pending).
     - **ANNOTATION RIGHTS:** `RIGHTS_VERIFICATION_REQUIRED` (Bounding boxes, polygon masks, and transcription metadata require formal project copyright assignment/dedication).
     - **TRADEMARK / TRADE DRESS:** Proprietary to respective trademark holders; not licensed, transferred, or sublicensable by the project.
     - **REDISTRIBUTION RIGHTS:** `RESTRICTED` (Public redistribution prohibited pending formal rights clearance).
     - **PUBLICATION RIGHTS:** `RESTRICTED` (Restricted to internal research and confidential review).
     - **HACKATHON DEMONSTRATION RIGHTS:** `RIGHTS_VERIFICATION_REQUIRED` (Non-commercial academic/statutory evaluation defense under Indian Copyright Act § 52 pending legal counsel sign-off).

2. **Category B: Procedural Synthetic Packaging Artifacts (`DS-SYNTH-001`)**
   - **Source:** Procedurally generated mock packaging layouts rendered by project scripts (`data/synthetic/`).
   - **Status:** `PLANNED / NOT_GENERATED` (0 synthetic renders exist on disk; target: 1,000 configurations).
   - **Intended License:** CC0-1.0 (Public Domain Dedication upon script execution; zero third-party trademark conflict).
   - **Rights Status:** `VERIFIED_SCHEMA / ARTIFACT_PENDING_GENERATION`.
   - **Permitted Usage:** Adversarial testing, font height bounds testing, public open-source repository distribution (upon generation).

3. **Category C: Official Demonstration Commodities (`SRC-DEMO-LIVE-01`)**
   - **Source:** Curated physical consumer commodities reserved for SIH live evaluation with NIST/NPL-traceable vernier measurements.
   - **Status:** `PLANNED` (Planned target: 3 physical SKUs: 1 carton, 1 can, 1 pouch).
   - **Rights Breakdown:** Same as Category A (`RIGHTS_VERIFICATION_REQUIRED`).
   - **Permitted Usage:** Live closed-room judging demonstration and verification only.

4. **Category D: Unverified Third-Party Scrapes**
   - **Rights Status:** `REJECTED`. Scraped web images without verifiable copyright provenance and collection consent are strictly prohibited.
