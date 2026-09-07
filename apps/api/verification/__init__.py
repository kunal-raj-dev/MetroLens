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
from .geometric_unwrapping import (
    GeometricUnwrapper,
    CylinderParameters,
    ConicalParameters,
    UnwrapResult,
    SurfaceType,
    InterpolationMethod,
    RectificationMetrics,
)
from .stroke_profile import (
    StrokeProfiler,
    StrokeVerdict,
    Rule7ComplianceReport,
    GlyphMeasurement,
    TextLineProfile,
)
from .barcode_verifier import (
    BarcodeVerifier,
    BarcodeVerificationResult,
    ISO15416Parameters,
    ISOGrade,
    SymbologyType,
    DeclarationDiscrepancy,
    GS1ParsedData,
)

__all__ = [
    "StandardQuantitiesValidator",
    "StandardQuantityRule",
    "StandardQuantityResult",
    "CommodityStandardSpec",
    "FontGeometryAnalyzer",
    "FontGeometryMetrics",
    "NumeralGeometryAuditResult",
    "GeometricUnwrapper",
    "CylinderParameters",
    "ConicalParameters",
    "UnwrapResult",
    "SurfaceType",
    "InterpolationMethod",
    "RectificationMetrics",
    "StrokeProfiler",
    "StrokeVerdict",
    "Rule7ComplianceReport",
    "GlyphMeasurement",
    "TextLineProfile",
    "BarcodeVerifier",
    "BarcodeVerificationResult",
    "ISO15416Parameters",
    "ISOGrade",
    "SymbologyType",
    "DeclarationDiscrepancy",
    "GS1ParsedData",
]

