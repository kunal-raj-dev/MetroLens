import json
import numpy as np
from nirikshak_ocr.types import OCRToken, OCRResult, ScriptType
from nirikshak_ocr.service import OCRService
from nirikshak_shared.models.contracts import OCRObservation
from nirikshak_shared.models.primitives import BoundingBox

print("=== CONTRACT & JSON ROUNDTRIP AUDIT ===")

# 1. Test OCRToken construction and validation
tok = OCRToken(
    token_id="tok_001",
    text="MRP ₹ 250.00 (incl. of all taxes)",
    confidence=0.985,
    polygon=[[10.0, 10.0], [100.0, 10.0], [100.0, 30.0], [10.0, 30.0]],
    bbox=[10.0, 10.0, 100.0, 30.0],
    script=ScriptType.LATIN,
    line_id=1,
    raw_pixel_height=20.0,
    model_name="SVTR-EN"
)

# 2. Conversion to OCRObservation
obs = tok.to_observation()
assert isinstance(obs, OCRObservation), "Expected OCRObservation"
assert obs.token_id == "tok_001"
assert obs.text == tok.text
assert obs.confidence == 0.985
assert obs.bounding_box.x_min == 10.0
assert obs.bounding_box.x_max == 100.0
assert obs.bounding_box.y_min == 10.0
assert obs.bounding_box.y_max == 30.0
assert obs.polygon == tok.polygon
assert obs.language == "en"
print("OCRToken -> OCRObservation conversion: PASS")

# 3. Test Hindi Devanagari Token with ₹ and Unicode symbols
tok_hi = OCRToken(
    token_id="tok_002",
    text="अधिकतम खुदरा मूल्य ₹ ९९.००",
    confidence=0.942,
    polygon=[[15.0, 40.0], [150.0, 40.0], [150.0, 65.0], [15.0, 65.0]],
    bbox=[15.0, 40.0, 150.0, 65.0],
    script=ScriptType.DEVANAGARI,
    line_id=2,
    raw_pixel_height=25.0,
    model_name="SVTR-HI"
)
obs_hi = tok_hi.to_observation()
assert obs_hi.language == "hi"
assert "₹" in obs_hi.text
assert "अधिकतम" in obs_hi.text

# 4. JSON Serialization & Deserialization
obs_json = obs_hi.model_dump_json()
print("Serialized JSON:", obs_json)
obs_reloaded = OCRObservation.model_validate_json(obs_json)
assert obs_reloaded.text == obs_hi.text
assert obs_reloaded.confidence == obs_hi.confidence
assert obs_reloaded.bounding_box.x_min == obs_hi.bounding_box.x_min
assert obs_reloaded.polygon == obs_hi.polygon
assert obs_reloaded.language == "hi"
print("OCRObservation JSON roundtrip: PASS")

# 5. Full OCRResult serialization
result = OCRResult(
    image_id="img_audit",
    image_width=800,
    image_height=600,
    tokens=[tok, tok_hi],
    engine="PP-OCRv3-ROUTED",
    detector_model="ch_PP-OCRv3_det_infer.onnx",
    recognizer_models={"latin": "ch_PP-OCRv3_rec_infer.onnx", "devanagari": "rec.onnx"},
    processing_time_ms=45.2,
    stage_timings={"detection_ms": 25.1, "recognition_ms": 20.1},
    warnings=[],
    routing_summary={"latin": 1, "devanagari": 1, "unknown": 0}
)
result_json = result.model_dump_json()
result_reloaded = OCRResult.model_validate_json(result_json)
assert len(result_reloaded.tokens) == 2
assert result_reloaded.tokens[1].text == tok_hi.text
assert result_reloaded.image_width == 800
print("OCRResult JSON roundtrip: PASS")

# 6. OCRService extract_dict() contract
service = OCRService.get_instance()
dummy = np.full((100, 200, 3), 255, dtype=np.uint8)
d = service.extract_dict(dummy)
assert d["status"] == "SUCCESS"
assert "tokens" in d
assert "observations" in d
assert "image_width" in d
assert "image_height" in d
assert "routing_summary" in d
print("OCRService extract_dict() structure: PASS")

# 7. Malformed Geometry Validation (Should raise ValueError)
try:
    OCRToken(
        token_id="bad_tok",
        text="bad",
        confidence=0.5,
        polygon=[[0.0, 0.0], [10.0, 0.0], [10.0, 10.0]], # 3 vertices instead of 4
        bbox=[0.0, 0.0, 10.0, 10.0]
    )
    print("Malformed geometry check: FAILED (did not raise)")
except Exception as e:
    print("Malformed geometry check (3 vertices): PASS (caught:", type(e).__name__, ")")

try:
    OCRToken(
        token_id="nan_tok",
        text="nan",
        confidence=0.5,
        polygon=[[0.0, 0.0], [float('nan'), 0.0], [10.0, 10.0], [0.0, 10.0]],
        bbox=[0.0, 0.0, 10.0, 10.0]
    )
    print("NaN geometry check: FAILED (did not raise)")
except Exception as e:
    print("NaN geometry check: PASS (caught:", type(e).__name__, ")")

print("=== ALL CONTRACT AUDITS PASSED ===")
