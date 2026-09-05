# RESEARCH GAPS & UNRESOLVED ITEMS REGISTER

**Repository:** `sih26034-nirikshak` (SIH 2026 — PS 26034)  
**Audit Execution Date:** 2026-09-04  
**Integrity Standard:** Anti-Hallucination Policy (Unverified items marked `PRIMARY_SOURCE_REQUIRED` or `EXPERIMENT_REQUIRED`)

---

## 1. Executive Summary

In accordance with the Nirikshak Governance Hardening Policy, the engineering team never invents legal provisions, fabricates empirical numbers, or completes missing facts from memory. This register explicitly catalogs every gap in primary evidence, unretrieved Gazette PDF, and required physical experiment.

---

## 2. Itemized Research Gaps Matrix

| Gap ID | Category | Description of Gap | Current Status | Blocker For | Resolution Protocol |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`GAP-LEGAL-01`** | Primary Source Retrieval | Official Gazette of India PDF for Base PCR 2011 (`G.S.R. 202(E)`) pending local download and SHA-256 hash pinning. | `PRIMARY_SOURCE_REQUIRED` | Rule promotion from `rules/proposed/` to `rules/verified/` | Download authentic PDF from `egazette.gov.in` into `regulations/sources/`; compute SHA-256; update `regulations/source_registry.yaml`. |
| **`GAP-LEGAL-02`** | Primary Source Retrieval | Official Gazette PDF for 2017 Amendment (`G.S.R. 629(E)`) and Corrigendum (`G.S.R. 1373(E)`) pending local download. | `PRIMARY_SOURCE_REQUIRED` | Promotion of Table-I font height rule to `rules/verified/` | Retrieve PDFs from DoCA portal; register cryptographic hashes. |
| **`GAP-LEGAL-03`** | Primary Source Retrieval | Official Gazette PDF for 2021 Amendment (`G.S.R. 779(E)`) regarding Unit Sale Price (USP) pending local download. | `PRIMARY_SOURCE_REQUIRED` | Promotion of USP rule to `rules/verified/` | Download Gazette PDF; verify commencement date (2022-12-01). |
| **`GAP-LEGAL-04`** | Unverified Citations | Putative 2026 amendments: `G.S.R. 128(E)`, `G.S.R. 312(E)`, `G.S.R. 418(E)` cited in informal hackathon discussions. | `BLOCKED — PENDING PRIMARY SOURCE` | Authoring any 2026 rules | Search `egazette.gov.in` by GSR number; if non-existent or draft, keep strictly blocked. |
| **`GAP-LEGAL-05`** | Statutory Notice Rules | Implementation rules for Jan Vishwas Act Section 36 Improvement Notice mechanism. | `PRIMARY_SOURCE_REQUIRED` | Inspection report recommendation categorization | Obtain official DoCA circular specifying form and timeline of statutory Improvement Notices. |
| **`GAP-VISION-01`**| Optical Experiment | Empirical measurement of pixel-to-millimeter homography scale factor error under varied camera angles ($0^\circ \dots 30^\circ$). | `EXPERIMENT_REQUIRED` | Quantitative measurement accuracy claims | Print certified ArUco / checkerboard targets; measure with digital caliper; compute reprojection residuals. |
| **`GAP-VISION-02`**| Optical Experiment | Empirical blur variance threshold (Laplacian variance) and glare mask HSV cutoffs under mixed lighting. | `EXPERIMENT_REQUIRED` | Quality gate parameter freeze | Capture 100 test exposures under outdoor sunlight, incandescent, and LED supermarket lighting; plot ROC curve. |
| **`GAP-VISION-03`**| Optical Experiment | Parametric cylindrical label unwrapping error on varying can radii ($30\text{ mm} \dots 60\text{ mm}$). | `EXPERIMENT_REQUIRED` | Font height measurement on curved containers | Run dewarping trials against ruled grid labels wrapped around certified test cylinders. |
| **`GAP-DATA-01`**  | Data Rights | Commercial packaging trade dress, brand logos, and artwork copyright clearance for dataset sharing. | `RIGHTS_VERIFICATION_REQUIRED` | Public release of retail packaging benchmark dataset | Legal counsel review of Section 52 fair dealing provisions of the Indian Copyright Act for statutory inspection datasets. |
| **`GAP-BENCH-01`** | Empirical Benchmark | Character Error Rate (CER) and Word Error Rate (WER) of PaddleOCR PP-OCRv4 on Indian FMCG packaging labels. | `EXPERIMENT_REQUIRED` | Stating measured OCR accuracy | Execute automated benchmark against annotated `data/golden/` test set; record confusion matrices in `benchmarks/reports/`. |

---

## 3. Governance Policy for Research Gaps

1. **No Assumption Policy:** Items in this register must remain marked `PRIMARY_SOURCE_REQUIRED` or `EXPERIMENT_REQUIRED` until physical proof (PDF file with SHA-256 hash, or measured experimental log) is committed to disk.
2. **Execution Gate:** No rule may enter `rules/current/` while its corresponding legal gap remains unresolved.
3. **Claim Gate:** No document may assert numerical precision or accuracy while its corresponding experimental gap remains unresolved.
