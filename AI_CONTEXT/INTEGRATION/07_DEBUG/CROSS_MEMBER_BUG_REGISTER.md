# Cross-Member Bug Register

**Milestone:** M1 → M5 Complete System Integration  
**Date:** September 2026  

---

## Registry of Discovered Cross-Member Anomalies & Resolutions

### BUG-INT-001: Missing `qrcode` Library in Environment
- **Severity:** High (Crash / Blocker)
- **Subsystem:** M4 Reporting (`packages/reporting` & `apps/api/routes/report.py`)
- **Symptom:** `ModuleNotFoundError: No module named 'qrcode'` upon importing report generator or calling `POST /api/v1/report/pdf`.
- **Root Cause:** Environment had `reportlab` installed, but `qrcode` dependency was missing from virtual environment.
- **Resolution:** Installed `qrcode-8.2` in Python 3.14 environment.
- **Status:** **RESOLVED & VERIFIED**.

### BUG-INT-002: In-Memory Rate Limiting False Positives During Test Runs
- **Severity:** Medium (Flaky Tests)
- **Subsystem:** M4 API Gateway (`apps/api/middleware/rate_limit.py`)
- **Symptom:** Integration test batch failed with HTTP 429 `TOO_MANY_REQUESTS` when executing multiple sequential pipeline tests against the ASGI TestClient.
- **Root Cause:** In-memory token bucket evaluated localhost requests as exceeding 60 req/min during rapid automated test execution.
- **Resolution:** Added `headers={"X-Bypass-Rate-Limit": "true"}` to TestClient fixtures in `tests/integration/test_vertical_slice_0.py`.
- **Status:** **RESOLVED & VERIFIED**.

### BUG-INT-003: Mock Fixture Key Mismatch in Legacy Inspection Test
- **Severity:** Low (Test Failure)
- **Subsystem:** M4 Integration Tests (`tests/integration/test_inspect_endpoint.py`)
- **Symptom:** `test_inspect_successful_compliant_upload` failed because it did not pass the required mock fixture key parameter.
- **Root Cause:** Test fixture signature updated in Member 4 refactor without updating legacy test call.
- **Resolution:** Explicitly supplied `mock_fixture_key="PKG-01-COMPLIANT-FMCG-CASHEWS"`.
- **Status:** **RESOLVED & VERIFIED**.

### BUG-INT-004: Low-Resolution Rejection of Synthetic Benchmark Fixtures
- **Severity:** Medium (Operational Gotcha)
- **Subsystem:** M4 API Security Gate (`apps/api/routes/inspect.py`)
- **Symptom:** Synthetic test images (640x360 px) resulted in HTTP 422 `IMAGE_RESOLUTION_TOO_LOW`.
- **Root Cause:** M4 strictly enforces image dimensions >= 800x600 px to ensure metrological accuracy under PCR 2011.
- **Resolution:** Real-world specimens (3072x4080 px) pass cleanly; test harnesses updated with >=800x600 synthetic targets.
- **Status:** **DOCUMENTED & WORKING AS DESIGNED**.

### BUG-INT-005: Playwright E2E Text Selector Collision
- **Severity:** Low (E2E Test)
- **Subsystem:** M5 Browser Test (`tests/e2e/test_browser_workflow.py`)
- **Symptom:** Playwright selector `text='NO IMAGE-VERIFIABLE VIOLATIONS', text='Overall Verdict'` failed to resolve single element.
- **Root Cause:** Comma syntax treated as compound selector in Playwright locator parser.
- **Resolution:** Replaced with `page.get_by_text("NO IMAGE-VERIFIABLE VIOLATIONS").first`.
- **Status:** **RESOLVED & VERIFIED**.
