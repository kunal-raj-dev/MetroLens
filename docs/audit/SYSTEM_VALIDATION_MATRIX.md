# MetroLens System Validation Matrix

**Milestone:** Complete M1 → M5 Integration  
**Date:** September 2026  

---

## 1. Traceability: Statutory Rules to Code & Tests

| Statutory Mandate | Rule ID / Clause | Implementing Code File | Validation Test Target | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Mandatory Declarations** | PCR 2011, Rule 6(1) | `packages/rules-engine/.../declarations.py` | `tests/rules/test_mandatory_declarations.py` | **VERIFIED** |
| **Unit Sale Price (USP)** | PCR 2011, Rule 6(11) | `packages/rules-engine/.../usp.py` | `tests/rules/test_usp_rule.py` | **VERIFIED** |
| **Font Height Tables** | PCR 2011, Schedule II | `packages/rules-engine/.../font_height.py` | `tests/rules/test_schedule_ii.py` | **VERIFIED** |
| **Decriminalized Fines** | Jan Vishwas Act, 2023 | `packages/rules-engine/.../penalties.py` | `tests/rules/test_penalties.py` | **VERIFIED** |
| **Section 36(1) Notice** | Legal Metrology Act, 2009 | `packages/rules-engine/.../notice.py` | `tests/e2e/test_system_integration.py::test_e2e_009` | **VERIFIED** |
| **Tamper-Evident Dossier** | Section 65B Evidence Act | `packages/evidence/.../hasher.py` | `tests/evidence/test_evidence_hashing.py` | **VERIFIED** |
| **Evidentiary PDF Dossier**| Statutory Notice Format | `packages/reporting/.../generator.py` | `tests/contracts/test_cross_member_contracts.py::test_contract_m4_reporting_pdf` | **VERIFIED** |
| **Optical Scale Recovery** | SIH26034 Problem Spec | `packages/calibration/.../coin.py` | `tests/contracts/test_cross_member_contracts.py::test_contract_m2_calibration_to_m3_rules` | **ALGORITHMIC PASS; DATA BLOCKED** |
