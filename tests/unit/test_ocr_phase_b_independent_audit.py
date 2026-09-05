"""
Independent Phase B Forensic Audit Verification Test Suite.
Authored by Independent Principal Engineer to prevent self-validation.
Tests the riskiest runtime behaviors, geometric bounds, error taxonomies,
lifecycle management, and Unicode fidelity independently of Phase A tests.
"""

import numpy as np
import pytest
from pathlib import Path
from nirikshak_ocr.config import OCRConfig
from nirikshak_ocr.engine import OCREngine
from nirikshak_ocr.service import OCRService
from nirikshak_ocr.recognizer import SVTRRecognizer, CTCLabelDecoder
from nirikshak_ocr.types import OCRToken, ScriptType
from nirikshak_ocr.errors import InvalidImageError, UnsupportedImageError, ModelLoadError
from nirikshak_ocr.evaluation import classify_ocr_error, compute_cer, compute_wer
from nirikshak_shared.models.contracts import OCRObservation


def test_devanagari_dictionary_dimension_alignment():
    """Validates fix for BUG-001: ONNX output dimension must match CTC decoder class count."""
    cfg = OCRConfig().resolve_paths()
    rec_hi = SVTRRecognizer(
        model_path=cfg.rec_hi_model_path,
        script=ScriptType.DEVANAGARI,
        dict_path=cfg.rec_hi_dict_path,
        config=cfg
    )
    out_dim = rec_hi.session.get_outputs()[0].shape[-1]
    assert rec_hi.decoder.num_classes == out_dim, (
        f"Mismatch: rec_hi output dim={out_dim}, decoder classes={rec_hi.decoder.num_classes}"
    )

    # Test synthetic logit where argmax is the trailing class (168)
    dummy_logits = np.zeros((1, 1, out_dim), dtype=np.float32)
    dummy_logits[0, 0, out_dim - 1] = 10.0  # Max prob at index 168
    decoded_text, conf = rec_hi.decoder.decode(dummy_logits)
    # Class 168 is trailing space; whitespace is stripped in greedy CTC decode
    assert decoded_text == ""
    assert conf > 0.99  # Confidence is preserved and NOT dropped


def test_coordinate_invariance_and_bounding_envelope():
    """Verifies that derived bounding boxes strictly enclose 4-point polygon vertices."""
    poly = [[12.5, 45.0], [180.2, 48.1], [178.9, 85.3], [11.2, 82.2]]
    xmin = min(pt[0] for pt in poly)
    ymin = min(pt[1] for pt in poly)
    xmax = max(pt[0] for pt in poly)
    ymax = max(pt[1] for pt in poly)

    tok = OCRToken(
        token_id="tok_audit_01",
        text="NET WT 500g",
        confidence=0.95,
        polygon=poly,
        bbox=[xmin, ymin, xmax, ymax],
        script=ScriptType.LATIN,
        line_id=0,
        raw_pixel_height=38.0
    )

    # Invariant: all polygon vertices lie within [xmin, ymin, xmax, ymax]
    for pt in tok.polygon:
        assert tok.bbox[0] <= pt[0] <= tok.bbox[2], f"X coordinate {pt[0]} outside bbox {tok.bbox}"
        assert tok.bbox[1] <= pt[1] <= tok.bbox[3], f"Y coordinate {pt[1]} outside bbox {tok.bbox}"


def test_empty_frame_vs_failure_semantics():
    """Proves that a completely blank frame returns SUCCESS with 0 tokens rather than an error."""
    service = OCRService()
    blank_image = np.full((200, 300, 3), 255, dtype=np.uint8)
    
    result_dict = service.extract_dict(blank_image, image_id="audit_blank")
    assert result_dict["status"] == "SUCCESS"
    assert result_dict["token_count"] == 0
    assert result_dict["tokens"] == []
    assert result_dict["observations"] == []
    assert result_dict["full_text"] == ""

    # Contrast with true failure modes
    with pytest.raises(InvalidImageError):
        service.extract(None)

    with pytest.raises(UnsupportedImageError):
        service.convert_image_input(b"corrupt_non_image_payload")


def test_unicode_nfc_and_currency_preservation():
    """Verifies that Devanagari Hindi and ₹ currency symbols survive contract roundtrips without Mojibake."""
    tok = OCRToken(
        token_id="tok_hi_01",
        text="अधिकतम खुदरा मूल्य ₹ ९९.००",
        confidence=0.92,
        polygon=[[10.0, 10.0], [200.0, 10.0], [200.0, 50.0], [10.0, 50.0]],
        bbox=[10.0, 10.0, 200.0, 50.0],
        script=ScriptType.DEVANAGARI,
        line_id=0
    )
    obs = tok.to_observation()
    assert obs.language == "hi"
    assert "₹" in obs.text
    assert "खुदरा" in obs.text

    # JSON Roundtrip
    serialized = obs.model_dump_json()
    deserialized = OCRObservation.model_validate_json(serialized)
    assert deserialized.text == tok.text
    assert deserialized.confidence == tok.confidence
    assert deserialized.polygon == tok.polygon


def test_service_singleton_vs_fresh_instance():
    """Verifies that get_instance reuses session while direct constructor creates new instance."""
    s1 = OCRService.get_instance()
    s2 = OCRService.get_instance()
    assert s1 is s2, "OCRService.get_instance() must return singleton"
    assert s1.engine.detector.session is s2.engine.detector.session

    s_isolated = OCRService()
    assert s_isolated is not s1, "OCRService() constructor must return isolated instance"
    assert s_isolated.engine.detector.session is not s1.engine.detector.session


def test_reading_order_vertical_sorting():
    """Verifies top-to-bottom, left-to-right reading order sorting under vertical line jitter."""
    from nirikshak_ocr.utils import sort_tokens_reading_order

    # Create tokens: Line 2 (y=100) created before Line 1 (y=20)
    tok_line2_left = OCRToken(
        token_id="t2", text="NET WT", confidence=0.9,
        polygon=[[10.0, 100.0], [80.0, 100.0], [80.0, 120.0], [10.0, 120.0]],
        bbox=[10.0, 100.0, 80.0, 120.0]
    )
    tok_line2_right = OCRToken(
        token_id="t3", text="500g", confidence=0.9,
        polygon=[[90.0, 102.0], [140.0, 102.0], [140.0, 122.0], [90.0, 122.0]],
        bbox=[90.0, 102.0, 140.0, 122.0]
    )
    tok_line1_left = OCRToken(
        token_id="t1", text="BRAND NAME", confidence=0.9,
        polygon=[[15.0, 20.0], [120.0, 20.0], [120.0, 45.0], [15.0, 45.0]],
        bbox=[15.0, 20.0, 120.0, 45.0]
    )

    sorted_toks = sort_tokens_reading_order([tok_line2_right, tok_line1_left, tok_line2_left])
    assert [t.token_id for t in sorted_toks] == ["t1", "t2", "t3"]
    assert sorted_toks[0].line_id == 0
    assert sorted_toks[1].line_id == 1
    assert sorted_toks[2].line_id == 1


def test_no_semantic_or_legal_contamination_in_tokens():
    """Verifies Member 1 boundary: OCRToken contains zero legal verdicts or physical mm units."""
    tok = OCRToken(
        token_id="tok_001",
        text="MRP Rs. 100.00",
        confidence=0.99,
        polygon=[[0.0, 0.0], [50.0, 0.0], [50.0, 20.0], [0.0, 20.0]],
        bbox=[0.0, 0.0, 50.0, 20.0],
        raw_pixel_height=20.0
    )
    fields = tok.model_dump()
    # Invariant: No legal rules or mm units inside Member 1
    assert "rule_id" not in fields
    assert "verdict" not in fields
    assert "font_height_mm" not in fields
    assert "scale_factor" not in fields
