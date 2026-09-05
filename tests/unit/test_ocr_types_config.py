"""
Unit tests for Nirikshak OCR types, configuration, and errors.
"""

import pytest
import math
from nirikshak_ocr.config import OCRConfig
from nirikshak_ocr.types import OCRToken, OCRResult, ScriptType
from nirikshak_ocr.errors import (
    OCRError,
    ConfigurationError,
    ModelLoadError,
    InvalidImageError,
    GeometryError
)


def test_ocr_config_defaults():
    config = OCRConfig()
    assert config.intra_op_num_threads == 4
    assert config.max_side_len == 960
    assert config.confidence_review_threshold == 0.60
    assert config.runtime_provider == "CPUExecutionProvider"


def test_ocr_token_valid_quad():
    token = OCRToken(
        token_id="tok_001",
        text="MRP Rs. 145.00",
        confidence=0.98,
        polygon=[[10.0, 20.0], [110.0, 20.0], [110.0, 50.0], [10.0, 50.0]],
        bbox=[10.0, 20.0, 110.0, 50.0],
        script=ScriptType.LATIN,
        line_id=0,
        raw_pixel_height=30.0,
        model_name="SVTR-EN"
    )
    assert token.token_id == "tok_001"
    assert token.text == "MRP Rs. 145.00"
    assert token.script == ScriptType.LATIN
    assert token.raw_pixel_height == 30.0

    # Test conversion to shared OCRObservation
    obs = token.to_observation()
    assert obs.token_id == "tok_001"
    assert obs.text == "MRP Rs. 145.00"
    assert obs.bounding_box.x_min == 10.0
    assert obs.bounding_box.y_min == 20.0
    assert obs.bounding_box.x_max == 110.0
    assert obs.bounding_box.y_max == 50.0
    assert obs.language == "en"


def test_ocr_token_invalid_polygon_points():
    with pytest.raises(ValueError, match="exactly 4 vertices"):
        OCRToken(
            token_id="tok_bad",
            text="Invalid",
            confidence=0.5,
            polygon=[[10.0, 20.0], [110.0, 20.0], [110.0, 50.0]],
            bbox=[10.0, 20.0, 110.0, 50.0]
        )


def test_ocr_token_nan_coordinates():
    with pytest.raises(ValueError, match="finite numbers"):
        OCRToken(
            token_id="tok_nan",
            text="Invalid",
            confidence=0.5,
            polygon=[[float("nan"), 20.0], [110.0, 20.0], [110.0, 50.0], [10.0, 50.0]],
            bbox=[10.0, 20.0, 110.0, 50.0]
        )


def test_ocr_result_structure():
    token1 = OCRToken(
        token_id="tok_001",
        text="Line 1",
        confidence=0.95,
        polygon=[[0.0, 0.0], [100.0, 0.0], [100.0, 20.0], [0.0, 20.0]],
        bbox=[0.0, 0.0, 100.0, 20.0],
        script=ScriptType.LATIN
    )
    token2 = OCRToken(
        token_id="tok_002",
        text="निवल मात्रा 500g",
        confidence=0.92,
        polygon=[[0.0, 30.0], [120.0, 30.0], [120.0, 55.0], [0.0, 55.0]],
        bbox=[0.0, 30.0, 120.0, 55.0],
        script=ScriptType.DEVANAGARI
    )
    res = OCRResult(
        image_id="test_img_01",
        image_width=1200,
        image_height=800,
        tokens=[token1, token2],
        processing_time_ms=125.4
    )
    assert res.full_text == "Line 1\nनिवल मात्रा 500g"
    obs_list = res.to_observations()
    assert len(obs_list) == 2
    assert obs_list[1].language == "hi"


def test_typed_errors():
    with pytest.raises(OCRError):
        raise ConfigurationError("Bad config")
    with pytest.raises(OCRError):
        raise ModelLoadError("Model missing")
    with pytest.raises(OCRError):
        raise InvalidImageError("Null image")
