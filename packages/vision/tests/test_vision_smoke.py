"""
Smoke test for nirikshak-vision quality gate.
"""

import numpy as np
from nirikshak_vision import check_image_quality


def test_quality_gate_synthetic_images():
    # Sharp, textured synthetic image
    sharp_image = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    res_sharp = check_image_quality(sharp_image, min_laplacian_variance=50.0)
    assert isinstance(res_sharp.passed, bool)
    assert res_sharp.laplacian_variance > 0

    # Flat, zero-texture image (simulating extreme blur)
    flat_image = np.full((200, 200, 3), 128, dtype=np.uint8)
    res_flat = check_image_quality(flat_image, min_laplacian_variance=50.0)
    assert not res_flat.passed
    assert res_flat.laplacian_variance == 0.0

    # High glare image (pure white specular reflection)
    glare_image = np.full((200, 200, 3), 255, dtype=np.uint8)
    res_glare = check_image_quality(glare_image, max_glare_ratio=0.10)
    assert not res_glare.passed
    assert res_glare.glare_ratio == 1.0
