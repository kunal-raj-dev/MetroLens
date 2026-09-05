"""
Canonical data contracts and geometry primitives for Nirikshak OCR subsystem.

COORDINATE CONVENTION:
- Space: Original input image pixel coordinates (unnormalized).
- Origin: Top-left corner (0.0, 0.0).
- X-axis: Horizontal pointing right.
- Y-axis: Vertical pointing downward.
- Polygon: 4-point convex quad [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] ordered clockwise:
  [top-left, top-right, bottom-right, bottom-left].
- Bounding Box: Derived axis-aligned envelope [xmin, ymin, xmax, ymax].

SEAM BOUNDARY NOTICE:
Member 1 (OCR) outputs raw geometry (polygons, bboxes, raw pixel heights).
Member 2 (Calibration) converts geometry into physical dimensions (mm).
Member 3 (Rule Engine) interprets extracted text semantically for Legal Metrology compliance.
"""

from enum import Enum
import math
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, field_validator

from nirikshak_shared.models.contracts import OCRObservation
from nirikshak_shared.models.primitives import BoundingBox


class ScriptType(str, Enum):
    """Detected or routed script category for text lines."""
    LATIN = "latin"
    DEVANAGARI = "devanagari"
    UNKNOWN = "unknown"


class OCRToken(BaseModel):
    """
    Atomic text token extracted from scene text detection and recognition.
    All coordinates refer strictly to original input image pixel space.
    """
    token_id: str = Field(..., description="Unique deterministic token identifier (e.g. tok_001)")
    text: str = Field(..., description="Recognized character sequence")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model CTC/decoder confidence score")
    polygon: List[List[float]] = Field(
        ...,
        description="Clockwise 4-point quadrilateral in original image space: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]"
    )
    bbox: List[float] = Field(
        ...,
        description="Derived axis-aligned bounding box: [xmin, ymin, xmax, ymax]"
    )
    script: ScriptType = Field(default=ScriptType.UNKNOWN, description="Identified script classification")
    line_id: int = Field(default=0, description="Logical text line index in reading order")
    raw_pixel_height: Optional[float] = Field(
        default=None,
        description="Average quadrilateral height in original image pixels. NOTE: THIS IS NOT LEGAL FONT HEIGHT. Physical font height in mm is computed exclusively by Member 2."
    )
    model_name: str = Field(default="", description="Name of the recognition model that decoded this token")

    @field_validator("polygon")
    @classmethod
    def validate_polygon_geometry(cls, v: List[List[float]]) -> List[List[float]]:
        if len(v) != 4:
            raise ValueError(f"Polygon must have exactly 4 vertices, got {len(v)}")
        for pt in v:
            if len(pt) != 2:
                raise ValueError(f"Each polygon vertex must be [x, y], got {pt}")
            if not math.isfinite(pt[0]) or not math.isfinite(pt[1]):
                raise ValueError(f"Polygon coordinates must be finite numbers, got {pt}")
        return v

    def to_observation(self) -> OCRObservation:
        """Converts OCRToken to shared canonical OCRObservation for downstream compatibility."""
        xmin, ymin, xmax, ymax = self.bbox
        width = max(0.0, xmax - xmin)
        height = max(0.0, ymax - ymin)
        
        shared_bbox = BoundingBox(
            x_min=float(xmin),
            y_min=float(ymin),
            x_max=float(xmax),
            y_max=float(ymax)
        )
        
        lang_code = "hi" if self.script == ScriptType.DEVANAGARI else "en"
        
        return OCRObservation(
            token_id=self.token_id,
            text=self.text,
            confidence=float(self.confidence),
            bounding_box=shared_bbox,
            polygon=self.polygon,
            language=lang_code
        )


class OCRResult(BaseModel):
    """
    Standardized payload produced by OCREngine.extract().
    Encapsulates all extracted tokens, execution timings, and routing metadata.
    """
    image_id: str = Field(default="img_001", description="Identifier of the inspected image")
    image_width: int = Field(..., ge=1, description="Original image width in pixels")
    image_height: int = Field(..., ge=1, description="Original image height in pixels")
    tokens: List[OCRToken] = Field(default_factory=list, description="Extracted tokens sorted in reading order")
    engine: str = Field(default="PP-OCRv3-ROUTED", description="Architecture descriptor")
    detector_model: str = Field(default="", description="Detector ONNX asset name")
    recognizer_models: Dict[str, str] = Field(default_factory=dict, description="Active recognizer ONNX assets")
    processing_time_ms: float = Field(default=0.0, description="Total wall-clock inference time in milliseconds")
    stage_timings: Dict[str, float] = Field(default_factory=dict, description="Granular latency breakdown in ms")
    warnings: List[str] = Field(default_factory=list, description="Diagnostic warnings or low-confidence alerts")
    routing_summary: Dict[str, int] = Field(
        default_factory=lambda: {"latin": 0, "devanagari": 0, "unknown": 0},
        description="Count of tokens routed to each recognizer"
    )

    @property
    def full_text(self) -> str:
        """Convenience property returning full transcription text joined by newlines."""
        return "\n".join(t.text for t in self.tokens)

    def to_observations(self) -> List[OCRObservation]:
        """Convenience conversion returning canonical OCRObservation list for Member 3/4."""
        return [t.to_observation() for t in self.tokens]
