"""
Nirikshak Vision Types: Dataclasses and configuration for image quality gating.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(frozen=True)
class QualityGateThresholds:
    """
    Configurable quality gate thresholds.

    NOTE: Default values reflect current project specification targets
    (ADR-006 / docs/05_AI_VISION/IMAGE_QUALITY_GATE.md) and are subject
    to empirical tuning on ground-truth retail datasets. They must NOT
    be treated as immutable physical or scientific constants.
    """
    min_blur_score: float = 100.0
    max_glare_candidate_ratio: float = 0.15
    min_mean_luminance: float = 40.0
    max_mean_luminance: float = 220.0
    specular_intensity_threshold: int = 250
    specular_saturation_threshold: int = 40
    local_contrast_threshold: int = 20
    global_blowout_ratio: float = 0.60
    local_neighborhood_ksize: int = 31


@dataclass(frozen=True)
class QualityGateResult:
    """
    Structured outcome of the pre-flight image quality evaluation.

    Attributes:
        passed: Whether the frame satisfied all quality criteria.
        blur_score: Variance of the 2D Laplacian operator (higher = sharper).
        glare_candidate_ratio: Fraction of pixels exhibiting specular highlight characteristics (0.0 to 1.0).
        mean_luminance: Mean grayscale intensity across the image (0.0 to 255.0).
        is_blurry: True if blur_score is below configured threshold.
        is_glared: True if glare_candidate_ratio exceeds configured threshold.
        is_under_exposed: True if mean_luminance is below configured floor.
        is_over_exposed: True if mean_luminance exceeds configured ceiling.
        remediation_cues: Actionable plain-language guidance for camera retake.
        details: Diagnostic dictionary containing thresholds and auxiliary metrics.
    """
    passed: bool
    blur_score: float
    glare_candidate_ratio: float
    mean_luminance: float
    is_blurry: bool
    is_glared: bool
    is_under_exposed: bool
    is_over_exposed: bool
    remediation_cues: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def laplacian_variance(self) -> float:
        """Backwards compatibility alias for blur_score."""
        return self.blur_score

    @property
    def glare_ratio(self) -> float:
        """Backwards compatibility alias for glare_candidate_ratio."""
        return self.glare_candidate_ratio

    def to_dict(self) -> Dict[str, Any]:
        """Serializes result into a standardized dictionary matching API contract."""
        return {
            "passed": self.passed,
            "blur_score": self.blur_score,
            "laplacian_variance": self.blur_score,
            "glare_candidate_ratio": self.glare_candidate_ratio,
            "glare_ratio": self.glare_candidate_ratio,
            "mean_luminance": self.mean_luminance,
            "is_blurry": self.is_blurry,
            "is_glared": self.is_glared,
            "is_under_exposed": self.is_under_exposed,
            "is_over_exposed": self.is_over_exposed,
            "remediation_cues": list(self.remediation_cues),
            "details": dict(self.details),
        }
