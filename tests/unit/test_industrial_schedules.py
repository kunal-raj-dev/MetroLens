"""
Unit Tests for Third, Fourth & Fifth Industrial Schedules Validator
===================================================================
Tests statutory verification for wholesale master cartons, safety matches,
sewing thread, agricultural seeds, fertilizers, industrial cement, textiles,
and Rule 26(b) institutional consumer exemptions under PCR 2011.
"""

import pytest

from apps.api.verification.industrial_schedules import (
    IndustrialSchedulesValidator,
    PackageCategoryType,
    WholesalePackageDeclarations,
    SpecialCommodityDeclarations,
    CementPackagingDeclarations,
    TextileFabricDeclarations,
    InstitutionalExemptionDeclarations,
)


@pytest.fixture
def validator() -> IndustrialSchedulesValidator:
    return IndustrialSchedulesValidator()


# ==============================================================================
# 1. Third Schedule: Wholesale Master Cartons (Rules 24 & 25)
# ==============================================================================

def test_wholesale_package_fully_compliant(validator: IndustrialSchedulesValidator):
    decl = WholesalePackageDeclarations(
        manufacturer_name_and_address="Britannia Industries Ltd, 5/1A Hungerford Street, Kolkata - 700017",
        identity_of_commodity="Good Day Butter Cookies Master Shipper",
        total_number_of_retail_packages=48,
        net_quantity_of_each_retail_unit="100 g",
        total_net_quantity="4.8 kg",
        gross_mass="5.2 kg",
        batch_or_lot_number="LOT-2026-X99",
        mrp_inclusive_taxes=1440.0,
        is_not_for_retail_sale_marked=True,
    )
    res = validator.audit_wholesale_package(decl)
    assert res.is_compliant is True
    assert res.package_category == PackageCategoryType.WHOLESALE_MULTI_PACK
    assert len(res.missing_mandatory_declarations) == 0
    assert len(res.statutory_defects) == 0


def test_wholesale_package_missing_declarations(validator: IndustrialSchedulesValidator):
    decl = WholesalePackageDeclarations(
        manufacturer_name_and_address=None,
        identity_of_commodity=None,
        total_number_of_retail_packages=0,
        net_quantity_of_each_retail_unit=None,
        is_not_for_retail_sale_marked=False,
    )
    res = validator.audit_wholesale_package(decl)
    assert res.is_compliant is False
    assert "Name and address of manufacturer or packer" in res.missing_mandatory_declarations
    assert "Identity of commodity" in res.missing_mandatory_declarations
    assert "Total number of retail packages contained" in res.missing_mandatory_declarations
    assert any("NOT FOR DIRECT RETAIL SALE" in d for d in res.statutory_defects)


# ==============================================================================
# 2. Fourth Schedule: Special Commodities (Rule 26 & 27)
# ==============================================================================

def test_safety_matches_standard_and_non_standard(validator: IndustrialSchedulesValidator):
    # Compliant 50 sticks
    c_decl = SpecialCommodityDeclarations(
        commodity_type=PackageCategoryType.SAFETY_MATCHES,
        declared_count=50,
    )
    res_c = validator.audit_special_commodity(c_decl)
    assert res_c.is_compliant is True

    # Non-standard 37 sticks
    ns_decl = SpecialCommodityDeclarations(
        commodity_type=PackageCategoryType.SAFETY_MATCHES,
        declared_count=37,
    )
    res_ns = validator.audit_special_commodity(ns_decl)
    assert res_ns.is_compliant is False
    assert any("non-standard under Fourth Schedule" in d for d in res_ns.statutory_defects)


def test_sewing_thread_length(validator: IndustrialSchedulesValidator):
    # Compliant 100m spool
    c_decl = SpecialCommodityDeclarations(
        commodity_type=PackageCategoryType.SEWING_THREAD_TEXTILE,
        declared_length_meters=100.0,
    )
    res_c = validator.audit_special_commodity(c_decl)
    assert res_c.is_compliant is True

    # Missing length
    nc_decl = SpecialCommodityDeclarations(
        commodity_type=PackageCategoryType.SEWING_THREAD_TEXTILE,
        declared_length_meters=0.0,
    )
    res_nc = validator.audit_special_commodity(nc_decl)
    assert res_nc.is_compliant is False
    assert "Length in meters" in res_nc.missing_mandatory_declarations


def test_agricultural_seeds_germination_and_purity(validator: IndustrialSchedulesValidator):
    # Compliant seeds
    c_decl = SpecialCommodityDeclarations(
        commodity_type=PackageCategoryType.AGRICULTURAL_SEEDS,
        germination_percentage=85.0,
        purity_percentage=98.5,
    )
    res_c = validator.audit_special_commodity(c_decl)
    assert res_c.is_compliant is True

    # Invalid > 100%
    inv_decl = SpecialCommodityDeclarations(
        commodity_type=PackageCategoryType.AGRICULTURAL_SEEDS,
        germination_percentage=105.0,
        purity_percentage=99.0,
    )
    res_inv = validator.audit_special_commodity(inv_decl)
    assert res_inv.is_compliant is False
    assert any("cannot exceed 100.0%" in d for d in res_inv.statutory_defects)


def test_fertilizer_hdpe_sack(validator: IndustrialSchedulesValidator):
    # Compliant 50kg DAP with N-P-K
    c_decl = SpecialCommodityDeclarations(
        commodity_type=PackageCategoryType.FERTILIZER_HDPE_SACK,
        net_mass_kg=50.0,
        nutrient_npk_ratio="18:46:0",
    )
    res_c = validator.audit_special_commodity(c_decl)
    assert res_c.is_compliant is True

    # Non-standard 35kg bag and missing NPK
    nc_decl = SpecialCommodityDeclarations(
        commodity_type=PackageCategoryType.FERTILIZER_HDPE_SACK,
        net_mass_kg=35.0,
        nutrient_npk_ratio=None,
    )
    res_nc = validator.audit_special_commodity(nc_decl)
    assert res_nc.is_compliant is False
    assert any("Non-standard fertilizer bag weight" in d for d in res_nc.statutory_defects)
    assert "Nutrient N-P-K guaranteed ratio" in res_nc.missing_mandatory_declarations


# ==============================================================================
# 3. Industrial Cement Bags (IS 1489 / IS 269)
# ==============================================================================

def test_cement_bag_compliant(validator: IndustrialSchedulesValidator):
    decl = CementPackagingDeclarations(
        manufacturer_name="UltraTech Cement Limited, Unit: Gujarat Cement Works",
        cement_type="Portland Pozzolana Cement (PPC)",
        net_mass_kg=50.0,
        mfg_week=34,
        mfg_year=2026,
        is_bis_isi_marked=True,
        bis_license_cm_l_number="CM/L-1234567",
        mrp_inr=395.0,
    )
    res = validator.audit_cement_bag(decl)
    assert res.is_compliant is True
    assert res.package_category == PackageCategoryType.CEMENT_HDPE_BAG
    assert len(res.statutory_defects) == 0


def test_cement_bag_violations(validator: IndustrialSchedulesValidator):
    decl = CementPackagingDeclarations(
        manufacturer_name="Unknown Works",
        cement_type="OPC 53",
        net_mass_kg=40.0,  # Prohibited 40kg retail bag
        mfg_week=58,       # Invalid week number > 53
        mfg_year=2026,
        is_bis_isi_marked=False,
        bis_license_cm_l_number=None,
        mrp_inr=None,
    )
    res = validator.audit_cement_bag(decl)
    assert res.is_compliant is False
    assert any("Non-standard retail cement mass (40.0 kg)" in d for d in res.statutory_defects)
    assert any("Invalid manufacturing week index" in d for d in res.statutory_defects)
    assert "BIS Standard Mark (ISI Certification)" in res.missing_mandatory_declarations
    assert "Maximum Retail Price (MRP inclusive of all taxes)" in res.missing_mandatory_declarations


# ==============================================================================
# 4. Textile Fabric & Piece Goods (Rule 13)
# ==============================================================================

def test_textile_piece_compliant(validator: IndustrialSchedulesValidator):
    decl = TextileFabricDeclarations(
        fiber_composition="100% Combed Compact Cotton",
        length_meters=2.5,
        width_centimeters=148.0,
        fabric_weight_gsm=180.0,
        finish_type="Mercerised",
        mrp_per_meter=350.0,
    )
    res = validator.audit_textile_piece(decl)
    assert res.is_compliant is True
    assert res.package_category == PackageCategoryType.TEXTILE_FABRIC_PIECE


def test_textile_piece_deficiencies(validator: IndustrialSchedulesValidator):
    decl = TextileFabricDeclarations(
        fiber_composition=None,
        length_meters=None,
        width_centimeters=-5.0,
        fabric_weight_gsm=-10.0,
        finish_type=None,
        mrp_per_meter=None,
    )
    res = validator.audit_textile_piece(decl)
    assert res.is_compliant is False
    assert "Fiber composition breakdown" in res.missing_mandatory_declarations
    assert "Length in standard meters (m)" in res.missing_mandatory_declarations
    assert "Width in standard centimeters (cm)" in res.missing_mandatory_declarations
    assert "Unit Sale Price per meter" in res.missing_mandatory_declarations
    assert any("Declared GSM" in d for d in res.statutory_defects)


# ==============================================================================
# 5. Rule 26(b) Institutional Consumer Exemption
# ==============================================================================

def test_institutional_exemption_audit(validator: IndustrialSchedulesValidator):
    # Legitimate institutional purchase
    legit_decl = InstitutionalExemptionDeclarations(
        purchaser_organization_name="Indian Railways - Northern Division Works",
        purchaser_gstin_or_cin="07AAAGR0123M1Z8",
        supply_contract_ref="NR/ELEC/2026/BID-8891",
        package_bearing_not_for_retail_sale=True,
        is_industrial_or_institutional_use=True,
    )
    res_legit = validator.audit_institutional_exemption(legit_decl)
    assert res_legit.is_compliant is True

    # Invalid claim: diverted to retail without markings
    bogus_decl = InstitutionalExemptionDeclarations(
        purchaser_organization_name="Corner Retail Grocer",
        purchaser_gstin_or_cin="27AAAAA0000A1Z5",
        supply_contract_ref=None,
        package_bearing_not_for_retail_sale=False,
        is_industrial_or_institutional_use=False,
    )
    res_bogus = validator.audit_institutional_exemption(bogus_decl)
    assert res_bogus.is_compliant is False
    assert any("NOT FOR RETAIL SALE" in d for d in res_bogus.statutory_defects)
    assert any("diverted for retail sale" in d for d in res_bogus.statutory_defects)
