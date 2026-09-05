# Principal Display Panel (PDP) Detection & Area Calculation

## Purpose
Specifies the computer vision segmentation models and geometric area calculation formulas used to determine the boundary and physical area ($A_{\text{PDP}}$) of the Principal Display Panel.

## Scope
Covers rectangular boxes, cartons, cylinders, bottles, and stand-up pouches.

## Authoritative Inputs
- Legal Metrology (Packaged Commodities) Rules, 2011 (Rule 7 and Explanations).

## Assumptions
- Principal Display Panel is defined as the primary display facet presented to the consumer under standard retail display conditions.

## Open Questions
- Automatic identification of the primary facet on multi-lingual symmetric packaging (e.g. English front vs. Hindi back) [TBD — MEASURE].

## Dependencies
- `packages/vision/`
- `packages/calibration/`

## Verification Requirements
- PDP area calculations must match physical manual caliper measurements within $\le \pm 5\%$ tolerance on calibrated targets.

---

## Statutory Area Calculation Formulas (Rule 7)

```
┌────────────────────────────────────────────────────────┐
│ PACKAGE GEOMETRY          │ STATUTORY PDP AREA FORMULA │
├───────────────────────────┼────────────────────────────┤
│ Rectangular Carton / Box  │ A_pdp = Height × Width     │
│                           │ (Area of front face)       │
├───────────────────────────┼────────────────────────────┤
│ Cylindrical Can / Bottle  │ A_pdp = 0.40 × (H × C)     │
│                           │ (40% of height × circumf.) │
├───────────────────────────┼────────────────────────────┤
│ Triangular / Any Other    │ A_pdp = 0.20 × Total Area  │
│ Shape                     │ (or major presented facet) │
└───────────────────────────┴────────────────────────────┘
```

### Detection Pipeline:
1. **Contour Extraction & Edge Fitting:** Detect outer boundary of the package container using Canny edge detection or instance segmentation mask.
2. **Perspective Rectification:** Calculate homography matrix $H$ to rectify package face to orthogonal frontal perspective.
3. **Physical Scaling:** Multiply pixel dimensions by scale factor $S$ ($\text{mm/px}$) to compute physical $H_{\text{cm}}$ and $W_{\text{cm}}$.
4. **Statutory Classification:** Map computed $A_{\text{PDP}}$ (in $\text{cm}^2$) to Table-I area bracket to establish required minimum font heights.
