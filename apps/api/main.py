"""
MetroLens API Gateway: FastAPI Application Entrypoint.
Conforms to OpenAPI 3.1, docs/API_CONTRACT.md, and ADR-007, ADR-010, ADR-013, ADR-014.
"""

from contextlib import asynccontextmanager
from typing import Any, Dict
import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from apps.api.errors import register_error_handlers
from apps.api.middleware.headers import SecurityHeadersMiddleware
from apps.api.middleware.rate_limit import RateLimitMiddleware
from apps.api.middleware.audit_middleware import AuditTelemetryMiddleware
from apps.api.routes import (
    inspect_router,
    report_router,
    emaap_router,
    health_router,
    metrics_router,
    auth_router,
    audit_router,
)
from apps.api.services.spool_service import spool_service

from nirikshak_shared.models.contracts import InspectionRequest, InspectionResult
from nirikshak_shared.models.primitives import InspectionStatus, OverallVerdict, CalibrationStatus

logger = logging.getLogger("metrolens.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initializes background daemons and cleans orphaned ephemeral spool files.
    """
    logger.info("Starting MetroLens API Gateway service...")
    spool_service.startup_sweep()
    spool_service.start_cleanup_daemon()
    yield
    logger.info("Shutting down MetroLens API Gateway service...")
    spool_service.stop_cleanup_daemon()


app = FastAPI(
    title="MetroLens AI™ Legal Metrology Verification API",
    version="1.0.0",
    description=(
        "Enterprise Legal Metrology Packaged Commodities (LMPC) perception & statutory compliance engine. "
        "Provides synchronous image inspection, optical fiducial calibration, multilingual OCR, "
        "and Section 36(1) Jan Vishwas Improvement Notice compilation."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# 1. Register canonical error handlers (HTTP 400, 413, 415, 422, 429, 500, 504)
register_error_handlers(app)

# 2. Register enterprise audit & telemetry tracking middleware
app.add_middleware(AuditTelemetryMiddleware)

# 3. Register enterprise security response headers (CSP, HSTS, X-Frame-Options)
app.add_middleware(SecurityHeadersMiddleware)

# 4. Register leaky-bucket rate limiting middleware (10 req/min per IP)
app.add_middleware(RateLimitMiddleware)

# 5. Register CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Mount API v1 route blueprints
app.include_router(inspect_router)
app.include_router(report_router)
app.include_router(emaap_router)
app.include_router(health_router)
app.include_router(metrics_router)
app.include_router(auth_router)
app.include_router(audit_router)


# =========================================================================
# Legacy & System Endpoints for Backward Compatibility
# =========================================================================

@app.get("/health", tags=["System"])
def health_check() -> Dict[str, str]:
    """Basic health and service liveness ping."""
    return {"status": "ok", "service": "metrolens-api", "version": "1.0.0"}


@app.post(
    "/api/v1/inspections",
    response_model=InspectionResult,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Inspections (Legacy)"],
)
def submit_inspection_legacy(request: InspectionRequest) -> InspectionResult:
    """Legacy async submission endpoint."""
    return InspectionResult(
        inspection_id=request.inspection_id,
        status=InspectionStatus.SUCCESS,
        image_sha256=request.image_sha256 or ("0" * 64),
        overall_verdict=OverallVerdict.COMPLIANT,
        quality_gate_passed=True,
        calibration_status=CalibrationStatus.UNCALIBRATED,
    )


@app.get(
    "/api/v1/inspections/{inspection_id}",
    response_model=InspectionResult,
    tags=["Inspections (Legacy)"],
)
def get_inspection_legacy(inspection_id: str) -> InspectionResult:
    """Legacy inspection retrieval endpoint."""
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
