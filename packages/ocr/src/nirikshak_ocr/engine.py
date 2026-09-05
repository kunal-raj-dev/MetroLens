"""
OCREngine: Unified, locally runnable scene text detection and script-routed recognition engine.
"""

from pathlib import Path
import time
from typing import Dict, List, Optional, Union
import cv2
import numpy as np

from .config import OCRConfig
from .detector import DBNetDetector
from .errors import InvalidImageError, OCRError
from .preprocessing import (
    ImagePreprocessHook,
    DomainPreprocessPipeline,
    apply_clahe,
    apply_bilateral_filter,
    apply_unsharp_mask,
    apply_morphological_dilation,
    apply_adaptive_preprocessing
)
from .recognizer import SVTRRecognizer
from .router import ScriptRouter
from .types import OCRResult, OCRToken, ScriptType
from .utils import (
    validate_input_image,
    get_rotate_crop_image,
    calculate_polygon_height,
    sort_tokens_reading_order
)


class OCREngine:
    """
    Public facade for the Nirikshak OCR subsystem.
    
    Conceptual Pipeline:
    IMAGE -> PREPROCESSING -> TEXT DETECTION (DBNet++) -> CROP -> CROP PREPROCESSING -> SCRIPT ROUTING -> RECOGNITION (SVTR) -> OCRResult
    
    Inviolable Architectural Boundaries:
    - Member 1 outputs raw geometry (polygons, bboxes, raw pixel heights).
    - Member 2 converts geometry into physical metrological dimensions (mm).
    - Member 3 interprets transcribed text semantically under Legal Metrology Rules.
    """

    def __init__(self, config: Optional[OCRConfig] = None):
        self.config = (config or OCRConfig()).resolve_paths()

        # Initialize detector session (loaded once)
        self.detector = DBNetDetector(self.config)

        # Initialize recognizer sessions (loaded once)
        self.en_recognizer = SVTRRecognizer(
            model_path=self.config.rec_en_model_path,
            script=ScriptType.LATIN,
            config=self.config
        )
        self.hi_recognizer = SVTRRecognizer(
            model_path=self.config.rec_hi_model_path,
            script=ScriptType.DEVANAGARI,
            dict_path=self.config.rec_hi_dict_path,
            config=self.config
        )

        # Initialize script router
        self.router = ScriptRouter(
            en_recognizer=self.en_recognizer,
            hi_recognizer=self.hi_recognizer
        )

        # Configure Image & Crop Preprocessing Hooks (Chunk 3)
        self._setup_preprocessing_pipelines()

    def _setup_preprocessing_pipelines(self) -> None:
        """Sets up image-level and crop-level preprocessing pipelines from config."""
        mode = self.config.preprocessing_mode.lower().strip()
        target = self.config.preprocess_target.lower().strip()

        if mode == "raw" or mode == "none":
            self.preprocessor_hook: ImagePreprocessHook = ImagePreprocessHook()
            self.crop_preprocessor_hook: ImagePreprocessHook = ImagePreprocessHook()
            return

        pipeline = DomainPreprocessPipeline(
            mode=mode,
            clahe_clip_limit=self.config.clahe_clip_limit,
            clahe_tile_grid_size=self.config.clahe_tile_grid_size,
            bilateral_d=self.config.bilateral_d,
            bilateral_sigma_color=self.config.bilateral_sigma_color,
            bilateral_sigma_space=self.config.bilateral_sigma_space,
            unsharp_amount=self.config.unsharp_amount,
            dilation_kernel_size=self.config.dilation_kernel_size,
            dilation_iterations=self.config.dilation_iterations,
            adaptive_contrast_threshold=self.config.adaptive_contrast_threshold
        )

        if target in ("image", "both"):
            self.preprocessor_hook = pipeline
        else:
            self.preprocessor_hook = ImagePreprocessHook()

        if target in ("crop", "both"):
            self.crop_preprocessor_hook = pipeline
        else:
            self.crop_preprocessor_hook = ImagePreprocessHook()

    def extract(
        self,
        image: Union[np.ndarray, str, Path],
        image_id: Optional[str] = None,
        language_hint: Optional[str] = None
    ) -> OCRResult:
        """
        Executes end-to-end scene text extraction on an image.
        
        Args:
            image: Input image as BGR numpy array or filesystem path.
            image_id: Optional string tracking ID for the image.
            language_hint: Optional hint ("en", "hi", or "auto") to guide script routing.
            
        Returns:
            OCRResult object with extracted tokens, coordinates, timings, and diagnostic warnings.
        """
        t_start = time.perf_counter()
        img_id = image_id or "img_001"

        # 1. Image Resolution & Validation
        if isinstance(image, (str, Path)):
            p = Path(image)
            if not p.is_file():
                raise InvalidImageError(f"Image file not found: {p}")
            img_bgr = cv2.imread(str(p))
            if img_bgr is None:
                raise InvalidImageError(f"Failed to decode image from path: {p}")
        else:
            img_bgr = image

        try:
            valid_img = validate_input_image(img_bgr)
        except InvalidImageError as e:
            # Handle invalid image safely without crashing process
            return OCRResult(
                image_id=img_id,
                image_width=1,
                image_height=1,
                tokens=[],
                warnings=[f"Invalid input image: {str(e)}"],
                processing_time_ms=round((time.perf_counter() - t_start) * 1000.0, 2)
            )

        orig_h, orig_w = valid_img.shape[:2]

        # 2. Preprocessing Hook
        t_prep_start = time.perf_counter()
        processed_img = self.preprocessor_hook(valid_img)
        t_prep_ms = (time.perf_counter() - t_prep_start) * 1000.0

        # 3. Text Detection (DBNet++)
        t_det_start = time.perf_counter()
        polygons, det_scores = self.detector.detect(processed_img)
        t_det_ms = (time.perf_counter() - t_det_start) * 1000.0

        # 4. Script Routing & Recognition (SVTR)
        t_rec_start = time.perf_counter()
        tokens: List[OCRToken] = []
        routing_counts: Dict[str, int] = {"latin": 0, "devanagari": 0, "unknown": 0}
        warnings: List[str] = []

        for idx, poly in enumerate(polygons):
            # Crop quadrilateral region from the original image
            crop = get_rotate_crop_image(processed_img, poly)
            if crop.size == 0 or crop.shape[0] < 4 or crop.shape[1] < 4:
                continue

            # Apply crop-level domain preprocessor (preserves detector polygon geometry)
            rec_crop = self.crop_preprocessor_hook(crop)

            # Route and recognize text
            text, conf, script, fallback_used, model_name = self.router.route_and_recognize(
                rec_crop, language_hint=language_hint
            )

            # Skip empty decodings
            if not text:
                continue

            # Record routing statistics
            routing_counts[script.value] = routing_counts.get(script.value, 0) + 1

            # Compute bounding box and raw quadrilateral height
            xmin = float(np.min(poly[:, 0]))
            ymin = float(np.min(poly[:, 1]))
            xmax = float(np.max(poly[:, 0]))
            ymax = float(np.max(poly[:, 1]))
            raw_h = calculate_polygon_height(poly)

            # Diagnostic confidence review check
            if conf < self.config.confidence_review_threshold:
                warnings.append(
                    f"Token '{text}' (conf {conf:.2f}) below confidence threshold {self.config.confidence_review_threshold}"
                )

            token = OCRToken(
                token_id=f"tok_{idx+1:03d}",
                text=text,
                confidence=conf,
                polygon=poly.tolist(),
                bbox=[xmin, ymin, xmax, ymax],
                script=script,
                line_id=0,
                raw_pixel_height=raw_h,
                model_name=model_name
            )
            tokens.append(token)

        t_rec_ms = (time.perf_counter() - t_rec_start) * 1000.0

        # 5. Deterministic Reading Order Sorting
        t_sort_start = time.perf_counter()
        sorted_tokens = sort_tokens_reading_order(tokens)
        t_sort_ms = (time.perf_counter() - t_sort_start) * 1000.0

        total_time_ms = (time.perf_counter() - t_start) * 1000.0

        stage_timings = {
            "preprocessing_ms": round(t_prep_ms, 2),
            "detection_ms": round(t_det_ms, 2),
            "recognition_ms": round(t_rec_ms, 2),
            "reading_order_ms": round(t_sort_ms, 2),
            "total_ms": round(total_time_ms, 2)
        }

        return OCRResult(
            image_id=img_id,
            image_width=orig_w,
            image_height=orig_h,
            tokens=sorted_tokens,
            engine="PP-OCRv3-ROUTED",
            detector_model=Path(self.config.det_model_path).name,
            recognizer_models={
                "latin": Path(self.config.rec_en_model_path).name,
                "devanagari": Path(self.config.rec_hi_model_path).name
            },
            processing_time_ms=round(total_time_ms, 2),
            stage_timings=stage_timings,
            warnings=warnings,
            routing_summary=routing_counts
        )
