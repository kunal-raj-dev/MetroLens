import numpy as np
import pytest
from pydantic import ValidationError
from nirikshak_ocr.config import OCRConfig
from nirikshak_ocr.service import OCRService
from nirikshak_ocr.errors import (
    OCRError,
    InvalidImageError,
    UnsupportedImageError,
    ModelLoadError,
    OCRServiceError
)

print("=== ERROR SEMANTICS & EMPTY RESULT AUDIT ===")

service = OCRService()

# A. Blank Image: MUST return valid OCRResult with 0 tokens, NOT an exception!
blank = np.full((300, 400, 3), 255, dtype=np.uint8)
res_blank = service.extract(blank, image_id="blank_test")
assert len(res_blank.tokens) == 0, f"Expected 0 tokens for blank frame, got {len(res_blank.tokens)}"
dict_blank = service.extract_dict(blank, image_id="blank_test")
assert dict_blank["status"] == "SUCCESS", f"Expected status SUCCESS, got {dict_blank['status']}"
assert dict_blank["token_count"] == 0
print("A. Blank Image (Empty Result Distinguishable from Failure): PASS")

# B. Unsupported Image: None, empty bytes, wrong type
try:
    service.extract(None)
    raise AssertionError("Did not raise on None")
except InvalidImageError as e:
    print("B1. None Image -> InvalidImageError: PASS")

try:
    service.convert_image_input(b"")
    raise AssertionError("Did not raise on empty bytes")
except InvalidImageError as e:
    print("B2. Empty Bytes -> InvalidImageError: PASS")

try:
    service.convert_image_input(12345) # invalid type
    raise AssertionError("Did not raise on invalid type")
except UnsupportedImageError as e:
    print("B3. Invalid Type -> UnsupportedImageError: PASS")

try:
    bad_channels = np.zeros((100, 100, 5), dtype=np.uint8) # 5 channels
    service.convert_image_input(bad_channels)
    raise AssertionError("Did not raise on 5 channels")
except UnsupportedImageError as e:
    print("B4. 5 Channels -> UnsupportedImageError: PASS")

# C. Corrupt Image: invalid binary payload
try:
    service.convert_image_input(b"NOT_A_VALID_IMAGE_FILE_HEADER")
    raise AssertionError("Did not raise on corrupt bytes")
except UnsupportedImageError as e:
    print("C. Corrupt Image Bytes -> UnsupportedImageError: PASS")

# D & E. Missing or Invalid Model Path
try:
    bad_cfg = OCRConfig(det_model_path="non_existent/weights/det.onnx")
    from nirikshak_ocr.detector import DBNetDetector
    DBNetDetector(bad_cfg)
    raise AssertionError("Did not raise on missing detector model")
except ModelLoadError as e:
    print("D/E. Missing Model Path -> ModelLoadError: PASS")

# F. Invalid Config: Pydantic validation enforcement
try:
    OCRConfig(intra_op_num_threads=0) # ge=1 constraint
    raise AssertionError("Did not raise on thread_count=0")
except ValidationError as e:
    print("F1. Config intra_op_num_threads=0 -> ValidationError: PASS")

try:
    OCRConfig(det_db_thresh=1.5) # le=1.0 constraint
    raise AssertionError("Did not raise on det_db_thresh > 1.0")
except ValidationError as e:
    print("F2. Config det_db_thresh=1.5 -> ValidationError: PASS")

# G. Decompression bomb guard (> 64MP)
try:
    huge_shape = (9000, 8000, 3) # 72 MP
    # Don't allocate real 72MP memory; simulate in ndarray check
    fake_huge = np.empty((8500, 8500, 3), dtype=np.uint8)
    service.convert_image_input(fake_huge)
    raise AssertionError("Did not raise on >64MP image")
except UnsupportedImageError as e:
    assert "decompression bomb" in str(e).lower()
    print("G. Decompression Bomb Guard -> UnsupportedImageError: PASS")

# H. Caller Array Immutability
test_arr = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
test_copy = test_arr.copy()
service.extract(test_arr, image_id="immutability_test")
assert np.array_equal(test_arr, test_copy), "Caller input array was modified in place!"
print("H. Caller Array Immutability: PASS (Zero in-place mutations)")

print("=== ALL ERROR SEMANTICS AUDITS PASSED ===")
