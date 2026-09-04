#!/usr/bin/env python3
"""
Nirikshak Claims Verification Script
Enforces the anti-hallucination policy for technical, performance, and legal claims.
Any claim marked 'VERIFIED' MUST point to an existing empirical benchmark report
or authenticated source record on disk; otherwise the build fails.
"""

import sys
import re
from pathlib import Path

CLAIMS_FILE = Path("docs/17_CLAIMS/CLAIMS_REGISTER.md")

ALLOWED_STATUSES = {
    "VERIFIED",
    "PARTIALLY_VERIFIED",
    "UNVERIFIED",
    "TBD_MEASURE",
    "EXPERIMENT_REQUIRED",
    "PRIMARY_SOURCE_REQUIRED",
    "REJECTED",
}

def main():
    if not CLAIMS_FILE.exists():
        print(f"ERROR: Claims register not found at {CLAIMS_FILE}")
        sys.exit(1)

    content = CLAIMS_FILE.read_text(encoding="utf-8")
    
    # Parse Markdown blocks for Claim items
    # Example format:
    # ## Claim: [ID]
    # - **Claim:** "..."
    # - **Type:** TECHNICAL | LEGAL | PERFORMANCE | COMPETITIVE
    # - **Status:** VERIFIED | TBD_MEASURE | ...
    # - **Evidence:** path/to/file or citation
    
    claim_blocks = re.findall(r"## Claim:\s*([^\n]+)(.*?)(?=\n## Claim:|\Z)", content, re.DOTALL)
    
    if not claim_blocks:
        print(f"WARNING: No structured claim blocks parsed in {CLAIMS_FILE}")
        return

    errors = []
    total_claims = 0

    for claim_id, body in claim_blocks:
        total_claims += 1
        claim_id = claim_id.strip()
        
        status_match = re.search(r"-\s*\*\*Status:\*\*\s*([A-Za-z0-9_—\- ]+)", body)
        evidence_match = re.search(r"-\s*\*\*Evidence:\*\*\s*([^\n]+)", body)
        verified_date_match = re.search(r"-\s*\*\*verified_date:\*\*\s*([^\n]+)", body)
        last_reviewed_match = re.search(r"-\s*\*\*last_reviewed:\*\*\s*([^\n]+)", body)
        
        if not status_match:
            errors.append(f"Claim [{claim_id}] missing '**Status:**' field.")
            continue
            
        status = status_match.group(1).strip().replace(" — ", "_").replace(" ", "_")
        
        if status not in ALLOWED_STATUSES:
            errors.append(f"Claim [{claim_id}] has invalid status '{status}'. Must be one of {ALLOWED_STATUSES}")
            
        if not last_reviewed_match:
            errors.append(f"Claim [{claim_id}] missing required field '**last_reviewed:**'.")

        if status == "VERIFIED":
            if not verified_date_match or verified_date_match.group(1).strip().lower() in ["null", "none", ""]:
                errors.append(f"Claim [{claim_id}] marked VERIFIED must have a valid non-null '**verified_date:**'.")
            if not evidence_match:
                errors.append(f"Claim [{claim_id}] marked VERIFIED but has no '**Evidence:**' path!")
            else:
                evidence_path = evidence_match.group(1).strip().strip("`").strip('"')
                p = Path(evidence_path)
                if not p.exists():
                    errors.append(
                        f"Claim [{claim_id}] marked VERIFIED, but evidence path '{evidence_path}' does not exist on disk! "
                        "Mark status as 'EXPERIMENT_REQUIRED' or 'TBD_MEASURE' until benchmark is executed."
                    )
        else:
            if verified_date_match and verified_date_match.group(1).strip().lower() not in ["null", "none", ""]:
                v_date = verified_date_match.group(1).strip()
                errors.append(
                    f"Claim [{claim_id}] status is '{status}' but has populated verified_date '{v_date}'. "
                    "Unverified claims must have verified_date: null (reviewed is NOT verified)."
                )

    if errors:
        print("\n--- Claims Verification Failures ---")
        for err in errors:
            print(f"  [X] {err}")
        print(f"\nTotal claim validation errors: {len(errors)}")
        sys.exit(1)
    else:
        print(f"SUCCESS: Verified {total_claims} claims in {CLAIMS_FILE}. No unbacked VERIFIED claims.")

if __name__ == "__main__":
    main()
