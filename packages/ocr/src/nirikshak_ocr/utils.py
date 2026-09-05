"""
Geometric utilities, coordinate transforms, and reading-order sorting for Nirikshak OCR.
"""

import math
from typing import Any, List, Tuple, Union
import cv2
import numpy as np

from .errors import InvalidImageError, GeometryError
from .types import OCRToken


def validate_input_image(image: Any) -> np.ndarray:
    """
    Validates that the input image is a valid, non-empty numpy array with supported dimensions.
    Returns the validated numpy array.
    """
    if image is None:
        raise InvalidImageError("Input image cannot be None")
    
    if not isinstance(image, np.ndarray):
        raise InvalidImageError(f"Input image must be a numpy.ndarray, got {type(image)}")
    
    if image.size == 0 or image.ndim < 2:
        raise InvalidImageError(f"Input image is empty or has invalid shape: {image.shape}")
    
    h, w = image.shape[:2]
    if h < 8 or w < 8:
        raise InvalidImageError(f"Input image dimensions too small for OCR: {w}x{h}")
    
    # Ensure 3-channel BGR format for consistency
    if image.ndim == 2:
        # Grayscale to BGR
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.ndim == 3 and image.shape[2] == 4:
        # BGRA to BGR
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    elif image.ndim == 3 and image.shape[2] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.ndim == 3 and image.shape[2] != 3:
        raise InvalidImageError(f"Unsupported channel count: {image.shape[2]}")
    
    return image


def order_points_clockwise(pts: np.ndarray) -> np.ndarray:
    """
    Orders 4 points of a quadrilateral in clockwise order starting from top-left:
    [top-left, top-right, bottom-right, bottom-left].
    """
    if len(pts) != 4:
        raise GeometryError(f"Expected 4 points, got {len(pts)}")
    
    pts = pts.astype(np.float32)
    # Sort points by x-coordinate
    x_sorted = pts[np.argsort(pts[:, 0]), :]
    
    left_pts = x_sorted[:2, :]
    right_pts = x_sorted[2:, :]
    
    # Left points sorted by y-coordinate -> top-left, bottom-left
    left_pts = left_pts[np.argsort(left_pts[:, 1]), :]
    tl, bl = left_pts[0], left_pts[1]
    
    # Right points sorted by y-coordinate -> top-right, bottom-right
    right_pts = right_pts[np.argsort(right_pts[:, 1]), :]
    tr, br = right_pts[0], right_pts[1]
    
    return np.array([tl, tr, br, bl], dtype=np.float32)


def calculate_polygon_height(pts: np.ndarray) -> float:
    """
    Calculates average height of a 4-point quadrilateral in original image pixels.
    Height is measured along the orientation of the side edges:
    h_px = (||p3 - p0|| + ||p2 - p1||) / 2
    NOTE: THIS IS A RAW PIXEL GEOMETRIC MEASUREMENT, NOT LEGAL FONT HEIGHT.
    """
    if len(pts) != 4:
        return 0.0
    h1 = float(np.linalg.norm(pts[3] - pts[0]))
    h2 = float(np.linalg.norm(pts[2] - pts[1]))
    return round((h1 + h2) / 2.0, 2)


def get_rotate_crop_image(img: np.ndarray, points: np.ndarray) -> np.ndarray:
    """
    Crops and perspective-unwarps a quadrilateral text region to an upright horizontal crop.
    """
    pts = order_points_clockwise(points)
    
    crop_w = int(max(np.linalg.norm(pts[0] - pts[1]), np.linalg.norm(pts[2] - pts[3])))
    crop_h = int(max(np.linalg.norm(pts[0] - pts[3]), np.linalg.norm(pts[1] - pts[2])))
    
    if crop_w <= 0 or crop_h <= 0:
        return np.zeros((16, 16, 3), dtype=np.uint8)
    
    pts_std = np.float32([
        [0, 0],
        [crop_w, 0],
        [crop_w, crop_h],
        [0, crop_h]
    ])
    
    matrix = cv2.getPerspectiveTransform(pts, pts_std)
    dst_img = cv2.warpPerspective(
        img,
        matrix,
        (crop_w, crop_h),
        borderMode=cv2.BORDER_REPLICATE,
        flags=cv2.INTER_CUBIC
    )
    
    # If height > 1.5 * width, rotate 90 deg clockwise (vertical text line handling)
    if dst_img.shape[0] * 1.0 / max(1, dst_img.shape[1]) >= 1.5:
        dst_img = np.rot90(dst_img, -1)
    
    return dst_img


def sort_tokens_reading_order(tokens: List[OCRToken], line_tolerance_ratio: float = 0.5) -> List[OCRToken]:
    """
    Sorts OCR tokens into deterministic reading order: top-to-bottom, left-to-right.
    Groups tokens whose vertical overlap exceeds line_tolerance_ratio * line_height into the same line.
    Assigns sequential line_id and returns sorted tokens.
    """
    if not tokens:
        return []
    
    # Sort initially by y_min
    sorted_by_y = sorted(tokens, key=lambda t: t.bbox[1])
    
    lines: List[List[OCRToken]] = []
    
    for tok in sorted_by_y:
        y_min, y_max = tok.bbox[1], tok.bbox[3]
        height = max(1.0, y_max - y_min)
        
        placed = False
        for line in lines:
            line_y_mins = [t.bbox[1] for t in line]
            line_y_maxs = [t.bbox[3] for t in line]
            line_avg_y = sum(line_y_mins) / len(line_y_mins)
            line_avg_h = max(1.0, (sum(line_y_maxs) / len(line_y_maxs)) - line_avg_y)
            
            # Check if this token vertically aligns with the line
            if abs(y_min - line_avg_y) < (line_avg_h * line_tolerance_ratio):
                line.append(tok)
                placed = True
                break
        
        if not placed:
            lines.append([tok])
    
    # Sort lines top-to-bottom
    lines.sort(key=lambda line: sum(t.bbox[1] for t in line) / len(line))
    
    result: List[OCRToken] = []
    for line_idx, line in enumerate(lines):
        # Sort tokens within the line left-to-right by x_min
        line.sort(key=lambda t: t.bbox[0])
        for tok in line:
            tok.line_id = line_idx
            result.append(tok)
    
    return result
