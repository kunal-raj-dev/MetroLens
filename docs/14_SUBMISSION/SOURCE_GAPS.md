# Final Quality Gate Audit & Source Gaps Register

## Purpose
This document constitutes the final self-audit quality gate for Project Nirikshak. In accordance with the project's Non-Negotiable Anti-Hallucination Policy, this register enumerates every pending primary legal source, unverified threshold, missing government integration API, unmeasured performance claim, ambiguous requirement, and unresolved regulatory conflict.

**Policy Directive:**
The objective of this repository is NOT to present a cosmetically complete facade. The objective is to produce a trustworthy, implementable, and legally defensible system before SIH judges. We deliberately document our source gaps rather than filling them with plausible-sounding hallucinations.

---

## 1. Pending Primary Legal Source Artifacts (Level 1 Gazettes)

| Source Identifier | Regulatory Title | Pending Primary Artifact | Gap Status | Blocking Impact |
| :--- | :--- | :--- | :--- | :--- |
| **IN-ACT-2009-01** | The Legal Metrology Act, 2009 | Authenticated India Code / Gazette PDF | PENDING_DOWNLOAD | Rule 52 rule-making powers confirmed; local SHA-256 hash required. |
| **IN-LMPC-2011-GSR202E** | Legal Metrology (Packaged Commodities) Rules, 2011 | Official Gazette G.S.R. 202(E) PDF | PENDING_DOWNLOAD | Base Table-I font height numbers pending PDF text extraction. |
| **IN-LMPC-2017-GSR629E** | LMPC Amendment Rules, 2017 | Official Gazette G.S.R. 629(E) PDF | PENDING_DOWNLOAD | E-commerce mandatory declaration clauses pending text extraction. |
| **IN-LMPC-2021-GSR779E** | LMPC Amendment Rules, 2021 | Official Gazette G.S.R. 779(E) PDF | PENDING_DOWNLOAD | Unit Sale Price (USP) exact rounding rules pending text extraction. |
| **GSR_128_E / 312_E / 418_E** | Purported 2026 Gazette Amendments | Gazette Notification Numbers | UNVERIFIED — PRIMARY SOURCE REQUIRED | No rules authored or implemented based on unverified citations. |

---

## 2. Unverified Regulatory Interpretations & Ambiguities

1. **Multi-Pack MRP Precedence:**
   - **Ambiguity:** How should the rule engine evaluate a multi-pack promotional carton where the outer box states "Rs. 100" but individual inner units state "Rs. 30" each?
   - **Current Status:** `UNVERIFIED — PRIMARY SOURCE REQUIRED`.
   - **System Safeguard:** Flagged as `REVIEW` with visual side-by-side crop comparison.

2. **Combination Exemptions (Rule 3):**
   - **Ambiguity:** Applicability of the 10g/10ml small-quantity exemption when an exempt sachet is sold inside a larger non-exempt consumer kit.
   - **Current Status:** `UNVERIFIED — ADVISORY CIRCULAR REQUIRED`.
   - **System Safeguard:** Routed to officer review.

3. **Sticker Overlays on Imported Goods:**
   - **Ambiguity:** Permissibility of supplementary label stickers affixed by an importer over foreign declarations.
   - **Current Status:** `PARTIALLY_VERIFIED` under Rule 6 provisos, but specific state inspection circulars vary.
   - **System Safeguard:** Highlighted as `REVIEW` in dossier.

---

## 3. Unverified External Government APIs & Integrations

1. **Department of Consumer Affairs (DoCA) Central Database API:**
   - **Claim:** Direct real-time cloud lookup of manufacturer Legal Metrology registration numbers.
   - **Audit Finding:** **NO PUBLIC OFFICIAL REST API EXISTS.**
   - **Action Taken:** Zero fake APIs mocked or integrated. Feature scoped strictly to local offline database validation.

2. **National Consumer Helpline (NCH) / e-Daakhil Direct Filing:**
   - **Claim:** Direct automated filing of compounding charges from the mobile app into e-Daakhil.
   - **Audit Finding:** **NO AUTHORIZED THIRD-PARTY WRITE API EXISTS.**
   - **Action Taken:** Marked as an explicit non-goal. Final dossiers are exported as standard signed PDFs for manual official submission.

---

## 4. Empirical Performance & Benchmark Placeholders

In strict accordance with the Benchmarking Policy, all quantitative performance claims remain unverified until empirical execution is completed against `data/benchmark/`:

| Performance Metric | Target Specification | Current Status | Required Empirical Action |
| :--- | :--- | :--- | :--- |
| **Character Error Rate (CER)** | $\le 2.5\%$ on clean packaging | `TBD — MEASURE` | Run PROTO-OCR-001 on retail test set. |
| **Word Error Rate (WER)** | $\le 5.0\%$ on clean packaging | `TBD — MEASURE` | Run PROTO-OCR-001 on retail test set. |
| **Font Measurement Error** | $\le \pm 0.2\text{ mm}$ with scale | `TBD — MEASURE` | Run PROTO-FONT-001 with digital caliper ground truth. |
| **PDP Area IoU** | $\ge 0.85$ IoU | `TBD — MEASURE` | Run PROTO-PDP-001 on segmented package contours. |
| **End-to-End Latency** | $\le 5.0\text{ s}$ per 4-panel SKU | `TBD — MEASURE` | Execute PROTO-LATENCY-001 on target 8-core CPU. |

---

## 5. Unresolved Regulatory Conflicts

| Conflict ID | Competing Source A | Competing Source B | Conflict Details | Current Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **CONF-01** | LMPC Rule 3(c) (2011 Base) | LMPC Amendment 2022 Circulars | Applicability threshold for bulk agricultural sacks (25 kg vs 50 kg limits) | Status: `BLOCKED / REVIEW`. Rule evaluator halts automated pass/fail on bulk agricultural packaging until circular is verified. |
