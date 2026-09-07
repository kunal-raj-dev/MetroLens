"""
Nirikshak Rules Engine: FSSAI Front-of-Pack Nutritional Labeling (FOPNL) & Dietary Display Auditor.
Codifies preliminary checklist under the Food Safety and Standards (Labelling and Display)
Regulations, 2020, and draft Front-of-Pack Nutritional Labeling / Indian Nutrition Rating (INR) norms.
"""

from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from .schemas import RuleEvaluationRecord, CanonicalDeclaration


class FoodClassification(str, Enum):
    """Classification of food commodity for HFSS threshold determination."""
    SOLID = "solid"
    LIQUID = "liquid"


class DietClassification(str, Enum):
    """Vegetarian / Non-Vegetarian diet symbol indicator."""
    VEGETARIAN = "vegetarian"         # Green circle inside green square
    NON_VEGETARIAN = "non_vegetarian" # Brown triangle inside brown square
    UNKNOWN = "unknown"


class NutritionalDeclaration(BaseModel):
    """
    Mandatory nutritional declaration values per 100g / 100ml or per serve
    under Regulation 5(3) of FSS (Labelling and Display) Regulations, 2020.
    """
    energy_kcal: Optional[float] = Field(None, ge=0.0, description="Energy in kcal")
    protein_g: Optional[float] = Field(None, ge=0.0, description="Protein in grams")
    carbohydrates_g: Optional[float] = Field(None, ge=0.0, description="Carbohydrates in grams")
    total_sugars_g: Optional[float] = Field(None, ge=0.0, description="Total sugars in grams")
    added_sugars_g: Optional[float] = Field(None, ge=0.0, description="Added sugars in grams")
    total_fat_g: Optional[float] = Field(None, ge=0.0, description="Total fat in grams")
    saturated_fat_g: Optional[float] = Field(None, ge=0.0, description="Saturated fat in grams")
    trans_fat_g: Optional[float] = Field(None, ge=0.0, description="Trans fat in grams")
    sodium_mg: Optional[float] = Field(None, ge=0.0, description="Sodium in milligrams")
    serving_size: Optional[str] = Field(None, description="Declared serving size (e.g., '30g', '200ml')")
    per_serve_rda_declared: bool = Field(
        default=False, description="Whether per-serve % contribution to RDA is declared"
    )
    diet_symbol: DietClassification = Field(
        default=DietClassification.UNKNOWN, description="Detected Veg/Non-Veg logo"
    )
    food_form: FoodClassification = Field(
        default=FoodClassification.SOLID, description="Solid or liquid food form"
    )

    model_config = ConfigDict(extra="ignore")


class HFSSWarning(BaseModel):
    """High in Fat, Sugar, Salt warning indicators."""
    high_saturated_fat: bool = False
    high_total_sugar: bool = False
    high_sodium: bool = False
    warning_summary: str = ""


class FOPNLValidator:
    """
    Evaluates auxiliary food labeling standards under FSSAI regulations.
    Zero generative LLM dependencies, 100% deterministic arithmetic.
    """

    # Statutory HFSS Thresholds (per 100g for solid, per 100ml for liquid)
    SOLID_SAT_FAT_THRESHOLD_G = 6.0    # grams / 100g
    SOLID_SUGAR_THRESHOLD_G = 21.0     # grams / 100g
    SOLID_SODIUM_THRESHOLD_MG = 700.0  # mg / 100g

    LIQUID_SAT_FAT_THRESHOLD_G = 3.0   # grams / 100ml
    LIQUID_SUGAR_THRESHOLD_G = 10.0    # grams / 100ml
    LIQUID_SODIUM_THRESHOLD_MG = 350.0 # mg / 100ml

    def evaluate_hfss(self, nutrition: NutritionalDeclaration) -> HFSSWarning:
        """
        Determines whether the product exceeds High in Fat, Sugar, Salt (HFSS) thresholds.
        """
        is_liquid = nutrition.food_form == FoodClassification.LIQUID

        sat_fat_limit = self.LIQUID_SAT_FAT_THRESHOLD_G if is_liquid else self.SOLID_SAT_FAT_THRESHOLD_G
        sugar_limit = self.LIQUID_SUGAR_THRESHOLD_G if is_liquid else self.SOLID_SUGAR_THRESHOLD_G
        sodium_limit = self.LIQUID_SODIUM_THRESHOLD_MG if is_liquid else self.SOLID_SODIUM_THRESHOLD_MG

        high_sat_fat = (
            nutrition.saturated_fat_g is not None and nutrition.saturated_fat_g > sat_fat_limit
        )
        high_sugar = (
            nutrition.total_sugars_g is not None and nutrition.total_sugars_g > sugar_limit
        )
        high_sodium = (
            nutrition.sodium_mg is not None and nutrition.sodium_mg > sodium_limit
        )

        warnings = []
        if high_sat_fat:
            warnings.append(f"High Saturated Fat ({nutrition.saturated_fat_g}g > {sat_fat_limit}g)")
        if high_sugar:
            warnings.append(f"High Total Sugar ({nutrition.total_sugars_g}g > {sugar_limit}g)")
        if high_sodium:
            warnings.append(f"High Sodium ({nutrition.sodium_mg}mg > {sodium_limit}mg)")

        summary = "; ".join(warnings) if warnings else "Within standard nutritional thresholds."
        return HFSSWarning(
            high_saturated_fat=high_sat_fat,
            high_total_sugar=high_sugar,
            high_sodium=high_sodium,
            warning_summary=summary,
        )

    def evaluate(
        self,
        decl: Optional[CanonicalDeclaration] = None,
        nutrition: Optional[NutritionalDeclaration] = None,
    ) -> List[RuleEvaluationRecord]:
        """
        Evaluates food labeling declarations against FSSAI requirements:
        1. FSSAI-R05-NUTRITION-TABLE: Mandatory nutrient declarations presence
        2. FSSAI-R05-TRANSFAT-LIMIT: Trans-fat statutory limit (<= 2% total fat per FSSAI 2021)
        3. FSSAI-R05-VEG-LOGO: Veg / Non-Veg logo presence
        4. FSSAI-R05-PER-SERVE-RDA: Per-serve RDA contribution declaration
        5. FSSAI-R05-HFSS-ALERT: High Fat, Sugar, Salt profile
        """
        records: List[RuleEvaluationRecord] = []

        if nutrition is None:
            records.append(
                RuleEvaluationRecord(
                    rule_id="FSSAI-R05-NUTRITION-TABLE",
                    rule_title="Mandatory Nutritional Information Table",
                    statutory_reference="Regulation 5(3)",
                    status="NOT_APPLICABLE",
                    is_compliant=True,
                    observed_value="No nutritional declaration provided",
                    required_value="Mandatory for pre-packaged food commodities",
                    statutory_citation="FSS (Labelling and Display) Regulations, 2020, Regulation 5(3)",
                    notes="Nutritional analysis omitted or product is non-food.",
                )
            )
            return records

        # 1. Mandatory Core Nutrients Presence (Energy, Protein, Carbs, Sugars, Fats, Sodium)
        missing_nutrients = []
        if nutrition.energy_kcal is None:
            missing_nutrients.append("Energy (kcal)")
        if nutrition.protein_g is None:
            missing_nutrients.append("Protein (g)")
        if nutrition.carbohydrates_g is None:
            missing_nutrients.append("Carbohydrates (g)")
        if nutrition.total_sugars_g is None and nutrition.added_sugars_g is None:
            missing_nutrients.append("Sugars (g)")
        if nutrition.total_fat_g is None:
            missing_nutrients.append("Total Fat (g)")
        if nutrition.sodium_mg is None:
            missing_nutrients.append("Sodium (mg)")

        is_table_compliant = len(missing_nutrients) == 0
        records.append(
            RuleEvaluationRecord(
                rule_id="FSSAI-R05-NUTRITION-TABLE",
                rule_title="Mandatory Nutritional Information Completeness",
                statutory_reference="Regulation 5(3)",
                status="PASS" if is_table_compliant else "FAIL",
                is_compliant=is_table_compliant,
                observed_value="All core nutrients declared" if is_table_compliant else f"Missing: {', '.join(missing_nutrients)}",
                required_value="Energy, Protein, Carbohydrates, Total/Added Sugars, Total/Saturated/Trans Fat, Sodium",
                statutory_citation="FSS (Labelling and Display) Regulations, 2020, Regulation 5(3)",
                notes="Regulation 5(3) mandates declaration of energy, protein, carbohydrate, sugars, fats, and sodium per 100g/ml or per serve.",
            )
        )

        # 2. Trans-fat limit (FSSAI Gazette 2021 mandates <= 2% of total fat)
        if nutrition.trans_fat_g is not None and nutrition.total_fat_g is not None and nutrition.total_fat_g > 0:
            trans_pct = (nutrition.trans_fat_g / nutrition.total_fat_g) * 100.0
            is_trans_compliant = trans_pct <= 2.05  # 2% with minor floating tolerance
            records.append(
                RuleEvaluationRecord(
                    rule_id="FSSAI-R05-TRANSFAT-LIMIT",
                    rule_title="Trans-Fat Statutory Limit (<= 2% of Total Fat)",
                    statutory_reference="Regulation 5(3)(b)",
                    status="PASS" if is_trans_compliant else "FAIL",
                    is_compliant=is_trans_compliant,
                    observed_value=f"{round(trans_pct, 2)}% of total fat ({nutrition.trans_fat_g}g / {nutrition.total_fat_g}g)",
                    required_value="<= 2.0% of total dietary fats",
                    statutory_citation="FSS (Labelling and Display) Regulations, 2020, Regulation 5(3)(b) read with 2021 Gazette Amendment",
                    notes="Industrial trans fat is statutorily capped at <= 2% of total fats by weight.",
                )
            )

        # 3. Veg / Non-Veg Diet Symbol
        has_symbol = nutrition.diet_symbol in [DietClassification.VEGETARIAN, DietClassification.NON_VEGETARIAN]
        records.append(
            RuleEvaluationRecord(
                rule_id="FSSAI-R05-VEG-LOGO",
                rule_title="Vegetarian / Non-Vegetarian Logo",
                statutory_reference="Regulation 5(4)",
                status="PASS" if has_symbol else "FAIL",
                is_compliant=has_symbol,
                observed_value=nutrition.diet_symbol.value if has_symbol else "No diet indicator symbol detected",
                required_value="Green filled circle (Veg) or Brown filled triangle (Non-Veg)",
                statutory_citation="FSS (Labelling and Display) Regulations, 2020, Regulation 5(4)",
                notes="Every pre-packaged food must display Vegetarian or Non-Vegetarian logo prominently.",
            )
        )

        # 4. Per-serve % contribution to RDA
        records.append(
            RuleEvaluationRecord(
                rule_id="FSSAI-R05-PER-SERVE-RDA",
                rule_title="Per-Serve % Contribution to RDA Declaration",
                statutory_reference="Regulation 5(3)(c)",
                status="PASS" if nutrition.per_serve_rda_declared else "REVIEW",
                is_compliant=nutrition.per_serve_rda_declared,
                observed_value="Declared" if nutrition.per_serve_rda_declared else "Not detected or omitted",
                required_value="Percentage contribution to Recommended Dietary Allowance (RDA) per serving",
                statutory_citation="FSS (Labelling and Display) Regulations, 2020, Regulation 5(3)(c)",
                notes="Per-serve RDA percentage enables consumer dietary assessment based on standard 2000 kcal intake.",
            )
        )

        # 5. HFSS Profile Check
        hfss = self.evaluate_hfss(nutrition)
        has_hfss_alert = hfss.high_saturated_fat or hfss.high_total_sugar or hfss.high_sodium
        records.append(
            RuleEvaluationRecord(
                rule_id="FSSAI-R05-HFSS-ALERT",
                rule_title="High in Fat, Sugar, Salt (HFSS) Threshold Audit",
                statutory_reference="FOPNL Draft Regulations / INR Guidelines",
                status="REVIEW" if has_hfss_alert else "PASS",
                is_compliant=not has_hfss_alert,
                observed_value=hfss.warning_summary,
                required_value=f"Solid: SatFat<={self.SOLID_SAT_FAT_THRESHOLD_G}g, Sugar<={self.SOLID_SUGAR_THRESHOLD_G}g, Sodium<={self.SOLID_SODIUM_THRESHOLD_MG}mg per 100g",
                statutory_citation="Draft Food Safety and Standards (Labelling and Display) Amendment Regulations (FOPNL)",
                notes="Advisory front-of-pack nutritional warning indicator." if has_hfss_alert else "Nutrient levels are within standard dietary thresholds.",
            )
        )

        return records
