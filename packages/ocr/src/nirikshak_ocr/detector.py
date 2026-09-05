"""
DBNet++ text detector using Direct ONNX Runtime.
"""

from pathlib import Path
from typing import List, Tuple
import cv2
import numpy as np
import onnxruntime as ort
import pyclipper
from shapely.geometry import Polygon

from .config import OCRConfig
from .errors import ModelLoadError, InferenceError
from .preprocessing import resize_image_for_detection, normalize_detector_input, remap_polygon_to_original
from .utils import order_points_clockwise


class DBNetDetector:
    """
    Direct ONNX Runtime implementation of DBNet++ scene text detector.
    Emits 4-point quadrilateral polygons in original image pixel coordinates.
    """

    def __init__(self, config: OCRConfig):
        self.config = config
        model_path = Path(config.det_model_path)
        if not model_path.is_file():
            raise ModelLoadError(f"Detection ONNX model not found at: {model_path}")

        sess_options = ort.SessionOptions()
        sess_options.intra_op_num_threads = config.intra_op_num_threads
        sess_options.inter_op_num_threads = config.inter_op_num_threads
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        try:
            self.session = ort.InferenceSession(
                str(model_path),
                sess_options=sess_options,
                providers=[config.runtime_provider]
            )
        except Exception as e:
            raise ModelLoadError(f"Failed to initialize ONNX detector session: {e}") from e

        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

        if config.enable_warmup:
            self._warmup()

    def _warmup(self) -> None:
        """Executes a single small dummy pass to prime the ONNX execution provider."""
        try:
            dummy = np.zeros((1, 3, 64, 64), dtype=np.float32)
            self.session.run([self.output_name], {self.input_name: dummy})
        except Exception:
            pass

    def detect(self, image: np.ndarray) -> Tuple[List[np.ndarray], List[float]]:
        """
        Executes DBNet++ text line detection on an input image (BGR numpy array).
        Returns a tuple of (polygons, confidence_scores):
        - polygons: List of 4-point numpy arrays [[x1,y1], [x2,y2], [x3,y3], [x4,y4]] in original image coordinates.
        - scores: List of float confidence scores in [0.0, 1.0].
        """
        h, w = image.shape[:2]
        resized_img, ratio_w, ratio_h = resize_image_for_detection(image, self.config.max_side_len)
        tensor_input = normalize_detector_input(resized_img)

        try:
            outputs = self.session.run([self.output_name], {self.input_name: tensor_input})
        except Exception as e:
            raise InferenceError(f"Detector ONNX inference failed: {e}") from e

        pred = outputs[0][0, 0]  # (H_res, W_res) probability map
        bitmap = (pred > self.config.det_db_thresh).astype(np.uint8)

        if self.config.det_use_dilation:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            bitmap = cv2.dilate(bitmap, kernel)

        contours, _ = cv2.findContours(bitmap * 255, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        boxes: List[np.ndarray] = []
        scores: List[float] = []

        for c in contours:
            if len(c) < 3:
                continue

            rect = cv2.minAreaRect(c)
            bw, bh = rect[1]
            if min(bw, bh) < 3:
                continue

            # Calculate box confidence score from the probability map
            mask = np.zeros(pred.shape, dtype=np.uint8)
            cv2.fillPoly(mask, [c], 1)
            score = float(cv2.mean(pred, mask)[0])
            if score < self.config.det_db_box_thresh:
                continue

            # Unclip (expand) the detected contour to recover true character boundary
            pts = cv2.boxPoints(rect)
            poly = Polygon(pts)
            if poly.length == 0:
                continue

            distance = poly.area * self.config.det_db_unclip_ratio / poly.length
            offset = pyclipper.PyclipperOffset()
            offset.AddPath(pts, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
            expanded = offset.Execute(distance)

            if not expanded or len(expanded[0]) < 4:
                continue

            expanded_pts = np.array(expanded[0], dtype=np.float32)
            exp_rect = cv2.minAreaRect(expanded_pts)
            box = cv2.boxPoints(exp_rect)
            box_clockwise = order_points_clockwise(box)

            # Remap polygon back to original input image coordinate space
            orig_box = remap_polygon_to_original(box_clockwise, ratio_w, ratio_h)

            # Clamp coordinates to original image bounds
            orig_box[:, 0] = np.clip(orig_box[:, 0], 0, w)
            orig_box[:, 1] = np.clip(orig_box[:, 1], 0, h)

            boxes.append(orig_box)
            scores.append(round(score, 4))

        return boxes, scores
