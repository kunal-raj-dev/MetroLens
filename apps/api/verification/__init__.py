"""
MetroLens AI - Statutory Packaging Verification Package
======================================================
Provides comprehensive statutory verification engines conforming to
the Second Schedule, Third Schedule, Fourth Schedule, and Fifth Schedule
of the Legal Metrology (Packaged Commodities) Rules, 2011.
"""

from .standard_quantities import (
    StandardQuantitiesValidator,
    StandardQuantityRule,
    StandardQuantityResult,
    CommodityStandardSpec,
)
from .font_geometry import (
    FontGeometryAnalyzer,
    FontGeometryMetrics,
    NumeralGeometryAuditResult,
)

__all__ = [
    "StandardQuantitiesValidator",
    "StandardQuantityRule",
    "StandardQuantityResult",
    "CommodityStandardSpec",
    "FontGeometryAnalyzer",
    "FontGeometryMetrics",
    "NumeralGeometryAuditResult",
]
