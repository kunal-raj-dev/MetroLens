"""
Unit Tests for Deep Geometric Font Height, Stroke & Aspect Ratio Analyzer
========================================================================
Verifies Rule 7(1) Table I minimum numeral heights, width-to-height ratio,
stroke thickness, and inter-character spacing constraints.
"""

import pytest

from apps.api.verification.font_geometry import (
    FontGeometryAnalyzer,
    NumeralGeometryAuditResult,
)


def test_font_geometry_table_1_height_tiers():
    """Verify Table I minimum numeral height thresholds across PDP area tiers."""
    analyzer = FontGeometryAnalyzer()

    # Tier 1: Area <= 50 cm2 -> 1.0 mm (blown: 2.0 mm)
    assert analyzer.compute_required_minimum_height(40.0, is_blown_moulded=False) == 1.0
    assert analyzer.compute_required_minimum_height(40.0, is_blown_moulded=True) == 2.0

    # Tier 2: 50 < Area <= 100 cm2 -> 1.5 mm (blown: 3.0 mm)
    assert analyzer.compute_required_minimum_height(80.0, is_blown_moulded=False) == 1.5
    assert analyzer.compute_required_minimum_height(80.0, is_blown_moulded=True) == 3.0

    # Tier 3: 100 < Area <= 500 cm2 -> 2.0 mm (blown: 4.0 mm)
    assert analyzer.compute_required_minimum_height(250.0, is_blown_moulded=False) == 2.0
    assert analyzer.compute_required_minimum_height(250.0, is_blown_moulded=True) == 4.0

    # Tier 4: Area > 500 cm2 -> 4.0 mm (blown: 6.0 mm)
    assert analyzer.compute_required_minimum_height(800.0, is_blown_moulded=False) == 4.0
    assert analyzer.compute_required_minimum_height(800.0, is_blown_moulded=True) == 6.0


def test_font_geometry_audit_compliant_numerals():
    """Verify compliant font dimensions on standard commodity packaging."""
    analyzer = FontGeometryAnalyzer(default_scale_factor_mm_per_px=0.10)

    # Token "500g" with height 30px (3.0mm), width 90px (30px/char = 3.0mm/char -> aspect ratio 1.0)
    # PDP area = 200 cm2 (requires min 2.0mm)
    token_boxes = [("500g", [100.0, 100.0, 190.0, 130.0])]

    result = analyzer.audit_declaration_numerals(
        token_boxes=token_boxes,
        pdp_area_cm2=200.0,
        scale_factor_mm_per_px=0.10,
        is_blown_moulded=False,
    )

    assert result.is_compliant is True
    assert result.is_height_compliant is True
    assert result.is_aspect_ratio_compliant is True
    assert result.is_stroke_width_compliant is True
    assert len(result.statutory_defects) == 0


def test_font_geometry_audit_undersized_height_violation():
    """Verify detection of undersized numerals violating Table I."""
    analyzer = FontGeometryAnalyzer(default_scale_factor_mm_per_px=0.10)

    # Token height 15px (1.5mm) on a package with PDP area 300 cm2 (requires min 2.0mm)
    token_boxes = [("Net Wt 500g", [100.0, 100.0, 300.0, 115.0])]

    result = analyzer.audit_declaration_numerals(
        token_boxes=token_boxes,
        pdp_area_cm2=300.0,
        scale_factor_mm_per_px=0.10,
    )

    assert result.is_compliant is False
    assert result.is_height_compliant is False
    assert any("less than statutory minimum" in d.lower() for d in result.statutory_defects)
