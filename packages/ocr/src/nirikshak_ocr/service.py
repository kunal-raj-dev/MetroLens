"""
Production OCR Service Adapter for MetroLens / Nirikshak Monorepo.
Provides a clean, reusable, configuration-safe service layer between the raw
OCREngine and application consumers (apps/api, apps/worker, Member 3, Member 5).
"""

import io
import logging
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import cv2
import numpy as np

from nirikshak_shared.models.contracts import OCRObservation

from .config import OCRConfig
from .engine import OCREngine
from .errors import (
    InvalidImageError,
    ModelLoadError,
    OCRError,
    OCRServiceError,
    UnsupportedImageError,
)
from .types import OCRResult, OCRToken

logger = logging.getLogger("nirikshak_ocr.service")


class OCRService:
    """
    Thread-safe, high-level service adapter for Nirikshak OCR.
    Encapsulates:
    - OCREngine lifecycle management and session reuse (singleton/application lifespan)
    - Multimodal input normalization (bytes, file paths, numpy arrays)
    - Safe caller memory protection (immutable input guarantees)
    - Unified exception translation for HTTP / Service consumption
    - Downstream contract serialization (OCRObservation, JSON-ready dictionaries)
    """

    _instance: Optional["OCRService"] = None
    _instance_lock = threading.Lock()

    def __init__(self, config: Optional[OCRConfig] = None):
        """
        Initializes the OCR service with an optional configuration.
        Defaults strictly to B0_BASELINE_RAW (preprocessing_mode="raw").
        """
        self.config = config or OCRConfig(preprocessing_mode="raw", preprocess_target="crop")
        self._engine_lock = threading.Lock()
        
        try:
            self.engine = OCREngine(self.config)
        except Exception as e:
            logger.error("Failed to initialize OCREngine: %s", e)
            if isinstance(e, OCRError):
                raise
            raise ModelLoadError(f"OCR service failed to load models: {e}") from e

        logger.info(
            "OCRService initialized successfully (engine=%s, preprocessing_mode=%s, target=%s)",
            self.engine.config.det_model_path,
            self.config.preprocessing_mode,
            self.config.preprocess_target,
        )

    @classmethod
    def get_instance(cls, config: Optional[OCRConfig] = None) -> "OCRService":
        """
        Thread-safe singleton accessor for application lifespan management (e.g. FastAPI startup).
        Reuses the existing OCR engine and session pools across multiple requests.
        """
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls(config=config)
            return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Resets the singleton instance (primarily for test isolation)."""
        with cls._instance_lock:
            cls._instance = None

    def warmup(self) -> float:
        """
        Executes a warmup pass with a synthetic dummy frame to prime ONNX Runtime
        session execution providers and thread pools before handling live requests.
        Returns warmup latency in milliseconds.
        """
        dummy = np.full((128, 256, 3), 255, dtype=np.uint8)
        t_start = time.perf_counter()
        with self._engine_lock:
            self.engine.extract(dummy, image_id="warmup")
        warmup_ms = (time.perf_counter() - t_start) * 1000.0
        logger.info("OCRService warmup complete (%.2f ms)", warmup_ms)
        return round(warmup_ms, 2)

    def convert_image_input(
        self, image: Union[np.ndarray, bytes, bytearray, str, Path]
    ) -> np.ndarray:
        """
        Normalizes polymorphic application input into a valid BGR numpy ndarray.
        Guarantees that caller's source memory is NOT mutated.
        """
        if image is None:
            raise InvalidImageError("Input image cannot be None")

        # 1. Raw binary bytes or bytearray (e.g. FastAPI UploadFile.read())
        if isinstance(image, (bytes, bytearray)):
            if len(image) == 0:
                raise InvalidImageError("Input image bytes cannot be empty (0 bytes)")
            
            buf = np.frombuffer(image, dtype=np.uint8)
            decoded = cv2.imdecode(buf, cv2.IMREAD_COLOR)
            if decoded is None or decoded.size == 0:
                raise UnsupportedImageError(
                    "Failed to decode image from binary bytes. Unsupported or corrupted format."
                )
            if (decoded.shape[0] * decoded.shape[1]) > (64 * 1024 * 1024):
                raise UnsupportedImageError(
                    f"Image resolution ({decoded.shape[1]}x{decoded.shape[0]}) exceeds 64MP decompression bomb threshold (ADR-014)."
                )
            return decoded

        # 2. Filesystem path (str or Path)
        if isinstance(image, (str, Path)):
            p = Path(image).resolve()
            if not p.is_file():
                raise InvalidImageError(f"Image file does not exist on disk: {p}")
            
            decoded = cv2.imread(str(p), cv2.IMREAD_COLOR)
            if decoded is None or decoded.size == 0:
                raise UnsupportedImageError(f"Failed to read or decode image file: {p}")
            if (decoded.shape[0] * decoded.shape[1]) > (64 * 1024 * 1024):
                raise UnsupportedImageError(
                    f"Image resolution ({decoded.shape[1]}x{decoded.shape[0]}) exceeds 64MP decompression bomb threshold (ADR-014)."
                )
            return decoded

        # 3. Existing Numpy ndarray
        if isinstance(image, np.ndarray):
            if image.size == 0:
                raise InvalidImageError("Input numpy array is empty (size 0)")
            if image.ndim not in (2, 3):
                raise UnsupportedImageError(
                    f"Unsupported image array dimensions: ndim={image.ndim}. Must be 2 (grayscale) or 3 (color)."
                )
            if image.shape[0] < 4 or image.shape[1] < 4:
                raise InvalidImageError(
                    f"Image dimensions too small ({image.shape[1]}x{image.shape[0]}). Minimum supported is 4x4."
                )
            if (image.shape[0] * image.shape[1]) > (64 * 1024 * 1024):
                raise UnsupportedImageError(
                    f"Image resolution ({image.shape[1]}x{image.shape[0]}) exceeds 64MP decompression bomb threshold (ADR-014)."
                )

            # Defensive copy to ensure caller's array is never mutated in-place
            copied = image.copy()

            if copied.ndim == 2:
                copied = cv2.cvtColor(copied, cv2.COLOR_GRAY2BGR)
            elif copied.ndim == 3 and copied.shape[2] == 4:
                copied = cv2.cvtColor(copied, cv2.COLOR_BGRA2BGR)
            elif copied.ndim == 3 and copied.shape[2] != 3:
                raise UnsupportedImageError(
                    f"Unsupported image channel count: {copied.shape[2]}. Expected 1, 3, or 4."
                )
            
            if copied.dtype != np.uint8:
                copied = np.clip(copied, 0, 255).astype(np.uint8)
            return copied

        raise UnsupportedImageError(f"Unsupported input type for OCR: {type(image)}")

    def extract(
        self,
        image: Union[np.ndarray, bytes, bytearray, str, Path],
        image_id: str = "img_001",
        language_hint: Optional[str] = None,
    ) -> OCRResult:
        """
        Synchronously extracts multilingual text from an image with bounding polygons.
        Returns strongly-typed OCRResult.
        """
        valid_img = self.convert_image_input(image)

        t_start = time.perf_counter()
        try:
            with self._engine_lock:
                result = self.engine.extract(
                    valid_img, image_id=image_id, language_hint=language_hint
                )
            elapsed_ms = (time.perf_counter() - t_start) * 1000.0
            logger.debug(
                "OCR extraction completed for '%s' in %.2f ms (%d tokens)",
                image_id,
                elapsed_ms,
                len(result.tokens),
            )
            return result
        except OCRError:
            raise
        except Exception as e:
            logger.exception("Unexpected error during OCR extraction for '%s': %s", image_id, e)
            raise OCRServiceError(
                f"OCR extraction failed unexpectedly for '{image_id}': {e}",
                cause=e,
            ) from e

    def extract_observations(
        self,
        image: Union[np.ndarray, bytes, bytearray, str, Path],
        image_id: str = "img_001",
        language_hint: Optional[str] = None,
    ) -> List[OCRObservation]:
        """
        Convenience adapter method returning canonical OCRObservations
        for downstream Member 3 (Rule Engine) and Member 4 (Evidence Dossier).
        """
        result = self.extract(image, image_id=image_id, language_hint=language_hint)
        return result.to_observations()

    def extract_dict(
        self,
        image: Union[np.ndarray, bytes, bytearray, str, Path],
        image_id: str = "img_001",
        language_hint: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Convenience adapter method returning a JSON-serializable dictionary
        for Member 4's FastAPI response and Member 5's React Canvas.
        """
        result = self.extract(image, image_id=image_id, language_hint=language_hint)
        
        # Serialize tokens conforming to API and Frontend needs
        serialized_tokens = []
        for t in result.tokens:
            serialized_tokens.append({
                "token_id": t.token_id,
                "text": t.text,
                "confidence": float(round(t.confidence, 4)),
                "polygon": t.polygon,
                "bbox": [float(round(c, 2)) for c in t.bbox],
                "script": t.script.value,
                "line_id": t.line_id,
                "raw_pixel_height": float(round(t.raw_pixel_height, 2)) if t.raw_pixel_height else None,
                "model_name": t.model_name,
            })

        # Canonical OCRObservations serialization
        serialized_observations = [obs.model_dump() for obs in result.to_observations()]

        return {
            "status": "SUCCESS",
            "image_id": result.image_id,
            "image_width": result.image_width,
            "image_height": result.image_height,
            "token_count": len(result.tokens),
            "tokens": serialized_tokens,
            "observations": serialized_observations,
            "full_text": result.full_text,
            "engine": result.engine,
            "detector_model": result.detector_model,
            "recognizer_models": result.recognizer_models,
            "processing_time_ms": result.processing_time_ms,
            "stage_timings": result.stage_timings,
            "routing_summary": result.routing_summary,
            "warnings": result.warnings,
        }
