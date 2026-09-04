# Failure Modes & Effects Analysis (FMEA)

## Purpose
Catalogues potential system failure modes, root causes, severity ratings, detection mechanisms, and defensive architectural fallbacks.

## Scope
Universal across optics, OCR, calibration, rules engine, and reporting.

## Authoritative Inputs
- Standard FMEA engineering methodology.
- Anti-Hallucination Policy.

## Assumptions
- Failure to recognize a defect must never lead to a false positive statutory violation notice.

## Open Questions
- None.

## Dependencies
- `docs/16_LIMITATIONS/KNOWN_FAILURES.md`

## Verification Requirements
- All high-RPI (Risk Priority Index) failure modes must have validated architectural fallbacks.

---

## FMEA Matrix

| Failure Mode | Root Cause | Severity (1-10) | Likelihood (1-10) | Detection (1-10) | Mitigation / Fallback Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **False Negative on Small Font** | High optical blur obscures tiny 1 mm numeral | 8 | 5 | 3 | Laplacian blur quality gate rejects frame before inference. |
| **Hallucinated Mandatory Field** | OCR misinterprets marketing slogan as generic name | 7 | 4 | 4 | Strict regex keyword grammar + confidence threshold $\ge 0.85$. |
| **Erroneous Physical Scale** | Reference marker tilted at steep perspective angle | 9 | 4 | 3 | Ellipse eccentricity check rejects markers tilted $> 20^\circ$. |
| **Incorrect Rule Application** | Manufacturing date misparsed leading to wrong epoch | 8 | 3 | 4 | Officer confirmation screen prompts explicit date verification. |
| **Database Tampering** | Local file manipulation on compromised device | 9 | 2 | 2 | SHA-256 hash chaining detects broken integrity on sync. |
