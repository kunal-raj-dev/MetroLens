# End-to-End Requirement Traceability Matrix

## Purpose
Establishes bidirectional traceability connecting statutory legal provisions, problem statement requirements, software architecture modules, code packages, and validation tests.

## Scope
Covers all system features from regulatory source ingestion to inspection report generation.

## Authoritative Inputs
- Legal Metrology (Packaged Commodities) Rules, 2011 (Rules 6, 7, 8, 9, 10, 11).
- `docs/01_PROBLEM_STATEMENT/PS_REQUIREMENTS_MATRIX.md`.

## Assumptions
- Traceability links must remain valid across code refactoring and regulatory amendments.

## Open Questions
- None.

## Dependencies
- `packages/`
- `tests/`

## Verification Requirements
- CI must verify that every requirement ID has at least one associated test module.

---

## Traceability Mapping

```
[Statutory Authority / PS Requirement]
                 ↓
      [System Specification]
                 ↓
     [Architectural Package]
                 ↓
       [Automated Test Vector]
                 ↓
      [Inspection Dossier Item]
```

### Traceability Breakdown

1. **Rule 6(1)(a) — Name & Address of Manufacturer / Packer / Importer**
   - Requirement: REQ-03
   - Architecture Module: `packages/extraction/address_parser.py`
   - Test Vector: `tests/rules/test_rule6_declarations.py::test_manufacturer_address_presence`
   - Dossier Field: `dossier.observations.manufacturer_details`

2. **Rule 6(1)(b) — Common or Generic Name**
   - Requirement: REQ-03
   - Architecture Module: `packages/extraction/generic_name_parser.py`
   - Test Vector: `tests/rules/test_rule6_declarations.py::test_generic_name_presence`
   - Dossier Field: `dossier.observations.generic_name`

3. **Rule 6(1)(c) & Rule 7 — Net Quantity & Numeral Height**
   - Requirement: REQ-03, REQ-05
   - Architecture Module: `packages/measurement/font_estimator.py`, `packages/calibration/target_detector.py`
   - Test Vector: `tests/rules/test_rule7_font_height.py::test_net_quantity_font_height`
   - Dossier Field: `dossier.observations.net_quantity_measured_height_mm`

4. **Rule 6(1)(d) — Month and Year of Manufacture / Pre-packing / Import**
   - Requirement: REQ-03
   - Architecture Module: `packages/extraction/date_parser.py`
   - Test Vector: `tests/rules/test_rule6_declarations.py::test_mfg_date_format`
   - Dossier Field: `dossier.observations.manufacturing_date`

5. **Rule 6(1)(e) — Maximum Retail Price (MRP) & Unit Sale Price (USP)**
   - Requirement: REQ-03
   - Architecture Module: `packages/extraction/mrp_parser.py`
   - Test Vector: `tests/rules/test_rule6_declarations.py::test_mrp_inclusive_all_taxes`
   - Dossier Field: `dossier.observations.mrp_declaration`

6. **Rule 6(1)(n) — Consumer Grievance Contact**
   - Requirement: REQ-03
   - Architecture Module: `packages/extraction/consumer_care_parser.py`
   - Test Vector: `tests/rules/test_rule6_declarations.py::test_consumer_care_details`
   - Dossier Field: `dossier.observations.consumer_care`
