# Legal Uncertainty Policy

**Default Policy:** DO NOT GUESS. Escalate to MANUAL_REVIEW.

## 1. Rule Applicability
If the product category cannot be conclusively identified as a "retail package", mark applicability as `UNKNOWN_RULE_APPLICABILITY` and require manual review.

## 2. OCR Confidence
If OCR text extraction confidence is below the defined engineering threshold, the legal check is skipped and marked `INSUFFICIENT_INPUT` -> `MANUAL_REVIEW`.

## 3. Engineering Uncertainty Review Band (Measurement Buffer)
- **Legal Threshold:** Absolute (e.g., 1.5mm).
- **Measurement Uncertainty Review Band:** An engineering buffer (e.g., +/- 0.10mm) to account for camera calibration error.
- **Action:** If the measured font height falls within `1.40mm - 1.60mm`, the system MUST output `MANUAL_REVIEW`. Do not output `PASS` falsely. Do not output `FAIL` falsely.

## 4. Conflicting Declarations
If a sticker covers original text, or two MRPs are visible, output `MANUAL_REVIEW`.
