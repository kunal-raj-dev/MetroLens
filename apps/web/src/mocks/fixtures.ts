/**
 * MetroLens AI™ - Synthetic Regression Fixtures
 * Subsystem: Member 5 (Web Frontend)
 * 
 * IMPORTANT COMPLIANCE NOTICE:
 * These fixtures are strictly SYNTHETIC REGRESSION & DEMO ASSETS modeled after
 * data/synthetic/regression/manifest.json. They are NEVER to be represented as
 * real-world retail field inspection validation data.
 */

import { BackendInspectionDTO } from "@/types/contract";

export interface SyntheticFixtureDefinition {
  id: string;
  title: string;
  packageType: string;
  language: string;
  disclaimer: string;
  data: BackendInspectionDTO;
}

export const SYNTHETIC_FIXTURES: Record<string, SyntheticFixtureDefinition> = {
  "SYNTH-01-ENG-FMCG": {
    id: "SYNTH-01-ENG-FMCG",
    title: "Standard English Biscuit Packaging",
    packageType: "biscuit_pouch",
    language: "en",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
    data: {
      inspection_id: "INSP-SYNTH-01-ENG",
      status: "SUCCESS",
      image_sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      overall_verdict: "COMPLIANT",
      quality_gate_passed: true,
      calibration_status: "CALIBRATED",
      declarations: {
        mrp: {
          field_name: "mrp",
          raw_text: "MRP Rs 20.00 (INCL. OF ALL TAXES)",
          normalized_value: 20.0,
          confidence: 0.985,
          source_token_ids: ["tok_005"],
          bounding_box: { x_min: 28.96, y_min: 72.57, x_max: 499.04, y_max: 102.31 },
          is_mandatory: true,
          is_present: true,
        },
        net_quantity: {
          field_name: "net_quantity",
          raw_text: "Net Qty: 65 g",
          normalized_value: { value: 65, unit: "g" },
          confidence: 0.978,
          source_token_ids: ["tok_004"],
          bounding_box: { x_min: 26.8, y_min: 114.35, x_max: 161.2, y_max: 142.35 },
          is_mandatory: true,
          is_present: true,
        },
        unit_sale_price: {
          field_name: "unit_sale_price",
          raw_text: "Unit Sale Price: Rs. 0.31 / g",
          normalized_value: { price: 0.31, unit: "g" },
          confidence: 0.964,
          source_token_ids: ["tok_003"],
          bounding_box: { x_min: 26.86, y_min: 156.34, x_max: 301.14, y_max: 188.32 },
          is_mandatory: true,
          is_present: true,
        },
        date_of_mfg: {
          field_name: "date_of_mfg",
          raw_text: "Mfg Date: 08/2026",
          normalized_value: "2026-08",
          confidence: 0.991,
          source_token_ids: ["tok_002"],
          bounding_box: { x_min: 26.89, y_min: 203.42, x_max: 211.11, y_max: 232.27 },
          is_mandatory: true,
          is_present: true,
        },
        consumer_care: {
          field_name: "consumer_care",
          raw_text: "Consumer Care: 1800-222-4444",
          normalized_value: "18002224444",
          confidence: 0.972,
          source_token_ids: ["tok_001"],
          bounding_box: { x_min: 29.0, y_min: 249.55, x_max: 392.0, y_max: 270.0 },
          is_mandatory: true,
          is_present: true,
        },
      },
      ocr_observations: [
        {
          token_id: "tok_006",
          text: "SYNTHETIC TEST NOT REAL PACKAGING",
          confidence: 0.8426,
          bounding_box: { x_min: 30.0, y_min: 25.57, x_max: 364.0, y_max: 42.95 },
          polygon: [
            [30.0, 25.57],
            [364.0, 25.57],
            [364.0, 42.95],
            [30.0, 42.95],
          ],
          language: "en",
        },
        {
          token_id: "tok_005",
          text: "MRP Rs 20.00 (INCL. OF ALL TAXES)",
          confidence: 0.985,
          bounding_box: { x_min: 28.96, y_min: 72.57, x_max: 499.04, y_max: 102.31 },
          polygon: [
            [28.96, 72.57],
            [499.04, 72.57],
            [499.04, 102.31],
            [28.96, 102.31],
          ],
          language: "en",
        },
        {
          token_id: "tok_004",
          text: "Net Qty: 65 g",
          confidence: 0.978,
          bounding_box: { x_min: 26.8, y_min: 114.35, x_max: 161.2, y_max: 142.35 },
          polygon: [
            [26.8, 114.35],
            [161.2, 114.35],
            [161.2, 142.35],
            [26.8, 142.35],
          ],
          language: "en",
        },
        {
          token_id: "tok_003",
          text: "Unit Sale Price: Rs. 0.31 / g",
          confidence: 0.9642,
          bounding_box: { x_min: 26.86, y_min: 156.34, x_max: 301.14, y_max: 188.32 },
          polygon: [
            [26.86, 156.34],
            [301.14, 156.34],
            [301.14, 188.32],
            [26.86, 188.32],
          ],
          language: "en",
        },
        {
          token_id: "tok_002",
          text: "Mfg Date: 08/2026",
          confidence: 0.991,
          bounding_box: { x_min: 26.89, y_min: 203.42, x_max: 211.11, y_max: 232.27 },
          polygon: [
            [26.89, 203.42],
            [211.11, 203.42],
            [211.11, 232.27],
            [26.89, 232.27],
          ],
          language: "en",
        },
        {
          token_id: "tok_001",
          text: "Consumer Care: 1800-222-4444",
          confidence: 0.972,
          bounding_box: { x_min: 29.0, y_min: 249.55, x_max: 392.0, y_max: 270.0 },
          polygon: [
            [29.0, 249.55],
            [392.0, 249.55],
            [392.0, 270.0],
            [29.0, 270.0],
          ],
          language: "en",
        },
      ],
      measurements: {
        net_quantity_numeral_height: {
          feature_name: "net_quantity_numeral_height",
          measured_pixels: 24.5,
          scale_factor_mm_per_pixel: 0.088,
          measured_mm: 2.15,
          uncertainty_mm: 0.12,
          calibration_status: "CALIBRATED",
          bounding_box: { x_min: 26.8, y_min: 114.35, x_max: 161.2, y_max: 142.35 },
        },
      },
      rule_evaluations: [
        {
          rule_id: "RULE_6_MANDATORY_DECLARATIONS",
          rule_title: "Rule 6: Mandatory Statutory Declarations",
          verdict: "PASS",
          statutory_reference: "Rule 6(1), Legal Metrology (Packaged Commodities) Rules, 2011",
          observed_summary: "All 5 mandatory declarations detected and verified on PDP.",
          required_summary: "MRP, Net Qty, USP, Date of Mfg, and Consumer Contact required.",
          evidence_ids: ["mrp", "net_quantity", "unit_sale_price", "date_of_mfg", "consumer_care"],
          uncertainty_flag: false,
          evaluation_notes: "Clean font detection, confidence above 0.96 threshold.",
        },
        {
          rule_id: "RULE_7_MINIMUM_NUMERAL_HEIGHT",
          rule_title: "Rule 7: Minimum Numeral Height Table-I",
          verdict: "PASS",
          statutory_reference: "Rule 7, Table-I, Legal Metrology (Packaged Commodities) Rules, 2011",
          observed_summary: "Measured net quantity numeral height is 2.15 mm (>= 2.0 mm required).",
          required_summary: "For packaging > 50g up to 200g, minimum numeral height is 2.0 mm.",
          evidence_ids: ["net_quantity"],
          uncertainty_flag: false,
          evaluation_notes: "Conforms to Table-I criteria with 0.15 mm safety margin.",
        },
      ],
      evidence_chain: [
        {
          evidence_id: "ev-01",
          image_sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          panel_name: "PRINCIPAL_DISPLAY_PANEL",
          bounding_box: { x_min: 28.96, y_min: 72.57, x_max: 499.04, y_max: 102.31 },
          calibration_status: "CALIBRATED",
          physical_scale_mm_per_pixel: 0.088,
          observed_value: {
            raw_text: "MRP Rs 20.00 (INCL. OF ALL TAXES)",
            normalized_value: "20.00",
            ocr_confidence: 0.985,
          },
        },
      ],
      errors: [],
      telemetry: {
        sharpness_score: 84.6,
        glare_ratio: 0.015,
        total_pipeline_ms: 1840,
        ocr_inference_ms: 150,
        rule_eval_ms: 45,
      },
      created_at: "2026-09-05T17:30:00Z",
    },
  },

  "SYNTH-02-HIN-FMCG": {
    id: "SYNTH-02-HIN-FMCG",
    title: "Pure Hindi FMCG Packaging Label (Devanagari)",
    packageType: "atta_bag",
    language: "hi",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
    data: {
      inspection_id: "INSP-SYNTH-02-HIN",
      status: "SUCCESS",
      image_sha256: "b7e4112098fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852ba44",
      overall_verdict: "COMPLIANT",
      quality_gate_passed: true,
      calibration_status: "CALIBRATED",
      declarations: {
        mrp: {
          field_name: "mrp",
          raw_text: "अधिकतम खुदरा मूल्य ₹ 245.00",
          normalized_value: 245.0,
          confidence: 0.8912,
          source_token_ids: ["hin_004"],
          bounding_box: { x_min: 28.82, y_min: 72.43, x_max: 346.18, y_max: 111.66 },
          is_mandatory: true,
          is_present: true,
        },
        net_quantity: {
          field_name: "net_quantity",
          raw_text: "निवल मात्रा: 5 किग्रा",
          normalized_value: { value: 5, unit: "kg" },
          confidence: 0.9639,
          source_token_ids: ["hin_003"],
          bounding_box: { x_min: 30.0, y_min: 118.64, x_max: 221.0, y_max: 146.25 },
          is_mandatory: true,
          is_present: true,
        },
        date_of_mfg: {
          field_name: "date_of_mfg",
          raw_text: "पैकिंग की तारीख: 05/2026",
          normalized_value: "2026-05",
          confidence: 0.8849,
          source_token_ids: ["hin_002"],
          bounding_box: { x_min: 28.88, y_min: 160.45, x_max: 266.12, y_max: 190.35 },
          is_mandatory: true,
          is_present: true,
        },
        consumer_care: {
          field_name: "consumer_care",
          raw_text: "care@atta.in",
          normalized_value: "care@atta.in",
          confidence: 0.8125,
          source_token_ids: ["hin_001"],
          bounding_box: { x_min: 28.96, y_min: 203.49, x_max: 277.03, y_max: 228.1 },
          is_mandatory: true,
          is_present: true,
        },
      },
      ocr_observations: [
        {
          token_id: "hin_005",
          text: "SYNTHETIC TEST - NOT REAL PACKAGING",
          confidence: 0.7234,
          bounding_box: { x_min: 31.0, y_min: 26.59, x_max: 363.0, y_max: 43.98 },
          polygon: [
            [31.0, 26.59],
            [363.0, 26.59],
            [363.0, 43.98],
            [31.0, 43.98],
          ],
          language: "hi",
        },
        {
          token_id: "hin_004",
          text: "अधिकतम खुदरा मूल्य ₹ 245.00",
          confidence: 0.8912,
          bounding_box: { x_min: 28.82, y_min: 72.43, x_max: 346.18, y_max: 111.66 },
          polygon: [
            [28.82, 72.43],
            [346.18, 72.43],
            [346.18, 111.66],
            [28.82, 111.66],
          ],
          language: "hi",
        },
        {
          token_id: "hin_003",
          text: "निवल मात्रा: 5 किग्रा",
          confidence: 0.9639,
          bounding_box: { x_min: 30.0, y_min: 118.64, x_max: 221.0, y_max: 146.25 },
          polygon: [
            [30.0, 118.64],
            [221.0, 118.64],
            [221.0, 146.25],
            [30.0, 146.25],
          ],
          language: "hi",
        },
        {
          token_id: "hin_002",
          text: "पैकिंग की तारीख: 05/2026",
          confidence: 0.8849,
          bounding_box: { x_min: 28.88, y_min: 160.45, x_max: 266.12, y_max: 190.35 },
          polygon: [
            [28.88, 160.45],
            [266.12, 160.45],
            [266.12, 190.35],
            [28.88, 190.35],
          ],
          language: "hi",
        },
        {
          token_id: "hin_001",
          text: "care@atta.in",
          confidence: 0.8125,
          bounding_box: { x_min: 28.96, y_min: 203.49, x_max: 277.03, y_max: 228.1 },
          polygon: [
            [28.96, 203.49],
            [277.03, 203.49],
            [277.03, 228.1],
            [28.96, 228.1],
          ],
          language: "hi",
        },
      ],
      measurements: {},
      rule_evaluations: [
        {
          rule_id: "RULE_6_DEVANAGARI_DECLARATIONS",
          rule_title: "Rule 6: Hindi (Devanagari) Declarations Verification",
          verdict: "PASS",
          statutory_reference: "Rule 6(1), Legal Metrology Rules, 2011",
          observed_summary: "All mandatory Hindi declarations detected with valid ₹ currency symbol.",
          required_summary: "MRP with ₹ symbol, Net Quantity in metric units, and manufacturer details.",
          evidence_ids: ["mrp", "net_quantity", "date_of_mfg", "consumer_care"],
          uncertainty_flag: false,
          evaluation_notes: "Devanagari OCR recognition passed with high confidence.",
        },
      ],
      evidence_chain: [],
      errors: [],
      telemetry: {
        sharpness_score: 79.2,
        glare_ratio: 0.021,
        total_pipeline_ms: 1420,
        ocr_inference_ms: 84,
      },
      created_at: "2026-09-05T17:30:00Z",
    },
  },

  "SYNTH-04-MICRO-FONT": {
    id: "SYNTH-04-MICRO-FONT",
    title: "Shrinkflation Microscopic Numeral Deficit",
    packageType: "confectionery_pouch",
    language: "en",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
    data: {
      inspection_id: "INSP-SYNTH-04-MICRO",
      status: "SUCCESS",
      image_sha256: "a1c5d78129ef31a49abff4c8996fb92427ae41e4649b934ca495991b7852f123",
      overall_verdict: "NON_COMPLIANT",
      quality_gate_passed: true,
      calibration_status: "CALIBRATED",
      declarations: {
        mrp: {
          field_name: "mrp",
          raw_text: "MRP Rs 10.00",
          normalized_value: 10.0,
          confidence: 0.965,
          source_token_ids: ["tok-10"],
          bounding_box: { x_min: 70, y_min: 120, x_max: 250, y_max: 155 },
          is_mandatory: true,
          is_present: true,
        },
        net_quantity: {
          field_name: "net_quantity",
          raw_text: "Net Qty: 35g",
          normalized_value: { value: 35, unit: "g" },
          confidence: 0.952,
          source_token_ids: ["tok-11"],
          bounding_box: { x_min: 70, y_min: 165, x_max: 180, y_max: 185 },
          is_mandatory: true,
          is_present: true,
        },
        unit_sale_price: {
          field_name: "unit_sale_price",
          raw_text: "USP Rs 0.28 / g",
          normalized_value: { price: 0.28, unit: "g" },
          confidence: 0.941,
          source_token_ids: ["tok-12"],
          bounding_box: { x_min: 70, y_min: 200, x_max: 210, y_max: 225 },
          is_mandatory: true,
          is_present: true,
        },
      },
      ocr_observations: [
        {
          token_id: "tok-10",
          text: "MRP Rs 10.00",
          confidence: 0.965,
          bounding_box: { x_min: 70, y_min: 120, x_max: 250, y_max: 155 },
          polygon: [
            [70, 120],
            [250, 120],
            [250, 155],
            [70, 155],
          ],
          language: "en",
        },
        {
          token_id: "tok-11",
          text: "Net Qty: 35g",
          confidence: 0.952,
          bounding_box: { x_min: 70, y_min: 165, x_max: 180, y_max: 185 },
          polygon: [
            [70, 165],
            [180, 165],
            [180, 185],
            [70, 185],
          ],
          language: "en",
        },
        {
          token_id: "tok-12",
          text: "USP Rs 0.28 / g",
          confidence: 0.941,
          bounding_box: { x_min: 70, y_min: 200, x_max: 210, y_max: 225 },
          polygon: [
            [70, 200],
            [210, 200],
            [210, 225],
            [70, 225],
          ],
          language: "en",
        },
      ],
      measurements: {
        net_quantity_numeral_height: {
          feature_name: "net_quantity_numeral_height",
          measured_pixels: 13.8,
          scale_factor_mm_per_pixel: 0.092,
          measured_mm: 1.27,
          uncertainty_mm: 0.08,
          calibration_status: "CALIBRATED",
          bounding_box: { x_min: 70, y_min: 165, x_max: 180, y_max: 185 },
        },
      },
      rule_evaluations: [
        {
          rule_id: "RULE_7_MINIMUM_NUMERAL_HEIGHT",
          rule_title: "Rule 7: Minimum Numeral Height Table-I",
          verdict: "FAIL",
          statutory_reference: "Rule 7, Table-I, Legal Metrology (Packaged Commodities) Rules, 2011",
          observed_summary: "Measured net quantity numeral height is 1.27 mm (Statutory minimum: 2.0 mm). Deficit of 0.73 mm.",
          required_summary: "For packages up to 200g, minimum numeral height is 2.0 mm.",
          evidence_ids: ["net_quantity"],
          uncertainty_flag: false,
          evaluation_notes: "Statutory font height deficit confirmed under metric scale calibration.",
        },
      ],
      evidence_chain: [
        {
          evidence_id: "ev-04",
          image_sha256: "a1c5d78129ef31a49abff4c8996fb92427ae41e4649b934ca495991b7852f123",
          panel_name: "PRINCIPAL_DISPLAY_PANEL",
          bounding_box: { x_min: 70, y_min: 165, x_max: 180, y_max: 185 },
          calibration_status: "CALIBRATED",
          physical_scale_mm_per_pixel: 0.092,
          observed_value: {
            raw_text: "Net Qty: 35g",
            measured_font_height_mm: 1.27,
            ocr_confidence: 0.952,
          },
        },
      ],
      errors: [],
      telemetry: {
        sharpness_score: 91.2,
        glare_ratio: 0.012,
        total_pipeline_ms: 1920,
      },
      created_at: "2026-09-05T17:30:00Z",
    },
  },

  "SYNTH-08-LOW-CONTRAST-FADED": {
    id: "SYNTH-08-LOW-CONTRAST-FADED",
    title: "Low Contrast Faded Thermal Print",
    packageType: "polybag_label",
    language: "en",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
    data: {
      inspection_id: "INSP-SYNTH-08-FADED",
      status: "NEEDS_HUMAN_REVIEW",
      image_sha256: "f8c2d11928fa31a49abff4c8996fb92427ae41e4649b934ca495991b7852beef",
      overall_verdict: "SUSPECT_REVIEW",
      quality_gate_passed: true,
      calibration_status: "APPROXIMATE_ASSISTED",
      declarations: {
        mrp: {
          field_name: "mrp",
          raw_text: "MRP Rs 4?.00",
          normalized_value: 45.0,
          confidence: 0.62,
          source_token_ids: ["tok-50"],
          bounding_box: { x_min: 90, y_min: 100, x_max: 220, y_max: 135 },
          is_mandatory: true,
          is_present: true,
        },
      },
      ocr_observations: [
        {
          token_id: "tok-50",
          text: "MRP Rs 4?.00",
          confidence: 0.62,
          bounding_box: { x_min: 90, y_min: 100, x_max: 220, y_max: 135 },
          polygon: [
            [90, 100],
            [220, 100],
            [220, 135],
            [90, 135],
          ],
          language: "en",
        },
      ],
      measurements: {},
      rule_evaluations: [
        {
          rule_id: "RULE_6_AMBIGUOUS_PRICE",
          rule_title: "Rule 6: Legible Retail Price Declaration",
          verdict: "REVIEW",
          statutory_reference: "Rule 6(1)(c), Legal Metrology Rules, 2011",
          observed_summary: "OCR confidence 0.62 below statutory certainty threshold (0.85). Faded thermal dot matrix requires officer verification.",
          required_summary: "Clear, unambiguous declaration of retail price required.",
          evidence_ids: ["mrp"],
          uncertainty_flag: true,
          evaluation_notes: "Character '5' in MRP is partially abraded.",
        },
      ],
      evidence_chain: [],
      errors: [],
      telemetry: {
        sharpness_score: 55.3,
        glare_ratio: 0.042,
        total_pipeline_ms: 2200,
      },
      created_at: "2026-09-05T17:30:00Z",
    },
  },

  "SYNTH-03-MIXED-BILINGUAL": {
    id: "SYNTH-03-MIXED-BILINGUAL",
    title: "Bilingual FMCG Packaging (English + Hindi)",
    packageType: "snack_carton",
    language: "mixed",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
    data: {
      inspection_id: "INSP-SYNTH-03-MIXED",
      status: "SUCCESS",
      image_sha256: "c3d4e5f609fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852c555",
      overall_verdict: "COMPLIANT",
      quality_gate_passed: true,
      calibration_status: "CALIBRATED",
      declarations: {
        mrp: {
          field_name: "mrp",
          raw_text: "MRP ₹ 50.00 (अधिकतम खुदरा मूल्य)",
          normalized_value: 50.0,
          confidence: 0.962,
          source_token_ids: ["mix_001"],
          bounding_box: { x_min: 30.0, y_min: 60.0, x_max: 380.0, y_max: 95.0 },
          is_mandatory: true,
          is_present: true,
        },
        net_quantity: {
          field_name: "net_quantity",
          raw_text: "Net Qty / निवल मात्रा: 150 g",
          normalized_value: { value: 150, unit: "g" },
          confidence: 0.971,
          source_token_ids: ["mix_002"],
          bounding_box: { x_min: 30.0, y_min: 105.0, x_max: 260.0, y_max: 135.0 },
          is_mandatory: true,
          is_present: true,
        },
        unit_sale_price: {
          field_name: "unit_sale_price",
          raw_text: "Unit Sale Price: ₹ 0.33 per g",
          normalized_value: { price: 0.33, unit: "g" },
          confidence: 0.945,
          source_token_ids: ["mix_003"],
          bounding_box: { x_min: 30.0, y_min: 145.0, x_max: 300.0, y_max: 175.0 },
          is_mandatory: true,
          is_present: true,
        },
        date_of_mfg: {
          field_name: "date_of_mfg",
          raw_text: "Mfg Date: 12/2026",
          normalized_value: "2026-12",
          confidence: 0.98,
          source_token_ids: ["mix_004"],
          bounding_box: { x_min: 30.0, y_min: 185.0, x_max: 220.0, y_max: 215.0 },
          is_mandatory: true,
          is_present: true,
        },
        consumer_care: {
          field_name: "consumer_care",
          raw_text: "support@snack.com",
          normalized_value: "support@snack.com",
          confidence: 0.953,
          source_token_ids: ["mix_005"],
          bounding_box: { x_min: 30.0, y_min: 225.0, x_max: 280.0, y_max: 250.0 },
          is_mandatory: true,
          is_present: true,
        },
      },
      ocr_observations: [
        {
          token_id: "mix_001",
          text: "MRP ₹ 50.00 (अधिकतम खुदरा मूल्य)",
          confidence: 0.962,
          bounding_box: { x_min: 30.0, y_min: 60.0, x_max: 380.0, y_max: 95.0 },
          polygon: [[30, 60], [380, 60], [380, 95], [30, 95]],
          language: "mixed",
        },
        {
          token_id: "mix_002",
          text: "Net Qty / निवल मात्रा: 150 g",
          confidence: 0.971,
          bounding_box: { x_min: 30.0, y_min: 105.0, x_max: 260.0, y_max: 135.0 },
          polygon: [[30, 105], [260, 105], [260, 135], [30, 135]],
          language: "mixed",
        },
        {
          token_id: "mix_003",
          text: "Unit Sale Price: ₹ 0.33 per g",
          confidence: 0.945,
          bounding_box: { x_min: 30.0, y_min: 145.0, x_max: 300.0, y_max: 175.0 },
          polygon: [[30, 145], [300, 145], [300, 175], [30, 175]],
          language: "en",
        },
        {
          token_id: "mix_004",
          text: "Mfg Date: 12/2026",
          confidence: 0.98,
          bounding_box: { x_min: 30.0, y_min: 185.0, x_max: 220.0, y_max: 215.0 },
          polygon: [[30, 185], [220, 185], [220, 215], [30, 215]],
          language: "en",
        },
        {
          token_id: "mix_005",
          text: "support@snack.com",
          confidence: 0.953,
          bounding_box: { x_min: 30.0, y_min: 225.0, x_max: 280.0, y_max: 250.0 },
          polygon: [[30, 225], [280, 225], [280, 250], [30, 250]],
          language: "en",
        },
      ],
      measurements: {},
      rule_evaluations: [
        {
          rule_id: "RULE_6_BILINGUAL",
          rule_title: "Rule 6: Mandatory Bilingual Declarations",
          verdict: "PASS",
          statutory_reference: "Rule 6(1), Legal Metrology Rules, 2011",
          observed_summary: "Dual English and Hindi declarations detected with valid ₹ symbols.",
          required_summary: "MRP, Net Quantity, and manufacturer details declared.",
          evidence_ids: ["mrp", "net_quantity"],
          uncertainty_flag: false,
          evaluation_notes: "Bilingual packaging conforms to national language mandates.",
        },
      ],
      evidence_chain: [],
      errors: [],
      telemetry: {
        sharpness_score: 86.4,
        glare_ratio: 0.018,
        total_pipeline_ms: 1650,
      },
      created_at: "2026-09-05T17:30:00Z",
    },
  },

  "SYNTH-05-LIQUID-VOLUME": {
    id: "SYNTH-05-LIQUID-VOLUME",
    title: "Personal Care Bottle (Liquid Volume in ml)",
    packageType: "handwash_bottle",
    language: "en",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
    data: {
      inspection_id: "INSP-SYNTH-05-VOL",
      status: "SUCCESS",
      image_sha256: "e5f6a7b809fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852e777",
      overall_verdict: "COMPLIANT",
      quality_gate_passed: true,
      calibration_status: "CALIBRATED",
      declarations: {
        mrp: {
          field_name: "mrp",
          raw_text: "MRP Rs 125.00",
          normalized_value: 125.0,
          confidence: 0.978,
          source_token_ids: ["vol_001"],
          bounding_box: { x_min: 30.0, y_min: 65.0, x_max: 200.0, y_max: 95.0 },
          is_mandatory: true,
          is_present: true,
        },
        net_quantity: {
          field_name: "net_quantity",
          raw_text: "Net Qty: 250 ml",
          normalized_value: { value: 250, unit: "ml" },
          confidence: 0.985,
          source_token_ids: ["vol_002"],
          bounding_box: { x_min: 30.0, y_min: 110.0, x_max: 190.0, y_max: 140.0 },
          is_mandatory: true,
          is_present: true,
        },
        unit_sale_price: {
          field_name: "unit_sale_price",
          raw_text: "USP: Rs 0.50 / ml",
          normalized_value: { price: 0.5, unit: "ml" },
          confidence: 0.962,
          source_token_ids: ["vol_003"],
          bounding_box: { x_min: 30.0, y_min: 155.0, x_max: 220.0, y_max: 185.0 },
          is_mandatory: true,
          is_present: true,
        },
      },
      ocr_observations: [
        {
          token_id: "vol_001",
          text: "MRP Rs 125.00",
          confidence: 0.978,
          bounding_box: { x_min: 30.0, y_min: 65.0, x_max: 200.0, y_max: 95.0 },
          polygon: [[30, 65], [200, 65], [200, 95], [30, 95]],
          language: "en",
        },
        {
          token_id: "vol_002",
          text: "Net Qty: 250 ml",
          confidence: 0.985,
          bounding_box: { x_min: 30.0, y_min: 110.0, x_max: 190.0, y_max: 140.0 },
          polygon: [[30, 110], [190, 110], [190, 140], [30, 140]],
          language: "en",
        },
      ],
      measurements: {},
      rule_evaluations: [
        {
          rule_id: "RULE_6_LIQUID_METRIC",
          rule_title: "Rule 6: Volume Metric Units Verification",
          verdict: "PASS",
          statutory_reference: "Rule 6(1)(e), Legal Metrology Rules, 2011",
          observed_summary: "Liquid volume declared in recognized SI metric unit 'ml'.",
          required_summary: "Liquids must be declared in ml or L.",
          evidence_ids: ["net_quantity"],
          uncertainty_flag: false,
          evaluation_notes: "Permissible metric volume unit verified.",
        },
      ],
      evidence_chain: [],
      errors: [],
      telemetry: {
        sharpness_score: 88.1,
        glare_ratio: 0.024,
        total_pipeline_ms: 1580,
      },
      created_at: "2026-09-05T17:30:00Z",
    },
  },

  "SYNTH-06-PROHIBITED-UNITS": {
    id: "SYNTH-06-PROHIBITED-UNITS",
    title: "Packaging with Prohibited Pluralized Units (Gms)",
    packageType: "detergent_pouch",
    language: "en",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
    data: {
      inspection_id: "INSP-SYNTH-06-UNITS",
      status: "SUCCESS",
      image_sha256: "f6a7b8c909fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852f888",
      overall_verdict: "NON_COMPLIANT",
      quality_gate_passed: true,
      calibration_status: "CALIBRATED",
      declarations: {
        mrp: {
          field_name: "mrp",
          raw_text: "MRP Rs 85",
          normalized_value: 85.0,
          confidence: 0.954,
          source_token_ids: ["unit_001"],
          bounding_box: { x_min: 30.0, y_min: 60.0, x_max: 180.0, y_max: 90.0 },
          is_mandatory: true,
          is_present: true,
        },
        net_quantity: {
          field_name: "net_quantity",
          raw_text: "Net Qty: 500 Gms",
          normalized_value: { value: 500, unit: "Gms" },
          confidence: 0.968,
          source_token_ids: ["unit_002"],
          bounding_box: { x_min: 30.0, y_min: 105.0, x_max: 230.0, y_max: 135.0 },
          is_mandatory: true,
          is_present: true,
        },
      },
      ocr_observations: [
        {
          token_id: "unit_001",
          text: "MRP Rs 85",
          confidence: 0.954,
          bounding_box: { x_min: 30.0, y_min: 60.0, x_max: 180.0, y_max: 90.0 },
          polygon: [[30, 60], [180, 60], [180, 90], [30, 90]],
          language: "en",
        },
        {
          token_id: "unit_002",
          text: "Net Qty: 500 Gms",
          confidence: 0.968,
          bounding_box: { x_min: 30.0, y_min: 105.0, x_max: 230.0, y_max: 135.0 },
          polygon: [[30, 105], [230, 105], [230, 135], [30, 135]],
          language: "en",
        },
      ],
      measurements: {},
      rule_evaluations: [
        {
          rule_id: "RULE_12_PROHIBITED_UNITS",
          rule_title: "Rule 12: Standard Units of Weight and Measure",
          verdict: "FAIL",
          statutory_reference: "Rule 12, Legal Metrology (Packaged Commodities) Rules, 2011",
          observed_summary: "Declared unit 'Gms' is a prohibited pluralized abbreviation. Statutory symbol is 'g'.",
          required_summary: "Mass must be expressed as 'g' or 'kg', never pluralized as 'Gms' or 'Kgs'.",
          evidence_ids: ["net_quantity"],
          uncertainty_flag: false,
          evaluation_notes: "Statutory violation of standard unit representation under Rule 12.",
        },
      ],
      evidence_chain: [],
      errors: [],
      telemetry: {
        sharpness_score: 82.5,
        glare_ratio: 0.031,
        total_pipeline_ms: 1710,
      },
      created_at: "2026-09-05T17:30:00Z",
    },
  },

  "SYNTH-07-BLANK-FRAME": {
    id: "SYNTH-07-BLANK-FRAME",
    title: "Blank / Texture-Only Failure Mode Frame",
    packageType: "blank_cardboard",
    language: "none",
    disclaimer: "SYNTHETIC REGRESSION ASSET — NOT REAL RETAIL PACKAGING",
    data: {
      inspection_id: "INSP-SYNTH-07-BLANK",
      status: "REJECTED_QUALITY",
      image_sha256: "a7b8c9d009fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852a111",
      overall_verdict: "INCONCLUSIVE",
      quality_gate_passed: false,
      calibration_status: "UNCALIBRATED",
      declarations: {},
      ocr_observations: [],
      measurements: {},
      rule_evaluations: [],
      evidence_chain: [],
      errors: [
        {
          error_code: "QUALITY_GATE_NO_TEXT",
          stage: "QualityGate",
          message: "No statutory declarations or readable typography detected in uploaded frame.",
          remediation_hint: "Provide an unoccluded, in-focus photograph of the Principal Display Panel.",
          is_fatal: true,
        },
      ],
      telemetry: {
        sharpness_score: 32.1,
        glare_ratio: 0.005,
        total_pipeline_ms: 780,
      },
      created_at: "2026-09-05T17:30:00Z",
    },
  },
};

/**
 * Returns a fallback synthetic fixture based on filename or defaults to SYNTH-01
 */
export function getSyntheticFixtureForFile(file: File): SyntheticFixtureDefinition {
  const name = file.name.toUpperCase();
  if (name.includes("SYNTH-02") || name.includes("HIN") || name.includes("HINDI") || name.includes("ATTA")) {
    return SYNTHETIC_FIXTURES["SYNTH-02-HIN-FMCG"];
  }
  if (name.includes("SYNTH-03") || name.includes("MIXED") || name.includes("BILINGUAL")) {
    return SYNTHETIC_FIXTURES["SYNTH-03-MIXED-BILINGUAL"];
  }
  if (name.includes("SYNTH-04") || name.includes("MICRO") || name.includes("DEFICIT")) {
    return SYNTHETIC_FIXTURES["SYNTH-04-MICRO-FONT"];
  }
  if (name.includes("SYNTH-05") || name.includes("LIQUID") || name.includes("VOLUME") || name.includes("BOTTLE")) {
    return SYNTHETIC_FIXTURES["SYNTH-05-LIQUID-VOLUME"];
  }
  if (name.includes("SYNTH-06") || name.includes("PROHIBITED") || name.includes("GMS") || name.includes("UNITS")) {
    return SYNTHETIC_FIXTURES["SYNTH-06-PROHIBITED-UNITS"];
  }
  if (name.includes("SYNTH-07") || name.includes("BLANK") || name.includes("TEXTURE")) {
    return SYNTHETIC_FIXTURES["SYNTH-07-BLANK-FRAME"];
  }
  if (name.includes("SYNTH-08") || name.includes("FADED") || name.includes("REVIEW")) {
    return SYNTHETIC_FIXTURES["SYNTH-08-LOW-CONTRAST-FADED"];
  }
  return SYNTHETIC_FIXTURES["SYNTH-01-ENG-FMCG"];
}

/**
 * Returns a synthetic fixture by id or prefix (e.g. 'SYNTH-01')
 */
export function getFixtureById(idOrPrefix: string): SyntheticFixtureDefinition | undefined {
  const key = Object.keys(SYNTHETIC_FIXTURES).find(
    (k) => k === idOrPrefix || k.startsWith(idOrPrefix)
  );
  return key ? SYNTHETIC_FIXTURES[key] : undefined;
}
