"""Parameterized API parsing scenarios with explicitly injected OCR observations.

Each case supplies distinct tokens to the real upload/normalizer/rules/storage
path through guarded_api. Quality and OCR outputs are controlled in tests;
these are not real-package accuracy or industry-specific legal validation.
Unimplemented dual-measurement, importer, and symbol-adjudication behavior is
not inferred from a successful response.
"""

import importlib
import re
from types import SimpleNamespace

import pytest


def _screen(guarded_api, monkeypatch, lines):
    tokens = [SimpleNamespace(token_id=f"scenario_{index}", text=text,
        confidence=0.95, bbox=[10.0, 20.0 + index * 30, 700.0, 40.0 + index * 30],
        script="latin") for index, text in enumerate(lines)]
    pipeline = importlib.import_module("apps.api.services.pipeline_orchestrator").pipeline_orchestrator
    monkeypatch.setattr(pipeline, "_get_ocr_service", lambda: SimpleNamespace(
        extract=lambda *args, **kwargs: SimpleNamespace(tokens=tokens)))
    result = guarded_api.upload()
    assert [token["text"] for token in result["ocr_observations"]] == lines
    assert result["improvement_notice"] is None
    assert result["rule_evaluations"]["font_height_audit"]["status"] == "REVIEW"
    return result


def _amount(text):
    return float(re.search(r"[0-9]+(?:[.][0-9]+)?", text).group())


def _check_quantity(declarations, quantity):
    magnitude, unit = quantity.split()
    assert declarations["net_quantity_value"] == float(magnitude)
    assert declarations["net_quantity_unit"] == ("N" if unit == "N" else unit.lower())


def _check_unit_price(declarations, usp):
    # Current parser supports at most two decimal places. Preserve a more precise
    # source observation without claiming it was parsed or legally rounded.
    numeric = re.search(r"[0-9]+(?:[.][0-9]+)?", usp).group()
    if "." in numeric and len(numeric.split(".")[1]) > 2:
        assert declarations["declared_usp_value"] is None
    else:
        assert declarations["declared_usp_value"] == float(numeric)
        assert declarations["declared_usp_unit"] == usp.split()[-1].lower()


@pytest.mark.parametrize('commodity_name, net_qty, mrp, usp',
[('Glucose Biscuits 100g', '100 g', 'Rs. 10.00', 'Rs. 0.10 per g'),
 ('Whole Wheat Atta 5kg', '5 kg', 'Rs. 240.00', 'Rs. 48.00 per kg'),
 ('Basmati Rice 1kg', '1 kg', 'Rs. 120.00', 'Rs. 120.00 per kg'),
 ('Instant Noodles 70g', '70 g', 'Rs. 14.00', 'Rs. 0.20 per g'),
 ('Potato Chips 40g', '40 g', 'Rs. 20.00', 'Rs. 0.50 per g'),
 ('Corn Flakes 500g', '500 g', 'Rs. 195.00', 'Rs. 0.39 per g'),
 ('Tomato Ketchup 950g', '950 g', 'Rs. 130.00', 'Rs. 0.137 per g'),
 ('Fruit Jam 500g', '500 g', 'Rs. 165.00', 'Rs. 0.33 per g'),
 ('Chocolate Bar 50g', '50 g', 'Rs. 45.00', 'Rs. 0.90 per g'),
 ('Breakfast Oats 1kg', '1 kg', 'Rs. 180.00', 'Rs. 180.00 per kg')])
def test_food_declaration_scenarios(guarded_api, monkeypatch, commodity_name, net_qty, mrp, usp):
    result = _screen(guarded_api, monkeypatch, [commodity_name, f"Net Quantity: {net_qty}",
        f"MRP: {mrp} inclusive of all taxes", f"Unit Sale Price: {usp}"])
    declarations = result["declarations"]
    assert declarations["commodity_name"] == commodity_name
    assert declarations["mrp_inr"] == _amount(mrp)
    assert declarations["tax_qualifier_present"] is True
    _check_quantity(declarations, net_qty)
    _check_unit_price(declarations, usp)


@pytest.mark.parametrize('oil_name, volume_str, mass_str, mrp, usp',
[('Mustard Oil 1L', '1 L', '910 g', 'Rs. 175.00', 'Rs. 175.00 per L'),
 ('Refined Sunflower Oil 1L', '1 L', '910 g', 'Rs. 140.00', 'Rs. 140.00 per L'),
 ('Groundnut Oil 5L Jar', '5 L', '4.55 kg', 'Rs. 950.00', 'Rs. 190.00 per L'),
 ('Desi Cow Ghee 500ml', '500 ml', '455 g', 'Rs. 360.00', 'Rs. 0.72 per ml'),
 ('Olive Oil Extra Virgin 250ml', '250 ml', '230 g', 'Rs. 450.00', 'Rs. 1.80 per ml'),
 ('Soyabean Oil 1L Pouch', '1 L', '910 g', 'Rs. 125.00', 'Rs. 125.00 per L'),
 ('Coconut Oil 200ml Bottle', '200 ml', '185 g', 'Rs. 85.00', 'Rs. 0.425 per ml'),
 ('Sesame Til Oil 500ml', '500 ml', '460 g', 'Rs. 210.00', 'Rs. 0.42 per ml')])
def test_oil_volume_and_mass_observations(guarded_api, monkeypatch, oil_name, volume_str, mass_str, mrp, usp):
    result = _screen(guarded_api, monkeypatch, [oil_name, f"Net Volume: {volume_str}",
        f"Equivalent Mass: {mass_str}", f"MRP: {mrp}", f"Unit Sale Price: {usp}"])
    declarations = result["declarations"]
    assert declarations["commodity_name"] == oil_name
    assert declarations["mrp_inr"] == _amount(mrp)
    _check_quantity(declarations, volume_str)
    _check_unit_price(declarations, usp)
    # Equivalent mass remains observable text; no dual-declaration verdict asserted.


@pytest.mark.parametrize('product_name, net_qty, mrp',
[('Herbal Shampoo 180ml', '180 ml', 'Rs. 160.00'),
 ('Bathing Bar Soap 125g', '125 g', 'Rs. 55.00'),
 ('Skin Moisturizing Cream 100g', '100 g', 'Rs. 220.00'),
 ('Ayurvedic Toothpaste 150g', '150 g', 'Rs. 95.00'),
 ('Hand Sanitizer Gel 500ml', '500 ml', 'Rs. 199.00'),
 ('Hair Conditioner 200ml', '200 ml', 'Rs. 240.00'),
 ('Face Wash Gel 100ml', '100 ml', 'Rs. 145.00'),
 ('Sunscreen Lotion SPF50 50g', '50 g', 'Rs. 399.00')])
def test_personal_care_declaration_scenarios(guarded_api, monkeypatch, product_name, net_qty, mrp):
    result = _screen(guarded_api, monkeypatch, [product_name, f"Net Quantity: {net_qty}", f"MRP: {mrp}"])
    declarations = result["declarations"]
    assert declarations["commodity_name"] == product_name
    assert declarations["mrp_inr"] == _amount(mrp)
    _check_quantity(declarations, net_qty)


@pytest.mark.parametrize('device_name, qty, mrp, country',
[('LED Bulb 9W B22', '1 N', 'Rs. 110.00', 'Made in India'),
 ('USB-C Fast Charging Cable 1m', '1 N', 'Rs. 349.00', 'Country of Origin: Vietnam'),
 ('Lithium AA Batteries 4-Pack', '4 N', 'Rs. 160.00', 'Country of Origin: Japan'),
 ('Smart Extension Cord 2m', '1 N', 'Rs. 899.00', 'Made in India'),
 ('Wireless Optical Mouse', '1 N', 'Rs. 499.00', 'Country of Origin: China'),
 ('Portable Bluetooth Speaker', '1 N', 'Rs. 1499.00', 'Country of Origin: India')])
def test_counted_goods_and_country_observations(guarded_api, monkeypatch, device_name, qty, mrp, country):
    result = _screen(guarded_api, monkeypatch, [device_name, f"Net Quantity: {qty}", f"MRP: {mrp}", country])
    declarations = result["declarations"]
    assert declarations["commodity_name"] == device_name
    assert declarations["mrp_inr"] == _amount(mrp)
    _check_quantity(declarations, qty)
    assert declarations["country_of_origin"] == country.split()[-1]


@pytest.mark.parametrize('imported_item, importer, origin, mrp',
[('Imported Swiss Chocolate 100g',
  'Imported by: Global Confections Pvt Ltd, Mumbai',
  'Country of Origin: Switzerland',
  'Rs. 350.00'),
 ('Extra Virgin Olive Oil 500ml',
  'Imported by: Mediterranean Foods Ltd, Delhi',
  'Country of Origin: Spain',
  'Rs. 750.00'),
 ('Imported Green Tea 50 Bags',
  'Imported by: Orient Beverage Importers, Chennai',
  'Country of Origin: Sri Lanka',
  'Rs. 420.00'),
 ('Sparkling Natural Mineral Water 750ml',
  'Imported by: Alps Pure Imports, Bengaluru',
  'Country of Origin: France',
  'Rs. 290.00')])
def test_importer_and_origin_text_are_preserved(guarded_api, monkeypatch, imported_item, importer, origin, mrp):
    result = _screen(guarded_api, monkeypatch, [imported_item, importer, origin, f"MRP: {mrp}"])
    assert result["declarations"]["commodity_name"] == imported_item
    assert result["declarations"]["mrp_inr"] == _amount(mrp)
    observed = [token["text"] for token in result["ocr_observations"]]
    assert importer in observed and origin in observed
    # Raw importer/country evidence survives; this does not certify import compliance.


@pytest.mark.parametrize('scenario_name, quantity_text, symbol',
[("Rule 26 Non-Standard Unit 'gm'", 'Net Wt: 250 gm | MRP Rs. 50', 'gm'),
 ("Rule 26 Non-Standard Unit 'gms'", 'Net Weight: 500 gms | MRP Rs. 90', 'gms'),
 ("Rule 26 Non-Standard Unit 'ml.'", 'Net Vol: 200 ml. | MRP Rs. 60', 'ml.'),
 ("Rule 26 Non-Standard Unit 'kgs'", 'Net Qty: 2 kgs | MRP Rs. 140', 'kgs'),
 ("Rule 26 Non-Standard Unit 'ltr'", 'Net Quantity: 1 ltr | MRP Rs. 110', 'ltr'),
 ("Rule 26 Prohibited Symbol 'Gms.'", 'Net Contents: 100 Gms. | MRP Rs. 35', 'Gms.')])
def test_quantity_symbol_observations_are_not_silently_replaced(guarded_api, monkeypatch, scenario_name, quantity_text, symbol):
    result = _screen(guarded_api, monkeypatch, ["Symbol specimen", quantity_text])
    declarations = result["declarations"]
    assert symbol in result["ocr_observations"][1]["text"]
    assert declarations["mrp_inr"] == _amount(quantity_text.split("MRP", 1)[1])
    # Assert supported normalized units; unsupported label text remains unresolved.
    expected = {"gm": (250.0, "g"), "gms": (500.0, "g"), "ml.": (200.0, "ml"),
                "kgs": (2.0, "kg"), "ltr": (1.0, "l"), "Gms.": (None, None)}
    magnitude, unit = expected[symbol]
    assert declarations["net_quantity_value"] == magnitude, scenario_name
    assert declarations["net_quantity_unit"] == unit, scenario_name
    assert result["state"] == "POTENTIAL_NON_COMPLIANCE"
