# MASTER CHECKLIST & GATE SIGN-OFF LEDGER
# MetroLens AI™ (SIH26034)
### Evaluation: Smart India Hackathon 2026 | Sponsoring Ministry: Ministry of Consumer Affairs
**Document Status:** Master Governance & Release Checklist | **Version:** 1.0.0

---

## 1. Daily Gate Sign-Off Ledger

| Gate | Target Milestone | Accountable Lead | Status | Sign-Off Criteria |
| :---: | :--- | :---: | :---: | :--- |
| **GATE 0** | **Hour 0: Planning & Ownership Freeze** | Lead Architect (M1/M6) | **SIGNED OFF** | All 6 members assigned single outcome; non-goals documented; `docs/team/` approved. |
| **GATE 1** | **T+24h: Proof of Core Risky Assumptions** | All Members | PENDING | PaddleOCR ONNX CPU $<1200\text{ms}$ (M1); Coin scale error $<5\%$ (M2); Schemas frozen (M3); Upload security passes (M4). |
| **GATE 2** | **T+48h: Vertical Slice 0 (The Kill-Switch)** | M1, M2, M3, M4 | PENDING | Headless CLI executes Ingestion $\rightarrow$ Calib $\rightarrow$ OCR $\rightarrow$ Normalizer $\rightarrow$ Rules $\rightarrow$ JSON in $<2.5\text{s}$. |
| **GATE 3** | **Day 3: Core Subsystems Functional** | M1, M3, M4, M5 | PENDING | Devanagari Hindi parsed; Rule 6 & 26 state machine passing; PDF template rendering; UI bounding boxes scaling. |
| **GATE 4** | **Day 4: End-to-End Web Integration** | M4, M5 | PENDING | React upload dropzone calls live FastAPI endpoint; renders 5-State cards in browser in $<2.5\text{s}$. |
| **GATE 5** | **Day 5: Feature-Complete MVP** | All Members | PENDING | Upload $\rightarrow$ Audit $\rightarrow$ Crop Zoom $\rightarrow$ PDF Report download functional end-to-end; 35 SKUs scanned. |
| **GATE 6** | **Day 6: Benchmark Results Locked** | M6, M1, M2 | PENDING | 35-SKU empirical benchmark executed on real hardware; CER $<6.0\%$, Font MAE $<0.15\text{mm}$ recorded in `benchmarks/results/`. |
| **GATE 7** | **Day 7: Demo Hardened & 5-Layer Failover Drill** | M6, Presenter | PENDING | Full demo executes on localhost with OS Wi-Fi toggled OFF; backup sample dropdown and 4K USB video verified. |
| **GATE 8** | **Day 8: Absolute Code & Presentation Freeze** | Lead Architect (M1/M6) | PENDING | Git `main` branch locked; zero active development; slides finalized; physical props kit packed. |
| **GATE 9** | **Day 9: Hackathon Stage Presentation** | Entire Team | PENDING | Live 3-minute pitch executed on hackathon stage; physical vernier caliper placed on jury table. |

---

## 2. Final Release & Submission Checklist

Before final submission to the Smart India Hackathon jury, the team must complete every item:

### A. Software & Build Verification
- [ ] Docker container builds clean without warnings: `docker-compose build`.
- [ ] Container boots in $< 10\text{s}$ and health check returns `HTTP 200 OK`: `curl http://127.0.0.1:8000/api/v1/health`.
- [ ] Zero external cloud AI API keys in codebase (no OpenAI, Claude, or Gemini dependencies).
- [ ] Zero unhandled 500 errors on invalid image uploads (magic-byte check rejects corrupted files).
- [ ] All automated unit, rule, and integration tests pass: `python -m pytest tests/`.

### B. Accuracy & Empirical Proof
- [ ] Benchmark dataset of 35 physical SKUs documented in `data/ground_truth/`.
- [ ] Dual-rater flatbed optical scans (1200 DPI) verified with inter-rater variance $< 0.04\text{mm}$.
- [ ] Automated benchmark harness executed on host hardware: `python -m pytest tests/benchmarks/`.
- [ ] Measured Character Error Rate (CER) $< 6.0\%$ documented in `benchmarks/results/summary.json`.
- [ ] Measured Numeral Height MAE $< 0.15\text{mm}$ documented in `benchmarks/results/summary.json`.
- [ ] Zero fabricated or staged benchmark numbers anywhere in presentation slides.

### C. Legal & Evidentiary Integrity
- [ ] 100% pass on 25 statutory rule test cases in `tests/rules/`.
- [ ] Zero LLM prompts in legal adjudication pipeline (pure deterministic Python state machine).
- [ ] Report correctly cites Section 36(1) Improvement Notice under *Jan Vishwas Act, 2026*.
- [ ] Report embeds authentic cryptographic SHA-256 hash of raw input image and crops.
- [ ] All synthetic defect packaging specimens clearly labeled: *"Synthetic Test Specimen — Not an Actual Manufacturer Violation"*.

### D. Live Demo Props & Failover Redundancy
- [ ] Physical Defective Benchmark Specimen (Net Qty printed at 1.15mm) packed in demo kit.
- [ ] Physical Compliant Retail Package (Dettol / Colgate) packed in demo kit.
- [ ] Crisp, uncirculated RBI standard 10-Rupee coin ($27.0\text{mm}$) + ISO ATM card packed.
- [ ] Physical digital vernier caliper ($0.01\text{mm}$ precision) cleaned and tested with fresh battery.
- [ ] Demonstrator laptop runs entire demo on `127.0.0.1:8000` with OS Wi-Fi switched OFF.
- [ ] Layer 2 failover: "Load Sample Package" dropdown verified in web UI navigation bar.
- [ ] Layer 5 failover: 4K uncut backup demonstration video copied to smartphone and USB thumb drive.
- [ ] Presenter rehearsed full 3-minute spoken script with second-by-second timing.
