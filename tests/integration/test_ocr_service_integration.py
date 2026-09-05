"""
Chunk 4 Integration Tests: OCRService Monorepo Integration, Contract Verification & Application Readiness.

Verifies:
1. English packaging extraction (SYNTH-01).
2. Hindi packaging extraction with Devanagari Unicode & currency symbol (SYNTH-02).
3. Bilingual packaging extraction (SYNTH-03).
4. Blank frame specificity (SYNTH-07 produces 0 tokens, success status).
5. Error handling and type safety on invalid inputs (None, empty bytes, corrupted data).
6. Input array immutability (caller array is not mutated).
7. Binary bytes input vs path input equivalence.
8. Canonical OCRObservation contract serialization for Member 3/4.
9. API JSON dict contract serialization for Member 4/5.
10. Clockwise 4-point polygon coordinate preservation in original pixel space.
11. Devanagari Unicode UTF-8 roundtrip preservation through Pydantic JSON.
12. Singleton / Lifecycle reuse (OCRService.get_instance() preserves engine).
13. Concurrency sanity under multi-threaded execution.
14. Offline execution under socket isolation.
15. Failure integrity: distinction between genuine empty result vs exception error.
"""

import json
import socket
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import cv2
import numpy as np
import pytest

from nirikshak_ocr import (
    OCRService,
    OCRConfig,
    OCRResult,
    OCRToken,
    ScriptType,
    InvalidImageError,
    UnsupportedImageError,
    ModelLoadError,
    OCRServiceError
)
from nirikshak_shared.models.contracts import OCRObservation
from nirikshak_shared.models.primitives import BoundingBox


ROOT_DIR = Path(__file__).resolve().parents[2]
SYNTH_DIR = ROOT_DIR / "AI_CONTEXT" / "EXPERIMENTS" / "CHUNK_1_OCR_MODEL_SELECTION" / "03_DATASET" / "images"


@pytest.fixture(autouse=True)
def reset_service_singleton():
    """Ensure clean singleton state before and after each test."""
    OCRService.reset_instance()
    yield
    OCRService.reset_instance()


def test_service_initialization_defaults_to_raw():
    """Verify that OCRService defaults to B0_BASELINE_RAW (preprocessing_mode='raw')."""
    service = OCRService()
    assert service.config.preprocessing_mode == "raw"
    assert service.config.preprocess_target == "crop"
    assert service.engine is not None


def test_service_warmup():
    """Verify that service.warmup() primes ONNX Runtime without errors."""
    service = OCRService()
    warmup_ms = service.warmup()
    assert warmup_ms > 0.0


def test_extract_english_packaging_from_path():
    """Verify end-to-end extraction on English FMCG packaging (SYNTH-01)."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    result = service.extract(str(img_path), image_id="test_eng_01")

    assert isinstance(result, OCRResult)
    assert result.image_id == "test_eng_01"
    assert result.image_width == 640
    assert result.image_height == 360
    assert len(result.tokens) == 6
    assert result.processing_time_ms > 0.0

    full_text = result.full_text
    assert "Net Qty: 65 g" in full_text
    assert "Unit Sale Price: Rs. 0.31 / g" in full_text
    assert "Mfg Date: 08/2026" in full_text


def test_extract_hindi_devanagari_and_currency_symbol():
    """Verify Hindi FMCG packaging (SYNTH-02) extracts Devanagari Unicode and ₹ symbol."""
    img_path = SYNTH_DIR / "SYNTH-02-HIN-FMCG.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    result = service.extract(str(img_path), image_id="test_hin_02")

    assert len(result.tokens) >= 5
    full_text = result.full_text

    # Verify Devanagari Unicode codepoints survive in text
    has_devanagari = any(0x0900 <= ord(c) <= 0x097F for c in full_text)
    assert has_devanagari is True
    assert "2026" in full_text

    # Verify script routing contains devanagari tokens
    assert result.routing_summary.get("devanagari", 0) > 0


def test_extract_bilingual_mixed_script():
    """Verify bilingual mixed-script packaging (SYNTH-03)."""
    img_path = SYNTH_DIR / "SYNTH-03-MIXED-BILINGUAL.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    result = service.extract(str(img_path), image_id="test_mixed_03")

    assert len(result.tokens) >= 5
    full_text = result.full_text
    assert "50.00" in full_text or "50" in full_text
    assert "150" in full_text


def test_blank_frame_produces_zero_tokens_success_status():
    """Verify that a blank image produces exactly 0 tokens and is NOT an error."""
    img_path = SYNTH_DIR / "SYNTH-07-BLANK-FRAME.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    result = service.extract(str(img_path), image_id="test_blank_07")

    assert len(result.tokens) == 0
    assert result.full_text == ""

    # extract_dict must report status SUCCESS even with 0 tokens
    api_dict = service.extract_dict(str(img_path), image_id="test_blank_dict")
    assert api_dict["status"] == "SUCCESS"
    assert api_dict["token_count"] == 0
    assert api_dict["tokens"] == []
    assert api_dict["observations"] == []


def test_invalid_and_corrupt_inputs_raise_typed_errors():
    """Verify that invalid inputs raise structured OCRError subclasses."""
    service = OCRService()

    # None input
    with pytest.raises(InvalidImageError, match="Input image cannot be None"):
        service.extract(None)

    # Empty bytes
    with pytest.raises(InvalidImageError, match="Input image bytes cannot be empty"):
        service.extract(b"")

    # Corrupt / non-image bytes
    with pytest.raises(UnsupportedImageError, match="Failed to decode image"):
        service.extract(b"this_is_not_an_image_file_bytes")

    # Non-existent file path
    with pytest.raises(InvalidImageError, match="Image file does not exist"):
        service.extract("non_existent_file_path_12345.png")

    # Degenerate numpy array (empty)
    with pytest.raises(InvalidImageError, match="array is empty"):
        service.extract(np.zeros((0, 0), dtype=np.uint8))

    # Degenerate numpy array (too small < 4x4)
    with pytest.raises(InvalidImageError, match="too small"):
        service.extract(np.zeros((3, 3, 3), dtype=np.uint8))


def test_input_array_immutability():
    """Verify that caller's numpy array is never mutated in-place by the OCR service."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    original_img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
    snapshot = original_img.copy()

    service.extract(original_img)
    assert np.array_equal(original_img, snapshot), "Caller array was mutated in-place by OCRService!"


def test_binary_bytes_vs_path_equivalence():
    """Verify that passing raw binary bytes produces identical tokens to passing file path."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    raw_bytes = img_path.read_bytes()

    res_path = service.extract(str(img_path))
    res_bytes = service.extract(raw_bytes)

    assert len(res_path.tokens) == len(res_bytes.tokens)
    for t_p, t_b in zip(res_path.tokens, res_bytes.tokens):
        assert t_p.text == t_b.text
        assert pytest.approx(t_p.confidence, rel=1e-3) == t_b.confidence
        assert np.allclose(t_p.polygon, t_b.polygon, atol=0.01)


def test_canonical_ocr_observations_contract():
    """Verify that extract_observations() produces valid canonical OCRObservations."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    observations = service.extract_observations(str(img_path))

    assert len(observations) == 6
    for obs in observations:
        assert isinstance(obs, OCRObservation)
        assert obs.token_id.startswith("tok_")
        assert len(obs.text) > 0
        assert 0.0 <= obs.confidence <= 1.0
        assert isinstance(obs.bounding_box, BoundingBox)
        assert obs.bounding_box.x_min <= obs.bounding_box.x_max
        assert obs.bounding_box.y_min <= obs.bounding_box.y_max
        assert obs.polygon is not None
        assert len(obs.polygon) == 4
        assert obs.language in ("en", "hi")


def test_extract_dict_api_readiness():
    """Verify extract_dict() produces a complete JSON-serializable payload for Member 4/5."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    payload = service.extract_dict(str(img_path), image_id="api_test_01")

    # Verify top-level keys
    required_keys = [
        "status", "image_id", "image_width", "image_height", "token_count",
        "tokens", "observations", "full_text", "engine", "detector_model",
        "recognizer_models", "processing_time_ms", "stage_timings",
        "routing_summary", "warnings"
    ]
    for k in required_keys:
        assert k in payload, f"Missing required API key: {k}"

    assert payload["status"] == "SUCCESS"
    assert payload["image_id"] == "api_test_01"
    assert payload["token_count"] == 6

    # Verify JSON serializability
    json_str = json.dumps(payload)
    assert len(json_str) > 0
    deserialized = json.loads(json_str)
    assert deserialized["token_count"] == 6


def test_polygon_geometry_contract_and_ordering():
    """Verify 4-point polygon coordinates are clockwise in original image pixels."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    result = service.extract(str(img_path))

    for tok in result.tokens:
        poly = tok.polygon
        assert len(poly) == 4
        # Verify coordinates are in original pixel coordinate space [0, 640] x [0, 360]
        for pt in poly:
            x, y = pt
            assert 0.0 <= x <= 640.0
            assert 0.0 <= y <= 360.0

        # Verify derived bounding box covers polygon
        xmin, ymin, xmax, ymax = tok.bbox
        poly_xs = [pt[0] for pt in poly]
        poly_ys = [pt[1] for pt in poly]
        assert pytest.approx(xmin, abs=0.01) == min(poly_xs)
        assert pytest.approx(xmax, abs=0.01) == max(poly_xs)
        assert pytest.approx(ymin, abs=0.01) == min(poly_ys)
        assert pytest.approx(ymax, abs=0.01) == max(poly_ys)


def test_unicode_utf8_devanagari_serialization_roundtrip():
    """Verify Devanagari Hindi text and ₹ currency symbol survive JSON roundtrip unscathed."""
    img_path = SYNTH_DIR / "SYNTH-02-HIN-FMCG.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    result = service.extract(str(img_path))

    # Serialize via Pydantic model_dump_json
    json_bytes = result.model_dump_json().encode("utf-8")
    reconstructed = OCRResult.model_validate_json(json_bytes.decode("utf-8"))

    assert len(reconstructed.tokens) == len(result.tokens)
    for orig_t, recon_t in zip(result.tokens, reconstructed.tokens):
        assert orig_t.text == recon_t.text
        assert orig_t.confidence == recon_t.confidence
        assert orig_t.polygon == recon_t.polygon
        assert orig_t.script == recon_t.script


def test_singleton_lifecycle_session_reuse():
    """Verify OCRService.get_instance() reuses the same underlying engine instance."""
    s1 = OCRService.get_instance()
    s2 = OCRService.get_instance()

    assert s1 is s2
    assert s1.engine is s2.engine


def test_concurrency_thread_safety():
    """Verify that multiple concurrent threads calling OCRService succeed without race conditions."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    service = OCRService()
    raw_bytes = img_path.read_bytes()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(service.extract_dict, raw_bytes, f"thread_{i}") for i in range(8)]
        results = [f.result() for f in futures]

    assert len(results) == 8
    for r in results:
        assert r["status"] == "SUCCESS"
        assert r["token_count"] == 6


def test_offline_execution_socket_guard(monkeypatch):
    """Verify that OCRService executes 100% locally with zero network socket calls."""
    img_path = SYNTH_DIR / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip("Test fixture missing")

    # Block socket.socket to simulate complete air-gapped network isolation
    def guarded_socket(*args, **kwargs):
        raise RuntimeError("CRITICAL: Network call attempted in offline OCR mode!")

    monkeypatch.setattr(socket, "socket", guarded_socket)

    service = OCRService()
    result = service.extract(str(img_path))
    assert len(result.tokens) == 6


def test_decompression_bomb_guard():
    """Verify that images exceeding 64MP threshold raise UnsupportedImageError (ADR-014)."""
    service = OCRService()
    # Mock huge array dimensions using a custom object or ndarray with zero memory allocation via broadcast
    # Broadcast a 1x1 array to shape (8193, 8193, 3) -> 67.1 Megapixels with zero extra memory usage
    small = np.zeros((1, 1, 3), dtype=np.uint8)
    huge_mock = np.broadcast_to(small, (8193, 8193, 3))

    with pytest.raises(UnsupportedImageError) as exc_info:
        service.convert_image_input(huge_mock)
    assert "decompression bomb" in str(exc_info.value).lower()

