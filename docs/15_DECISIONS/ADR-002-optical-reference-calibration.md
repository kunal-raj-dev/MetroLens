# ADR-002: Optical Reference Calibration vs. Uncalibrated Pixel Heuristics

## Status
ACCEPTED

## Date
2026-09-04

## Deciders
Principal Software Architect, Computer Vision Lead, Metrology Lead

---

## Context & Problem Statement
Rule 9 and the Second Schedule of the Legal Metrology (Packaged Commodities) Rules, 2011 mandate minimum numeral and letter font heights in millimeters (e.g., 1.0 mm to 6.0 mm depending on Principal Display Panel area). Camera sensors capture packages in pixel dimensions, which vary wildly based on camera-to-package distance, focal length, perspective slant, and sensor resolution.

We must decide how to reliably convert pixel dimensions into certified physical millimeter dimensions.

---

## Decision Drivers
- **Metrological Integrity**: "Pixels are not millimeters." Arbitrary pixel heuristics or uncalibrated distance estimation cannot stand up in statutory inspection.
- **Bounded Measurement Uncertainty**: Any measurement presented to an inspector must carry an explicit uncertainty interval (e.g. $\pm 0.15\text{ mm}$).
- **Hardware Agnosticism**: Field officers use standard consumer smartphone cameras rather than calibrated laboratory optical benches.

---

## Considered Options
1. **Option 1: Optical Reference Marker Calibration** (Chosen)
   - Utilizing a known physical reference marker placed in the same focal plane (e.g., standard AruCo fiducial marker, standard Indian circulating coin, or certified calibration card).
2. **Option 2: Camera Monocular Depth Estimation / AI Distance Estimation**
   - Using neural depth prediction models (e.g. MiDaS/ZoeDepth).
3. **Option 3: Fixed Assumed Distance Heuristic**
   - Assuming the officer takes photos from exactly 30 cm distance.

---

## Decision Outcome
**Chosen Option:** Option 1: Optical Reference Marker Calibration.
A physical fiducial marker with known metric dimensions is detected in the image to derive a scale factor $S = \text{mm}/\text{pixel}$ and an associated optical uncertainty bound. When no marker is present, the measurement engine explicitly returns `UNCALIBRATED` status rather than making unverified guesses.

### Positive Consequences
- Mathematically defensible physical measurement conversion.
- Supports clear error bars and statutory compliance buffers.
- Prevents spurious font-height violation citations caused by camera distance variations.

### Negative Consequences / Trade-offs
- Requires the inspecting officer to include a reference marker in the frame for certified measurement.
- If the marker is missing or occluded, font-height checks are flagged as `UNCALIBRATED` and require manual physical ruler verification.

---

## References & Statutory Linkages
- Legal Metrology (Packaged Commodities) Rules, 2011, Rule 9 & First/Second Schedules.
- Legal Metrology (General) Rules, 2011 (Verification standards).
