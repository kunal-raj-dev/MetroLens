# MetroLens AI — Technical Debt Registry
**Audit Baseline Date:** 2026-09-05  
**Severity Classification:** `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`  
**Standard:** Only technical debt confirmed by physical code and filesystem evidence is cataloged.

---

## 1. Technical Debt Inventory

### 1. Architectural & Interface Debt

#### TD-01: Endpoint Path Divergence between API Code and Work Plans (Severity: HIGH)
- **Component:** `apps/api/main.py` vs `docs/team/MEMBER_4_WORK_PLAN.md` vs `docs/API_CONTRACT.md`
- **Evidence:** `main.py` line 34 defines `@app.post("/api/v1/inspections")` (plural). Work plans and documentation references cite `POST /api/v1/inspect` (singular).
- **Risk:** Frontend client calls will fail with HTTP 404 Not Found if the frontend engineer builds against the documentation rather than inspecting the router code.
- **Remediation:** Standardize on `/api/v1/inspections` (or add an alias router) and update the contract documentation.

#### TD-02: Framework Divergence between Frontend Code and Work Plan (Severity: MEDIUM)
- **Component:** `apps/web/package.json` vs `docs/team/MEMBER_5_WORK_PLAN.md`
- **Evidence:** `MEMBER_5_WORK_PLAN.md` explicitly mandates `React 19 + TypeScript + Vite SPA`. In reality, `apps/web/` is scaffolded as a `Next.js 14.2.5` App Router project using `React 18.3.1`.
- **Risk:** Contradictory instructions for anyone implementing frontend components; confusion regarding build commands (`npm run dev` in Next.js vs Vite dev server).
- **Remediation:** Update `MEMBER_5_WORK_PLAN.md` to formally reflect Next.js 14 App Router, or replace `apps/web/` with a Vite scaffold if SSR is not required.

#### TD-03: Stale Architecture References to Celery and Redis (Severity: HIGH)
- **Component:** `docs/ARCHITECTURE.md`, `docs/PRODUCT_BLUEPRINT.md`
- **Evidence:** Architecture documents describe distributed Celery workers and Redis message brokers. However, ADR-011 and `CURRENT_STATE/PROJECT_SNAPSHOT.md` formally rejected Celery/Redis for the 8-day sprint in favor of direct local CPU execution.
- **Risk:** New team members or AI agents may attempt to install, configure, or troubleshoot non-existent Celery workers.
- **Remediation:** Mark the Celery/Redis sections in architecture documents as `SUPERSEDED (HISTORICAL)` and document direct synchronous execution.

---

### 2. Implementation & Code Quality Debt

#### TD-04: Mock Return in Core API Ingestion Route (Severity: CRITICAL)
- **Component:** `apps/api/main.py` (lines 39–51)
- **Evidence:** `submit_inspection` returns hardcoded dummy `InspectionResult` without decoding the image payload or invoking `OCRService`, `nirikshak_vision`, or `nirikshak_rules_engine`.
- **Risk:** The API is non-functional for real testing and creates a false impression of backend readiness.
- **Remediation:** Import `nirikshak_ocr.OCRService` and call `extract_observations()`.

#### TD-05: Incomplete Image Quality Gate Implementation (Severity: HIGH)
- **Component:** `packages/vision/src/nirikshak_vision/__init__.py` (lines 51–56)
- **Evidence:** Quality gate calculates `np.var(gray)` as a proxy for Laplacian blur variance instead of applying a true 2D discrete Laplacian filter (`cv2.Laplacian`), and calculates glare simply by thresholding `gray >= 250` rather than analyzing HSV saturation/value channels.
- **Risk:** Highly inaccurate blur and glare gating; false positives or false negatives during live image ingestion.
- **Remediation:** Implement standard OpenCV `cv2.Laplacian(gray, cv2.CV_64F).var()` and HSV specular highlight masking.

#### TD-06: Uninstalled Frontend Environment (Severity: MEDIUM)
- **Component:** `apps/web/`
- **Evidence:** `node_modules` does not exist in `apps/web/`.
- **Risk:** Frontend cannot be started or tested locally without running `npm install`.
- **Remediation:** Run `npm install` in `apps/web/` and verify that `npm run build` passes.

---

### 3. Repository Structure & Artifact Debt

#### TD-07: Proliferation of Empty Placeholder Folders (Severity: LOW)
- **Component:** `assets/`, `experiments/`, `regulations/` (subdirs), `infra/deployment/`, `benchmarks/datasets/`
- **Evidence:** More than 25 subdirectories contain nothing except empty `.gitkeep` files.
- **Risk:** Visual clutter; makes navigation confusing for developers trying to find active code.
- **Remediation:** Retain only necessary folders; delete or archive unpopulated directories during repository cleanup.

#### TD-08: Redundant 720KB Concatenated All-in-One Documentation Dump (Severity: LOW)
- **Component:** `ALL-IN-ONE context/METROLENS_AI_ALL_IN_ONE_DOCS.md`
- **Evidence:** A single 720KB file concatenating 30+ markdown files. Prone to silent divergence whenever individual source documents in `docs/` are modified.
- **Risk:** Consumes significant disk/git space; risk of developers reading outdated concatenated text rather than the source docs.
- **Remediation:** Treat as a generated build artifact; ignore in git or add a pre-commit check to regenerate it automatically.

#### TD-09: Unimplemented Automated CI Workflow (Severity: MEDIUM)
- **Component:** `.github/`
- **Evidence:** `.github/workflows/` does not exist on disk.
- **Risk:** Regression errors and linting failures are not caught automatically on GitHub pull requests.
- **Remediation:** Add `.github/workflows/ci.yml` to run `python -m pytest` across the 89 tests.
