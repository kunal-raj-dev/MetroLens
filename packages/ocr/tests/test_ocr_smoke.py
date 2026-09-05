"""
Smoke test for nirikshak-ocr.
"""

import numpy as np
from nirikshak_ocr import NirikshakOCREngine


def test_ocr_engine_initialization():
    engine = NirikshakOCREngine(languages=["en", "hi"])
    assert "en" in engine.languages
    # Empty image check
    empty_img = np.zeros((100, 100, 3), dtype=np.uint8)
    res = engine.extract_text_tokens(empty_img)
    assert isinstance(res, list)
