"""
Third, Fourth & Fifth Schedule Industrial & Wholesale Packaging Validator
========================================================================
Implements statutory validation for wholesale packages, special commodities,
textiles, matchboxes, agricultural seeds, cement, and HDPE woven sacks under the
Third, Fourth, and Fifth Schedules of the Legal Metrology (Packaged Commodities) Rules, 2011.

Statutory Schedules:
    - Third Schedule: Declarations on Wholesale Packages (Rule 24 & Rule 25).
    - Fourth Schedule: Exceptions in Respect of Particular Commodities (Rule 26 & Rule 27).
    - Fifth Schedule: Permissible Special Packaging Quantities under Central Notification / Institutional Exemptions.
"""

from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


class PackageCategoryType(str, enum.Enum):
    RETAIL_SINGLE = "RETAIL_SINGLE"
    WHOLESALE_MULTI_PACK = "WHOLESALE_MULTI_PACK"  # Third Schedule
    SEWING_THREAD_TEXTILE = "SEWING_THREAD_TEXTILE"# Fourth Schedule Item 1
    SAFETY_MATCHES = "SAFETY_MATCHES"              # Fourth Schedule Item 2
    CIGARETTES_BIDIS = "CIGARETTES_BIDIS"          # Fourth Schedule Item 3
    AGRICULTURAL_SEEDS = "AGRICULTURAL_SEEDS"      # Fourth Schedule Item 4
    FERTILIZER_HDPE_SACK = "FERTILIZER_HDPE_SACK"  # Fourth Schedule Item 5
    CEMENT_HDPE_BAG = "CEMENT_HDPE_BAG"            # Standard 50kg Industrial Bag
    TEXTILE_FABRIC_PIECE = "TEXTILE_FABRIC_PIECE"  # Rule 13 Fabric Piece Goods
    INSTITUTIONAL_EXEMPT = "INSTITUTIONAL_EXEMPT"  # Rule 26(b) / Fifth Schedule


@dataclass(frozen=True)
class WholesalePackageDeclarations:
    """Mandatory fields for wholesale and master-carton packages under Third Schedule."""

    manufacturer_name_and_address: Optional[str] = None
    identity_of_commodity: Optional[str] = None
    total_number_of_retail_packages: Optional[int] = None
    net_quantity_of_each_retail_unit: Optional[str] = None
    total_net_quantity: Optional[str] = None
    gross_mass: Optional[str] = None
    batch_or_lot_number: Optional[str] = None
    mrp_inclusive_taxes: Optional[float] = None
    is_not_for_retail_sale_marked: bool = False


@dataclass(frozen=True)
class SpecialCommodityDeclarations:
    """Specialized fields for Fourth Schedule commodities."""

    commodity_type: PackageCategoryType
    declared_count: Optional[int] = None          # e.g., match sticks, cigarettes
    declared_length_meters: Optional[float] = None# e.g., sewing thread, twine
    germination_percentage: Optional[float] = None# e.g., agricultural seeds
    purity_percentage: Optional[float] = None     # e.g., agricultural seeds
    net_mass_kg: Optional[float] = None           # e.g., 25kg, 50kg fertilizer sack
    nutrient_npk_ratio: Optional[str] = None      # e.g., 19:19:19 or 46:0:0 for urea


@dataclass(frozen=True)
class CementPackagingDeclarations:
    """Mandatory statutory declarations for industrial cement packaging (IS 1489/IS 269)."""

    manufacturer_name: Optional[str]
    cement_type: Optional[str]                    # e.g., OPC 53, PPC, PSC
    net_mass_kg: Optional[float]                  # Standard is 50.0 kg
    mfg_week: Optional[int]                       # Week number 1-53
    mfg_year: Optional[int]                       # Manufacturing year
    is_bis_isi_marked: bool
    bis_license_cm_l_number: Optional[str]
    mrp_inr: Optional[float]


@dataclass(frozen=True)
class TextileFabricDeclarations:
    """Mandatory declarations for woven textiles and piece goods under Rule 13."""

    fiber_composition: Optional[str] = None       # e.g., 100% Pure Cotton, 65% Poly 35% Cotton
    length_meters: Optional[float] = None
    width_centimeters: Optional[float] = None
    fabric_weight_gsm: Optional[float] = None
    finish_type: Optional[str] = None             # e.g., Bleached, Mercerised, Grey
    mrp_per_meter: Optional[float] = None


@dataclass(frozen=True)
class InstitutionalExemptionDeclarations:
    """Declarations for commodities claimed exempt under Rule 26(b) / Fifth Schedule."""

    purchaser_organization_name: Optional[str]
    purchaser_gstin_or_cin: Optional[str]
    supply_contract_ref: Optional[str]
    package_bearing_not_for_retail_sale: bool
    is_industrial_or_institutional_use: bool


@dataclass(frozen=True)
class ScheduleAuditResult:
    """Outcome of Third, Fourth, or Fifth Schedule audit."""

    is_compliant: bool
    package_category: PackageCategoryType
    schedule_applied: str
    missing_mandatory_declarations: List[str]
    statutory_defects: List[str]
    statutory_citations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_compliant": self.is_compliant,
            "package_category": self.package_category.value,
            "schedule_applied": self.schedule_applied,
            "missing_declarations": self.missing_mandatory_declarations,
            "statutory_defects": self.statutory_defects,
            "statutory_citations": self.statutory_citations,
        }


class IndustrialSchedulesValidator:
    """
    Validates wholesale master cartons, scheduled commodities, and industrial packages
    under Third, Fourth, and Fifth Schedules of Legal Metrology (Packaged Commodities) Rules, 2011.
    """

    def audit_wholesale_package(
        self, decl: WholesalePackageDeclarations
    ) -> ScheduleAuditResult:
        """
        Audit wholesale master carton against Third Schedule (Rules 24 & 25).
        """
        missing: List[str] = []
        defects: List[str] = []
        citations: List[str] = [
            "Third Schedule, Rule 24 PCR 2011",
            "Rule 25 PCR 2011 (Master Carton Labelling)",
        ]

        # Rule 24(a): Manufacturer identity
        if not decl.manufacturer_name_and_address:
            missing.append("Name and address of manufacturer or packer")
            defects.append("Wholesale master carton lacks manufacturer legal metrology details.")

        # Rule 24(b): Commodity identity
        if not decl.identity_of_commodity:
            missing.append("Identity of commodity")
            defects.append("Wholesale package fails to state generic identity of contained goods.")

        # Rule 24(c): Total number of retail packages
        if not decl.total_number_of_retail_packages or decl.total_number_of_retail_packages <= 0:
            missing.append("Total number of retail packages contained")
            defects.append("Wholesale package must declare total retail package unit count.")

        # Rule 24(c): Net quantity of each retail unit
        if not decl.net_quantity_of_each_retail_unit:
            missing.append("Net quantity of each contained retail package")
            defects.append("Wholesale carton must declare individual retail unit net quantity.")

        # Wholesale markings defense
        if not decl.is_not_for_retail_sale_marked:
            defects.append(
                "Wholesale package missing mandatory bold disclaimer: 'NOT FOR DIRECT RETAIL SALE'."
            )

        is_pass = len(missing) == 0 and len(defects) == 0

        return ScheduleAuditResult(
            is_compliant=is_pass,
            package_category=PackageCategoryType.WHOLESALE_MULTI_PACK,
            schedule_applied="Third Schedule (Wholesale Packages)",
            missing_mandatory_declarations=missing,
            statutory_defects=defects,
            statutory_citations=citations,
        )

    def audit_special_commodity(
        self, decl: SpecialCommodityDeclarations
    ) -> ScheduleAuditResult:
        """
        Audit special commodities against Fourth Schedule exceptions (Rule 26 & 27).
        """
        missing: List[str] = []
        defects: List[str] = []
        citations: List[str] = ["Fourth Schedule, PCR 2011"]

        cat = decl.commodity_type

        # 1. Safety Matches (Item 2)
        if cat == PackageCategoryType.SAFETY_MATCHES:
            citations.append("Fourth Schedule Item 2 (Safety Matches)")
            if not decl.declared_count or decl.declared_count <= 0:
                missing.append("Number of match sticks per box")
                defects.append("Safety matchbox must declare average number of match sticks (e.g., 40s, 50s).")
            elif decl.declared_count not in (40, 50, 60):
                defects.append(
                    f"Declared match count ({decl.declared_count}) is non-standard under Fourth Schedule specifications."
                )

        # 2. Sewing Thread and Twine (Item 1)
        elif cat == PackageCategoryType.SEWING_THREAD_TEXTILE:
            citations.append("Fourth Schedule Item 1 (Sewing Thread)")
            if not decl.declared_length_meters or decl.declared_length_meters <= 0.0:
                missing.append("Length in meters")
                defects.append("Sewing thread spool must declare length in standard metric meters (m).")

        # 3. Cigarettes and Bidis (Item 3)
        elif cat == PackageCategoryType.CIGARETTES_BIDIS:
            citations.append("Fourth Schedule Item 3 (Cigarettes & Bidis)")
            if not decl.declared_count or decl.declared_count <= 0:
                missing.append("Number of cigarettes/bidis in package")
                defects.append("Cigarette pack must declare exact count of sticks contained.")
            elif decl.declared_count not in (10, 20):
                defects.append(
                    f"Non-standard cigarette pack count ({decl.declared_count}). Standard retail packs are 10s or 20s."
                )

        # 4. Agricultural Seeds (Item 4)
        elif cat == PackageCategoryType.AGRICULTURAL_SEEDS:
            citations.append("Fourth Schedule Item 4 (Agricultural Seeds)")
            if decl.germination_percentage is None or decl.germination_percentage <= 0.0:
                missing.append("Minimum Germination Percentage")
                defects.append("Certified seed packaging must declare minimum germination percentage.")
            elif decl.germination_percentage > 100.0:
                defects.append("Germination percentage cannot exceed 100.0%.")

            if decl.purity_percentage is None or decl.purity_percentage <= 0.0:
                missing.append("Minimum Genetic/Physical Purity Percentage")
                defects.append("Certified seed packaging must declare genetic and physical purity percentage.")
            elif decl.purity_percentage > 100.0:
                defects.append("Purity percentage cannot exceed 100.0%.")

        # 5. Fertilizers in HDPE/PP Sacks (Item 5)
        elif cat == PackageCategoryType.FERTILIZER_HDPE_SACK:
            citations.append("Fourth Schedule Item 5 (Fertilizers)")
            if decl.net_mass_kg is None:
                missing.append("Net mass in kilograms")
                defects.append("Fertilizer sacks must declare net mass in kilograms (standard 25kg or 50kg).")
            elif decl.net_mass_kg not in (25.0, 45.0, 50.0):
                defects.append(
                    f"Non-standard fertilizer bag weight ({decl.net_mass_kg} kg). Standard is 25kg, 45kg (neem-coated urea), or 50kg."
                )
            if not decl.nutrient_npk_ratio:
                missing.append("Nutrient N-P-K guaranteed ratio")
                defects.append("Fertilizer packaging must display statutory N-P-K nutrient ratio under FCO.")

        is_pass = len(missing) == 0 and len(defects) == 0

        return ScheduleAuditResult(
            is_compliant=is_pass,
            package_category=cat,
            schedule_applied="Fourth Schedule (Particular Commodity Exceptions)",
            missing_mandatory_declarations=missing,
            statutory_defects=defects,
            statutory_citations=citations,
        )

    def audit_cement_bag(
        self, decl: CementPackagingDeclarations
    ) -> ScheduleAuditResult:
        """
        Validates industrial cement bags under BIS Quality Control Order & Legal Metrology Rules.
        Standard retail cement bags must be 50.0 kg, declare week/year of packing, and carry ISI mark.
        """
        missing: List[str] = []
        defects: List[str] = []
        citations: List[str] = [
            "Rule 6 & Rule 12 PCR 2011",
            "Cement (Quality Control) Order, BIS IS 1489 / IS 269",
        ]

        if not decl.manufacturer_name:
            missing.append("Manufacturer brand and manufacturing works address")
            defects.append("Cement bag lacks licensed manufacturing works details.")

        if not decl.cement_type:
            missing.append("Cement grade / type classification")
            defects.append("Missing cement classification (e.g., OPC 53 Grade, Portland Pozzolana Cement - PPC).")

        if decl.net_mass_kg is None:
            missing.append("Net mass in kilograms")
            defects.append("Cement bag must state net mass in metric kilograms.")
        elif decl.net_mass_kg != 50.0:
            defects.append(
                f"Non-standard retail cement mass ({decl.net_mass_kg} kg). Mandatory standard size is 50.0 kg net."
            )

        current_year = datetime.datetime.now().year
        if decl.mfg_week is None or decl.mfg_year is None:
            missing.append("Week and Year of manufacture (WW/YYYY)")
            defects.append("Cement is time-perishable; must declare week and year of manufacture.")
        else:
            if not (1 <= decl.mfg_week <= 53):
                defects.append(f"Invalid manufacturing week index: {decl.mfg_week}. Must be between 1 and 53.")
            if decl.mfg_year > current_year or decl.mfg_year < (current_year - 2):
                defects.append(f"Stale or forward-dated manufacturing year: {decl.mfg_year}.")

        if not decl.is_bis_isi_marked:
            missing.append("BIS Standard Mark (ISI Certification)")
            defects.append("Cement is under mandatory BIS certification; ISI logo and CM/L license number required.")
        elif not decl.bis_license_cm_l_number:
            missing.append("BIS CM/L License Number")
            defects.append("ISI mark present but lacks statutory 7 or 8 digit CM/L license number.")

        if decl.mrp_inr is None or decl.mrp_inr <= 0.0:
            missing.append("Maximum Retail Price (MRP inclusive of all taxes)")
            defects.append("Mandatory retail price declaration absent.")

        is_pass = len(missing) == 0 and len(defects) == 0

        return ScheduleAuditResult(
            is_compliant=is_pass,
            package_category=PackageCategoryType.CEMENT_HDPE_BAG,
            schedule_applied="Cement Standards (IS 1489 / PCR 2011)",
            missing_mandatory_declarations=missing,
            statutory_defects=defects,
            statutory_citations=citations,
        )

    def audit_textile_piece(
        self, decl: TextileFabricDeclarations
    ) -> ScheduleAuditResult:
        """
        Validates fabric piece goods and woven textiles under Rule 13 PCR 2011.
        """
        missing: List[str] = []
        defects: List[str] = []
        citations: List[str] = [
            "Rule 13 PCR 2011 (Textile Goods and Piece Fabrics)",
            "Rule 13(1) Composition and Dimensions Declaration",
        ]

        if not decl.fiber_composition:
            missing.append("Fiber composition breakdown")
            defects.append("Textile piece goods must declare fiber percentage (e.g., 100% Cotton, 60% Silk 40% Viscose).")

        if decl.length_meters is None or decl.length_meters <= 0.0:
            missing.append("Length in standard meters (m)")
            defects.append("Mandatory metric length declaration missing on textile fabric piece.")

        if decl.width_centimeters is None or decl.width_centimeters <= 0.0:
            missing.append("Width in standard centimeters (cm)")
            defects.append("Mandatory metric width declaration missing on fabric bolt.")

        if decl.fabric_weight_gsm is not None and decl.fabric_weight_gsm <= 0.0:
            defects.append("Declared GSM (grams per square meter) must be a positive number.")

        if decl.mrp_per_meter is None or decl.mrp_per_meter <= 0.0:
            missing.append("Unit Sale Price per meter")
            defects.append("Textile fabric sold by length must declare Unit Sale Price (MRP per meter).")

        is_pass = len(missing) == 0 and len(defects) == 0

        return ScheduleAuditResult(
            is_compliant=is_pass,
            package_category=PackageCategoryType.TEXTILE_FABRIC_PIECE,
            schedule_applied="Rule 13 (Textile Fabric Goods)",
            missing_mandatory_declarations=missing,
            statutory_defects=defects,
            statutory_citations=citations,
        )

    def audit_institutional_exemption(
        self, decl: InstitutionalExemptionDeclarations
    ) -> ScheduleAuditResult:
        """
        Audits validity of claims for institutional/industrial consumer exemption
        under Rule 26(b) of Legal Metrology (Packaged Commodities) Rules, 2011.
        """
        missing: List[str] = []
        defects: List[str] = []
        citations: List[str] = [
            "Rule 26(b) PCR 2011 (Institutional Consumer Exemption)",
            "Rule 2(p) Definition of Industrial / Institutional Consumer",
        ]

        if not decl.purchaser_organization_name:
            missing.append("Institutional / industrial purchaser name")
            defects.append("Exemption claim lacks corporate identity of institutional buyer.")

        if not decl.purchaser_gstin_or_cin:
            missing.append("Purchaser GSTIN or Corporate Identity Number (CIN)")
            defects.append("Commercial institutional purchases require valid corporate identifier.")

        if not decl.supply_contract_ref:
            missing.append("Institutional purchase order or commercial supply contract reference")
            defects.append("Direct institutional supply agreement reference missing.")

        if not decl.package_bearing_not_for_retail_sale:
            defects.append(
                "Package lacks mandatory bold notice: 'FOR USE BY INSTITUTIONAL CONSUMER ONLY - NOT FOR RETAIL SALE'."
            )

        if not decl.is_industrial_or_institutional_use:
            defects.append(
                "Goods diverted for retail sale; buyer does not qualify as direct consumer for service or production."
            )

        is_pass = len(missing) == 0 and len(defects) == 0

        return ScheduleAuditResult(
            is_compliant=is_pass,
            package_category=PackageCategoryType.INSTITUTIONAL_EXEMPT,
            schedule_applied="Rule 26(b) Institutional Exemption",
            missing_mandatory_declarations=missing,
            statutory_defects=defects,
            statutory_citations=citations,
        )
