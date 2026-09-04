# Project Glossary & Acronyms

## Purpose
Establishes unambiguous statutory and technical definitions used throughout the Nirikshak codebase, documentation, and evaluation presentations.

## Scope
Universal across all engineering and legal modules.

## Authoritative Inputs
- The Legal Metrology Act, 2009 (Section 2 Definitions).
- The Legal Metrology (Packaged Commodities) Rules, 2011 (Rule 2 Definitions).
- ISO/IEC 17025 (General requirements for the competence of testing and calibration laboratories).

## Assumptions
- Terms defined in statutory law take precedence over colloquial or general software terminology.

## Open Questions
- None.

## Dependencies
- All documentation files.

## Verification Requirements
- All team members and documents must adhere strictly to these defined meanings.

---

## Terminology & Definitions

- **DoCA:** Department of Consumer Affairs, Ministry of Consumer Affairs, Food & Public Distribution, Government of India.
- **LMA 2009:** The Legal Metrology Act, 2009 (Act No. 1 of 2010).
- **LMPC Rules 2011:** The Legal Metrology (Packaged Commodities) Rules, 2011, as amended.
- **Principal Display Panel (PDP):** That part of the package which is intended or likely to be displayed, presented, shown, or examined under normal and customary conditions of display for retail sale.
- **Area of PDP ($A_{\text{PDP}}$):** The surface area of the principal display panel calculated according to statutory geometric rules (Rule 7).
- **Pre-Packaged Commodity:** A commodity which without the purchaser being present is placed in a package, whether of any kind or not, so that the quantity of the product contained therein has a predetermined value.
- **Retail Package:** Packages intended for retail sale to the ultimate consumer.
- **Wholesale Package:** A package containing a number of retail packages or sold to an intermediary.
- **Institutional Consumer:** Those who buy packaged commodities directly from the manufacturer for use by that institution (e.g. airlines, railways, hotels) and not for commercial resale.
- **MRP:** Maximum Retail Price inclusive of all taxes.
- **Unit Sale Price (USP):** The retail price of a commodity expressed in terms of the statutory unit of measurement (e.g., per gram, per kilogram, per millilitre, per litre, per metre, or per number).
- **Physical Scale Calibration:** The mathematical process of establishing real-world millimetre distance per image pixel ($\text{mm/px}$) using a known reference target.
- **Deterministic Rule Engine:** A software evaluator where identical inputs (measurements, extracted declarations, applicable rule version) always produce identical outputs (`PASS`, `FAIL`, `REVIEW`, `NOT_APPLICABLE`) without stochastic randomness.
- **Evidence Graph:** A directed acyclic graph (DAG) linking the raw photographic capture to its crops, extracted tokens, calibrated measurements, rule evaluations, and officer actions.
- **Regulatory Snapshot:** The exact set of rules, subrules, and tables in force on a specific historical date (e.g., the manufacturing date of a package).
- **Observation Layer:** The computer vision and OCR subsystems responsible for detecting visual tokens and measuring geometries without making legal conclusions.
