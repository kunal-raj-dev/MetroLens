"""Truthful local hash verification; statutory certification is unavailable."""

from fastapi import APIRouter, Depends, HTTPException

from apps.api.auth.dependencies import ServicePrincipal, require_api_access
from apps.api.services.inspection_store import require_inspection, verify_retained_evidence
from apps.api.services.spool_service import spool_service


router = APIRouter(prefix="/api/v1/audit", tags=["Local Evidence Integrity"])


@router.post("/affidavit", dependencies=[Depends(require_api_access)])
def generate_bsa_affidavit():
    raise HTTPException(501, "Statutory certificates require verified officer identity and a signing workflow; this service does not provide them.")


@router.get("/verify/{inspection_id}")
def verify_inspection_proof(
    inspection_id: str, principal: ServicePrincipal = Depends(require_api_access),
):
    record = require_inspection(inspection_id, principal.subject)
    checks = verify_retained_evidence(record, spool_service)
    matches = all(checks.values())
    return {
        "status": "LOCAL_HASHES_MATCH" if matches else "INTEGRITY_MISMATCH",
        "inspection_id": record.inspection_id,
        "checks": checks,
        "tamper_detected": not matches,
        "verification_scope": "Retained raw and sanitized files compared with hashes recorded at ingestion in this process.",
        "cryptographic_signature_verified": False,
        "officer_identity_verified": False,
        "legal_admissibility_certified": False,
    }
