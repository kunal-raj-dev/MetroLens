# CURRENT STATE: MEMBER 5 — BASELINE M5-1
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering, Web Application & User Experience Lead  
**Timestamp:** 2026-09-05T17:10:00+05:30  
**Phase:** Chunk M5-1 — Frontend Foundation + Design System + Application Shell  

---

## 1. Initial State Prior to M5-1 Execution
Before starting M5-1, the `apps/web` directory contains only the following bare scaffold files:
- `next.config.mjs`
- `package.json`
- `tsconfig.json`
- `README.md`
- `src/app/layout.tsx` (minimal shell, references unconfigured Tailwind classes)
- `src/app/page.tsx` (static text placeholder)

### Missing Foundation Elements Identified:
- No `tailwind.config.ts` or `tailwind.config.js`
- No `postcss.config.js`
- No `src/app/globals.css`
- No UI component library or design tokens
- No component directories (`src/components/ui`, `src/features`, `src/services`, `src/types`, `src/hooks`, `src/utils`, `src/mocks`)
- `node_modules` not installed yet

---

## 2. Inviolable Stack and Scope Boundaries
- **Framework**: Next.js 14.2.5 (App Router) — Strict: Do NOT replace with Vite.
- **Runtime / UI**: React 18.3.1, TypeScript 5.5.3, Tailwind CSS 3.4.4, Lucide React icons.
- **Path Aliases**: `@/*` mapped to `./src/*`.
- **Architectural Boundary**:
  - Frontend owns: **Presentation**, **User Interaction**, and **API Client Adapter**.
  - Frontend does NOT own: Legal compliance logic, OCR inference, calibration mathematics, or physical measurements.
- **Member 1 Coordinate Invariant**: Member 1 OCR output coordinates are in **original-image pixel space**. The frontend must never convert or distort them into arbitrary percentages.
- **Backend Seam**: `POST /api/v1/inspect` consuming `multipart/form-data` with 15MB limit.

---

## 3. Scope of Chunk M5-1
1. Setup PostCSS and Tailwind CSS configuration (`tailwind.config.ts`, `postcss.config.js`).
2. Implement semantic design tokens and dark inspection theme in `src/app/globals.css`.
3. Create reusable, accessible UI primitives:
   - `Button`
   - `Card` (Header, Title, Description, Content, Footer)
   - `Badge`
   - `StatusIndicator` (mapping backend verdicts: `COMPLIANT`, `NON_COMPLIANT`, `SUSPECT_REVIEW`, `INCONCLUSIVE`)
   - `Dialog` / `Modal` (accessible with focus trap and keyboard ESC)
   - `Tooltip`
   - `Alert`
   - `Skeleton`
   - `Input`
4. Build Officer Workstation Application Shell (`Header`, inspection hero workspace, empty state).
5. Establish type system foundation (`src/types/inspection.ts`).
6. Set up directory scaffolds for services, mocks, features, and utils.
7. Verify compilation, build, and real browser rendering.
