# Operational & Technical Assumptions

## Purpose
Documents foundational assumptions regarding deployment hardware, operator training, packaging conditions, and environmental factors.

## Scope
Applies to technical requirements, computer vision thresholds, and operational testing.

## Authoritative Inputs
- Standard field conditions for Legal Metrology inspections in retail markets, warehouses, and e-commerce fulfilment centers.

## Operational Assumptions & Field Validation Protocols

### Assumption 1: Authorized Operator Role
- **Statement:** The primary operator is an authorized Inspector of Legal Metrology or trained enforcement official familiar with statutory requirements and packaging inspection procedures.
- **Status:** `ASSUMPTION — NOT FIELD VERIFIED`
- **Required Validation Method:** User testing and operational workflow review with practicing enforcement officers during departmental pilot (`docs/10_TESTING/TEST_STRATEGY.md`).

### Assumption 2: Minimum Field Device Hardware
- **Statement:** Field inspection hardware provides at least an 8-core ARM/x86 processor, 8 GB RAM, and a camera capable of $\ge 1080\text{p}$ optical capture with autofocus and macro focus support.
- **Status:** `ASSUMPTION — NOT FIELD VERIFIED`
- **Required Validation Method:** Hardware compatibility benchmark across low-tier and mid-tier Android smartphones (`benchmarks/protocols/PROTO_OFFLINE_EVAL.md`).

### Assumption 3: Ambient Lighting Tolerance
- **Statement:** Field inspections take place under varied ambient retail fluorescent, LED, or indirect natural lighting without specialized studio lamps.
- **Status:** `ASSUMPTION — NOT FIELD VERIFIED`
- **Required Validation Method:** Lux-level sweep experiments measuring OCR CER across 50 lux to 1500 lux lighting environments (`experiments/ocr/`).

### Assumption 4: Physical Packaging Structural Integrity
- **Statement:** Inspected packages are retail units without severe structural crushing, tearing, or label surface mutilation.
- **Status:** `ASSUMPTION — NOT FIELD VERIFIED`
- **Required Validation Method:** Evaluation on degraded package dataset assessing automated routing to `REQUEST_RETAKE` vs. `REVIEW` (`docs/10_TESTING/FAILURE_MODES.md`).

### Assumption 5: Network Connectivity Absence
- **Statement:** Cellular and Wi-Fi internet connectivity is intermittent or completely absent during field inspections in basement retail stores and rural warehouses.
- **Status:** `ASSUMPTION — NOT FIELD VERIFIED`
- **Required Validation Method:** Hardware airplane mode offline regression testing verifying zero remote API calls (`tests/e2e/test_offline.py`).

---

## Open Questions
- Optimal physical calibration marker format: high-contrast circular sticker vs. standardized departmental card [TBD — MEASURE].

## Dependencies
- `docs/03_PRODUCT_REQUIREMENTS/`
- `docs/10_TESTING/`

## Verification Requirements
- Every assumption above must undergo empirical validation or stakeholder confirmation before production deployment sign-off.
