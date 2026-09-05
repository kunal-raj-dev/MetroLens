# Adversarial Test Suite Specification

## Purpose
Defines adversarial scenarios, deceptive packaging samples, optical distortions, and attack payloads used to stress-test system robustness and anti-hallucination guardrails.

## Scope
Covers vision pipeline resilience, deceptive packaging detection, and input security.

## Authoritative Inputs
- Known real-world deceptive packaging patterns identified in Legal Metrology enforcement reports.

## Assumptions
- The system must fail safely to `REVIEW` or `REQUEST_RETAKE` when confronted with adversarial manipulations.

## Open Questions
- Generating synthetic micro-printed text near optical sensor Nyquist limits [TBD — MEASURE].

## Dependencies
- `tests/fixtures/`

## Verification Requirements
- Adversarial tests must confirm zero false passes on deceptive samples.

---

## Adversarial Scenarios

1. **Adversarial Test ADV-01: Micro-Font / Camouflaged Text**
   - **Pattern:** Net quantity printed in light gray text on low-contrast patterned background, font height $0.85\text{ mm}$ (statutory requirement $2.0\text{ mm}$).
   - **Expected Outcome:** Text detection identifies low contrast; measurement evaluates to `FAIL` with visual contrast warning.

2. **Adversarial Test ADV-02: Glare-Masked Expiry / Net Qty**
   - **Pattern:** High-intensity flash reflection occluding the month and year of packing.
   - **Expected Outcome:** Image quality gate triggers `REQUEST_RETAKE` prior to OCR inference.

3. **Adversarial Test ADV-03: Dual MRP Tampering**
   - **Pattern:** Original MRP (Rs. 80.00) obscured by a secondary price sticker (Rs. 110.00) without statutory authorized alteration markings.
   - **Expected Outcome:** Text detection locates two conflicting MRP price tokens; triggers `CROSS_PANEL_CONTRADICTION` and routes to `REVIEW`.

4. **Adversarial Test ADV-04: False Calibration Marker**
   - **Pattern:** Non-standard circular coin or distorted circular logo introduced instead of calibrated target.
   - **Expected Outcome:** Target detector fails circularity or aspect-ratio test; rejects marker and falls back to `UNCALIBRATED` mode (verdict: `REVIEW`).
