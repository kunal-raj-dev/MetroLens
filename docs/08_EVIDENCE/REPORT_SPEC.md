# Inspection Dossier & Report Specification

## Purpose
Defines the visual layout, metadata schema, and statutory disclosures required in every generated PDF and JSON inspection dossier.

## Scope
Governs final inspection artifacts exported for departmental review or court submission.

## Authoritative Inputs
- Legal Metrology standard inspection memo formats.
- `docs/LEGAL_NOTICES.md`.

## Assumptions
- The dossier must present clear visual crops and side-by-side evidence that an adjudicating officer or judge can easily inspect without technical training.

## Open Questions
- Departmental seal / emblem inclusion guidelines [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `packages/reporting/`

## Verification Requirements
- Generated PDF must include all mandatory disclaimer clauses from `docs/LEGAL_NOTICES.md`.

---

## Dossier Sections & Content

```
┌────────────────────────────────────────────────────────┐
│ NIRIKSHAK LEGAL METROLOGY INSPECTION DOSSIER           │
│ Inspection ID: 8f7e2a9b-... | Date: 2026-09-04 12:30   │
│ Officer ID: INSP-DL-0482   | Location: Warehouse B     │
├────────────────────────────────────────────────────────┤
│ 1. COMMODITY & PACKAGING IDENTIFIERS                   │
│ • Brand / Commodity: "Crunchy Biscuits"                │
│ • Packaging Geometry: Rectangular Carton               │
│ • Declared Mfg Date: 2024-03-15 (Epoch: EPOCH-2022)    │
├────────────────────────────────────────────────────────┤
│ 2. SUMMARY OF COMPLIANCE VERDICTS                      │
│ • Rule 6(1) Mandatory Declarations: PASS               │
│ • Rule 7 Net Qty Font Height:       FAIL (1.4 mm < 2mm)│
│ • Rule 6(11) Unit Sale Price:       PASS               │
├────────────────────────────────────────────────────────┤
│ 3. OPTICAL EVIDENCE & MEASUREMENT CROPS                │
│ [Crop: Net Qty]   Measured: 1.4 ± 0.15 mm              │
│                   Required: 2.0 mm (Table-I, PDP 120cm²)│
│ [Crop: MRP]       Declared: Rs. 40.00 (incl. of taxes) │
├────────────────────────────────────────────────────────┤
│ 4. CRYPTOGRAPHIC PROVENANCE & CHAIN OF CUSTODY         │
│ • Raw Image SHA-256: 7f83a...                          │
│ • Scale Calibration: 0.082 mm/px (Marker ID: STD-25)   │
│ • Applied Ruleset Hash: c381b...                       │
├────────────────────────────────────────────────────────┤
│ 5. STATUTORY DISCLAIMER & OFFICER ATTESTATION          │
│ "This report represents technical inspection assistance│
│ and cryptographic provenance. Legal evidentiary status │
│ is determined by the competent authority under law."   │
│ Officer Signature: [Signed Digitally]                  │
└────────────────────────────────────────────────────────┘
```
