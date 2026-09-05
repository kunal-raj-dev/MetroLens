# DATA PROVENANCE & PRIVACY SPECIFICATION
**Document:** `AI_CONTEXT/EXPERIMENTS/CHUNK_3_REAL_DATA/02_DATA/PROVENANCE_SPECIFICATION.md`  
**Standard:** Member 1 Packaging Dataset Metadata Standard v1.0  
**Target Collection:** 35 Authentic Indian Retail SKUs  

---

## 1. Required Metadata Fields
For every authentic physical packaging image ingested into `data/raw/real/`, the following metadata fields must be registered in `data/manifests/real_packaging_manifest.json`:

| Field Name | Type | Description / Constraints | Example |
| :--- | :--- | :--- | :--- |
| `image_id` | String | Unique image token (alphanumeric + hyphen) | `"REAL-01-SNACK-POUCH"` |
| `sku_id` | String | Product SKU identifier (disjoint grouping key) | `"SKU-HALDIRAM-BHUJIA-200G"` |
| `product_category` | Enum | `snacks`, `beverages`, `personal_care`, `household_products`, `packaged_staples` | `"snacks"` |
| `brand` | String | Commercial product brand / label | `"Haldiram's"` |
| `capture_source` | String | Store type / geography | `"Kirana Store, Gurugram, NCR"` |
| `capture_method` | String | Camera sensor, resolution, handheld/tripod | `"Handheld Smartphone (12MP 4032x3024)"` |
| `capture_date` | String | Date of photo acquisition (YYYY-MM-DD) | `"2026-09-05"` |
| `image_resolution` | [int, int] | Pixel width and height `[W, H]` | `[1920, 1080]` |
| `surface_type` | Enum | `flat_carton`, `flexible_pouch`, `glossy_foil`, `curved_can`, `curved_bottle`, `blister_pack` | `"flexible_pouch"` |
| `language_script` | Enum | Primary script(s): `latin`, `devanagari`, `mixed` | `"mixed"` |
| `special_conditions` | List[Enum] | `clean`, `dot_matrix_inkjet`, `low_contrast_foil`, `glare_reflection`, `micro_font_below_1mm`, `creased_pouch` | `["low_contrast_foil", "dot_matrix_inkjet"]` |
| `ground_truth_status` | Enum | `annotated_single`, `annotated_consensus`, `pending` | `"annotated_consensus"` |
| `dataset_split` | Enum | `development` (70%) or `holdout` (30%) | `"development"` |

## 2. Privacy & Data Minimization Protocol
1. **Zero Personal Identifiable Information (PII):** No customer faces, fingers/hands, retail clerk details, or payment counters may appear in images. Any accidental PII must be cropped prior to ingestion.
2. **Exif Stripping:** All GPS coordinates, camera serial numbers, and device unique IDs must be stripped prior to disk committing.
3. **Third-Party Trademark Notice:** Packaging images are ingested under statutory fair dealing for non-commercial standards verification research.
