"""
Unit Tests for Media Forensics & Steganography Defense
======================================================
Verifies Error Level Analysis (ELA), Steganography chunk scanning,
ICC profile parsing/sanitizing, and Perceptual Hashing (aHash/dHash/pHash).
"""

import io
import struct
import pytest
from PIL import Image, ImageDraw

from apps.api.forensics.ela import ErrorLevelAnalyzer, ELAResult
from apps.api.forensics.steganography import (
    SteganographyScanner,
    SteganographyScanResult,
    ChunkSanitizationResult,
)
from apps.api.forensics.icc_sanitizer import ICCProfileSanitizer, ICCSanitizationResult
from apps.api.forensics.perceptual_hash import PerceptualHasher, PerceptualHashResult


def _create_sample_jpeg(width: int = 200, height: int = 150) -> bytes:
    img = Image.new("RGB", (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 100, 80], fill=(20, 120, 200), outline=(0, 0, 0))
    draw.text((30, 30), "MRP Rs. 150.00", fill=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def _create_sample_png(width: int = 200, height: int = 150) -> bytes:
    img = Image.new("RGB", (width, height), color=(250, 250, 250))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 80, 50], fill=(180, 40, 40))
    draw.text((15, 15), "Net Qty: 500g", fill=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# 1. Error Level Analysis (ELA) Tests
# ---------------------------------------------------------------------------

def test_ela_analyzer_clean_image():
    """Verify that a standard clean JPEG generates a valid ELAResult with low error variance."""
    analyzer = ErrorLevelAnalyzer(default_resave_quality=90)
    raw_jpeg = _create_sample_jpeg()

    result = analyzer.analyze(raw_jpeg, generate_visual_ela=True)
    assert isinstance(result, ELAResult)
    assert result.global_mean_error >= 0.0
    assert result.resave_quality == 90
    assert result.tamper_verdict in {"CLEAN", "INCONCLUSIVE"}
    assert result.ela_image_bytes is not None
    assert len(result.ela_image_bytes) > 0

    # Ensure serialized dict matches contract
    d = result.to_dict(include_image_bytes=True)
    assert "tamper_probability" in d
    assert "global_mean_error" in d
    assert "anomaly_regions" in d


def test_ela_analyzer_corrupted_payload_handles_gracefully():
    """Verify that corrupt byte payload does not raise unhandled exception."""
    analyzer = ErrorLevelAnalyzer()
    corrupt_bytes = b"\xFF\xD8\xFF" + b"\x00" * 50
    result = analyzer.analyze(corrupt_bytes)
    assert result.tamper_verdict == "INCONCLUSIVE"
    assert len(result.forensic_notes) > 0


def test_ela_tamper_detection_on_spliced_region():
    """Verify that splicing a low-quality region onto a high-quality background creates detectable ELA variance."""
    base_img = Image.new("RGB", (400, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(base_img)
    draw.rectangle([50, 50, 350, 250], fill=(100, 150, 200))

    # Save at high quality 98%
    buf_hq = io.BytesIO()
    base_img.save(buf_hq, format="JPEG", quality=98)
    hq_img = Image.open(buf_hq)

    # Create a spliced patch saved at very low quality 20%
    patch = Image.new("RGB", (100, 80), color=(255, 0, 0))
    buf_lq = io.BytesIO()
    patch.save(buf_lq, format="JPEG", quality=20)
    lq_patch = Image.open(buf_lq)

    # Paste low quality patch onto high quality image
    hq_img.paste(lq_patch, (60, 60))
    spliced_buf = io.BytesIO()
    hq_img.save(spliced_buf, format="JPEG", quality=98)

    analyzer = ErrorLevelAnalyzer(default_resave_quality=90, anomaly_sigma_threshold=2.0)
    result = analyzer.analyze(spliced_buf.getvalue())
    assert result.global_max_error > 0
    assert len(result.detected_anomaly_regions) >= 0


# ---------------------------------------------------------------------------
# 2. Steganography & Chunk Sanitization Tests
# ---------------------------------------------------------------------------

def test_steganography_scanner_clean_png():
    """Verify scanner on clean PNG without suspicious chunks or trailing payloads."""
    scanner = SteganographyScanner()
    clean_png = _create_sample_png()

    res = scanner.scan(clean_png)
    assert res.is_clean is True
    assert res.detected_format == "PNG"
    assert res.trailing_payload_bytes == 0
    assert len(res.suspicious_chunks) == 0


def test_steganography_scanner_detects_appended_trailing_payload():
    """Verify detection of malicious payload appended beyond PNG IEND marker."""
    scanner = SteganographyScanner()
    clean_png = _create_sample_png()
    malicious_payload = clean_png + b"<?php system($_GET['cmd']); ?>"

    res = scanner.scan(malicious_payload)
    assert res.trailing_payload_bytes == len(b"<?php system($_GET['cmd']); ?>")
    assert res.is_clean is False
    assert res.suspicion_score > 0.3
    assert any("trailing payload" in alert.lower() for alert in res.forensic_alerts)


def test_steganography_png_chunk_sanitization():
    """Verify stripping of non-essential ancillary chunks while preserving valid PNG structure."""
    clean_png = _create_sample_png()
    scanner = SteganographyScanner()

    # Artificially inject an ancillary tEXt chunk
    iend_pos = clean_png.find(b"IEND")
    assert iend_pos != -1
    comment_data = b"Comment\x00Author=Mallory"
    comment_chunk = (
        struct.pack(">I", len(comment_data))
        + b"tEXt"
        + comment_data
        + struct.pack(">I", 0x12345678)
    )
    png_with_text = clean_png[: iend_pos - 4] + comment_chunk + clean_png[iend_pos - 4 :]

    sanitized_res = scanner.sanitize_png_chunks(png_with_text)
    assert isinstance(sanitized_res, ChunkSanitizationResult)
    assert sanitized_res.stripped_chunks_count >= 1
    assert "tEXt" in sanitized_res.stripped_chunk_types
    assert sanitized_res.sanitized_bytes.startswith(b"\x89PNG\r\n\x1a\n")


# ---------------------------------------------------------------------------
# 3. ICC Profile Sanitizer Tests
# ---------------------------------------------------------------------------

def test_icc_sanitizer_image_without_profile():
    """Verify clean inspection when image lacks ICC profile."""
    sanitizer = ICCProfileSanitizer()
    clean_jpeg = _create_sample_jpeg()
    res = sanitizer.sanitize(clean_jpeg)
    assert res.has_icc_profile is False
    assert res.is_profile_valid is True
    assert res.is_sanitized is False


def test_icc_sanitizer_validates_acsp_signature():
    """Verify that corrupt ICC bytes lacking 'acsp' signature are rejected."""
    sanitizer = ICCProfileSanitizer()
    # Construct a malformed 140-byte ICC profile without 'acsp'
    fake_icc = bytearray(140)
    struct.pack_into(">I", fake_icc, 0, 140)  # declared length
    fake_icc[8] = 4  # version 4
    fake_icc[36:40] = b"XXXX"  # Invalid signature instead of 'acsp'

    is_valid, ver, cs, pcs, dev, tags, actions = sanitizer._validate_icc_bytes(bytes(fake_icc))
    assert is_valid is False
    assert any("invalid icc file signature" in a.lower() for a in actions)


# ---------------------------------------------------------------------------
# 4. Perceptual Hashing Tests
# ---------------------------------------------------------------------------

def test_perceptual_hasher_reproducibility():
    """Verify that identical images yield identical aHash, dHash, and pHash."""
    hasher = PerceptualHasher()
    img_bytes = _create_sample_jpeg(250, 200)

    res1 = hasher.compute(img_bytes)
    res2 = hasher.compute(img_bytes)

    assert res1.ahash_hex == res2.ahash_hex
    assert res1.dhash_hex == res2.dhash_hex
    assert res1.phash_hex == res2.phash_hex
    assert res1.hamming_distance(res2, "phash") == 0
    assert res1.similarity(res2, "phash") == 1.0


def test_perceptual_hasher_similarity_under_recompression():
    """Verify that pHash remains highly similar under JPEG recompression."""
    hasher = PerceptualHasher()
    base_bytes = _create_sample_jpeg(300, 200)
    hash_base = hasher.compute(base_bytes)

    # Re-encode at quality 60
    with Image.open(io.BytesIO(base_bytes)) as img:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=60)
        recompressed_bytes = buf.getvalue()

    hash_recomp = hasher.compute(recompressed_bytes)
    distance = hash_base.hamming_distance(hash_recomp, "phash")
    sim = hash_base.similarity(hash_recomp, "phash")

    # Recompressed version should have low Hamming distance (< 8 bits difference out of 64)
    assert distance <= 8
    assert sim >= 0.875
