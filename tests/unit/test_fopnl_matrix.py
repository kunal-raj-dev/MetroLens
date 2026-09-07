"""
Unit Tests for FSSAI FOPNL & Indian Nutrition Rating (INR) Engine
=================================================================
Verifies nutritional threshold evaluation, star ratings (0.5 to 5.0),
warning badge triggers, and ReportLab vector drawing generation.
"""

import pytest
from reportlab.graphics.shapes import Drawing

from packages.reporting.src.nirikshak_reporting.fopnl_matrix import (
    FOPNLMatrixCalculator,
    FOPNLEvaluationResult,
)


def test_fopnl_high_sugar_high_fat_evaluation():
    """Verify low star rating and warning badge trigger on unhealthy solid food."""
    calc = FOPNLMatrixCalculator()

    unhealthy_nutrients = {
        "energy_kcal": 450.0,    # Above 250 kcal cutoff
        "total_sugar_g": 38.0,   # Far above 6.0g cutoff
        "saturated_fat_g": 14.0, # Far above 2.2g cutoff
        "sodium_mg": 400.0,      # Above 250mg cutoff
    }

    result = calc.evaluate(unhealthy_nutrients, is_liquid=False)

    assert isinstance(result, FOPNLEvaluationResult)
    assert result.inr_star_rating <= 1.5
    assert result.requires_warning_badge is True
    assert "HIGH SUGAR" in result.warning_nutrients
    assert "HIGH SATURATED FAT" in result.warning_nutrients
    assert "HIGH ENERGY (CALORIES)" in result.warning_nutrients


def test_fopnl_healthy_whole_grain_evaluation():
    """Verify high star rating on nutritious food with high fiber/protein and low sugar."""
    calc = FOPNLMatrixCalculator()

    healthy_nutrients = {
        "energy_kcal": 180.0,
        "total_sugar_g": 1.5,
        "saturated_fat_g": 0.5,
        "sodium_mg": 80.0,
    }

    result = calc.evaluate(
        healthy_nutrients,
        is_liquid=False,
        fruit_veg_nut_percent=50.0,
        protein_g=12.0,
        fiber_g=8.0,
    )

    assert result.inr_star_rating >= 4.0
    assert result.requires_warning_badge is False
    assert len(result.warning_nutrients) == 0


def test_fopnl_reportlab_drawing_generation():
    """Verify generation of ReportLab Drawing vector badge for PDF embedding."""
    calc = FOPNLMatrixCalculator()

    sample_nutrients = {
        "energy_kcal": 200.0,
        "total_sugar_g": 2.0,
        "saturated_fat_g": 1.0,
        "sodium_mg": 120.0,
    }

    res = calc.evaluate(sample_nutrients)
    drawing = calc.generate_fopnl_drawing(res, width=150.0, height=50.0)

    assert isinstance(drawing, Drawing)
    assert drawing.width == 150.0
    assert drawing.height == 50.0
    assert len(drawing.contents) >= 5
