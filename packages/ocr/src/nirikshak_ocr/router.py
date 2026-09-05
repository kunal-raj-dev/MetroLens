"""
Script routing logic for Nirikshak OCR subsystem.

IMPORTANT LIMITATION (STEP 8):
This router implements a controlled engineering heuristic.
It is an ENGINEERING HEURISTIC, NOT a verified neural script classifier.
Performance will be empirically calibrated once real Indian packaging datasets are collected.
"""

from typing import Tuple, Optional
import numpy as np

from .types import ScriptType
from .recognizer import SVTRRecognizer


class ScriptRouter:
    """
    Routes text line crops between Latin and Devanagari recognizers.
    Avoids running both recognizers over every crop unconditionally to maintain latency budgets.
    """

    ROUTING_METHOD = "heuristic_confidence_gate"

    def __init__(
        self,
        en_recognizer: SVTRRecognizer,
        hi_recognizer: SVTRRecognizer,
        confidence_fallback_margin: float = 0.15
    ):
        self.en_rec = en_recognizer
        self.hi_rec = hi_recognizer
        self.fallback_margin = confidence_fallback_margin

    def route_and_recognize(
        self,
        crop: np.ndarray,
        language_hint: Optional[str] = None
    ) -> Tuple[str, float, ScriptType, bool, str]:
        """
        Routes crop to the appropriate recognizer.
        Returns:
            (transcribed_text, confidence, script_type, fallback_used, model_name)
        """
        # 1. Explicit Language Hint Routing
        if language_hint == "hi":
            text, conf = self.hi_rec.recognize(crop)
            return text, conf, ScriptType.DEVANAGARI, False, "SVTR-HI"
        elif language_hint == "en":
            text, conf = self.en_rec.recognize(crop)
            return text, conf, ScriptType.LATIN, False, "SVTR-EN"

        # 2. Heuristic Confidence Gate (Default Auto Mode)
        # Primary pass: Execute English recognizer
        en_text, en_conf = self.en_rec.recognize(crop)

        # If English prediction is confident, accept without evaluating Hindi
        if en_conf >= 0.70 and len(en_text) >= 2:
            return en_text, en_conf, ScriptType.LATIN, False, "SVTR-EN"

        # Fallback evaluation: If English is uncertain, evaluate Devanagari recognizer
        hi_text, hi_conf = self.hi_rec.recognize(crop)

        # If Hindi model shows clear superiority, select Devanagari
        if hi_conf > (en_conf + self.fallback_margin) and len(hi_text) > 0:
            return hi_text, hi_conf, ScriptType.DEVANAGARI, True, "SVTR-HI"

        # If English is still better or equal
        if en_conf >= hi_conf:
            script = ScriptType.LATIN if en_conf >= 0.40 else ScriptType.UNKNOWN
            return en_text, en_conf, script, True, "SVTR-EN"
        else:
            script = ScriptType.DEVANAGARI if hi_conf >= 0.40 else ScriptType.UNKNOWN
            return hi_text, hi_conf, script, True, "SVTR-HI"
