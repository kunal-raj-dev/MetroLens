"""
Nirikshak Calibration Types: Data contracts and configuration for metric anchor detection.

Architecture:
AI PERCEIVES.
MATH VALIDATES.
RULES DECIDE.
HUMANS GOVERN.

Separation of Concerns:
Anchor Detection characterizes candidate physical anchors in the 2D image frame.
It does NOT estimate metric scale factor, does NOT apply homography, and does NOT
claim calibration.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple, Union, Dict, Any


class AnchorType(str, Enum):
    """Supported physical metric reference fiducial classes."""
    COIN_INR_10 = "COIN_INR_10"
    ID1_CARD = "ID1_CARD"


class AnchorDetectionStatus(str, Enum):
    """
    Structured outcome and failure state taxonomy for anchor detection.
    Normal malformed inputs return structured error states without raising unhandled exceptions.
    """
    SUCCESS = "SUCCESS"
    INVALID_INPUT = "INVALID_INPUT"
    NO_ANCHOR = "NO_ANCHOR"
    AMBIGUOUS_ANCHOR = "AMBIGUOUS_ANCHOR"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    INVALID_GEOMETRY = "INVALID_GEOMETRY"
    GLARE_INTERFERENCE = "GLARE_INTERFERENCE"
    INSUFFICIENT_EDGE_SUPPORT = "INSUFFICIENT_EDGE_SUPPORT"


@dataclass(frozen=True)
class EllipseGeometry:
    """
    Recovered 2D ellipse geometry for circular/elliptical anchors.

    Attributes:
        center: Sub-pixel (x, y) coordinates of the ellipse centroid.
        major_axis_px: Full major-axis diameter in pixels (2 * semi-major axis).
        minor_axis_px: Full minor-axis diameter in pixels (2 * semi-minor axis).
        angle_deg: Rotation angle in degrees of the first axis from the horizontal.
        aspect_ratio: Ratio of minor axis to major axis (b / a <= 1.0 under tilt).
    """
    center: Tuple[float, float]
    major_axis_px: float
    minor_axis_px: float
    angle_deg: float
    aspect_ratio: float


@dataclass(frozen=True)
class CardGeometry:
    """
    Recovered 2D quadrilateral boundary for ISO/IEC 7810 ID-1 reference card.

    Attributes:
        corners: Structurally immutable 4-tuple of (x, y) coordinates ordered
                 consistently: (Top-Left, Top-Right, Bottom-Right, Bottom-Left).
        width_px: Average measured pixel width of the card.
        height_px: Average measured pixel height of the card.
        aspect_ratio: Measured ratio of longer edge to shorter edge.
    """
    corners: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]]
    width_px: float
    height_px: float
    aspect_ratio: float


@dataclass(frozen=True)
class ConcentricRingInfo:
    """
    Auxiliary geometric evidence for bimetallic circular references (e.g. RBI Rs 10 coin).

    Attributes:
        outer_major_px: Full major-axis diameter of the outer brass ring in pixels.
        inner_major_px: Full major-axis diameter of the inner nickel-silver core in pixels.
        diameter_ratio: Measured ratio of inner to outer major-axis diameter.
        has_concentric_ring: True if concentric core was identified with spatial alignment.
    """
    outer_major_px: float
    inner_major_px: float
    diameter_ratio: float
    has_concentric_ring: bool


@dataclass(frozen=True)
class AnchorDetectorConfig:
    """
    Configurable detection, filtering, and scoring thresholds.

    Evidentiary Status:
        Default values represent initial hypotheses and proposed heuristics.
        They must NOT be treated as immutable physical constants or validated
        statutory criteria until physical packaging ground truth is established.
    """
    # Contour area limits (px / ratio)
    min_contour_area_px: float = 200.0
    max_contour_area_ratio: float = 0.60

    # Ellipse fit filtering (PROPOSED HEURISTIC / NOT PHYSICALLY VALIDATED)
    max_ellipse_residual: float = 0.15
    min_ellipse_aspect_ratio: float = 0.35
    max_ellipse_aspect_ratio: float = 1.05

    # Concentric ring candidate evidence (PROPOSED HEURISTIC / NOT PHYSICALLY VALIDATED)
    # RBI Rs 10 coin specification: 19.6 mm inner / 27.0 mm outer ≈ 0.7259
    concentric_ring_ratio_target: float = 0.726
    concentric_ring_ratio_tolerance: float = 0.08
    concentric_center_dist_ratio: float = 0.15

    # ID-1 Card specifications & tolerances
    # ISO/IEC 7810 ID-1 standard: 85.60 mm x 53.98 mm -> ratio ≈ 1.58577 (SOURCE / SPECIFICATION)
    card_aspect_ratio_target: float = 1.58577
    card_aspect_ratio_tolerance: float = 0.30  # PROPOSED HEURISTIC (accommodates perspective foreshortening)
    card_min_corner_angle_deg: float = 60.0    # PROPOSED HEURISTIC
    card_max_corner_angle_deg: float = 120.0   # PROPOSED HEURISTIC

    # Candidate scoring & quality gates (PROPOSED HEURISTICS)
    min_edge_support_ratio: float = 0.30
    max_glare_overlap_ratio: float = 0.40
    min_confidence_threshold: float = 0.50
    ambiguity_confidence_margin: float = 0.08


@dataclass(frozen=True)
class AnchorDetectionResult:
    """
    Minimal, strongly-typed outcome of metric reference anchor detection.

    Attributes:
        detected: True if a credible, unambiguous anchor candidate was identified.
        anchor_type: Identified anchor type (COIN_INR_10 or ID1_CARD), or None.
        status: Specific detection outcome or failure reason code.
        confidence: Normalized confidence score (0.0 to 1.0).
        geometry: Recovered 2D geometric boundary or None if not detected.
        fit_quality: Normalized geometric fit quality (e.g. 1.0 - residual).
        ring_information: Concentric ring evidence if a circular coin was detected.
        message: Optional human-readable diagnostic message.
    """
    detected: bool
    anchor_type: Optional[AnchorType]
    status: AnchorDetectionStatus
    confidence: float
    geometry: Optional[Union[EllipseGeometry, CardGeometry]] = None
    fit_quality: float = 0.0
    ring_information: Optional[ConcentricRingInfo] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serializes result into an inspectable dictionary."""
        geom_dict = None
        if isinstance(self.geometry, EllipseGeometry):
            geom_dict = {
                "type": "ellipse",
                "center": list(self.geometry.center),
                "major_axis_px": self.geometry.major_axis_px,
                "minor_axis_px": self.geometry.minor_axis_px,
                "angle_deg": self.geometry.angle_deg,
                "aspect_ratio": self.geometry.aspect_ratio,
            }
        elif isinstance(self.geometry, CardGeometry):
            geom_dict = {
                "type": "card_quadrilateral",
                "corners": [list(pt) for pt in self.geometry.corners],
                "width_px": self.geometry.width_px,
                "height_px": self.geometry.height_px,
                "aspect_ratio": self.geometry.aspect_ratio,
            }

        ring_dict = None
        if self.ring_information is not None:
            ring_dict = {
                "outer_major_px": self.ring_information.outer_major_px,
                "inner_major_px": self.ring_information.inner_major_px,
                "diameter_ratio": self.ring_information.diameter_ratio,
                "has_concentric_ring": self.ring_information.has_concentric_ring,
            }

        return {
            "detected": self.detected,
            "anchor_type": self.anchor_type.value if self.anchor_type else None,
            "status": self.status.value,
            "confidence": self.confidence,
            "geometry": geom_dict,
            "fit_quality": self.fit_quality,
            "ring_information": ring_dict,
            "message": self.message,
        }
