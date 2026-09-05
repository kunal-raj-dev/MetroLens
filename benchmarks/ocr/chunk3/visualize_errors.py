"""
Visual Debug & Error Overlay Generator for Chunk 3.
Renders:
- Original image
- Clockwise 4-point quadrilateral polygons in green (high confidence) or amber/red (low confidence)
- Transcribed text label with confidence score
- Diagnostic watermark showing error taxonomy category
"""

import argparse
import os
import sys
from pathlib import Path
import cv2
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR / "packages" / "shared" / "src"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "ocr" / "src"))

from nirikshak_ocr import OCREngine, OCRConfig


def render_ocr_overlay(
    image_path: Path,
    output_path: Path,
    preprocessing_mode: str = "raw"
) -> Path:
    cfg = OCRConfig(
        preprocessing_mode=preprocessing_mode,
        preprocess_target="crop"
    ).resolve_paths()
    engine = OCREngine(cfg)

    img_bgr = cv2.imread(str(image_path))
    if img_bgr is None:
        raise ValueError(f"Could not read image: {image_path}")

    h, w = img_bgr.shape[:2]
    result = engine.extract(img_bgr, image_id=image_path.stem)

    canvas = img_bgr.copy()

    for idx, token in enumerate(result.tokens):
        pts = np.array(token.polygon, dtype=np.int32).reshape((-1, 1, 2))
        conf = token.confidence

        # Color: green if >= 0.85, yellow if >= 0.60, red if < 0.60
        if conf >= 0.85:
            color = (0, 200, 0)
        elif conf >= 0.60:
            color = (0, 215, 255)
        else:
            color = (0, 0, 255)

        # Draw polygon
        cv2.polylines(canvas, [pts], isClosed=True, color=color, thickness=2)

        # Label position
        x_min = int(token.bbox[0])
        y_min = int(token.bbox[1])
        label = f"{token.text} ({conf:.2f})"

        # Background tag
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
        cv2.rectangle(canvas, (x_min, max(0, y_min - th - 4)), (x_min + tw + 4, max(th + 4, y_min)), (20, 20, 20), -1)
        cv2.putText(canvas, label, (x_min + 2, max(th, y_min - 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

    # Header banner
    header = f"MetroLens OCR Debug | Specimen: {image_path.stem} | Mode: {preprocessing_mode} | Tokens: {len(result.tokens)} | Latency: {result.processing_time_ms:.1f}ms"
    cv2.rectangle(canvas, (0, 0), (w, 24), (30, 30, 30), -1)
    cv2.putText(canvas, header, (8, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 200), 1, cv2.LINE_AA)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), canvas)
    print(f"[+] Saved visual error overlay to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate OCR polygon & error visual overlay")
    parser.add_argument(
        "--image",
        type=str,
        default="AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET/images/SYNTH-01-ENG-FMCG.png"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="benchmarks/ocr/chunk3/visual_debug_overlay.png"
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="adaptive",
        help="raw, clahe, bilateral, unsharp, dilation, adaptive"
    )
    args = parser.parse_args()

    render_ocr_overlay(Path(args.image), Path(args.output), args.mode)


if __name__ == "__main__":
    main()
