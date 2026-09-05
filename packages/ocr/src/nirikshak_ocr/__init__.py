"""
Nirikshak OCR: High-performance, 100% local scene text detection and script-routed recognition.
"""

from typing import List, Optional
import numpy as np

from nirikshak_shared.models.contracts import OCRObservation

from .config import OCRConfig
from .types import OCRToken, OCRResult, ScriptType
from .detector import DBNetDetector
from .recognizer import SVTRRecognizer, CTCLabelDecoder
from .router import ScriptRouter
from .engine import OCREngine
from .preprocessing import (
    ImagePreprocessHook,
    DomainPreprocessPipeline,
    apply_clahe,
    apply_bilateral_filter,
    apply_unsharp_mask,
    apply_morphological_dilation,
    apply_adaptive_preprocessing
)
from .evaluation import (
    compute_cer,
    compute_wer,
    evaluate_numeric_accuracy,
    classify_ocr_error,
    levenshtein_distance,
    compute_routing_accuracy
)
from .service import OCRService
from .errors import (
    OCRError,
    ConfigurationError,
    ModelLoadError,
    InvalidImageError,
    UnsupportedImageError,
    InferenceError,
    GeometryError,
    OCRServiceError,
)



class NirikshakOCREngine:
    """
    Backward-compatible adapter for NirikshakOCREngine interface.
    Delegates to the high-performance OCREngine and emits canonical OCRObservation list.
    """

    def __init__(self, languages: Optional[List[str]] = None, config: Optional[OCRConfig] = None):
        self.languages = languages or ["en", "hi"]
        self.engine = OCREngine(config)

    def extract_text_tokens(self, image: np.ndarray) -> List[OCRObservation]:
        """
        Executes text detection and recognition on the supplied image.
        Returns a list of structured OCRObservation tokens.
        """
        if image is None or image.size == 0:
            return []
        result = self.engine.extract(image)
        return result.to_observations()


__all__ = [
    "OCREngine",
    "NirikshakOCREngine",
    "OCRConfig",
    "OCRToken",
    "OCRResult",
    "ScriptType",
    "DBNetDetector",
    "SVTRRecognizer",
    "CTCLabelDecoder",
    "ScriptRouter",
    "ImagePreprocessHook",
    "DomainPreprocessPipeline",
    "apply_clahe",
    "apply_bilateral_filter",
    "apply_unsharp_mask",
    "apply_morphological_dilation",
    "apply_adaptive_preprocessing",
    "compute_cer",
    "compute_wer",
    "evaluate_numeric_accuracy",
    "classify_ocr_error",
    "levenshtein_distance",
    "compute_routing_accuracy",
    "OCRError",
    "ConfigurationError",
    "ModelLoadError",
    "InvalidImageError",
    "UnsupportedImageError",
    "InferenceError",
    "GeometryError",
    "OCRServiceError",
    "OCRService",
]

