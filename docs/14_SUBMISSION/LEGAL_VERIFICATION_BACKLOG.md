# Legal Verification Backlog & Source Retrieval Plan

## Purpose
Catalogues pending legal retrieval tasks, Gazette downloads, and human legal reviews required to promote rules from `rules/proposed/` to `rules/verified/` and `rules/current/`.

## Scope
Covers all Level 1 and Level 2 statutory sources pending ingestion into `regulations/`.

---

## Actionable Legal Verification Backlog

| Backlog ID | Target Instrument | Action Required | Responsible Lead | Target Date | Gate Condition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LEG-BACK-01** | The Legal Metrology Act, 2009 | Download authentic PDF from egazette.gov.in; compute SHA-256; store in `regulations/current/legal_metrology_act_2009/`. | Legal Engineering Lead | 2026-09-10 | Checksum verification |
| **LEG-BACK-02** | LMPC Rules, 2011 (Base GSR 202(E)) | Download base gazette; extract verbatim text of Rule 6 and Rule 7 Table-I into `verified_text.md`. | Legal Engineering Lead | 2026-09-10 | Verbatim text review |
| **LEG-BACK-03** | LMPC Amendment 2017 (GSR 629(E)) | Download gazette; verify e-commerce declaration clauses and font visibility amendments. | Legal Engineering Lead | 2026-09-12 | Source record update |
| **LEG-BACK-04** | LMPC Amendment 2021 (GSR 779(E)) | Retrieve notification; extract Unit Sale Price (USP) threshold parameters and effective date. | Legal Engineering Lead | 2026-09-12 | Source record update |
| **LEG-BACK-05** | Official DoCA Implementation Guidelines | Archive published FAQs and advisories into `regulations/interpretations/`. | Metrology Lead | 2026-09-15 | Advisory review |
