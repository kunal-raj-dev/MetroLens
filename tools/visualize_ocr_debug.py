"""
Visual debugging tool for Nirikshak OCR subsystem (Engineering Validation).
Renders detected 4-point bounding polygons, text, confidence, and script tags onto the image.
"""

import sys
import os
from pathlib import Path
import cv2
import numpy as np

sys.path.insert(0, os.path.abspath("packages/shared/src"))
sys.path.insert(0, os.path.abspath("packages/ocr/src"))

from nirikshak_ocr import OCREngine, OCRConfig


def render_debug_image(input_image_path: Path, output_image_path: Path):
    cfg = OCRConfig().resolve_paths()
    engine = OCREngine(cfg)

    img = cv2.imread(str(input_image_path))
    if img is None:
        print(f"Error loading image: {input_image_path}")
        return

    result = engine.extract(img, image_id=input_image_path.name)
    canvas = img.copy()

    for tok in result.tokens:
        pts = np.array(tok.polygon, dtype=np.int32).reshape((-1, 1, 2))
        # Draw 4-point polygon in green
        cv2.polylines(canvas, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Top-left corner for label
        tl = (int(tok.polygon[0][0]), max(15, int(tok.polygon[0][1]) - 5))
        label = f"{tok.text} ({tok.confidence:.2f}) [{tok.script.value}]"
        cv2.putText(canvas, label, tl, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)

    os.makedirs(output_image_path.parent, exist_ok=True)
    cv2.imwrite(str(output_image_path), canvas)
    print(f"Saved debug visualization ({len(result.tokens)} tokens) to: {output_image_path}")


if __name__ == "__main__":
    default_input = Path("AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET/images/SYNTH-01-ENG-FMCG.png")
    default_output = Path("benchmarks/ocr/chunk2/debug_visual.png")
    render_debug_image(default_input, default_output)
