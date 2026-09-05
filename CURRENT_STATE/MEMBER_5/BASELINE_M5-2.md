# BASELINE: MEMBER 5 — CHUNK M5-2
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering & Web UX Lead  
**Timestamp:** 2026-09-05T17:35:00+05:30  
**Baseline Phase:** Starting Chunk M5-2 (Image Upload + Inspection Client + Mock/Live Adapter)  
**Previous Milestone:** M5-1 Complete & Verified (App Shell, Mastercard Design Tokens, 10 UI Primitives)

---

## 1. Initial State Prior to M5-2
- `apps/web/` has Next.js 14 App Router, React 18, Tailwind CSS v3 with Mastercard design tokens.
- `apps/web/src/components/ui/` has 10 tested primitives.
- `apps/web/src/types/contract.ts` contains direct backend DTO interfaces mirroring `contracts.py`.
- `apps/web/src/types/frontend.ts` contains initial `FrontendInspectionModel` scaffolding.
- `apps/web/src/services/index.ts` has preliminary `IInspectionClient` interface.
- Packaging Ingestion Zone in `page.tsx` is currently an `EmptyState` placeholder.
- No client-side image validation, magic bytes sniffing, or file decode validation exists.
- No concrete `MockInspectionAdapter` or `LiveInspectionAdapter` exists.
- Synthetic regression assets exist at `data/synthetic/regression/` (`SYNTH-01` to `SYNTH-08`).

## 2. Invariants & Rules
- **Coordinate Space:** Member 1 OCR coordinates remain frozen original pixel coordinates. No client-side mutation.
- **No Legal Engine Logic:** Frontend does not compute font heights, Rule 6 compliance, or USP arithmetic.
- **No Cloud AI / No ONNX in Browser:** Frontend delegates inference exclusively to backend/adapters.
- **Backend Boundary:** 15 MiB limit, accepted formats: JPEG, PNG, WebP. Backend is authoritative security boundary.
- **Git Safety:** Zero git commits, zero git pushes.
