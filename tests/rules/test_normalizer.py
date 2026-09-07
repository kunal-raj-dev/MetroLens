"""
Tests for TokenNormalizer in nirikshak_rules_engine.normalizer.
Verifies Gate 2 / CP-2 deterministic entity extraction from mock OCR tokens.
"""

import json
import time
from pathlib import Path
import pytest

from nirikshak_rules_engine import (
    TokenNormalizer,
    CanonicalDeclaration,
    UnitType,
    OCRToken,
)

FIXTURES_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "mock_ocr_tokens.json"


@pytest.fixture(scope="module")
def mock_fixtures():
    assert FIXTURES_PATH.exists(), f"Fixtures missing at {FIXTURES_PATH}"
    with open(FIXTURES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("fixtures", {})


@pytest.fixture
def normalizer():
    return TokenNormalizer()


def test_normalize_standard_fmcg_cashews(normalizer, mock_fixtures):
    """Verify parsing of clean, fully compliant FMCG retail package."""
    fixture = mock_fixtures["PKG-01-COMPLIANT-FMCG-CASHEWS"]
    decl = normalizer.normalize(fixture["tokens"])

    assert decl.mrp_inr == 240.0
    assert decl.tax_qualifier_present is True
    assert decl.net_quantity_value == 200.0
    assert decl.net_quantity_unit == UnitType.GRAM
    assert decl.declared_usp_value == 1.20
    assert decl.declared_usp_unit == "g"
    assert decl.mfg_month == 8
    assert decl.mfg_year == 2026
    assert decl.manufacturer_pincode == "110020"
    assert "MetroLens Foods" in (decl.manufacturer_name or "")
    assert decl.consumer_care_phone == "1800-11-4000"
    assert decl.consumer_care_email == "care@metrolens.in"
    assert decl.country_of_origin == "India"
    assert decl.is_pan_masala_or_tobacco is False
    assert decl.is_wholesale_or_bulk is False


def test_normalize_bilingual_devanagari_hindi(normalizer, mock_fixtures):
    """Verify parsing of Devanagari Hindi statutory declarations."""
    fixture = mock_fixtures["PKG-02-BILINGUAL-HINDI-ATTA"]
    decl = normalizer.normalize(fixture["tokens"])

    assert decl.mrp_inr == 45.0
    assert decl.tax_qualifier_present is True
    assert decl.net_quantity_value == 1.0
    assert decl.net_quantity_unit == UnitType.KILOGRAM
    assert decl.declared_usp_value == 45.0
    assert decl.declared_usp_unit == "kg"
    assert decl.mfg_month == 5
    assert decl.mfg_year == 2026
    assert decl.manufacturer_pincode == "302013"
    assert decl.consumer_care_email == "support@kisanfoods.in"
    assert decl.consumer_care_phone == "1800-200-5555"
    assert decl.country_of_origin == "India"


def test_detect_missing_tax_qualifier(normalizer, mock_fixtures):
    """Verify detection when MRP is declared without mandatory tax qualifier."""
    fixture = mock_fixtures["PKG-03-MISSING-TAX-QUALIFIER"]
    decl = normalizer.normalize(fixture["tokens"])

    assert decl.mrp_inr == 20.0
    assert decl.tax_qualifier_present is False
    assert decl.net_quantity_value == 50.0
    assert decl.net_quantity_unit == UnitType.GRAM


def test_prohibited_units_handling(normalizer, mock_fixtures):
    """Verify normalization of prohibited unit notations like Gms and capital ML."""
    fixture_gms = mock_fixtures["PKG-04-PROHIBITED-UNITS-GMS"]
    decl_gms = normalizer.normalize(fixture_gms["tokens"])
    assert decl_gms.net_quantity_value == 500.0
    assert decl_gms.net_quantity_unit == UnitType.GRAM
    assert decl_gms.declared_usp_unit in ["gm", "g"]

    fixture_ml = mock_fixtures["PKG-05-PROHIBITED-UNITS-CAPS-ML"]
    decl_ml = normalizer.normalize(fixture_ml["tokens"])
    assert decl_ml.net_quantity_value == 750.0
    assert decl_ml.net_quantity_unit == UnitType.MILLILITER


def test_ctc_confusion_repair(normalizer, mock_fixtures):
    """Verify CTC character confusion repair (O for 0, l for 1)."""
    fixture = mock_fixtures["PKG-06-NOISY-CTC-CONFUSIONS"]
    decl = normalizer.normalize(fixture["tokens"])

    # Repaired: '2O5.OO' -> 205.00
    assert decl.mrp_inr == 205.0
    # Repaired: 'l000 g' -> 1000 g
    assert decl.net_quantity_value == 1000.0
    assert decl.net_quantity_unit == UnitType.GRAM
    # Repaired: 'O8/2026' -> 8 / 2026
    assert decl.mfg_month == 8
    assert decl.mfg_year == 2026
    assert decl.manufacturer_pincode == "132001"
    assert decl.consumer_care_phone == "1800-180-2222"


def test_best_before_date_parsing(normalizer, mock_fixtures):
    """Verify manufacturing date extraction from Best Before phrasing."""
    fixture = mock_fixtures["PKG-07-DATE-FORMAT-BEST-BEFORE"]
    decl = normalizer.normalize(fixture["tokens"])

    assert decl.mfg_month == 6
    assert decl.mfg_year == 2026
    assert decl.mrp_inr == 75.0
    assert decl.net_quantity_value == 150.0
    assert decl.net_quantity_unit == UnitType.GRAM


def test_pan_masala_category_flag(normalizer, mock_fixtures):
    """Verify that miniature pan masala is flagged as non-exempt per G.S.R. 881(E)."""
    fixture = mock_fixtures["PKG-08-MINIATURE-PAN-MASALA"]
    decl = normalizer.normalize(fixture["tokens"])

    assert decl.is_pan_masala_or_tobacco is True
    assert decl.net_quantity_value == 4.0
    assert decl.net_quantity_unit == UnitType.GRAM
    assert decl.mrp_inr == 5.0


def test_wholesale_bulk_flag(normalizer, mock_fixtures):
    """Verify that wholesale packages (>25kg) are flagged for Rule 3 exclusion."""
    fixture = mock_fixtures["PKG-10-WHOLESALE-BULK-30KG"]
    decl = normalizer.normalize(fixture["tokens"])

    assert decl.is_wholesale_or_bulk is True
    assert decl.net_quantity_value == 30.0
    assert decl.net_quantity_unit == UnitType.KILOGRAM


def test_blank_frame_handling(normalizer, mock_fixtures):
    """Verify that an empty token list returns a clean default declaration without exceptions."""
    fixture = mock_fixtures["PKG-12-BLANK-FRAME"]
    decl = normalizer.normalize(fixture["tokens"])

    assert isinstance(decl, CanonicalDeclaration)
    assert decl.mrp_inr is None
    assert decl.net_quantity_value is None
    assert decl.tax_qualifier_present is False


def test_raw_string_and_ocr_token_objects(normalizer):
    """Verify normalizer works with OCRToken objects as well as raw strings."""
    tokens = [
        OCRToken(
            token_id="t1",
            text="MRP Rs. 99.00 (inclusive of all taxes)",
            confidence=0.98,
            bbox=[10.0, 10.0, 100.0, 30.0],
        ),
        OCRToken(
            token_id="t2",
            text="Net Qty: 250 g",
            confidence=0.97,
            bbox=[10.0, 40.0, 100.0, 60.0],
        ),
    ]
    decl = normalizer.normalize(tokens)
    assert decl.mrp_inr == 99.0
    assert decl.tax_qualifier_present is True
    assert decl.net_quantity_value == 250.0
    assert decl.net_quantity_unit == UnitType.GRAM

    # Raw string input
    raw_str = "MRP ₹ 150.00 incl. of all taxes\nNet Quantity: 500 ml\nMfg: 10/2026"
    decl2 = normalizer.normalize(raw_str)
    assert decl2.mrp_inr == 150.0
    assert decl2.tax_qualifier_present is True
    assert decl2.net_quantity_value == 500.0
    assert decl2.net_quantity_unit == UnitType.MILLILITER
    assert decl2.mfg_month == 10
    assert decl2.mfg_year == 2026


def test_normalizer_latency_budget(normalizer, mock_fixtures):
    """Verify that normalization executes in < 5ms per frame on CPU."""
    fixture = mock_fixtures["PKG-01-COMPLIANT-FMCG-CASHEWS"]
    tokens = fixture["tokens"]

    # Warmup
    for _ in range(5):
        normalizer.normalize(tokens)

    start = time.perf_counter()
    iterations = 100
    for _ in range(iterations):
        normalizer.normalize(tokens)
    elapsed = time.perf_counter() - start

    avg_ms = (elapsed / iterations) * 1000
    assert avg_ms < 5.0, f"Normalizer exceeded 5ms latency budget: {avg_ms:.2f} ms"
