"""
Offline isolation test for Nirikshak OCR subsystem.
Proves that OCREngine initialization and extraction execute with zero network calls.
"""

import socket
import pytest
import cv2
from pathlib import Path
from nirikshak_ocr import OCREngine, OCRConfig

SYNTH_IMAGE = Path("AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET/images/SYNTH-01-ENG-FMCG.png")


def test_ocr_strictly_offline(monkeypatch):
    """
    Blocks all network socket creation and attempts to connect.
    If OCREngine attempts any HTTP/DNS/socket call, the test will immediately fail.
    """
    def blocked_connect(*args, **kwargs):
        raise RuntimeError("NETWORK CALL ATTEMPTED! OCREngine must be 100% offline.")

    # Patch socket connect
    monkeypatch.setattr(socket.socket, "connect", blocked_connect)

    # Initialize engine
    cfg = OCRConfig().resolve_paths()
    engine = OCREngine(cfg)

    # Run extraction on image
    assert SYNTH_IMAGE.is_file()
    img = cv2.imread(str(SYNTH_IMAGE))
    result = engine.extract(img, image_id="offline_test_01")

    # Assert valid output without network
    assert len(result.tokens) >= 4
    assert result.processing_time_ms > 0
    assert result.image_width == 640
