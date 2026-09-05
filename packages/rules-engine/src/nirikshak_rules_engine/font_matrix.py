"""
Nirikshak Rules Engine: Rule 7 Tables I & II Numeral/Letter Height Matrix.
Statutory Authority: Rule 7 of Legal Metrology (Packaged Commodities) Rules, 2011
(as amended by G.S.R. 629(E) and G.S.R. 1373(E)).

Statutory Matrices:
Table-I: Minimum Height of Numerals for Net Quantity Declared by Weight or Volume:
- PDP Area (A) <= 50 cm²:           Normal = 1.0 mm, Blown/Formed = 1.5 mm
- 50 cm² < A <= 100 cm²:           Normal = 1.5 mm, Blown/Formed = 3.0 mm
- 100 cm² < A <= 500 cm²:          Normal = 2.5 mm, Blown/Formed = 4.0 mm
- 500 cm² < A <= 2500 cm²:         Normal = 4.0 mm, Blown/Formed = 6.0 mm
- A > 2500 cm²:                    Normal = 6.0 mm, Blown/Formed = 6.0 mm

Table-II: Minimum Height of Numerals for Net Quantity Declared by Length, Area, or Number:
- PDP Area (A) <= 100 cm²:          Normal = 1.0 mm, Blown/Formed = 2.0 mm
- 100 cm² < A <= 500 cm²:          Normal = 2.0 mm, Blown/Formed = 4.0 mm
- 500 cm² < A <= 2500 cm²:         Normal = 4.0 mm, Blown/Formed = 6.0 mm
- A > 2500 cm²:                    Normal = 6.0 mm, Blown/Formed = 6.0 mm

Benefit-of-Doubt Buffer:
- 0.10 mm buffer applied in favor of the manufacturer before asserting non-compliance.
"""

from typing import Optional, Tuple, List
from .schemas import (
    CanonicalDeclaration,
    MetricScaleResult,
    RuleEvaluationRecord,
    UnitType,
)


class FontMatrixValidator:
    """
    Evaluates Rule 7 font and numeral height compliance across Principal Display Panel (PDP) area tiers.
    Applies statutory benefit-of-doubt buffer of 0.10 mm.
    """

    BENEFIT_OF_DOUBT_BUFFER_MM: float = 0.10
    UNCERTAINTY_BAND_MM: float = 0.25

    @classmethod
    def get_table_and_threshold(
        cls,
        pdp_area_sqcm: float,
        unit_type: Optional[UnitType],
        is_blown_or_formed: bool = False,
    ) -> Tuple[float, str, str]:
        """
        Determines the minimum statutory height (in mm), table name, and citation
        for the specified PDP area and unit type.

        Returns:
            (min_height_mm, table_name, statutory_citation)
        """
        # Determine whether Table-I or Table-II governs
        # Table-I: Net Quantity by Weight or Volume
        is_table_1 = unit_type in [
            UnitType.GRAM,
            UnitType.KILOGRAM,
            UnitType.MILLILITER,
            UnitType.LITER,
            None,  # Default to Table-I if unit is unknown
        ]

        if is_table_1:
            table_name = "Rule 7 Table-I (Weight/Volume)"
            citation = "Rule 7 Table-I of Legal Metrology (Packaged Commodities) Rules, 2011"
            if pdp_area_sqcm <= 50.0:
                h = 1.5 if is_blown_or_formed else 1.0
            elif pdp_area_sqcm <= 100.0:
                h = 3.0 if is_blown_or_formed else 1.5
            elif pdp_area_sqcm <= 500.0:
                h = 4.0 if is_blown_or_formed else 2.5
            elif pdp_area_sqcm <= 2500.0:
                h = 6.0 if is_blown_or_formed else 4.0
            else:
                h = 6.0
        else:
            # Table-II: Net Quantity by Length, Area, or Number (Count)
            table_name = "Rule 7 Table-II (Length/Area/Count)"
            citation = "Rule 7 Table-II of Legal Metrology (Packaged Commodities) Rules, 2011"
            if pdp_area_sqcm <= 100.0:
                h = 2.0 if is_blown_or_formed else 1.0
            elif pdp_area_sqcm <= 500.0:
                h = 4.0 if is_blown_or_formed else 2.0
            elif pdp_area_sqcm <= 2500.0:
                h = 6.0 if is_blown_or_formed else 4.0
            else:
                h = 6.0

        return h, table_name, citation

    def evaluate(
        self,
        decl: CanonicalDeclaration,
        scale: Optional[MetricScaleResult] = None,
        measured_height_mm: Optional[float] = None,
        is_blown_or_formed: bool = False,
    ) -> RuleEvaluationRecord:
        """
        Deterministically evaluates Rule 7 font height compliance.
        Applies a 0.10 mm benefit-of-doubt buffer before asserting non-compliance.
        """
        rule_id = "LMPC-R07-FONT-001"
        rule_title = "Minimum Height of Numerals and Letters"
        stat_ref = "Rule 7"
        citation = "Rule 7 of Legal Metrology (Packaged Commodities) Rules, 2011"

        # 1. Check calibration availability
        if scale is None or not scale.is_calibrated or scale.scale_factor_mm_per_px is None:
            return RuleEvaluationRecord(
                rule_id=rule_id,
                rule_title=rule_title,
                statutory_reference=stat_ref,
                status="REVIEW",
                is_compliant=True,  # Does not trigger hard violation on uncalibrated image
                observed_value="Uncalibrated",
                required_value="Metric calibration reference (Coin/Card)",
                statutory_citation=citation,
                notes=(
                    "Optical metric scale is uncalibrated. Cannot compute millimeter numeral height "
                    "without reference anchor. Manual inspection or physical gauge required."
                ),
            )

        # 2. Check PDP area computation
        if scale.pdp_area_sqcm is None or scale.pdp_area_sqcm <= 0:
            return RuleEvaluationRecord(
                rule_id=rule_id,
                rule_title=rule_title,
                statutory_reference=stat_ref,
                status="REVIEW",
                is_compliant=True,
                observed_value="PDP Area Unknown",
                required_value="Principal Display Panel area (cm²)",
                statutory_citation=citation,
                notes="Principal Display Panel (PDP area) could not be determined from optical geometry.",
            )


        pdp_area = scale.pdp_area_sqcm
        min_required_h, table_name, stat_citation = self.get_table_and_threshold(
            pdp_area, decl.net_quantity_unit, is_blown_or_formed=is_blown_or_formed
        )

        # 3. Check measured numeral height
        if measured_height_mm is None or measured_height_mm <= 0:
            return RuleEvaluationRecord(
                rule_id=rule_id,
                rule_title=rule_title,
                statutory_reference=stat_ref,
                status="REVIEW",
                is_compliant=True,
                observed_value="Unmeasured",
                required_value=f"{min_required_h:.1f} mm (PDP: {pdp_area:.1f} cm²)",
                statutory_citation=stat_citation,
                notes=f"Principal Display Panel area is {pdp_area:.1f} cm², requiring minimum height of {min_required_h:.1f} mm under {table_name}. Height unmeasured.",
            )

        # 4. Compare with Benefit-of-Doubt Buffer (0.10 mm)
        effective_height = measured_height_mm + self.BENEFIT_OF_DOUBT_BUFFER_MM
        deficit = round(min_required_h - measured_height_mm, 2)

        if measured_height_mm >= min_required_h:
            # Fully compliant
            return RuleEvaluationRecord(
                rule_id=rule_id,
                rule_title=rule_title,
                statutory_reference=stat_ref,
                status="PASS",
                is_compliant=True,
                observed_value=f"{measured_height_mm:.2f} mm",
                required_value=f">= {min_required_h:.1f} mm (PDP: {pdp_area:.1f} cm²)",
                statutory_citation=stat_citation,
                notes=f"Measured numeral height {measured_height_mm:.2f} mm strictly satisfies {table_name} threshold of {min_required_h:.1f} mm.",
                benefit_of_doubt_applied=False,
            )

        elif effective_height >= min_required_h:
            # Compliant via 0.10 mm benefit-of-doubt buffer
            return RuleEvaluationRecord(
                rule_id=rule_id,
                rule_title=rule_title,
                statutory_reference=stat_ref,
                status="PASS",
                is_compliant=True,
                observed_value=f"{measured_height_mm:.2f} mm (+0.10mm buffer)",
                required_value=f">= {min_required_h:.1f} mm (PDP: {pdp_area:.1f} cm²)",
                statutory_citation=stat_citation,
                notes=(
                    f"Measured numeral height {measured_height_mm:.2f} mm is marginally under {min_required_h:.1f} mm, "
                    f"but accepted as compliant under the statutory 0.10 mm benefit-of-doubt tolerance buffer ({table_name})."
                ),
                benefit_of_doubt_applied=True,
            )

        elif measured_height_mm >= (min_required_h - self.UNCERTAINTY_BAND_MM):
            # Borderline within measurement uncertainty review band -> REVIEW / DEVIATION_DETECTED
            return RuleEvaluationRecord(
                rule_id=rule_id,
                rule_title=rule_title,
                statutory_reference=stat_ref,
                status="REVIEW",
                is_compliant=False,
                observed_value=f"{measured_height_mm:.2f} mm",
                required_value=f">= {min_required_h:.1f} mm (PDP: {pdp_area:.1f} cm²)",
                deficit_mm=deficit,
                statutory_citation=stat_citation,
                notes=(
                    f"Borderline numeral height {measured_height_mm:.2f} mm shows a deficit of {deficit:.2f} mm "
                    f"against {min_required_h:.1f} mm threshold ({table_name}). Within optical uncertainty band; physical gauge verification recommended."
                ),
                benefit_of_doubt_applied=False,
            )

        else:
            # Concrete non-compliance
            return RuleEvaluationRecord(
                rule_id=rule_id,
                rule_title=rule_title,
                statutory_reference=stat_ref,
                status="FAIL",
                is_compliant=False,
                observed_value=f"{measured_height_mm:.2f} mm",
                required_value=f">= {min_required_h:.1f} mm (PDP: {pdp_area:.1f} cm²)",
                deficit_mm=deficit,
                statutory_citation=stat_citation,
                notes=(
                    f"Statutory font height deficit: Measured {measured_height_mm:.2f} mm fails {table_name} "
                    f"minimum threshold of {min_required_h:.1f} mm by {deficit:.2f} mm (even after applying 0.10 mm benefit-of-doubt buffer)."
                ),
                benefit_of_doubt_applied=False,
            )
