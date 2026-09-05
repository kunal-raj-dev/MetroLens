"""
Nirikshak Vision: Pre-flight image quality gating and frame validation.
"""

from typing import Optional
import numpy as np

from .types import QualityGateResult, QualityGateThresholds
from .quality import (
    evaluate_image_quality,
    compute_laplacian_variance,
    compute_glare_candidate_ratio,
    compute_mean_luminance,
    convert_to_grayscale,
)


def check_image_quality(
    image: np.ndarray,
    min_laplacian_variance: float = 100.0,
    max_glare_ratio: float = 0.15,
) -> QualityGateResult:
    """
    Backwards-compatible wrapper around evaluate_image_quality.

    Maintains full compatibility with existing worker pipeline and legacy smoke tests:
    - Accepts positional or keyword arguments for min_laplacian_variance and max_glare_ratio.
    - Disables luminance exposure checks when called via this legacy interface unless configured.
    - Returns QualityGateResult with .passed, .laplacian_variance, .glare_ratio, .details.
    """
    # Legacy caller expects exposure checks not to cause failure unless explicitly requested
    thresholds = QualityGateThresholds(
        min_blur_score=min_laplacian_variance,
        max_glare_candidate_ratio=max_glare_ratio,
        min_mean_luminance=0.0,
        max_mean_luminance=255.0,
    )
    return evaluate_image_quality(image, thresholds=thresholds)


__all__ = [
    "QualityGateResult",
    "QualityGateThresholds",
    "evaluate_image_quality",
    "check_image_quality",
    "compute_laplacian_variance",
    "compute_glare_candidate_ratio",
    "compute_mean_luminance",
    "convert_to_grayscale",
]
