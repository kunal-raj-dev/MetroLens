"""
Nirikshak Vision Types: Dataclasses and configuration for image quality gating.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass(frozen=True, init=False)
class QualityGateThresholds:
    """
    Configurable quality gate thresholds.

    NOTE: Default values reflect current project specification targets and
    empirical baselines. They must NOT be treated as immutable physical or
    scientific constants.
    """
    min_blur_score: float
    max_glare_candidate_ratio: float
    min_contrast_score: float
    min_mean_luminance: float
    max_mean_luminance: float
    max_aspect_ratio: Optional[float]
    specular_intensity_threshold: int
    specular_saturation_threshold: int
    local_contrast_threshold: int
    global_blowout_ratio: float
    local_neighborhood_ksize: int

    def __init__(
        self,
        min_blur_score: float = 100.0,
        max_glare_candidate_ratio: Optional[float] = None,
        max_glare_ratio: Optional[float] = None,
        min_contrast_score: float = 20.0,
        min_mean_luminance: float = 40.0,
        max_mean_luminance: float = 220.0,
        max_aspect_ratio: Optional[float] = None,
        specular_intensity_threshold: int = 250,
        specular_saturation_threshold: int = 40,
        local_contrast_threshold: int = 20,
        global_blowout_ratio: float = 0.60,
        local_neighborhood_ksize: int = 31,
    ):
        glare_thresh = 0.15
        if max_glare_ratio is not None:
            glare_thresh = max_glare_ratio
        elif max_glare_candidate_ratio is not None:
            glare_thresh = max_glare_candidate_ratio

        object.__setattr__(self, "min_blur_score", float(min_blur_score))
        object.__setattr__(self, "max_glare_candidate_ratio", float(glare_thresh))
        object.__setattr__(self, "min_contrast_score", float(min_contrast_score))
        object.__setattr__(self, "min_mean_luminance", float(min_mean_luminance))
        object.__setattr__(self, "max_mean_luminance", float(max_mean_luminance))
        object.__setattr__(self, "max_aspect_ratio", max_aspect_ratio)
        object.__setattr__(self, "specular_intensity_threshold", int(specular_intensity_threshold))
        object.__setattr__(self, "specular_saturation_threshold", int(specular_saturation_threshold))
        object.__setattr__(self, "local_contrast_threshold", int(local_contrast_threshold))
        object.__setattr__(self, "global_blowout_ratio", float(global_blowout_ratio))
        object.__setattr__(self, "local_neighborhood_ksize", int(local_neighborhood_ksize))

    @property
    def max_glare_ratio(self) -> float:
        """Alias for max_glare_candidate_ratio."""
        return self.max_glare_candidate_ratio


# Alias for naming consistency
ImageQualityThresholds = QualityGateThresholds


@dataclass(frozen=True, init=False)
class ImageQualityResult:
    """
    Structured outcome of the pre-flight image quality evaluation.

    Attributes:
        passed: True if the image is valid and satisfies all optical quality criteria.
        is_valid_input: True if the input was a processable image array.
        blur_score: Variance of the 2D Laplacian operator (higher = sharper).
        glare_score: Fraction of pixels exhibiting specular highlight characteristics (0.0 to 1.0).
        contrast_score: RMS contrast (intensity standard deviation).
        mean_luminance: Mean grayscale intensity across the image (0.0 to 255.0).
        is_blurry: True if blur_score is below configured threshold.
        is_glared: True if glare_score exceeds configured threshold.
        is_low_contrast: True if contrast_score is below configured threshold.
        is_dark: True if mean_luminance is below configured floor.
        is_over_exposed: True if mean_luminance exceeds configured ceiling.
        failure_reasons: Actionable plain-language guidance explaining failures.
        details: Diagnostic dictionary containing thresholds and auxiliary metrics.
    """
    passed: bool
    is_valid_input: bool
    blur_score: float
    glare_score: float
    contrast_score: float
    mean_luminance: float
    is_blurry: bool
    is_glared: bool
    is_low_contrast: bool
    is_dark: bool
    is_over_exposed: bool
    failure_reasons: List[str]
    details: Dict[str, Any]

    def __init__(
        self,
        passed: bool,
        is_valid_input: bool = True,
        blur_score: float = 0.0,
        glare_score: Optional[float] = None,
        glare_candidate_ratio: Optional[float] = None,
        glare_ratio: Optional[float] = None,
        contrast_score: float = 0.0,
        mean_luminance: float = 0.0,
        is_blurry: bool = False,
        is_glared: bool = False,
        is_low_contrast: bool = False,
        is_dark: Optional[bool] = None,
        is_under_exposed: Optional[bool] = None,
        is_over_exposed: bool = False,
        failure_reasons: Optional[List[str]] = None,
        remediation_cues: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None,
        laplacian_variance: Optional[float] = None,
    ):
        b_score = blur_score if laplacian_variance is None else laplacian_variance

        g_score = 0.0
        if glare_score is not None:
            g_score = glare_score
        elif glare_candidate_ratio is not None:
            g_score = glare_candidate_ratio
        elif glare_ratio is not None:
            g_score = glare_ratio

        dark = False
        if is_dark is not None:
            dark = is_dark
        elif is_under_exposed is not None:
            dark = is_under_exposed

        reasons: List[str] = []
        if failure_reasons is not None:
            reasons = list(failure_reasons)
        elif remediation_cues is not None:
            reasons = list(remediation_cues)

        det = dict(details) if details is not None else {}

        object.__setattr__(self, "passed", bool(passed))
        object.__setattr__(self, "is_valid_input", bool(is_valid_input))
        object.__setattr__(self, "blur_score", float(b_score))
        object.__setattr__(self, "glare_score", float(g_score))
        object.__setattr__(self, "contrast_score", float(contrast_score))
        object.__setattr__(self, "mean_luminance", float(mean_luminance))
        object.__setattr__(self, "is_blurry", bool(is_blurry))
        object.__setattr__(self, "is_glared", bool(is_glared))
        object.__setattr__(self, "is_low_contrast", bool(is_low_contrast))
        object.__setattr__(self, "is_dark", bool(dark))
        object.__setattr__(self, "is_over_exposed", bool(is_over_exposed))
        object.__setattr__(self, "failure_reasons", reasons)
        object.__setattr__(self, "details", det)

    @property
    def laplacian_variance(self) -> float:
        """Backwards compatibility alias for blur_score."""
        return self.blur_score

    @property
    def glare_ratio(self) -> float:
        """Backwards compatibility alias for glare_score."""
        return self.glare_score

    @property
    def glare_candidate_ratio(self) -> float:
        """Backwards compatibility alias for glare_score."""
        return self.glare_score

    @property
    def is_under_exposed(self) -> bool:
        """Backwards compatibility alias for is_dark."""
        return self.is_dark

    @property
    def remediation_cues(self) -> List[str]:
        """Backwards compatibility alias for failure_reasons."""
        return self.failure_reasons

    def to_dict(self) -> Dict[str, Any]:
        """Serializes result into a standardized dictionary matching API contract."""
        return {
            "passed": self.passed,
            "is_valid_input": self.is_valid_input,
            "blur_score": self.blur_score,
            "laplacian_variance": self.blur_score,
            "glare_score": self.glare_score,
            "glare_ratio": self.glare_score,
            "glare_candidate_ratio": self.glare_score,
            "contrast_score": self.contrast_score,
            "mean_luminance": self.mean_luminance,
            "is_blurry": self.is_blurry,
            "is_glared": self.is_glared,
            "is_low_contrast": self.is_low_contrast,
            "is_dark": self.is_dark,
            "is_under_exposed": self.is_dark,
            "is_over_exposed": self.is_over_exposed,
            "failure_reasons": list(self.failure_reasons),
            "remediation_cues": list(self.failure_reasons),
            "details": dict(self.details),
        }


# Backwards compatibility alias for Phase 1
QualityGateResult = ImageQualityResult
