"""
FSSAI Front-of-Pack Nutrition Labelling (FOPNL) & Indian Nutrition Rating (INR) Engine
=====================================================================================
Evaluates nutritional declarations and computes statutory Indian Nutrition Rating (INR)
star scores and high-sugar / high-fat / high-sodium warning thresholds under the
Food Safety and Standards (Labelling and Display) Regulations, 2020.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from reportlab.graphics.shapes import Circle, Drawing, Group, Line, Rect, String
from reportlab.lib import colors


@dataclass(frozen=True)
class NutrientValue:
    """Represents a declared nutrient value per 100g or 100ml."""

    nutrient_name: str
    declared_value: float
    unit: str
    statutory_threshold: float
    is_high_threshold_exceeded: bool
    threshold_percent_of_daily_intake: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nutrient_name": self.nutrient_name,
            "declared_value": self.declared_value,
            "unit": self.unit,
            "statutory_threshold": self.statutory_threshold,
            "is_high_threshold_exceeded": self.is_high_threshold_exceeded,
            "threshold_percent_of_daily_intake": round(
                self.threshold_percent_of_daily_intake, 2
            ),
        }


@dataclass(frozen=True)
class FOPNLEvaluationResult:
    """Comprehensive FOPNL statutory assessment outcome."""

    is_compliant: bool
    product_category: str  # 'SOLID_FOOD', 'LIQUID_BEVERAGE', 'DAIRY'
    inr_star_rating: float  # 0.5 to 5.0 stars
    baseline_negative_points: int
    positive_nutrient_points: int
    final_inr_score: int
    requires_warning_badge: bool
    warning_nutrients: List[str]
    nutrients_breakdown: List[NutrientValue] = field(default_factory=list)
    statutory_citation: str = "FSSAI (Labelling and Display) Regulations 2020, Schedule II"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_compliant": self.is_compliant,
            "product_category": self.product_category,
            "inr_star_rating": self.inr_star_rating,
            "requires_warning_badge": self.requires_warning_badge,
            "warning_nutrients": self.warning_nutrients,
            "baseline_negative_points": self.baseline_negative_points,
            "positive_nutrient_points": self.positive_nutrient_points,
            "final_inr_score": self.final_inr_score,
            "nutrients": [n.to_dict() for n in self.nutrients_breakdown],
            "statutory_citation": self.statutory_citation,
        }


class FOPNLMatrixCalculator:
    """
    Computes FSSAI thresholds and generates ReportLab FOPNL warning badges.
    """

    # Solid Food Cutoff Thresholds per 100g
    SOLID_THRESHOLDS = {
        "energy_kcal": 250.0,
        "total_sugar_g": 6.0,
        "added_sugar_g": 4.0,
        "saturated_fat_g": 2.2,
        "trans_fat_g": 0.2,
        "sodium_mg": 250.0,
    }

    # Liquid Beverage Cutoff Thresholds per 100ml
    LIQUID_THRESHOLDS = {
        "energy_kcal": 70.0,
        "total_sugar_g": 4.0,
        "added_sugar_g": 2.5,
        "saturated_fat_g": 1.0,
        "trans_fat_g": 0.1,
        "sodium_mg": 100.0,
    }

    def evaluate(
        self,
        nutrients: Dict[str, float],
        is_liquid: bool = False,
        fruit_veg_nut_percent: float = 0.0,
        protein_g: float = 0.0,
        fiber_g: float = 0.0,
    ) -> FOPNLEvaluationResult:
        """
        Evaluate nutrients per 100g/ml against FSSAI INR algorithm.

        Args:
            nutrients: Dictionary of nutrient values (energy_kcal, total_sugar_g, saturated_fat_g, sodium_mg).
            is_liquid: Whether commodity is liquid beverage.
            fruit_veg_nut_percent: Content percentage of fruits, vegetables, nuts, legumes (FVNL).
            protein_g: Protein in grams per 100g/ml.
            fiber_g: Dietary fiber in grams per 100g/ml.
        """
        thresholds = self.LIQUID_THRESHOLDS if is_liquid else self.SOLID_THRESHOLDS
        category = "LIQUID_BEVERAGE" if is_liquid else "SOLID_FOOD"

        nutrient_records: List[NutrientValue] = []
        warning_nutrients: List[str] = []

        # 1. Evaluate negative baseline points
        neg_points = 0

        # Energy
        energy = nutrients.get("energy_kcal", 0.0)
        e_thresh = thresholds["energy_kcal"]
        e_exceeded = energy > e_thresh
        if e_exceeded:
            warning_nutrients.append("HIGH ENERGY (CALORIES)")
        neg_points += min(10, int(energy / (80.0 if is_liquid else 150.0)))
        nutrient_records.append(
            NutrientValue(
                nutrient_name="Energy",
                declared_value=energy,
                unit="kcal",
                statutory_threshold=e_thresh,
                is_high_threshold_exceeded=e_exceeded,
                threshold_percent_of_daily_intake=(energy / 2000.0) * 100.0,
            )
        )

        # Saturated Fat
        sat_fat = nutrients.get("saturated_fat_g", 0.0)
        sf_thresh = thresholds["saturated_fat_g"]
        sf_exceeded = sat_fat > sf_thresh
        if sf_exceeded:
            warning_nutrients.append("HIGH SATURATED FAT")
        neg_points += min(10, int(sat_fat / 1.5))
        nutrient_records.append(
            NutrientValue(
                nutrient_name="Saturated Fat",
                declared_value=sat_fat,
                unit="g",
                statutory_threshold=sf_thresh,
                is_high_threshold_exceeded=sf_exceeded,
                threshold_percent_of_daily_intake=(sat_fat / 22.0) * 100.0,
            )
        )

        # Sugar
        sugar = nutrients.get("total_sugar_g", nutrients.get("added_sugar_g", 0.0))
        sugar_thresh = thresholds["total_sugar_g"]
        sugar_exceeded = sugar > sugar_thresh
        if sugar_exceeded:
            warning_nutrients.append("HIGH SUGAR")
        neg_points += min(10, int(sugar / 4.5))
        nutrient_records.append(
            NutrientValue(
                nutrient_name="Total Sugars",
                declared_value=sugar,
                unit="g",
                statutory_threshold=sugar_thresh,
                is_high_threshold_exceeded=sugar_exceeded,
                threshold_percent_of_daily_intake=(sugar / 50.0) * 100.0,
            )
        )

        # Sodium
        sodium = nutrients.get("sodium_mg", 0.0)
        sod_thresh = thresholds["sodium_mg"]
        sod_exceeded = sodium > sod_thresh
        if sod_exceeded:
            warning_nutrients.append("HIGH SODIUM (SALT)")
        neg_points += min(10, int(sodium / 90.0))
        nutrient_records.append(
            NutrientValue(
                nutrient_name="Sodium",
                declared_value=sodium,
                unit="mg",
                statutory_threshold=sod_thresh,
                is_high_threshold_exceeded=sod_exceeded,
                threshold_percent_of_daily_intake=(sodium / 2000.0) * 100.0,
            )
        )

        # 2. Positive nutrient points
        pos_points = 0
        pos_points += min(5, int(fruit_veg_nut_percent / 20.0))
        pos_points += min(5, int(protein_g / 1.6))
        pos_points += min(5, int(fiber_g / 0.9))

        # 3. Final INR Score = Negative Points - Positive Points
        final_score = neg_points - pos_points

        # Calculate Stars (0.5 to 5.0)
        if final_score <= -1:
            stars = 5.0
        elif final_score <= 2:
            stars = 4.5
        elif final_score <= 5:
            stars = 4.0
        elif final_score <= 9:
            stars = 3.5
        elif final_score <= 13:
            stars = 3.0
        elif final_score <= 17:
            stars = 2.5
        elif final_score <= 21:
            stars = 2.0
        elif final_score <= 25:
            stars = 1.5
        elif final_score <= 29:
            stars = 1.0
        else:
            stars = 0.5

        has_warnings = len(warning_nutrients) > 0

        return FOPNLEvaluationResult(
            is_compliant=True,
            product_category=category,
            inr_star_rating=stars,
            baseline_negative_points=neg_points,
            positive_nutrient_points=pos_points,
            final_inr_score=final_score,
            requires_warning_badge=has_warnings,
            warning_nutrients=warning_nutrients,
            nutrients_breakdown=nutrient_records,
        )

    def generate_fopnl_drawing(
        self, result: FOPNLEvaluationResult, width: float = 160.0, height: float = 60.0
    ) -> Drawing:
        """
        Generate a ReportLab Drawing containing the statutory INR star rating badge.
        """
        d = Drawing(width, height)

        # Background card
        card_color = colors.HexColor("#FFF8E7") if result.requires_warning_badge else colors.HexColor("#F0FFF4")
        border_color = colors.HexColor("#D97706") if result.requires_warning_badge else colors.HexColor("#16A34A")

        d.add(Rect(0, 0, width, height, fillColor=card_color, strokeColor=border_color, strokeWidth=1, rx=4, ry=4))

        # Title
        d.add(
            String(
                8,
                height - 14,
                f"FSSAI INR RATING: {result.inr_star_rating:.1f} STARS",
                fontName="Helvetica-Bold",
                fontSize=8.5,
                fillColor=colors.HexColor("#0B2545"),
            )
        )

        # Draw Star indicators
        star_x = 8
        full_stars = int(result.inr_star_rating)
        has_half = (result.inr_star_rating - full_stars) >= 0.5

        for i in range(5):
            cx = star_x + (i * 18) + 6
            cy = height - 28
            if i < full_stars:
                fill_c = colors.HexColor("#F59E0B")  # Gold
            elif i == full_stars and has_half:
                fill_c = colors.HexColor("#FBBF24")  # Half gold
            else:
                fill_c = colors.HexColor("#D1D5DB")  # Gray

            d.add(Circle(cx, cy, 6, fillColor=fill_c, strokeColor=colors.HexColor("#9CA3AF"), strokeWidth=0.5))

        # Warnings note
        if result.warning_nutrients:
            warn_str = " | ".join(result.warning_nutrients[:2])
            d.add(
                String(
                    8,
                    8,
                    f"Warning: {warn_str}",
                    fontName="Helvetica-Bold",
                    fontSize=6.5,
                    fillColor=colors.HexColor("#DC2626"),
                )
            )
        else:
            d.add(
                String(
                    8,
                    8,
                    "Nutritional Profile within FSSAI Thresholds",
                    fontName="Helvetica",
                    fontSize=7,
                    fillColor=colors.HexColor("#15803D"),
                )
            )

        return d
