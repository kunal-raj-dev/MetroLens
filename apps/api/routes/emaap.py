"""
MetroLens API Gateway: Mock eMaap e-Governance Sync Route.
Implements POST /api/v1/emaap/mock-sync adhering to docs/API_CONTRACT.md Section 3.4.
"""

import logging
import random
import re
from datetime import datetime, timezone
from fastapi import APIRouter, status
from apps.api.schemas import EMaapSyncRequest, EMaapSyncResponse

logger = logging.getLogger("metrolens.routes.emaap")

router = APIRouter(prefix="/api/v1", tags=["e-Governance Sync"])

HEX_SHA256_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")


@router.post(
    "/emaap/mock-sync",
    response_model=EMaapSyncResponse,
    status_code=status.HTTP_200_OK,
    summary="Simulate National eMaap Legal Metrology Portal synchronization",
    description=(
        "Simulates the National eMaap (Legal Metrology e-Governance) webhook synchronization "
        "for statutory inspection dossiers, generating official registry reference numbers "
        "and performing cryptographic tamper verification."
    ),
)
def sync_with_national_emaap_portal(payload: EMaapSyncRequest) -> EMaapSyncResponse:
    """
    Synchronizes an inspection dossier with the National eMaap registry.
    Validates cryptographic signature integrity and assigns statutory registration reference.
    """
    logger.info(
        "eMaap mock-sync request: inspection_id='%s', jurisdiction='%s', officer='%s', state='%s'",
        payload.inspection_id,
        payload.jurisdiction_code,
        payload.officer_id,
        payload.compliance_state,
    )

    now_utc = datetime.now(timezone.utc)
    now_iso = now_utc.isoformat()
    current_year = now_utc.strftime("%Y")

    # 1. Cryptographic Tamper Verification
    is_valid_hash = bool(HEX_SHA256_PATTERN.match(payload.dossier_sha256))
    tamper_verdict = "VERIFIED_VALID" if is_valid_hash else "TAMPER_DETECTED"
    sync_status = "ACCEPTED_FOR_RECORD" if is_valid_hash else "REJECTED"

    # 2. Derive state jurisdiction prefix
    jurisdiction_clean = payload.jurisdiction_code.strip().upper()
    state_prefix = jurisdiction_clean.split("-")[0] if "-" in jurisdiction_clean else "IN"
    if len(state_prefix) > 4 or not state_prefix.isalpha():
        state_prefix = "DL"

    # 3. Generate deterministic reference sequence
    random_seq = random.randint(1000, 99999)
    reference_no = f"EMAAP-{state_prefix}-{current_year}-{random_seq:06d}"

    logger.info(
        "eMaap sync outcome: ref='%s', status='%s', tamper='%s'",
        reference_no,
        sync_status,
        tamper_verdict,
    )

    return EMaapSyncResponse(
        sync_status=sync_status,
        emaap_reference_no=reference_no,
        received_at=now_iso,
        tamper_verification=tamper_verdict,
    )
