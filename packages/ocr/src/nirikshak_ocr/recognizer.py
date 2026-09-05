"""
SVTR scene text recognizer and CTC greedy decoder using Direct ONNX Runtime.
"""

from pathlib import Path
from typing import List, Tuple, Optional, Union
import cv2
import numpy as np
import onnxruntime as ort

from .config import OCRConfig
from .errors import ModelLoadError, InferenceError
from .preprocessing import resize_norm_recognizer_input
from .types import ScriptType


class CTCLabelDecoder:
    """
    Greedy Connectionist Temporal Classification (CTC) sequence decoder.
    Converts model logits into transcribed text and character confidences.
    """

    def __init__(self, character_list: List[str], expected_classes: Optional[int] = None):
        # CTC blank token is index 0
        self.character_list = ["blank"] + list(character_list)
        if expected_classes is not None and len(self.character_list) < expected_classes:
            while len(self.character_list) < expected_classes:
                self.character_list.append(" ")
        elif " " not in self.character_list:
            self.character_list.append(" ")
        self.num_classes = len(self.character_list)

    def decode(self, preds: np.ndarray) -> Tuple[str, float]:
        """
        Greedy decoding of softmax/logit array of shape (1, seq_len, num_classes)
        or (seq_len, num_classes).
        Returns (decoded_text, mean_confidence).
        """
        if preds.ndim == 3:
            preds = preds[0]

        pred_indices = preds.argmax(axis=1)
        pred_probs = preds.max(axis=1)

        char_list: List[str] = []
        conf_list: List[float] = []

        for i in range(len(pred_indices)):
            idx = pred_indices[i]
            # Skip CTC blank (index 0)
            if idx == 0:
                continue
            # Collapse repeated consecutive tokens
            if i > 0 and idx == pred_indices[i - 1]:
                continue
            if idx < len(self.character_list):
                char_list.append(self.character_list[idx])
                conf_list.append(float(pred_probs[i]))

        text = "".join(char_list).strip()
        mean_conf = float(np.mean(conf_list)) if conf_list else 0.0
        return text, round(mean_conf, 4)


class SVTRRecognizer:
    """
    Direct ONNX Runtime implementation of SVTR text line recognizer.
    Supports both Latin (SVTR-EN) and Devanagari (SVTR-HI) models.
    """

    def __init__(
        self,
        model_path: str,
        script: ScriptType,
        dict_path: Optional[str] = None,
        config: Optional[OCRConfig] = None
    ):
        self.script = script
        self.model_path = Path(model_path)
        if not self.model_path.is_file():
            raise ModelLoadError(f"Recognition ONNX model not found at: {self.model_path}")

        cfg = config or OCRConfig()
        sess_options = ort.SessionOptions()
        sess_options.intra_op_num_threads = cfg.intra_op_num_threads
        sess_options.inter_op_num_threads = cfg.inter_op_num_threads
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        try:
            self.session = ort.InferenceSession(
                str(self.model_path),
                sess_options=sess_options,
                providers=[cfg.runtime_provider]
            )
        except Exception as e:
            raise ModelLoadError(f"Failed to initialize ONNX recognizer session ({script}): {e}") from e

        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

        # Load character dictionary
        char_list = self._load_characters(dict_path)
        out_shape = self.session.get_outputs()[0].shape
        expected_classes = int(out_shape[-1]) if len(out_shape) >= 3 and isinstance(out_shape[-1], int) else None
        self.decoder = CTCLabelDecoder(char_list, expected_classes=expected_classes)

        if cfg.enable_warmup:
            self._warmup(cfg.rec_img_h, cfg.rec_img_w)

    def _load_characters(self, dict_path: Optional[str]) -> List[str]:
        # First check custom metadata embedded in the ONNX file
        meta = self.session.get_modelmeta().custom_metadata_map
        if "character" in meta:
            return meta["character"].splitlines()

        # Fallback to external dictionary file
        if dict_path:
            p = Path(dict_path)
            if p.is_file():
                with open(p, "r", encoding="utf-8") as f:
                    return [line.strip("\r\n") for line in f]

        raise ModelLoadError(
            f"No character dictionary found in model metadata or external path: {dict_path}"
        )

    def _warmup(self, h: int, w: int) -> None:
        try:
            dummy = np.zeros((1, 3, h, w), dtype=np.float32)
            self.session.run([self.output_name], {self.input_name: dummy})
        except Exception:
            pass

    def recognize(self, crop: np.ndarray) -> Tuple[str, float]:
        """
        Executes recognition on an upright horizontal image crop (BGR numpy array).
        Returns (transcribed_text, confidence_score).
        """
        if crop is None or crop.size == 0 or crop.shape[0] < 2 or crop.shape[1] < 2:
            return "", 0.0

        tensor_input = resize_norm_recognizer_input(crop)

        try:
            outputs = self.session.run([self.output_name], {self.input_name: tensor_input})
        except Exception as e:
            raise InferenceError(f"Recognizer ONNX inference failed ({self.script}): {e}") from e

        logits = outputs[0]
        text, conf = self.decoder.decode(logits)
        return text, conf
