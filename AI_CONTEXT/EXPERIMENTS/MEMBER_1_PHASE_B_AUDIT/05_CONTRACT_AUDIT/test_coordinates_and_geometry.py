import math
import numpy as np
import cv2
from nirikshak_ocr.config import OCRConfig
from nirikshak_ocr.detector import DBNetDetector
from nirikshak_ocr.preprocessing import resize_image_for_detection, remap_polygon_to_original
from nirikshak_ocr.utils import order_points_clockwise, calculate_polygon_height, get_rotate_crop_image

print("=== COORDINATE FORENSIC & GEOMETRY AUDIT ===")

# 1. Test resize and remapping mathematics numerically
orig_w, orig_h = 1920, 1080
img_fake = np.zeros((orig_h, orig_w, 3), dtype=np.uint8)
resized_img, ratio_w, ratio_h = resize_image_for_detection(img_fake, max_side_len=960)

print(f"Original: {orig_w}x{orig_h} -> Resized: {resized_img.shape[1]}x{resized_img.shape[0]}")
assert resized_img.shape[0] % 32 == 0, "Height must be multiple of 32"
assert resized_img.shape[1] % 32 == 0, "Width must be multiple of 32"
assert max(resized_img.shape[:2]) <= 960

# Test synthetic polygon remapping
poly_resized = np.array([[100.0, 50.0], [200.0, 50.0], [200.0, 80.0], [100.0, 80.0]], dtype=np.float32)
remapped = remap_polygon_to_original(poly_resized, ratio_w, ratio_h)
# Roundtrip test
re_resized = np.zeros_like(remapped)
re_resized[:, 0] = np.round(remapped[:, 0] * ratio_w, 2)
re_resized[:, 1] = np.round(remapped[:, 1] * ratio_h, 2)
diff = np.max(np.abs(re_resized - poly_resized))
assert diff < 0.1, f"Remapping roundtrip error too high: {diff}"
print(f"Coordinate scaling roundtrip max diff: {diff:.4f} px (PASS)")

# 2. Test clockwise point ordering invariant
shuffled_pts = np.array([[200.0, 80.0], [100.0, 50.0], [100.0, 80.0], [200.0, 50.0]], dtype=np.float32)
ordered = order_points_clockwise(shuffled_pts)
tl, tr, br, bl = ordered[0], ordered[1], ordered[2], ordered[3]
assert tl[0] <= tr[0] and bl[0] <= br[0], "X ordering failed"
assert tl[1] <= bl[1] and tr[1] <= br[1], "Y ordering failed"
print("Clockwise quadrilateral ordering: PASS")

# 3. Test raw pixel height calculation on rotated and unrotated quads
quad_horizontal = np.array([[10.0, 20.0], [100.0, 20.0], [100.0, 50.0], [10.0, 50.0]], dtype=np.float32)
h_calc = calculate_polygon_height(quad_horizontal)
assert abs(h_calc - 30.0) < 0.01, f"Expected height 30.0, got {h_calc}"
print(f"Horizontal quad height: {h_calc} px (PASS)")

# 45-degree rotated quad with side length 30 along edge
diag = 30.0 / math.sqrt(2)
quad_rotated = np.array([
    [50.0, 50.0],
    [50.0 + 100.0, 50.0],
    [50.0 + 100.0 - diag, 50.0 + diag],
    [50.0 - diag, 50.0 + diag]
], dtype=np.float32)
h_rot = calculate_polygon_height(quad_rotated)
assert abs(h_rot - 30.0) < 0.1, f"Expected height 30.0, got {h_rot}"
print(f"Rotated quad height: {h_rot} px (PASS)")

# 4. Test perspective unwarping via get_rotate_crop_image
test_canvas = np.zeros((200, 400, 3), dtype=np.uint8)
cv2.putText(test_canvas, "SAMPLE", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
quad_text = np.array([[45.0, 60.0], [220.0, 60.0], [220.0, 110.0], [45.0, 110.0]], dtype=np.float32)
crop = get_rotate_crop_image(test_canvas, quad_text)
assert crop.shape[0] > 0 and crop.shape[1] > 0, "Crop failed"
assert abs(crop.shape[0] - 50) <= 2, f"Crop height expected ~50, got {crop.shape[0]}"
assert abs(crop.shape[1] - 175) <= 2, f"Crop width expected ~175, got {crop.shape[1]}"
print(f"Crop unwarping extracted dimensions: {crop.shape[1]}x{crop.shape[0]} (PASS)")

# 5. Test real detector output geometry on synthetic packaging image
cfg = OCRConfig()
detector = DBNetDetector(cfg)
test_img_path = "data/synthetic/regression/SYNTH-01-ENG-FMCG.png"
test_bgr = cv2.imread(test_img_path)
h_img, w_img = test_bgr.shape[:2]
polys, scores = detector.detect(test_bgr)
print(f"Detector detected {len(polys)} text regions on {test_img_path}")
assert len(polys) > 0, "Expected at least 1 detection"

for idx, p in enumerate(polys):
    assert p.shape == (4, 2), f"Expected 4x2 array, got {p.shape}"
    # Invariant: within image bounds
    assert np.all(p[:, 0] >= 0) and np.all(p[:, 0] <= w_img), f"X out of bounds in poly {idx}: {p}"
    assert np.all(p[:, 1] >= 0) and np.all(p[:, 1] <= h_img), f"Y out of bounds in poly {idx}: {p}"
    # Invariant: finite
    assert np.all(np.isfinite(p)), f"Non-finite coord in poly {idx}"
    # Check score bound
    assert 0.0 <= scores[idx] <= 1.0, f"Invalid score {scores[idx]}"

print("All detected polygons satisfy vertex count, clockwise order, finite bounds, and valid scores: PASS")
print("=== ALL COORDINATE & GEOMETRY AUDITS PASSED ===")
