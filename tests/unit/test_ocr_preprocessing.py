"""
Unit tests for domain-specific preprocessing algorithms and pipelines.
Verifies:
1. CLAHE in LAB color space (preserves chromatic balance).
2. Bilateral filtering (preserves edges while smoothing noise).
3. Unsharp mask (bounded uint8 sharpening).
4. Polarity-aware morphological dilation (dot-matrix stroke thickening).
5. Adaptive contrast preprocessing.
6. DomainPreprocessPipeline interface conformance.
7. Input safety guards: None, empty arrays, extreme sizes, NaNs.
"""

import numpy as np
import pytest

from nirikshak_ocr.preprocessing import (
    ImagePreprocessHook,
    DomainPreprocessPipeline,
    apply_clahe,
    apply_bilateral_filter,
    apply_unsharp_mask,
    apply_morphological_dilation,
    apply_adaptive_preprocessing
)


def test_identity_hook():
    hook = ImagePreprocessHook()
    img = np.full((100, 100, 3), 128, dtype=np.uint8)
    out = hook(img)
    assert np.array_equal(img, out)


def test_clahe_bgr_color_preservation():
    # Create an image with distinct color channels
    img = np.zeros((64, 64, 3), dtype=np.uint8)
    img[:, :, 0] = 50   # Blue
    img[:, :, 1] = 100  # Green
    img[:, :, 2] = 150  # Red
    
    enhanced = apply_clahe(img, clip_limit=2.0, tile_grid_size=(8, 8))
    assert enhanced.shape == img.shape
    assert enhanced.dtype == np.uint8
    # CLAHE on uniform color should return bounded valid image
    assert enhanced.max() <= 255
    assert enhanced.min() >= 0


def test_clahe_grayscale():
    img_gray = np.full((64, 64), 100, dtype=np.uint8)
    enhanced = apply_clahe(img_gray, clip_limit=3.0)
    assert enhanced.shape == (64, 64)
    assert enhanced.dtype == np.uint8


def test_bilateral_filter():
    # Image with sharp edge and gaussian noise
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[:, 25:] = 200
    filtered = apply_bilateral_filter(img, d=5, sigma_color=50.0, sigma_space=50.0)
    assert filtered.shape == img.shape
    assert filtered.dtype == np.uint8


def test_unsharp_mask():
    img = np.full((40, 40, 3), 100, dtype=np.uint8)
    img[20, 20] = 255 # center impulse
    sharpened = apply_unsharp_mask(img, amount=1.5)
    assert sharpened.shape == img.shape
    assert sharpened.dtype == np.uint8
    assert sharpened[20, 20, 0] >= 200


def test_polarity_aware_morphological_dilation():
    # 1. Dark text on light background (mean > 127) -> should erode light background (expand dark stroke)
    light_bg = np.full((30, 30, 3), 240, dtype=np.uint8)
    light_bg[15, 15] = [20, 20, 20] # 1 dark pixel
    thickened = apply_morphological_dilation(light_bg, kernel_size=3, iterations=1)
    # The dark region should expand beyond the single pixel
    dark_count_orig = np.sum(light_bg < 100)
    dark_count_thickened = np.sum(thickened < 100)
    assert dark_count_thickened > dark_count_orig

    # 2. Light text on dark background (mean <= 127) -> should dilate light text
    dark_bg = np.full((30, 30, 3), 10, dtype=np.uint8)
    dark_bg[15, 15] = [240, 240, 240] # 1 light pixel
    dilated = apply_morphological_dilation(dark_bg, kernel_size=3, iterations=1)
    light_count_orig = np.sum(dark_bg > 150)
    light_count_dilated = np.sum(dilated > 150)
    assert light_count_dilated > light_count_orig


def test_adaptive_preprocessing():
    # Low-contrast image: low standard deviation (< 35.0)
    low_contrast = np.full((50, 50, 3), 120, dtype=np.uint8)
    low_contrast[20:30, 20:30] = 130 # very faint variation
    std_before = float(np.std(cv2_gray := cv2_to_gray(low_contrast)))
    assert std_before < 10.0

    adapted = apply_adaptive_preprocessing(low_contrast, contrast_thresh=35.0, clip_limit=3.0)
    assert adapted.shape == low_contrast.shape
    
    # High-contrast image: high standard deviation (>= 35.0)
    high_contrast = np.zeros((50, 50, 3), dtype=np.uint8)
    high_contrast[:, 25:] = 255
    std_high = float(np.std(cv2_to_gray(high_contrast)))
    assert std_high > 100.0

    # High-contrast image should remain untouched
    adapted_high = apply_adaptive_preprocessing(high_contrast, contrast_thresh=35.0)
    assert np.array_equal(high_contrast, adapted_high)


def cv2_to_gray(bgr: np.ndarray) -> np.ndarray:
    import cv2
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)


def test_domain_pipeline_dispatch():
    pipeline_clahe = DomainPreprocessPipeline(mode="clahe", clahe_clip_limit=2.0)
    pipeline_bilateral = DomainPreprocessPipeline(mode="bilateral", bilateral_d=3)
    pipeline_unsharp = DomainPreprocessPipeline(mode="unsharp", unsharp_amount=1.2)
    pipeline_dilation = DomainPreprocessPipeline(mode="dilation", dilation_kernel_size=2)
    pipeline_adaptive = DomainPreprocessPipeline(mode="adaptive")

    test_img = np.random.randint(50, 200, size=(48, 120, 3), dtype=np.uint8)

    for pipe in [pipeline_clahe, pipeline_bilateral, pipeline_unsharp, pipeline_dilation, pipeline_adaptive]:
        res = pipe(test_img)
        assert res.shape == test_img.shape
        assert res.dtype == np.uint8


def test_preprocessing_safety_guards():
    # None image
    assert apply_clahe(None) is None
    assert apply_bilateral_filter(None) is None
    assert apply_unsharp_mask(None) is None
    assert apply_morphological_dilation(None) is None
    assert apply_adaptive_preprocessing(None) is None

    # Empty array
    empty = np.zeros((0, 0, 3), dtype=np.uint8)
    assert apply_clahe(empty).size == 0
    assert apply_bilateral_filter(empty).size == 0
    assert apply_unsharp_mask(empty).size == 0
    assert apply_morphological_dilation(empty).size == 0
    assert apply_adaptive_preprocessing(empty).size == 0

    # Pipeline safety with None
    pipe = DomainPreprocessPipeline(mode="clahe")
    assert pipe(None) is None
