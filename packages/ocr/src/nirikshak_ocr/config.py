"""
Typed configuration for Nirikshak OCR subsystem.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


def _default_root() -> Path:
    if env_root := os.environ.get("METROLENS_ROOT"):
        p = Path(env_root).resolve()
        if p.is_dir():
            return p
    # Walk up from this file to locate project root containing 'models/'
    current = Path(__file__).resolve().parent
    for _ in range(5):
        if (current / "models").is_dir():
            return current
        current = current.parent
    return Path.cwd()


PROJECT_ROOT = _default_root()


def _get_models_dir() -> Path:
    if env_models := os.environ.get("METROLENS_MODELS_DIR"):
        p = Path(env_models).resolve()
        if p.is_dir():
            return p
    return PROJECT_ROOT / "models"


class OCRConfig(BaseModel):
    """
    Configuration parameters for DBNet++ detection and script-routed recognition.
    """
    # Model Weights Paths
    det_model_path: str = Field(
        default_factory=lambda: str(_get_models_dir() / "weights" / "ocr" / "det" / "ch_PP-OCRv3_det_infer.onnx"),
        description="Filesystem path to DBNet++ ONNX detection model"
    )
    rec_en_model_path: str = Field(
        default_factory=lambda: str(_get_models_dir() / "weights" / "ocr" / "rec_en" / "ch_PP-OCRv3_rec_infer.onnx"),
        description="Filesystem path to SVTR-EN ONNX alphanumeric recognizer"
    )
    rec_hi_model_path: str = Field(
        default_factory=lambda: str(_get_models_dir() / "weights" / "ocr" / "rec_hi" / "rec.onnx"),
        description="Filesystem path to SVTR-HI ONNX Devanagari recognizer"
    )
    rec_hi_dict_path: str = Field(
        default_factory=lambda: str(_get_models_dir() / "weights" / "ocr" / "rec_hi" / "dict.txt"),
        description="Filesystem path to Devanagari character dictionary"
    )


    # Runtime Execution Settings
    runtime_provider: str = Field(default="CPUExecutionProvider", description="ONNX Runtime execution provider")
    intra_op_num_threads: int = Field(default=4, ge=1, le=32, description="Number of intra-op threads for CPU execution")
    inter_op_num_threads: int = Field(default=1, ge=1, le=16, description="Number of inter-op threads")
    enable_warmup: bool = Field(default=False, description="Perform dummy inference on initialization to warm CPU cache")

    # Detection & Bounding Box Parameters
    max_side_len: int = Field(default=960, ge=320, le=2400, description="Upper bound for image resize before detection")
    det_db_thresh: float = Field(default=0.3, ge=0.0, le=1.0, description="DBNet binarization threshold")
    det_db_box_thresh: float = Field(default=0.5, ge=0.0, le=1.0, description="Detection box score threshold")
    det_db_unclip_ratio: float = Field(default=1.6, ge=1.0, le=3.0, description="Polygon expansion unclip ratio")
    det_use_dilation: bool = Field(default=True, description="Apply morphological dilation on detection probability map")

    # Script Routing & Recognition
    confidence_review_threshold: float = Field(
        default=0.60, ge=0.0, le=1.0,
        description="Threshold below which tokens trigger a low-confidence diagnostic warning"
    )
    rec_img_h: int = Field(default=48, description="Target crop height for SVTR recognizer")
    rec_img_w: int = Field(default=320, description="Target crop width for SVTR recognizer")

    # Domain-Specific Preprocessing Parameters (Chunk 3)
    preprocessing_mode: str = Field(
        default="raw",
        description="Preprocessing mode: 'raw', 'clahe', 'bilateral', 'unsharp', 'dilation', or 'adaptive'"
    )
    preprocess_target: str = Field(
        default="crop",
        description="Application target: 'crop' (recommended to preserve detector geometry), 'image', or 'both'"
    )
    clahe_clip_limit: float = Field(default=2.0, ge=0.5, le=10.0, description="CLAHE contrast clip limit")
    clahe_tile_grid_size: tuple[int, int] = Field(default=(8, 8), description="CLAHE tile grid dimensions (W, H)")
    bilateral_d: int = Field(default=5, ge=1, le=15, description="Bilateral filter pixel neighborhood diameter")
    bilateral_sigma_color: float = Field(default=50.0, ge=5.0, le=200.0, description="Bilateral filter sigma in color space")
    bilateral_sigma_space: float = Field(default=50.0, ge=5.0, le=200.0, description="Bilateral filter sigma in coordinate space")
    unsharp_amount: float = Field(default=1.5, ge=0.1, le=5.0, description="Unsharp mask sharpening strength multiplier")
    dilation_kernel_size: int = Field(default=2, ge=1, le=7, description="Morphological dilation rectangular kernel size")
    dilation_iterations: int = Field(default=1, ge=1, le=5, description="Number of dilation iterations for dot-matrix text")
    adaptive_contrast_threshold: float = Field(
        default=35.0, ge=5.0, le=128.0,
        description="Luma standard deviation threshold below which adaptive CLAHE is triggered on low-contrast crops"
    )

    def resolve_paths(self) -> "OCRConfig":
        """Ensures all model and dictionary paths are absolute and verified."""
        self.det_model_path = str(Path(self.det_model_path).resolve())
        self.rec_en_model_path = str(Path(self.rec_en_model_path).resolve())
        self.rec_hi_model_path = str(Path(self.rec_hi_model_path).resolve())
        self.rec_hi_dict_path = str(Path(self.rec_hi_dict_path).resolve())
        return self
