# AI CONTEXT: MEMBER 5 (WEB FRONTEND & USER EXPERIENCE)
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering, Web Application & User Experience Lead  
**Scope:** `apps/web/` (Next.js 14 App Router, TypeScript, Tailwind CSS, Lucide React)  
**Status:** M5-0 Repository & Contract Audit Completed | Ready for M5-1 Foundation  

---

## 1. Subsystem Mission & Role
Member 5 owns the regulatory officer workstation and judge-facing explainability interface. The goal is to make complex Legal Metrology statutory compliance (Packaged Commodities Rules 2011, Jan Vishwas Act 2026) visually clear, mathematically transparent, and tamper-evident to non-technical users.

### Core Architecture Philosophy
$$\text{AI Perceives (M1 OCR)} \longrightarrow \text{Math Validates (M2 Scale)} \longrightarrow \text{Rules Decide (M3 Rules)} \longrightarrow \text{Frontend Visualizes (M5 UI)}$$

Member 5 **never** acts as a secondary rule engine. It visualizes decisions computed by the backend, preserves sub-pixel coordinate geometry from Member 1, and enables human-in-the-loop regulatory oversight.

---

## 2. Directory Navigation
```text
AI_CONTEXT/MEMBER_5_WEB_FRONTEND/
├── INDEX.md                         # This file: Subsystem overview and index
├── 01_REVISED_WORK_PLAN.md          # Re-architected 7-chunk execution roadmap (M5-0 to M5-6)
├── 02_ARCHITECTURAL_BOUNDARIES.md   # The 8 boundary corrections and seam principles
└── 03_SEAM_CONTRACTS_AUDIT.md       # Monorepo contract mappings (M1, M2, M3, M4 -> M5)
```

---

## 3. High-Level 7-Chunk Progression Summary

| Chunk ID | Chunk Name | Target Scope | Current Status | Key Deliverable |
| :---: | :--- | :--- | :---: | :--- |
| **M5-0** | **Repository & Contract Audit** | `apps/web`, `apps/api`, `packages/shared`, `packages/ocr` | **COMPLETE** | Current state audit, contract gap analysis, coordinate invariance |
| **M5-1** | **Frontend Foundation & Design System** | `apps/web/src/components/ui`, `globals.css`, Tailwind config | **READY** | UI primitives, design tokens, accessible multi-modal badges |
| **M5-2** | **Upload Zone & Inspection Client** | `ImageUploadZone.tsx`, `inspectionClient.ts` | **PENDING** | Drag/drop, 15MB guard, Mock & Live API adapter layer |
| **M5-3** | **Results Dashboard & Evidence Canvas** | `ComplianceDashboard.tsx`, `EvidenceCanvas.tsx` | **PENDING** | 5-state multi-modal banner, unnormalized canvas affine zoom/pan |
| **M5-4** | **Declarations & Inspector Review** | `DeclarationTable.tsx`, `InspectorReviewModal.tsx` | **PENDING** | Click-to-zoom crops, 1-tap confirm, 2-point caliper override dispatch |
| **M5-5** | **Live API, Real Samples & PDF** | `/api/v1/inspect`, `SamplePackageSelector.tsx`, PDF | **PENDING** | End-to-end FastAPI integration, 8 real synthetic demo packages, PDF |
| **M5-6** | **QA, Accessibility & Demo Freeze** | Cross-browser, responsive matrix, projector audit | **PENDING** | WCAG 2.1 AA audit, full responsive suite, M5 Release Candidate Freeze |

---

## 4. Key Monorepo References & Documents
- **Individual Work Plan (Legacy 9-Day reference)**: `docs/team/MEMBER_5_WORK_PLAN.md`
- **Monorepo Current State Baseline**: `CURRENT_STATE/MEMBER_5_BASELINE.md`
- **Monorepo Current State Status**: `CURRENT_STATE/MEMBER_5_STATUS.md`
- **API Contract Specification**: `docs/API_CONTRACT.md`
- **Shared Pydantic Seam Contracts**: `packages/shared/src/nirikshak_shared/models/contracts.py`
- **Member 1 Frozen OCR Types**: `packages/ocr/src/nirikshak_ocr/types.py`
- **Worker Pipeline Orchestrator**: `apps/worker/main.py`
- **Synthetic Test Fixtures**: `data/synthetic/regression/`
