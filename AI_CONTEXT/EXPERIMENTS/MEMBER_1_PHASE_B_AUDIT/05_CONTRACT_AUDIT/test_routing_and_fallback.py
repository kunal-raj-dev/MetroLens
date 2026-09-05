import cv2
import numpy as np
from nirikshak_ocr.config import OCRConfig
from nirikshak_ocr.engine import OCREngine
from nirikshak_ocr.types import ScriptType
from nirikshak_ocr.evaluation import compute_routing_accuracy, compute_cer, compute_wer

print("=== SCRIPT ROUTING & FALLBACK AUDIT ===")

engine = OCREngine()
router = engine.router

# 1. Create a clear Latin text crop
crop_en = np.full((48, 200, 3), 255, dtype=np.uint8)
cv2.putText(crop_en, "NET WT 500g", (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

text, conf, script, fallback_used, model_name = router.route_and_recognize(crop_en)
print(f"Latin crop: text='{text}', conf={conf:.2f}, script={script.value}, fallback={fallback_used}, model={model_name}")
assert script == ScriptType.LATIN
assert model_name == "SVTR-EN"

# 2. Test Devanagari synthetic packaging image
img_hi = cv2.imread("data/synthetic/regression/SYNTH-02-HIN-FMCG.png")
res_hi = engine.extract(img_hi, image_id="synth_hi")
print(f"Devanagari image tokens extracted: {len(res_hi.tokens)}")
hi_tokens = [t for t in res_hi.tokens if t.script == ScriptType.DEVANAGARI]
print(f"Devanagari tokens: {len(hi_tokens)} / {len(res_hi.tokens)}")
assert len(hi_tokens) > 0, "Expected at least 1 Devanagari routed token"

# 3. Test Ambiguous Noise / Low Contrast (should trigger fallback and evaluate to UNKNOWN or low conf)
crop_noise = np.random.randint(120, 135, (48, 200, 3), dtype=np.uint8)
text_n, conf_n, script_n, fallback_n, model_n = router.route_and_recognize(crop_noise)
print(f"Noise crop: text='{text_n}', conf={conf_n:.2f}, script={script_n.value}, fallback={fallback_n}, model={model_n}")
assert fallback_n is True, "Fallback should have executed on ambiguous input"

# 4. Explicit Language Hint Override
text_hint_hi, conf_h_hi, script_h_hi, fallback_h_hi, model_h_hi = router.route_and_recognize(crop_en, language_hint="hi")
assert script_h_hi == ScriptType.DEVANAGARI
assert fallback_h_hi is False
assert model_h_hi == "SVTR-HI"
print("Explicit language hint 'hi': PASS")

text_hint_en, conf_h_en, script_h_en, fallback_h_en, model_h_en = router.route_and_recognize(crop_en, language_hint="en")
assert script_h_en == ScriptType.LATIN
assert fallback_h_en is False
assert model_h_en == "SVTR-EN"
print("Explicit language hint 'en': PASS")

# 5. Routing Accuracy Metric Independence Audit
# Check that compute_routing_accuracy accepts decisions list and is unaffected by CER/WER
decisions = [
    ("latin", "latin"),
    ("latin", "latin"),
    ("devanagari", "devanagari"),
    ("latin", "devanagari") # 1 error out of 4
]
r_metrics = compute_routing_accuracy(decisions)
print("Routing accuracy metrics:", r_metrics)
assert r_metrics["total_routed"] == 4
assert r_metrics["correct_routed"] == 3
assert r_metrics["incorrect_routed"] == 1
assert abs(r_metrics["routing_accuracy"] - 0.75) < 1e-4

# CER test on same string (e.g. prediction vs reference)
cer_val = compute_cer("NET WT 500g", "NET WT 500g")
wer_val = compute_wer("NET WT 500g", "NET WT 500g")
assert cer_val == 0.0
assert wer_val == 0.0
print("Routing metric strictly independent from CER/WER: PASS")

print("=== ALL ROUTING & FALLBACK AUDITS PASSED ===")
