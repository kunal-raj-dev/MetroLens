# MEMBER 5 BASELINE: STARTING ENVIRONMENT & CODEBASE SNAPSHOT
**Project:** MetroLens AI™ (SIH26034)  
**Lead:** Member 5 — Frontend Engineering & Web UX Lead  
**Subsystem:** Officer Inspection Workstation (`apps/web/`)  
**Snapshot Timestamp:** 2026-09-05T16:47:00+05:30  
**Phase:** M5-0 Audit Completed | Preparing for M5-1 Execution  

---

## 1. Monorepo Location & Framework State

- **Primary Directory**: `apps/web/`
- **Framework**: Next.js `14.2.5` (App Router)
- **Runtime**: Node.js v20+ / React `18.3.1` / React DOM `18.3.1`
- **Language**: TypeScript `5.5.3` (Strict mode enabled, `@/*` alias mapped to `./src/*`)
- **Package Manager**: `npm`
- **Current File Inventory in `apps/web/`**:
  - `package.json`: Configured with Next.js, React, Tailwind, PostCSS, Lucide React
  - `next.config.mjs`: `reactStrictMode: true`, `output: "standalone"`
  - `tsconfig.json`: Module resolution bundler, Next.js plugin enabled
  - `src/app/layout.tsx`: HTML shell with header title ("NIRIKSHAK - SIH26034")
  - `src/app/page.tsx`: Static 3-card landing page placeholder
  - `README.md`: High-level purpose and tech stack description
- **Missing Foundations to be Created in M5-1**:
  - `tailwind.config.ts` (currently missing)
  - `postcss.config.js` (currently missing)
  - `src/app/globals.css` (currently missing)
  - Subdirectories: `src/components/`, `src/services/`, `src/types/`, `src/mocks/`, `src/utils/`

---

## 2. Upstream Monorepo Seam Health

| Upstream Subsystem | Status in Repo | Interaction with Member 5 |
| :--- | :---: | :--- |
| **Member 1 (OCR)** | **PERMANENTLY FROZEN** | Delivers unnormalized original image pixel coordinates in `OCRToken` polygons and bounding boxes. M5 preserves these coordinates directly on Canvas without percentage conversion. |
| **Member 2 (Calibration)** | In Progress | Will deliver optical scale factor ($S = \text{mm/px}$) and manual calibration endpoint. M5 provides 2-point caliper interaction (pixel distance only). |
| **Member 3 (Rules Engine)** | In Progress | Owns deterministic compliance verdicts (`OverallVerdict`, `RuleEvaluation`). M5 visualizes these states without embedding legal logic. |
| **Member 4 (API & Pipeline)** | In Progress | Gateway active at `POST /api/v1/inspect` consuming `multipart/form-data` with 15MB limit and returning `InspectionResult`. M5 connects via `InspectionClient` adapter. |
| **Member 6 (QA & Datasets)** | In Progress | Curation of physical packaging dataset. Synthetic regression suite (`SYNTH-01` to `SYNTH-08`) already available in `data/synthetic/regression/`. |

---

## 3. Available Real Test Image Fixtures

The following genuine synthetic package assets are present in `data/synthetic/regression/` and verified for M5 demo failover integration:

1. `SYNTH-01-ENG-FMCG.png` (640x360) - Standard English biscuit packaging (Pass)
2. `SYNTH-02-HIN-FMCG.png` (640x360) - Pure Devanagari/Hindi Atta bag (Pass)
3. `SYNTH-03-MIXED-BILINGUAL.png` (640x380) - Bilingual English + Hindi snack carton (Pass)
4. `SYNTH-04-MICRO-FONT.png` (640x320) - Microscopic numeral height deficit (Fail - Rule 7)
5. `SYNTH-05-LIQUID-VOLUME.png` (640x360) - Liquid handwash bottle with volume in ml (Pass)
6. `SYNTH-06-PROHIBITED-UNITS.png` (640x320) - Prohibited plural units "Gms", "ML" (Fail - Rule 13)
7. `SYNTH-07-BLANK-FRAME.png` (640x320) - Blank texture failure mode (Inconclusive)
8. `SYNTH-08-LOW-CONTRAST-FADED.png` (640x320) - Low-contrast faded date stamp (Suspect Review)

---

## 4. Git & Working Tree Invariants

- **Active Branch**: Current working branch
- **Git HEAD**: Preserved cleanly
- **Safety Enforcement**: **ZERO COMMITS, ZERO PUSHES, ZERO FILE DELETIONS**.
- **Execution Mode**: Documentation of baseline complete. Source code modification deferred until explicit user instruction.
