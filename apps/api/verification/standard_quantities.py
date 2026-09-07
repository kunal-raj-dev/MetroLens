"""
Second Schedule Standard Package Quantities & Maximum Permissible Error (MPE) Engine
=====================================================================================
Validates pre-packaged commodity quantities against Rule 5, the Second Schedule,
and the First Schedule (Maximum Permissible Errors) of the Legal Metrology (Packaged
Commodities) Rules, 2011.

Rule 5 Statutory Principle:
    "No person shall pre-pack or cause or permit to be pre-packed any commodity
    for sale, distribution or delivery except in such standard quantities as are
    specified in the Second Schedule."
"""

from __future__ import annotations

import enum
import math
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class MeasurementDimension(str, enum.Enum):
    WEIGHT = "WEIGHT"      # grams, kilograms
    VOLUME = "VOLUME"      # milliliters, liters
    LENGTH = "LENGTH"      # meters, centimeters
    AREA = "AREA"          # square meters
    NUMBER = "NUMBER"      # items, pieces (N or U)


@dataclass(frozen=True)
class StandardQuantityRule:
    """Represents a discrete standard size or a continuous step size."""

    is_discrete: bool
    discrete_values: Tuple[float, ...] = field(default_factory=tuple)
    step_multiple: Optional[float] = None
    min_step_range: Optional[float] = None
    max_step_range: Optional[float] = None
    unit_symbol: str = "g"

    def is_valid_quantity(self, qty: float) -> bool:
        """Check whether numeric quantity matches discrete list or permissible step multiple."""
        # 1. Check discrete exact values
        for val in self.discrete_values:
            if math.isclose(qty, val, rel_tol=1e-5, abs_tol=1e-5):
                return True

        # 2. Check step multiple within range
        if (
            self.step_multiple is not None
            and self.min_step_range is not None
            and self.max_step_range is not None
        ):
            if self.min_step_range <= qty <= self.max_step_range:
                # Check divisibility by step multiple
                remainder = math.fmod(qty - self.min_step_range, self.step_multiple)
                if math.isclose(remainder, 0.0, abs_tol=1e-5) or math.isclose(
                    remainder, self.step_multiple, abs_tol=1e-5
                ):
                    return True

        return False


@dataclass(frozen=True)
class CommodityStandardSpec:
    """Commodity schedule specification."""

    commodity_key: str
    official_name: str
    dimension: MeasurementDimension
    rules: Tuple[StandardQuantityRule, ...]
    schedule_reference: str = "Second Schedule, PCR 2011"
    exemptions_allowed: bool = True


@dataclass(frozen=True)
class StandardQuantityResult:
    """Outcome of statutory quantity evaluation."""

    is_compliant: bool
    commodity_key: str
    declared_quantity_raw: str
    normalized_value: float
    normalized_unit: str
    permissible_sizes_summary: str
    mpe_tolerance_value: float
    mpe_tolerance_percent: float
    statutory_citation: str
    defect_reason: Optional[str] = None
    is_exempt_under_rule_26: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_compliant": self.is_compliant,
            "commodity_key": self.commodity_key,
            "declared_quantity_raw": self.declared_quantity_raw,
            "normalized_value": self.normalized_value,
            "normalized_unit": self.normalized_unit,
            "permissible_sizes_summary": self.permissible_sizes_summary,
            "mpe_tolerance_value": round(self.mpe_tolerance_value, 4),
            "mpe_tolerance_percent": round(self.mpe_tolerance_percent, 2),
            "statutory_citation": self.statutory_citation,
            "defect_reason": self.defect_reason,
            "is_exempt_under_rule_26": self.is_exempt_under_rule_26,
        }


class StandardQuantitiesValidator:
    """
    Authoritative validator for standard package sizes and First Schedule MPE tolerances.
    """

    def __init__(self) -> None:
        self._specs: Dict[str, CommodityStandardSpec] = {}
        self._initialize_second_schedule_specs()

    def validate(
        self,
        commodity_key: str,
        quantity_value: float,
        quantity_unit: str,
        is_institutional_consumer: bool = False,
    ) -> StandardQuantityResult:
        """
        Validate package quantity against statutory schedule.

        Args:
            commodity_key: Unique commodity key (e.g. 'biscuits', 'tea', 'edible_oil').
            quantity_value: Declared numerical quantity (e.g. 75.0).
            quantity_unit: Declared unit symbol (e.g. 'g', 'kg', 'ml', 'l').
            is_institutional_consumer: Whether package is for bulk institutional sale (Rule 26 exemption).
        """
        clean_key = commodity_key.lower().strip()
        spec = self._specs.get(clean_key)

        # Normalize unit and value to base SI (grams for weight, milliliters for volume)
        norm_val, norm_unit = self._normalize_to_base_unit(quantity_value, quantity_unit)

        # Rule 26 Exemptions:
        # 1. Institutional consumers (Rule 26(d))
        # 2. Small packages: weight <= 10g or volume <= 10ml (Rule 26(a))
        # 3. Bulk agricultural commodities exceeding 50kg (Rule 26(b))
        if is_institutional_consumer:
            return StandardQuantityResult(
                is_compliant=True,
                commodity_key=clean_key,
                declared_quantity_raw=f"{quantity_value} {quantity_unit}",
                normalized_value=norm_val,
                normalized_unit=norm_unit,
                permissible_sizes_summary="Exempt from standard package sizes under Rule 26(d)",
                mpe_tolerance_value=0.0,
                mpe_tolerance_percent=0.0,
                statutory_citation="Rule 26(d) Exemption (Institutional Consumer)",
                is_exempt_under_rule_26=True,
            )

        if norm_val <= 10.0 and norm_unit in ("g", "ml"):
            return StandardQuantityResult(
                is_compliant=True,
                commodity_key=clean_key,
                declared_quantity_raw=f"{quantity_value} {quantity_unit}",
                normalized_value=norm_val,
                normalized_unit=norm_unit,
                permissible_sizes_summary="Small package exempt under Rule 26(a) (<= 10g or <= 10ml)",
                mpe_tolerance_value=0.0,
                mpe_tolerance_percent=0.0,
                statutory_citation="Rule 26(a) Small Package Exemption",
                is_exempt_under_rule_26=True,
            )

        if norm_val > 50000.0 and norm_unit == "g":
            return StandardQuantityResult(
                is_compliant=True,
                commodity_key=clean_key,
                declared_quantity_raw=f"{quantity_value} {quantity_unit}",
                normalized_value=norm_val,
                normalized_unit=norm_unit,
                permissible_sizes_summary="Bulk package exempt under Rule 26(b) (> 50kg)",
                mpe_tolerance_value=0.0,
                mpe_tolerance_percent=0.0,
                statutory_citation="Rule 26(b) Bulk Package Exemption",
                is_exempt_under_rule_26=True,
            )

        # Calculate First Schedule Maximum Permissible Error (MPE)
        mpe_val, mpe_pct = self.calculate_maximum_permissible_error(norm_val, norm_unit)

        if not spec:
            # Commodity not regulated under Second Schedule discrete list
            return StandardQuantityResult(
                is_compliant=True,
                commodity_key=clean_key,
                declared_quantity_raw=f"{quantity_value} {quantity_unit}",
                normalized_value=norm_val,
                normalized_unit=norm_unit,
                permissible_sizes_summary="Non-scheduled commodity; free packaging quantities permitted.",
                mpe_tolerance_value=mpe_val,
                mpe_tolerance_percent=mpe_pct,
                statutory_citation="Rule 5 & General PCR 2011",
            )

        # Evaluate against schedule rules
        is_pass = False
        for rule in spec.rules:
            if rule.unit_symbol == norm_unit and rule.is_valid_quantity(norm_val):
                is_pass = True
                break

        defect = None
        if not is_pass:
            defect = (
                f"Declared net quantity ({quantity_value} {quantity_unit}) is not a permitted standard size "
                f"under the Second Schedule for {spec.official_name}. Violation of Rule 5."
            )

        summary = self._format_spec_summary(spec)

        return StandardQuantityResult(
            is_compliant=is_pass,
            commodity_key=clean_key,
            declared_quantity_raw=f"{quantity_value} {quantity_unit}",
            normalized_value=norm_val,
            normalized_unit=norm_unit,
            permissible_sizes_summary=summary,
            mpe_tolerance_value=mpe_val,
            mpe_tolerance_percent=mpe_pct,
            statutory_citation=f"Rule 5 read with {spec.schedule_reference}",
            defect_reason=defect,
        )

    def calculate_maximum_permissible_error(
        self, norm_val: float, norm_unit: str
    ) -> Tuple[float, float]:
        """
        Compute First Schedule Maximum Permissible Error (MPE) tolerance.
        Table I: Maximum Permissible Errors on Net Quantities Declared by Weight or Volume.
        """
        # Value is in grams or milliliters
        q = norm_val
        if q <= 50.0:
            pct = 9.0
            val = q * 0.09
        elif q <= 100.0:
            pct = 4.5
            val = 4.5  # Fixed 4.5g/ml
        elif q <= 200.0:
            pct = 4.5
            val = q * 0.045
        elif q <= 300.0:
            pct = 3.0
            val = 9.0  # Fixed 9.0g/ml
        elif q <= 500.0:
            pct = 3.0
            val = q * 0.03
        elif q <= 1000.0:
            pct = 1.5
            val = 15.0  # Fixed 15g/ml
        elif q <= 10000.0:
            pct = 1.5
            val = q * 0.015
        elif q <= 15000.0:
            pct = 1.0
            val = 150.0 # Fixed 150g/ml
        else:
            pct = 1.0
            val = q * 0.01

        return val, pct

    def _normalize_to_base_unit(self, val: float, unit: str) -> Tuple[float, str]:
        u = unit.lower().strip()
        if u in ("kg", "kilogram", "kilograms"):
            return val * 1000.0, "g"
        elif u in ("g", "gram", "grams"):
            return val, "g"
        elif u in ("mg", "milligram"):
            return val / 1000.0, "g"
        elif u in ("l", "ltr", "liter", "litre", "litres"):
            return val * 1000.0, "ml"
        elif u in ("ml", "milliliter", "millilitre"):
            return val, "ml"
        return val, u

    def _format_spec_summary(self, spec: CommodityStandardSpec) -> str:
        parts = []
        for r in spec.rules:
            if r.discrete_values:
                items_str = ", ".join(f"{v:g}{r.unit_symbol}" for v in r.discrete_values)
                parts.append(f"Standard sizes: {items_str}")
            if r.step_multiple:
                parts.append(
                    f"Multiples of {r.step_multiple:g}{r.unit_symbol} from {r.min_step_range:g}{r.unit_symbol} to {r.max_step_range:g}{r.unit_symbol}"
                )
        return "; ".join(parts)

    def _initialize_second_schedule_specs(self) -> None:
        """Register all commodities enumerated in the Second Schedule of PCR 2011."""
        # 1. Baby Food
        self._specs["baby_food"] = CommodityStandardSpec(
            commodity_key="baby_food",
            official_name="Baby food",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(is_discrete=True, discrete_values=(100, 200, 400, 500, 1000), unit_symbol="g"),
            ),
        )

        # 2. Weaning Food
        self._specs["weaning_food"] = CommodityStandardSpec(
            commodity_key="weaning_food",
            official_name="Weaning food",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(is_discrete=True, discrete_values=(100, 200, 400, 500, 1000), unit_symbol="g"),
            ),
        )

        # 3. Biscuits
        self._specs["biscuits"] = CommodityStandardSpec(
            commodity_key="biscuits",
            official_name="Biscuits and Rusks",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(25, 50, 60, 75, 100, 120, 150, 200, 250, 300),
                    step_multiple=100,
                    min_step_range=300,
                    max_step_range=1000,
                    unit_symbol="g",
                ),
            ),
        )

        # 4. Bread
        self._specs["bread"] = CommodityStandardSpec(
            commodity_key="bread",
            official_name="Bread including brown bread",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(100, 200, 400, 800),
                    step_multiple=400,
                    min_step_range=800,
                    max_step_range=4000,
                    unit_symbol="g",
                ),
            ),
        )

        # 5. Tea
        self._specs["tea"] = CommodityStandardSpec(
            commodity_key="tea",
            official_name="Uncanned unchilled tea",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(25, 50, 75, 100, 125, 150, 200, 250, 500, 1000),
                    step_multiple=1000,
                    min_step_range=1000,
                    max_step_range=10000,
                    unit_symbol="g",
                ),
            ),
        )

        # 6. Coffee
        self._specs["coffee"] = CommodityStandardSpec(
            commodity_key="coffee",
            official_name="Coffee and coffee-chicory mixture",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(25, 50, 100, 200, 500, 1000),
                    step_multiple=1000,
                    min_step_range=1000,
                    max_step_range=10000,
                    unit_symbol="g",
                ),
            ),
        )

        # 7. Edible Oils, Ghee, Vanaspati
        self._specs["edible_oil"] = CommodityStandardSpec(
            commodity_key="edible_oil",
            official_name="Edible oils, Vanaspati, Ghee and Butter Oil",
            dimension=MeasurementDimension.VOLUME,
            rules=(
                # In volume (ml)
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(50, 100, 200, 500, 1000, 2000, 3000, 5000),
                    step_multiple=5000,
                    min_step_range=5000,
                    max_step_range=20000,
                    unit_symbol="ml",
                ),
                # In mass (g)
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(50, 100, 200, 500, 1000, 2000, 3000, 5000),
                    step_multiple=5000,
                    min_step_range=5000,
                    max_step_range=20000,
                    unit_symbol="g",
                ),
            ),
        )

        # 8. Rice, Wheat, Cereals, Pulses
        self._specs["grains"] = CommodityStandardSpec(
            commodity_key="grains",
            official_name="Rice, Wheat, Atta and Pulses",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(100, 200, 500, 1000, 2000, 5000),
                    step_multiple=5000,
                    min_step_range=5000,
                    max_step_range=50000,
                    unit_symbol="g",
                ),
            ),
        )

        # 9. Salt
        self._specs["salt"] = CommodityStandardSpec(
            commodity_key="salt",
            official_name="Table salt and common salt",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(100, 200, 500, 1000, 2000, 5000),
                    step_multiple=5000,
                    min_step_range=5000,
                    max_step_range=50000,
                    unit_symbol="g",
                ),
            ),
        )

        # 10. Toilet Soap
        self._specs["soap"] = CommodityStandardSpec(
            commodity_key="soap",
            official_name="Toilet soap, laundry soap and bathing bars",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(25, 50, 75, 100, 125, 150),
                    step_multiple=50,
                    min_step_range=150,
                    max_step_range=500,
                    unit_symbol="g",
                ),
            ),
        )

        # 11. Detergent Powders
        self._specs["detergent"] = CommodityStandardSpec(
            commodity_key="detergent",
            official_name="Detergent powder and washing powder",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(50, 100, 200, 500, 1000, 1500, 2000, 3000, 4000, 5000),
                    step_multiple=1000,
                    min_step_range=5000,
                    max_step_range=25000,
                    unit_symbol="g",
                ),
            ),
        )

        # 12. Aerated Soft Drinks
        self._specs["soft_drink"] = CommodityStandardSpec(
            commodity_key="soft_drink",
            official_name="Aerated soft drinks and carbonated waters",
            dimension=MeasurementDimension.VOLUME,
            rules=(
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(
                        100, 150, 200, 250, 300, 330, 500, 600, 750, 1000, 1250, 1500, 1750, 2000, 2250
                    ),
                    unit_symbol="ml",
                ),
            ),
        )

        # 13. Packaged Drinking Water
        self._specs["water"] = CommodityStandardSpec(
            commodity_key="water",
            official_name="Packaged drinking water and mineral water",
            dimension=MeasurementDimension.VOLUME,
            rules=(
                StandardQuantityRule(
                    is_discrete=True,
                    discrete_values=(100, 150, 200, 250, 300, 500, 750, 1000, 1500, 2000, 5000),
                    step_multiple=5000,
                    min_step_range=5000,
                    max_step_range=20000,
                    unit_symbol="ml",
                ),
            ),
        )

        # 14. Cement
        self._specs["cement"] = CommodityStandardSpec(
            commodity_key="cement",
            official_name="Portland cement, slag cement and pozzolana cement",
            dimension=MeasurementDimension.WEIGHT,
            rules=(
                StandardQuantityRule(is_discrete=True, discrete_values=(25000, 50000), unit_symbol="g"),
            ),
        )
