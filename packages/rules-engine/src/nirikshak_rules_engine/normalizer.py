"""
Nirikshak Rules Engine: Deterministic Entity Normalizer.
Extracts and standardizes statutory declaration entities from raw OCR tokens,
applying CTC error repairs, regex token parsing, SI unit validation,
and category classification flags.
"""

import re
from typing import List, Dict, Any, Optional, Union
from .schemas import (
    CanonicalDeclaration,
    UnitType,
    OCRToken,
)


class TokenNormalizer:
    """
    Deterministic entity extraction and normalization pipeline.
    Parses OCR token streams into typed CanonicalDeclaration models without LLM inference.
    """

    # Prohibited or non-standard unit strings under Legal Metrology Rules
    PROHIBITED_UNITS = {"gms", "gm", "kgs", "ml_caps"}

    def __init__(self):
        # Pre-compile regex extractors for maximum evaluation speed (< 5ms)
        self._regex_mrp = re.compile(
            r"(?:MRP|M\.R\.P|PRICE|MRP\s*Rs|अधिकतम\s*खुदरा\s*मूल्य)\.?\s*[:.-]?\s*(?:₹|Rs\.?|INR)?\s*(\d+(?:\.\d{1,2})?)",
            re.IGNORECASE,
        )
        self._regex_currency_fallback = re.compile(
            r"(?:₹|Rs\.?|INR)\s*(\d+(?:\.\d{1,2})?)",
            re.IGNORECASE,
        )
        self._regex_tax_qualifier = re.compile(
            r"(?:inclusive\s*of\s*all\s*taxes|incl\.?\s*of\s*all\s*taxes|incl\.?\s*all\s*taxes|incl\.?\s*taxes|सभी\s*कर\s*सहित|कर\s*सहित)",
            re.IGNORECASE,
        )
        self._regex_net_qty = re.compile(
            r"(?:Net\s*(?:Quantity|Qty|Weight|Wt|Volume|Vol)|शुद्ध\s*मात्रा)\s*[:.-]?\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]+)",
            re.IGNORECASE,
        )
        self._regex_qty_fallback = re.compile(
            r"(\d+(?:\.\d+)?)\s*(g|kg|ml|l|m|cm|piece|pc|pcs|N)\b",
            re.IGNORECASE,
        )
        self._regex_usp = re.compile(
            r"(?:Unit\s*Sale\s*Price|USP|इकाई\s*विक्रय\s*मूल्य)\s*[:.-]?\s*(?:₹|Rs\.?|INR)?\s*(\d+(?:\.\d{1,2})?)\s*(?:/|per|प्रत्येक)?\s*([a-zA-Z]+)",
            re.IGNORECASE,
        )
        self._regex_mfg_date = re.compile(
            r"(?:Mfg(?:\s*Date)?|MFG|PKD|Packed|Date\s*of\s*Packing|पैकिंग\s*तिथि|उत्पादन\s*तिथि)\s*[:.-]?\s*(\d{1,2})[/\-.](\d{2,4})",
            re.IGNORECASE,
        )
        self._regex_mfg_date_fallback = re.compile(
            r"\b(0[1-9]|1[0-2])[/\-.](20\d{2}|\d{2})\b"
        )
        self._regex_mfr = re.compile(
            r"(?:Manufactured\s*By|Mfg\s*By|Packed\s*By|Mfr|उत्पादक|निर्माता)\s*[:.-]?\s*([^,\n]+(?:,[^,\n]+)?)",
            re.IGNORECASE,
        )
        self._regex_pincode = re.compile(r"(?<!\d)([1-9]\d{5})(?!\d)")
        self._regex_email = re.compile(
            r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        )
        self._regex_phone = re.compile(
            r"(?:1800[-\s]?\d{2,3}[-\s]?\d{3,4}|(?:\+?91[-\s]?)?[6-9]\d{9}|0\d{2,4}[-\s]?\d{6,8})"
        )
        self._regex_coo = re.compile(
            r"(?:Country\s*of\s*Origin|Made\s*in|Product\s*of)\s*[:.-]?\s*([A-Za-z\s]+)",
            re.IGNORECASE,
        )

    def repair_ctc_confusions(self, text: str) -> str:
        """
        Repairs common OCR CTC character confusions in numeric & currency contexts.
        Example: 'MRP Rs. 2O5.OO' -> 'MRP Rs. 205.00'
                 'Net Qty: l000 g' -> 'Net Qty: 1000 g'
        """
        # Replace O/o with 0 when adjacent to digits or decimal points
        cleaned = re.sub(r"(?<=\d)[Oo](?=\d|\.|$)", "0", text)
        cleaned = re.sub(r"(?<=[₹RsINR:\s])[Oo](?=\d)", "0", cleaned)
        cleaned = re.sub(r"(?<=\d\.)[Oo]+", lambda m: "0" * len(m.group(0)), cleaned)
        
        # Replace l/I with 1 when adjacent to digits or decimal points
        cleaned = re.sub(r"(?<=\d)[lI](?=\d|\.|$)", "1", cleaned)
        cleaned = re.sub(r"(?<=[₹RsINR:\s])[lI](?=\d)", "1", cleaned)
        cleaned = re.sub(r"(?<=\s)[lI](?=\d{2,})", "1", cleaned)

        # Fix spaces around commas in decimal prices/quantities: '245 , 00' -> '245.00'
        cleaned = re.sub(r"(\d+)\s*,\s*(\d{2})\b", r"\1.\2", cleaned)
        
        return cleaned

    def normalize(
        self, tokens: Union[List[OCRToken], List[Dict[str, Any]], List[Any], str]
    ) -> CanonicalDeclaration:
        """
        Parses tokens into a typed CanonicalDeclaration.
        Supports OCRToken objects, token dicts, or raw string input.
        """
        if isinstance(tokens, str):
            token_texts = [tokens]
        elif isinstance(tokens, list):
            token_texts = []
            for t in tokens:
                if isinstance(t, str):
                    token_texts.append(t)
                elif isinstance(t, dict):
                    token_texts.append(str(t.get("text", "")))
                elif hasattr(t, "text"):
                    token_texts.append(str(t.text))
        else:
            token_texts = []

        if not token_texts:
            return CanonicalDeclaration()

        # Join full text and apply CTC repairs
        full_raw_text = "\n".join(token_texts)
        full_cleaned_text = "\n".join(self.repair_ctc_confusions(t) for t in token_texts)

        decl = CanonicalDeclaration()

        # 1. Extract MRP and Tax Qualifier
        mrp_match = self._regex_mrp.search(full_cleaned_text)
        if mrp_match:
            try:
                decl.mrp_inr = float(mrp_match.group(1))
            except ValueError:
                pass
        else:
            # Fallback to general currency symbol search
            curr_match = self._regex_currency_fallback.search(full_cleaned_text)
            if curr_match:
                try:
                    decl.mrp_inr = float(curr_match.group(1))
                except ValueError:
                    pass

        decl.tax_qualifier_present = bool(self._regex_tax_qualifier.search(full_cleaned_text))

        # 2. Extract Net Quantity
        qty_match = self._regex_net_qty.search(full_cleaned_text)
        if qty_match:
            try:
                decl.net_quantity_value = float(qty_match.group(1))
                raw_unit = qty_match.group(2).strip()
                decl.raw_net_quantity_unit = raw_unit
                if raw_unit in ["Gms", "gms", "GM", "gm", "Kgs", "kgs", "ML", "Ml"]:
                    decl.has_non_standard_unit = True
                decl.net_quantity_unit = UnitType.from_string(raw_unit)
            except ValueError:
                pass
        else:
            # Fallback for standalone quantity patterns
            fallback_match = self._regex_qty_fallback.search(full_cleaned_text)
            if fallback_match:
                try:
                    decl.net_quantity_value = float(fallback_match.group(1))
                    raw_unit = fallback_match.group(2).strip()
                    decl.raw_net_quantity_unit = raw_unit
                    if raw_unit in ["Gms", "gms", "GM", "gm", "Kgs", "kgs", "ML", "Ml"]:
                        decl.has_non_standard_unit = True
                    decl.net_quantity_unit = UnitType.from_string(raw_unit)
                except ValueError:
                    pass

        # 3. Extract Declared Unit Sale Price (USP)
        usp_match = self._regex_usp.search(full_cleaned_text)
        if usp_match:
            try:
                decl.declared_usp_value = float(usp_match.group(1))
                decl.declared_usp_unit = usp_match.group(2).strip().lower()
            except ValueError:
                pass

        # 4. Extract Manufacturing Date (Month / Year)
        date_match = self._regex_mfg_date.search(full_cleaned_text)
        if date_match:
            month = int(date_match.group(1))
            year = int(date_match.group(2))
            if year < 100:
                year += 2000
            if 1 <= month <= 12:
                decl.mfg_month = month
                decl.mfg_year = year
        else:
            fallback_date = self._regex_mfg_date_fallback.search(full_cleaned_text)
            if fallback_date:
                month = int(fallback_date.group(1))
                year = int(fallback_date.group(2))
                if year < 100:
                    year += 2000
                if 1 <= month <= 12:
                    decl.mfg_month = month
                    decl.mfg_year = year

        # 5. Extract Manufacturer Name & Address
        mfr_match = self._regex_mfr.search(full_cleaned_text)
        if mfr_match:
            decl.manufacturer_name = mfr_match.group(1).strip()
            decl.manufacturer_address = decl.manufacturer_name

        # 6. Extract Postal Pincode
        pin_match = self._regex_pincode.search(full_cleaned_text)
        if pin_match:
            decl.manufacturer_pincode = pin_match.group(1)

        # 7. Extract Consumer Care Grievance Contacts
        email_match = self._regex_email.search(full_cleaned_text)
        if email_match:
            decl.consumer_care_email = email_match.group(0).strip()

        phone_match = self._regex_phone.search(full_cleaned_text)
        if phone_match:
            decl.consumer_care_phone = phone_match.group(0).strip()

        # 8. Extract Country of Origin
        coo_match = self._regex_coo.search(full_cleaned_text)
        if coo_match:
            coo_val = coo_match.group(1).strip().strip(".,- ")
            # Take only the first word or country phrase (e.g. 'India')
            decl.country_of_origin = coo_val.split()[0] if coo_val else "India"

        # 9. Extract Commodity Name (heuristic: first non-declaration line)
        for line in token_texts:
            s = line.strip()
            if not s:
                continue
            lower_s = s.lower()
            if not any(
                k in lower_s
                for k in [
                    "mrp",
                    "net",
                    "mfg",
                    "pkd",
                    "care",
                    "consumer",
                    "unit sale",
                    "country",
                    "made in",
                    "₹",
                    "rs.",
                    "शुद्ध",
                    "मूल्य",
                ]
            ):
                decl.commodity_name = s
                break

        # 10. Classify Statutory Category Flags
        lower_full = full_raw_text.lower()
        # Pan Masala & Tobacco carve-out under G.S.R. 881(E)
        if any(
            k in lower_full
            for k in [
                "pan masala",
                "gutkha",
                "gutka",
                "tobacco",
                "zarda",
                "khaini",
                "bidi",
                "cigarette",
            ]
        ):
            decl.is_pan_masala_or_tobacco = True

        # Wholesale bulk package exclusion (> 25kg/L) under Rule 3
        if decl.net_quantity_value is not None and decl.net_quantity_unit in [
            UnitType.KILOGRAM,
            UnitType.LITER,
        ]:
            if decl.net_quantity_value > 25.0:
                decl.is_wholesale_or_bulk = True

        if any(
            k in lower_full
            for k in ["wholesale", "industrial use", "institutional pack", "not for retail sale"]
        ):
            decl.is_wholesale_or_bulk = True

        return decl
