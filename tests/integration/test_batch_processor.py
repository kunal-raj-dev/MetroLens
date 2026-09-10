"""
Integration Tests for Retail Raid Batch Processor & ZIP Stream Defense
======================================================================
Tests bounded ZIP reads, directory traversal defenses, and faithful aggregation
using a test-only pipeline replacement. These are not live OCR accuracy tests.
"""

import io
import zipfile
from types import SimpleNamespace
import pytest
from PIL import Image, ImageDraw

from apps.api.services.batch_processor import (
    RetailRaidBatchProcessor,
    RaidBatchReport,
)
from apps.api.services import batch_processor as batch_module


@pytest.fixture
def pipeline_stub(monkeypatch):
    """Inject observations only in tests; use the current pipeline signature."""
    calls = []

    def inspect(*, image_bytes, filename):
        calls.append((filename, image_bytes))
        return _response()

    monkeypatch.setattr(batch_module.pipeline_orchestrator, "orchestrate_inspection", inspect)
    return calls


def _response(state="MANUAL_REVIEW_REQUIRED", failed_groups=()):
    return SimpleNamespace(
        inspection_id="INSP-BATCH-TEST",
        state=state,
        declarations=SimpleNamespace(
            net_quantity_value=100, net_quantity_unit="g", mrp_inr=40,
            commodity_name="Test specimen",
        ),
        rule_evaluations=SimpleNamespace(
            rule6_mandatory_status=SimpleNamespace(overall_status="FAIL" if "Rule 6(1)" in failed_groups else "REVIEW"),
            usp_audit=SimpleNamespace(status="FAIL" if "Rule 6(11)" in failed_groups else "REVIEW"),
            font_height_audit=SimpleNamespace(status="FAIL" if "Rule 7" in failed_groups else "REVIEW"),
        ),
    )


def _archive(entries, compression=zipfile.ZIP_STORED):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=compression) as archive:
        for name, data in entries:
            archive.writestr(name, data)
    return buf.getvalue()


def _process(processor, payload):
    return processor.process_zip_archive(payload, "Test Store", "Test District", "Test State")


def _create_sample_jpeg_bytes(text: str = "SAMPLE") -> bytes:
    img = Image.new("RGB", (1000, 800), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    draw.text((60, 60), text, fill=(20, 20, 20))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def test_batch_processor_valid_zip_archive(pipeline_stub):
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
    assert len(pipeline_stub) == 3
    assert report.review_required_count == 3
    assert report.compliant_count == report.non_compliant_count == 0
    assert report.total_potential_compounding_inr == 0


def test_batch_processor_zip_slip_traversal_defense(pipeline_stub):
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


@pytest.mark.parametrize("state", ["MANUAL_REVIEW_REQUIRED", "UNCERTAIN", "FLAGGED_FOR_REVIEW", "DEVIATION_DETECTED"])
def test_review_is_not_a_violation_or_penalty(monkeypatch, state):
    monkeypatch.setattr(batch_module.pipeline_orchestrator, "orchestrate_inspection",
                        lambda **kwargs: _response(state))
    report = _process(RetailRaidBatchProcessor(), _archive([("photo.jpg", _create_sample_jpeg_bytes())]))
    assert report.review_required_count == 1
    assert report.compliant_count == report.non_compliant_count == 0
    assert report.violations_by_rule == {}
    assert report.itemized_results[0].violations_count == 0
    assert report.itemized_results[0].violated_rules == []
    assert report.total_potential_compounding_inr == 0
    assert report.to_dict()["compounding_estimate_available"] is False


def test_exemption_is_kept_separate_from_compliance(monkeypatch):
    monkeypatch.setattr(batch_module.pipeline_orchestrator, "orchestrate_inspection",
                        lambda **kwargs: _response("EXEMPTED"))
    report = _process(RetailRaidBatchProcessor(), _archive([("photo.jpg", _create_sample_jpeg_bytes())]))
    assert report.exempted_count == 1
    assert report.review_required_count == report.non_compliant_count == report.compliant_count == 0
    assert report.itemized_results[0].overall_verdict == "EXEMPTED"
    assert report.itemized_results[0].violated_rules == []


def test_potential_failure_preserves_actual_rule_groups_without_penalty(monkeypatch):
    monkeypatch.setattr(batch_module.pipeline_orchestrator, "orchestrate_inspection",
                        lambda **kwargs: _response("POTENTIAL_NON_COMPLIANCE", ("Rule 6(11)", "Rule 7")))
    report = _process(RetailRaidBatchProcessor(), _archive([("photo.jpg", _create_sample_jpeg_bytes())]))
    assert report.potential_non_compliance_count == 1
    assert report.non_compliant_count == 0
    assert report.violations_by_rule == {"Rule 6(11)": 1, "Rule 7": 1}
    assert report.itemized_results[0].violations_count == 2
    assert report.itemized_results[0].violated_rules == ["Rule 6(11)", "Rule 7"]
    assert report.total_potential_compounding_inr == 0


def test_pipeline_failure_creates_no_fabricated_assessment(monkeypatch):
    def unavailable(**kwargs):
        raise RuntimeError("OCR unavailable")
    monkeypatch.setattr(batch_module.pipeline_orchestrator, "orchestrate_inspection", unavailable)
    report = _process(RetailRaidBatchProcessor(), _archive([("photo.jpg", _create_sample_jpeg_bytes())]))
    assert report.total_images_processed == 0
    assert report.compliant_count == report.non_compliant_count == 0
    assert "OCR unavailable" in report.rejected_files[0]["reason"]


def test_incompatible_response_does_not_increment_success_counts(monkeypatch):
    monkeypatch.setattr(batch_module.pipeline_orchestrator, "orchestrate_inspection",
                        lambda **kwargs: SimpleNamespace(state="COMPLIANT"))
    report = _process(RetailRaidBatchProcessor(), _archive([("photo.jpg", _create_sample_jpeg_bytes())]))
    assert report.total_images_processed == report.compliant_count == 0
    assert report.violations_by_rule == {}
    assert len(report.rejected_files) == 1


def test_duplicate_zip_name_cannot_substitute_unchecked_member(pipeline_stub, monkeypatch):
    small = _create_sample_jpeg_bytes()
    larger = small + b"extra" * 100
    processor = RetailRaidBatchProcessor()
    monkeypatch.setattr(processor, "MAX_ENTRY_UNCOMPRESSED_BYTES", len(small) + 1, raising=False)
    with pytest.warns(UserWarning, match="Duplicate name"):
        payload = _archive([("photo.jpg", small), ("photo.jpg", larger)])
    report = _process(processor, payload)
    assert pipeline_stub == [("photo.jpg", small)]
    assert report.total_images_processed == 1
    assert len(report.rejected_files) == 1


def test_oversized_member_is_rejected_before_decompression(pipeline_stub, monkeypatch):
    processor = RetailRaidBatchProcessor()
    monkeypatch.setattr(processor, "MAX_ENTRY_UNCOMPRESSED_BYTES", 32, raising=False)
    payload = _archive([("photo.jpg", b"\xff\xd8\xff" + b"x" * 30)])
    monkeypatch.setattr(zipfile.ZipFile, "open", lambda *args, **kwargs: pytest.fail("Oversized member must not be decompressed"))
    report = _process(processor, payload)
    assert pipeline_stub == []
    assert report.total_images_processed == 0
    assert "size" in report.rejected_files[0]["reason"].lower()


@pytest.mark.parametrize("name", ["C:\\outside.jpg", "C:outside.jpg", "nested\\..\\outside.jpg", "../outside.jpg", "/outside.jpg"])
def test_cross_platform_archive_paths_are_rejected(pipeline_stub, name):
    report = _process(RetailRaidBatchProcessor(), _archive([(name, _create_sample_jpeg_bytes())]))
    assert pipeline_stub == []
    assert report.total_images_processed == 0
    assert "traversal" in report.rejected_files[0]["reason"].lower()


@pytest.mark.parametrize("limit", ["MAX_ARCHIVE_BYTES", "MAX_TOTAL_UNCOMPRESSED_BYTES", "MAX_ZIP_ENTRIES"])
def test_archive_budgets_stop_inspection(pipeline_stub, monkeypatch, limit):
    processor = RetailRaidBatchProcessor()
    monkeypatch.setattr(processor, limit, 1)
    payload = _archive([("first.jpg", _create_sample_jpeg_bytes()), ("second.jpg", _create_sample_jpeg_bytes())])
    report = _process(processor, payload)
    assert pipeline_stub == []
    assert report.total_images_processed == 0
    assert report.rejected_files[0]["filename"] == "ARCHIVE"


def test_high_compression_ratio_is_rejected_without_inference(pipeline_stub):
    payload = _archive([("photo.jpg", b"\xff\xd8\xff" + b"x" * 100_000)], zipfile.ZIP_DEFLATED)
    report = _process(RetailRaidBatchProcessor(), payload)
    assert pipeline_stub == []
    assert report.total_images_processed == 0
    assert "compression ratio" in report.rejected_files[0]["reason"].lower()
