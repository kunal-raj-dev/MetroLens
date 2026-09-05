"""
Nirikshak Canonical Seam Contracts: Inter-package DTOs and Data Transfer Objects.
These contracts govern data interchange between vision, calibration, ocr, extraction,
measurement, rules-engine, evidence, reporting, api, and worker services.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, field_validator

from .primitives import (
    BoundingBox,
    CalibrationStatus,
    PanelName,
    RuleVerdict,
    OverallVerdict,
    InspectionStatus,
    ObservedValue,
    OperatorAnnotation,
)


class OCRObservation(BaseModel):
    """Atomic OCR text observation with spatial bounding polygon."""
    token_id: str = Field(..., description="Unique token identifier within the inspection frame")
    text: str = Field(..., description="Transcribed string content")
    confidence: float = Field(..., ge=0.0, le=1.0, description="OCR model confidence score")
    bounding_box: BoundingBox = Field(..., description="Bounding box enclosing the token")
    polygon: Optional[List[List[float]]] = Field(
        None, description="Detailed polygon vertices [[x1, y1], [x2, y2], ...]"
    )
    language: Optional[str] = Field("en", description="Detected language code (ISO 639-1)")


class DeclarationField(BaseModel):
    """Mandatory or voluntary statutory declaration parsed from OCR observations."""
    field_name: str = Field(
        ...,
        description="Standard declaration key (e.g., mrp, net_quantity, mfg_date, expiry_date, manufacturer_name, country_of_origin, consumer_care)"
    )
    raw_text: str = Field(..., description="Original verbatim text string extracted from the label")
    normalized_value: Optional[Any] = Field(None, description="Cleaned, standardized value object")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Extraction model confidence")
    source_token_ids: List[str] = Field(
        default_factory=list, description="IDs of source OCRObservations contributing to this field"
    )
    bounding_box: Optional[BoundingBox] = Field(None, description="Enclosing bounding box of the declaration")
    is_mandatory: bool = Field(True, description="Whether this declaration is mandatory under Rule 6")
    is_present: bool = Field(True, description="Whether the declaration was detected on the package")


class MeasurementResult(BaseModel):
    """Physical metrological dimension calculated using optical reference calibration."""
    feature_name: str = Field(
        ...,
        description="Feature measured (e.g. pdp_area_cm2, numeral_height_mm, symbol_height_mm, line_spacing_mm)"
    )
    measured_pixels: float = Field(..., description="Raw optical measurement in pixel units")
    scale_factor_mm_per_pixel: Optional[float] = Field(
        None, description="Optical calibration scale factor applied (mm / pixel)"
    )
    measured_mm: Optional[float] = Field(
        None, description="Computed physical measurement in millimeters"
    )
    uncertainty_mm: Optional[float] = Field(
        None, description="Estimated measurement uncertainty bound (± mm)"
    )
    calibration_status: CalibrationStatus = Field(
        default=CalibrationStatus.UNCALIBRATED,
        description="Calibration state under which the measurement was recorded"
    )
    bounding_box: Optional[BoundingBox] = Field(None, description="Bounding box of the measured feature")


class RuleEvaluation(BaseModel):
    """Deterministic evaluation outcome of a single machine-readable rule."""
    rule_id: str = Field(..., description="Canonical rule ID (e.g., LMPC-R06-MRP-001)")
    rule_title: str = Field(..., description="Human-readable rule title")
    verdict: RuleVerdict = Field(..., description="Evaluation outcome")
    statutory_reference: str = Field(
        ..., description="Exact statutory citation (e.g., Rule 6(1)(e), Rule 9 Table 1)"
    )
    observed_summary: str = Field(..., description="Summary of observed values used in evaluation")
    required_summary: str = Field(..., description="Summary of statutory requirement")
    evidence_ids: List[str] = Field(
        default_factory=list, description="IDs of EvidenceItems supporting this evaluation"
    )
    uncertainty_flag: bool = Field(
        False, description="Whether measurement uncertainty impacts the evaluation verdict"
    )
    evaluation_notes: Optional[str] = Field(None, description="Detailed rationale or deviation explanation")


class EvidenceItem(BaseModel):
    """Immutable forensic evidence node matching rules/schema/evidence.schema.json."""
    evidence_id: str = Field(..., description="Unique evidence node identifier")
    image_sha256: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$", description="SHA-256 hash of the parent raw image")
    panel_name: PanelName = Field(default=PanelName.PRINCIPAL_DISPLAY_PANEL, description="Package panel location")
    bounding_box: BoundingBox = Field(..., description="Pixel coordinate bounding box")
    calibration_status: CalibrationStatus = Field(..., description="Calibration status during capture")
    physical_scale_mm_per_pixel: Optional[float] = Field(
        None, description="Scale factor applied to this evidence crop"
    )
    observed_value: ObservedValue = Field(..., description="Measured or extracted observation payload")
    operator_annotation: Optional[OperatorAnnotation] = Field(
        None, description="Inspector manual annotation or override"
    )

    def to_schema_dict(self) -> Dict[str, Any]:
        """Returns dictionary strictly validated against rules/schema/evidence.schema.json."""
        return self.model_dump(mode="json", exclude_none=True)


class InspectionError(BaseModel):
    """Standardized error object for failures across the pipeline."""
    error_code: str = Field(..., description="Machine-readable error identifier (e.g., ERR_IMAGE_BLUR)")
    stage: str = Field(..., description="Pipeline stage where the error occurred")
    message: str = Field(..., description="Human-readable error description")
    remediation_hint: Optional[str] = Field(None, description="Actionable instruction for the operator")
    is_fatal: bool = Field(True, description="Whether this error halted the inspection pipeline")


class InspectionRequest(BaseModel):
    """Ingestion payload initiating an automated inspection run."""
    inspection_id: str = Field(..., description="Globally unique inspection run identifier")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Submission timestamp")
    officer_id: Optional[str] = Field(None, description="Inspector officer badge or account ID")
    device_id: Optional[str] = Field(None, description="Client device hardware or installation ID")
    commodity_category: Optional[str] = Field(None, description="Target commodity classification")
    image_payload_base64: Optional[str] = Field(None, description="Base64 encoded raw image data")
    image_path: Optional[str] = Field(None, description="Local or object storage path to raw image")
    image_sha256: Optional[str] = Field(None, description="SHA-256 digest of the image bytes")
    target_ruleset: Optional[str] = Field("current", description="Target rule corpus directory (default: current)")


class InspectionResult(BaseModel):
    """Master inspection outcome containing complete evidence DAG, evaluations, and verdict."""
    inspection_id: str = Field(..., description="Unique inspection run identifier")
    status: InspectionStatus = Field(..., description="Pipeline processing lifecycle status")
    image_sha256: str = Field(..., pattern=r"^[a-fA-F0-9]{64}$", description="Cryptographic SHA-256 of raw image")
    overall_verdict: OverallVerdict = Field(..., description="Composite statutory compliance verdict")
    quality_gate_passed: bool = Field(..., description="Whether input frame passed blur and glare thresholds")
    calibration_status: CalibrationStatus = Field(..., description="Calibration level achieved")
    declarations: Dict[str, DeclarationField] = Field(
        default_factory=dict, description="Extracted mandatory declarations keyed by field name"
    )
    measurements: Dict[str, MeasurementResult] = Field(
        default_factory=dict, description="Computed metric dimensions keyed by feature name"
    )
    rule_evaluations: List[RuleEvaluation] = Field(
        default_factory=list, description="Evaluations of applicable machine-readable rules"
    )
    evidence_chain: List[EvidenceItem] = Field(
        default_factory=list, description="Cryptographic evidence items linking pixels to verdicts"
    )
    errors: List[InspectionError] = Field(
        default_factory=list, description="Non-fatal warnings or fatal pipeline execution errors"
    )
    dossier_pdf_path: Optional[str] = Field(None, description="Path to generated signed inspection dossier PDF")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Completion timestamp")
