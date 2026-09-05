#!/usr/bin/env python3
"""
Nirikshak Legal Source Verification Script
Ensures every regulatory source record has verified provenance, required dates,
valid instrument_status, and valid SHA-256 hashes if the file is present on disk.
"""

import os
import sys
import hashlib
import yaml
from pathlib import Path

REGISTRY_PATH = Path("regulations/source_registry.yaml")

REQUIRED_FIELDS = [
    "source_id",
    "title",
    "issuing_authority",
    "source_type",
    "publication_date",
    "effective_from",
    "effective_to",
    "instrument_status",
    "official_url",
    "retrieval_date",
    "document_sha256",
    "local_artifact",
    "verification_status",
    "verified_by",
    "verification_date",
    "last_reviewed",
    "notes",
]

VALID_INSTRUMENT_STATUSES = [
    "IN_FORCE",
    "PROPOSED",
    "DRAFT",
    "SUPERSEDED",
    "REPEALED",
    "UNKNOWN",
]

VALID_VERIFICATION_STATUSES = [
    "VERIFIED_PRIMARY",
    "VERIFIED_SECONDARY",
    "PARTIALLY_VERIFIED",
    "CONFLICTING",
    "UNVERIFIED",
    "PRIMARY_SOURCE_REQUIRED",
    "SUPERSEDED",
    "REJECTED",
]

def calculate_sha256(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    if not REGISTRY_PATH.exists():
        print(f"ERROR: Source registry file not found at {REGISTRY_PATH}")
        sys.exit(1)

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"ERROR: Failed to parse {REGISTRY_PATH}: {e}")
            sys.exit(1)

    sources = data.get("sources", [])
    if not sources:
        print("WARNING: No sources defined in source_registry.yaml")
        return

    errors = []
    seen_ids = set()

    for idx, src in enumerate(sources):
        src_id = src.get("source_id", f"INDEX_{idx}")
        if src_id in seen_ids:
            errors.append(f"Duplicate source_id: '{src_id}'")
        seen_ids.add(src_id)

        ver_status = src.get("verification_status")

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in src:
                errors.append(f"Source [{src_id}] missing required field: '{field}'")
            elif field == "effective_to":
                # effective_to can be null for active in-force instruments
                pass
            elif field == "verification_date":
                if ver_status in ["VERIFIED_PRIMARY", "VERIFIED_SECONDARY"]:
                    if src[field] is None or src[field] == "":
                        errors.append(f"Source [{src_id}] marked '{ver_status}' but 'verification_date' is null or empty.")
                else:
                    if src[field] is not None and src[field] != "":
                        errors.append(f"Source [{src_id}] status is '{ver_status}' but 'verification_date' is populated ('{src[field]}'). Unverified sources must have verification_date: null and record last_reviewed.")
            elif src[field] is None or src[field] == "":
                errors.append(f"Source [{src_id}] empty required field: '{field}'")

        # Validate status enums
        inst_status = src.get("instrument_status")
        if inst_status and inst_status not in VALID_INSTRUMENT_STATUSES:
            errors.append(f"Source [{src_id}] invalid instrument_status: '{inst_status}'. Must be one of {VALID_INSTRUMENT_STATUSES}")

        ver_status = src.get("verification_status")
        if ver_status and ver_status not in VALID_VERIFICATION_STATUSES:
            errors.append(f"Source [{src_id}] invalid verification_status: '{ver_status}'. Must be one of {VALID_VERIFICATION_STATUSES}")

        # Check file integrity if local file path is specified
        local_path = src.get("local_artifact")
        if local_path and local_path != "PRIMARY_SOURCE_REQUIRED":
            p = Path(local_path)
            if p.exists() and p.is_file() and p.name != ".gitkeep":
                computed_hash = calculate_sha256(p)
                recorded_hash = src.get("document_sha256", "")
                if recorded_hash and recorded_hash != "PRIMARY_SOURCE_REQUIRED" and recorded_hash.lower() != computed_hash.lower():
                    errors.append(f"Source [{src_id}] SHA-256 mismatch! Recorded: {recorded_hash}, Computed: {computed_hash}")
            else:
                if ver_status == "VERIFIED_PRIMARY":
                    errors.append(f"Source [{src_id}] marked VERIFIED_PRIMARY but local file '{local_path}' does not exist on disk!")

    if errors:
        print("\n--- Legal Source Verification Failures ---")
        for err in errors:
            print(f"  [X] {err}")
        print(f"\nTotal errors found: {len(errors)}")
        sys.exit(1)
    else:
        print(f"SUCCESS: Verified {len(sources)} legal source records in {REGISTRY_PATH}.")

if __name__ == "__main__":
    main()
