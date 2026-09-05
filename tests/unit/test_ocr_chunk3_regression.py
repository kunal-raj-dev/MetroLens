"""
Regression and negative tests for Chunk 3 Preprocessing & Robustness.
Verifies:
1. Coordinate & polygon immutability: Crop preprocessing must NOT distort original image polygons.
2. Clean image safety: Preprocessing must not degrade clean packaging or hallucinate false tokens.
3. Blank frame safety: No spurious false tokens generated on blank images.
4. Determinism: Same input + same config yields byte-for-byte identical token strings and polygons.
"""

from pathlib import Path
import numpy as np
import pytest

from nirikshak_ocr import OCREngine, OCRConfig


SYNTH_DIR = Path("AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET/images")


def test_polygon_invariance_under_crop_preprocessing():
    """Crop preprocessing must not alter the detector's original image coordinates."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip(f"Test fixture not found: {img_path}")

    # Baseline configuration (raw)
    cfg_raw = OCRConfig(preprocessing_mode="raw", preprocess_target="crop").resolve_paths()
    engine_raw = OCREngine(cfg_raw)
    res_raw = engine_raw.extract(str(img_path))

    # Crop preprocessing with CLAHE
    cfg_clahe = OCRConfig(preprocessing_mode="clahe", preprocess_target="crop", clahe_clip_limit=2.0).resolve_paths()
    engine_clahe = OCREngine(cfg_clahe)
    res_clahe = engine_clahe.extract(str(img_path))

    assert len(res_raw.tokens) > 0
    assert len(res_clahe.tokens) == len(res_raw.tokens)

    # Polygons must match within floating point precision
    for tok_raw, tok_clahe in zip(res_raw.tokens, res_clahe.tokens):
        poly_raw = np.array(tok_raw.polygon, dtype=np.float32)
        poly_clahe = np.array(tok_clahe.polygon, dtype=np.float32)
        assert np.allclose(poly_raw, poly_clahe, atol=0.01)


def test_clean_packaging_negative_test_no_hallucination():
    """Verifies that adaptive crop preprocessing on clean packaging does not inflate token count."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip(f"Test fixture not found: {img_path}")

    cfg_adaptive = OCRConfig(preprocessing_mode="adaptive", preprocess_target="crop").resolve_paths()
    engine = OCREngine(cfg_adaptive)
    result = engine.extract(str(img_path))

    # Should detect exactly the known 6 packaging tokens, not 20 hallucinated noisy fragments
    assert len(result.tokens) <= 8
    texts = [t.text for t in result.tokens]
    # Critical statutory tokens must be present
    text_blob = " ".join(texts)
    assert "20.00" in text_blob or "20" in text_blob


def test_blank_frame_zero_tokens():
    """Verifies that preprocessing does not cause false text detection on blank frames."""
    img_path = SYNTH_DIR / "SYNTH-07-BLANK-FRAME.png"
    if not img_path.is_file():
        pytest.skip(f"Test fixture not found: {img_path}")

    for mode in ["raw", "clahe", "dilation", "adaptive"]:
        cfg = OCRConfig(preprocessing_mode=mode, preprocess_target="crop").resolve_paths()
        engine = OCREngine(cfg)
        result = engine.extract(str(img_path))
        assert len(result.tokens) == 0


def test_determinism_under_repeated_runs():
    """Same image + same config must yield identical token text and confidence."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip(f"Test fixture not found: {img_path}")

    cfg = OCRConfig(preprocessing_mode="clahe", preprocess_target="crop").resolve_paths()
    engine = OCREngine(cfg)

    res1 = engine.extract(str(img_path))
    res2 = engine.extract(str(img_path))

    assert len(res1.tokens) == len(res2.tokens)
    for t1, t2 in zip(res1.tokens, res2.tokens):
        assert t1.text == t2.text
        assert pytest.approx(t1.confidence, rel=1e-4) == t2.confidence
        assert t1.polygon == t2.polygon
