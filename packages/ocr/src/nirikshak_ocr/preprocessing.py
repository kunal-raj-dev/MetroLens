"""
Image preprocessing, aspect-ratio-preserving resizing, coordinate unscaling, and extension hooks.
"""

from typing import Tuple, List, Optional
import cv2
import numpy as np


class ImagePreprocessHook:
    """
    Base extension interface for image preprocessing hooks.
    Default implementation is an identity pass-through.
    Per architectural rules, heavy filters are not hardcoded into every request.
    """
    def __call__(self, img: np.ndarray) -> np.ndarray:
        return img


def apply_clahe(
    img: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8)
) -> np.ndarray:
    """
    Applies Contrast Limited Adaptive Histogram Equalization (CLAHE).
    For BGR images, operates in LAB color space on the L-channel (luminance)
    to enhance local contrast without chromatic shifts or color banding.
    """
    if img is None or img.size == 0:
        return img

    h, w = img.shape[:2]
    # Ensure tile size does not exceed image dimensions
    grid_w = max(1, min(tile_grid_size[0], w))
    grid_h = max(1, min(tile_grid_size[1], h))
    clahe = cv2.createCLAHE(clipLimit=float(clip_limit), tileGridSize=(grid_w, grid_h))

    if len(img.shape) == 2:
        return clahe.apply(img)
    elif len(img.shape) == 3 and img.shape[2] == 3:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        cl = clahe.apply(l_channel)
        merged_lab = cv2.merge((cl, a_channel, b_channel))
        return cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)
    elif len(img.shape) == 3 and img.shape[2] == 1:
        res = clahe.apply(img[:, :, 0])
        return np.expand_dims(res, axis=-1)
    return img.copy()


def apply_bilateral_filter(
    img: np.ndarray,
    d: int = 5,
    sigma_color: float = 50.0,
    sigma_space: float = 50.0
) -> np.ndarray:
    """
    Edge-preserving smoothing filter. Smooths flat packaging textures
    (e.g. grain, foil sheen) while preserving sharp text stroke edges.
    """
    if img is None or img.size == 0:
        return img
    d_clamped = max(1, min(d, 15))
    return cv2.bilateralFilter(img, d_clamped, float(sigma_color), float(sigma_space))


def apply_unsharp_mask(
    img: np.ndarray,
    amount: float = 1.5,
    kernel_size: int = 5,
    sigma: float = 1.0
) -> np.ndarray:
    """
    Applies an unsharp mask to restore edge definition on slightly blurred packaging text.
    Formula: sharpened = img * (1 + amount) - blurred * amount
    """
    if img is None or img.size == 0:
        return img
    k = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
    blurred = cv2.GaussianBlur(img, (k, k), float(sigma))
    sharpened = cv2.addWeighted(img, 1.0 + float(amount), blurred, -float(amount), 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)


def apply_morphological_dilation(
    img: np.ndarray,
    kernel_size: int = 2,
    iterations: int = 1
) -> np.ndarray:
    """
    Connects disconnected dot-matrix inkjet character dots into continuous strokes.
    Polarity-aware:
    - On light backgrounds (mean luma > 127), erodes bright pixels to expand dark ink dots.
    - On dark backgrounds (mean luma <= 127), dilates bright pixels to expand light ink dots.
    """
    if img is None or img.size == 0:
        return img

    k = max(1, min(kernel_size, 7))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))

    # Determine polarity from grayscale luminance
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    mean_val = float(np.mean(gray))

    if mean_val > 127.0:
        # Dark text on light background: erode light background to expand dark text strokes
        return cv2.erode(img, kernel, iterations=iterations)
    else:
        # Light text on dark background: dilate light text
        return cv2.dilate(img, kernel, iterations=iterations)


def apply_adaptive_preprocessing(
    img: np.ndarray,
    contrast_thresh: float = 35.0,
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8)
) -> np.ndarray:
    """
    Adaptive domain preprocessor:
    Measures standard deviation of luminance across the crop/image.
    If contrast is low (std < contrast_thresh), applies CLAHE to boost readability.
    If contrast is already sufficient, preserves the pristine input to avoid artifacts.
    """
    if img is None or img.size == 0:
        return img

    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    contrast_std = float(np.std(gray))
    if contrast_std < contrast_thresh:
        return apply_clahe(img, clip_limit=clip_limit, tile_grid_size=tile_grid_size)
    return img.copy()


class DomainPreprocessPipeline(ImagePreprocessHook):
    """
    Configurable, production-grade preprocessing pipeline for packaging OCR.
    Guarantees:
    - Input safety and non-destructive image copying.
    - Preserves dimensional shape and array strides.
    - Reversible coordinate preservation.
    """

    def __init__(
        self,
        mode: str = "raw",
        clahe_clip_limit: float = 2.0,
        clahe_tile_grid_size: Tuple[int, int] = (8, 8),
        bilateral_d: int = 5,
        bilateral_sigma_color: float = 50.0,
        bilateral_sigma_space: float = 50.0,
        unsharp_amount: float = 1.5,
        dilation_kernel_size: int = 2,
        dilation_iterations: int = 1,
        adaptive_contrast_threshold: float = 35.0
    ):
        self.mode = mode.lower().strip()
        self.clahe_clip_limit = clahe_clip_limit
        self.clahe_tile_grid_size = clahe_tile_grid_size
        self.bilateral_d = bilateral_d
        self.bilateral_sigma_color = bilateral_sigma_color
        self.bilateral_sigma_space = bilateral_sigma_space
        self.unsharp_amount = unsharp_amount
        self.dilation_kernel_size = dilation_kernel_size
        self.dilation_iterations = dilation_iterations
        self.adaptive_contrast_threshold = adaptive_contrast_threshold

    def __call__(self, img: np.ndarray) -> np.ndarray:
        if img is None or img.size == 0:
            return img

        out = img.copy()
        if self.mode in ("raw", "passthrough", "none"):
            return out

        if self.mode == "clahe":
            return apply_clahe(out, self.clahe_clip_limit, self.clahe_tile_grid_size)

        if self.mode == "bilateral":
            return apply_bilateral_filter(
                out, self.bilateral_d, self.bilateral_sigma_color, self.bilateral_sigma_space
            )

        if self.mode == "unsharp":
            return apply_unsharp_mask(out, amount=self.unsharp_amount)

        if self.mode == "dilation":
            return apply_morphological_dilation(
                out, self.dilation_kernel_size, self.dilation_iterations
            )

        if self.mode == "adaptive":
            return apply_adaptive_preprocessing(
                out,
                contrast_thresh=self.adaptive_contrast_threshold,
                clip_limit=self.clahe_clip_limit,
                tile_grid_size=self.clahe_tile_grid_size
            )

        if self.mode == "targeted_combo_clahe_dilate":
            # CLAHE for contrast followed by dilation for dot-matrix
            c = apply_clahe(out, self.clahe_clip_limit, self.clahe_tile_grid_size)
            return apply_morphological_dilation(c, self.dilation_kernel_size, self.dilation_iterations)

        # Fallback to pristine copy
        return out


def resize_image_for_detection(
    img: np.ndarray,
    max_side_len: int = 960
) -> Tuple[np.ndarray, float, float]:
    """
    Resizes image while preserving aspect ratio and ensuring dimensions are multiples of 32
    (mandatory constraint for DBNet feature pyramid network).
    Returns (resized_image, ratio_w, ratio_h).
    """
    h, w = img.shape[:2]
    
    # Compute scaling factor to ensure maximum side <= max_side_len
    ratio = 1.0
    if max(h, w) > max_side_len:
        if h > w:
            ratio = float(max_side_len) / float(h)
        else:
            ratio = float(max_side_len) / float(w)
            
    resize_h = int(round(h * ratio))
    resize_w = int(round(w * ratio))
    
    # DBNet requires dimensions divisible by 32
    resize_h = max(32, int(round(resize_h / 32.0) * 32))
    resize_w = max(32, int(round(resize_w / 32.0) * 32))
    
    resized_img = cv2.resize(img, (resize_w, resize_h), interpolation=cv2.INTER_LINEAR)
    
    # Exact scale factors for coordinate remapping
    ratio_w = float(resize_w) / float(w)
    ratio_h = float(resize_h) / float(h)
    
    return resized_img, ratio_w, ratio_h


def normalize_detector_input(img: np.ndarray) -> np.ndarray:
    """
    Normalizes RGB image array for DBNet++ detection:
    1. Rescale to [0.0, 1.0]
    2. Subtract ImageNet mean [0.485, 0.456, 0.406]
    3. Divide by ImageNet std [0.229, 0.224, 0.225]
    4. Transpose to shape (1, 3, H, W) float32
    """
    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    img_float = img_rgb.astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    
    norm = (img_float - mean) / std
    # H, W, C -> C, H, W
    transposed = norm.transpose((2, 0, 1))
    # Add batch dimension: (1, 3, H, W)
    return np.expand_dims(transposed, axis=0)


def remap_polygon_to_original(
    polygon: np.ndarray,
    ratio_w: float,
    ratio_h: float
) -> np.ndarray:
    """
    Remaps detection polygon coordinates from resized space back to original image pixel space.
    """
    remapped = polygon.copy().astype(np.float32)
    remapped[:, 0] = remapped[:, 0] / ratio_w
    remapped[:, 1] = remapped[:, 1] / ratio_h
    return np.round(remapped, 2)


def resize_norm_recognizer_input(
    crop: np.ndarray,
    rec_img_h: int = 48,
    rec_img_w: int = 320
) -> np.ndarray:
    """
    Normalizes a text line crop for SVTR recognition:
    1. Scales height to rec_img_h (48) while preserving aspect ratio
    2. Zero-pads width to rec_img_w (320)
    3. Normalizes pixel values to [-0.5, 0.5]: (x / 255.0 - 0.5) / 0.5
    4. Transposes to shape (1, 3, H, W) float32
    """
    h, w = crop.shape[:2]
    if h == 0 or w == 0:
        return np.zeros((1, 3, rec_img_h, rec_img_w), dtype=np.float32)
        
    ratio = float(w) / float(h)
    resized_w = int(round(rec_img_h * ratio))
    resized_w = min(rec_img_w, max(1, resized_w))
    
    resized_crop = cv2.resize(crop, (resized_w, rec_img_h), interpolation=cv2.INTER_LINEAR)
    
    # Normalize: (pixel / 255 - 0.5) / 0.5 -> [-1.0, 1.0] standard SVTR normalization
    norm_crop = (resized_crop.astype(np.float32) / 255.0 - 0.5) / 0.5
    
    # Canvas with zero padding on right
    canvas = np.zeros((rec_img_h, rec_img_w, 3), dtype=np.float32)
    canvas[:, :resized_w, :] = norm_crop
    
    # H, W, C -> C, H, W
    transposed = canvas.transpose((2, 0, 1))
    return np.expand_dims(transposed, axis=0)
