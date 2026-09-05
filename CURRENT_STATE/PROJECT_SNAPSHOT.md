# CURRENT STATE: PROJECT SNAPSHOT
**Project:** MetroLens AI™ / MetroSetu (SIH26034)  
**Snapshot Date:** 2026-09-05T05:36:00+05:30  
**Phase:** Chunk 4 Completed — OCR Monorepo Integration, Service Adapter & Contract Verification Active  
**Governing Architecture:** Online Web Application MVP (ADR-011 through ADR-017)  

## 1. High-Level Status
- **Legal Source Base:** 74 authentic government legal documents cataloged and verified under `METROLENS_LEGAL_SOURCE_PACK/`.
- **Legal Rule Matrix:** PCR 2011 (Rules 6, 6(11), 7, 8, 9, 26) and Jan Vishwas Act 2026 Section 36(1) codified in documentation.
- **System Architecture:** Decoupled Web Delivery (React/Next.js + FastAPI) from Deterministic Processing Engine (Local CPU execution, zero cloud AI APIs, zero Celery/Redis).
- **OCR Subsystem Status:** **INTEGRATED, ADAPTER-WRAPPED & CONTRACT-VERIFIED (Chunk 4)**.
  - Production-ready Direct ONNX Runtime engine (`PP-OCRv3-ROUTED`) packaged as `nirikshak-ocr` via pip editable install.
  - High-level production service adapter: `nirikshak_ocr.OCRService`.
  - Canonical Default Baseline: `B0_BASELINE_RAW` (`preprocessing_mode="raw"`), median latency 109.64 ms, adapter overhead 3.04 ms.
  - Provisional Experimental Candidate: `P_ADAPTIVE_CROP` (`preprocessing_mode="adaptive"`).
  - Multi-threaded Concurrency: 8.81 req/sec throughput under 4 worker threads; serialized engine lock ensures zero race conditions.
  - Memory Profile: 71.11 MB start $\rightarrow$ 150.17 MB warm $\rightarrow$ 296.85 MB peak concurrency (comfortably under 400 MB budget).
  - Standardized Contracts: Transforms output directly to `nirikshak_shared.schemas.OCRObservation`.
  - Geometric Integrity: 4-point clockwise quadrilateral polygon coordinates in original image pixel space.
  - Multilingual Unicode: Devanagari Hindi text and Indian Rupee symbol (`₹`) survive in-memory serialization and JSON roundtrips.
  - 89 unit, integration, hardening, and offline isolation tests passing (100% repository pass rate).
- **Real-Data Status:** **PATH B ENFORCED (REAL DATA BLOCKED)**. Zero real images fabricated. Real-world validation remains formally blocked awaiting physical retail specimen collection by Member 6.
- **Application Code Status:** Monorepo package layout configured. `packages/ocr/` fully hardened and integrated; `packages/shared/` schemas aligned; `packages/calibration/`, `packages/rules/`, and `apps/api/` scaffolding active.
- **Team Workstreams:** 6 distinct outcome-based work plans defined in `docs/team/` (M1: OCR, M2: Calibration/Pre-flight, M3: Rules, M4: API/PDF, M5: Web UX, M6: QA/Release).

## 2. Immediate Active Objective
- Complete **Chunk 4 to Chunk 5 Handoff**.
- Execute **Chunk 5: Inspection Pipeline Orchestration, Route Mounting & Deployment Hardening**.
- Member 6 to deliver 35-SKU physical retail packaging dataset and ground-truth annotations under Path B protocol.
