# AI CONTEXT: PROJECT CONTEXT & ARCHITECTURAL INVARIANTS
**Project:** MetroLens AI™ / MetroSetu (SIH26034)  
**Sponsoring Ministry:** Ministry of Consumer Affairs, Food & Public Distribution (Government of India)  
**Master Reference:** `ALL-IN-ONE context/METROLENS_AI_ALL_IN_ONE_DOCS.md`  
**Current Phase:** Member 1 Final Implementation + Forensic Audit + Freeze Complete (M1 Release Candidate Certified)


---

## 1. Core Mission & Problem Statement
Automate statutory compliance assessment for pre-packaged commodities under the *Legal Metrology (Packaged Commodities) Rules, 2011* (PCR 2011) and the *Legal Metrology Act, 2009* (incorporating the *Jan Vishwas (Amendment of Provisions) Act, 2026* statutory revisions).
- **Enforcement Blind Spot:** Over ₹12 Lakh Crore ($150B) in retail goods across 780+ districts with fewer than 2,500 inspecting officers ($<0.01\%$ inspected).
- **Core Violations Audited:** Missing/deceptive Unit Sale Price (USP) under Rule 6(11), microscopic numeral heights under Rule 7 Tables I/II, missing statutory declarations under Rule 6(1), and non-standard imperial units.
- **Jan Vishwas 2026 Shift:** First offenses under Section 36(1) transition to administrative **Improvement Notices** requiring indisputable, objective visual and mathematical evidence dossiers.

---

## 2. Inviolable Architectural Principles
1. **Zero Cloud AI in Legal Adjudication:** No external generative LLMs (OpenAI, Anthropic, Gemini) may ever be used to determine legal compliance. All compliance decisions are 100% deterministic Python state machines codifying Gazette clauses.
2. **Local CPU Execution (ADR-001, ADR-017):** All computer vision (DBNet++) and scene text OCR (SVTR) neural models execute locally on consumer server/laptop CPUs via ONNX Runtime without discrete GPU reliance.
3. **Synchronous Sub-2.5s Budget (ADR-012):** The inspection pipeline completes in $< 2.5\text{s}$ wall-clock time on standard CPU hardware from image upload to compliance dossier rendering.
4. **Separation of Perception from Law:**
   $$\text{AI Perceives (OCR)} \longrightarrow \text{Math Validates (Scale/USP)} \longrightarrow \text{Rules Decide (Gazette Law)} \longrightarrow \text{Humans Govern (Section 15)}$$
5. **Data Minimization & Ephemeral Storage (ADR-014):** Ingestion security gate (magic bytes, 64MP decompression bomb cap, EXIF strip). Images spooled to temporary storage with a 60-minute TTL strictly for PDF download, then purged. Zero permanent unauthenticated image retention.
6. **Delivery Model vs Engine Philosophy (ADR-011):** Web-first delivery model (responsive React/Next.js client + FastAPI backend) decoupled from pure, offline-capable Python calculation packages.

---

## 3. Verified Empirical Baseline (Chunk 2 & 3 Reconciled)
Empirically measured on host hardware (AMD Ryzen 8C/16T, 15.31 GB RAM, Windows 11 CPU-only):
- **Selected Engine:** `PP-OCRv3-ROUTED` (DBNet++ shared det + script-routed SVTR-EN / SVTR-HI ONNX via direct `onnxruntime==1.29.0`).
- **Total Weights Size:** 22.10 MB (DBNet++ det: 2.43 MB, SVTR-EN rec: 10.69 MB, SVTR-HI rec: 8.98 MB + `dict.txt`).
- **Cold Load Latency:** 283.66 ms.
- **Warm Latency (Median):** ~90 - 107 ms (4 CPU intra-op threads).
- **Peak Process RSS:** ~101 MB (well below the 400 MB server worker budget).
- **Domain Preprocessing:** Adaptive Crop Preprocessing (`P_ADAPTIVE_CROP`) preserves clean packaging and boosts low-contrast text with zero coordinate distortion.
- **Devanagari Support:** Local SVTR Hindi session with Devanagari dictionary.
- **Licensing:** Apache-2.0 across all models and inference runners.

---

## 4. Monorepo Organization & Team Ownership
- `packages/shared`: Frozen API schemas, Pydantic domain models, data contracts (All Members).
- `packages/ocr`: Direct ONNX Runtime `PP-OCRv3-ROUTED` engine, Devanagari SVTR session, adaptive crop preprocessing, token parser (Member 1).
- `packages/calibration`: Reference scale recovery (27.0mm coin / ISO card), PPM conversion, $h_{\text{mm}}$ measurement (Member 2).
- `packages/vision`: Ingestion quality gates, blur/glare filters, PDP area segmentation, cylinder generator strip (Member 2).
- `packages/rules`: Deterministic statutory state machine for Rules 6, 7, 8, 9, 11, 26 and Jan Vishwas 2026 (Member 3).
- `packages/reporting`: Cryptographic SHA-256 evidence chain, PDF report generation, Improvement Notice generator (Member 4).
- `apps/api`: FastAPI REST gateway (`/api/v1/inspect`, `/api/v1/reports`, `/api/v1/calibration`, `/api/v1/emaap/mock-sync`) (Member 4).
- `apps/web`: Next.js / Tailwind CSS responsive inspector interface & evidence viewer (Member 5).
- `apps/worker`: Celery / Redis background worker service for bulk audits (Member 4).
- `infra/postgres`: PostgreSQL database schema initialization (Member 4).
- `tests/` & `benchmarks/`: 35-SKU ground truth test suite, calibration verification, regression harness (Member 6).

---

## 5. Master Specification Reference
For complete exhaustive specifications, cross-cutting contracts, and all 17 ADRs, refer to:
`ALL-IN-ONE context/METROLENS_AI_ALL_IN_ONE_DOCS.md`
