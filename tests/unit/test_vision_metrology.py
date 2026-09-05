"""
Unit Test Suite for Physical Vision Metrology Subsystem
======================================================
Tests geometric unwrapping of curved container labels, Rule 7 sub-pixel stroke
and character geometry profiling, and ISO/IEC 15416 barcode print quality corroboration.
"""

import datetime
import numpy as np
import pytest
import cv2

from apps.api.verification.geometric_unwrapping import (
    GeometricUnwrapper,
    CylinderParameters,
    ConicalParameters,
    Point2D,
    SurfaceType,
    InterpolationMethod,
    UnwrapResult,
)
from apps.api.verification.stroke_profile import (
    StrokeProfiler,
    StrokeVerdict,
    Rule7ComplianceReport,
    GlyphMeasurement,
    TextLineProfile,
    EXEMPT_CHARACTERS,
)
from apps.api.verification.barcode_verifier import (
    BarcodeVerifier,
    BarcodeVerificationResult,
    ISO15416Parameters,
    ISOGrade,
    SymbologyType,
    DeclarationDiscrepancy,
    GS1ParsedData,
)


# =============================================================================
# 1. Geometric Surface Unwrapping Tests
# =============================================================================

class TestGeometricUnwrapper:
    """Test suite for cylinder, cone, and perspective planar unwarping."""

    @pytest.fixture
    def sample_cylindrical_image(self):
        """Generates a synthetic cylindrical label image."""
        h, w = 200, 300
        img = np.full((h, w, 3), 220, dtype=np.uint8)
        # Draw horizontal text lines
        for y in range(40, 180, 30):
            cv2.line(img, (20, y), (280, y), (30, 30, 30), 2)
        # Add shading simulating cylinder curvature
        for x in range(w):
            factor = np.sin((x / w) * np.pi)
            img[:, x] = (img[:, x] * factor).astype(np.uint8)
        return img

    def test_cylinder_unwrap_success(self, sample_cylindrical_image):
        unwrapper = GeometricUnwrapper()
        params = CylinderParameters(
            axis_x=150.0,
            radius=120.0,
            tilt_deg=0.0,
            viewing_distance_px=2000.0,
        )
        res = unwrapper.unwrap_cylinder(sample_cylindrical_image, params, angular_span_deg=100.0)

        assert isinstance(res, UnwrapResult)
        assert res.surface_type == SurfaceType.CYLINDRICAL
        assert res.rectified_image.shape[0] == sample_cylindrical_image.shape[0]
        assert res.rectified_image.shape[1] > 50
        assert res.mask.shape == res.rectified_image.shape[:2]
        assert len(res.foreshortening_lut) == res.rectified_image.shape[1]
        assert res.metrics.edge_straightness_index >= 0.0
        assert res.metrics.valid_pixel_mask_ratio > 0.50

    def test_cylinder_unwrap_with_tilt(self, sample_cylindrical_image):
        unwrapper = GeometricUnwrapper()
        params = CylinderParameters(
            axis_x=150.0,
            radius=120.0,
            tilt_deg=5.0,
        )
        res = unwrapper.unwrap_cylinder(sample_cylindrical_image, params)
        assert res.rectified_image is not None
        assert res.parameters_used["tilt_deg"] == 5.0

    def test_cylinder_validation_errors(self):
        unwrapper = GeometricUnwrapper()
        # Radius too small
        with pytest.raises(ValueError, match="unrealistically small"):
            p = CylinderParameters(axis_x=100.0, radius=5.0)
            p.validate(image_width=200)

        # Axis out of bounds
        with pytest.raises(ValueError, match="outside reasonable"):
            p = CylinderParameters(axis_x=500.0, radius=50.0)
            p.validate(image_width=200)

    def test_conical_frustum_unroll(self, sample_cylindrical_image):
        unwrapper = GeometricUnwrapper()
        params = ConicalParameters(
            apex=Point2D(x=150.0, y=-200.0),
            top_radius=80.0,
            bottom_radius=120.0,
            height=200.0,
        )
        res = unwrapper.unwrap_cone(sample_cylindrical_image, params)
        assert isinstance(res, UnwrapResult)
        assert res.surface_type == SurfaceType.CONICAL
        assert res.rectified_image.shape[0] > 0
        assert res.rectified_image.shape[1] > 0

    def test_planar_quadrilateral_rectification(self, sample_cylindrical_image):
        unwrapper = GeometricUnwrapper()
        corners = [(20.0, 30.0), (280.0, 10.0), (290.0, 190.0), (10.0, 170.0)]
        res = unwrapper.rectify_planar_quadrilateral(
            sample_cylindrical_image,
            corners=corners,
            target_aspect_ratio=1.5,
        )
        assert isinstance(res, UnwrapResult)
        assert res.surface_type == SurfaceType.PLANAR_SKEWED
        assert res.metrics.aspect_ratio_restoration_factor > 1.0


# =============================================================================
# 2. Sub-Pixel Stroke Geometry & Rule 7 Profiler Tests
# =============================================================================

class TestStrokeProfiler:
    """Test suite for Rule 7 character geometry, height, width, and stroke thickness."""

    @pytest.fixture
    def profiler(self):
        return StrokeProfiler(min_glyph_pixels=6)

    @pytest.fixture
    def synthetic_text_roi(self):
        """Generates synthetic image containing characters 'MRP Rs 250'."""
        img = np.full((60, 200, 3), 255, dtype=np.uint8)
        # Render clean black text
        cv2.putText(img, "MRP Rs 250", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), thickness=3)
        return img

    def test_zhang_suen_skeletonization(self, profiler):
        # Create a solid black square on white canvas
        binary = np.zeros((40, 40), dtype=np.uint8)
        binary[10:30, 10:30] = 255
        skel = profiler.zhang_suen_skeleton(binary)

        assert skel.shape == (40, 40)
        assert np.count_nonzero(skel) > 0
        # Medial axis should have much fewer pixels than original area (400 pixels)
        assert np.count_nonzero(skel) < 150

    def test_analyze_roi_compliant_text(self, profiler, synthetic_text_roi):
        report = profiler.analyze_roi(
            roi_image=synthetic_text_roi,
            expected_text="MRP Rs 250",
            pixels_per_mm=8.0,
            statutory_min_height_mm=1.5,
            declaration_key="mrp",
        )

        assert isinstance(report, Rule7ComplianceReport)
        assert report.declaration_key == "mrp"
        assert report.detailed_line_profile.num_glyphs > 0
        assert report.is_height_compliant is True

    def test_stroke_too_thin_detection(self, profiler):
        img = np.full((80, 200, 3), 255, dtype=np.uint8)
        # Tall 60px font with thin 1px stroke
        cv2.putText(img, "NET 500g", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 0), thickness=1)

        report = profiler.analyze_roi(
            roi_image=img,
            expected_text="NET 500g",
            pixels_per_mm=10.0,
            statutory_min_height_mm=1.0,
            declaration_key="net_quantity",
        )
        assert report.detailed_line_profile.median_stroke_to_height_ratio <= 0.20

    def test_exempt_characters_rule7(self, profiler):
        # Test character '1' and 'l' which are statutory exempt from the 1/3 width requirement
        for ch in ("1", "l", "I", "i"):
            assert ch in EXEMPT_CHARACTERS


# =============================================================================
# 3. Barcode Print Quality & Corroboration Tests
# =============================================================================

class TestBarcodeVerifier:
    """Test suite for ISO/IEC 15416 print quality grading and Legal Metrology corroboration."""

    @pytest.fixture
    def verifier(self):
        return BarcodeVerifier(num_scanlines=8)

    @pytest.fixture
    def synthetic_barcode_roi(self):
        """Generates a synthetic high-contrast 1D barcode pattern."""
        h, w = 100, 240
        img = np.full((h, w), 245, dtype=np.uint8)  # White quiet zone
        # Draw alternating vertical black bars
        x = 30
        pattern = [2, 1, 3, 1, 1, 2, 4, 2, 1, 3, 2, 1, 1, 3, 2, 2, 1, 4]
        for idx, width in enumerate(pattern):
            if idx % 2 == 0:
                cv2.rectangle(img, (x, 15), (x + width * 4, 85), 15, -1)
            x += width * 4
        return img

    def test_iso_15416_grading_clean_symbol(self, verifier, synthetic_barcode_roi):
        res = verifier.verify_barcode(synthetic_barcode_roi)

        assert isinstance(res, BarcodeVerificationResult)
        assert isinstance(res.iso_grading, ISO15416Parameters)
        assert res.iso_grading.symbol_contrast > 0.60
        assert res.iso_grading.overall_iso_letter in (ISOGrade.A, ISOGrade.B, ISOGrade.C, ISOGrade.D, ISOGrade.F)

    def test_ean_checksum_validation(self, verifier):
        # Valid EAN-13
        assert verifier._validate_ean_checksum("8901030383847") is True
        # Invalid checksum
        assert verifier._validate_ean_checksum("8901030383849") is False
        # Short string
        assert verifier._validate_ean_checksum("12345") is False

    def test_gs1_ai_parsing(self, verifier):
        payload = "(01)08901030383848(10)LOT778(17)261231(3103)000500(3922)0015000"
        data = verifier._parse_gs1_identifiers(payload)

        assert isinstance(data, GS1ParsedData)
        assert data.gtin == "08901030383848"
        assert data.batch_lot == "LOT778"
        assert data.exp_date == datetime.date(2026, 12, 31)
        assert data.net_weight_kg == 0.500  # 500 / 10^3 = 0.500 kg
        assert data.mrp_inr == 150.0  # 15000 / 10^2 = 150.0

    def test_metrological_cross_corroboration_match(self, verifier, synthetic_barcode_roi):
        ocr_data = {
            "mrp": "150.00",
            "net_quantity": "500 g",
            "batch": "LOT778",
            "exp_date": "2026-12-31",
        }
        res = verifier.verify_barcode(synthetic_barcode_roi, human_readable_ocr=ocr_data)
        assert isinstance(res, BarcodeVerificationResult)

    def test_metrological_cross_corroboration_discrepancy(self, verifier, synthetic_barcode_roi):
        # Deliberate mismatch: OCR claims MRP ₹250.00, but barcode has ₹150.00
        gs1 = GS1ParsedData(
            gtin="8901030383848",
            net_weight_kg=0.500,
            mrp_inr=150.0,
            batch_lot="BATCH-A",
            exp_date=datetime.date(2026, 10, 31),
        )
        ocr = {
            "mrp": "250.00",
            "net_quantity": "1 kg",  # Conflict: 1 kg vs 0.5 kg
            "batch": "BATCH-Z",     # Conflict: BATCH-Z vs BATCH-A
            "exp_date": "2025-01-01", # Conflict: > 30 days off
        }
        discrepancies = verifier._cross_corroborate_declarations(gs1, ocr)

        assert len(discrepancies) >= 3
        fields = [d.field_name for d in discrepancies]
        assert "net_quantity" in fields
        assert "mrp" in fields
        assert "batch_number" in fields
