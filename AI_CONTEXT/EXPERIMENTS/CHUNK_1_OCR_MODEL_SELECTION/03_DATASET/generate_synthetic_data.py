"""
Controlled Synthetic Test Specimen Generator for Chunk 1 OCR Spike.
Generates 8 standardized test packaging labels covering:
1. English Standard FMCG (Parle-G style)
2. Hindi Standard FMCG (Atta / Biscuit style)
3. Bilingual Mixed Packaging (English + Hindi)
4. Unit Sale Price & Microscopic Font (Shrinkflation test)
5. Personal Care Bottle (Liquid Volume + Contact Info)
6. Non-Metric Prohibited Units ("Gms", "ML")
7. Blank / No-Text Failure Mode
8. Low-Contrast Faded Expiry Date Stamp
All images are explicitly stamped: 'SYNTHETIC TEST — NOT REAL PACKAGING'
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont

DATASET_DIR = "AI_CONTEXT/EXPERIMENTS/CHUNK_1_OCR_MODEL_SELECTION/03_DATASET"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# Load fonts
FONT_PATH_HINDI = "C:/Windows/Fonts/Nirmala.ttc"
try:
    font_en_large = ImageFont.truetype("arial.ttf", 28)
    font_en_medium = ImageFont.truetype("arial.ttf", 22)
    font_en_small = ImageFont.truetype("arial.ttf", 16)
    font_hi_large = ImageFont.truetype(FONT_PATH_HINDI, 26)
    font_hi_medium = ImageFont.truetype(FONT_PATH_HINDI, 22)
except Exception:
    font_en_large = ImageFont.load_default()
    font_en_medium = ImageFont.load_default()
    font_en_small = ImageFont.load_default()
    font_hi_large = font_en_large
    font_hi_medium = font_en_medium

test_cases = [
    {
        "id": "SYNTH-01-ENG-FMCG",
        "title": "Standard English Biscuit Packaging",
        "language": "en",
        "package_type": "biscuit_pouch",
        "resolution": (640, 360),
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "lines": [
            ("SYNTHETIC TEST - NOT REAL PACKAGING", font_en_small, (150, 150, 150)),
            ("MRP Rs. 20.00 (inclusive of all taxes)", font_en_large, (0, 0, 0)),
            ("Net Qty: 65 g", font_en_medium, (0, 0, 0)),
            ("Unit Sale Price: Rs. 0.31 / g", font_en_medium, (0, 0, 0)),
            ("Mfg Date: 08/2026", font_en_medium, (0, 0, 0)),
            ("Consumer Care: 1800-222-4444 or care@biscuit.in", font_en_small, (0, 0, 0)),
        ],
        "ground_truth": {
            "mrp": "20.00",
            "net_quantity": "65 g",
            "usp": "0.31 / g",
            "date": "08/2026",
            "contact": "1800-222-4444"
        }
    },
    {
        "id": "SYNTH-02-HIN-FMCG",
        "title": "Pure Hindi Packaging Label",
        "language": "hi",
        "package_type": "atta_bag",
        "resolution": (640, 360),
        "bg_color": (250, 248, 240),
        "text_color": (0, 0, 0),
        "lines": [
            ("SYNTHETIC TEST - NOT REAL PACKAGING", font_en_small, (150, 150, 150)),
            ("अधिकतम खुदरा मूल्य: 245.00", font_hi_large, (0, 0, 0)),
            ("निवल मात्रा: 5 किग्रा", font_hi_medium, (0, 0, 0)),
            ("पैकिंग की तारीख: 05/2026", font_hi_medium, (0, 0, 0)),
            ("उपभोक्ता सेवा: care@atta.in", font_en_small, (0, 0, 0)),
        ],
        "ground_truth": {
            "mrp": "245.00",
            "net_quantity": "5 किग्रा",
            "usp": None,
            "date": "05/2026",
            "contact": "care@atta.in"
        }
    },
    {
        "id": "SYNTH-03-MIXED-BILINGUAL",
        "title": "Bilingual FMCG Packaging (English + Hindi)",
        "language": "mixed",
        "package_type": "snack_carton",
        "resolution": (640, 380),
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "lines": [
            ("SYNTHETIC TEST - NOT REAL PACKAGING", font_en_small, (150, 150, 150)),
            ("MRP / अधिकतम खुदरा मूल्य: Rs. 50.00", font_hi_medium, (0, 0, 0)),
            ("Net Qty / निवल मात्रा: 150 g", font_hi_medium, (0, 0, 0)),
            ("USP: Rs. 0.33 per g", font_en_medium, (0, 0, 0)),
            ("Best Before: 12/2026", font_en_medium, (0, 0, 0)),
            ("Customer Care: support@snack.com", font_en_small, (0, 0, 0)),
        ],
        "ground_truth": {
            "mrp": "50.00",
            "net_quantity": "150 g",
            "usp": "0.33 per g",
            "date": "12/2026",
            "contact": "support@snack.com"
        }
    },
    {
        "id": "SYNTH-04-MICRO-FONT",
        "title": "Shrinkflation Microscopic Numeral Deficit",
        "language": "en",
        "package_type": "confectionery_pouch",
        "resolution": (640, 320),
        "bg_color": (245, 245, 245),
        "text_color": (0, 0, 0),
        "lines": [
            ("SYNTHETIC TEST - NOT REAL PACKAGING", font_en_small, (150, 150, 150)),
            ("MRP Rs. 10.00 incl. of all taxes", font_en_medium, (0, 0, 0)),
            ("Net Weight: 35g", font_en_small, (0, 0, 0)),
            ("Unit Sale Price: Rs. 0.28/g", font_en_small, (0, 0, 0)),
            ("Mfg: 07/2026", font_en_small, (0, 0, 0)),
        ],
        "ground_truth": {
            "mrp": "10.00",
            "net_quantity": "35g",
            "usp": "0.28/g",
            "date": "07/2026",
            "contact": None
        }
    },
    {
        "id": "SYNTH-05-LIQUID-VOLUME",
        "title": "Personal Care Bottle (Liquid Volume in ml)",
        "language": "en",
        "package_type": "handwash_bottle",
        "resolution": (640, 360),
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "lines": [
            ("SYNTHETIC TEST - NOT REAL PACKAGING", font_en_small, (150, 150, 150)),
            ("Maximum Retail Price: Rs. 125.00", font_en_large, (0, 0, 0)),
            ("Net Volume: 250 ml", font_en_large, (0, 0, 0)),
            ("Unit Sale Price: Rs. 0.50/ml", font_en_medium, (0, 0, 0)),
            ("Expiry: 04/2028 Batch B-902", font_en_medium, (0, 0, 0)),
            ("Helpline: 1800-100-9999", font_en_small, (0, 0, 0)),
        ],
        "ground_truth": {
            "mrp": "125.00",
            "net_quantity": "250 ml",
            "usp": "0.50/ml",
            "date": "04/2028",
            "contact": "1800-100-9999"
        }
    },
    {
        "id": "SYNTH-06-PROHIBITED-UNITS",
        "title": "Packaging with Prohibited Pluralized Units (Gms, ML)",
        "language": "en",
        "package_type": "detergent_pouch",
        "resolution": (640, 320),
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "lines": [
            ("SYNTHETIC TEST - NOT REAL PACKAGING", font_en_small, (150, 150, 150)),
            ("MRP Rs. 85/- (inclusive all taxes)", font_en_medium, (0, 0, 0)),
            ("Net Wt: 500 Gms", font_en_medium, (0, 0, 0)),
            ("Vol: 1000 ML", font_en_medium, (0, 0, 0)),
            ("Mfg: 01/2026", font_en_medium, (0, 0, 0)),
        ],
        "ground_truth": {
            "mrp": "85",
            "net_quantity": "500 Gms",
            "usp": None,
            "date": "01/2026",
            "contact": None
        }
    },
    {
        "id": "SYNTH-07-BLANK-FRAME",
        "title": "Blank / Texture-Only Failure Mode Frame",
        "language": "none",
        "package_type": "blank_cardboard",
        "resolution": (640, 320),
        "bg_color": (230, 220, 200),
        "text_color": (0, 0, 0),
        "lines": [],
        "ground_truth": {
            "mrp": None,
            "net_quantity": None,
            "usp": None,
            "date": None,
            "contact": None
        }
    },
    {
        "id": "SYNTH-08-LOW-CONTRAST-FADED",
        "title": "Low-Contrast Faded Expiry Stamp",
        "language": "en",
        "package_type": "foil_crimp",
        "resolution": (640, 320),
        "bg_color": (220, 220, 220),
        "text_color": (160, 160, 160),
        "lines": [
            ("SYNTHETIC TEST - NOT REAL PACKAGING", font_en_small, (180, 180, 180)),
            ("MRP Rs. 30.00", font_en_medium, (140, 140, 140)),
            ("NET: 40 g", font_en_medium, (140, 140, 140)),
            ("EXP 11/2026", font_en_small, (160, 160, 160)),
        ],
        "ground_truth": {
            "mrp": "30.00",
            "net_quantity": "40 g",
            "usp": None,
            "date": "11/2026",
            "contact": None
        }
    }
]

manifest = []

for case in test_cases:
    img = Image.new("RGB", case["resolution"], color=case["bg_color"])
    draw = ImageDraw.Draw(img)
    y_offset = 25
    for text, font, color in case["lines"]:
        draw.text((30, y_offset), text, fill=color, font=font)
        y_offset += 45
    
    file_path = os.path.join(IMAGES_DIR, f"{case['id']}.png")
    img.save(file_path)
    
    manifest.append({
        "id": case["id"],
        "title": case["title"],
        "language": case["language"],
        "package_type": case["package_type"],
        "file_path": file_path,
        "resolution": case["resolution"],
        "is_synthetic": True,
        "disclaimer": "SYNTHETIC TEST — NOT REAL PACKAGING",
        "ground_truth": case["ground_truth"]
    })

manifest_path = os.path.join(DATASET_DIR, "manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Generated {len(manifest)} synthetic test specimens in {IMAGES_DIR}")
print(f"Manifest written to {manifest_path}")
