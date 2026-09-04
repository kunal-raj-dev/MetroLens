# Project Scope Specification

## Purpose
Defines the technical, functional, and regulatory boundaries of the Nirikshak inspection system.

## Scope
Details both the full-scale system architecture and operational domains covered across field inspections, market surveillance, and laboratory audits.

## Authoritative Inputs
- SIH 2026 Problem Statement 26034 description and guidelines.
- Department of Consumer Affairs (DoCA) mandate for Packaged Commodities compliance.

## Assumptions
- Target packaging encompasses standard Fast-Moving Consumer Goods (FMCG), dry packaged foods, cosmetics, household chemicals, and electronic packaged goods.

## Open Questions
- Special exemptions for medicinal packages under Drugs & Cosmetics Act vs. LMPC Rules [TBD — PRIMARY SOURCE REQUIRED].
- Standard operating procedures for inspecting export-oriented packages [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `docs/00_PROJECT_CHARTER/MVP_SCOPE.md`
- `docs/00_PROJECT_CHARTER/NON_GOALS.md`

## Verification Requirements
- All scoped features must have corresponding verification test cases in `docs/10_TESTING/TEST_MATRIX.md`.

---

## In-Scope Capabilities

1. **Guided Multi-Panel Package Capture:**
   - Interactive UI directing the inspector to photograph front (PDP), rear, top, bottom, and side panels.
   - Image quality gating: real-time detection of motion blur, severe specular glare, and insufficient illumination.

2. **Optical Character Recognition & Field Extraction:**
   - Multi-lingual text extraction (English and Hindi numeral/text support).
   - Extraction of mandatory declarations: Name & Address of Manufacturer/Packer/Importer, Common/Generic Name, Net Quantity, Month & Year of Manufacture, Maximum Retail Price (MRP), Unit Sale Price (USP), and Consumer Grievance Contact.

3. **Physical Scale Calibration & Geometry:**
   - Integration of reference target detection (e.g. standard circular marker or fiducial card).
   - Principal Display Panel (PDP) bounding box calculation and surface area calculation ($A_{\text{PDP}}$).
   - Font height measurement ($\text{mm}$) of numerals and letters.

4. **Deterministic Legal Rule Engine:**
   - Evaluation of declarations against verified rules in force on the packaging manufacture date.
   - Evaluation of net quantity numeral height against statutory area tables.
   - Classification into four states: `PASS`, `FAIL`, `REVIEW`, `NOT_APPLICABLE`.

5. **Evidence Dossier & Audit Graph:**
   - Generation of cryptographic inspection dossiers (JSON/PDF) embedding raw image SHA-256 hashes, crop coordinates, OCR token confidence scores, and officer review logs.
