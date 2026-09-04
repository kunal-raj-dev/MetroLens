# MetroLens Legal Rule Matrix — Engineering Interpretation of Identified Legal Requirements

> **Final legal determinations remain with authorized authorities.**

| Rule ID | Legal Provision | Requirement | Applicable To | Exceptions | Effective From | Effective To | Image Verifiable | Inputs | Validation | Output | Manual Review | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LMPC-R3-SCOPE | Rule 3 | Intended for retail sale | All retail packages | >25kg/L, Institutional | 2011-04-01 | - | PARTIALLY | Image text, Weight | Declared weight <= 25kg | PASS / FAIL / MR | If institutional context | PCR 2011 |
| LMPC-R6-1-A-MFR | Rule 6(1)(a) | Mfr/Packer/Importer Name | Retail packages | - | 2011-04-01 | - | YES | Image text | Entity name detected | PASS / MR | If OCR unclear | PCR 2011 |
| LMPC-R6-1-AA-COO | Rule 6(1)(aa) | Country of Origin | Imported retail | Domestic mfg | 2018-01-01 | - | YES | Image text | Matches known country | PASS / MR | If OCR unclear | G.S.R. 629(E) |
| LMPC-R6-1-C-QTY | Rule 6(1)(c) | Net Quantity | Retail packages | - | 2011-04-01 | - | YES | Image text | Value + Standard Unit | PASS / FAIL / MR | If OCR unclear | PCR 2011 |
| LMPC-R6-1-D-MFG | Rule 6(1)(d) | Month & Year of Mfg | Retail packages | - | 2022-04-01 | - | YES | Image text | Valid month/year format | PASS / FAIL / MR | If pre-pack date used | G.S.R. 779(E) |
| LMPC-R6-1-E-MRP | Rule 6(1)(e) | MRP inclusive of taxes | Retail packages | - | 2011-04-01 | - | YES | Image text | "MRP" + INR symbol/text | PASS / FAIL | - | PCR 2011 |
| LMPC-R6-11-USP | Rule 6(11) | Unit Sale Price | Retail packages | <10g/ml | 2022-04-01 | - | YES | MRP, Qty | Calculated vs Declared | PASS / FAIL / MR | If OCR values missing | G.S.R. 226(E) |
| LMPC-R7-FONT | Rule 7(4) | Minimum Font Height | Retail packages | - | 2018-01-01 | - | PARTIALLY | Measured px | Pixel height > calibration | PASS / FAIL / MR | In uncertainty band | G.S.R. 629(E) |
