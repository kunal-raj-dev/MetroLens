#!/usr/bin/env python3
"""
Nirikshak Rule Registry Verification Script
Enforces schema validity, exact source location provenance, and strict lifecycle rules:
rules/current/ MUST contain only rules whose status = IN_FORCE and whose
verification_status is VERIFIED_PRIMARY. Placeholder/unverified rules must reside in proposed/.
"""

import os
import sys
import yaml
import json
from pathlib import Path

REGISTRY_PATH = Path("regulations/source_registry.yaml")
RULES_DIR = Path("rules")
SCHEMA_DIR = Path("rules/schema")

REQUIRED_RULE_FIELDS = [
    "rule_id",
    "title",
    "status",
    "source_id",
    "source_document_sha256",
    "source_page",
    "source_section",
    "source_rule",
    "source_subrule",
    "source_table",
    "effective_from",
    "effective_to",
    "applicability",
    "requirements",
    "exceptions",
    "evidence_required",
    "uncertainty_policy",
    "verification_status",
    "last_verified",
]

ALLOWED_STATUSES = {
    "IN_FORCE",
    "PROPOSED",
    "DRAFT",
    "SUPERSEDED",
    "REPEALED",
    "PRIMARY_SOURCE_REQUIRED",
}

ALLOWED_VERIFICATION_STATUSES = {
    "VERIFIED_PRIMARY",
    "VERIFIED_SECONDARY",
    "PARTIALLY_VERIFIED",
    "CONFLICTING",
    "UNVERIFIED",
    "PRIMARY_SOURCE_REQUIRED",
    "SUPERSEDED",
    "REJECTED",
}

def load_known_source_ids():
    if not REGISTRY_PATH.exists():
        return set()
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {s["source_id"] for s in data.get("sources", []) if "source_id" in s}

def verify_rule_file(path: Path, known_sources: set, is_current_dir: bool) -> list:
    errors = []
    with open(path, "r", encoding="utf-8") as f:
        try:
            rule_data = yaml.safe_load(f)
        except Exception as e:
            return [f"YAML syntax error in {path}: {e}"]

    if not isinstance(rule_data, dict):
        return [f"Invalid format in {path}: root must be a mapping"]

    rule_id = rule_data.get("rule_id", path.stem)

    # Check required fields
    for field in REQUIRED_RULE_FIELDS:
        if field not in rule_data:
            errors.append(f"Rule [{rule_id}] in {path} missing required field: '{field}'")

    # Validate status
    st = rule_data.get("status")
    if st and st not in ALLOWED_STATUSES:
        errors.append(f"Rule [{rule_id}] invalid status: '{st}'. Must be one of {ALLOWED_STATUSES}")

    ver_st = rule_data.get("verification_status")
    if ver_st and ver_st not in ALLOWED_VERIFICATION_STATUSES:
        errors.append(f"Rule [{rule_id}] invalid verification_status: '{ver_st}'. Must be one of {ALLOWED_VERIFICATION_STATUSES}")

    # Check source_id exists in registry
    src_id = rule_data.get("source_id")
    if src_id and src_id not in known_sources and src_id != "PRIMARY_SOURCE_REQUIRED":
        errors.append(f"Rule [{rule_id}] references unknown source_id '{src_id}' not found in {REGISTRY_PATH}")

    # Lifecycle gate: rules/current/ MUST contain only IN_FORCE + VERIFIED_PRIMARY
    if is_current_dir:
        if st != "IN_FORCE":
            errors.append(f"Lifecycle Violation: Rule [{rule_id}] in rules/current/ has status '{st}'. Only 'IN_FORCE' rules with verified dates may reside in current/.")
        if ver_st != "VERIFIED_PRIMARY":
            errors.append(f"Lifecycle Violation: Rule [{rule_id}] in rules/current/ has verification_status '{ver_st}'. Only 'VERIFIED_PRIMARY' rules may reside in current/.")
    else:
        if rule_data.get("executable") is True and ver_st != "VERIFIED_PRIMARY":
            errors.append(f"Safety Violation: Rule [{rule_id}] in {path} has executable: true but verification_status is '{ver_st}'. Non-verified rules must have executable: false.")

    return errors

def main():
    known_sources = load_known_source_ids()
    all_errors = []

    folders = [
        ("rules/proposed", False),
        ("rules/verified", False),
        ("rules/current", True),
        ("rules/historical", False),
        ("rules/superseded", False),
    ]

    total_rules = 0
    for folder_path, is_current in folders:
        p = Path(folder_path)
        if not p.exists():
            continue
        for rule_file in p.glob("*.yaml"):
            total_rules += 1
            errs = verify_rule_file(rule_file, known_sources, is_current)
            all_errors.extend(errs)

    if all_errors:
        print("\n--- Rule Registry Verification Failures ---")
        for err in all_errors:
            print(f"  [X] {err}")
        print(f"\nTotal rule validation errors: {len(all_errors)}")
        sys.exit(1)
    else:
        print(f"SUCCESS: Validated {total_rules} rule files across lifecycle directories.")

if __name__ == "__main__":
    main()
