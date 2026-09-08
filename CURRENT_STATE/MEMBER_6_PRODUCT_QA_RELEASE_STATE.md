# MEMBER 6 — PRODUCT / QA / BENCHMARK / RELEASE STATE

**System Name:** MetroLens AI™ / Nirikshak AI (Legal Metrology Compliance System)  
**SIH Problem Statement:** SIH 2026 PS 26034 (Automated Compliance Verification for Pre-Packaged Commodities)  
**Subsystem / Role:** Member 6 — Product Integration, Quality Assurance, Benchmark Verification & Release Governance  
**Audit Date:** September 8, 2026  
**Git Commit Audit:**
- `HEAD_BEFORE_MEMBER_6`: `a06872f`
- `HEAD_AFTER_MEMBER_6`: `a06872f`
- `NEW_COMMIT_CREATED`: `NO`
- `PUSH_PERFORMED`: `NO`

---

## 1. Executive Verdict

**Verdict:** **APPROVED FOR CONTROLLED SIH DEMONSTRATION**  
**Physical Metrology Benchmark:** **`BENCHMARK_BLOCKED`**  
**Docker Runtime Execution:** **`NOT_VERIFIED`**  
**Live Network-Disabled Drill:** **`NOT_VERIFIED`**  

### Scope & Release Classification
Software integration and regression testing are verified for controlled SIH 2026 demonstration. Physical metrology benchmark remains BLOCKED. Docker runtime and live network-disabled execution are marked NOT_VERIFIED unless directly demonstrated.

This prototype is **NOT** certified for statutory enforcement, is **NOT** production-ready, and has **NOT** been metrologically validated against physical retail commodities.

---

## 2. Final Release Matrix

| Area | Result | Evidence |
|---|:---:|---|
| **Backend tests** | **PASS** | 832 passed, 0 failures (`pytest -q`, 196.70s) |
| **Frontend tests** | **PASS** | 307 passed, 0 failures (`npm test` across 6 test suites) |
| **E2E** | **PASS** | 3 passed, 0 failures (Playwright browser workflow) |
| **TypeScript** | **PASS** | 0 errors (`npx tsc --noEmit`, strict mode) |
| **Build** | **PASS** | Exit code 0, 4/4 static pages generated (`npm run build`) |
| **Security** | **PASS** | 11 passed, 0 failures (`tests/security/test_security_regression.py`) |
| **Synthetic OCR** | **POOR / DEFECT** | CER = `1.1961` (119.61% CER across 7 synthetic specimens) |
| **Physical OCR** | **BENCHMARK_BLOCKED**| 0 physical samples in `data/raw/` (Denominator: 0) |
| **Scale error** | **BENCHMARK_BLOCKED**| 0 physical calibration specimens (Denominator: 0) |
| **Font MAE** | **BENCHMARK_BLOCKED**| 0 physical vernier caliper ground-truth records (Denominator: 0) |
| **Physical dataset** | **BENCHMARK_BLOCKED**| 0 SKUs on disk (Target: 35 SKUs) |
| **Docker runtime** | **NOT_VERIFIED** | Docker CLI present; host daemon inactive (startup unmeasured) |
| **Offline static audit** | **PASS** | 0 external HTTP/CDN/cloud API calls in AST/grep audit |
| **Offline live drill** | **NOT_VERIFIED** | Disabling network adapters would sever remote agent session |
| **Demo failover** | **PASS** | 5-layer failover mechanism rehearsed and documented (`docs/DEMO_PLAN.md`) |

---

## 3. Synthetic OCR CER Forensic Investigation

### Reported Aggregate Metric
- **Synthetic Aggregate CER:** `1.1961` ($119.61\%$)
- **Total Reference Characters:** 459 characters
- **Total Levenshtein Edit Distance:** 549 edits
- **Specimens Evaluated:** 7 evaluated, 1 excluded (`SYNTH-07-BLANK-FRAME` has no text)

### Per-Sample CER Breakdown

| Sample ID | Detected Tokens (`PRED`) | Documented Reference (`REF`) | Ref Chars | Pred Chars | Edit Distance | Sample CER | Diagnosis |
|---|---|---|:---:|:---:|:---:|:---:|---|
| `SYNTH-01-ENG-FMCG` | `"SYNTHETICTESTNOTREALPACKAGG MRP Rs.20 incusive o al aes Net Qty: 65 g Unit Sale Price: Rs. 0.31 / g Mfg Date: 08/2026 Consume Cae oo zsad caeobseain"` | `"mrp: 20.00 net_quantity: 65 g usp: 0.31 / g date: 08/2026 contact: 1800-222-4444"` | 80 | 148 | 103 | **1.2875** | Length asymmetry + JSON key mismatch + watermark insertion |
| `SYNTH-02-HIN-FMCG` | `"SYNTHETICTESTNOTREALPACKAGNG : 245.00 निवलमात्राःजकिग्रा : 05/2026 00000:care@ata.in"` | `"mrp: 245.00 net_quantity: 5 किग्रा date: 05/2026 contact: care@atta.in"` | 70 | 84 | 58 | **0.8286** | Devanagari numerals detected, partial Hindi label segmentation |
| `SYNTH-03-MIXED-BILINGUAL` | `"SYNTHETICTESTNOTREALPACKAGG MRPI3eकत 7द! Hu. RS. 500 Net Qty /fa HaRT: 150 g USP: Rs. 0.33 per g Best Before: 12/2026 CustomerCaresuppo@nack.com"` | `"mrp: 50.00 net_quantity: 150 g usp: 0.33 per g date: 12/2026 contact: support@snack.com"` | 87 | 144 | 91 | **1.0460** | OCR noise on dense bilingual font + watermark insertion |
| `SYNTH-04-MICRO-FONT` | `"SYTHETICTESTNOTREALPACKAGG MRPRs.10.00incl.ofall axes Net Weight: 35g Unit Sale Price: Rs. 0.28/g Mfg: 07/2026"` | `"mrp: 10.00 net_quantity: 35g usp: 0.28/g date: 07/2026"` | 54 | 110 | 77 | **1.4259** | Numerals extracted correctly (`10.00`, `35g`, `0.28/g`, `07/2026`), but reference length is short |
| `SYNTH-05-LIQUID-VOLUME` | `"SYNTHETICTESTNOTREALPACKAGG MaximumRetailPrice R1200 Net Volume: 250 ml Unit Sale Price: Rs. 0.50/ml Expiry: 04/2028 Batch B-902 Helpline: 1800-100-9999"` | `"mrp: 125.00 net_quantity: 250 ml usp: 0.50/ml date: 04/2028 contact: 1800-100-9999"` | 82 | 152 | 101 | **1.2317** | OCR extracted extra batch/helpline text absent in reference |
| `SYNTH-06-PROHIBITED-UNITS` | `"SYNTHETICTESTNOTREALPACKAGNG MRPR85-(inclusivealltax) Net Wt: 500 Gms Vol: 1000 ML Mfg: 01/2026"` | `"mrp: 85 net_quantity: 500 Gms date: 01/2026"` | 43 | 95 | 69 | **1.6047** | Pred has 95 chars, ref has 43 chars (insertion penalty drives CER > 100%) |
| `SYNTH-07-BLANK-FRAME` | `""` | `""` | 0 | 0 | 0 | **`null`** | Excluded from denominator (no text on blank image) |
| `SYNTH-08-LOW-CONTRAST-FADED` | `"SYNTHETICTESTNOTREALPACKAGNG MRP Rs. 30.00 NET: 40 g EXP 11/2026"` | `"mrp: 30.00 net_quantity: 40 g date: 11/2026"` | 43 | 64 | 50 | **1.1628** | Short reference, watermark insertion penalty |

### Root Cause Determination
The high synthetic CER ($1.1961$ / $119.61\%$) is primarily **Category B (Benchmark Implementation Defect)** combined with **Category D (Normalization Mismatch)** and **Category C (Synthetic Fixture Suitability Problem)**:
1. **Semantic Ground Truth vs. Verbatim Optical Ground Truth:** `data/synthetic/regression/manifest.json` was created as an evaluation target for Member 3's regex rules engine. Its `ground_truth` entries are semantic key-value pairs (e.g. `{"mrp": "20.00"}`), NOT an exhaustive transcription of all glyphs on the image.
2. **Artificial Reference String Construction:** The benchmark harness concatenated dictionary keys (`f"{k}: {v}"`), inserting artificial words (`"net_quantity:"`, `"usp:"`, `"contact:"`) that do not exist on the image.
3. **Unpaired Text Elements:** The test images contain legal boilerplate (`"inclusive of all taxes"`) and a synthetic disclaimer banner (`"SYNTHETIC TEST NOT REAL PACKAGING"`), generating ~28 extra characters per specimen.
4. **Length Asymmetry:** Because $CER = \frac{\text{Levenshtein}(pred, ref)}{\text{len}(ref)}$, when $pred$ contains 148 characters and $ref$ is only 80 characters, insertion edits push the edit distance (103) past the reference length, producing $CER > 100\%$.
5. **Release Rule Enforcement:** This is honestly reported as **POOR / DEFECTIVE SYNTHETIC CER**. Under no circumstances is this synthetic metric used to claim physical packaging OCR accuracy.

---

## 4. Docker Runtime Verification Status

- **Status:** **`NOT_VERIFIED`**
- **Findings:**
  - Docker CLI v29.7.2 and Docker Compose v5.4.0 are installed on the host.
  - The Docker Desktop Linux engine service was inactive (`failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`).
  - Container build time, cold startup time, memory footprint, and `/health` HTTP 200 latency were **NOT MEASURED** on this host.
  - Dockerfiles have been hardened with non-root runtime `appuser:10001`, multi-stage builds, and health probes, but live container boot is classified strictly as **`NOT_VERIFIED`**.

---

## 5. Offline Operation Status

- **Static Dependency Audit:** **`PASS`**
  - Zero external CDN scripts, remote fonts, or third-party telemetry in Next.js build.
  - PaddleOCR ONNX models (detection, Latin recognition, Devanagari recognition) reside 100% locally on disk (`models/weights/ocr/`).
  - Inspection pipeline conductor (`POST /api/v1/inspect`) makes zero outbound network requests.
- **Live Network-Disabled Drill:** **`NOT_VERIFIED`**
  - In this cloud/agent execution environment, disabling all network adapters would terminate the remote management connection.
  - While code inspection proves zero network calls, the physical disconnected drill is honestly reported as **`NOT_VERIFIED`**.

---

## 6. Physical Metrology Benchmark Status

- **Status:** **`BENCHMARK_BLOCKED`**
- **Justification:**
  - Canonical target: 35 authentic retail SKUs (25 dev / 10 holdout).
  - `data/raw/` contains **0 physical packaging files**.
  - `data/manifests/real_packaging_manifest.json` explicitly states `disk_images_present: 0`.
  - Only 1 physical specimen exists (`data/real_world/dairy_milk_bubbly/`), but calibrated dual-rater vernier caliper ground-truth measurements and 1200 DPI optical comparator scans are not on disk.
  - Optical scale error, physical font height MAE, and real SKU compliance accuracy remain gated as `BENCHMARK_BLOCKED`.

---

## 7. Security Regression Status

- **Status:** **`PASS`** (11 / 11 tests passed).
- **Enforced Defenses:**
  - Decompression bomb safety cap (> 64 MP rejected).
  - Minimum resolution threshold (< 800x600 rejected).
  - Empty and corrupt byte stream validation.
  - Path traversal and null-byte filename sanitization.
  - API rate limiting (10 req/min).

---

## 8. Commit & Push Audit

- `HEAD_BEFORE_MEMBER_6`: `a06872f`
- `HEAD_AFTER_MEMBER_6`: `a06872f`
- `NEW_COMMIT_CREATED`: `NO`
- `PUSH_PERFORMED`: `NO`
- All Member 6 assets (CI workflow, benchmark suite, security tests, hardened Dockerfiles, documentation) remain in the working tree for team review.

---

## 9. Final Release Recommendation

**VERDICT: APPROVED FOR CONTROLLED SIH DEMONSTRATION.**  
The software integration, regression suites, and 5-layer failover mechanisms are verified. Physical metrological claims remain strictly and honestly declared as `BENCHMARK_BLOCKED`, while Docker runtime execution and live network-disabled execution are declared `NOT_VERIFIED`.
