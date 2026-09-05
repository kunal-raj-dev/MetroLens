#!/usr/bin/env python3
"""
Nirikshak Dataset Manifest Verification Script
Validates data/manifests/manifest.yaml to guarantee that every dataset batch
has explicit source, license, collection date, ground truth method, and limitations.
"""

import sys
import yaml
from pathlib import Path

MANIFEST_PATH = Path("data/manifests/manifest.yaml")

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
]

def main():
    if not MANIFEST_PATH.exists():
        print(f"ERROR: Dataset manifest not found at {MANIFEST_PATH}")
        sys.exit(1)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"ERROR: Failed to parse {MANIFEST_PATH}: {e}")
            sys.exit(1)

    datasets = data.get("datasets", [])
    if not datasets:
        print(f"WARNING: No datasets defined in {MANIFEST_PATH}")
        return

    errors = []
    seen_ids = set()

    for idx, ds in enumerate(datasets):
        ds_id = ds.get("dataset_id", f"INDEX_{idx}")
        if ds_id in seen_ids:
            errors.append(f"Duplicate dataset_id: '{ds_id}'")
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

    if errors:
        print("\n--- Dataset Manifest Verification Failures ---")
        for err in errors:
            print(f"  [X] {err}")
        print(f"\nTotal dataset manifest errors: {len(errors)}")
        sys.exit(1)
    else:
        print(f"SUCCESS: Verified {len(datasets)} dataset manifest entries in {MANIFEST_PATH}.")

if __name__ == "__main__":
    main()
