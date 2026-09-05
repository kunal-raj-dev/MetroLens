# Competitive Claims & Differentiation Register

## Purpose
Governs all comparative claims against existing commercial packaging QA systems, generic OCR mobile apps, and government inspection procedures.

## Core Mandate
> [!IMPORTANT]
> In the reviewed systems listed in `docs/12_PRIOR_ART/PRIOR_ART_REGISTER.md`, we did not identify solutions combining physical scale calibration, multi-panel 3D packaging correlation, and multi-epoch statutory versioning for Indian Legal Metrology.
> Absolute blanket claims (e.g. "no solution exists worldwide") are strictly prohibited. Comparative assertions are limited to systems specifically evaluated in `docs/12_PRIOR_ART/PRIOR_ART_REGISTER.md`.

---

## Controlled Competitive Assertions

| Dimension | Generic OCR / Scanner Apps | Enterprise Packaging QA (Pre-Print) | Nirikshak System Architecture | Status | verified_date | last_reviewed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Physical Font Measurement** | Not observed (Pixels only) | N/A (Digital vector analysis) | Physical reference calibration + optical measurement in mm | EXPERIMENT_REQUIRED | null | 2026-09-04 |
| **Multi-Panel Cross-Check** | Not observed (Single view) | Single artwork file | Correlates MRP, Net Qty, and Address across distinct 3D faces | EXPERIMENT_REQUIRED | null | 2026-09-04 |
| **Regulatory Versioning** | Not observed | Static guidelines | Regulatory snapshot based on package manufacture date | EXPERIMENT_REQUIRED | null | 2026-09-04 |
| **Failure Mode Handling** | Unbounded guesses | Rejection in pre-press | Routing to REVIEW / REQUEST_RETAKE on blur or uncalibrated scale | EXPERIMENT_REQUIRED | null | 2026-09-04 |
| **Tamper Evidence** | Plain export | Proprietary log | SHA-256 evidence chain linking raw crop to rule verdict | EXPERIMENT_REQUIRED | null | 2026-09-04 |

*Note: "Not observed" denotes that this capability was not identified in the technical documentation or public evaluation of the systems reviewed in `docs/12_PRIOR_ART/PRIOR_ART_REGISTER.md`.*
