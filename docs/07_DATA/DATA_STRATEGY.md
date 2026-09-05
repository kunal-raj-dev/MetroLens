# Data Strategy & Dataset Governance

## Purpose
Establishes the data acquisition, annotation, synthetic generation, licensing, and quality verification standards for all packaging image datasets in Nirikshak.

## Scope
Governs data stored in `data/`, `benchmarks/datasets/`, and `assets/sample_packages/`.

## Authoritative Inputs
- Indian Copyright Act, 1957.
- Digital Personal Data Protection (DPDP) Act, 2023.

## Assumptions
- No unverified images from general internet image search engines may be added to the repository without explicit provenance tracking in `data/manifests/manifest.yaml`.

## Open Questions
- Departmental data sharing permissions for seized packaging evidence repositories [TBD — PRIMARY SOURCE REQUIRED].

## Dependencies
- `data/manifests/manifest.yaml`
- `scripts/verification/verify_dataset_manifest.py`

## Verification Requirements
- Every dataset partition must validate via `python scripts/verification/verify_dataset_manifest.py`.

---

## Dataset Partitioning & Stratification

```
data/
├── raw/            # Team-collected physical packaging photographs (unprocessed)
├── processed/      # Perspective-rectified and glare-filtered images
├── annotations/    # Ground-truth JSON bounding boxes, text strings, and caliper mm measurements
├── synthetic/      # Procedurally rendered 2D/3D mock packaging layouts (zero copyright friction)
├── benchmark/      # Standardized evaluation set for repeatable empirical scoring
└── manifests/      # Canonical YAML manifests tracking provenance, licenses, and collection dates
```

### Ethical Collection & Ground Truth Protocol:
1. **Physical Retail Sourcing:** Physical products purchased at standard retail price.
2. **Caliper Ground Truth:** Font heights and panel dimensions measured using calibrated digital vernier calipers ($\pm 0.02\text{ mm}$ resolution).
3. **Dual-Blind Annotation:** Two independent annotators transcribe text declarations; discrepancies resolved by senior lead.
