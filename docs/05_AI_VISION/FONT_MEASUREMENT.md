# Font Height Measurement & Table-I Compliance

## Purpose

Specifies the optical measurement algorithms, baseline detection methods, x-height/cap-height estimations, and uncertainty calculations used to evaluate font heights in millimetres.

## Scope

Focuses on numerals and letters declaring Net Quantity, MRP, and statutory notices on the Principal Display Panel under Rule 7, Table-I.

## Authoritative Inputs

- Legal Metrology (Packaged Commodities) Rules, 2011 (Rule 7 and Table-I).

## Assumptions

- Font height in statutory metrology refers to the height of the numeral or uppercase letter, excluding descenders and ascenders.
- Measurement in physical millimetres requires an authenticated scale factor $S$ ($\text{mm/px}$) from the calibration subsystem.

## Open Questions

- Standardized handling of stylized brand typography where numerals have non-uniform vertical heights [TBD — MEASURE].

## Dependencies

- `packages/measurement/`
- `packages/calibration/`

## Verification Requirements

- Optical measurements must match physical optical comparator or vernier caliper measurements within $\le \pm 0.2\text{ mm}$ on calibrated ground truth targets.

---

## 1. Mathematical Measurement Formulation

Let $h_{\text{px}}$ be the vertical pixel height of a detected numeral character, and $S$ be the calibrated scale factor in $\text{mm/pixel}$.
The physical font height $H_{\text{font}}$ is given by:

$$
H_{\text{font}} = h_{\text{px}} \cdot S
$$

### Bounded Uncertainty Formulation:

Let $\sigma_{h}$ be the pixel edge localization uncertainty ($\approx \pm 1.0\text{ px}$), and $\sigma_{S}$ be the calibration scale uncertainty.
The combined measurement uncertainty $\sigma_{H}$ is:

$$
\sigma_{H} = \sqrt{ \left( S \cdot \sigma_h \right)^2 + \left( h_{\text{px}} \cdot \sigma_S \right)^2 }
$$

Reported physical measurement:

$$
H_{\text{reported}} = H_{\text{font}} \pm 2\sigma_H \quad (95\% \text{ confidence interval})
$$

---

## 2. Table-I Statutory Area vs. Minimum Height Brackets (Rule 7)

```
┌────────────────────────────────────────────────────────────────────────┐
│ Area of PDP (A_pdp in cm²) │ Min Height of Numerals / Letters (mm)     │
│                            ├─────────────────────┬─────────────────────┤
│                            │ Net Qty in Wt / Vol │ Other Declarations  │
├────────────────────────────┼─────────────────────┼─────────────────────┤
│ A_pdp ≤ 50                 │ 1.0 mm              │ 1.0 mm              │
├────────────────────────────┼─────────────────────┼─────────────────────┤
│ 50 < A_pdp ≤ 100           │ 1.5 mm              │ 1.0 mm              │
├────────────────────────────┼─────────────────────┼─────────────────────┤
│ 100 < A_pdp ≤ 500          │ 2.0 mm              │ 1.5 mm              │
├────────────────────────────┼─────────────────────┼─────────────────────┤
│ 500 < A_pdp ≤ 2500         │ 4.0 mm              │ 2.5 mm              │
├────────────────────────────┼─────────────────────┼─────────────────────┤
│ A_pdp > 2500               │ 6.0 mm              │ 3.0 mm              │
└────────────────────────────┴─────────────────────┴─────────────────────┘
```

### Deterministic Decision Rules:

1. **PASS:** If $(H_{\text{font}} - \sigma_H) \ge H_{\text{statutory\_min}}$.
2. **FAIL:** If $(H_{\text{font}} + \sigma_H) < H_{\text{statutory\_min}}$.
3. **REVIEW:** If the confidence interval $[H_{\text{font}} - \sigma_H, H_{\text{font}} + \sigma_H]$ spans across $H_{\text{statutory\_min}}$ (Borderline Measurement).
4. **REVIEW (Uncalibrated):** If $S$ is unavailable, $H_{\text{font}}$ cannot be computed. The system returns `REVIEW` and flags: *"Scale calibration missing; physical measurement required."*
