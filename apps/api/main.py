"""
Nirikshak API Service: FastAPI application entrypoint.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from nirikshak_shared.models.contracts import InspectionRequest, InspectionResult
from nirikshak_shared.models.primitives import InspectionStatus, OverallVerdict, CalibrationStatus

app = FastAPI(
    title="Nirikshak Legal Metrology Inspection API",
    version="0.1.0",
    description="Automated, auditable legal metrology verification API conforming to Packaged Commodities Rules, 2011.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
def health_check() -> Dict[str, str]:
    """Health and readiness check endpoint."""
    return {"status": "ok", "service": "nirikshak-api", "version": "0.1.0"}


@app.post(
    "/api/v1/inspections",
    response_model=InspectionResult,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Inspections"],
)
def submit_inspection(request: InspectionRequest) -> InspectionResult:
    """
    Submits a new packaging frame for automated inspection.
    In development scaffold, returns an initialized InspectionResult.
    """
    return InspectionResult(
        inspection_id=request.inspection_id,
        status=InspectionStatus.SUCCESS,
        image_sha256=request.image_sha256 or ("0" * 64),
        overall_verdict=OverallVerdict.COMPLIANT,
        quality_gate_passed=True,
        calibration_status=CalibrationStatus.UNCALIBRATED,
    )


@app.get("/api/v1/inspections/{inspection_id}", response_model=InspectionResult, tags=["Inspections"])
def get_inspection(inspection_id: str) -> InspectionResult:
    """Retrieves current inspection state and evidence graph."""
    if not inspection_id:
        raise HTTPException(status_code=404, detail="Inspection ID not found")
    return InspectionResult(
        inspection_id=inspection_id,
        status=InspectionStatus.SUCCESS,
        image_sha256="0" * 64,
        overall_verdict=OverallVerdict.COMPLIANT,
        quality_gate_passed=True,
        calibration_status=CalibrationStatus.UNCALIBRATED,
    )
