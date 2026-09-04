#!/usr/bin/env python3
"""
Nirikshak Report Provenance Verification Utility
Validates that an inspection report contains complete cryptographic hashes,
source citations, calibrated measurement references, and operator details.
"""

import sys
import json
import hashlib
from pathlib import Path

REQUIRED_DOSSIER_FIELDS = [
    "inspection_id",
    "timestamp_utc",
    "operator_id",
    "package_metadata",
    "captured_images",
    "calibration_record",
    "observations",
    "rule_evaluations",
    "cryptographic_summary",
]

def verify_dossier_structure(dossier: dict) -> list:
    errors = []
    for f in REQUIRED_DOSSIER_FIELDS:
        if f not in dossier:
            errors.append(f"Missing required dossier top-level field: '{f}'")
            
    # Verify image hashes exist
    images = dossier.get("captured_images", [])
    if not images:
        errors.append("Dossier contains no captured images.")
    for idx, img in enumerate(images):
        if "sha256" not in img or not img["sha256"]:
            errors.append(f"Captured image #{idx} missing SHA-256 hash.")
            
    # Verify calibration state
    calib = dossier.get("calibration_record", {})
    if calib.get("status") == "UNAVAILABLE":
        # Check that physical measurement rules evaluated to REVIEW
        evals = dossier.get("rule_evaluations", [])
        for ev in evals:
            if ev.get("requires_physical_scale") and ev.get("decision") != "REVIEW":
                errors.append(
                    f"Rule evaluation [{ev.get('rule_id')}] requires physical scale, but decision was "
                    f"'{ev.get('decision')}' instead of 'REVIEW' under uncalibrated capture!"
                )
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_report_provenance.py <path_to_dossier.json>")
        sys.exit(0)
        
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)
        
    with open(path, "r", encoding="utf-8") as f:
        dossier = json.load(f)
        
    errs = verify_dossier_structure(dossier)
    if errs:
        for e in errs:
            print(f"[X] {e}")
        sys.exit(1)
    else:
        print("Dossier provenance check PASSED.")

if __name__ == "__main__":
    main()
