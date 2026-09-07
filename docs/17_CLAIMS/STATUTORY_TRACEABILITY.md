# STATUTORY TRACEABILITY REGISTER
### Project: MetroLens AI (SIH26034) | Sponsoring Ministry: Ministry of Consumer Affairs
**Document Status:** Authoritative Statutory-to-Code Traceability Mapping | **Author:** Member 3 (Legal Rules Lead)  
**Primary Engine:** `packages/rules-engine/` (`nirikshak_rules_engine`)

---

## 1. Statutory Traceability Matrix

| Rule ID | Statutory Reference | Primary Gazette / Enactment | Gazette Date / Effective Date | Codified Module | Test Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LMPC-R03-WHOLESALE-EXCLUSION** | LM(PC) Rules 2011, Rule 3 | G.S.R. 202(E) | 07.03.2011 / 01.04.2011 | `rule_engine.py:evaluate_exemptions` | `test_rule_26_exemptions.py`, `test_rules_engine.py` (Cases 19, 20) |
| **LMPC-R06-MFR-001** | LM(PC) Rules 2011, Rule 6(1)(a) | G.S.R. 202(E) | 07.03.2011 / 01.04.2011 | `rule_engine.py:evaluate_rule_6` | `test_rule_6.py`, `test_rules_engine.py` (Case 03) |
| **LMPC-R06-COO-001** | LM(PC) Rules 2011, Rule 6(1)(aa) | G.S.R. 629(E) read with G.S.R. 779(E) | 23.06.2017 / 01.01.2018 | `rule_engine.py:evaluate_rule_6` | `test_rule_6.py`, `test_rules_engine.py` (Case 04) |
| **LMPC-R06-NAME-001** | LM(PC) Rules 2011, Rule 6(1)(b) | G.S.R. 202(E) | 07.03.2011 / 01.04.2011 | `rule_engine.py:evaluate_rule_6` | `test_rule_6.py`, `test_rules_engine.py` (Case 05) |
| **LMPC-R06-QTY-001** | LM(PC) Rules 2011, Rule 6(1)(c) read with Rule 13 | G.S.R. 202(E) | 07.03.2011 / 01.04.2011 | `rule_engine.py:evaluate_rule_6` | `test_rule_6.py`, `test_rules_engine.py` (Cases 06, 07, 08) |
| **LMPC-R06-DATE-001** | LM(PC) Rules 2011, Rule 6(1)(d) | G.S.R. 779(E) | 02.11.2021 / 01.10.2022 | `rule_engine.py:evaluate_rule_6` | `test_rule_6.py`, `test_rules_engine.py` (Case 09) |
| **LMPC-R06-MRP-001** | LM(PC) Rules 2011, Rule 6(1)(e) | G.S.R. 202(E) | 07.03.2011 / 01.04.2011 | `rule_engine.py:evaluate_rule_6` | `test_rule_6.py`, `test_rules_engine.py` (Cases 10, 11) |
| **LMPC-R06-CARE-001** | LM(PC) Rules 2011, Rule 6(1)(g) | G.S.R. 202(E) | 07.03.2011 / 01.04.2011 | `rule_engine.py:evaluate_rule_6` | `test_rule_6.py`, `test_rules_engine.py` (Case 12) |
| **LMPC-R06-USP-001** | LM(PC) Rules 2011, Rule 6(11) | G.S.R. 779(E) / G.S.R. 226(E) | 28.03.2022 / 01.10.2022 | `usp_validator.py:evaluate` | `test_rule_6_11.py`, `test_usp_arithmetic.py`, `test_rules_engine.py` (Cases 13–18) |
| **LMPC-R07-FONT-001** | LM(PC) Rules 2011, Rule 7 (Tables I & II) | G.S.R. 629(E) / G.S.R. 1373(E) | 23.06.2017 & 06.10.2017 | `font_matrix.py:evaluate` | `test_rule_7.py`, `test_rules_engine.py` (Cases 23, 24, 25) |
| **LMPC-R26-SMALL-PACK** | LM(PC) Rules 2011, Rule 26(a) | G.S.R. 202(E) | 07.03.2011 / 01.04.2011 | `rule_engine.py:evaluate_exemptions` | `test_rule_26_exemptions.py`, `test_rules_engine.py` (Case 21) |
| **LMPC-R26-GSR881E-CARVEOUT** | LM(PC) Rules 2011, Rule 26(a) override | G.S.R. 881(E) | 02.12.2025 / 01.02.2026 | `rule_engine.py:evaluate_exemptions` | `test_rule_26_exemptions.py`, `test_rules_engine.py` (Case 22) |
| **STATUTORY-IMPROVEMENT-NOTICE** | Legal Metrology Act 2009, Section 36(1) | Jan Vishwas (Amendment of Provisions) Act, 2026 | Enacted 2026 / 01.05.2026 | `notice_builder.py:build_notice` | `test_notice_builder.py`, `test_rules_engine.py` |
| **FSSAI-R05-NUTRITION-TABLE** | FSS (Labelling & Display) Regs 2020, Reg 5(3) | FSSAI Gazette Notification | 17.11.2020 / 01.07.2022 | `fopnl.py:evaluate` | `test_fopnl.py` |
| **FSSAI-R05-VEG-LOGO** | FSS (Labelling & Display) Regs 2020, Reg 5(4) | FSSAI Gazette Notification | 17.11.2020 / 01.07.2022 | `fopnl.py:evaluate` | `test_fopnl.py` |
| **FSSAI-R05-HFSS-ALERT** | FOPNL Draft Regulations / INR Guidelines | FSSAI Draft Gazette (INR) | 2022 / Draft Standard | `fopnl.py:evaluate_hfss` | `test_fopnl.py` |
| **SEC48-RECIDIVISM-COMPOUNDING** | Legal Metrology Act 2009, Sec 36(1) r/w 48 & 48A | Jan Vishwas Act 2026 | Enacted 2026 / 01.05.2026 | `penalties.py:calculate_penalty` | `test_penalties.py` |

---

## 2. Decriminalization & Jan Vishwas Act Compliance Guarantee
- **Parent Provision:** Section 36(1) of the Legal Metrology Act, 2009.
- **Amendment Statute:** Jan Vishwas (Amendment of Provisions) Act, 2026 (Act 18 of 2023 / 2026 amendments).
- **Enforcement Window:** Mandatory 15-day statutory rectification / cure window prior to compounding or financial penalty proceedings.
- **Prohibited Terminology Audit:** All generated notice drafts and UI inspection labels are audited by `ImprovementNoticeBuilder.audit_text_decriminalization()` to ensure strictly ZERO occurrences of "imprisonment", "jail", "arrest", "custody", "cognizable", or "non-bailable" terms.
