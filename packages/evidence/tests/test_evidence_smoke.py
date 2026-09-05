"""
Smoke test for nirikshak-evidence.
"""

from nirikshak_evidence import compute_sha256, create_evidence_item
from nirikshak_shared.models.primitives import BoundingBox, CalibrationStatus, ObservedValue


def test_compute_sha256():
    digest = compute_sha256(b"Nirikshak Test Payload")
    assert len(digest) == 64
    assert isinstance(digest, str)


def test_create_evidence_item_valid():
    dummy_sha = "0" * 64
    item = create_evidence_item(
        evidence_id="ev_001",
        image_sha256=dummy_sha,
        bounding_box=BoundingBox(x_min=0, y_min=0, x_max=50, y_max=50),
        calibration_status=CalibrationStatus.UNCALIBRATED,
        observed_value=ObservedValue(raw_text="Sample text"),
    )
    assert item.evidence_id == "ev_001"
    assert item.image_sha256 == dummy_sha
