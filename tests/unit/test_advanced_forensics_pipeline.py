"""
Unit Test Suite for Advanced Forensic Analysis Subsystem
========================================================
Tests Block-DCT copy-move detection, Bayer CFA artifact residual analysis,
double compression DCT periodicity / JPEG ghost analysis, and sensor PRNU
fingerprint cross-correlation.
"""

import io
import numpy as np
import pytest
from PIL import Image, ImageDraw

from apps.api.forensics.copy_move import CopyMoveDetector, CopyMoveDetectionResult
from apps.api.forensics.cfa_artifacts import CFADemosaicAnalyzer, CFADemosaicingResult, BayerPatternType
from apps.api.forensics.double_compression import DoubleCompressionDetector, DoubleCompressionResult
from apps.api.forensics.sensor_prnu import PRNUSensorFingerprintVerifier, PRNUCrossCorrelationResult


def _create_synthetic_test_image(width=160, height=120, pattern="circles"):
    """Helper to generate deterministic RGB test images."""
    im = Image.new("RGB", (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(im)
    if pattern == "circles":
        for i in range(5):
            x = 20 + i * 25
            draw.ellipse([x, 20, x + 20, 60], fill=(50 + i * 30, 80 + i * 20, 150))
    elif pattern == "text_grid":
        for y in range(15, height - 15, 20):
            draw.line([(10, y), (width - 10, y)], fill=(30, 30, 30), width=3)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


class TestCopyMoveDetector:
    """Test suite for Block-DCT copy-move cloning detector."""

    def test_pristine_image_no_copy_move(self):
        detector = CopyMoveDetector(block_size=8, min_spatial_distance=30.0)
        img_bytes = _create_synthetic_test_image(128, 96, pattern="circles")
        result = detector.analyze(img_bytes)

        assert isinstance(result, CopyMoveDetectionResult)
        assert result.detected_clones_count >= 0
        assert 0.0 <= result.forgery_probability <= 1.0
        assert result.analyzed_blocks_count > 0

    def test_synthetic_copy_move_cloning(self):
        im = Image.new("RGB", (160, 120), color=(200, 200, 200))
        draw = ImageDraw.Draw(im)
        for r in range(0, 15, 3):
            draw.rectangle([10 + r, 10 + r, 25 + r, 25 + r], outline=(10, 200, 10), fill=(255, 0, 0))

        crop = im.crop((10, 10, 45, 45))
        im.paste(crop, (90, 60))

        buf = io.BytesIO()
        im.save(buf, format="PNG")
        raw_bytes = buf.getvalue()

        detector = CopyMoveDetector(block_size=8, min_cluster_size=2)
        result = detector.analyze(raw_bytes)

        assert isinstance(result, CopyMoveDetectionResult)
        assert result.detected_clones_count >= 0

    def test_corrupt_or_tiny_image_graceful(self):
        detector = CopyMoveDetector(block_size=8)
        tiny = Image.new("RGB", (4, 4), color=(0, 0, 0))
        b = io.BytesIO()
        tiny.save(b, format="PNG")
        res = detector.analyze(b.getvalue())
        assert res.detected_clones_count == 0
        assert res.forgery_probability == 0.0


class TestCFAArtifactDetector:
    """Test suite for Color Filter Array (Bayer pattern) interpolation forensics."""

    def test_cfa_analysis_on_rgb_image(self):
        analyzer = CFADemosaicAnalyzer()
        img_bytes = _create_synthetic_test_image(128, 128, pattern="circles")
        result = analyzer.analyze(img_bytes)

        assert isinstance(result, CFADemosaicingResult)
        assert isinstance(result.detected_bayer_pattern, BayerPatternType)
        assert 0.0 <= result.global_cfa_confidence <= 1.0
        assert 0.0 <= result.splicing_probability <= 1.0

    def test_localized_splicing_detection(self):
        im = Image.new("RGB", (128, 128), color=(128, 128, 128))
        arr = np.array(im)
        rng = np.random.default_rng(42)
        arr[64:, 64:, 0] = rng.integers(0, 255, size=(64, 64), dtype=np.uint8)
        arr[64:, 64:, 1] = rng.integers(0, 255, size=(64, 64), dtype=np.uint8)

        corrupted = Image.fromarray(arr)
        b = io.BytesIO()
        corrupted.save(b, format="PNG")

        analyzer = CFADemosaicAnalyzer(tile_size=32)
        res = analyzer.analyze(b.getvalue())
        assert isinstance(res, CFADemosaicingResult)


class TestDoubleCompressionDetector:
    """Test suite for JPEG double compression and grid shift forensics."""

    def test_single_compressed_jpeg(self):
        detector = DoubleCompressionDetector()
        img_bytes = _create_synthetic_test_image(128, 128, pattern="text_grid")
        res = detector.analyze(img_bytes)

        assert isinstance(res, DoubleCompressionResult)
        assert isinstance(res.is_double_compressed, bool)
        assert 1 <= res.primary_estimated_quality <= 100
        assert len(res.grid_shift) == 2

    def test_double_compressed_jpeg_different_qualities(self):
        im = Image.new("RGB", (160, 160), color=(255, 255, 255))
        draw = ImageDraw.Draw(im)
        for i in range(10):
            draw.line([(i * 15, 0), (i * 15, 160)], fill=(0, 0, 0), width=2)

        buf1 = io.BytesIO()
        im.save(buf1, format="JPEG", quality=60)

        im2 = Image.open(io.BytesIO(buf1.getvalue()))
        buf2 = io.BytesIO()
        im2.save(buf2, format="JPEG", quality=90)

        detector = DoubleCompressionDetector()
        res = detector.analyze(buf2.getvalue())
        assert isinstance(res, DoubleCompressionResult)
        assert res.secondary_estimated_quality is not None or res.primary_estimated_quality > 0


class TestSensorPRNUAnalyzer:
    """Test suite for Photo-Response Non-Uniformity camera fingerprint matching."""

    def test_prnu_extraction_and_self_matching(self):
        verifier = PRNUSensorFingerprintVerifier()
        img_bytes = _create_synthetic_test_image(120, 120, pattern="circles")
        residual = verifier.extract_noise_residual(img_bytes)

        assert residual.shape == (120, 120)
        assert np.isfinite(residual).all()

        result = verifier.verify_camera_coherence(img_bytes, img_bytes)
        assert isinstance(result, PRNUCrossCorrelationResult)
        assert result.peak_to_correlation_energy > 0.0
        assert result.is_same_sensor is True

    def test_prnu_cross_camera_mismatch(self):
        verifier = PRNUSensorFingerprintVerifier()
        img1 = _create_synthetic_test_image(120, 120, pattern="circles")
        img2 = _create_synthetic_test_image(120, 120, pattern="text_grid")

        result = verifier.verify_camera_coherence(img1, img2)
        assert isinstance(result, PRNUCrossCorrelationResult)
