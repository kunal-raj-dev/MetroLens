"""Single image inspection entry point with bounded processing capacity."""

import threading

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from starlette.concurrency import run_in_threadpool

from apps.api.auth.dependencies import ServicePrincipal, require_api_access
from apps.api.errors import ImageTooLargeError, InvalidImagePayloadError
from apps.api.middleware.security import MAX_UPLOAD_SIZE_BYTES
from apps.api.schemas import AnchorType, InspectionResponse, PanelType
from apps.api.services.inspection_store import inspection_store
from apps.api.services.pipeline_orchestrator import pipeline_orchestrator


router = APIRouter(prefix="/api/v1", tags=["Inspection"])
processing_slot = threading.BoundedSemaphore(1)


def _process(content: bytes, filename: str, anchor_type: str, panel_type: str,
             principal: ServicePrincipal) -> InspectionResponse:
    response = pipeline_orchestrator.orchestrate_inspection(
        image_bytes=content, filename=filename, anchor_type=anchor_type,
        panel_type=panel_type, officer_id=principal.display_name,
    )
    session = pipeline_orchestrator.spooler.get_session(response.inspection_id)
    if session is None:
        raise HTTPException(503, "Inspection evidence could not be retained. Please retry.")
    inspection_store.put(
        response=response, compliance_result=session.metadata["compliance_result"],
        principal_id=principal.subject, raw_sha256=session.metadata["raw_sha256"],
        sanitized_sha256=session.metadata["sanitized_sha256"],
        raw_size_bytes=session.metadata["raw_size_bytes"],
        sanitized_size_bytes=session.metadata["sanitized_size_bytes"],
    )
    return response


@router.post("/inspect", response_model=InspectionResponse)
async def inspect_packaging(
    request: Request,
    principal: ServicePrincipal = Depends(require_api_access),
    file: UploadFile = File(...),
    anchor_type: AnchorType = Form(AnchorType.INR_10_COIN),
    panel_type: PanelType = Form(PanelType.FRONT_PDP),
) -> InspectionResponse:
    form = await request.form()
    if any(key in form for key in ("mock_fixture_key", "mock_tokens")):
        raise HTTPException(400, "Test fixtures are unavailable in the live inspection API.")
    if len(form.getlist("file")) != 1:
        raise InvalidImagePayloadError("Provide exactly one packaging image.")
    if not processing_slot.acquire(blocking=False):
        raise HTTPException(429, "Another inspection is processing. Please retry shortly.", headers={"Retry-After": "5"})
    try:
        chunks = bytearray()
        while True:
            chunk = await file.read(min(65536, MAX_UPLOAD_SIZE_BYTES + 1 - len(chunks)))
            if not chunk:
                break
            chunks.extend(chunk)
            if len(chunks) > MAX_UPLOAD_SIZE_BYTES:
                raise ImageTooLargeError(len(chunks), MAX_UPLOAD_SIZE_BYTES)
        if not chunks:
            raise InvalidImagePayloadError("Uploaded file payload is empty.")
        filename = (file.filename or "upload.jpg").replace("\\", "/").rsplit("/", 1)[-1]
        filename = "".join(c for c in filename if c.isprintable())[:200] or "upload.jpg"
        return await run_in_threadpool(_process, bytes(chunks), filename, anchor_type.value, panel_type.value, principal)
    finally:
        await file.close()
        processing_slot.release()
