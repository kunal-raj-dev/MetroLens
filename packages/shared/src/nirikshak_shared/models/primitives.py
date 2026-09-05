"""
Nirikshak Domain Primitives: Geometric, metrological, and evidentiary value objects.
"""

from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, Field


class CalibrationStatus(str, Enum):
    CALIBRATED = "CALIBRATED"
    UNCALIBRATED = "UNCALIBRATED"
    APPROXIMATE_ASSISTED = "APPROXIMATE_ASSISTED"


class PanelName(str, Enum):
    PRINCIPAL_DISPLAY_PANEL = "PRINCIPAL_DISPLAY_PANEL"
    TOP = "TOP"
    BOTTOM = "BOTTOM"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    BACK = "BACK"
    UNKNOWN = "UNKNOWN"


class RuleVerdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    REVIEW = "REVIEW"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class OverallVerdict(str, Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    SUSPECT_REVIEW = "SUSPECT_REVIEW"
    INCONCLUSIVE = "INCONCLUSIVE"


class InspectionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    REJECTED_QUALITY = "REJECTED_QUALITY"
    FAILED_PROCESSING = "FAILED_PROCESSING"
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"


class BoundingBox(BaseModel):
    """Normalized or pixel bounding box coordinates."""
    x_min: float = Field(..., description="Minimum X coordinate")
    y_min: float = Field(..., description="Minimum Y coordinate")
    x_max: float = Field(..., description="Maximum X coordinate")
    y_max: float = Field(..., description="Maximum Y coordinate")


class ObservedValue(BaseModel):
    """Value payload observed through OCR or optical measurement."""
    raw_text: Optional[str] = Field(None, description="Raw OCR transcribed text")
    normalized_value: Optional[Union[str, float, int, bool]] = Field(
        None, description="Cleaned, normalized, or parsed field value"
    )
    measured_font_height_mm: Optional[float] = Field(
        None, description="Physical measured font height in millimeters"
    )
    measured_pdp_area_cm2: Optional[float] = Field(
        None, description="Calculated Principal Display Panel area in square centimeters"
    )
    ocr_confidence: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Confidence score from OCR engine (0.0 to 1.0)"
    )


class OperatorAnnotation(BaseModel):
    """Human officer annotation and audit trail."""
    reviewed_by: Optional[str] = Field(None, description="Officer ID or badge number")
    confirmed: Optional[bool] = Field(None, description="Whether officer confirmed the automated finding")
    notes: Optional[str] = Field(None, description="Justification or observation notes")
