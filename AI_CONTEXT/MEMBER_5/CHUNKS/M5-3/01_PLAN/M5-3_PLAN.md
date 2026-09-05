# ARCHITECTURAL PLAN: CHUNK M5-3
**Subsystem:** Member 5 — Web Frontend & Officer Workstation  
**Chunk:** M5-3: Compliance Dashboard + Evidence Canvas + Evidence Interaction  
**Date:** 2026-09-05T17:50:45+05:30  

---

## 1. Objectives & Scope
- Transform the raw inspection results from Chunk M5-2 into an interactive evidence exploration workspace.
- Build a dedicated `ComplianceDashboard` communicating the backend verdict, quality metrics, physical calibration factor, and telemetry through multi-modal status indicators.
- Build an HTML5 `EvidenceCanvas` that renders the original package photograph and overlays Member 1's unnormalized OCR polygons in image pixel space.
- Implement an affine transform system (`scale`, `panX`, `panY`) with cursor-anchored zoom, pan, fit-to-screen, and reset controls.
- Implement inverse hit-testing (`screen -> canvas -> image space`) with point-in-polygon ray casting to support token selection on click.
- Build an accessible synchronized DOM evidence panel so keyboard and screen reader users have complete access to evidence text, confidence scores, and script information outside the canvas.
- Display transparent synthetic disclaimers for all demo fixtures and prohibit silent fallbacks on live API failures.

## 2. Inviolable Invariants
- Member 1's OCR coordinates remain in original image pixel space (origin top-left).
- Zero legal rule engine logic or font height calculations in React.
- Zero local neural network inference models in web client.
- Zero git commits or pushes.
