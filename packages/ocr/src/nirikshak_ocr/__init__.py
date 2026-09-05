"""
Nirikshak OCR: Multilingual optical text detection and token extraction.
"""

from typing import List, Optional
import numpy as np
from nirikshak_shared.models.contracts import OCRObservation
from nirikshak_shared.models.primitives import BoundingBox


class NirikshakOCREngine:
    """Interface for pluggable OCR inference backends (e.g. RapidOCR, PaddleOCR)."""

    def __init__(self, languages: Optional[List[str]] = None):
        self.languages = languages or ["en", "hi"]

    def extract_text_tokens(self, image: np.ndarray) -> List[OCRObservation]:
        """
        Executes text detection and recognition on the supplied image.
        Returns a list of structured OCRObservation tokens.
        """
        if image is None or image.size == 0:
            return []

        # Concrete OCR integration points are populated by the AI/OCR lead.
        # Fallback empty list if uninitialized.
        return []


__all__ = ["NirikshakOCREngine", "OCRObservation"]
