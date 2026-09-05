"""
Nirikshak Vision Quality: Pure, deterministic optical pre-flight quality filters.

Evaluates image sharpness (Laplacian variance), specular glare candidates (localized
intensity saturation), global illumination (mean luminance), and contrast (intensity std).
Provides clear distinction between invalid input and poor-quality images.
"""

from typing import List, Optional, Dict, Any
import cv2
import numpy as np

from .types import (
    ImageQualityResult,
    QualityGateResult,
    QualityGateThresholds,
    ImageQualityThresholds,
)


def convert_to_grayscale(
    image: np.ndarray,
    color_format: str = "BGR",
) -> np.ndarray:
    """
    Converts 2D or 3D image array to single-channel uint8 grayscale without mutating input.

    Supports BGR, RGB, BGRA, RGBA color formats and float/integer normalization.
    """
    if image.dtype != np.uint8:
        if np.issubdtype(image.dtype, np.floating):
            if np.isnan(image).any() or np.isinf(image).any():
                raise ValueError("Floating-point image array contains NaN or Inf values.")
            max_val = float(np.max(image)) if image.size > 0 else 1.0
            if max_val <= 1.0:
                clipped = np.clip(image * 255.0, 0, 255).astype(np.uint8)
            else:
                clipped = np.clip(image, 0, 255).astype(np.uint8)
        else:
            clipped = np.clip(image, 0, 255).astype(np.uint8)
    else:
        clipped = image

    if clipped.ndim == 2:
        return clipped.copy()

    if clipped.ndim == 3:
        channels = clipped.shape[2]
        fmt = color_format.upper()
        if channels == 1:
            return np.squeeze(clipped, axis=2).copy()
        if channels == 3:
            if fmt == "RGB":
                return cv2.cvtColor(clipped, cv2.COLOR_RGB2GRAY)
            return cv2.cvtColor(clipped, cv2.COLOR_BGR2GRAY)
        if channels == 4:
            if fmt == "RGBA":
                return cv2.cvtColor(clipped, cv2.COLOR_RGBA2GRAY)
            return cv2.cvtColor(clipped, cv2.COLOR_BGRA2GRAY)

    raise ValueError(f"Unsupported image array shape for grayscale conversion: {clipped.shape}")


def compute_laplacian_variance(gray: np.ndarray) -> float:
    """
    Computes variance of the 2D Laplacian operator.

    Higher variance corresponds to sharper transitions and edges; low variance indicates blur.
    """
    if gray.shape[0] < 3 or gray.shape[1] < 3:
        return 0.0

    laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=1)
    return float(np.var(laplacian))


def compute_glare_candidate_ratio(
    image: np.ndarray,
    gray: np.ndarray,
    thresholds: QualityGateThresholds,
) -> float:
    """
    Computes the fraction of pixels classified as candidate specular glare highlights (0.0 to 1.0).

    To avoid false-positive rejections on diffuse white regions (such as white labels or
    white packaging backgrounds), candidate detection requires intensity clipping (>= 250)
    and either:
    1. Global frame blowout (where > 60% of pixels are saturated white), OR
    2. Localized specular prominence (where saturated pixels exhibit a steep intensity
       gradient relative to their surrounding neighborhood).
    """
    if gray.size == 0:
        return 0.0

    # 1. Saturated intensity mask
    saturated = (gray >= thresholds.specular_intensity_threshold)
    saturated_count = int(np.count_nonzero(saturated))

    if saturated_count == 0:
        return 0.0

    # 2. Saturation filter for 3-channel images (specular glare is desaturated white)
    if image.ndim == 3 and image.shape[2] == 3:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        low_saturation = (hsv[:, :, 1] <= thresholds.specular_saturation_threshold)
        candidates = saturated & low_saturation
    else:
        candidates = saturated

    candidate_count = int(np.count_nonzero(candidates))
    if candidate_count == 0:
        return 0.0

    total_pixels = gray.size
    raw_candidate_fraction = candidate_count / total_pixels

    # 3. Global blowout case (e.g. overexposed flash or test fixture with 100% white pixels)
    if raw_candidate_fraction >= thresholds.global_blowout_ratio:
        return float(min(1.0, max(0.0, raw_candidate_fraction)))

    # 4. Localized specular highlight detection (isolates hotspots from broad diffuse white regions)
    raw_ksize = thresholds.local_neighborhood_ksize
    if raw_ksize <= 0:
        raw_ksize = 31
    if raw_ksize % 2 == 0:
        raw_ksize += 1
    max_odd_dim = max(3, (min(gray.shape[0], gray.shape[1]) // 2) * 2 + 1)
    ksize = min(raw_ksize, max_odd_dim)
    local_bg = cv2.boxFilter(gray, ddepth=-1, ksize=(ksize, ksize))
    local_contrast = gray.astype(np.int16) - local_bg.astype(np.int16)

    hotspot_edges = candidates & (local_contrast >= thresholds.local_contrast_threshold)

    if np.count_nonzero(hotspot_edges) == 0:
        return 0.0

    # Connect contiguous saturated regions that contain specular contrast edges
    num_labels, labels = cv2.connectedComponents(candidates.astype(np.uint8))
    active_labels = np.unique(labels[hotspot_edges])
    active_labels = active_labels[active_labels > 0]
    if len(active_labels) == 0:
        return 0.0

    specular_mask = np.isin(labels, active_labels)
    specular_pixels = int(np.count_nonzero(specular_mask))
    return float(min(1.0, max(0.0, specular_pixels / total_pixels)))


def compute_contrast(gray: np.ndarray) -> float:
    """
    Computes RMS contrast (standard deviation of grayscale pixel intensities).

    Returns 0.0 for completely uniform images; higher values correspond to greater
    contrast between packaging text and background.
    """
    if gray.size == 0:
        return 0.0
    return float(np.std(gray))


def compute_mean_luminance(gray: np.ndarray) -> float:
    """Computes global average grayscale intensity across the image (0.0 to 255.0)."""
    if gray.size == 0:
        return 0.0
    return float(np.mean(gray))


def evaluate_image_quality(
    image: Optional[np.ndarray],
    thresholds: Optional[QualityGateThresholds] = None,
    color_format: str = "BGR",
) -> ImageQualityResult:
    """
    Evaluates pre-flight packaging frame quality deterministically.

    Validates:
    1. Input array integrity (non-null, numpy ndarray, non-empty, finite values, valid dimensions).
    2. Blur via Laplacian variance against configurable threshold.
    3. Specular glare via localized saturation clipping ratio against configurable threshold.
    4. Contrast via intensity standard deviation against configurable threshold.
    5. Illumination via mean luminance against under/over-exposure bounds.
    6. Optional aspect ratio check against configurable threshold.

    Provides a strict distinction between invalid inputs (is_valid_input=False) and
    poor-quality images (is_valid_input=True, passed=False).
    """
    if thresholds is None:
        thresholds = QualityGateThresholds()

    # Input validation: Distinct from poor-quality image evaluation
    if image is None:
        return ImageQualityResult(
            passed=False,
            is_valid_input=False,
            blur_score=0.0,
            glare_score=0.0,
            contrast_score=0.0,
            mean_luminance=0.0,
            is_blurry=False,
            is_glared=False,
            is_low_contrast=False,
            is_dark=False,
            is_over_exposed=False,
            failure_reasons=["INVALID_INPUT: Input image is None."],
            details={"error": "NULL_INPUT"},
        )

    if not isinstance(image, np.ndarray):
        return ImageQualityResult(
            passed=False,
            is_valid_input=False,
            blur_score=0.0,
            glare_score=0.0,
            contrast_score=0.0,
            mean_luminance=0.0,
            is_blurry=False,
            is_glared=False,
            is_low_contrast=False,
            is_dark=False,
            is_over_exposed=False,
            failure_reasons=[f"INVALID_INPUT: Input must be a numpy.ndarray, got {type(image).__name__}."],
            details={"error": "INVALID_TYPE", "type": type(image).__name__},
        )

    if image.size == 0:
        return ImageQualityResult(
            passed=False,
            is_valid_input=False,
            blur_score=0.0,
            glare_score=0.0,
            contrast_score=0.0,
            mean_luminance=0.0,
            is_blurry=False,
            is_glared=False,
            is_low_contrast=False,
            is_dark=False,
            is_over_exposed=False,
            failure_reasons=["INVALID_INPUT: Input image array is empty (0 pixels)."],
            details={"error": "EMPTY_ARRAY"},
        )

    if np.issubdtype(image.dtype, np.floating):
        if np.isnan(image).any() or np.isinf(image).any():
            return ImageQualityResult(
                passed=False,
                is_valid_input=False,
                blur_score=0.0,
                glare_score=0.0,
                contrast_score=0.0,
                mean_luminance=0.0,
                is_blurry=False,
                is_glared=False,
                is_low_contrast=False,
                is_dark=False,
                is_over_exposed=False,
                failure_reasons=["INVALID_INPUT: Input image contains non-finite values (NaN or Inf)."],
                details={"error": "NON_FINITE_VALUES"},
            )

    if image.ndim not in (2, 3):
        return ImageQualityResult(
            passed=False,
            is_valid_input=False,
            blur_score=0.0,
            glare_score=0.0,
            contrast_score=0.0,
            mean_luminance=0.0,
            is_blurry=False,
            is_glared=False,
            is_low_contrast=False,
            is_dark=False,
            is_over_exposed=False,
            failure_reasons=[f"INVALID_INPUT: Invalid image dimensions: {image.ndim}D. Expected 2D or 3D array."],
            details={"error": "INVALID_DIMENSIONS", "ndim": image.ndim},
        )

    if image.shape[0] < 3 or image.shape[1] < 3:
        return ImageQualityResult(
            passed=False,
            is_valid_input=False,
            blur_score=0.0,
            glare_score=0.0,
            contrast_score=0.0,
            mean_luminance=0.0,
            is_blurry=False,
            is_glared=False,
            is_low_contrast=False,
            is_dark=False,
            is_over_exposed=False,
            failure_reasons=[f"INVALID_INPUT: Image resolution too small ({image.shape[0]}x{image.shape[1]}). Minimum 3x3 required."],
            details={"error": "RESOLUTION_TOO_LOW", "shape": list(image.shape)},
        )

    if image.ndim == 3 and image.shape[2] not in (1, 3, 4):
        return ImageQualityResult(
            passed=False,
            is_valid_input=False,
            blur_score=0.0,
            glare_score=0.0,
            contrast_score=0.0,
            mean_luminance=0.0,
            is_blurry=False,
            is_glared=False,
            is_low_contrast=False,
            is_dark=False,
            is_over_exposed=False,
            failure_reasons=[f"INVALID_INPUT: Unsupported number of color channels: {image.shape[2]}. Expected 1, 3, or 4."],
            details={"error": "INVALID_CHANNELS", "channels": image.shape[2]},
        )

    # Grayscale conversion
    try:
        gray = convert_to_grayscale(image, color_format=color_format)
    except Exception as exc:
        return ImageQualityResult(
            passed=False,
            is_valid_input=False,
            blur_score=0.0,
            glare_score=0.0,
            contrast_score=0.0,
            mean_luminance=0.0,
            is_blurry=False,
            is_glared=False,
            is_low_contrast=False,
            is_dark=False,
            is_over_exposed=False,
            failure_reasons=[f"INVALID_INPUT: Failed to convert image to grayscale: {str(exc)}"],
            details={"error": "CONVERSION_ERROR", "exception": str(exc)},
        )

    # Compute quality metrics
    blur_score = compute_laplacian_variance(gray)
    glare_score = compute_glare_candidate_ratio(image, gray, thresholds)
    contrast_score = compute_contrast(gray)
    mean_luminance = compute_mean_luminance(gray)

    h, w = gray.shape[:2]
    aspect_ratio = float(max(w / h, h / w))

    # Evaluate quality flags
    is_blurry = blur_score < thresholds.min_blur_score
    is_glared = glare_score > thresholds.max_glare_candidate_ratio
    is_low_contrast = contrast_score < thresholds.min_contrast_score
    is_dark = mean_luminance < thresholds.min_mean_luminance
    is_over_exposed = mean_luminance > thresholds.max_mean_luminance
    is_extreme_aspect_ratio = bool(
        thresholds.max_aspect_ratio is not None and aspect_ratio > thresholds.max_aspect_ratio
    )

    # Construct actionable failure reasons
    reasons: List[str] = []
    if is_blurry:
        reasons.append(
            f"Image is blurry (blur score: {blur_score:.1f} < threshold {thresholds.min_blur_score:.1f}). "
            "Please hold the camera steady and tap to focus on packaging text."
        )
    if is_glared:
        reasons.append(
            f"Specular glare detected ({glare_score * 100:.1f}% > threshold {thresholds.max_glare_candidate_ratio * 100:.1f}%). "
            "Please angle the light source away from shiny packaging foil or tilt the package."
        )
    if is_low_contrast:
        reasons.append(
            f"Low image contrast detected (contrast score: {contrast_score:.1f} < threshold {thresholds.min_contrast_score:.1f}). "
            "Please ensure distinct contrast between packaging text and background."
        )
    if is_dark:
        reasons.append(
            f"Image is underexposed/dark (mean luminance: {mean_luminance:.1f} < threshold {thresholds.min_mean_luminance:.1f}). "
            "Please increase ambient illumination."
        )
    if is_over_exposed:
        reasons.append(
            f"Image is overexposed (mean luminance: {mean_luminance:.1f} > threshold {thresholds.max_mean_luminance:.1f}). "
            "Please reduce direct light or harsh flash reflection."
        )
    if is_extreme_aspect_ratio:
        reasons.append(
            f"Extreme image aspect ratio ({aspect_ratio:.1f}:1 > threshold {thresholds.max_aspect_ratio:.1f}:1). "
            "Please capture the full product packaging within standard camera framing."
        )

    passed = not (
        is_blurry
        or is_glared
        or is_low_contrast
        or is_dark
        or is_over_exposed
        or is_extreme_aspect_ratio
    )

    return ImageQualityResult(
        passed=passed,
        is_valid_input=True,
        blur_score=round(blur_score, 2),
        glare_score=round(glare_score, 4),
        contrast_score=round(contrast_score, 2),
        mean_luminance=round(mean_luminance, 2),
        is_blurry=is_blurry,
        is_glared=is_glared,
        is_low_contrast=is_low_contrast,
        is_dark=is_dark,
        is_over_exposed=is_over_exposed,
        failure_reasons=reasons,
        details={
            "min_blur_threshold": thresholds.min_blur_score,
            "max_glare_threshold": thresholds.max_glare_candidate_ratio,
            "min_contrast_threshold": thresholds.min_contrast_score,
            "min_luminance_threshold": thresholds.min_mean_luminance,
            "max_luminance_threshold": thresholds.max_mean_luminance,
            "max_aspect_ratio_threshold": thresholds.max_aspect_ratio,
            "aspect_ratio": round(aspect_ratio, 2),
            "is_extreme_aspect_ratio": is_extreme_aspect_ratio,
            "global_blowout_ratio": thresholds.global_blowout_ratio,
            "local_neighborhood_ksize": thresholds.local_neighborhood_ksize,
            "image_shape": list(image.shape),
            "grayscale_shape": list(gray.shape),
        },
    )
