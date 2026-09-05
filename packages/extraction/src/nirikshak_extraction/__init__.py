"""
Nirikshak Extraction: Parsing mandatory Legal Metrology Rule 6 declarations from OCR tokens.
"""

from typing import List, Dict, Optional, Any
import re
from nirikshak_shared.models.contracts import OCRObservation, DeclarationField
from nirikshak_shared.models.primitives import BoundingBox


def _contextual_numeric_normalize(text: str) -> str:
    """
    Contextually fixes common CTC visual glyph confusions in numeric substrings.
    Auditable: Only replaces 'O'->'0' and 'I'/'l'->'1' when adjacent to digits or decimal points.
    Preserves original raw text.
    """
    # Replace O with 0 when adjacent to digits or period
    text = re.sub(r'(?<=\d)O(?=\d|\b)', '0', text)
    text = re.sub(r'(?<=\b)O(?=\d)', '0', text)
    # Replace I or l with 1 when adjacent to digits or period
    text = re.sub(r'(?<=\d)[Il](?=\d|\b)', '1', text)
    text = re.sub(r'(?<=\b)[Il](?=\d)', '1', text)
    return text


class DeclarationExtractor:
    """Extracts statutory declaration entities from OCR observation tokens."""

    MANDATORY_FIELDS = [
        "mrp",
        "net_quantity",
        "mfg_date",
        "consumer_care",
        "country_of_origin",
    ]

    def extract_declarations(self, observations: List[OCRObservation]) -> Dict[str, DeclarationField]:
        """
        Processes OCR tokens using regex patterns and contextual normalization to extract
        mandatory declaration fields.
        """
        extracted: Dict[str, DeclarationField] = {}
        
        # 1. Evaluate per-token and joined full-text
        token_texts = [tok.text for tok in observations]
        full_text = " \n ".join(token_texts)

        # Helper to find source token ids and merged bounding box
        def find_sources(pattern: str) -> tuple[List[str], Optional[BoundingBox]]:
            matched_ids = []
            boxes = []
            for tok in observations:
                if re.search(pattern, tok.text, re.IGNORECASE):
                    matched_ids.append(tok.token_id)
                    boxes.append(tok.bounding_box)
            if not boxes:
                return matched_ids, None
            merged_box = BoundingBox(
                x_min=min(b.x_min for b in boxes),
                y_min=min(b.y_min for b in boxes),
                x_max=max(b.x_max for b in boxes),
                y_max=max(b.y_max for b in boxes),
            )
            return matched_ids, merged_box

        # --- A. MRP Declaration (Rule 6(1)(e)) ---
        mrp_pattern = r"(?:MRP|M\.R\.P\.?|Rs\.?|₹|अधिकतम\s*खुदरा\s*मूल्य)\s*[:.]?\s*(?:Rs\.?|₹)?\s*([0-9OIl]+(?:\.[0-9OIl]{1,2})?)"
        mrp_match = re.search(mrp_pattern, full_text, re.IGNORECASE)
        if mrp_match:
            raw_val_str = mrp_match.group(1)
            norm_val_str = _contextual_numeric_normalize(raw_val_str)
            try:
                amount_val = float(norm_val_str)
            except ValueError:
                amount_val = 0.0
            
            src_ids, box = find_sources(r"(?:MRP|M\.R\.P\.?|Rs\.?|₹|अधिकतम\s*खुदरा\s*मूल्य)")
            has_tax = bool(re.search(r"(?:incl(?:usive)?\s*(?:of)?\s*all\s*taxes|करों\s*सहित)", full_text, re.IGNORECASE))
            
            extracted["mrp"] = DeclarationField(
                field_name="mrp",
                raw_text=mrp_match.group(0).strip(),
                normalized_value={
                    "amount": amount_val,
                    "currency": "INR",
                    "tax_inclusive": has_tax,
                },
                confidence=0.95,
                source_token_ids=src_ids,
                bounding_box=box,
                is_mandatory=True,
                is_present=True,
            )
        else:
            extracted["mrp"] = DeclarationField(
                field_name="mrp",
                raw_text="",
                normalized_value=None,
                confidence=0.0,
                source_token_ids=[],
                bounding_box=None,
                is_mandatory=True,
                is_present=False,
            )

        # --- B. Net Quantity Declaration (Rule 6(1)(f)) ---
        net_qty_pattern = r"(?:Net\s*(?:Qty|Quantity|Weight|Wt|Vol|Volume)|शुद्ध\s*मात्रा)\s*[:.]?\s*([0-9OIl]+(?:\.[0-9OIl]+)?)\s*([a-zA-Z]+|pieces|units|N|U)\b"
        net_qty_match = re.search(net_qty_pattern, full_text, re.IGNORECASE)
        if net_qty_match:
            raw_mag_str = net_qty_match.group(1)
            unit_str = net_qty_match.group(2).lower()
            norm_mag_str = _contextual_numeric_normalize(raw_mag_str)
            try:
                mag_val = float(norm_mag_str)
            except ValueError:
                mag_val = 0.0
            
            src_ids, box = find_sources(r"(?:Net\s*(?:Qty|Quantity|Weight|Wt|Vol|Volume)|शुद्ध\s*मात्रा)")
            
            extracted["net_quantity"] = DeclarationField(
                field_name="net_quantity",
                raw_text=net_qty_match.group(0).strip(),
                normalized_value={
                    "magnitude": mag_val,
                    "unit": unit_str,
                },
                confidence=0.92,
                source_token_ids=src_ids,
                bounding_box=box,
                is_mandatory=True,
                is_present=True,
            )
        else:
            extracted["net_quantity"] = DeclarationField(
                field_name="net_quantity",
                raw_text="",
                normalized_value=None,
                confidence=0.0,
                source_token_ids=[],
                bounding_box=None,
                is_mandatory=True,
                is_present=False,
            )

        # --- C. Date of Manufacture/Packaging (Rule 6(1)(d)) ---
        date_pattern = r"(?:Mfg(?:\s*Date)?|PKD|Packed|Date\s*of\s*Pkg|पैकिंग\s*तिथि|उत्पादन\s*तिथि)\s*[:.]?\s*([0-1]?[0-9OIl][/.-][0-2]?[0-9OIl]{2,4})"
        date_match = re.search(date_pattern, full_text, re.IGNORECASE)
        if date_match:
            raw_date_str = date_match.group(1)
            norm_date_str = _contextual_numeric_normalize(raw_date_str)
            src_ids, box = find_sources(r"(?:Mfg|PKD|Packed|पैकिंग\s*तिथि|उत्पादन\s*तिथि)")
            
            extracted["mfg_date"] = DeclarationField(
                field_name="mfg_date",
                raw_text=date_match.group(0).strip(),
                normalized_value={"date_string": norm_date_str},
                confidence=0.90,
                source_token_ids=src_ids,
                bounding_box=box,
                is_mandatory=True,
                is_present=True,
            )
        else:
            extracted["mfg_date"] = DeclarationField(
                field_name="mfg_date",
                raw_text="",
                normalized_value=None,
                confidence=0.0,
                source_token_ids=[],
                bounding_box=None,
                is_mandatory=True,
                is_present=False,
            )

        # --- D. Consumer Care Details (Rule 6(1)(da)) ---
        care_pattern = r"(?:Consumer\s*Care|Customer\s*Care|Help\s*line|Care|उपभोक्ता\s*सेवा)\s*[:.]?\s*([^\n,]+)"
        care_match = re.search(care_pattern, full_text, re.IGNORECASE)
        email_or_phone = re.search(r"([\w.-]+@[\w.-]+\.\w+|1800[-\s]?\d{2,4}[-\s]?\d{3,4})", full_text)
        if care_match or email_or_phone:
            raw_str = care_match.group(0).strip() if care_match else email_or_phone.group(0).strip()
            contact_str = email_or_phone.group(0).strip() if email_or_phone else care_match.group(1).strip()
            src_ids, box = find_sources(r"(?:Consumer\s*Care|Customer\s*Care|Help\s*line|Care|उपभोक्ता\s*सेवा|@|1800)")
            
            extracted["consumer_care"] = DeclarationField(
                field_name="consumer_care",
                raw_text=raw_str,
                normalized_value={"contact": contact_str},
                confidence=0.88,
                source_token_ids=src_ids,
                bounding_box=box,
                is_mandatory=True,
                is_present=True,
            )
        else:
            extracted["consumer_care"] = DeclarationField(
                field_name="consumer_care",
                raw_text="",
                normalized_value=None,
                confidence=0.0,
                source_token_ids=[],
                bounding_box=None,
                is_mandatory=True,
                is_present=False,
            )

        # --- E. Country of Origin (Rule 6(10A)) ---
        origin_pattern = r"(?:Country\s*of\s*Origin|Made\s*in|Product\s*of)\s*[:.]?\s*([a-zA-Z\s]+)"
        origin_match = re.search(origin_pattern, full_text, re.IGNORECASE)
        if origin_match:
            country_name = origin_match.group(1).strip()
            src_ids, box = find_sources(r"(?:Country\s*of\s*Origin|Made\s*in|Product\s*of)")
            
            extracted["country_of_origin"] = DeclarationField(
                field_name="country_of_origin",
                raw_text=origin_match.group(0).strip(),
                normalized_value={"country": country_name},
                confidence=0.91,
                source_token_ids=src_ids,
                bounding_box=box,
                is_mandatory=True,
                is_present=True,
            )
        else:
            extracted["country_of_origin"] = DeclarationField(
                field_name="country_of_origin",
                raw_text="",
                normalized_value=None,
                confidence=0.0,
                source_token_ids=[],
                bounding_box=None,
                is_mandatory=False,
                is_present=False,
            )

        return extracted


__all__ = ["DeclarationExtractor", "DeclarationField", "_contextual_numeric_normalize"]
