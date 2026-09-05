import sys
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "packages" / "shared" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "ocr" / "src"))

import cv2
from nirikshak_ocr import OCREngine

engine = OCREngine()
base_dir = ROOT / "AI_CONTEXT" / "EXPERIMENTS" / "CHUNK_1_OCR_MODEL_SELECTION" / "03_DATASET" / "images"

specimens = [
    ("English FMCG", base_dir / "SYNTH-01-ENG-FMCG.png", None),
    ("Hindi FMCG", base_dir / "SYNTH-02-HIN-FMCG.png", "hi"),
    ("Blank Frame", base_dir / "SYNTH-07-BLANK-FRAME.png", None),
]

for label, img_path, hint in specimens:
    print(f"\n==================== {label.upper()} ({img_path.name}) ====================")
    img = cv2.imread(str(img_path))
    result = engine.extract(img, image_id=label, language_hint=hint)
    print(f"Dimensions: {result.image_width}x{result.image_height}")
    print(f"Total Processing Time: {result.processing_time_ms} ms")
    print(f"Stage Timings: {result.stage_timings}")
    print(f"Routing Summary: {result.routing_summary}")
    print(f"Extracted Tokens ({len(result.tokens)}):")
    for t in result.tokens:
        print(f"  [{t.token_id}] Text: '{t.text}' | Script: {t.script.value} | Conf: {t.confidence:.4f} | RawHeight: {t.raw_pixel_height}px | BBox: {t.bbox}")
    if result.warnings:
        print(f"Warnings: {result.warnings}")

print("\n==================== TESTING INVALID INPUT (NONE) ====================")
res_none = engine.extract(None, image_id="none_test")
print(f"None handled safely: tokens={len(res_none.tokens)}, warnings={res_none.warnings}")
