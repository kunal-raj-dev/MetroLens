# System Integration Baseline State

**Timestamp:** September 2026  
**Milestone:** Complete M1 → M5 System Integration  

---

## 1. Monorepo Baseline Inventory

- **Python Version:** 3.14.3 (Windows 11 AMD64)
- **Node.js Version:** v25.6.1 (npm 11.9.0)
- **Installed Packages:**
  - `nirikshak-calibration` (0.1.0) -> `packages/calibration`
  - `nirikshak-evidence` (0.1.0) -> `packages/evidence`
  - `nirikshak-extraction` (0.1.0) -> `packages/extraction`
  - `nirikshak-measurement` (0.1.0) -> `packages/measurement`
  - `nirikshak-ocr` (0.1.0) -> `packages/ocr`
  - `nirikshak-reporting` (0.1.0) -> `packages/reporting`
  - `nirikshak-rules-engine` (0.1.0) -> `packages/rules-engine`
  - `nirikshak-shared` (0.1.0) -> `packages/shared`
  - `nirikshak-vision` (0.1.0) -> `packages/vision`
- **Frontend App:** `apps/web` (Next.js 16.1.6, React 19.2.3)
- **Backend API:** `apps/api` (FastAPI 0.115+, Uvicorn 0.34+)

---

## 2. Test Execution Baseline

| Test Target | Runner | Passed | Failed | Duration |
| :--- | :--- | :--- | :--- | :--- |
| Monorepo Python Tests | Pytest 9.1.1 | 807 | 0 | 58.80s |
| Cross-Member Contracts | Pytest 9.1.1 | 12 | 0 | 0.81s |
| System E2E Suite | Pytest 9.1.1 | 15 | 0 | 1.45s |
| Browser E2E Workflows | Playwright 1.62.0 | 3 | 0 | 14.04s |
| Frontend Unit/Component | Vitest | 174 | 0 | 4.80s |
| **Total Test Verification** | **All Runners** | **1,011** | **0** | **~80s** |
