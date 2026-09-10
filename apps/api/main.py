"""MetroLens MVP API: authenticated access to bounded inspection sessions."""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from apps.api.auth.dependencies import ServicePrincipal, require_api_access
from apps.api.errors import register_error_handlers
from apps.api.middleware.audit_middleware import AuditTelemetryMiddleware
from apps.api.middleware.body_limit import BodyLimitMiddleware
from apps.api.middleware.headers import SecurityHeadersMiddleware
from apps.api.middleware.rate_limit import RateLimitMiddleware, rate_limiter
from apps.api.routes import (
    inspect_router, report_router, health_router, metrics_router, auth_router, audit_router,
)
from apps.api.schemas import InspectionResponse
from apps.api.services.inspection_store import require_inspection
from apps.api.services.spool_service import spool_service

logger = logging.getLogger("metrolens.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Never discard retained evidence merely because a server process restarts.
    spool_service.start_cleanup_daemon()
    yield
    spool_service.stop_cleanup_daemon()


app = FastAPI(
    title="MetroLens Packaging Screening API", version="1.0.0",
    docs_url=None, redoc_url=None,
    description="Preliminary image-based screening. Officer identity and statutory certification are not implemented.",
    lifespan=lifespan,
)
register_error_handlers(app)


@app.exception_handler(Exception)
async def internal_error_handler(request, exc):
    logger.error("API request failed", exc_info=(type(exc), exc, exc.__traceback__))
    return JSONResponse(status_code=500, content={"detail": "Inspection service failed. Please contact the administrator."})


app.add_middleware(BodyLimitMiddleware)
app.add_middleware(AuditTelemetryMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, rate_limiter=rate_limiter)

default_origins = "https://metrolens.netlify.app,http://localhost:3000,http://127.0.0.1:3000"
origins = [value.strip() for value in os.environ.get("METROLENS_CORS_ORIGINS", default_origins).split(",") if value.strip()]
if any(origin == "*" for origin in origins):
    raise ValueError("METROLENS_CORS_ORIGINS must list explicit trusted origins.")
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["Content-Disposition", "Retry-After"],
)

app.include_router(inspect_router)
app.include_router(report_router)
app.include_router(health_router)
app.include_router(metrics_router)
app.include_router(auth_router)
app.include_router(audit_router)


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": "metrolens-api"}


@app.post("/api/v1/inspections", tags=["Inspections"], dependencies=[Depends(require_api_access)])
def submit_inspection():
    raise HTTPException(501, "Structured inspection creation is unavailable. Submit an image to /api/v1/inspect.")


@app.get("/api/v1/inspections/{inspection_id}", response_model=InspectionResponse, tags=["Inspections"])
def get_inspection(inspection_id: str, principal: ServicePrincipal = Depends(require_api_access)):
    return require_inspection(inspection_id, principal.subject).response


@app.post("/api/v1/emaap/mock-sync", dependencies=[Depends(require_api_access)], tags=["Integrations"])
def unavailable_emaap_sync():
    raise HTTPException(501, "Government portal synchronization is not implemented.")


submit_inspection_legacy = submit_inspection
get_inspection_legacy = get_inspection
