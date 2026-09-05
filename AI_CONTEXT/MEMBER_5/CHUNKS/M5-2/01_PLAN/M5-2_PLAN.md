# ARCHITECTURAL PLAN: CHUNK M5-2
**Subsystem:** Member 5 — Web Frontend & Officer Workstation  
**Chunk:** M5-2: Image Upload + Inspection Client + Mock/Live Adapter  
**Date:** 2026-09-05T17:35:15+05:30  

---

## 1. Objectives & Scope
- Deliver a production-grade packaging image ingestion experience designed for enforcement officers under the Mastercard design language (warm stone/cream canvas, 40px stadium cards, 20px pill buttons, satellite micro-CTAs).
- Build defensive client-side validation (15 MiB ceiling, format sniffing, browser raster decoding) before sending data over the wire.
- Implement an adapter-based inspection client (`IInspectionClient`), cleanly isolating the UI from network transport details.
- Provide a deterministic `MockInspectionAdapter` backed by synthetic regression assets (`SYNTH-01` to `SYNTH-08`).
- Provide a robust `LiveInspectionAdapter` targeting `POST /api/v1/inspect`.
- Build a defensive response normalizer that maps `BackendInspectionDTO` into `FrontendInspectionModel`.
- Support memory-leak-free Object URL lifecycle management.
- Provide comprehensive tests and automated browser verification.

## 2. Inviolable Invariants
- Zero client-side legal metrology decisions (Rule 6, Rule 7, USP arithmetic belong to backend M3/M4).
- Zero OCR inference models in the frontend (M1 coordinates in raw image pixel space).
- Zero fetch calls inside React components.
- Zero git commits or pushes.
