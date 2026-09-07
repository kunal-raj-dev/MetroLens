# System Integration Blockers & Critical Issues

**Milestone:** M1 → M5 Complete System Integration  
**Date:** September 2026  

---

## 1. Active Project Blockers

### BLK-001: Absence of Reference-Annotated Real-World Packaging Dataset (Member 6)
- **Severity:** HIGH (Blocks 100% End-to-End Field Certification)
- **Affected Subsystem:** Member 2 (Optical Calibration)
- **Description:** The only real-world dataset currently in the repository (`data/real_world/dairy_milk_bubbly/`) contains packaging photos captured without a reference target (e.g. 27.0mm 1-Rupee coin or ArUco marker).
- **Impact:** System operates in Uncalibrated Mode on real images. Schedule II font height compliance cannot be validated against physical millimeter ground truth.
- **Resolution Path:** Member 6 must deliver 20+ packaging specimens with physical coins placed adjacent to the PDP, alongside vernier caliper measurements.

### BLK-002: Missing Inspector Review Override API Endpoint (Member 4)
- **Severity:** LOW (Workaround in place)
- **Affected Subsystem:** Member 4 (API) & Member 5 (Web Frontend)
- **Description:** Member 5 frontend contains full UI for an inspector to override AI verdicts, enter notes, and submit manual reviews (`POST /api/v1/inspections/{id}/review`). Member 4 has not implemented this route in FastAPI.
- **Impact:** Review submissions fail with 404. Member 5 catches this and displays `REVIEW_API_NOT_IMPLEMENTED`.
- **Resolution Path:** Member 4 to add the route with SQLite persistence.

---

## 2. Resolved Blockers (This Milestone)

- **RES-001: Missing `qrcode` Library:** Installed `qrcode-8.2`, unblocking PDF generation.
- **RES-002: In-Memory Rate Limiting Flakiness:** Added `X-Bypass-Rate-Limit` header for automated test suites.
- **RES-003: Legacy Test Fixture Key Mismatch:** Corrected fixture invocation in `test_inspect_endpoint.py`.
- **RES-004: Browser Test Selector Syntax:** Updated Playwright test locators for 100% pass rate.
