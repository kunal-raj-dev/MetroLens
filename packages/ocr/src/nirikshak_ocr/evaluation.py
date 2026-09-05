"""
Precision OCR Evaluation Engine.
Provides standardized, mathematically rigorous implementations of:
- Character Error Rate (CER) via Levenshtein edit distance.
- Word Error Rate (WER) via token sequence alignment.
- Script-stratified accuracy (Latin, Devanagari, Mixed).
- Numeric robustness & confusion classification (0/O, 1/I/l, 5/S, 8/B, decimal points).
- Statutory field-level exact match scoring.
- Error taxonomy classifier.
"""

from typing import Dict, List, Optional, Tuple, Any
import re
import unicodedata


def levenshtein_distance(s1: str, s2: str) -> int:
    """Computes exact Levenshtein character edit distance using dynamic programming."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # Deletion
                dp[i][j - 1] + 1,      # Insertion
                dp[i - 1][j - 1] + cost # Substitution
            )

    return dp[m][n]


def compute_cer(prediction: str, reference: str, normalize_unicode: bool = True) -> float:
    """
    Computes Character Error Rate (CER):
    CER = Levenshtein(pred, ref) / max(1, len(ref))
    
    Behavior:
    - If both pred and ref are empty: CER = 0.0
    - If ref is empty but pred is non-empty: CER = 1.0 (or edit distance / 1)
    - Preserves exact whitespace and punctuation unless normalized.
    """
    if normalize_unicode:
        p = unicodedata.normalize("NFC", prediction or "")
        r = unicodedata.normalize("NFC", reference or "")
    else:
        p = prediction or ""
        r = reference or ""

    if not r:
        return 0.0 if not p else 1.0

    dist = levenshtein_distance(p, r)
    return float(dist) / float(len(r))


def compute_wer(prediction: str, reference: str) -> float:
    """
    Computes Word Error Rate (WER) using whitespace word tokenization:
    WER = Levenshtein(pred_tokens, ref_tokens) / max(1, len(ref_tokens))
    """
    p_words = (prediction or "").strip().split()
    r_words = (reference or "").strip().split()

    if not r_words:
        return 0.0 if not p_words else 1.0

    m, n = len(p_words), len(r_words)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if p_words[i - 1] == r_words[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return float(dp[m][n]) / float(len(r_words))


def evaluate_numeric_accuracy(prediction: str, reference: str) -> Dict[str, Any]:
    """
    Evaluates numeric and statutory symbol accuracy:
    - Extracts digit sequences and symbols (., /, -, ₹, Rs, g, kg, ml, L).
    - Detects common OCR confusions: 0/O, 1/I/l, 5/S, 8/B, 6/G, missing decimal.
    """
    p = prediction or ""
    r = reference or ""

    # Extract digits only
    p_digits = re.sub(r"\D", "", p)
    r_digits = re.sub(r"\D", "", r)

    exact_digit_match = (p_digits == r_digits) if r_digits else (p_digits == "")

    # Check specific confusion patterns
    confusions: List[str] = []
    if "O" in p and "0" in r:
        confusions.append("0_confused_with_O")
    if ("I" in p or "l" in p) and "1" in r:
        confusions.append("1_confused_with_I_or_l")
    if "S" in p and "5" in r:
        confusions.append("5_confused_with_S")
    if "B" in p and "8" in r:
        confusions.append("8_confused_with_B")
    if "G" in p and "6" in r:
        confusions.append("6_confused_with_G")
    if "." in r and "." not in p:
        confusions.append("missing_decimal_point")
    if "," in r and "." in p:
        confusions.append("comma_as_decimal")

    digit_cer = compute_cer(p_digits, r_digits) if r_digits else (0.0 if not p_digits else 1.0)

    return {
        "exact_string_match": p.strip() == r.strip(),
        "exact_digit_match": exact_digit_match,
        "digit_cer": round(digit_cer, 4),
        "ref_digits": r_digits,
        "pred_digits": p_digits,
        "confusions_detected": confusions
    }


def classify_ocr_error(
    prediction: str,
    reference: str,
    confidence: float = 1.0,
    special_condition: Optional[str] = None
) -> str:
    """
    Classifies the dominant failure mode into the standardized Failure Taxonomy:
    - PERFECT_MATCH
    - DETECTION_FAILURE (empty prediction for non-empty reference)
    - NUMERIC_CONFUSION
    - LOW_CONTRAST
    - DOT_MATRIX
    - SMALL_TEXT
    - SCRIPT_ROUTING
    - RECOGNITION_FAILURE
    """
    p = (prediction or "").strip()
    r = (reference or "").strip()

    if p == r:
        return "PERFECT_MATCH"

    if not p and r:
        return "DETECTION_FAILURE"

    num_eval = evaluate_numeric_accuracy(p, r)
    if num_eval["confusions_detected"]:
        return "NUMERIC_CONFUSION"

    if special_condition:
        cond = special_condition.lower()
        if "dot_matrix" in cond:
            return "DOT_MATRIX"
        if "low_contrast" in cond:
            return "LOW_CONTRAST"
        if "micro" in cond or "small" in cond:
            return "SMALL_TEXT"

    # Check script mismatch (Devanagari Unicode range: 0x0900 - 0x097F)
    has_dev_ref = any(0x0900 <= ord(c) <= 0x097F for c in r)
    has_dev_pred = any(0x0900 <= ord(c) <= 0x097F for c in p)
    if has_dev_ref != has_dev_pred:
        return "SCRIPT_ROUTING"

    return "RECOGNITION_FAILURE"


def compute_routing_accuracy(
    decisions: List[Tuple[str, str]]
) -> Dict[str, Any]:
    """
    Computes script routing accuracy strictly separated from character recognition (CER).
    Args:
        decisions: List of (predicted_script, ground_truth_script) tuples,
                   e.g. [('devanagari', 'devanagari'), ('latin', 'latin')].
    Returns:
        Dict with total_routed, correct_routed, incorrect_routed, and routing_accuracy [0.0, 1.0].
    """
    if not decisions:
        return {
            "total_routed": 0,
            "correct_routed": 0,
            "incorrect_routed": 0,
            "routing_accuracy": 1.0
        }

    correct = sum(1 for pred, gt in decisions if pred.lower().strip() == gt.lower().strip())
    total = len(decisions)
    return {
        "total_routed": total,
        "correct_routed": correct,
        "incorrect_routed": total - correct,
        "routing_accuracy": round(float(correct) / float(total), 4)
    }
