"""
Unit tests for the Precision OCR Evaluation Engine.
Verifies:
1. Exact Levenshtein character edit distance.
2. Character Error Rate (CER) edge cases (empty strings, deletions, insertions, substitutions).
3. Word Error Rate (WER) with multi-script whitespace tokenization.
4. Hindi / Devanagari Unicode preservation & distance.
5. Numeric robustness & confusion classification (0/O, 1/I/l, 5/S, 8/B, decimal points).
6. Error taxonomy classification.
"""

import pytest
from nirikshak_ocr.evaluation import (
    levenshtein_distance,
    compute_cer,
    compute_wer,
    evaluate_numeric_accuracy,
    classify_ocr_error
)


def test_levenshtein_distance():
    assert levenshtein_distance("", "") == 0
    assert levenshtein_distance("kitten", "sitting") == 3
    assert levenshtein_distance("MRP", "MRP") == 0
    assert levenshtein_distance("100", "1O0") == 1 # 0 vs O
    assert levenshtein_distance("₹50.00", "50.00") == 1 # missing ₹


def test_compute_cer():
    # Identical
    assert compute_cer("Hello", "Hello") == 0.0
    # Both empty
    assert compute_cer("", "") == 0.0
    # Empty prediction, reference of length 5 -> CER = 1.0 (5/5)
    assert compute_cer("", "Hello") == 1.0
    # Reference empty, non-empty prediction
    assert compute_cer("Hello", "") == 1.0
    # 1 edit on length 10 -> 0.10
    assert pytest.approx(compute_cer("1234567890", "123456789O")) == 0.10


def test_hindi_unicode_cer():
    # Devanagari strings
    ref_hindi = "किग्रा" # 6 Unicode codepoints (क + ि + ग + ् + र + ा)
    pred_hindi = "किग्रा"
    assert compute_cer(pred_hindi, ref_hindi) == 0.0

    # 1 glyph missing
    pred_partial = "किग्र"
    cer = compute_cer(pred_partial, ref_hindi)
    assert cer > 0.0 and cer < 0.5


def test_compute_wer():
    # Exact match
    assert compute_wer("Best Before 6 Months", "Best Before 6 Months") == 0.0
    # 1 word substitution out of 4 -> WER = 0.25
    assert pytest.approx(compute_wer("Best After 6 Months", "Best Before 6 Months")) == 0.25
    # Word insertion
    assert pytest.approx(compute_wer("Net Qty 100 g net", "Net Qty 100 g")) == 0.25
    # Empty cases
    assert compute_wer("", "") == 0.0
    assert compute_wer("", "One Two") == 1.0


def test_evaluate_numeric_accuracy():
    # Clean match
    res_clean = evaluate_numeric_accuracy("MRP Rs. 50.00", "MRP Rs. 50.00")
    assert res_clean["exact_string_match"] is True
    assert res_clean["exact_digit_match"] is True
    assert len(res_clean["confusions_detected"]) == 0

    # 0 confused with O
    res_zero_o = evaluate_numeric_accuracy("MRP Rs. 5O.00", "MRP Rs. 50.00")
    assert res_zero_o["exact_digit_match"] is False
    assert "0_confused_with_O" in res_zero_o["confusions_detected"]

    # 1 confused with I or l
    res_one_i = evaluate_numeric_accuracy("Net Qty I00g", "Net Qty 100g")
    assert "1_confused_with_I_or_l" in res_one_i["confusions_detected"]

    # 5 confused with S
    res_five_s = evaluate_numeric_accuracy("MRP S0", "MRP 50")
    assert "5_confused_with_S" in res_five_s["confusions_detected"]

    # Missing decimal point
    res_missing_dot = evaluate_numeric_accuracy("MRP 5000", "MRP 50.00")
    assert "missing_decimal_point" in res_missing_dot["confusions_detected"]


def test_classify_ocr_error():
    assert classify_ocr_error("MRP 50", "MRP 50") == "PERFECT_MATCH"
    assert classify_ocr_error("", "MRP 50") == "DETECTION_FAILURE"
    assert classify_ocr_error("MRP 5O", "MRP 50") == "NUMERIC_CONFUSION"
    assert classify_ocr_error("BATCH", "BATCH 2026", special_condition="dot_matrix_inkjet") == "DOT_MATRIX"
    assert classify_ocr_error("NET", "NET WT", special_condition="low_contrast_foil") == "LOW_CONTRAST"
    # Hindi reference but English predicted -> SCRIPT_ROUTING
    assert classify_ocr_error("atta", "आटा") == "SCRIPT_ROUTING"
