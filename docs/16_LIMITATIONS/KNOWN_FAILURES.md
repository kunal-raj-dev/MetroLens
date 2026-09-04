# Known Failures & Controlled Refusal Register

## Purpose
Catalogues explicit scenarios where Nirikshak deliberately refuses to provide an automated decision, routing instead to human officer intervention.

## Core Refusal Principles
Refusing to decide under high uncertainty is an engineering safeguard, not a flaw. Nirikshak chooses `REVIEW` over false certainty.

---

## Controlled Refusal Registry

| Refusal ID | Trigger Condition | System Behavior | Rationale |
| :--- | :--- | :--- | :--- |
| **REF-01** | Missing Physical Calibration Target | Sets calibration status to `UNCALIBRATED`; flags all font height and area rules as `REVIEW`. | Prevents ungrounded pixel-to-mm conversions from creating spurious legal notices. |
| **REF-02** | Specular Glare on Mandatory Fields | Quality gate rejects frame; prompts `REQUEST_RETAKE`. | Prevents OCR from guessing obscured letters or numbers. |
| **REF-03** | Conflicting Cross-Panel Declarations | Emits `CROSS_PANEL_CONTRADICTION` alert; routes dossier to `REVIEW`. | Resolving whether front or rear panel declaration is genuine requires human investigation. |
| **REF-04** | Borderline Measurement Interval | Measurement uncertainty $[H - \sigma, H + \sigma]$ crosses threshold; routes to `REVIEW`. | Prevents false penalization when measurement error exceeds margin of violation. |
| **REF-05** | Unverified Regulatory Rule | Machine rule marked `PRIMARY_SOURCE_REQUIRED`; blocks automated pass/fail. | Prevents enforcement based on unauthenticated legal assumptions. |
