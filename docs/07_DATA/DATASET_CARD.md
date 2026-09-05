# Dataset Card — Nirikshak Packaging Benchmark Suite

## Purpose
Provides standardized documentation on dataset provenance, intended tasks, composition, collection methodology, and known limitations.

## Scope
Covers `data/raw/` and `data/benchmark/` image corpora.

## Authoritative Inputs
- `data/manifests/manifest.yaml`
- Gebru et al., "Datasheets for Datasets" framework.

## Assumptions
- Datasets are intended exclusively for developing, benchmarking, and evaluating Legal Metrology computer vision systems.

## Open Questions
- Representation of regional language declarations (e.g. Tamil, Bengali, Marathi) on state-distributed packaging [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `data/manifests/`

## Verification Requirements
- All fields must be verified against actual dataset files before final submission.

---

## Dataset Summary

- **Curator:** Nirikshak Engineering Team
- **Release Date:** 2026-09-04
- **Language(s):** English, Hindi (Devanagari numerals and text)
- **Modalities:** 2D High-Resolution Color Photographs (JPEG, PNG)
- **Annotations:** Bounding polygons, transcription text, physical mm measurements, calibration scale.

### Composition & Categories:
1. **Dry Packaged Foods:** Biscuit cartons, tea boxes, spice pouches.
2. **Personal Care & Cosmetics:** Shampoo bottles (cylindrical), soap wrappers (curved cuboid).
3. **Beverages & Oils:** Aluminium beverage cans, plastic edible oil bottles.
4. **Synthetic Edge Cases:** Rendered packages with borderline font heights ($0.98\text{ mm}$ vs $1.00\text{ mm}$).

### Known Biases & Limitations:
- Initial retail pilot (`DS-RETAIL-PILOT-001`) focuses primarily on national FMCG brands purchased in Delhi-NCR retail stores.
- Severely battered, torn, or water-damaged packages are currently excluded from baseline benchmarks.
