# Data Sources & Acquisition Registry

## Purpose
Catalogues all origin points, physical procurement channels, and procedural generation scripts used to create the image data feeding Nirikshak.

## Scope
Universal across training, fine-tuning, and benchmarking data.

## Authoritative Inputs
- `data/manifests/manifest.yaml`

## Assumptions
- Images of public commercial retail packaging labels represent statutory public disclosures.

## Open Questions
- Standardizing acquisition protocols across varied smartphone camera lens profiles [TBD — MEASURE].

## Dependencies
- `data/manifests/`

## Verification Requirements
- Every image in `data/raw/` must correlate to an entry in `data/manifests/manifest.yaml`.

---

## Controlled Data Sources

| Source Identifier | Source Category | Description / Geography | Primary Target SKUs | Rights & Provenance Status |
| :--- | :--- | :--- | :--- | :--- |
| **SRC-TEAM-FIELD-01** | Physical Procurement (Planned) | Retail supermarkets, Delhi-NCR, India | Planned target: 50 SKUs: Food (biscuits, spices), personal care (shampoo, soap) | `RIGHTS_VERIFICATION_REQUIRED` (`DECLARED_BUT_MISSING`) |
| **SRC-SYNTH-PROC-01** | Procedural Generation (Planned) | Synthetic Python renderer (`scripts/data_prep/`) | Planned target: 1,000 configurations (edge case fonts, Table-I thresholds) | `PLANNED` (`NOT_GENERATED`) |
| **SRC-DEMO-LIVE-01** | Live Demonstration SKU (Planned)| Physical packages reserved for hackathon judging | Planned target: 3 SKUs (1 rectangular carton, 1 cylindrical can, 1 stand-up pouch) | `RIGHTS_VERIFICATION_REQUIRED` (`PLANNED`) |
| **SRC-WEB-SCRAPE-01** | Web Search Scraping | Uncurated Google/Bing image results | Various | `REJECTED — PROHIBITED BY POLICY` |
