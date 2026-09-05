# TESTING STRATEGY & VERIFICATION SPECIFICATION (V1.0)
# MetroLens AI™ — Web Application Quality Assurance & Benchmark Framework
### Document Status: Authoritative Quality Assurance Reference | Standards: RFC 2119
**Test Execution Engines:** `pytest` (Python Backend) | `vitest` (React Frontend) | Anti-Hallucination Scripts

---

## 1. Executive Purpose & Quality Assurance Mission

MetroLens AI operates as an engineering decision-support tool for statutory legal enforcement. A software defect that fails to flag an illegal net quantity omission or falsely cites a compliant merchant has serious regulatory and legal repercussions.

This document establishes the **multi-tiered testing pyramid, automated verification gates, regression benchmark protocols, and adversarial upload fuzzing suites** designed specifically for the **Online Web Application MVP**.

---

## 2. The Web Application Testing Pyramid

```text
                             ▲
                            / \
                           /   \      Tier 5: E2E Browser Flows (Playwright / Cypress)
                          /     \     - Drag & drop upload -> 5-State cards -> PDF download
                         /-------\
                        /         \   Tier 4: Empirical Benchmark Suite (tests/benchmarks/)
                       /           \  - 35-SKU physical packaging dataset (CER, MAE, Latency)
                      /-------------\
                     /               \ Tier 3: Security & Upload Fuzzing (tests/security/)
                    /                 \ - Decompression bombs, spoofed magic-bytes, path traversal
                   /-------------------\
                  /                     \ Tier 2: API & Integration Tests (tests/integration/)
                 /                       \ - FastAPI multipart uploads, status codes, error payloads
                /-------------------------\
               /                           \ Tier 1: Deterministic Unit Tests (tests/unit/, tests/rules/)
              /                             \ - Pure Python rule state machine, USP math, homography
             /-------------------------------\
            /                                 \ Tier 0: Anti-Hallucination Gates (scripts/verification/)
           /                                   \ - Primary legal source checksums, claims validation
          ───────────────────────────────────────
```

---

## 3. Tier-by-Tier Testing Protocols

### Tier 0: Anti-Hallucination & Legal Source Gates
Enforces that every algorithmic calculation and legal citation in the repository traces directly to authentic Gazette notifications:
- **`python scripts/verification/verify_legal_sources.py`**: Verifies SHA-256 checksums and provenance of all primary Acts (2009, 2023, 2026) and LMPC Rules in `regulations/`.
- **`python scripts/verification/verify_rule_registry.py`**: Ensures all active rules in `rules/current/` conform to the canonical JSON schema and cite in-force statutory clauses.
- **`python scripts/verification/verify_claims.py`**: Blocks CI merges if any benchmark claim is marked `VERIFIED` without an empirical benchmark report artifact.

---

### Tier 1: Deterministic Unit Testing (`tests/unit/`, `tests/rules/`)
Verifies isolated algorithmic components in pure Python without web server or disk dependencies:
- **Rule Engine Conformance (`test_rules_engine.py`):**
  - Evaluates all 8 clauses of Rule 6(1).
  - Tests Rule 26 statutory exemptions (net quantity $\le 10\text{g/ml}$, wholesale $> 25\text{kg}$).
  - Tests Rule 7 Table-I and Table-II area-to-height bracket lookups across all 5 area tiers.
- **Unit Sale Price (USP) Arithmetic (`test_usp_arithmetic.py`):**
  - Floating-point division and statutory rounding: $\text{Expected USP} = \text{MRP} / \text{NetQty}$.
  - Verification of standard denominators: ₹/g, ₹/kg, ₹/ml, ₹/l, ₹/piece.
  - Detects prohibited abbreviations ("gm", "gms", "ML", "pk") and flags non-compliance.
- **Geometric Calibration Math (`test_calibration_math.py`):**
  - Ellipse fitting algorithms on known circular contours.
  - Homography matrix calculation ($3 \times 3$ transform matrix $H$).
  - Vertical generator strip angle projection ($\cos\phi \ge 0.94$).

---

### Tier 2: API & Integration Testing (`tests/integration/`)
Validates the FastAPI gateway, multipart upload ingestion, and JSON serialization using `httpx.AsyncClient`:
- **File Upload Contract:** Submits valid JPEG, PNG, and WebP payloads; asserts HTTP 200 and schema validity.
- **Error Mapping:** Submits oversized payloads ($> 15\text{MB}$) and asserts HTTP 413; submits `.txt` or `.exe` and asserts HTTP 415.
- **Health & Readiness:** Tests `GET /api/v1/health` under diverse load conditions.
- **PDF Generation:** Asserts `POST /api/v1/report/pdf` returns a valid binary PDF with correct HTTP headers.

---

### Tier 3: Web Security & Adversarial Upload Fuzzing (`tests/security/`)
Exposes the web ingestion pipeline to real-world malicious and malformed inputs:
- **Decompression Bomb Defense:** Submits synthetic 40,000 x 40,000 pixel 1-bit images; verifies that Pillow triggers `Image.DecompressionBombError` and API cleanly returns HTTP 422 instead of crashing.
- **Magic-Byte Mismatch:** Submits an executable shell script renamed to `photo.jpg`; verifies immediate rejection via magic-byte inspection.
- **Path Traversal Inoculation:** Submits filenames containing `../../../../etc/passwd`; verifies filename is safely discarded and replaced with a server-generated UUID4.
- **Malformed Image Headers:** Submits truncated image streams; asserts graceful HTTP 422 error without unhandled Python stack traces.

---

### Tier 4: Empirical Benchmark Regression Suite (`tests/benchmarks/`)
Managed by M5; evaluates the complete pipeline against physical retail packages:
- **Dataset Composition:** 35 real Indian packaging SKUs across food, cosmetics, pharmaceuticals, and household goods.
- **Ground Truth Standard:** 1200 DPI flatbed optical scans with manually verified bounding boxes and caliper-measured numeral heights.
- **Evaluated Metrics:**
  - Character Error Rate (CER): $\le 6.0\%$.
  - Word Error Rate (WER): $\le 10.0\%$.
  - Scale Factor ($S$) Error: $\le 5.0\%$.
  - Numeral Height Mean Absolute Error (MAE): $\le 0.15\text{mm}$.
  - End-to-End Latency: $\le 2,500\text{ms}$ on 4-core CPU.
- **Regression Blocker:** Any pull request that increases CER by $> 0.5\%$ or causes a regression on synthetic statutory cases is automatically blocked by CI.

---

### Tier 5: Real Browser End-to-End Verification
Verifies the complete user journey in a real browser:
- Tests drag-and-drop file upload in Chrome, Firefox, and Safari viewports.
- Verifies upload progress indicator animation.
- Asserts 5-State compliance badge renders with correct color codes and plain-language reasoning.
- Clicks declaration items and verifies visual evidence modal displays synchronized bounding box crops.
- Clicks "Download Report" and verifies PDF download initiates cleanly.

---

## 4. Automated Test Nodes Directory (T01–T06)

| Node ID | Purpose & Target Module | Execution Command | Success Threshold |
| :---: | :--- | :--- | :--- |
| **T01** | **Quality Gate Unit Suite**<br/>Blur ($\sigma^2 < 120$) & Glare ($> 8\%$) | `python -m pytest tests/unit/test_quality_gate.py` | 100% pass on 20 synthetic frames. |
| **T02** | **Calibration & Scale Harness**<br/>₹10 coin ellipse detection & homography | `python -m pytest tests/unit/test_calibration.py` | Scale error $< 5.0\%$ at tilt $\le 15^\circ$. |
| **T03** | **OCR Benchmark Suite**<br/>Multilingual text detection & recognition | `python -m pytest tests/benchmarks/test_ocr_benchmark.py` | CER $< 6.0\%$, CPU latency $< 800\text{ms}$. |
| **T04** | **Deterministic Rule Suite**<br/>Rules 6, 6(11), 7, 26 statutory cases | `python -m pytest tests/rules/test_rules_engine.py` | 100% pass across 25 statutory test cases. |
| **T05** | **Evidentiary PDF & API Suite**<br/>SHA-256 seal & eMaap mock sync | `python -m pytest tests/integration/test_reporting_and_api.py` | PDF compiles in $< 500\text{ms}$, HTTP 200 OK. |
| **T06** | **Headless E2E Pipeline**<br/>Image In $\rightarrow$ Rules $\rightarrow$ Verdict | `python -m pytest tests/e2e/test_e2e_pipeline.py` | Full pipeline executes in $< 2.5\text{s}$ on CPU. |

---

## 5. CI/CD Integration & PR Merge Gate

Every Pull Request submitted to `main` must pass the following automated GitHub Actions gate before maintainer merge:

```yaml
# .github/workflows/ci.yml
name: Continuous Integration & Verification Pipeline

on:
  pull_request:
    branches: [ main ]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python 3.14
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"
      
      - name: Install Dependencies
        run: pip install -r requirements.txt
      
      - name: Gate 0: Anti-Hallucination Verification
        run: |
          python scripts/verification/verify_legal_sources.py
          python scripts/verification/verify_rule_registry.py
          python scripts/verification/verify_claims.py
      
      - name: Gate 1: Code Linting & Static Typing
        run: ruff check .
      
      - name: Gate 2: Deterministic Unit & Rule Tests
        run: python -m pytest tests/unit/ tests/rules/
      
      - name: Gate 3: API & Security Integration Tests
        run: python -m pytest tests/integration/ tests/security/
```
