"""
MetroLens API Gateway: Primary Inspection Route.
Implements POST /api/v1/inspect adhering strictly to docs/API_CONTRACT.md.
"""

import logging
from typing import Optional
from fastapi import APIRouter, File, Form, Header, UploadFile, status
from fastapi.responses import JSONResponse

from apps.api.errors import (
    InvalidImagePayloadError,
    PipelineExecutionError,
)
from apps.api.schemas import InspectionResponse
from apps.api.services.pipeline_orchestrator import pipeline_orchestrator

logger = logging.getLogger("metrolens.routes.inspect")

router = APIRouter(prefix="/api/v1", tags=["Inspection"])


@router.post(
    "/inspect",
    response_model=InspectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload packaging photograph for synchronous legal metrology inspection",
    description=(
        "Executes multi-stage image ingestion security, metric scale calibration, "
        "multilingual OCR token recognition, entity normalization, and master statutory "
        "rules evaluation under the Legal Metrology (Packaged Commodities) Rules, 2011."
    ),
)
async def inspect_packaging(
    file: UploadFile = File(..., description="Packaging photograph (JPEG, PNG, or WebP; max 15MB)"),
    anchor_type: Optional[str] = Form(
        "INR_10_COIN",
        description="Fiducial reference calibration anchor ('INR_10_COIN', 'ISO_CARD', 'NONE')",
    ),
    panel_type: Optional[str] = Form(
        "FRONT_PDP",
        description="Packaging panel classification ('FRONT_PDP', 'BACK_INFO', 'ALL_IN_ONE')",
    ),
    officer_id: Optional[str] = Form(
        "WEB-GUEST",
        description="Inspecting officer identifier or test session tag",
    ),
    mock_fixture_key: Optional[str] = Form(
        None,
        description="Optional fixture identifier for offline deterministic test evaluation",
    ),
    x_request_id: Optional[str] = Header(
        None,
        alias="X-Request-ID",
        description="Client tracing correlation UUID",
    ),
) -> InspectionResponse:
    """
    Synchronous packaging compliance inspection endpoint.
    Guarantees sub-2.5 second latency on standard CPU hardware.
    """
    if not file:
        raise InvalidImagePayloadError("Missing required 'file' multipart form field.")

    filename = file.filename or "upload.jpg"
    logger.info(
        "Received inspection request: file='%s', anchor='%s', panel='%s', officer='%s', req_id='%s'",
        filename,
        anchor_type,
        panel_type,
        officer_id,
        x_request_id,
    )

    # Read binary stream
    try:
        content = await file.read()
    except Exception as e:
        logger.error("Failed to read uploaded file stream: %s", e)
        raise InvalidImagePayloadError(f"Could not read upload stream: {e}")

    if not content or len(content) == 0:
        raise InvalidImagePayloadError("Uploaded file payload is empty (0 bytes).")

    # Delegate to pipeline orchestrator
    response = pipeline_orchestrator.orchestrate_inspection(
        image_bytes=content,
        filename=filename,
        anchor_type=anchor_type or "INR_10_COIN",
        panel_type=panel_type or "FRONT_PDP",
        officer_id=officer_id or "WEB-GUEST",
        mock_fixture_key=mock_fixture_key,
    )

    return response
