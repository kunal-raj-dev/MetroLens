# MetroLens AI — Repository Clutter Cleanup Plan
**Audit Baseline Date:** 2026-09-05  
**Execution Constraint:** ADVISORY ONLY — NO FILES ARE DELETED OR MODIFIED DURING THIS AUDIT.  
**Action Categories:** `KEEP`, `ARCHIVE`, `MERGE`, `DELETE LATER`, `REVIEW FIRST`

---

## 1. Clutter Identification & Recommendation Registry

| # | Path | Action | Why It Is Clutter | Technical Risk | Dependencies |
| :- | :--- | :--- | :--- | :--- | :--- |
| **1** | `ALL-IN-ONE context/METROLENS_AI_ALL_IN_ONE_DOCS.md` | **DELETE LATER** (or Gitignore) | 720KB redundant concatenation of files in `docs/`. Diverges automatically as soon as any underlying doc is updated. | **VERY LOW**. Can be regenerated in 2 seconds via `python tools/build_all_in_one_context.py`. | None. |
| **2** | `ALL-IN-ONE context/` | **DELETE LATER** | Directory contains only the single generated file above. | **VERY LOW**. | None. |
| **3** | `problem statement #1/` | **ARCHIVE** to `archive/` | Historical initial research dossier (HTML, PDF, MD, script totaling ~1MB). Completely superseded by `docs/01_PROBLEM_STATEMENT/`. | **LOW**. May contain early reference notes; safe to preserve in an archive folder. | None. |
| **4** | `experiments/` (all 8 empty subdirs) | **ARCHIVE** or **DELETE LATER** | `calibration/`, `dewarping/`, `end_to_end/`, `extraction/`, `font_measurement/`, `ocr/`, `pdp_detection/`, `rules/` contain only `.gitkeep`. Active experiments live under `AI_CONTEXT/EXPERIMENTS/`. | **ZERO**. Contains no code. | None. |
| **5** | `assets/` (all 5 empty subdirs) | **KEEP** (Populate as needed) | `demo/`, `diagrams/`, `presentation/`, `sample_packages/`, `screenshots/` contain only `.gitkeep`. Will be needed for presentation materials. | **ZERO**. | Presentation team. |
| **6** | `regulations/` (10 empty subdirs) | **DELETE LATER** | Subdirectories (`amendments/`, `current/`, etc.) contain only `.gitkeep`. Real legal source files live under `METROLENS_LEGAL_SOURCE_PACK/`. | **ZERO**. Canonical source registry is `regulations/source_registry.yaml`. | Verification scripts only check `source_registry.yaml`. |
| **7** | `benchmarks/datasets/`, `protocols/`, `reports/`, `results/`, `runs/` | **REVIEW FIRST** | Empty directories containing only `.gitkeep`. Real benchmark code currently resides under `benchmarks/ocr/chunk*/`. | **LOW**. Member 6 work plan references `benchmarks/results/`. Check if scripts expect this folder before deleting. | Member 6. |
| **8** | `infra/deployment/`, `monitoring/`, `storage/` | **REVIEW FIRST** | Empty scaffold directories. | **ZERO**. | DevOps setup. |
| **9** | `pptx/SIH2026-IDEA-Presentation-Format.pptx` | **KEEP** | Official competition slide deck template (924 KB). Needed for final submission. | **HIGH (If deleted)**. Loss of official submission asset. | Pitch presentation team. |
| **10**| `METROLENS_LEGAL_SOURCE_PACK/99_ARCHIVE/` | **KEEP** | Contains 8 archived PDFs and harvest scripts from the legal source gathering phase. | **LOW**. Serves as provenance verification for collected acts. | Legal verification scripts. |
| **11**| `CURRENT_STATE/CHUNK_1_STATUS.md`, `CHUNK_2_STATUS.md`, `CHUNK_3_STATUS.md` | **KEEP** | Historical status checkpoints documenting evolution of the perception engine. | **MODERATE (If deleted)**. Documents experimental decisions and prevents AI re-inventing past conclusions. | AI Context. |
| **12**| `docs/API_CONTRACT.md` vs `docs/04_ARCHITECTURE/SYSTEM_ARCHITECTURE.md` | **MERGE** | API contract is defined in multiple places with slight parameter differences. | **LOW**. Consolidating prevents endpoint confusion. | Member 4, Member 5. |

---

## 2. Safe Post-Audit Execution Sequence

1. **Step 1 (Zero-Risk Archive):** Create `archive/historical/` and move `problem statement #1/` into it.
2. **Step 2 (Prune Dead Scaffold):** Remove empty directories under `experiments/` that have no corresponding package code.
3. **Step 3 (Gitignore Generated Dumps):** Add `ALL-IN-ONE context/` to `.gitignore` and provide a script in `tools/` to generate it ephemerally when an external prompt requires it.
4. **Step 4 (Retain All Code & Models):** Unconditionally preserve all files in `packages/`, `apps/`, `models/`, `data/`, `CURRENT_STATE/`, and `METROLENS_LEGAL_SOURCE_PACK/`.
