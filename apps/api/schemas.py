"""
MetroLens API Gateway: Pydantic Schema Specifications (v1.0).
Strictly conforms to docs/API_CONTRACT.md and ADR-007, ADR-010, ADR-013, ADR-014.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class AnchorType(str, Enum):
    """Supported fiducial calibration anchor types."""
    INR_10_COIN = "INR_10_COIN"
    ISO_CARD = "ISO_CARD"
    NONE = "NONE"


class PanelType(str, Enum):
    """Packaging display panel classification."""
    FRONT_PDP = "FRONT_PDP"
    BACK_INFO = "BACK_INFO"
    ALL_IN_ONE = "ALL_IN_ONE"


class OverallComplianceState(str, Enum):
    """5-State statutory compliance taxonomy."""
    COMPLIANT = "COMPLIANT"
    POTENTIAL_NON_COMPLIANCE = "POTENTIAL_NON_COMPLIANCE"
    NON_COMPLIANT = "NON_COMPLIANT"
    EXEMPTED = "EXEMPTED"
    FLAGGED_FOR_REVIEW = "FLAGGED_FOR_REVIEW"


class ImageMetadata(BaseModel):
    """Forensic metadata and quality assessment metrics of the uploaded packaging photograph."""
    model_config = ConfigDict(extra="ignore")

    filename: str = Field(..., description="Original filename of uploaded asset")
    width_px: int = Field(..., description="Image horizontal width in pixels")
    height_px: int = Field(..., description="Image vertical height in pixels")
    sha256_hash: str = Field(..., min_length=64, max_length=64, description="Cryptographic SHA-256 digest of clean raw image")
    is_quality_valid: bool = Field(..., description="Whether image satisfies pre-flight blur and glare quality thresholds")
    blur_score: float = Field(..., description="Laplacian variance sharpness score")
    glare_percentage: float = Field(..., description="Percentage of pixels exhibiting specular glare (luminance >= 250)")


class CalibrationInfo(BaseModel):
    """Optical calibration and metric scale factor outcomes."""
    model_config = ConfigDict(extra="ignore")

    is_calibrated: bool = Field(..., description="Whether reliable optical metric calibration was achieved")
    anchor_type: str = Field(..., description="Reference fiducial anchor type evaluated")
    coin_detected: bool = Field(..., description="Whether the requested calibration reference was successfully located")
    scale_mm_per_px: Optional[float] = Field(None, description="Computed metric scale conversion factor in mm/pixel")
    pdp_width_mm: Optional[float] = Field(None, description="Principal Display Panel physical width in millimeters")
    pdp_height_mm: Optional[float] = Field(None, description="Principal Display Panel physical height in millimeters")
    pdp_area_cm2: Optional[float] = Field(None, description="Principal Display Panel area in square centimeters")
    calibration_confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score of anchor contour detection")


class DeclarationsInfo(BaseModel):
    """Normalized mandatory statutory declarations extracted from packaging label."""
    model_config = ConfigDict(extra="ignore")

    commodity_name: Optional[str] = Field(None, description="Generic or specific commodity identity")
    mrp_inr: Optional[float] = Field(None, description="Maximum Retail Price in Indian Rupees")
    tax_qualifier_present: bool = Field(False, description="Presence of statutory qualifier 'inclusive of all taxes'")
    net_quantity_value: Optional[float] = Field(None, description="Net quantity declared magnitude")
    net_quantity_unit: Optional[str] = Field(None, description="Standardized net quantity unit symbol (e.g., 'g', 'kg', 'ml', 'l')")
    declared_usp_value: Optional[float] = Field(None, description="Declared Unit Sale Price in INR")
    declared_usp_unit: Optional[str] = Field(None, description="Unit denominator of declared USP (e.g., 'g', 'kg')")
    mfg_month: Optional[int] = Field(None, ge=1, le=12, description="Month of manufacture or packing")
    mfg_year: Optional[int] = Field(None, ge=2000, le=2100, description="Year of manufacture or packing")
    manufacturer_name: Optional[str] = Field(None, description="Name and address of manufacturer or packer")
    manufacturer_pincode: Optional[str] = Field(None, description="6-digit postal code of manufacturer premise")
    consumer_care_email: Optional[str] = Field(None, description="Grievance redressal email address")
    consumer_care_phone: Optional[str] = Field(None, description="Grievance redressal telephone or toll-free helpline")
    country_of_origin: Optional[str] = Field(None, description="Country of origin / manufacture")


class Rule6MandatoryDetails(BaseModel):
    """Itemized evaluation of mandatory declarations under Rule 6(1)."""
    model_config = ConfigDict(extra="ignore")

    manufacturer_details: str = Field(..., description="'PASS' | 'FAIL' | 'REVIEW'")
    net_quantity: str = Field(..., description="'PASS' | 'FAIL' | 'REVIEW'")
    mrp: str = Field(..., description="'PASS' | 'FAIL' | 'REVIEW'")
    usp: str = Field(..., description="'PASS' | 'FAIL' | 'REVIEW'")
    mfg_date: str = Field(..., description="'PASS' | 'FAIL' | 'REVIEW'")
    consumer_care: str = Field(..., description="'PASS' | 'FAIL' | 'REVIEW'")


class Rule6MandatoryStatus(BaseModel):
    """Aggregate status of Rule 6(1) mandatory packaging declarations."""
    model_config = ConfigDict(extra="ignore")

    overall_status: str = Field(..., description="'PASS' | 'FAIL'")
    missing_declarations: List[str] = Field(default_factory=list, description="List of omitted mandatory statutory fields")
    details: Dict[str, str] = Field(default_factory=dict, description="Detailed field-level verdicts")


class USPAudit(BaseModel):
    """Audit outcome of Rule 6(11) Unit Sale Price computation and standard unit denominator."""
    model_config = ConfigDict(extra="ignore")

    is_compliant: bool = Field(..., description="Whether USP satisfies statutory arithmetic and denominator rules")
    declared_usp: Optional[float] = Field(None, description="Observed declared USP value")
    expected_usp: Optional[float] = Field(None, description="Statutorily recalculated USP value using standard rounding")
    discrepancy_pct: Optional[float] = Field(None, description="Percentage discrepancy between declared and expected USP")
    standard_denominator: Optional[str] = Field(None, description="Mandatory statutory denominator ('g', 'kg', 'ml', 'l')")
    notes: Optional[str] = Field(None, description="Detailed legal metrology compliance notes")


class FontHeightAudit(BaseModel):
    """Audit outcome of Rule 7 Tables I & II minimum numeral height compliance."""
    model_config = ConfigDict(extra="ignore")

    is_compliant: bool = Field(..., description="Whether font height meets or exceeds statutory threshold")
    pdp_area_cm2: Optional[float] = Field(None, description="Principal display panel area used for table lookup")
    statutory_min_height_mm: Optional[float] = Field(None, description="Minimum mandatory numeral height from Table-I")
    measured_net_qty_height_mm: Optional[float] = Field(None, description="Observed numeral height in millimeters")
    deficit_mm: Optional[float] = Field(None, description="Height deficit below statutory threshold if non-compliant")
    benefit_of_doubt_applied: bool = Field(False, description="Whether 0.10mm measurement tolerance buffer was granted")


class ExemptionStatus(BaseModel):
    """Evaluation of statutory exemptions under Rule 26 or Rule 3."""
    model_config = ConfigDict(extra="ignore")

    is_exempt: bool = Field(False, description="Whether package qualifies for statutory exemption")
    statutory_clause: Optional[str] = Field(None, description="Specific exemption clause (e.g. 'Rule 26(a)', 'Rule 3(1)')")


class RuleEvaluationsGroup(BaseModel):
    """Composite group of statutory rule evaluation modules matching API Contract."""
    model_config = ConfigDict(extra="ignore")

    rule6_mandatory_status: Rule6MandatoryStatus = Field(..., description="Rule 6(1) mandatory completeness audit")
    usp_audit: USPAudit = Field(..., description="Rule 6(11) Unit Sale Price audit")
    font_height_audit: FontHeightAudit = Field(..., description="Rule 7 Tables I & II font height audit")
    exemption_status: ExemptionStatus = Field(..., description="Rule 26 / Rule 3 exemption evaluation")


class ImprovementNoticeInfo(BaseModel):
    """Section 36(1) Statutory Improvement Notice under Jan Vishwas Act, 2026."""
    model_config = ConfigDict(extra="ignore")

    recommended: bool = Field(..., description="Whether issuance of an improvement notice is recommended")
    act_provision: str = Field(..., description="Statutory provision under Jan Vishwas Act")
    cure_period_days: int = Field(default=15, description="Mandatory statutory cure period in days")
    statutory_grounds: str = Field(..., description="Articulated legal grounds and itemized contraventions")


class EvidenceCrop(BaseModel):
    """Visual forensic evidence crop bounding box and base64 thumbnail."""
    model_config = ConfigDict(extra="ignore")

    field_name: str = Field(..., description="Declaration field identifier (e.g., 'mrp', 'net_quantity', 'usp')")
    label: str = Field(..., description="Human-readable evidence description")
    bbox_px: List[int] = Field(..., description="Bounding box [x, y, width, height] in pixel coordinates")
    measured_height_mm: Optional[float] = Field(None, description="Calibrated height in millimeters")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Extraction confidence score")
    crop_base64: str = Field(..., description="Base64 encoded data URI (e.g., 'data:image/jpeg;base64,...')")


class TelemetryStages(BaseModel):
    """Per-stage execution latency breakdown in milliseconds."""
    model_config = ConfigDict(extra="ignore")

    quality_gate: float = Field(..., description="Image quality gate duration in ms")
    metric_calibration: float = Field(..., description="Metric scale fiducial detection duration in ms")
    ocr_perception: float = Field(..., description="Multilingual OCR recognition duration in ms")
    normalization: float = Field(..., description="Token normalization and entity parsing duration in ms")
    rule_engine: float = Field(..., description="Statutory rules state machine evaluation duration in ms")
    evidence_packaging: float = Field(..., description="Evidence cropping and base64 serialization duration in ms")


class TelemetryInfo(BaseModel):
    """Execution latency and performance metrics."""
    model_config = ConfigDict(extra="ignore")

    total_duration_ms: float = Field(..., description="End-to-end processing latency in milliseconds")
    stages_ms: TelemetryStages = Field(..., description="Granular per-stage latency breakdown")


class InspectionResponse(BaseModel):
    """
    Authoritative synchronous inspection response dossier.
    Conforms strictly to docs/API_CONTRACT.md Section 3.1.
    """
    model_config = ConfigDict(extra="ignore")

    inspection_id: str = Field(..., description="Unique inspection identifier (e.g., 'INSP-20260905-8741')")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp of inspection completion")
    state: str = Field(..., description="5-State overall compliance outcome")
    summary_reason: str = Field(..., description="Authoritative statutory summary of inspection outcome")
    image_metadata: ImageMetadata = Field(..., description="Forensic metadata and quality scores")
    calibration: CalibrationInfo = Field(..., description="Metric scale calibration parameters")
    declarations: DeclarationsInfo = Field(..., description="Extracted canonical packaging declarations")
    rule_evaluations: RuleEvaluationsGroup = Field(..., description="Statutory rule evaluation outcomes")
    improvement_notice: Optional[ImprovementNoticeInfo] = Field(None, description="Jan Vishwas improvement notice if non-compliant")
    evidence_crops: List[EvidenceCrop] = Field(default_factory=list, description="Visual evidence crops for UI rendering")
    telemetry: TelemetryInfo = Field(..., description="Latency telemetry breakdown")


# =========================================================================
# Auxiliary Endpoint Contracts
# =========================================================================

class SystemMetrics(BaseModel):
    """Live system CPU and memory resource consumption."""
    cpu_percent: float = Field(..., description="Host CPU utilization percentage")
    memory_used_mb: float = Field(..., description="Resident memory utilized in megabytes")
    memory_total_mb: float = Field(..., description="Total system RAM in megabytes")


class ModelStatus(BaseModel):
    """Readiness status of embedded inference models."""
    paddleocr_onnx_det: str = Field("loaded_cpu_int8", description="OCR detection model status")
    paddleocr_onnx_rec: str = Field("loaded_cpu_int8", description="OCR recognition model status")
    scale_calibrator: str = Field("ready", description="Calibration subsystem status")


class RulesEngineStatus(BaseModel):
    """Rules engine versioning and verified rule set."""
    status: str = Field("active", description="Rules engine operational state")
    ruleset_version: str = Field("2026.09-JanVishwas-v1.0", description="Active statutory ruleset tag")
    verified_rules_count: int = Field(4, description="Number of verified statutory rules active")


class HealthResponse(BaseModel):
    """GET /api/v1/health readiness probe schema matching API Contract 3.2."""
    status: str = Field("healthy", description="Application health status")
    version: str = Field("1.0.0", description="API software semantic version")
    environment: str = Field("production", description="Operating environment")
    uptime_seconds: float = Field(..., description="Process uptime in seconds")
    system: SystemMetrics = Field(..., description="System resource utilization")
    models: ModelStatus = Field(default_factory=ModelStatus, description="Inference engine statuses")
    rules_engine: RulesEngineStatus = Field(default_factory=RulesEngineStatus, description="Rules engine status")


class ReportPdfRequest(BaseModel):
    """POST /api/v1/report/pdf request body matching API Contract 3.3."""
    inspection_id: str = Field(..., description="Identifier of completed inspection to render")
    officer_notes: Optional[str] = Field(None, description="Optional inspecting officer annotations")
    include_raw_image: bool = Field(True, description="Whether to embed packaging thumbnail in PDF")


class EMaapSyncRequest(BaseModel):
    """POST /api/v1/emaap/mock-sync request body matching API Contract 3.4."""
    inspection_id: str = Field(..., description="Unique inspection identifier")
    jurisdiction_code: str = Field(..., description="Legal metrology jurisdiction code")
    officer_id: str = Field(..., description="Inspector identification token")
    compliance_state: str = Field(..., description="Compliance state outcome")
    improvement_notice_issued: bool = Field(..., description="Whether improvement notice was served")
    dossier_sha256: str = Field(..., min_length=64, max_length=64, description="Cryptographic SHA-256 seal of inspection dossier")


class EMaapSyncResponse(BaseModel):
    """POST /api/v1/emaap/mock-sync response matching API Contract 3.4."""
    sync_status: str = Field(..., description="Sync outcome: 'ACCEPTED_FOR_RECORD' | 'REJECTED'")
    emaap_reference_no: str = Field(..., description="Generated eMaap national registry reference number")
    received_at: str = Field(..., description="ISO 8601 UTC timestamp of portal receipt")
    tamper_verification: str = Field(..., description="Integrity check outcome: 'VERIFIED_VALID' | 'TAMPER_DETECTED'")
