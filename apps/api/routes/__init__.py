"""
MetroLens API Gateway: Route Modules.
"""

from .inspect import router as inspect_router
from .report import router as report_router
from .emaap import router as emaap_router
from .health import router as health_router

__all__ = [
    "inspect_router",
    "report_router",
    "emaap_router",
    "health_router",
]
