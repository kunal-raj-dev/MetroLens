"""
Nirikshak Rules Engine: Canonical 25-Case Statutory Regression Test Suite.
Verifies Gate 5 & Gate 7 compliance across all codified statutory clauses:
- Rule 3 (Wholesale exclusions and cement/fertilizer exception)
- Rule 6(1)(a)-(g) (Mandatory declarations completeness & Rule 13 SI unit compliance)
- Rule 6(11) (Unit Sale Price denominators, provisos a, b, c, and decimal arithmetic)
- Rule 7 (Tables I & II numeral font heights, 0.10mm benefit-of-doubt buffer, uncertainty band)
- Rule 26(a) (Small pack exemptions and G.S.R. 881(E) Pan Masala / Tobacco revocation)
- Section 36(1) (Jan Vishwas Act 2026 15-day Improvement Notice generation)
"""

import pytest
from nirikshak_rules_engine import (
    StatutoryRuleEngine,
    CanonicalDeclaration,
    MetricScaleResult,
    UnitType,
    ComplianceState,
)


@pytest.fixture
def engine():
    return StatutoryRuleEngine()


# ---------------------------------------------------------------------------
# Case 01: Standard Compliant FMCG Retail Pouch (Cashews, 200g)
# ---------------------------------------------------------------------------
def test_case_01_standard_compliant_fmcg(engine):
    """Case 01: Full retail compliance across all 8 mandatory declarations and Rule 7 font height."""
    decl = CanonicalDeclaration(
        commodity_name="Premium Roasted Cashews",
        manufacturer_name="MetroLens Foods Pvt Ltd, Okhla Phase-III, New Delhi 110020",
        manufacturer_pincode="110020",
        country_of_origin="India",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=8,
        mfg_year=2026,
        mrp_inr=240.0,
        tax_qualifier_present=True,
        consumer_care_email="care@metrolens.in",
        consumer_care_phone="1800-11-4000",
        declared_usp_value=1.20,
        declared_usp_unit="g",
    )
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)
    res = engine.evaluate(decl, scale=scale, measured_font_height_mm=1.65, inspection_id="CASE-01")

    assert res.overall_verdict == ComplianceState.COMPLIANT
    assert res.verdict_badge_color == "green"
    assert res.improvement_notice.recommended is False


# ---------------------------------------------------------------------------
# Case 02: Bilingual Devanagari Hindi Retail Package (Atta, 1kg)
# ---------------------------------------------------------------------------
def test_case_02_bilingual_devanagari_hindi(engine):
    """Case 02: Bilingual package declared in Devanagari Hindi satisfying all statutory clauses."""
    decl = CanonicalDeclaration(
        commodity_name="चक्की ताजा आटा",
        manufacturer_name="किसान फूड्स लिमिटेड, जयपुर 302013",
        manufacturer_pincode="302013",
        country_of_origin="India",
        net_quantity_value=1.0,
        net_quantity_unit=UnitType.KILOGRAM,
        mfg_month=5,
        mfg_year=2026,
        mrp_inr=45.0,
        tax_qualifier_present=True,
        consumer_care_email="support@kisanfoods.in",
        consumer_care_phone="1800-200-5555",
        declared_usp_value=45.0,
        declared_usp_unit="kg",
    )
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=250.0)
    res = engine.evaluate(decl, scale=scale, measured_font_height_mm=2.60, inspection_id="CASE-02")

    assert res.overall_verdict == ComplianceState.COMPLIANT
    assert res.verdict_badge_color == "green"


# ---------------------------------------------------------------------------
# Case 03: Rule 6(1)(a) Missing Manufacturer Name & Address
# ---------------------------------------------------------------------------
def test_case_03_missing_manufacturer(engine):
    """Case 03: Violation of Rule 6(1)(a) when manufacturer details are omitted."""
    decl = CanonicalDeclaration(
        commodity_name="Biscuits",
        manufacturer_name=None,  # VIOLATION
        country_of_origin="India",
        net_quantity_value=100.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=8,
        mfg_year=2026,
        mrp_inr=30.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-22-3344",
        declared_usp_value=0.30,
        declared_usp_unit="g",
    )
    res = engine.evaluate(decl, inspection_id="CASE-03")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    mfr_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-MFR-001")
    assert mfr_eval.is_compliant is False


# ---------------------------------------------------------------------------
# Case 04: Rule 6(1)(aa) Missing Country of Origin
# ---------------------------------------------------------------------------
def test_case_04_missing_country_of_origin(engine):
    """Case 04: Violation of Rule 6(1)(aa) (G.S.R. 629(E)) when Country of Origin is omitted."""
    decl = CanonicalDeclaration(
        commodity_name="Dark Chocolate",
        manufacturer_name="ChocoCraft Ltd",
        country_of_origin=None,  # VIOLATION
        net_quantity_value=80.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=6,
        mfg_year=2026,
        mrp_inr=120.0,
        tax_qualifier_present=True,
        consumer_care_email="help@chococraft.in",
        declared_usp_value=1.50,
        declared_usp_unit="g",
    )
    res = engine.evaluate(decl, inspection_id="CASE-04")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    coo_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-COO-001")
    assert coo_eval.is_compliant is False


# ---------------------------------------------------------------------------
# Case 05: Rule 6(1)(b) Missing Commodity Generic Name
# ---------------------------------------------------------------------------
def test_case_05_missing_commodity_name(engine):
    """Case 05: Violation of Rule 6(1)(b) when common or generic commodity name is absent."""
    decl = CanonicalDeclaration(
        commodity_name=None,  # VIOLATION
        manufacturer_name="BeverageWorld Ltd",
        country_of_origin="India",
        net_quantity_value=500.0,
        net_quantity_unit=UnitType.MILLILITER,
        mfg_month=7,
        mfg_year=2026,
        mrp_inr=40.0,
        tax_qualifier_present=True,
        consumer_care_email="care@bevworld.com",
        declared_usp_value=0.08,
        declared_usp_unit="ml",
    )
    res = engine.evaluate(decl, inspection_id="CASE-05")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    name_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-NAME-001")
    assert name_eval.is_compliant is False


# ---------------------------------------------------------------------------
# Case 06: Rule 6(1)(c) Missing Net Quantity
# ---------------------------------------------------------------------------
def test_case_06_missing_net_quantity(engine):
    """Case 06: Violation of Rule 6(1)(c) when net quantity declaration is absent."""
    decl = CanonicalDeclaration(
        commodity_name="Hand Wash",
        manufacturer_name="CleanCare Ltd",
        country_of_origin="India",
        net_quantity_value=None,  # VIOLATION
        net_quantity_unit=None,
        mfg_month=4,
        mfg_year=2026,
        mrp_inr=99.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-11-9988",
    )
    res = engine.evaluate(decl, inspection_id="CASE-06")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    qty_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-QTY-001")
    assert qty_eval.is_compliant is False


# ---------------------------------------------------------------------------
# Case 07: Rule 6(1)(c) read with Rule 13: Prohibited "Gms" Unit Symbol
# ---------------------------------------------------------------------------
def test_case_07_prohibited_unit_gms(engine):
    """Case 07: Violation of Rule 13 when prohibited non-standard unit 'Gms' is used."""
    decl = CanonicalDeclaration(
        commodity_name="Turmeric Powder",
        manufacturer_name="SpiceWorld Ltd",
        country_of_origin="India",
        net_quantity_value=500.0,
        net_quantity_unit=UnitType.GRAM,
        raw_net_quantity_unit="Gms",
        has_non_standard_unit=True,  # VIOLATION
        mfg_month=7,
        mfg_year=2026,
        mrp_inr=150.0,
        tax_qualifier_present=True,
        consumer_care_email="care@spiceworld.in",
        declared_usp_value=0.30,
        declared_usp_unit="g",
    )
    res = engine.evaluate(decl, inspection_id="CASE-07")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    qty_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-QTY-001")
    assert qty_eval.is_compliant is False
    assert "Rule 13" in qty_eval.statutory_reference


# ---------------------------------------------------------------------------
# Case 08: Rule 6(1)(c) read with Rule 13: Prohibited "ML" Unit Symbol
# ---------------------------------------------------------------------------
def test_case_08_prohibited_unit_capital_ml(engine):
    """Case 08: Violation of Rule 13 when non-standard capital 'ML' is used."""
    decl = CanonicalDeclaration(
        commodity_name="Mineral Water",
        manufacturer_name="AquaPure Ltd",
        country_of_origin="India",
        net_quantity_value=750.0,
        net_quantity_unit=UnitType.MILLILITER,
        raw_net_quantity_unit="ML",
        has_non_standard_unit=True,  # VIOLATION
        mfg_month=7,
        mfg_year=2026,
        mrp_inr=30.0,
        tax_qualifier_present=True,
        consumer_care_email="help@aquapure.com",
        declared_usp_value=0.04,
        declared_usp_unit="ml",
    )
    res = engine.evaluate(decl, inspection_id="CASE-08")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT


# ---------------------------------------------------------------------------
# Case 09: Rule 6(1)(d) Missing Manufacturing Month & Year
# ---------------------------------------------------------------------------
def test_case_09_missing_mfg_date(engine):
    """Case 09: Violation of Rule 6(1)(d) when manufacturing date is omitted."""
    decl = CanonicalDeclaration(
        commodity_name="Green Tea",
        manufacturer_name="TeaEstate Ltd",
        country_of_origin="India",
        net_quantity_value=100.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=None,  # VIOLATION
        mfg_year=None,
        mrp_inr=250.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-44-5566",
        declared_usp_value=2.50,
        declared_usp_unit="g",
    )
    res = engine.evaluate(decl, inspection_id="CASE-09")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    date_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-DATE-001")
    assert date_eval.is_compliant is False


# ---------------------------------------------------------------------------
# Case 10: Rule 6(1)(e) Missing Maximum Retail Price (MRP)
# ---------------------------------------------------------------------------
def test_case_10_missing_mrp(engine):
    """Case 10: Violation of Rule 6(1)(e) when MRP numeric value is missing entirely."""
    decl = CanonicalDeclaration(
        commodity_name="Basmati Rice",
        manufacturer_name="GrainCorp Ltd",
        country_of_origin="India",
        net_quantity_value=1.0,
        net_quantity_unit=UnitType.KILOGRAM,
        mfg_month=6,
        mfg_year=2026,
        mrp_inr=None,  # VIOLATION
        tax_qualifier_present=False,
        consumer_care_email="care@graincorp.in",
    )
    res = engine.evaluate(decl, inspection_id="CASE-10")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    mrp_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-MRP-001")
    assert mrp_eval.is_compliant is False


# ---------------------------------------------------------------------------
# Case 11: Rule 6(1)(e) MRP Missing Mandatory Tax Qualifier
# ---------------------------------------------------------------------------
def test_case_11_mrp_missing_tax_qualifier(engine):
    """Case 11: Violation of Rule 6(1)(e) when 'inclusive of all taxes' is missing."""
    decl = CanonicalDeclaration(
        commodity_name="Potato Chips",
        manufacturer_name="SnackCo Ltd",
        country_of_origin="India",
        net_quantity_value=50.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=5,
        mfg_year=2026,
        mrp_inr=20.0,
        tax_qualifier_present=False,  # VIOLATION
        consumer_care_phone="1800-00-1111",
        declared_usp_value=0.40,
        declared_usp_unit="g",
    )
    res = engine.evaluate(decl, inspection_id="CASE-11")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    mrp_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-MRP-001")
    assert mrp_eval.is_compliant is False
    assert "tax qualifier" in mrp_eval.notes.lower()


# ---------------------------------------------------------------------------
# Case 12: Rule 6(1)(g) Missing Consumer Care Redressal Contacts
# ---------------------------------------------------------------------------
def test_case_12_missing_consumer_care(engine):
    """Case 12: Violation of Rule 6(1)(g) when consumer grievance redressal is absent."""
    decl = CanonicalDeclaration(
        commodity_name="Coffee Beans",
        manufacturer_name="RoastCo Ltd",
        country_of_origin="India",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=8,
        mfg_year=2026,
        mrp_inr=450.0,
        tax_qualifier_present=True,
        consumer_care_phone=None,  # VIOLATION
        consumer_care_email=None,  # VIOLATION
        declared_usp_value=2.25,
        declared_usp_unit="g",
    )
    res = engine.evaluate(decl, inspection_id="CASE-12")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    care_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-CARE-001")
    assert care_eval.is_compliant is False


# ---------------------------------------------------------------------------
# Case 13: Rule 6(11) Unit Sale Price Missing on Package > 10g
# ---------------------------------------------------------------------------
def test_case_13_missing_unit_sale_price(engine):
    """Case 13: Violation of Rule 6(11) when USP is omitted on package > 10g."""
    decl = CanonicalDeclaration(
        commodity_name="Oats",
        manufacturer_name="HealthFoods Ltd",
        country_of_origin="India",
        net_quantity_value=500.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=7,
        mfg_year=2026,
        mrp_inr=150.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-55-6677",
        declared_usp_value=None,  # VIOLATION: Missing USP
        declared_usp_unit=None,
    )
    res = engine.evaluate(decl, inspection_id="CASE-13")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    usp_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-USP-001")
    assert usp_eval.is_compliant is False


# ---------------------------------------------------------------------------
# Case 14: Rule 6(11) Prohibited "per 100g" Denominator
# ---------------------------------------------------------------------------
def test_case_14_prohibited_per_100g_usp(engine):
    """Case 14: Violation of G.S.R. 226(E) when obsolete 'per 100g' denominator is used."""
    decl = CanonicalDeclaration(
        commodity_name="Breakfast Cereal",
        manufacturer_name="CrunchyGrains Ltd",
        country_of_origin="India",
        net_quantity_value=400.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=6,
        mfg_year=2026,
        mrp_inr=160.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-44-3322",
        declared_usp_value=40.0,
        declared_usp_unit="100g",  # PROHIBITED DENOMINATOR
    )
    res = engine.evaluate(decl, inspection_id="CASE-14")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    usp_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-USP-001")
    assert usp_eval.is_compliant is False
    assert "prohibited" in usp_eval.notes.lower()


# ---------------------------------------------------------------------------
# Case 15: Rule 6(11) Incorrect Denominator (Declared per kg on < 1kg)
# ---------------------------------------------------------------------------
def test_case_15_incorrect_usp_denominator(engine):
    """Case 15: Violation of Rule 6(11)(i) when USP is declared per kg on package < 1kg."""
    decl = CanonicalDeclaration(
        commodity_name="Almonds",
        manufacturer_name="NutriBite Ltd",
        country_of_origin="India",
        net_quantity_value=500.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=8,
        mfg_year=2026,
        mrp_inr=400.0,
        tax_qualifier_present=True,
        consumer_care_email="care@nutribite.in",
        declared_usp_value=800.0,
        declared_usp_unit="kg",  # VIOLATION: Must be per gram for < 1kg
    )
    res = engine.evaluate(decl, inspection_id="CASE-15")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    usp_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-USP-001")
    assert usp_eval.is_compliant is False


# ---------------------------------------------------------------------------
# Case 16: Rule 6(11) Unit Sale Price Arithmetic Mismatch > 1%
# ---------------------------------------------------------------------------
def test_case_16_usp_arithmetic_mismatch(engine):
    """Case 16: Arithmetic mismatch where declared USP deviates by > 1% from expected."""
    decl = CanonicalDeclaration(
        commodity_name="Cashews",
        manufacturer_name="DryFruit Hub Ltd",
        country_of_origin="India",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=240.0,            # Expected = ₹1.20 / g
        tax_qualifier_present=True,
        consumer_care_phone="1800-11-2233",
        declared_usp_value=1.80,  # VIOLATION: Mismatch of ₹0.60
        declared_usp_unit="g",
    )
    res = engine.evaluate(decl, inspection_id="CASE-16")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    usp_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-USP-001")
    assert usp_eval.is_compliant is False
    assert "arithmetic mismatch" in usp_eval.notes.lower()


# ---------------------------------------------------------------------------
# Case 17: Rule 6(11) Proviso (c) Exemption: MRP equals USP
# ---------------------------------------------------------------------------
def test_case_17_usp_exemption_mrp_equals_usp(engine):
    """Case 17: Under Rule 6(11) proviso (c), package where MRP equals USP is exempt from USP declaration."""
    decl = CanonicalDeclaration(
        commodity_name="Wheat Flour",
        manufacturer_name="GrainMill Ltd",
        country_of_origin="India",
        net_quantity_value=1.0,
        net_quantity_unit=UnitType.KILOGRAM,
        mfg_month=8,
        mfg_year=2026,
        mrp_inr=50.0,             # Expected USP = ₹50/kg == MRP
        tax_qualifier_present=True,
        consumer_care_phone="1800-11-0011",
        declared_usp_value=None,  # Exempt from declaring
        declared_usp_unit=None,
    )
    res = engine.evaluate(decl, inspection_id="CASE-17")
    assert res.overall_verdict == ComplianceState.COMPLIANT
    usp_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R06-USP-001")
    assert usp_eval.is_compliant is True
    assert "proviso (c)" in usp_eval.notes.lower()


# ---------------------------------------------------------------------------
# Case 18: Rule 6(11) Proviso (a) Exemption: Net Quantity < 10g
# ---------------------------------------------------------------------------
def test_case_18_usp_exemption_small_pack(engine):
    """Case 18: Net quantity < 10g is exempt from separate USP declaration under Rule 6(11) proviso (a)."""
    decl = CanonicalDeclaration(
        commodity_name="Cardamom Powder",
        manufacturer_name="SpiceWorld Ltd",
        country_of_origin="India",
        net_quantity_value=5.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=8,
        mfg_year=2026,
        mrp_inr=25.0,
        tax_qualifier_present=True,
        consumer_care_email="care@spiceworld.in",
        declared_usp_value=None,
    )
    rec = engine.usp_validator.evaluate(decl)
    assert rec.status == "NOT_APPLICABLE"
    assert rec.is_compliant is True


# ---------------------------------------------------------------------------
# Case 19: Rule 3 Wholesale Bulk Exclusion (> 25kg)
# ---------------------------------------------------------------------------
def test_case_19_wholesale_bulk_exclusion(engine):
    """Case 19: Package > 25kg marked for wholesale is excluded from retail declarations under Rule 3."""
    decl = CanonicalDeclaration(
        commodity_name="Industrial Raw Sugar",
        is_wholesale_or_bulk=True,
        net_quantity_value=50.0,
        net_quantity_unit=UnitType.KILOGRAM,
        mrp_inr=3000.0,
    )
    res = engine.evaluate(decl, inspection_id="CASE-19")
    assert res.overall_verdict == ComplianceState.EXEMPTED
    assert res.verdict_badge_color == "blue"


# ---------------------------------------------------------------------------
# Case 20: Rule 3 Cement / Fertilizer Wholesale Exception (50kg Bag)
# ---------------------------------------------------------------------------
def test_case_20_cement_fertilizer_rule_3_exception(engine):
    """Case 20: Cement bags up to 50kg are statutorily NOT excluded by Rule 3 wholesale exemption."""
    decl = CanonicalDeclaration(
        commodity_name="Portland Pozzolana Cement",
        manufacturer_name="UltraBuild Cement Ltd, Mumbai 400001",
        country_of_origin="India",
        net_quantity_value=50.0,
        net_quantity_unit=UnitType.KILOGRAM,
        is_wholesale_or_bulk=True,  # Would normally be exempt, but cement up to 50kg is governed!
        mfg_month=8,
        mfg_year=2026,
        mrp_inr=420.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-22-9900",
        declared_usp_value=8.40,
        declared_usp_unit="kg",
    )
    res = engine.evaluate(decl, inspection_id="CASE-20")
    # Cement is NOT excluded -> evaluated under Chapter II retail rules -> COMPLIANT
    assert res.overall_verdict == ComplianceState.COMPLIANT


# ---------------------------------------------------------------------------
# Case 21: Rule 26(a) Small Pack Exemption (<= 10g General Commodity)
# ---------------------------------------------------------------------------
def test_case_21_rule_26_small_pack_exemption(engine):
    """Case 21: Miniature package <= 10g (e.g. hotel soap) is exempt from Chapter II declarations."""
    decl = CanonicalDeclaration(
        commodity_name="Guest Luxury Soap",
        manufacturer_name=None,  # Missing, but package is exempt!
        net_quantity_value=8.0,
        net_quantity_unit=UnitType.GRAM,
        is_pan_masala_or_tobacco=False,
    )
    res = engine.evaluate(decl, inspection_id="CASE-21")
    assert res.overall_verdict == ComplianceState.EXEMPTED
    assert res.verdict_badge_color == "blue"


# ---------------------------------------------------------------------------
# Case 22: G.S.R. 881(E) Pan Masala Miniature Sachet Strictly Non-Exempt
# ---------------------------------------------------------------------------
def test_case_22_gsr_881e_pan_masala_non_exemption(engine):
    """Case 22: Pan masala sachet <= 10g is strictly NON-EXEMPT under G.S.R. 881(E); all declarations required."""
    decl = CanonicalDeclaration(
        commodity_name="Royal Pan Masala",
        manufacturer_name="Royal Products Ltd, Kanpur 208001",
        country_of_origin="India",
        net_quantity_value=4.0,
        net_quantity_unit=UnitType.GRAM,
        is_pan_masala_or_tobacco=True,  # NON-EXEMPT
        mfg_month=8,
        mfg_year=2026,
        mrp_inr=5.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-44-1122",
    )
    res = engine.evaluate(decl, inspection_id="CASE-22")
    # Must NOT be exempt; must evaluate declarations
    assert res.overall_verdict == ComplianceState.COMPLIANT
    gsr_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R26-GSR881E-CARVEOUT")
    assert gsr_eval.is_compliant is True


# ---------------------------------------------------------------------------
# Case 23: Rule 7 Table-I Font Height Severe Deficit
# ---------------------------------------------------------------------------
def test_case_23_rule_7_font_height_deficit(engine):
    """Case 23: Font height deficit exceeding 0.10mm benefit-of-doubt buffer triggers NON_COMPLIANT."""
    decl = CanonicalDeclaration(
        commodity_name="Biscuits",
        manufacturer_name="BakeWorld Ltd",
        country_of_origin="India",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=40.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-11-2233",
        declared_usp_value=0.20,
        declared_usp_unit="g",
    )
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)
    # Threshold for 80 cm² is 1.5mm. Measured is 0.80mm (deficit 0.70mm).
    res = engine.evaluate(decl, scale=scale, measured_font_height_mm=0.80, inspection_id="CASE-23")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    font_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R07-FONT-001")
    assert font_eval.is_compliant is False
    assert font_eval.deficit_mm == 0.70


# ---------------------------------------------------------------------------
# Case 24: Rule 7 Table-I Benefit-of-Doubt Buffer Applied
# ---------------------------------------------------------------------------
def test_case_24_rule_7_benefit_of_doubt_applied(engine):
    """Case 24: Measured numeral height marginally under threshold passes via 0.10mm benefit-of-doubt buffer."""
    decl = CanonicalDeclaration(
        commodity_name="Biscuits",
        manufacturer_name="BakeWorld Ltd",
        country_of_origin="India",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=40.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-11-2233",
        declared_usp_value=0.20,
        declared_usp_unit="g",
    )
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)
    # Threshold is 1.5mm. Measured is 1.42mm (1.42 + 0.10 = 1.52 >= 1.50)
    res = engine.evaluate(decl, scale=scale, measured_font_height_mm=1.42, inspection_id="CASE-24")
    assert res.overall_verdict == ComplianceState.COMPLIANT
    font_eval = next(r for r in res.rule_evaluations if r.rule_id == "LMPC-R07-FONT-001")
    assert font_eval.is_compliant is True
    assert font_eval.benefit_of_doubt_applied is True


# ---------------------------------------------------------------------------
# Case 25: Rule 7 Borderline Deficit within Optical Uncertainty Band
# ---------------------------------------------------------------------------
def test_case_25_rule_7_borderline_uncertainty(engine):
    """Case 25: Borderline measurement deficit within 0.25mm uncertainty band yields DEVIATION_DETECTED."""
    decl = CanonicalDeclaration(
        commodity_name="Biscuits",
        manufacturer_name="BakeWorld Ltd",
        country_of_origin="India",
        net_quantity_value=200.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=40.0,
        tax_qualifier_present=True,
        consumer_care_phone="1800-11-2233",
        declared_usp_value=0.20,
        declared_usp_unit="g",
    )
    scale = MetricScaleResult(is_calibrated=True, scale_factor_mm_per_px=0.05, pdp_area_sqcm=80.0)
    # Threshold is 1.5mm. Measured is 1.30mm (deficit 0.20mm, within 0.25mm uncertainty)
    res = engine.evaluate(decl, scale=scale, measured_font_height_mm=1.30, inspection_id="CASE-25")
    assert res.overall_verdict == ComplianceState.DEVIATION_DETECTED
    assert res.verdict_badge_color == "amber"
