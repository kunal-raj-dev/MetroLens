"""
Nirikshak Vision: Image quality gating and panel segmentation.
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np


class QualityGateResult:
    """Represents the outcome of the pre-inference quality gate."""
    def __init__(
        self,
        passed: bool,
        laplacian_variance: float,
        glare_ratio: float,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.passed = passed
        self.laplacian_variance = laplacian_variance
        self.glare_ratio = glare_ratio
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "laplacian_variance": self.laplacian_variance,
            "glare_ratio": self.glare_ratio,
            "details": self.details,
        }


def check_image_quality(
    image: np.ndarray,
    min_laplacian_variance: float = 100.0,
    max_glare_ratio: float = 0.15,
) -> QualityGateResult:
    """
    Evaluates image sharpness via Laplacian variance and specular glare via high-luminance thresholding.
    Deterministic and fast (< 15 ms).
    """
    if image is None or image.size == 0:
        return QualityGateResult(passed=False, laplacian_variance=0.0, glare_ratio=1.0, details={"error": "Empty image"})

    # Convert to grayscale if 3-channel
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Standard luminance weighting
        gray = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
    else:
        gray = image

    # Edge sharpness via Laplacian variance (or fallback to pixel variance)
    try:
        import cv2
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    except Exception:
        laplacian_var = float(np.var(gray))
    glare_pixels = int(np.sum(gray >= 250))
    total_pixels = gray.size
    glare_ratio = float(glare_pixels / total_pixels) if total_pixels > 0 else 1.0

    passed = (laplacian_var >= min_laplacian_variance) and (glare_ratio <= max_glare_ratio)

    return QualityGateResult(
        passed=passed,
        laplacian_variance=laplacian_var,
        glare_ratio=glare_ratio,
        details={
            "min_laplacian_threshold": min_laplacian_variance,
            "max_glare_threshold": max_glare_ratio,
        },
    )


__all__ = ["QualityGateResult", "check_image_quality"]
