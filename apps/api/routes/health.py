"""Public liveness only; this does not assert OCR or legal-rule readiness."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health")
def get_service_health():
    return {"status": "ok", "service": "metrolens-api"}
