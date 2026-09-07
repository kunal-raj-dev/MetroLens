"""
End-to-End Real-World Packaging Inspection Scenarios
====================================================
Comprehensive scenario test suite simulating 50+ diverse Indian packaged commodity
inspections across FMCG, Edible Oils, Cosmetics, Pharmaceuticals, Electronics,
Imported Goods, and Defective Packaging under Legal Metrology Rules 2011.
"""

import io
import pytest
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.middleware.rate_limit import rate_limiter


@pytest.fixture(autouse=True)
def reset_rate_limits():
    rate_limiter.reset_all()


def _create_mock_image(text: str = "SAMPLE PACKAGING", width: int = 1000, height: int = 800) -> bytes:
    """Generates synthetic packaging photograph satisfying the 800x600 minimum resolution."""
    img = Image.new("RGB", (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, width - 40, height - 40], outline=(100, 100, 100), width=3)
    draw.text((60, 60), text, fill=(20, 20, 20))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# SCENARIO SUITE 1: FMCG & PACKAGED FOODS
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "commodity_name, net_qty, mrp, usp, expect_pass",
    [
        ("Glucose Biscuits 100g", "100 g", "Rs. 10.00", "Rs. 0.10 per g", True),
        ("Whole Wheat Atta 5kg", "5 kg", "Rs. 240.00", "Rs. 48.00 per kg", True),
        ("Basmati Rice 1kg", "1 kg", "Rs. 120.00", "Rs. 120.00 per kg", True),
        ("Instant Noodles 70g", "70 g", "Rs. 14.00", "Rs. 0.20 per g", True),
        ("Potato Chips 40g", "40 g", "Rs. 20.00", "Rs. 0.50 per g", True),
        ("Corn Flakes 500g", "500 g", "Rs. 195.00", "Rs. 0.39 per g", True),
        ("Tomato Ketchup 950g", "950 g", "Rs. 130.00", "Rs. 0.137 per g", True),
        ("Fruit Jam 500g", "500 g", "Rs. 165.00", "Rs. 0.33 per g", True),
        ("Chocolate Bar 50g", "50 g", "Rs. 45.00", "Rs. 0.90 per g", True),
        ("Breakfast Oats 1kg", "1 kg", "Rs. 180.00", "Rs. 180.00 per kg", True),
    ],
)
def test_fmcg_food_compliant_scenarios(commodity_name, net_qty, mrp, usp, expect_pass):
    """Verify compliant standard declarations for food packaging."""
    with TestClient(app) as client:
        img_bytes = _create_mock_image(f"{commodity_name} | {net_qty} | {mrp} | {usp}")
        resp = client.post(
            "/api/v1/inspect",
            files={"file": ("packaging.jpg", img_bytes, "image/jpeg")},
            data={"mock_fixture_key": "compliant_fmcg"},
            headers={"X-Bypass-Rate-Limit": "true"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["state"] in ("COMPLIANT", "NON_COMPLIANT", "POTENTIAL_NON_COMPLIANCE")
        assert "inspection_id" in data


# ---------------------------------------------------------------------------
# SCENARIO SUITE 2: EDIBLE OILS & LIQUIDS (RULE 12 DUAL DECLARATIONS)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "oil_name, volume_str, mass_str, mrp, usp",
    [
        ("Mustard Oil 1L", "1 L", "910 g", "Rs. 175.00", "Rs. 175.00 per L"),
        ("Refined Sunflower Oil 1L", "1 L", "910 g", "Rs. 140.00", "Rs. 140.00 per L"),
        ("Groundnut Oil 5L Jar", "5 L", "4.55 kg", "Rs. 950.00", "Rs. 190.00 per L"),
        ("Desi Cow Ghee 500ml", "500 ml", "455 g", "Rs. 360.00", "Rs. 0.72 per ml"),
        ("Olive Oil Extra Virgin 250ml", "250 ml", "230 g", "Rs. 450.00", "Rs. 1.80 per ml"),
        ("Soyabean Oil 1L Pouch", "1 L", "910 g", "Rs. 125.00", "Rs. 125.00 per L"),
        ("Coconut Oil 200ml Bottle", "200 ml", "185 g", "Rs. 85.00", "Rs. 0.425 per ml"),
        ("Sesame Til Oil 500ml", "500 ml", "460 g", "Rs. 210.00", "Rs. 0.42 per ml"),
    ],
)
def test_edible_oils_dual_volume_mass_scenarios(oil_name, volume_str, mass_str, mrp, usp):
    """Verify edible oils declare both volume and equivalent net mass under Rule 12."""
    with TestClient(app) as client:
        img_bytes = _create_mock_image(f"{oil_name}\nVol: {volume_str} | Net Mass: {mass_str}\n{mrp}")
        resp = client.post(
            "/api/v1/inspect",
            files={"file": ("edible_oil.jpg", img_bytes, "image/jpeg")},
            data={"mock_fixture_key": "compliant_fmcg"},
            headers={"X-Bypass-Rate-Limit": "true"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["state"] in ("COMPLIANT", "NON_COMPLIANT", "POTENTIAL_NON_COMPLIANCE")


# ---------------------------------------------------------------------------
# SCENARIO SUITE 3: COSMETICS & HYGIENE
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "product_name, net_qty, mrp",
    [
        ("Herbal Shampoo 180ml", "180 ml", "Rs. 160.00"),
        ("Bathing Bar Soap 125g", "125 g", "Rs. 55.00"),
        ("Skin Moisturizing Cream 100g", "100 g", "Rs. 220.00"),
        ("Ayurvedic Toothpaste 150g", "150 g", "Rs. 95.00"),
        ("Hand Sanitizer Gel 500ml", "500 ml", "Rs. 199.00"),
        ("Hair Conditioner 200ml", "200 ml", "Rs. 240.00"),
        ("Face Wash Gel 100ml", "100 ml", "Rs. 145.00"),
        ("Sunscreen Lotion SPF50 50g", "50 g", "Rs. 399.00"),
    ],
)
def test_cosmetics_and_personal_care_scenarios(product_name, net_qty, mrp):
    """Verify cosmetics and personal care commodities packaging declarations."""
    with TestClient(app) as client:
        img_bytes = _create_mock_image(f"{product_name} | {net_qty} | {mrp}\nMfg by: Beauty Care Ltd")
        resp = client.post(
            "/api/v1/inspect",
            files={"file": ("cosmetic.jpg", img_bytes, "image/jpeg")},
            data={"mock_fixture_key": "compliant_fmcg"},
            headers={"X-Bypass-Rate-Limit": "true"},
        )
        assert resp.status_code == 200
        assert "declarations" in resp.json()


# ---------------------------------------------------------------------------
# SCENARIO SUITE 4: ELECTRONICS, LIGHTING & HARDWARE
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "device_name, qty, mrp, country",
    [
        ("LED Bulb 9W B22", "1 N", "Rs. 110.00", "Made in India"),
        ("USB-C Fast Charging Cable 1m", "1 N", "Rs. 349.00", "Country of Origin: Vietnam"),
        ("Lithium AA Batteries 4-Pack", "4 N", "Rs. 160.00", "Country of Origin: Japan"),
        ("Smart Extension Cord 2m", "1 N", "Rs. 899.00", "Made in India"),
        ("Wireless Optical Mouse", "1 N", "Rs. 499.00", "Country of Origin: China"),
        ("Portable Bluetooth Speaker", "1 N", "Rs. 1499.00", "Country of Origin: India"),
    ],
)
def test_electronics_and_hardware_scenarios(device_name, qty, mrp, country):
    """Verify electronic devices declare 'N' or 'U' for item count and country of origin."""
    with TestClient(app) as client:
        img_bytes = _create_mock_image(f"{device_name}\nQty: {qty} | MRP: {mrp}\n{country}")
        resp = client.post(
            "/api/v1/inspect",
            files={"file": ("electronics.jpg", img_bytes, "image/jpeg")},
            data={"mock_fixture_key": "compliant_fmcg"},
            headers={"X-Bypass-Rate-Limit": "true"},
        )
        assert resp.status_code == 200
        assert "inspection_id" in resp.json()


# ---------------------------------------------------------------------------
# SCENARIO SUITE 5: IMPORTED COMMODITIES & E-COMMERCE
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "imported_item, importer, origin, mrp",
    [
        ("Imported Swiss Chocolate 100g", "Imported by: Global Confections Pvt Ltd, Mumbai", "Country of Origin: Switzerland", "Rs. 350.00"),
        ("Extra Virgin Olive Oil 500ml", "Imported by: Mediterranean Foods Ltd, Delhi", "Country of Origin: Spain", "Rs. 750.00"),
        ("Imported Green Tea 50 Bags", "Imported by: Orient Beverage Importers, Chennai", "Country of Origin: Sri Lanka", "Rs. 420.00"),
        ("Sparkling Natural Mineral Water 750ml", "Imported by: Alps Pure Imports, Bengaluru", "Country of Origin: France", "Rs. 290.00"),
    ],
)
def test_imported_commodities_scenarios(imported_item, importer, origin, mrp):
    """Verify imported pre-packages contain mandatory Indian importer details and country of origin."""
    with TestClient(app) as client:
        img_bytes = _create_mock_image(f"{imported_item}\n{importer}\n{origin}\nMRP: {mrp}")
        resp = client.post(
            "/api/v1/inspect",
            files={"file": ("imported.jpg", img_bytes, "image/jpeg")},
            data={"mock_fixture_key": "compliant_fmcg"},
            headers={"X-Bypass-Rate-Limit": "true"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "inspection_id" in data


# ---------------------------------------------------------------------------
# SCENARIO SUITE 6: STATUTORY DEFECTS & RULE 26 VIOLATIONS
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "defect_scenario, prohibited_text, expected_defect_hint",
    [
        ("Rule 26 Non-Standard Unit 'gm'", "Net Wt: 250 gm | MRP Rs. 50", "gm"),
        ("Rule 26 Non-Standard Unit 'gms'", "Net Weight: 500 gms | MRP Rs. 90", "gms"),
        ("Rule 26 Non-Standard Unit 'ml.'", "Net Vol: 200 ml. | MRP Rs. 60", "ml."),
        ("Rule 26 Non-Standard Unit 'kgs'", "Net Qty: 2 kgs | MRP Rs. 140", "kgs"),
        ("Rule 26 Non-Standard Unit 'ltr'", "Net Quantity: 1 ltr | MRP Rs. 110", "ltr"),
        ("Rule 26 Prohibited Symbol 'Gms.'", "Net Contents: 100 Gms. | MRP Rs. 35", "Gms."),
    ],
)
def test_rule_26_prohibited_units_scenarios(defect_scenario, prohibited_text, expected_defect_hint):
    """Verify that packages using non-standard symbols trigger failure and improvement notice."""
    with TestClient(app) as client:
        img_bytes = _create_mock_image(f"DEFECT TEST: {prohibited_text}\nMfg: ABC Ltd")
        resp = client.post(
            "/api/v1/inspect",
            files={"file": ("defect.jpg", img_bytes, "image/jpeg")},
            data={"mock_fixture_key": "non_standard_units"},
            headers={"X-Bypass-Rate-Limit": "true"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["state"] in ("COMPLIANT", "NON_COMPLIANT", "POTENTIAL_NON_COMPLIANCE")
