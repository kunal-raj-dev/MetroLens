"""Render a screening report only from an authenticated retained inspection."""

import hashlib

from fastapi import APIRouter, Depends, HTTPException, Response

from apps.api.auth.dependencies import ServicePrincipal, require_api_access
from apps.api.schemas import ReportPdfRequest
from apps.api.services.inspection_store import require_inspection, verify_retained_evidence
from apps.api.services.spool_service import spool_service
from nirikshak_reporting.pdf_compiler import pdf_compiler


router = APIRouter(prefix="/api/v1", tags=["Reports"])


@router.post("/report/pdf")
def download_inspection_report_pdf(
    payload: ReportPdfRequest, principal: ServicePrincipal = Depends(require_api_access),
) -> Response:
    record = require_inspection(payload.inspection_id, principal.subject)
    checks = verify_retained_evidence(record, spool_service)
    if not all(checks.values()):
        raise HTTPException(409, "Retained evidence no longer matches the ingestion hashes.")
    # Compile a copy of the authoritative result; rendering must never invent data
    # on a cache miss or mutate the stored assessment.
    result = record.compliance_result.model_copy(deep=True)
    reference_image_bytes = None
    if payload.include_raw_image:
        session = spool_service.get_session(record.inspection_id)
        if session is None or session.sanitized_image_path is None:
            raise HTTPException(404, "Inspection reference image is unavailable.")
        try:
            path = spool_service._checked_path(session.sanitized_image_path, record.inspection_id)
            with path.open("rb") as source:
                reference_image_bytes = source.read(record.sanitized_size_bytes + 1)
        except (ValueError, OSError):
            raise HTTPException(409, "Inspection reference image is unavailable or changed.") from None
        if (len(reference_image_bytes) != record.sanitized_size_bytes
                or hashlib.sha256(reference_image_bytes).hexdigest() != record.sanitized_sha256):
            raise HTTPException(409, "Inspection reference image changed during report preparation.")
    pdf_bytes = pdf_compiler.compile_report_pdf(
        result, officer_id=principal.display_name, jurisdiction_code="Not verified",
        include_evidence_crops=payload.include_raw_image,
        officer_notes=payload.officer_notes, reference_image_bytes=reference_image_bytes,
    )
    # Retained report is a derivative. It is not a signature or officer attestation.
    spool_service.save_pdf_report(record.inspection_id, pdf_bytes)
    session = spool_service.get_session(record.inspection_id)
    if session is not None:
        session.metadata["report_sha256"] = hashlib.sha256(pdf_bytes).hexdigest()
    return Response(
        content=pdf_bytes, media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="metrolens_report_{record.inspection_id}.pdf"',
            "Cache-Control": "no-store",
        },
    )
