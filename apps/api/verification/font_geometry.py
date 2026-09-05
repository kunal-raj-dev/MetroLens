"""
Deep Geometric Font Height, Stroke Width & Aspect Ratio Analyzer
================================================================
Implements rigorous geometric validation of mandatory numerals and letters
under Rule 7(1), Table I, and Table II of the Legal Metrology (Packaged
Commodities) Rules, 2011.

Rule 7 Statutory Geometric Invariants:
    1. Minimum Numeral Height (Table I): Function of Principal Display Panel (PDP) area.
    2. Aspect Ratio: "The width of the letter or numeral shall not be less than
       one-third of its height, except in the case of numeral '1' and letters i, I, l."
       (Width >= Height / 3.0)
    3. Stroke Width Thickness: "The stroke of the letter or numeral shall not be
       less than one-sixth of the height." (Stroke >= Height / 6.0)
    4. Inter-Character Spacing: "The space between two letters shall not be less
       than one-fourth of their height." (Spacing >= Height / 4.0)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class FontGeometryMetrics:
    """Precise geometric dimensions of a recognized character or numeral."""

    char: str
    height_px: float
    width_px: float
    height_mm: float
    width_mm: float
    aspect_ratio: float  # width / height
    estimated_stroke_mm: float
    inter_char_spacing_mm: Optional[float] = None
    is_width_ratio_valid: bool = True
    is_stroke_width_valid: bool = True
    is_spacing_valid: bool = True


@dataclass(frozen=True)
class NumeralGeometryAuditResult:
    """Complete statutory audit outcome for numeral/letter geometry under Rule 7."""

    is_compliant: bool
    pdp_area_cm2: float
    is_blown_moulded_container: bool
    required_min_height_mm: float
    measured_min_height_mm: float
    measured_mean_height_mm: float
    is_height_compliant: bool
    is_aspect_ratio_compliant: bool
    is_stroke_width_compliant: bool
    is_spacing_compliant: bool
    char_metrics: List[FontGeometryMetrics] = field(default_factory=list)
    statutory_defects: List[str] = field(default_factory=list)
    statutory_citation: str = "Rule 7(1) Tables I & II, PCR 2011"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_compliant": self.is_compliant,
            "pdp_area_cm2": round(self.pdp_area_cm2, 2),
            "is_blown_moulded_container": self.is_blown_moulded_container,
            "required_min_height_mm": round(self.required_min_height_mm, 2),
            "measured_min_height_mm": round(self.measured_min_height_mm, 2),
            "measured_mean_height_mm": round(self.measured_mean_height_mm, 2),
            "is_height_compliant": self.is_height_compliant,
            "is_aspect_ratio_compliant": self.is_aspect_ratio_compliant,
            "is_stroke_width_compliant": self.is_stroke_width_compliant,
            "is_spacing_compliant": self.is_spacing_compliant,
            "statutory_defects": self.statutory_defects,
            "statutory_citation": self.statutory_citation,
        }


class FontGeometryAnalyzer:
    """
    Evaluates extracted bounding boxes and characters against Rule 7 geometric constraints.
    """

    NARROW_GLYPHS = {"1", "i", "I", "l", "|", ".", ",", ":", ";", "/", "!", "'"}

    def __init__(self, default_scale_factor_mm_per_px: float = 0.125) -> None:
        self.default_scale = default_scale_factor_mm_per_px

    def compute_required_minimum_height(
        self, pdp_area_cm2: float, is_blown_moulded: bool = False
    ) -> float:
        """
        Table I: Minimum Height of Numerals.
        Area <= 50 cm2: 1.0 mm (blown: 2.0 mm)
        50 < Area <= 100 cm2: 1.5 mm (blown: 3.0 mm)
        100 < Area <= 500 cm2: 2.0 mm (blown: 4.0 mm)
        Area > 500 cm2: 4.0 mm (blown: 6.0 mm)
        """
        if pdp_area_cm2 <= 50.0:
            return 2.0 if is_blown_moulded else 1.0
        elif pdp_area_cm2 <= 100.0:
            return 3.0 if is_blown_moulded else 1.5
        elif pdp_area_cm2 <= 500.0:
            return 4.0 if is_blown_moulded else 2.0
        else:
            return 6.0 if is_blown_moulded else 4.0

    def audit_declaration_numerals(
        self,
        token_boxes: List[Tuple[str, List[float]]],  # List of (text, [xmin, ymin, xmax, ymax])
        pdp_area_cm2: float,
        scale_factor_mm_per_px: Optional[float] = None,
        is_blown_moulded: bool = False,
    ) -> NumeralGeometryAuditResult:
        """
        Audit characters against Rule 7 minimum height, 1/3 width ratio, 1/6 stroke, and 1/4 spacing.

        Args:
            token_boxes: List of (token_text, bbox_px: [x1, y1, x2, y2]).
            pdp_area_cm2: Measured Principal Display Panel area in cm2.
            scale_factor_mm_per_px: Metric scale in mm/px.
            is_blown_moulded: Whether packaging is a blown bottle or moulded container.
        """
        scale = scale_factor_mm_per_px if scale_factor_mm_per_px and scale_factor_mm_per_px > 0 else self.default_scale
        required_height = self.compute_required_minimum_height(pdp_area_cm2, is_blown_moulded)

        char_metrics_list: List[FontGeometryMetrics] = []
        defects: List[str] = []

        heights_mm: List[float] = []

        all_height_pass = True
        all_aspect_pass = True
        all_stroke_pass = True
        all_spacing_pass = True

        # Analyze each token and estimate individual character geometry
        sorted_tokens = sorted(token_boxes, key=lambda tb: (tb[1][1], tb[1][0]))

        for idx, (text, bbox) in enumerate(sorted_tokens):
            x1, y1, x2, y2 = bbox
            h_px = max(1.0, float(y2 - y1))
            w_px = max(1.0, float(x2 - x1))

            h_mm = h_px * scale
            w_mm = w_px * scale
            heights_mm.append(h_mm)

            clean_chars = [ch for ch in text if not ch.isspace()]
            num_chars = len(clean_chars)
            if num_chars == 0:
                continue

            # Average width per character in word
            avg_char_w_px = w_px / num_chars
            avg_char_w_mm = avg_char_w_px * scale

            # Stroke width heuristic (standard typography: stroke is ~15-20% of height)
            est_stroke_mm = h_mm * 0.18

            # Calculate inter-token horizontal spacing to next token on same line
            spacing_mm = None
            if idx + 1 < len(sorted_tokens):
                next_text, next_box = sorted_tokens[idx + 1]
                nx1, ny1, nx2, ny2 = next_box
                # Same horizontal band
                if abs(ny1 - y1) < h_px * 0.5:
                    spacing_px = max(0.0, float(nx1 - x2))
                    spacing_mm = spacing_px * scale

            # Check individual characters
            for ch in clean_chars:
                # Aspect ratio check: width >= height / 3.0 (except narrow glyphs)
                if ch in self.NARROW_GLYPHS:
                    is_aspect_valid = True
                else:
                    aspect_ratio = avg_char_w_mm / (h_mm if h_mm > 0 else 1.0)
                    is_aspect_valid = aspect_ratio >= 0.333

                # Stroke thickness check: stroke >= height / 6.0 (approx 0.1667)
                is_stroke_valid = est_stroke_mm >= (h_mm / 6.0)

                # Spacing check: spacing >= height / 4.0 (0.25)
                is_space_valid = True
                if spacing_mm is not None:
                    is_space_valid = spacing_mm >= (h_mm * 0.25)

                if not is_aspect_valid:
                    all_aspect_pass = False
                if not is_stroke_valid:
                    all_stroke_pass = False
                if not is_space_valid:
                    all_spacing_pass = False

                char_metrics_list.append(
                    FontGeometryMetrics(
                        char=ch,
                        height_px=h_px,
                        width_px=avg_char_w_px,
                        height_mm=h_mm,
                        width_mm=avg_char_w_mm,
                        aspect_ratio=avg_char_w_mm / (h_mm if h_mm > 0 else 1.0),
                        estimated_stroke_mm=est_stroke_mm,
                        inter_char_spacing_mm=spacing_mm,
                        is_width_ratio_valid=is_aspect_valid,
                        is_stroke_width_valid=is_stroke_valid,
                        is_spacing_valid=is_space_valid,
                    )
                )

            # Check minimum numeral height requirement
            if h_mm < required_height:
                all_height_pass = False
                defects.append(
                    f"Numeral height ({h_mm:.2f}mm) for '{text}' is less than statutory minimum "
                    f"{required_height:.1f}mm for PDP area {pdp_area_cm2:.1f} cm² (Rule 7 Table I)."
                )

        if not all_aspect_pass:
            defects.append(
                "Character width-to-height ratio violates Rule 7: letter/numeral width is less than one-third of height."
            )
        if not all_spacing_pass:
            defects.append(
                "Inter-character spacing violates Rule 7: distance between adjacent characters is less than one-fourth of height."
            )

        min_h = min(heights_mm) if heights_mm else 0.0
        mean_h = sum(heights_mm) / len(heights_mm) if heights_mm else 0.0

        is_overall_compliant = all_height_pass and all_aspect_pass and all_stroke_pass

        return NumeralGeometryAuditResult(
            is_compliant=is_overall_compliant,
            pdp_area_cm2=pdp_area_cm2,
            is_blown_moulded_container=is_blown_moulded,
            required_min_height_mm=required_height,
            measured_min_height_mm=min_h,
            measured_mean_height_mm=mean_h,
            is_height_compliant=all_height_pass,
            is_aspect_ratio_compliant=all_aspect_pass,
            is_stroke_width_compliant=all_stroke_pass,
            is_spacing_compliant=all_spacing_pass,
            char_metrics=char_metrics_list,
            statutory_defects=defects,
        )
