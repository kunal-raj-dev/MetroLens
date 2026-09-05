# MetroLens AI — Documentation Cleanup & Harmonization Plan
**Audit Baseline Date:** 2026-09-05  
**Execution Constraint:** ADVISORY ONLY — NO FILES ARE MODIFIED DURING THIS AUDIT.  
**Classification Taxonomy:** `KEEP CURRENT`, `MERGE`, `ARCHIVE`, `DEPRECATE`, `DELETE LATER`, `REVIEW`

---

## 1. Documentation Inventory & Classification

| Document / Group | Action | Rationale & Target State |
| :--- | :--- | :--- |
| **`CURRENT_STATE/PROJECT_SNAPSHOT.md`** | **KEEP CURRENT** | Canonical single-page project baseline. Update with each completed chunk. |
| **`docs/audit/*` (All Audit Documents)** | **KEEP CURRENT** | Permanent authoritative baseline establishing ground truth for the 6-member team. |
| **`docs/team/MEMBER_1_WORK_PLAN.md` to `MEMBER_6_WORK_PLAN.md`** | **KEEP CURRENT** | Individual accountability contracts for the 6 team members. Update with verified progress. |
| **`docs/PRODUCT_BLUEPRINT.md`** | **MERGE / HARMONIZE** | Contains target scope, but needs a clear disclaimer stating what is built vs what is planned. Merge duplicate architecture sections with `docs/ARCHITECTURE.md`. |
| **`docs/ARCHITECTURE.md`** | **MERGE / HARMONIZE** | Needs explicit removal or deprecation tag on Celery/Redis sections, marking local CPU execution as canonical. |
| **`docs/API_CONTRACT.md`** | **KEEP CURRENT / HARMONIZE** | Update endpoint paths to match `apps/api/main.py` (`POST /api/v1/inspections`). |
| **`docs/17_CLAIMS/CLAIMS_REGISTER.md`** | **KEEP CURRENT** | Authoritative anti-hallucination register checked by `scripts/verification/verify_claims.py`. |
| **`regulations/source_registry.yaml`** | **KEEP CURRENT** | Canonical metadata source of truth for sovereign legal instruments. |
| **`ALL-IN-ONE context/METROLENS_AI_ALL_IN_ONE_DOCS.md`** | **DELETE LATER** (or Gitignore) | Generated artifact prone to drift. Keep generator script in `tools/build_all_in_one_context.py`. |
| **`problem statement #1/SIH26034_Dossier.*`** | **ARCHIVE** | Historical inception documents. Move to `docs/archive/historical_dossier/`. |
| **`docs/AUDIT_V0_3.md` & `docs/ARCHITECTURE_REVIEW_V0_3.md`** | **ARCHIVE** | Early v0.3 milestone reviews. Superseded by the current Chunk 4 audit. |
| **`docs/00_PROJECT_CHARTER/` to `docs/17_CLAIMS/`** | **REVIEW & HARMONIZE** | Valuable domain encyclopedias, but must be clearly demarcated as TARGET REQUIREMENTS rather than existing code. |
| **`AI_CONTEXT/HANDOFFS/`** | **KEEP CURRENT** | Critical audit trail documenting the progression across execution chunks. |
| **`AI_CONTEXT/RUN_LOGS/`** | **KEEP CURRENT** | Granular execution history for AI pair programming sessions. |

---

## 2. Harmonization Guidelines

1. **Add Status Badges to Blueprint Documents:**  
   Every top-level architecture and blueprint document should feature a prominent banner:
   > `[STATUS: TARGET ARCHITECTURE / PARTIALLY IMPLEMENTED — Refer to docs/audit/CURRENT_PROJECT_DASHBOARD.md for physical code reality]`
2. **Eliminate Competing Sources of Truth:**  
   - Source of truth for **Current Progress:** `CURRENT_STATE/PROJECT_SNAPSHOT.md` and `docs/audit/`.
   - Source of truth for **OCR Models:** `models/manifest.yaml` and `packages/ocr/src/nirikshak_ocr/config.py`.
   - Source of truth for **Legal Acts:** `METROLENS_LEGAL_SOURCE_PACK/` and `regulations/source_registry.yaml`.
   - Source of truth for **API Contracts:** `apps/api/main.py` and `docs/API_CONTRACT.md`.
