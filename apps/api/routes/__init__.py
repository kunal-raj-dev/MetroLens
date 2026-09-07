"""
MetroLens API Gateway: Route Modules.
"""

from .inspect import router as inspect_router
from .report import router as report_router
from .emaap import router as emaap_router
from .health import router as health_router
from .metrics import router as metrics_router
from .auth import router as auth_router
from .audit import router as audit_router

__all__ = [
    "inspect_router",
    "report_router",
    "emaap_router",
    "health_router",
    "metrics_router",
    "auth_router",
    "audit_router",
]
