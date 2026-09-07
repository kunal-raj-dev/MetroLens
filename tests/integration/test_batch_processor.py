"""
Integration Tests for Retail Raid Batch Processor & ZIP Stream Defense
======================================================================
Tests safe ZIP extraction, directory traversal (Zip-Slip) defenses,
zip-bomb mitigation, and aggregated district enforcement reports.
"""

import io
import zipfile
import pytest
from PIL import Image, ImageDraw

from apps.api.services.batch_processor import (
    RetailRaidBatchProcessor,
    RaidBatchReport,
)


def _create_sample_jpeg_bytes(text: str = "SAMPLE") -> bytes:
    img = Image.new("RGB", (1000, 800), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    draw.text((60, 60), text, fill=(20, 20, 20))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def test_batch_processor_valid_zip_archive():
    """Verify safe unpacking and aggregated inspection report for multiple packaging photos."""
    processor = RetailRaidBatchProcessor()

    # Create in-memory ZIP with 3 valid packaging images
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("shelf_biscuit_01.jpg", _create_sample_jpeg_bytes("Biscuits 100g"))
        zf.writestr("shelf_oil_02.jpg", _create_sample_jpeg_bytes("Edible Oil 1L"))
        zf.writestr("shelf_chips_03.jpg", _create_sample_jpeg_bytes("Potato Chips 40g"))

    report = processor.process_zip_archive(
        zip_bytes=zip_buffer.getvalue(),
        establishment_name="MegaMart Hypermarket #14",
        district="Bengaluru Urban",
        state="Karnataka",
    )

    assert isinstance(report, RaidBatchReport)
    assert report.total_images_processed == 3
    assert report.establishment_name == "MegaMart Hypermarket #14"
    assert report.compliance_rate_percent >= 0.0
    assert len(report.itemized_results) == 3
    assert len(report.rejected_files) == 0


def test_batch_processor_zip_slip_traversal_defense():
    """Verify that malicious directory traversal filenames (Zip-Slip) are rejected."""
    processor = RetailRaidBatchProcessor()

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        # Malicious traversal path
        zf.writestr("../../etc/passwd.jpg", _create_sample_jpeg_bytes())
        zf.writestr("safe_photo.jpg", _create_sample_jpeg_bytes())

    report = processor.process_zip_archive(
        zip_bytes=zip_buffer.getvalue(),
        establishment_name="Test Store",
        district="Central Delhi",
        state="Delhi",
    )

    # Safe file processed, traversal file rejected
    assert report.total_images_processed == 1
    assert len(report.rejected_files) >= 1
    assert any("traversal" in r["reason"].lower() for r in report.rejected_files)


def test_batch_processor_corrupt_archive_handles_gracefully():
    """Verify that corrupt or truncated ZIP data returns safe error report without crashing."""
    processor = RetailRaidBatchProcessor()

    corrupt_zip = b"PK\x03\x04" + b"\x00" * 40

    report = processor.process_zip_archive(
        zip_bytes=corrupt_zip,
        establishment_name="Test Store",
        district="South Delhi",
        state="Delhi",
    )

    assert report.total_images_processed == 0
    assert len(report.rejected_files) > 0
    assert "corrupt" in report.rejected_files[0]["reason"].lower()
