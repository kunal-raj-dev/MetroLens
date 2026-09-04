# Image Verifiability Matrix

| Legal Check | Verifiability | Why | Failure Mode | Manual Review Condition | Applicable Source |
|---|---|---|---|---|---|
| Net Weight | NOT IMAGE-VERIFIABLE | Requires physical scale | - | - | Section 27 |
| Declared Net Qty | FULLY IMAGE-VERIFIABLE | Printed text is visible | Blur/Glare | OCR Confidence < 85% | Rule 6(1)(c) |
| Declared USP | FULLY IMAGE-VERIFIABLE | Printed text is visible | OCR failure | Missing field | Rule 6(11) |
| USP Computation | FULLY IMAGE-VERIFIABLE | Derived math from visible fields | OCR failure on MRP/Qty | Missing denominator | Rule 6(11) |
| Font Height | PARTIALLY IMAGE-VERIFIABLE | Camera distortion, lack of physical scale | Perspective warp | Value in Engineering Band | Rule 7(4) |
| Package Category | REQUIRES EXTERNAL DATA | Visual ID is subjective | Ambiguous product | Cannot determine if institutional | Rule 3 |
