# Data Dictionary & Schema Definitions

## Purpose
Establishes normalized field types, measurement units, coordinate systems, and nullability constraints for all internal data structures.

## Scope
Universal across database schemas, JSON schemas, OCR token pipelines, and report models.

## Authoritative Inputs
- `rules/schema/`

## Assumptions
- All physical lengths are in millimetres ($\text{mm}$), areas in square centimetres ($\text{cm}^2$), masses in grams ($\text{g}$), volumes in millilitres ($\text{ml}$), and currency in Indian Rupees ($\text{INR}$).

## Open Questions
- **OQ-SCHEMA-01 (Cylindrical Surface Coordinates):** How should multi-panel cylindrical unwraps represent bounding coordinates—as 2D projected unwrap coordinates $(u, v)$ or as 3D cylindrical surface coordinates $(\theta, h, r)$ in downstream inspection JSON?
- **OQ-SCHEMA-02 (Devanagari / Indic Script Numerals):** Standardization protocol for normalizing Indian script numerals (e.g. Devanagari ०, १, २... vs Hindu-Arabic 0, 1, 2...) in `net_quantity_declared` and `mrp_declared` without discarding raw OCR script tokens.
- **OQ-SCHEMA-03 (Dual-Unit Net Quantity Declarations):** Data structure definition for commodities declaring both unit count and net mass/volume (e.g. "100 N (500 g)" or "50 units of 10 ml") to prevent schema type validation failures.
- **OQ-SCHEMA-04 (Vernier Zero-Error Margin Tracking):** Inclusion of an explicit zero-error calibration margin field ($\Delta_{\text{cal}}$) and ambient temperature record in the physical ground-truth measurement schema (`data/benchmark/caliper_measurements.csv`).
- **OQ-SCHEMA-05 (Flexible Packaging Curvature Deformation):** Maximum allowable out-of-plane surface curvature variance threshold ($\sigma_{\text{depth}}^2$) before planar homography approximations must be aborted in favor of non-rigid thin-plate spline modeling.

## Dependencies
- `packages/shared/`

## Verification Requirements
- Database migrations and Pydantic models must conform strictly to these types.

---

## Field Specifications

| Field Name | Type | Unit | Nullable? | Description & Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `inspection_id` | UUIDv4 / String | — | No | Unique immutable identifier for inspection session. |
| `timestamp_utc` | ISO-8601 String | UTC | No | Standard timestamp: `YYYY-MM-DDTHH:MM:SSZ`. |
| `image_sha256` | Hex String (64) | — | No | SHA-256 cryptographic digest of raw image frame. |
| `pdp_area_cm2` | Float | $\text{cm}^2$ | Yes | Calculated area of Principal Display Panel. |
| `measured_font_height_mm`| Float | $\text{mm}$ | Yes | Calibrated vertical height of numeral or uppercase letter. |
| `scale_factor_mm_per_px` | Float | $\text{mm/px}$ | Yes | Spatial calibration factor from reference marker. |
| `measurement_uncertainty`| Float | $\pm\text{mm}$ | Yes | Bounded $2\sigma$ optical and calibration uncertainty. |
| `net_quantity_declared` | Float | Base SI | Yes | Normalized net weight/volume value. |
| `mrp_declared` | Float | $\text{INR}$ | Yes | Declared maximum retail price inclusive of taxes. |
| `rule_verdict` | Enum | — | No | `PASS` \| `FAIL` \| `REVIEW` \| `NOT_APPLICABLE`. |
