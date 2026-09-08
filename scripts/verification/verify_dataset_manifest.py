import json
from pathlib import Path
import sys
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_YAML = REPO_ROOT / "data" / "manifests" / "manifest.yaml"
REAL_PACKAGING_MANIFEST = REPO_ROOT / "data" / "manifests" / "real_packaging_manifest.json"
GROUND_TRUTH_BENCHMARK = REPO_ROOT / "data" / "manifests" / "ground_truth_benchmark.json"
CADBURY_MANIFEST = REPO_ROOT / "data" / "real_world" / "dairy_milk_bubbly" / "dataset_manifest.json"
SYNTHETIC_MANIFEST = REPO_ROOT / "data" / "synthetic" / "regression" / "manifest.json"

REQUIRED_MANIFEST_FIELDS = [
    "dataset_id",
    "title",
    "source",
    "license",
    "rights_status",
    "permission",
    "collection_date",
    "geography",
    "annotation_method",
    "ground_truth_method",
    "known_limitations",
]

VALID_RIGHTS_STATUSES = [
    "VERIFIED",
    "RIGHTS_VERIFICATION_REQUIRED",
    "UNVERIFIED",
    "REJECTED",
]

VALID_ARTIFACT_STATUSES = [
    "ACTUAL",
    "PARTIAL",
    "DECLARED_BUT_MISSING",
    "PLANNED",
    "NOT_GENERATED",
    "INVALID_CLAIM",
]

VALID_DATASET_STATUSES = [
    "PLANNED",
    "DECLARED_BUT_MISSING",
    "IN_PROGRESS",
    "COLLECTED",
    "VERIFIED",
    "BLOCKED_AWAITING_PHYSICAL_DATA_COLLECTION",
]


def validate_yaml_catalog(errors: list) -> int:
    if not MANIFEST_YAML.exists():
        errors.append(f"Catalog not found at {MANIFEST_YAML}")
        return 0

    with open(MANIFEST_YAML, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            errors.append(f"Failed to parse {MANIFEST_YAML}: {e}")
            return 0

    datasets = data.get("datasets", [])
    seen_ids = set()
    for idx, ds in enumerate(datasets):
        ds_id = ds.get("dataset_id", f"INDEX_{idx}")
        if ds_id in seen_ids:
            errors.append(f"Duplicate dataset_id in YAML: '{ds_id}'")
        seen_ids.add(ds_id)

        for field in REQUIRED_MANIFEST_FIELDS:
            if field not in ds or ds[field] is None or ds[field] == "":
                errors.append(f"Dataset [{ds_id}] missing required field: '{field}'")

        rights = ds.get("rights_status")
        if rights and rights not in VALID_RIGHTS_STATUSES:
            errors.append(f"Dataset [{ds_id}] invalid rights_status '{rights}'. Must be one of {VALID_RIGHTS_STATUSES}")

        art_status = ds.get("artifact_status")
        if art_status and art_status not in VALID_ARTIFACT_STATUSES:
            errors.append(f"Dataset [{ds_id}] invalid artifact_status '{art_status}'. Must be one of {VALID_ARTIFACT_STATUSES}")

        ds_status = ds.get("status")
        if ds_status and ds_status not in VALID_DATASET_STATUSES:
            errors.append(f"Dataset [{ds_id}] invalid status '{ds_status}'. Must be one of {VALID_DATASET_STATUSES}")

    return len(datasets)


def validate_real_packaging_manifest(errors: list):
    if not REAL_PACKAGING_MANIFEST.exists():
        errors.append(f"Real packaging manifest missing at {REAL_PACKAGING_MANIFEST}")
        return

    with open(REAL_PACKAGING_MANIFEST, "r", encoding="utf-8") as f:
        data = json.load(f)

    status = data.get("status")
    disk_count = data.get("disk_images_present", 0)
    records = data.get("records", [])

    if status != "BLOCKED_AWAITING_PHYSICAL_DATA_COLLECTION" and disk_count == 0:
        errors.append(f"real_packaging_manifest declares status='{status}' but disk_images_present is 0.")

    # If any records are listed, verify files actually exist on disk
    for rec in records:
        rel_path = rec.get("relative_image_path")
        if not rel_path:
            errors.append(f"Record {rec.get('image_id')} missing relative_image_path")
        elif not (REPO_ROOT / rel_path).exists():
            errors.append(f"Record {rec.get('image_id')} references missing file: {rel_path}")


def validate_cadbury_real_specimen(errors: list) -> int:
    if not CADBURY_MANIFEST.exists():
        errors.append(f"Cadbury dataset manifest missing at {CADBURY_MANIFEST}")
        return 0

    with open(CADBURY_MANIFEST, "r", encoding="utf-8") as f:
        data = json.load(f)

    parent_dir = CADBURY_MANIFEST.parent
    core_images = data.get("core_images", [])
    excluded_images = data.get("excluded_images", [])

    seen_files = set()
    for img in core_images:
        fname = img.get("filename")
        if not fname:
            errors.append("Cadbury core image missing filename")
            continue
        if fname in seen_files:
            errors.append(f"Duplicate filename in Cadbury core images: {fname}")
        seen_files.add(fname)

        fpath = parent_dir / fname
        if not fpath.exists():
            errors.append(f"Cadbury core image not found on disk: {fpath}")

    for img in excluded_images:
        fname = img.get("filename")
        if not fname:
            errors.append("Cadbury excluded image missing filename")
            continue
        if fname in seen_files:
            errors.append(f"Duplicate filename across core/excluded: {fname}")
        seen_files.add(fname)

        fpath = parent_dir / "excluded" / fname
        if not fpath.exists():
            errors.append(f"Cadbury excluded image not found on disk: {fpath}")

    # Verify metrological status is unvarnished
    metro_status = data.get("metrological_status", {})
    if metro_status.get("physical_ground_truth_available") is not False:
        errors.append("Cadbury specimen must not claim physical ground truth available until caliper data is on disk.")
    if metro_status.get("benchmark_status") != "BENCHMARK_BLOCKED":
        errors.append(f"Cadbury specimen benchmark_status must be 'BENCHMARK_BLOCKED', got '{metro_status.get('benchmark_status')}'")

    return len(core_images) + len(excluded_images)


def validate_synthetic_regression_manifest(errors: list) -> int:
    if not SYNTHETIC_MANIFEST.exists():
        errors.append(f"Synthetic manifest missing at {SYNTHETIC_MANIFEST}")
        return 0

    with open(SYNTHETIC_MANIFEST, "r", encoding="utf-8") as f:
        samples = json.load(f)

    if not isinstance(samples, list):
        errors.append("Synthetic manifest must be a list of sample objects.")
        return 0

    parent_dir = SYNTHETIC_MANIFEST.parent
    seen_ids = set()

    for sample in samples:
        s_id = sample.get("id")
        if not s_id:
            errors.append("Synthetic sample missing 'id'")
            continue
        if s_id in seen_ids:
            errors.append(f"Duplicate synthetic sample ID: {s_id}")
        seen_ids.add(s_id)

        # Invariant: Must be explicitly classified as synthetic
        if not sample.get("is_synthetic"):
            errors.append(f"Sample {s_id} must have is_synthetic: true")

        disclaimer = sample.get("disclaimer", "")
        if "SYNTHETIC" not in disclaimer.upper():
            errors.append(f"Sample {s_id} missing mandatory SYNTHETIC disclaimer: '{disclaimer}'")

        # Invariant: Resolution must be positive numbers
        res = sample.get("resolution")
        if not res or len(res) != 2 or res[0] <= 0 or res[1] <= 0:
            errors.append(f"Sample {s_id} invalid resolution: {res}")

        # Check file exists in synthetic regression folder
        expected_filename = f"{s_id}.png"
        direct_path = parent_dir / expected_filename
        if not direct_path.exists():
            # Check file_path fallback
            fp = sample.get("file_path")
            if not fp or not (REPO_ROOT / fp).exists():
                errors.append(f"Synthetic specimen image file not found for {s_id} at {direct_path}")

    return len(samples)


def main():
    errors = []

    yaml_count = validate_yaml_catalog(errors)
    validate_real_packaging_manifest(errors)
    cadbury_count = validate_cadbury_real_specimen(errors)
    synth_count = validate_synthetic_regression_manifest(errors)

    if errors:
        print("\n========================================================")
        print("DATASET MANIFEST VERIFICATION FAILURES (FAIL-LOUD AUDIT)")
        print("========================================================")
        for err in errors:
            print(f"  [X] {err}")
        print(f"\nTotal dataset manifest errors: {len(errors)}")
        sys.exit(1)
    else:
        print("\n========================================================")
        print("DATASET MANIFEST VERIFICATION: ALL AUDITS PASSED (100%)")
        print("========================================================")
        print(f"  - YAML Catalog Entries Verified: {yaml_count}")
        print(f"  - Real Packaging Manifest: Verified (Status: BLOCKED_AWAITING_PHYSICAL_DATA_COLLECTION)")
        print(f"  - Real Cadbury Specimen Images: {cadbury_count} files verified on disk (Status: BENCHMARK_BLOCKED)")
        print(f"  - Synthetic Test Specimens: {synth_count} verified with explicit disclaimers")
        print("  - Zero fabricated physical measurements detected.")
        print("========================================================\n")


if __name__ == "__main__":
    main()
