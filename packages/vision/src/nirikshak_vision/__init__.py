"""
Nirikshak Vision: Pre-flight image quality gating and frame validation.
"""

from typing import Optional
import numpy as np

from .types import (
    ImageQualityResult,
    ImageQualityThresholds,
    QualityGateResult,
    QualityGateThresholds,
)
from .quality import (
    evaluate_image_quality,
    compute_laplacian_variance,
    compute_glare_candidate_ratio,
    compute_contrast,
    compute_mean_luminance,
    convert_to_grayscale,
)


def check_image_quality(
    image: np.ndarray,
    min_laplacian_variance: float = 100.0,
    max_glare_ratio: float = 0.15,
) -> ImageQualityResult:
    """
    Backwards-compatible wrapper around evaluate_image_quality.

    Maintains full compatibility with existing worker pipeline and legacy smoke tests:
    - Accepts positional or keyword arguments for min_laplacian_variance and max_glare_ratio.
    - Disables luminance exposure and contrast checks when called via this legacy interface unless configured.
    - Returns ImageQualityResult / QualityGateResult with .passed, .laplacian_variance, .glare_ratio, .details.
    """
    thresholds = QualityGateThresholds(
        min_blur_score=min_laplacian_variance,
        max_glare_candidate_ratio=max_glare_ratio,
        min_contrast_score=0.0,
        min_mean_luminance=0.0,
        max_mean_luminance=255.0,
    )
    return evaluate_image_quality(image, thresholds=thresholds)


__all__ = [
    "ImageQualityResult",
    "ImageQualityThresholds",
    "QualityGateResult",
    "QualityGateThresholds",
    "evaluate_image_quality",
    "check_image_quality",
    "compute_laplacian_variance",
    "compute_glare_candidate_ratio",
    "compute_contrast",
    "compute_mean_luminance",
    "convert_to_grayscale",
]
