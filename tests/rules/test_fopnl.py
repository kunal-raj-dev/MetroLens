"""
Tests for FSSAI Front-of-Pack Nutritional Labeling (FOPNL) & Dietary Display Checklist.
Verifies compliance under FSS (Labelling and Display) Regulations, 2020.
"""

import time
import pytest
from nirikshak_rules_engine.fopnl import (
    FOPNLValidator,
    NutritionalDeclaration,
    DietClassification,
    FoodClassification,
)


@pytest.fixture
def fopnl_validator():
    return FOPNLValidator()


def test_complete_compliant_food_nutrition(fopnl_validator):
    """Verifies a fully compliant packaged food product passes all checks."""
    decl = NutritionalDeclaration(
        energy_kcal=350.0,
        protein_g=8.0,
        carbohydrates_g=60.0,
        total_sugars_g=12.0,
        added_sugars_g=5.0,
        total_fat_g=10.0,
        saturated_fat_g=3.5,
        trans_fat_g=0.1,  # 1% of total fat (<= 2% limit)
        sodium_mg=300.0,
        serving_size="30g",
        per_serve_rda_declared=True,
        diet_symbol=DietClassification.VEGETARIAN,
        food_form=FoodClassification.SOLID,
    )

    records = fopnl_validator.evaluate(nutrition=decl)
    assert len(records) == 5

    # Check table completeness
    table_rec = next(r for r in records if r.rule_id == "FSSAI-R05-NUTRITION-TABLE")
    assert table_rec.is_compliant is True
    assert table_rec.status == "PASS"

    # Check trans fat
    trans_rec = next(r for r in records if r.rule_id == "FSSAI-R05-TRANSFAT-LIMIT")
    assert trans_rec.is_compliant is True
    assert trans_rec.status == "PASS"

    # Check veg logo
    veg_rec = next(r for r in records if r.rule_id == "FSSAI-R05-VEG-LOGO")
    assert veg_rec.is_compliant is True
    assert veg_rec.status == "PASS"

    # Check RDA
    rda_rec = next(r for r in records if r.rule_id == "FSSAI-R05-PER-SERVE-RDA")
    assert rda_rec.is_compliant is True
    assert rda_rec.status == "PASS"

    # Check HFSS
    hfss_rec = next(r for r in records if r.rule_id == "FSSAI-R05-HFSS-ALERT")
    assert hfss_rec.is_compliant is True
    assert hfss_rec.status == "PASS"


def test_missing_mandatory_nutrients(fopnl_validator):
    """Verifies missing energy and sodium flags non-compliance."""
    decl = NutritionalDeclaration(
        protein_g=5.0,
        carbohydrates_g=40.0,
        total_fat_g=5.0,
        diet_symbol=DietClassification.VEGETARIAN,
    )
    records = fopnl_validator.evaluate(nutrition=decl)
    table_rec = next(r for r in records if r.rule_id == "FSSAI-R05-NUTRITION-TABLE")
    assert table_rec.is_compliant is False
    assert table_rec.status == "FAIL"
    assert "Energy (kcal)" in table_rec.observed_value
    assert "Sodium (mg)" in table_rec.observed_value


def test_trans_fat_exceeds_two_percent(fopnl_validator):
    """Verifies trans fat > 2% of total fat is flagged as violation."""
    decl = NutritionalDeclaration(
        energy_kcal=400.0,
        protein_g=5.0,
        carbohydrates_g=50.0,
        total_fat_g=10.0,
        trans_fat_g=0.5,  # 5% of total fat (limit is 2%)
        sodium_mg=200.0,
        diet_symbol=DietClassification.VEGETARIAN,
    )
    records = fopnl_validator.evaluate(nutrition=decl)
    trans_rec = next(r for r in records if r.rule_id == "FSSAI-R05-TRANSFAT-LIMIT")
    assert trans_rec.is_compliant is False
    assert trans_rec.status == "FAIL"
    assert "5.0%" in trans_rec.observed_value


def test_missing_diet_symbol(fopnl_validator):
    """Verifies missing veg/non-veg logo is flagged."""
    decl = NutritionalDeclaration(
        energy_kcal=200.0,
        protein_g=4.0,
        carbohydrates_g=30.0,
        total_fat_g=2.0,
        sodium_mg=100.0,
        diet_symbol=DietClassification.UNKNOWN,
    )
    records = fopnl_validator.evaluate(nutrition=decl)
    veg_rec = next(r for r in records if r.rule_id == "FSSAI-R05-VEG-LOGO")
    assert veg_rec.is_compliant is False
    assert veg_rec.status == "FAIL"


def test_non_vegetarian_diet_symbol(fopnl_validator):
    """Verifies non-vegetarian diet symbol passes."""
    decl = NutritionalDeclaration(
        energy_kcal=250.0,
        protein_g=15.0,
        carbohydrates_g=10.0,
        total_fat_g=8.0,
        sodium_mg=400.0,
        diet_symbol=DietClassification.NON_VEGETARIAN,
    )
    records = fopnl_validator.evaluate(nutrition=decl)
    veg_rec = next(r for r in records if r.rule_id == "FSSAI-R05-VEG-LOGO")
    assert veg_rec.is_compliant is True
    assert veg_rec.status == "PASS"


def test_solid_food_hfss_alerts(fopnl_validator):
    """Verifies solid food exceeding saturated fat and sugar thresholds triggers HFSS warnings."""
    decl = NutritionalDeclaration(
        energy_kcal=500.0,
        protein_g=4.0,
        carbohydrates_g=65.0,
        total_sugars_g=35.0,     # > 21.0g solid limit
        total_fat_g=25.0,
        saturated_fat_g=12.0,    # > 6.0g solid limit
        sodium_mg=850.0,         # > 700mg solid limit
        food_form=FoodClassification.SOLID,
        diet_symbol=DietClassification.VEGETARIAN,
    )
    hfss = fopnl_validator.evaluate_hfss(decl)
    assert hfss.high_saturated_fat is True
    assert hfss.high_total_sugar is True
    assert hfss.high_sodium is True

    records = fopnl_validator.evaluate(nutrition=decl)
    hfss_rec = next(r for r in records if r.rule_id == "FSSAI-R05-HFSS-ALERT")
    assert hfss_rec.is_compliant is False
    assert hfss_rec.status == "REVIEW"
    assert "High Saturated Fat" in hfss_rec.observed_value
    assert "High Total Sugar" in hfss_rec.observed_value
    assert "High Sodium" in hfss_rec.observed_value


def test_liquid_food_hfss_thresholds(fopnl_validator):
    """Verifies liquid beverage sugar threshold (> 10g/100ml)."""
    decl = NutritionalDeclaration(
        energy_kcal=45.0,
        protein_g=0.0,
        carbohydrates_g=11.5,
        total_sugars_g=11.2,     # > 10.0g liquid limit
        total_fat_g=0.0,
        sodium_mg=20.0,
        food_form=FoodClassification.LIQUID,
        diet_symbol=DietClassification.VEGETARIAN,
    )
    hfss = fopnl_validator.evaluate_hfss(decl)
    assert hfss.high_total_sugar is True
    assert hfss.high_saturated_fat is False
    assert hfss.high_sodium is False


def test_null_nutrition_graceful_handling(fopnl_validator):
    """Verifies None nutrition returns NOT_APPLICABLE without exception."""
    records = fopnl_validator.evaluate(nutrition=None)
    assert len(records) == 1
    assert records[0].status == "NOT_APPLICABLE"


def test_fopnl_latency_sub_millisecond(fopnl_validator):
    """Verifies evaluation latency is strictly sub-millisecond."""
    decl = NutritionalDeclaration(
        energy_kcal=300.0,
        protein_g=10.0,
        carbohydrates_g=40.0,
        total_sugars_g=15.0,
        total_fat_g=8.0,
        saturated_fat_g=3.0,
        sodium_mg=250.0,
        diet_symbol=DietClassification.VEGETARIAN,
    )
    start = time.perf_counter()
    for _ in range(100):
        _ = fopnl_validator.evaluate(nutrition=decl)
    elapsed_total_ms = (time.perf_counter() - start) * 1000
    avg_ms = elapsed_total_ms / 100.0
    assert avg_ms < 0.5, f"FOPNL latency too high: {avg_ms:.4f}ms"
