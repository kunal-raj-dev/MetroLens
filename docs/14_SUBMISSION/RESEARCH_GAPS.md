# NIRIKSHAK — RESEARCH GAPS & EVIDENCE REQUIREMENTS

**Submission Artifact:** Smart India Hackathon 2026 — PS 26034  
**Audit Execution Date:** 2026-09-04  
**Integrity Standard:** Anti-Hallucination & Governance Hardening Standard  
**Core Governance Statement:** A system that truthfully documents its research boundaries is legally and technically superior to one that conceals gaps behind synthetic assertions.

---

## 1. Executive Summary

Project Nirikshak is architected as a high-trust, legally defensible inspection-assistance system for Legal Metrology officers. In accordance with the Anti-Hallucination Policy, this document provides evaluators with a complete, unvarnished accounting of what has been **conclusively verified**, what remains **pending primary-source retrieval**, and what requires **physical bench experimentation** before Stage 2 deployment.

---

## 2. Research Gaps & Evidence Requirements Matrix

| Gap ID | Research Domain | Current Evidence Status | What We Know | What We Do Not Know (The Gap) | Mandatory Stage 2 Action Plan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`GAP-SRC-01`** | Base PCR 2011 Primary Source | `PRIMARY_SOURCE_REQUIRED` | `G.S.R. 202(E)` dated 2011-03-07 was notified by DoCA; text of Rules 6, 7, 8, 9, 10 is confirmed via official compendia. | SHA-256 hash of official Gazette PDF on disk is unpinned pending local archival. | Download authentic Gazette PDF from `egazette.gov.in` to `regulations/sources/` and pin SHA-256 checksum. |
| **`GAP-SRC-02`** | 2017 Amendments & Corrigenda | `PRIMARY_SOURCE_REQUIRED` | `G.S.R. 629(E)` substituted Table-I and added Rule 6(10); `G.S.R. 1373(E)` corrected Table-I row 2 to 2.0 mm. | Official Gazette PDF files pending local disk deposit. | Ingest authentic Gazette PDFs; pin hashes in `regulations/source_registry.yaml`. |
| **`GAP-SRC-03`** | Putative 2026 Amendments | `BLOCKED — PENDING PRIMARY SOURCE` | Citations `G.S.R. 128(E)`, `G.S.R. 312(E)`, `G.S.R. 418(E)` appear in informal hackathon discussions. | Whether these are enacted notifications, draft consultations, or erroneous citations. | Verify against `egazette.gov.in`; keep all rules blocked until confirmed. |
| **`GAP-MEAS-01`**| Optical Homography Uncertainty | `EXPERIMENT_REQUIRED` | Mathematical homography equations $H \in \mathbb{R}^{3 \times 3}$ and ArUco pose estimation algorithms are mathematically specified. | Measured physical millimeter reprojection error distribution across varied smartphone camera lenses. | Execute bench calibration across 100 test angles ($0^\circ \dots 35^\circ$) using certified digital calipers. |
| **`GAP-MEAS-02`**| Cylinder Unwrapping Error | `EXPERIMENT_REQUIRED` | Parametric cylinder projection model $A = 0.4 \times H \times \pi D$ is mathematically formulated. | Pixel stretch and glyph deformation at tangential outer edges of small cans ($D < 50\text{ mm}$). | Perform physical trials against test cans wrapped with calibrated millimeter grid paper. |
| **`GAP-BENCH-01`**| Field Packaging OCR Accuracy | `EXPERIMENT_REQUIRED` | PaddleOCR PP-OCRv4 achieves $> 85\%$ on academic scene text benchmarks (ICDAR, BSTD). | Exact Character Error Rate (CER) on metallic foil, embossed text, and tiny packaging print ($< 1.5\text{ mm}$). | Execute automated test benchmark against annotated physical test corpus `data/golden/`. |
| **`GAP-DATA-01`** | Packaging Artwork Rights | `RIGHTS_VERIFICATION_REQUIRED` | Statutory declarations on packaging are mandatory public disclosures under Section 18 of the Act. | Permissibility of redistributing third-party commercial brand trade dress in public open-source benchmark sets. | Consult Legal Metrology counsel regarding Section 52 Fair Dealing exceptions under Indian Copyright Act. |

---

## 3. Truthful System Boundaries

1. **What Nirikshak Does NOT Claim Today:**
   - Nirikshak does NOT claim that the computer vision pipeline is tested on physical packages.
   - Nirikshak does NOT claim that optical measurement accuracy is $\le 0.2\text{ mm}$ (it is explicitly marked `TARGET — NOT VALIDATED`).
   - Nirikshak does NOT publish unverified declarative rules into `rules/current/`.
2. **What Nirikshak DOES Guarantee Today:**
   - Disciplined, evidence-backed architectural skeleton.
   - Complete formal specifications for optical calibration, multi-panel staging, and OCR extraction.
   - Non-retroactive statutory rule evaluation architecture protecting businesses from improper retroactive enforcement.
   - Automated CI verification pipeline that prevents unverified rules, duplicate sources, and broken links from ever entering the system.
