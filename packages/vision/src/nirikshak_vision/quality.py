"""
Nirikshak Vision Quality: Pure, deterministic optical pre-flight quality filters.

Evaluates image sharpness (Laplacian variance), specular glare candidates (localized
intensity saturation), and global illumination (mean luminance).
"""

from typing import List, Optional, Tuple
import cv2
import numpy as np

from .types import QualityGateResult, QualityGateThresholds


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Converts 2D or 3D image array to single-channel uint8 grayscale without mutating input.

    Assumes OpenCV standard BGR ordering for 3-channel images.
    """
    if image.dtype != np.uint8:
        # Normalize/clip float or other integer types safely without mutating caller array
        if np.issubdtype(image.dtype, np.floating):
            if np.isnan(image).any() or np.isinf(image).any():
                raise ValueError("Floating-point image array contains NaN or Inf values.")
            # If float in [0.0, 1.0], scale to [0, 255]
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
        if channels == 3:
            return cv2.cvtColor(clipped, cv2.COLOR_BGR2GRAY)
        if channels == 4:
            return cv2.cvtColor(clipped, cv2.COLOR_BGRA2GRAY)
        if channels == 1:
            return np.squeeze(clipped, axis=2).copy()

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
        # Saturated pixels exist, but they are uniformly diffuse without steep specular roll-off
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


def compute_mean_luminance(gray: np.ndarray) -> float:
    """Computes global average grayscale intensity across the image (0.0 to 255.0)."""
    if gray.size == 0:
        return 0.0
    return float(np.mean(gray))


def evaluate_image_quality(
    image: Optional[np.ndarray],
    thresholds: Optional[QualityGateThresholds] = None,
) -> QualityGateResult:
    """
    Evaluates pre-flight packaging frame quality deterministically.

    Validates:
    1. Input array integrity (non-null, valid dimensions, minimum 3x3 resolution).
    2. Blur via Laplacian variance against configurable threshold.
    3. Specular glare via localized saturation clipping ratio against configurable threshold.
    4. Exposure via mean luminance against under/over-exposure bounds.

    Returns an immutable QualityGateResult with plain-language remediation cues.
    """
    if thresholds is None:
        thresholds = QualityGateThresholds()

    # Input validation
    if image is None:
        return QualityGateResult(
            passed=False,
            blur_score=0.0,
            glare_candidate_ratio=0.0,
            mean_luminance=0.0,
            is_blurry=True,
            is_glared=False,
            is_under_exposed=False,
            is_over_exposed=False,
            remediation_cues=["Input image is None."],
            details={"error": "NULL_INPUT"},
        )

    if not isinstance(image, np.ndarray):
        return QualityGateResult(
            passed=False,
            blur_score=0.0,
            glare_candidate_ratio=0.0,
            mean_luminance=0.0,
            is_blurry=True,
            is_glared=False,
            is_under_exposed=False,
            is_over_exposed=False,
            remediation_cues=["Input must be a numpy.ndarray."],
            details={"error": "INVALID_TYPE", "type": type(image).__name__},
        )

    if image.size == 0:
        return QualityGateResult(
            passed=False,
            blur_score=0.0,
            glare_candidate_ratio=0.0,
            mean_luminance=0.0,
            is_blurry=True,
            is_glared=False,
            is_under_exposed=False,
            is_over_exposed=False,
            remediation_cues=["Input image array is empty (0 pixels)."],
            details={"error": "EMPTY_ARRAY"},
        )

    if np.issubdtype(image.dtype, np.floating):
        if np.isnan(image).any() or np.isinf(image).any():
            return QualityGateResult(
                passed=False,
                blur_score=0.0,
                glare_candidate_ratio=0.0,
                mean_luminance=0.0,
                is_blurry=True,
                is_glared=False,
                is_under_exposed=False,
                is_over_exposed=False,
                remediation_cues=["Input image contains non-finite values (NaN or Inf)."],
                details={"error": "NON_FINITE_VALUES"},
            )

    if image.ndim not in (2, 3):
        return QualityGateResult(
            passed=False,
            blur_score=0.0,
            glare_candidate_ratio=0.0,
            mean_luminance=0.0,
            is_blurry=True,
            is_glared=False,
            is_under_exposed=False,
            is_over_exposed=False,
            remediation_cues=[f"Invalid image dimensions: {image.ndim}D. Expected 2D or 3D array."],
            details={"error": "INVALID_DIMENSIONS", "ndim": image.ndim},
        )

    if image.shape[0] < 3 or image.shape[1] < 3:
        return QualityGateResult(
            passed=False,
            blur_score=0.0,
            glare_candidate_ratio=0.0,
            mean_luminance=0.0,
            is_blurry=True,
            is_glared=False,
            is_under_exposed=False,
            is_over_exposed=False,
            remediation_cues=[f"Image resolution too small ({image.shape[0]}x{image.shape[1]}). Minimum 3x3 required."],
            details={"error": "RESOLUTION_TOO_LOW", "shape": list(image.shape)},
        )

    if image.ndim == 3 and image.shape[2] not in (1, 3, 4):
        return QualityGateResult(
            passed=False,
            blur_score=0.0,
            glare_candidate_ratio=0.0,
            mean_luminance=0.0,
            is_blurry=True,
            is_glared=False,
            is_under_exposed=False,
            is_over_exposed=False,
            remediation_cues=[f"Unsupported number of color channels: {image.shape[2]}. Expected 1, 3, or 4."],
            details={"error": "INVALID_CHANNELS", "channels": image.shape[2]},
        )

    # Convert to grayscale
    try:
        gray = convert_to_grayscale(image)
    except Exception as exc:
        return QualityGateResult(
            passed=False,
            blur_score=0.0,
            glare_candidate_ratio=0.0,
            mean_luminance=0.0,
            is_blurry=True,
            is_glared=False,
            is_under_exposed=False,
            is_over_exposed=False,
            remediation_cues=[f"Failed to process image array: {str(exc)}"],
            details={"error": "CONVERSION_ERROR", "exception": str(exc)},
        )

    # Compute metrics
    blur_score = compute_laplacian_variance(gray)
    glare_candidate_ratio = compute_glare_candidate_ratio(image, gray, thresholds)
    mean_luminance = compute_mean_luminance(gray)

    # Evaluate flags
    is_blurry = blur_score < thresholds.min_blur_score
    is_glared = glare_candidate_ratio > thresholds.max_glare_candidate_ratio
    is_under_exposed = mean_luminance < thresholds.min_mean_luminance
    is_over_exposed = mean_luminance > thresholds.max_mean_luminance

    # Construct remediation cues
    cues: List[str] = []
    if is_blurry:
        cues.append(
            f"Image is blurry (score: {blur_score:.1f} < threshold {thresholds.min_blur_score:.1f}). "
            "Please hold the camera steady and re-focus on the packaging."
        )
    if is_glared:
        cues.append(
            f"Specular glare detected ({glare_candidate_ratio * 100:.1f}% > threshold {thresholds.max_glare_candidate_ratio * 100:.1f}%). "
            "Please angle the light source away from shiny packaging foil or tilt the package."
        )
    if is_under_exposed:
        cues.append(
            f"Image is underexposed (luminance: {mean_luminance:.1f} < threshold {thresholds.min_mean_luminance:.1f}). "
            "Please increase ambient lighting."
        )
    if is_over_exposed:
        cues.append(
            f"Image is overexposed (luminance: {mean_luminance:.1f} > threshold {thresholds.max_mean_luminance:.1f}). "
            "Please reduce direct light or harsh glare."
        )

    passed = not (is_blurry or is_glared or is_under_exposed or is_over_exposed)

    return QualityGateResult(
        passed=passed,
        blur_score=round(blur_score, 2),
        glare_candidate_ratio=round(glare_candidate_ratio, 4),
        mean_luminance=round(mean_luminance, 2),
        is_blurry=is_blurry,
        is_glared=is_glared,
        is_under_exposed=is_under_exposed,
        is_over_exposed=is_over_exposed,
        remediation_cues=cues,
        details={
            "min_blur_threshold": thresholds.min_blur_score,
            "max_glare_threshold": thresholds.max_glare_candidate_ratio,
            "min_luminance_threshold": thresholds.min_mean_luminance,
            "max_luminance_threshold": thresholds.max_mean_luminance,
            "global_blowout_ratio": thresholds.global_blowout_ratio,
            "local_neighborhood_ksize": thresholds.local_neighborhood_ksize,
            "image_shape": list(image.shape),
            "grayscale_shape": list(gray.shape),
        },
    )
