"""
Nirikshak Rules Engine: Canonical Data Schemas & Statutory Compliance Contracts.
Conforms strictly to docs/API_CONTRACT.md, docs/team/INTEGRATION_CHECKLIST.md,
and the Legal Metrology (Packaged Commodities) Rules, 2011 (incorporating
the Jan Vishwas (Amendment of Provisions) Act, 2026).
"""

from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict
import math


class ComplianceState(str, Enum):
    """
    Standardized statutory compliance states.
    Conforms strictly to docs/API_CONTRACT.md Section 5.
    """
    GREEN = "NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED"
    RED = "POTENTIAL_NON_COMPLIANCE"
    AMBER = "MANUAL_REVIEW_REQUIRED"
    BLUE = "STATUTORY_EXEMPTION_APPLIED"
    GRAY = "NOT_IMAGE_VERIFIABLE"

    # Semantic 5-State taxonomy aliases
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    DEVIATION_DETECTED = "DEVIATION_DETECTED"
    UNCERTAIN = "UNCERTAIN"
    EXEMPTED = "EXEMPTED"


class VerdictBadgeColor(str, Enum):
    """Badge color corresponding to compliance state for UI rendering."""
    GREEN = "green"
    RED = "red"
    AMBER = "amber"
    BLUE = "blue"
    GRAY = "gray"


class UnitType(str, Enum):
    """Statutory standard units of weight, measure, length, area, and count."""
    GRAM = "g"
    KILOGRAM = "kg"
    MILLILITER = "ml"
    LITER = "l"
    METER = "m"
    CENTIMETER = "cm"
    NUMBER = "N"
    PIECE = "piece"

    @classmethod
    def from_string(cls, val: str) -> Optional["UnitType"]:
        """Normalizes common string units to canonical UnitType, returning None if non-standard."""
        if not val:
            return None
        cleaned = val.strip().lower()
        mapping = {
            "g": cls.GRAM,
            "gm": cls.GRAM,
            "gms": cls.GRAM,
            "gram": cls.GRAM,
            "grams": cls.GRAM,
            "kg": cls.KILOGRAM,
            "kgs": cls.KILOGRAM,
            "kilogram": cls.KILOGRAM,
            "kilograms": cls.KILOGRAM,
            "ml": cls.MILLILITER,
            "milliliter": cls.MILLILITER,
            "millilitres": cls.MILLILITER,
            "l": cls.LITER,
            "ltr": cls.LITER,
            "litre": cls.LITER,
            "litres": cls.LITER,
            "m": cls.METER,
            "metre": cls.METER,
            "meter": cls.METER,
            "cm": cls.CENTIMETER,
            "centimetre": cls.CENTIMETER,
            "centimeter": cls.CENTIMETER,
            "n": cls.NUMBER,
            "no": cls.NUMBER,
            "number": cls.NUMBER,
            "piece": cls.PIECE,
            "pc": cls.PIECE,
            "pcs": cls.PIECE,
            "units": cls.PIECE,
            "unit": cls.PIECE,
        }
        return mapping.get(cleaned)


class ScriptType(str, Enum):
    """Language script classification for extracted tokens."""
    LATIN = "latin"
    DEVANAGARI = "devanagari"
    UNKNOWN = "unknown"


class OCRToken(BaseModel):
    """
    Atomic text token extracted from optical detection.
    Matches contract schema in docs/team/INTEGRATION_CHECKLIST.md Handoff 2.
    """
    token_id: str = Field(..., description="Unique token identifier (e.g., 'tok_001')")
    text: str = Field(..., description="Transcribed character sequence")
    confidence: float = Field(..., ge=0.0, le=1.0, description="OCR confidence score")
    polygon: Optional[List[List[float]]] = Field(
        None, description="Clockwise 4-point quad [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]"
    )
    bbox: List[float] = Field(..., description="[xmin, ymin, xmax, ymax] in pixel coordinates")
    script: ScriptType = Field(default=ScriptType.UNKNOWN, description="Script type")
    line_id: int = Field(default=0, description="Reading order line index")
    raw_pixel_height: Optional[float] = Field(
        default=None, description="Raw pixel height (geometry only, not legal font height)"
    )
    char_height_px: Optional[float] = Field(
        default=None, description="Measured character stroke pixel height"
    )
    model_name: str = Field(default="", description="Name of OCR model")


class MetricScaleResult(BaseModel):
    """
    Optical metric scale and physical dimensions from Member 2 (CV/Calibration).
    Matches contract schema in docs/team/INTEGRATION_CHECKLIST.md Handoff 3.
    """
    is_calibrated: bool = Field(default=False, description="Whether metric calibration target was detected")
    scale_factor_mm_per_px: Optional[float] = Field(
        default=None, description="Millimeters per pixel optical scale factor"
    )
    pdp_area_sqcm: Optional[float] = Field(
        default=None, description="Computed Principal Display Panel area in square centimeters"
    )
    anchor_type_detected: Optional[str] = Field(
        default="none", description="Calibration anchor detected: 'coin_10rs', 'iso_card', or 'none'"
    )
    tilt_angle_deg: Optional[float] = Field(
        default=None, description="Estimated surface tilt angle in degrees"
    )
    is_cylindrical: bool = Field(
        default=False, description="Whether package is cylindrical/curved"
    )


class CanonicalDeclaration(BaseModel):
    """
    Normalized statutory declarations parsed from raw OCR observations.
    Conforms strictly to docs/API_CONTRACT.md Section 5 lines 319-334.
    """
    commodity_name: Optional[str] = Field(None, description="Generic commodity name under Rule 6(1)(b)")
    mrp_inr: Optional[float] = Field(None, description="Maximum Retail Price in INR under Rule 6(1)(e)")
    tax_qualifier_present: bool = Field(
        default=False, description="Whether 'inclusive of all taxes' or equivalent qualifier is present"
    )
    net_quantity_value: Optional[float] = Field(None, description="Numeric magnitude of net quantity")
    net_quantity_unit: Optional[UnitType] = Field(None, description="Canonical standard unit under Rule 6(1)(c)")
    raw_net_quantity_unit: Optional[str] = Field(None, description="Raw verbatim unit token extracted before normalization")
    has_non_standard_unit: bool = Field(
        default=False, description="Whether a non-standard or prohibited unit (e.g. Gms, ML) was detected"
    )
    declared_usp_value: Optional[float] = Field(None, description="Declared Unit Sale Price under Rule 6(11)")
    declared_usp_unit: Optional[str] = Field(None, description="Declared unit symbol for USP (e.g., 'g', 'kg', 'ml')")
    mfg_month: Optional[int] = Field(None, ge=1, le=12, description="Manufacturing month (1-12) under Rule 6(1)(d)")
    mfg_year: Optional[int] = Field(None, ge=1990, le=2050, description="Manufacturing year (YYYY) under Rule 6(1)(d)")
    manufacturer_name: Optional[str] = Field(None, description="Manufacturer/packer/importer name under Rule 6(1)(a)")
    manufacturer_pincode: Optional[str] = Field(None, description="Postal pincode extracted from address")
    manufacturer_address: Optional[str] = Field(None, description="Full or partial street address")
    consumer_care_email: Optional[str] = Field(None, description="Grievance email under Rule 6(1)(g)")
    consumer_care_phone: Optional[str] = Field(None, description="Grievance telephone or toll-free number")
    country_of_origin: Optional[str] = Field(None, description="Country of origin under Rule 6(1)(aa)")
    is_pan_masala_or_tobacco: bool = Field(
        default=False, description="Whether commodity is pan masala or tobacco (non-exempt per G.S.R. 881(E))"
    )
    is_wholesale_or_bulk: bool = Field(
        default=False, description="Whether commodity is wholesale bulk (>25kg or >25L per Rule 3)"
    )

    model_config = ConfigDict(extra="ignore")


class RuleEvaluationRecord(BaseModel):
    """
    Deterministic evaluation record for a single statutory rule.
    Matches docs/team/INTEGRATION_CHECKLIST.md.
    """
    rule_id: str = Field(..., description="Statutory rule identifier (e.g., 'LMPC-R06-MRP-001')")
    rule_title: str = Field(..., description="Human-readable rule title")
    statutory_reference: str = Field(..., description="Exact statutory clause (e.g., 'Rule 6(1)(e)')")
    status: str = Field(..., description="'PASS' | 'FAIL' | 'REVIEW' | 'NOT_APPLICABLE'")
    is_compliant: bool = Field(..., description="Boolean compliance indicator")
    observed_value: Any = Field(default=None, description="Observed declaration or measurement")
    required_value: Any = Field(default=None, description="Statutory threshold or requirement")
    deficit_mm: Optional[float] = Field(default=None, description="Font height deficit in mm if applicable")
    statutory_citation: str = Field(..., description="Gazette notification or statute citation")
    notes: Optional[str] = Field(default=None, description="Detailed explanatory notes or error reasons")
    benefit_of_doubt_applied: bool = Field(
        default=False, description="Whether benefit-of-doubt tolerance buffer was applied"
    )


class EvidenceCropMetadata(BaseModel):
    """
    Metadata and crop bounding box for a visual evidence item.
    Matches docs/API_CONTRACT.md EvidenceCrop and INTEGRATION_CHECKLIST.md.
    """
    field_name: str = Field(..., description="Declaration field name (e.g., 'net_quantity')")
    label: str = Field(..., description="Human-readable label (e.g., 'Net Quantity Declaration')")
    bbox_px: List[int] = Field(..., description="Bounding box [x, y, width, height] in image pixels")
    measured_height_mm: Optional[float] = Field(None, description="Calibrated height in millimeters")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Extraction confidence score")
    crop_base64: str = Field(default="", description="Base64 encoded image thumbnail")


class ImprovementNoticePayload(BaseModel):
    """
    Section 36(1) Improvement Notice data structure.
    Conforms strictly to Jan Vishwas (Amendment of Provisions) Act, 2026.
    """
    recommended: bool = Field(default=False, description="Whether an Improvement Notice is recommended")
    act_provision: str = Field(
        default="Section 36(1) read with Jan Vishwas (Amendment of Provisions) Act, 2026",
        description="Governing statutory enactment citation"
    )
    cure_period_days: int = Field(default=15, description="Statutory rectification cure period (15 days)")
    statutory_grounds: str = Field(default="", description="Summary of non-compliance grounds")
    compounding_authority: str = Field(
        default="Legal Metrology Compounding Officer",
        description="Designated statutory authority"
    )
    notice_title: Optional[str] = Field(
        default="STATUTORY IMPROVEMENT NOTICE", description="Formal title of statutory notice"
    )
    notice_text: Optional[str] = Field(default=None, description="Draft notice body text for PDF rendering")
    itemized_violations: Optional[List[str]] = Field(
        default=None, description="List of itemized statutory grounds"
    )
    addressed_to: Optional[str] = Field(
        default=None, description="Target manufacturer/packer entity"
    )

    model_config = ConfigDict(extra="ignore")



class ComplianceEvaluationResult(BaseModel):
    """
    Master compliance evaluation result object.
    Matches contract schema in docs/team/INTEGRATION_CHECKLIST.md Handoff 4
    and response schema in docs/API_CONTRACT.md.
    """
    inspection_id: str = Field(..., description="Globally unique inspection identifier")
    timestamp_utc: str = Field(..., description="ISO 8601 UTC timestamp")
    overall_verdict: str = Field(
        ...,
        description="'COMPLIANT' | 'NON_COMPLIANT' | 'DEVIATION_DETECTED' | 'UNCERTAIN' | 'EXEMPTED'"
    )
    verdict_badge_color: str = Field(
        ...,
        description="'green' | 'red' | 'amber' | 'blue' | 'gray'"
    )
    primary_legal_summary: str = Field(..., description="Executive statutory summary of the inspection outcome")
    rule_evaluations: List[RuleEvaluationRecord] = Field(
        default_factory=list, description="List of granular rule evaluation outcomes"
    )
    declarations: CanonicalDeclaration = Field(
        default_factory=CanonicalDeclaration, description="Parsed canonical entities"
    )
    calibrated_measurements: Optional[MetricScaleResult] = Field(
        default=None, description="Optical calibration results"
    )
    evidence_crops: List[EvidenceCropMetadata] = Field(
        default_factory=list, description="Crops of verified declaration regions"
    )
    improvement_notice: Optional[ImprovementNoticePayload] = Field(
        default=None, description="Section 36(1) Improvement Notice payload if non-compliant"
    )
    sha256_hash: str = Field(default="", description="Cryptographic SHA-256 hash of input image")
    pdf_report_url: str = Field(default="", description="Download URL for signed assessment dossier")
    telemetry_ms: float = Field(default=0.0, description="Rule evaluation duration in milliseconds")

    model_config = ConfigDict(extra="ignore")
