#!/usr/bin/env python3
"""
Nirikshak Master Repository Integrity Verification Script
Enforces holistic repository invariants:
1. Exactly one canonical regulatory registry exists (regulations/source_registry.yaml).
2. No duplicate source registries exist in docs/ or elsewhere.
3. rules/current/ contains ONLY rules that are IN_FORCE and VERIFIED_PRIMARY.
4. All machine rules link back to a valid source_id in regulations/source_registry.yaml.
5. Proposed or draft instruments are NEVER treated as active law.
6. Claims in docs/17_CLAIMS/ marked VERIFIED must have existing evidence on disk.
7. Subordinate verification scripts are invoked and must pass.
"""

import sys
import subprocess
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

CANONICAL_REGISTRY = REPO_ROOT / "regulations" / "source_registry.yaml"
FORBIDDEN_DUPLICATES = [
    REPO_ROOT / "docs" / "02_LEGAL_AUTHORITY" / "SOURCE_REGISTER.yaml",
    REPO_ROOT / "docs" / "02_LEGAL_AUTHORITY" / "source_registry.yaml",
    REPO_ROOT / "rules" / "source_registry.yaml",
]

SUBORDINATE_SCRIPTS = [
    REPO_ROOT / "scripts" / "verification" / "verify_legal_sources.py",
    REPO_ROOT / "scripts" / "verification" / "verify_rule_registry.py",
    REPO_ROOT / "scripts" / "verification" / "verify_claims.py",
    REPO_ROOT / "scripts" / "verification" / "verify_dataset_manifest.py",
]

def check_registry_duplicates() -> list:
    errors = []
    if not CANONICAL_REGISTRY.exists():
        errors.append(f"Missing canonical source registry at {CANONICAL_REGISTRY}")
    for forbidden in FORBIDDEN_DUPLICATES:
        if forbidden.exists():
            errors.append(f"Forbidden duplicate source registry found at {forbidden}! Canonical location is regulations/source_registry.yaml.")
    return errors

def check_rules_lifecycle_safety() -> list:
    errors = []
    current_dir = REPO_ROOT / "rules" / "current"
    if current_dir.exists():
        for rule_file in current_dir.glob("*.yaml"):
            try:
                with open(rule_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                st = data.get("status")
                vst = data.get("verification_status")
                if st != "IN_FORCE":
                    errors.append(f"Rule safety failure in {rule_file}: status is '{st}'. Only 'IN_FORCE' rules with verified dates may reside in rules/current/.")
                if vst != "VERIFIED_PRIMARY":
                    errors.append(f"Rule safety failure in {rule_file}: verification_status is '{vst}'. Only 'VERIFIED_PRIMARY' rules may reside in rules/current/.")
            except Exception as e:
                errors.append(f"Failed to parse rule file {rule_file}: {e}")
    return errors

def check_features_governance_safety() -> list:
    errors = []
    features_doc = REPO_ROOT / "docs" / "14_SUBMISSION" / "FINAL_FEATURES.md"
    if not features_doc.exists():
        errors.append(f"Missing final features register at {features_doc}")
        return errors
    
    content = features_doc.read_text(encoding="utf-8")
    if "VERIFIED_PRIMARY" in content:
        # Check that VERIFIED_PRIMARY is not used in the table for FEAT- rows
        for line in content.splitlines():
            if line.strip().startswith("| **FEAT-"):
                cols = [c.strip() for c in line.split("|")[1:-1]]
                if len(cols) >= 5:
                    impl_status = cols[4]
                    if "VERIFIED_PRIMARY" in impl_status:
                        errors.append(f"Governance Violation: {cols[0]} has implementation stage '{impl_status}'. Software features must not use VERIFIED_PRIMARY.")
    return errors

def run_subordinate_scripts() -> list:
    errors = []
    for script in SUBORDINATE_SCRIPTS:
        if not script.exists():
            errors.append(f"Subordinate script missing: {script}")
            continue
        res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        if res.returncode != 0:
            errors.append(f"Script {script.name} failed with exit code {res.returncode}:\n{res.stdout}\n{res.stderr}")
    return errors

def main():
    print("Running Nirikshak Master Repository Integrity Audit...")
    all_errors = []

    # 1. Check duplicate registries
    errs = check_registry_duplicates()
    all_errors.extend(errs)

    # 2. Check rules lifecycle safety
    errs = check_rules_lifecycle_safety()
    all_errors.extend(errs)

    # 3. Check features governance safety
    errs = check_features_governance_safety()
    all_errors.extend(errs)

    # 4. Run all subordinate verification scripts
    errs = run_subordinate_scripts()
    all_errors.extend(errs)

    if all_errors:
        print("\n=======================================================")
        print("CRITICAL: Master Repository Integrity Verification FAILED")
        print("=======================================================")
        for e in all_errors:
            print(f"  [X] {e}")
        print(f"\nTotal integrity failures: {len(all_errors)}")
        sys.exit(1)
    else:
        print("\n=======================================================")
        print("SUCCESS: Master Repository Integrity Audit PASSED (100%)")
        print("All structural, legal lifecycle, and claims invariants satisfied.")
        print("=======================================================")

if __name__ == "__main__":
    main()
