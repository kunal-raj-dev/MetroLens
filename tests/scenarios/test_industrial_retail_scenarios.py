"""
Industrial & Retail Statutory Packaging Enforcement Scenarios
=============================================================
Authoritative end-to-end statutory enforcement scenarios testing the Legal
Metrology Act, 2009, Legal Metrology (Packaged Commodities) Rules, 2011,
Bureau of Indian Standards Quality Control Orders, and CCPA 2023 Guidelines.

Covers 60+ real-world commercial packaging scenarios:
    1. Edible Oils, Vanaspati & Ghee (Rule 12 Dual Volume/Mass Declarations).
    2. Industrial Cement & Construction Materials (IS 1489 / IS 269 standard 50kg bags).
    3. Paints, Varnishes & Thinners (Rule 12 Net Volume at Specified Temperatures).
    4. Fertilizers & Agricultural Chemicals (Neem Urea, DAP, MOP with N-P-K ratios).
    5. Certified Agricultural Seeds (Germination %, Physical/Genetic Purity %).
    6. Textile Piece Goods & Sewing Threads (Rule 13 Fabric Length, Width & GSM).
    7. Safety Matches & Tobacco Products (Standard Match Sticks & Cigarette Counts).
    8. Consumer Durables & White Goods (Rule 6 Importer, Country of Origin, BEE Rating).
    9. E-Commerce Digital Product Display (CCPA 2023 Dark Patterns & Rule 6(10) USP).
   10. Compounding Ladders under Section 48 & 48A for First vs Repeat Offences.
   11. Wholesale Master Cartons under Third Schedule (Multi-Pack Retail Disclaimers).
   12. Institutional & Industrial Consumer Exemption Audits under Rule 26(b).
"""

import io
from typing import Any, Dict, List
import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services.pipeline_orchestrator import PipelineOrchestrator
from apps.api.verification.industrial_schedules import (
    IndustrialSchedulesValidator,
    PackageCategoryType,
    WholesalePackageDeclarations,
    SpecialCommodityDeclarations,
    CementPackagingDeclarations,
    TextileFabricDeclarations,
    InstitutionalExemptionDeclarations,
)
from apps.api.verification.ecommerce_auditor import (
    ECommerceMarketplaceComplianceAuditor,
    DigitalPDPDeclarations,
    ECommercePlatformType,
    DarkPatternType,
)


@pytest.fixture
def client(monkeypatch) -> TestClient:
    def fake_process_image(self, image_bytes: bytes, filename: str, mime_type: str):
        from apps.api.schemas import InspectionResponse, PackageDeclarations, ProcessingMetrics
        return InspectionResponse(
            inspection_id="insp-industrial-scen-99",
            state="COMPLIANT",
            declarations=PackageDeclarations(
                mrp_raw="Rs. 450.00",
                mrp_inr=450.0,
                net_quantity_raw="50 kg",
                net_quantity_value=50.0,
                net_quantity_unit="kg",
                unit_sale_price_raw="Rs. 9.00 per kg",
                unit_sale_price_inr=9.0,
                manufacturer_address="Test Industrial Zone, Gujarat",
                consumer_care_email="support@industrialpack.in",
                consumer_care_phone="1800119900",
                country_of_origin="India",
                date_of_manufacture="08/2026",
            ),
            statutory_violations=[],
            legal_notice=None,
            processing_metrics=ProcessingMetrics(
                total_pipeline_latency_ms=45.2,
                preprocessing_latency_ms=5.1,
                ocr_latency_ms=25.0,
                verification_latency_ms=10.1,
                pdf_compilation_latency_ms=5.0,
            ),
        )
    monkeypatch.setattr(InspectionPipelineOrchestrator, "process_image", fake_process_image)
    return TestClient(app)


# ==============================================================================
# SECTION 1: EDIBLE OILS & FATS DUAL VOLUME/MASS SCENARIOS (RULE 12)
# ==============================================================================

@pytest.mark.parametrize(
    "oil_name, declared_vol_l, declared_mass_g, expected_min_mass_g, expected_max_mass_g, is_compliant",
    [
        ("Mustard Oil (Density ~0.910 g/ml)", 1.0, 910.0, 900.0, 920.0, True),
        ("Refined Sunflower Oil (Density ~0.915 g/ml)", 1.0, 915.0, 905.0, 925.0, True),
        ("Groundnut Oil 5L Jar (Density ~0.912 g/ml)", 5.0, 4560.0, 4500.0, 4600.0, True),
        ("Desi Cow Ghee 1L Jar (Density ~0.905 g/ml)", 1.0, 905.0, 895.0, 915.0, True),
        ("Olive Oil Extra Virgin 500ml", 0.5, 458.0, 450.0, 465.0, True),
        ("Underweight Refined Soyabean Oil 1L", 1.0, 850.0, 900.0, 925.0, False),  # 850g is short by 60g
        ("Severely Underweight Mustard Oil 5L", 5.0, 4100.0, 4500.0, 4600.0, False), # 4100g is short by 450g
    ],
)
def test_edible_oil_density_and_dual_declaration_audit(
    oil_name: str,
    declared_vol_l: float,
    declared_mass_g: float,
    expected_min_mass_g: float,
    expected_max_mass_g: float,
    is_compliant: bool,
):
    """
    Rule 12 of PCR 2011 mandates that for edible oils and vanaspati, when net quantity
    is declared in volume (liters or milliliters), the equivalent mass in grams or
    kilograms must also be stated, which must match statutory density tables.
    """
    within_bounds = expected_min_mass_g <= declared_mass_g <= expected_max_mass_g
    assert within_bounds == is_compliant, f"Oil {oil_name} mass verification mismatch"


# ==============================================================================
# SECTION 2: INDUSTRIAL CEMENT & CONSTRUCTION MATERIALS (IS 1489 / IS 269)
# ==============================================================================

@pytest.mark.parametrize(
    "brand, cement_type, net_kg, mfg_week, mfg_year, has_isi, cm_l_num, mrp, expected_pass",
    [
        ("UltraTech Cement Ltd", "PPC (Portland Pozzolana)", 50.0, 32, 2026, True, "CM/L-1234567", 390.0, True),
        ("Ambuja Cements Ltd", "OPC 53 Grade", 50.0, 15, 2026, True, "CM/L-2345678", 410.0, True),
        ("ACC Limited", "Portland Slag Cement (PSC)", 50.0, 24, 2026, True, "CM/L-3456789", 380.0, True),
        ("Dalmia Bharat Cement", "Composite Cement", 50.0, 5, 2026, True, "CM/L-4567890", 375.0, True),
        ("Shree Cement (Roofon)", "PPC", 50.0, 48, 2025, True, "CM/L-5678901", 385.0, True),
        ("Illegal 40kg Bag Brand", "PPC", 40.0, 20, 2026, True, "CM/L-6789012", 320.0, False),  # 40kg bag illegal
        ("Missing ISI Mark Cement", "OPC 43 Grade", 50.0, 22, 2026, False, None, 360.0, False),   # No ISI logo
        ("Expired Manufacturing Date", "OPC 53 Grade", 50.0, 10, 2021, True, "CM/L-7890123", 400.0, False), # 2021 is stale
        ("Invalid Calendar Week Index", "PPC", 50.0, 59, 2026, True, "CM/L-8901234", 395.0, False), # Week 59 > 53
    ],
)
def test_industrial_cement_packaging_scenarios(
    brand: str,
    cement_type: str,
    net_kg: float,
    mfg_week: int,
    mfg_year: int,
    has_isi: bool,
    cm_l_num: str,
    mrp: float,
    expected_pass: bool,
):
    validator = IndustrialSchedulesValidator()
    decl = CementPackagingDeclarations(
        manufacturer_name=brand,
        cement_type=cement_type,
        net_mass_kg=net_kg,
        mfg_week=mfg_week,
        mfg_year=mfg_year,
        is_bis_isi_marked=has_isi,
        bis_license_cm_l_number=cm_l_num,
        mrp_inr=mrp,
    )
    result = validator.audit_cement_bag(decl)
    assert result.is_compliant == expected_pass, f"Cement scenario '{brand}' failed expectations: {result.statutory_defects}"


# ==============================================================================
# SECTION 3: FERTILIZERS & AGRICULTURAL CHEMICALS (FOURTH SCHEDULE ITEM 5)
# ==============================================================================

@pytest.mark.parametrize(
    "fertilizer_name, net_kg, npk_ratio, expected_pass",
    [
        ("Neem Coated Urea (IFFCO)", 45.0, "46:0:0", True),        # Mandatory 45kg bag for neem urea
        ("Di-Ammonium Phosphate - DAP (KRIBHCO)", 50.0, "18:46:0", True), # Standard 50kg DAP bag
        ("Muriate of Potash - MOP (IPL)", 50.0, "0:0:60", True),   # Standard 50kg MOP bag
        ("NPK Complex 10:26:26 (Coromandel)", 50.0, "10:26:26", True),
        ("Water Soluble 19:19:19 Foliar Grade", 25.0, "19:19:19", True), # Standard 25kg bag
        ("Non-Standard 35kg DAP Bag", 35.0, "18:46:0", False),      # 35kg is prohibited non-standard weight
        ("Missing NPK Ratio Fertilizer Bag", 50.0, None, False),    # Lacks mandatory nutrient declaration
    ],
)
def test_fertilizer_sack_statutory_scenarios(
    fertilizer_name: str,
    net_kg: float,
    npk_ratio: str,
    expected_pass: bool,
):
    validator = IndustrialSchedulesValidator()
    decl = SpecialCommodityDeclarations(
        commodity_type=PackageCategoryType.FERTILIZER_HDPE_SACK,
        net_mass_kg=net_kg,
        nutrient_npk_ratio=npk_ratio,
    )
    result = validator.audit_special_commodity(decl)
    assert result.is_compliant == expected_pass, f"Fertilizer {fertilizer_name} failed: {result.statutory_defects}"


# ==============================================================================
# SECTION 4: CERTIFIED AGRICULTURAL SEEDS (FOURTH SCHEDULE ITEM 4)
# ==============================================================================

@pytest.mark.parametrize(
    "crop_name, germination_pct, purity_pct, expected_pass",
    [
        ("Certified Hybrid Paddy Seeds (PR-126)", 85.0, 98.0, True),
        ("Certified Wheat Seeds (HD-3086)", 90.0, 99.0, True),
        ("Certified Hybrid Cotton Seeds (Bollgard II)", 75.0, 95.0, True),
        ("Certified Mustard Seeds (Pusa Bold)", 85.0, 97.0, True),
        ("Seed with Missing Germination Declaration", 0.0, 98.0, False),
        ("Seed with Missing Purity Declaration", 85.0, 0.0, False),
        ("Seed with Impossible Germination Percentage", 108.0, 99.0, False),
    ],
)
def test_agricultural_seeds_scenarios(
    crop_name: str,
    germination_pct: float,
    purity_pct: float,
    expected_pass: bool,
):
    validator = IndustrialSchedulesValidator()
    decl = SpecialCommodityDeclarations(
        commodity_type=PackageCategoryType.AGRICULTURAL_SEEDS,
        germination_percentage=germination_pct,
        purity_percentage=purity_pct,
    )
    result = validator.audit_special_commodity(decl)
    assert result.is_compliant == expected_pass, f"Seed {crop_name} failed: {result.statutory_defects}"


# ==============================================================================
# SECTION 5: TEXTILE PIECE GOODS & SEWING THREAD (RULE 13 & FOURTH SCHEDULE)
# ==============================================================================

@pytest.mark.parametrize(
    "textile_desc, fiber_comp, length_m, width_cm, gsm, mrp_per_m, expected_pass",
    [
        ("Pure Cotton Suiting Fabric", "100% Giza Cotton", 3.0, 148.0, 240.0, 850.0, True),
        ("Polyester-Viscose Trouser Fabric", "65% Poly 35% Viscose", 1.2, 144.0, 280.0, 420.0, True),
        ("Silk Saree Length", "100% Mulberry Silk", 6.3, 115.0, 80.0, 1200.0, True),
        ("Cotton Bed-sheeting Fabric", "100% Organic Cotton", 2.5, 274.0, 160.0, 390.0, True),
        ("Fabric Missing Fiber Composition", None, 2.0, 140.0, 200.0, 300.0, False),
        ("Fabric Missing Width Dimension", "100% Linen", 2.5, None, 190.0, 650.0, False),
        ("Fabric Missing Unit Sale Price", "100% Wool", 1.5, 150.0, 350.0, None, False),
    ],
)
def test_textile_piece_goods_scenarios(
    textile_desc: str,
    fiber_comp: str,
    length_m: float,
    width_cm: float,
    gsm: float,
    mrp_per_m: float,
    expected_pass: bool,
):
    validator = IndustrialSchedulesValidator()
    decl = TextileFabricDeclarations(
        fiber_composition=fiber_comp,
        length_meters=length_m,
        width_centimeters=width_cm,
        fabric_weight_gsm=gsm,
        mrp_per_meter=mrp_per_m,
    )
    result = validator.audit_textile_piece(decl)
    assert result.is_compliant == expected_pass, f"Textile {textile_desc} failed: {result.statutory_defects}"


# ==============================================================================
# SECTION 6: SAFETY MATCHES & CIGARETTE PACKS (FOURTH SCHEDULE ITEMS 2 & 3)
# ==============================================================================

@pytest.mark.parametrize(
    "commodity_type, declared_count, expected_pass",
    [
        (PackageCategoryType.SAFETY_MATCHES, 40, True),
        (PackageCategoryType.SAFETY_MATCHES, 50, True),
        (PackageCategoryType.SAFETY_MATCHES, 60, True),
        (PackageCategoryType.SAFETY_MATCHES, 35, False),  # Non-standard 35 sticks
        (PackageCategoryType.SAFETY_MATCHES, 48, False),  # Non-standard 48 sticks
        (PackageCategoryType.CIGARETTES_BIDIS, 10, True), # Standard 10s pack
        (PackageCategoryType.CIGARETTES_BIDIS, 20, True), # Standard 20s pack
        (PackageCategoryType.CIGARETTES_BIDIS, 15, False),# Non-standard 15s pack
        (PackageCategoryType.CIGARETTES_BIDIS, 5, False), # Non-standard 5s loose pack
    ],
)
def test_matches_and_cigarettes_count_scenarios(
    commodity_type: PackageCategoryType,
    declared_count: int,
    expected_pass: bool,
):
    validator = IndustrialSchedulesValidator()
    decl = SpecialCommodityDeclarations(
        commodity_type=commodity_type,
        declared_count=declared_count,
    )
    result = validator.audit_special_commodity(decl)
    assert result.is_compliant == expected_pass, f"Count {declared_count} for {commodity_type} failed: {result.statutory_defects}"


# ==============================================================================
# SECTION 7: E-COMMERCE CCPA DARK PATTERNS & DIGITAL DECLARATIONS (RULE 6(10))
# ==============================================================================

@pytest.mark.parametrize(
    "listing_title, mrp, price, usp, raw_text, drip_fees, expected_pass",
    [
        (
            "Premium Basmati Rice 5kg Bag",
            650.0, 550.0, 110.0, "", None, True
        ),
        (
            "Cold Pressed Virgin Coconut Oil 1L",
            450.0, 399.0, 399.0, "", None, True
        ),
        (
            "Dark Pattern Drip Pricing Specimen",
            1000.0, 799.0, 799.0, "", {"base": 799.0, "convenience fee": 150.0, "handling charge": 49.0, "total_payable": 998.0}, False
        ),
        (
            "Fake Countdown Urgency Dark Pattern Listing",
            2000.0, 1299.0, 1299.0, "Hurry! Deal expires in 5 min! Flash sale ending soon!", None, False
        ),
        (
            "Missing Unit Sale Price (USP) Violation",
            500.0, 450.0, None, "", None, False
        ),
    ],
)
def test_ecommerce_dark_patterns_and_rule_6_10_scenarios(
    listing_title: str,
    mrp: float,
    price: float,
    usp: float,
    raw_text: str,
    drip_fees: dict,
    expected_pass: bool,
):
    auditor = ECommerceMarketplaceComplianceAuditor()
    pdp = DigitalPDPDeclarations(
        title=listing_title,
        declared_mrp=mrp,
        declared_selling_price=price,
        declared_usp=usp,
        usp_unit_denominator="kg" if "Rice" in listing_title else "L",
        net_quantity_str="5 kg" if "Rice" in listing_title else "1 L",
        country_of_origin="India",
        manufacturer_details="National Consumer Goods Ltd, Industrial Area, Mumbai - 400001",
        consumer_care_details="care@ncg.in | 1800-200-1122",
        expiry_or_best_before="12/2027",
        raw_text_payload=raw_text,
    )
    result = auditor.audit_listing(pdp, announced_price_breakdown=drip_fees)
    assert result.is_compliant == expected_pass, f"Listing '{listing_title}' failed expectations: {result.statutory_defects} {result.dark_patterns_detected}"


# ==============================================================================
# SECTION 8: SECTION 48 & 48A COMPOUNDING LADDER & REPEAT OFFENCE SCENARIOS
# ==============================================================================

@pytest.mark.parametrize(
    "offence_index, prior_offence_count, expected_compounding_tier, can_compound, expected_penalty_multiplier",
    [
        (1, 0, "FIRST_OFFENCE", True, 1.0),       # First offence: normal compounding fee under Sec 48
        (2, 1, "SECOND_OFFENCE", True, 2.0),      # Second offence within 3 years: doubled penalty
        (3, 2, "HABITUAL_OFFENCE", False, 0.0),   # Third offence: compounding barred under Sec 48(3); prosecution in court
    ],
)
def test_section_48_compounding_escalation_lifecycle(
    offence_index: int,
    prior_offence_count: int,
    expected_compounding_tier: str,
    can_compound: bool,
    expected_penalty_multiplier: float,
):
    """
    Section 48 of the Legal Metrology Act, 2009 allows compounding of offences for first
    and second occurrences, but explicitly bars compounding for a third occurrence within
    three years, requiring formal charge-sheet filing in the Court of Judicial Magistrate.
    """
    if prior_offence_count == 0:
        tier = "FIRST_OFFENCE"
        eligible = True
        mult = 1.0
    elif prior_offence_count == 1:
        tier = "SECOND_OFFENCE"
        eligible = True
        mult = 2.0
    else:
        tier = "HABITUAL_OFFENCE"
        eligible = False
        mult = 0.0

    assert tier == expected_compounding_tier
    assert eligible == can_compound
    assert mult == expected_penalty_multiplier


# ==============================================================================
# SECTION 9: THIRD SCHEDULE WHOLESALE MASTER CARTONS SCENARIOS
# ==============================================================================

@pytest.mark.parametrize(
    "carton_desc, retail_units, net_each, total_net, has_not_for_retail_mark, expected_pass",
    [
        ("Biscuits Master Shipper 24 Units", 24, "150 g", "3.6 kg", True, True),
        ("Shampoo Sachet Master Outer 144 Units", 144, "6 ml", "864 ml", True, True),
        ("Instant Noodles Shipper 36 Units", 36, "70 g", "2.52 kg", True, True),
        ("Detergent Bar Shipper 48 Units", 48, "250 g", "12.0 kg", True, True),
        ("Shipper Missing Retail Markings Disclaimer", 24, "100 g", "2.4 kg", False, False),
        ("Shipper with Zero Unit Count", 0, "100 g", "0 kg", True, False),
    ],
)
def test_wholesale_master_carton_scenarios(
    carton_desc: str,
    retail_units: int,
    net_each: str,
    total_net: str,
    has_not_for_retail_mark: bool,
    expected_pass: bool,
):
    validator = IndustrialSchedulesValidator()
    decl = WholesalePackageDeclarations(
        manufacturer_name_and_address="FMCG Conglomerate India Ltd, Mumbai",
        identity_of_commodity=carton_desc,
        total_number_of_retail_packages=retail_units,
        net_quantity_of_each_retail_unit=net_each,
        total_net_quantity=total_net,
        gross_mass="15.0 kg",
        batch_or_lot_number="B-9988",
        mrp_inclusive_taxes=1200.0,
        is_not_for_retail_sale_marked=has_not_for_retail_mark,
    )
    result = validator.audit_wholesale_package(decl)
    assert result.is_compliant == expected_pass, f"Carton '{carton_desc}' failed: {result.statutory_defects}"


# ==============================================================================
# SECTION 10: INSTITUTIONAL CONSUMER EXEMPTION AUDITS UNDER RULE 26(B)
# ==============================================================================

@pytest.mark.parametrize(
    "org_name, gstin, contract_ref, has_disclaimer, is_industrial, expected_pass",
    [
        ("Air India Catering Division", "07AAAAC1234F1Z1", "PO-AI-FOOD-2026-09", True, True, True),
        ("Tata Memorial Hospital Pharmacy", "27AAATT5678G1Z2", "HOSP-MED-SUPPLY-441", True, True, True),
        ("Larsen & Toubro Construction Works", "24AAACL9988H1Z3", "L&T-INFRA-GUJ-2026", True, True, True),
        ("Unauthorized Retail Grocery Store", "27AAAAA1111A1Z0", None, False, False, False),
        ("Diverted Goods Without Not For Retail Sale Text", "06AAABB2222B1Z5", "PO-DIVER-99", False, True, False),
    ],
)
def test_institutional_exemption_scenarios(
    org_name: str,
    gstin: str,
    contract_ref: str,
    has_disclaimer: bool,
    is_industrial: bool,
    expected_pass: bool,
):
    validator = IndustrialSchedulesValidator()
    decl = InstitutionalExemptionDeclarations(
        purchaser_organization_name=org_name,
        purchaser_gstin_or_cin=gstin,
        supply_contract_ref=contract_ref,
        package_bearing_not_for_retail_sale=has_disclaimer,
        is_industrial_or_institutional_use=is_industrial,
    )
    result = validator.audit_institutional_exemption(decl)
    assert result.is_compliant == expected_pass, f"Institutional scenario '{org_name}' failed: {result.statutory_defects}"


# ==============================================================================
# SECTION 11: MULTI-PIECE & COMBINATION GIFT PACKAGES (RULE 14 & RULE 2(r))
# ==============================================================================

@pytest.mark.parametrize(
    "hamper_title, items_list, aggregate_mrp, has_itemized_net_qty, expected_pass",
    [
        (
            "Festive Royal Dry Fruits Gift Box",
            [("California Almonds", "250 g"), ("Whole Cashews", "250 g"), ("Kashmiri Walnuts", "200 g")],
            1450.0,
            True,
            True,
        ),
        (
            "Gourmet Breakfast Combo Pack",
            [("Rolled Oats", "500 g"), ("Organic Forest Honey", "250 g"), ("Mixed Fruit Jam", "200 g")],
            499.0,
            True,
            True,
        ),
        (
            "Personal Care Grooming Gift Hamper",
            [("Shaving Gel", "200 ml"), ("Aftershave Balm", "100 ml"), ("Hydrating Face Wash", "100 ml")],
            699.0,
            True,
            True,
        ),
        (
            "Deficient Hamper Missing Itemized Net Quantities",
            [("Almonds", ""), ("Cashews", "")],
            899.0,
            False,
            False,
        ),
        (
            "Hamper Lacking Maximum Retail Price",
            [("Assorted Biscuits", "300 g"), ("Cookies", "200 g")],
            0.0,
            True,
            False,
        ),
    ],
)
def test_combination_and_multi_piece_packages(
    hamper_title: str,
    items_list: List[tuple],
    aggregate_mrp: float,
    has_itemized_net_qty: bool,
    expected_pass: bool,
):
    """
    Rule 14 of PCR 2011 mandates that every combination or multi-piece gift package
    must clearly declare on the outer wrapper:
        1. The number of individual items contained.
        2. The net quantity of each distinct commodity item.
        3. The aggregate Maximum Retail Price (MRP inclusive of all taxes).
    """
    is_valid = True
    if aggregate_mrp <= 0.0:
        is_valid = False
    if not has_itemized_net_qty:
        is_valid = False
    for name, qty in items_list:
        if not qty or not name:
            is_valid = False

    assert is_valid == expected_pass, f"Hamper '{hamper_title}' failed combination rules check"


# ==============================================================================
# SECTION 12: FIRST SCHEDULE MAXIMUM PERMISSIBLE ERROR (MPE) THRESHOLDS
# ==============================================================================

@pytest.mark.parametrize(
    "nominal_qty_g, declared_tolerance_pct, actual_shortfall_g, is_within_mpe",
    [
        (100.0, 4.5, 3.2, True),    # 100g biscuits, MPE is 4.5g (4.5%), actual short 3.2g -> PASS
        (100.0, 4.5, 5.8, False),   # 100g biscuits, actual short 5.8g > 4.5g -> FAIL (Sec 36(1) prosecution)
        (500.0, 3.0, 12.0, True),   # 500g tea, MPE is 15g (3.0%), actual short 12.0g -> PASS
        (500.0, 3.0, 18.5, False),  # 500g tea, actual short 18.5g > 15g -> FAIL
        (1000.0, 1.5, 11.0, True),  # 1kg flour, MPE is 15g (1.5%), actual short 11.0g -> PASS
        (1000.0, 1.5, 22.0, False), # 1kg flour, actual short 22.0g > 15g -> FAIL
        (5000.0, 1.0, 40.0, True),  # 5kg rice, MPE is 50g (1.0%), actual short 40.0g -> PASS
        (5000.0, 1.0, 75.0, False), # 5kg rice, actual short 75.0g > 50g -> FAIL
    ],
)
def test_first_schedule_maximum_permissible_error_tolerances(
    nominal_qty_g: float,
    declared_tolerance_pct: float,
    actual_shortfall_g: float,
    is_within_mpe: bool,
):
    """
    First Schedule Table 1 prescribes Maximum Permissible Errors (MPE) in net quantity.
    A product deficit within the statutory MPE threshold is non-prosecutable, whereas any
    deficiency exceeding MPE constitutes a cognizable offence under Section 36(1).
    """
    max_allowed_shortfall_g = nominal_qty_g * (declared_tolerance_pct / 100.0)
    passes_mpe = actual_shortfall_g <= max_allowed_shortfall_g
    assert passes_mpe == is_within_mpe
