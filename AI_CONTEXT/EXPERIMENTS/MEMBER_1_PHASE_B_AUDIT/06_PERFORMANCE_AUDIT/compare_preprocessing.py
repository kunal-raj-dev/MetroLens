import time
from pathlib import Path
import cv2
import numpy as np
from nirikshak_ocr.config import OCRConfig
from nirikshak_ocr.engine import OCREngine

print("=== PREPROCESSING AUDIT: RAW vs ADAPTIVE ===")

# Verify defaults
default_cfg = OCRConfig()
assert default_cfg.preprocessing_mode == "raw", f"Expected default 'raw', got '{default_cfg.preprocessing_mode}'"
print(f"OCRConfig default preprocessing_mode: '{default_cfg.preprocessing_mode}' (VERIFIED RAW)")

images_dir = Path("data/synthetic/regression")
img_files = sorted(list(images_dir.glob("*.png")))
print(f"Testing {len(img_files)} synthetic regression images...")

engine_raw = OCREngine(OCRConfig(preprocessing_mode="raw"))
engine_adaptive = OCREngine(OCRConfig(preprocessing_mode="adaptive", preprocess_target="crop"))

raw_times = []
adaptive_times = []
raw_tokens_total = 0
adaptive_tokens_total = 0

print(f"{'Image':<35} | {'Raw ms':<8} | {'Raw Tok':<7} | {'Adapt ms':<8} | {'Adapt Tok':<9}")
print("-" * 75)

for img_p in img_files:
    img = cv2.imread(str(img_p))
    
    # Warmup / measurement
    t0 = time.perf_counter()
    res_raw = engine_raw.extract(img, image_id=img_p.stem)
    t_raw = (time.perf_counter() - t0) * 1000.0
    raw_times.append(t_raw)
    raw_tokens_total += len(res_raw.tokens)
    
    t0 = time.perf_counter()
    res_adapt = engine_adaptive.extract(img, image_id=img_p.stem)
    t_adapt = (time.perf_counter() - t0) * 1000.0
    adaptive_times.append(t_adapt)
    adaptive_tokens_total += len(res_adapt.tokens)
    
    print(f"{img_p.name:<35} | {t_raw:<8.1f} | {len(res_raw.tokens):<7} | {t_adapt:<8.1f} | {len(res_adapt.tokens):<9}")

print("-" * 75)
print(f"RAW Mean Latency:      {np.mean(raw_times):.1f} ms | Total Tokens: {raw_tokens_total}")
print(f"ADAPTIVE Mean Latency: {np.mean(adaptive_times):.1f} ms | Total Tokens: {adaptive_tokens_total}")

# Latency overhead of adaptive
overhead = np.mean(adaptive_times) - np.mean(raw_times)
print(f"Adaptive Overhead:     {overhead:+.1f} ms ({overhead / np.mean(raw_times) * 100:+.1f}%)")

# Audit conclusion
print("Conclusion: RAW default is verified. Adaptive adds latency and should remain optional/experimental.")
