"""
Comprehensive unit and integration tests for Nirikshak OCR Subsystem (Member 1 Chunk 2).
"""

import os
from pathlib import Path
import cv2
import numpy as np
import pytest

from nirikshak_ocr import (
    OCREngine,
    NirikshakOCREngine,
    OCRConfig,
    OCRToken,
    OCRResult,
    ScriptType,
    DBNetDetector,
    SVTRRecognizer,
    ScriptRouter
)
from nirikshak_ocr.errors import (
    OCRError,
    ModelLoadError,
    InvalidImageError,
    GeometryError
)
from nirikshak_ocr.preprocessing import (
    resize_image_for_detection,
    normalize_detector_input,
    remap_polygon_to_original,
    resize_norm_recognizer_input
)
from nirikshak_ocr.utils import (
    validate_input_image,
    order_points_clockwise,
    calculate_polygon_height,
    sort_tokens_reading_order
)

SYNTH_DIR = Path("AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET/images")


@pytest.fixture(scope="module")
def default_config():
    return OCRConfig().resolve_paths()


@pytest.fixture(scope="module")
def ocr_engine(default_config):
    return OCREngine(default_config)


# ============================================================================
# 1. Configuration & Model Loading Error Tests
# ============================================================================

def test_missing_detector_model_raises_error():
    bad_cfg = OCRConfig(det_model_path="non_existent_detector.onnx")
    with pytest.raises(ModelLoadError, match="Detection ONNX model not found"):
        DBNetDetector(bad_cfg)


def test_missing_recognizer_model_raises_error():
    bad_cfg = OCRConfig(rec_en_model_path="non_existent_rec.onnx")
    with pytest.raises(ModelLoadError, match="Recognition ONNX model not found"):
        SVTRRecognizer(model_path="non_existent_rec.onnx", script=ScriptType.LATIN, config=bad_cfg)


# ============================================================================
# 2. Input Image Validation Tests (Step 9)
# ============================================================================

def test_validate_none_image():
    with pytest.raises(InvalidImageError, match="cannot be None"):
        validate_input_image(None)


def test_validate_empty_image():
    empty_arr = np.array([], dtype=np.uint8)
    with pytest.raises(InvalidImageError, match="empty or has invalid shape"):
        validate_input_image(empty_arr)


def test_validate_too_small_image():
    tiny = np.zeros((4, 4, 3), dtype=np.uint8)
    with pytest.raises(InvalidImageError, match="too small"):
        validate_input_image(tiny)


def test_validate_grayscale_conversion():
    gray = np.zeros((50, 50), dtype=np.uint8)
    converted = validate_input_image(gray)
    assert converted.ndim == 3
    assert converted.shape[2] == 3


def test_engine_safe_handling_of_invalid_input(ocr_engine):
    # Process must not crash when given invalid/empty image
    res = ocr_engine.extract(np.zeros((2, 2, 3), dtype=np.uint8), image_id="bad_01")
    assert isinstance(res, OCRResult)
    assert len(res.tokens) == 0
    assert len(res.warnings) > 0


# ============================================================================
# 3. Coordinate Remapping & Geometry Tests (Steps 2, 11)
# ============================================================================

def test_resize_aspect_ratio_and_multiples_of_32():
    dummy = np.zeros((720, 1280, 3), dtype=np.uint8)
    resized, rw, rh = resize_image_for_detection(dummy, max_side_len=960)
    h_res, w_res = resized.shape[:2]
    assert h_res % 32 == 0
    assert w_res % 32 == 0
    assert max(h_res, w_res) <= 960
    assert rw > 0.0
    assert rh > 0.0


def test_coordinate_remapping_roundtrip():
    orig_poly = np.array([[100.0, 200.0], [300.0, 200.0], [300.0, 250.0], [100.0, 250.0]])
    ratio_w = 0.5
    ratio_h = 0.5
    # Scaled down polygon
    scaled_poly = orig_poly * 0.5
    # Remap back
    restored = remap_polygon_to_original(scaled_poly, ratio_w, ratio_h)
    np.testing.assert_allclose(restored, orig_poly, atol=0.1)


def test_order_points_clockwise():
    # Unordered quad points
    unordered = np.array([[300.0, 250.0], [100.0, 200.0], [100.0, 250.0], [300.0, 200.0]])
    ordered = order_points_clockwise(unordered)
    # Expected: TL, TR, BR, BL
    np.testing.assert_allclose(ordered[0], [100.0, 200.0])
    np.testing.assert_allclose(ordered[1], [300.0, 200.0])
    np.testing.assert_allclose(ordered[2], [300.0, 250.0])
    np.testing.assert_allclose(ordered[3], [100.0, 250.0])


def test_calculate_polygon_height():
    poly = np.array([[0.0, 0.0], [100.0, 0.0], [100.0, 24.0], [0.0, 24.0]])
    h_px = calculate_polygon_height(poly)
    assert h_px == 24.0


# ============================================================================
# 4. Reading Order Sorting Tests (Step 13)
# ============================================================================

def test_reading_order_sorting():
    # Create 3 tokens out of order
    t_bottom = OCRToken(
        token_id="t3", text="Bottom", confidence=0.9,
        polygon=[[0.0, 100.0], [50.0, 100.0], [50.0, 120.0], [0.0, 120.0]],
        bbox=[0.0, 100.0, 50.0, 120.0]
    )
    t_top_right = OCRToken(
        token_id="t2", text="Right", confidence=0.9,
        polygon=[[60.0, 10.0], [100.0, 10.0], [100.0, 30.0], [60.0, 30.0]],
        bbox=[60.0, 10.0, 100.0, 30.0]
    )
    t_top_left = OCRToken(
        token_id="t1", text="Left", confidence=0.9,
        polygon=[[0.0, 10.0], [50.0, 10.0], [50.0, 30.0], [0.0, 30.0]],
        bbox=[0.0, 10.0, 50.0, 30.0]
    )

    sorted_toks = sort_tokens_reading_order([t_bottom, t_top_right, t_top_left])
    assert [t.token_id for t in sorted_toks] == ["t1", "t2", "t3"]
    assert sorted_toks[0].line_id == 0
    assert sorted_toks[1].line_id == 0
    assert sorted_toks[2].line_id == 1


# ============================================================================
# 5. Model Integration Tests (Synthetic Test Specimens)
# ============================================================================

def test_extract_english_synthetic_specimen(ocr_engine):
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    assert img_path.is_file(), f"Test fixture not found: {img_path}"
    
    result = ocr_engine.extract(str(img_path), image_id="synth_01_test")
    assert isinstance(result, OCRResult)
    assert result.image_width == 640
    assert result.image_height == 360
    assert len(result.tokens) >= 4

    # Check key text elements are present
    full_text = result.full_text
    assert "Net Qty" in full_text or "Unit Sale Price" in full_text or "Mfg Date" in full_text
    
    # Check polygon structure
    for tok in result.tokens:
        assert len(tok.polygon) == 4
        assert len(tok.bbox) == 4
        assert 0.0 <= tok.confidence <= 1.0
        assert tok.raw_pixel_height is not None
        assert tok.raw_pixel_height > 0.0


def test_extract_hindi_synthetic_specimen(ocr_engine):
    img_path = SYNTH_DIR / "SYNTH-02-HIN-FMCG.png"
    assert img_path.is_file(), f"Test fixture not found: {img_path}"
    
    result = ocr_engine.extract(str(img_path), image_id="synth_02_test")
    assert len(result.tokens) >= 3

    # Check Devanagari script routing
    dev_tokens = [t for t in result.tokens if t.script == ScriptType.DEVANAGARI]
    assert len(dev_tokens) >= 1
    assert result.routing_summary["devanagari"] >= 1


def test_nirikshak_ocr_engine_adapter(default_config):
    adapter = NirikshakOCREngine(config=default_config)
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    img = cv2.imread(str(img_path))
    
    observations = adapter.extract_text_tokens(img)
    assert len(observations) >= 4
    first_obs = observations[0]
    assert hasattr(first_obs, "token_id")
    assert hasattr(first_obs, "text")
    assert hasattr(first_obs, "bounding_box")
    assert first_obs.bounding_box.x_min >= 0.0
    assert first_obs.bounding_box.y_min >= 0.0
