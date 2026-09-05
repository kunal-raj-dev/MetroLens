"""
Bilingual Typography & Devanagari Script Support Engine
======================================================
Provides bilingual legal metrology terminology dictionaries, Hindi Devanagari
Unicode normalization, transliteration fallbacks, and safe ReportLab dual-script
formatting under Rule 6(3) of Legal Metrology (Packaged Commodities) Rules, 2011.

Rule 6(3) Statutory Mandate:
    "Every package shall bear the declarations in Hindi in Devanagari script or
    in English: Provided that the declarations may also be made in any one or
    more other languages in addition to Hindi or English."
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class BilingualTerm:
    """Represents an official statutory term in English, Hindi (Devanagari), and IAST Transliteration."""

    english: str
    hindi_devanagari: str
    hindi_transliteration: str
    statutory_rule_citation: str

    def format_heading(self, prefer_hindi: bool = False, use_transliteration: bool = False) -> str:
        """Format a dual-language heading suitable for court dossiers."""
        hindi_part = self.hindi_transliteration if use_transliteration else self.hindi_devanagari
        if prefer_hindi:
            return f"{hindi_part} / {self.english}"
        return f"{self.english} / {hindi_part}"


class BilingualTypographyEngine:
    """
    Manages dual Hindi-English typography and statutory terminology translation.
    """

    # Official Ministry of Consumer Affairs legal terminology mapping
    LEGAL_METROLOGY_VOCABULARY: Dict[str, BilingualTerm] = {
        "mrp": BilingualTerm(
            english="Maximum Retail Price (incl. of all taxes)",
            hindi_devanagari="अधिकतम खुदरा मूल्य (सभी करों सहित)",
            hindi_transliteration="Adhiktam Khudrā Mūlya (Sabhī Karōṅ Sahit)",
            statutory_rule_citation="Rule 6(1)(e)",
        ),
        "net_quantity": BilingualTerm(
            english="Net Quantity",
            hindi_devanagari="शुद्ध मात्रा",
            hindi_transliteration="Shuddh Mātrā",
            statutory_rule_citation="Rule 6(1)(c) & Rule 11",
        ),
        "manufacturer": BilingualTerm(
            english="Name and Address of Manufacturer / Packer",
            hindi_devanagari="निर्माता / पैकर का नाम एवं पता",
            hindi_transliteration="Nirmātā / Paikar kā Nām evaṁ Patā",
            statutory_rule_citation="Rule 6(1)(a)",
        ),
        "consumer_care": BilingualTerm(
            english="Consumer Care Details (Phone / Email)",
            hindi_devanagari="उपभोक्ता सेवा विवरण (दूरभाष / ईमेल)",
            hindi_transliteration="Upabhōktā Sēvā Vivaraṇ",
            statutory_rule_citation="Rule 6(1)(h)",
        ),
        "country_of_origin": BilingualTerm(
            english="Country of Origin",
            hindi_devanagari="उत्पत्ति का देश",
            hindi_transliteration="Utpatti kā Dēsh",
            statutory_rule_citation="Rule 6(1)(d)",
        ),
        "unit_sale_price": BilingualTerm(
            english="Unit Sale Price (USP)",
            hindi_devanagari="इकाई विक्रय मूल्य (यूएसपी)",
            hindi_transliteration="Ikāī Vikray Mūlya (USP)",
            statutory_rule_citation="Rule 6(1)(g) & GSR 881(E)",
        ),
        "date_of_manufacture": BilingualTerm(
            english="Date of Manufacture / Packing / Import",
            hindi_devanagari="निर्माण / पैकिंग / आयात की तिथि",
            hindi_transliteration="Nirmāṇ / Paikiṅg / Āyāt kī Tithi",
            statutory_rule_citation="Rule 6(1)(b)",
        ),
        "best_before": BilingualTerm(
            english="Best Before / Expiry Date",
            hindi_devanagari="सर्वोत्तम उपभोग तिथि / समाप्ति तिथि",
            hindi_transliteration="Sarvōttam Upabhōg Tithi / Samāpti Tithi",
            statutory_rule_citation="Rule 6(1)(f)",
        ),
        "improvement_notice": BilingualTerm(
            english="Improvement Notice under Section 36(1)",
            hindi_devanagari="धारा 36(1) के अंतर्गत सुधार नोटिस",
            hindi_transliteration="Dhārā 36(1) kē Antargat Sudhār Notice",
            statutory_rule_citation="Section 36(1) Jan Vishwas Act",
        ),
        "non_compliant": BilingualTerm(
            english="NON-COMPLIANT",
            hindi_devanagari="अननुपालक (दोषपूर्ण)",
            hindi_transliteration="Ananupālak (Dōṣapūrṇ)",
            statutory_rule_citation="Rule 32",
        ),
        "compliant": BilingualTerm(
            english="COMPLIANT",
            hindi_devanagari="अनुपालक (मानक अनुरूप)",
            hindi_transliteration="Anupālak (Mānak Anurūp)",
            statutory_rule_citation="Rule 32",
        ),
    }

    @classmethod
    def get_term(cls, term_key: str) -> Optional[BilingualTerm]:
        """Retrieve bilingual metadata by canonical term identifier."""
        return cls.LEGAL_METROLOGY_VOCABULARY.get(term_key.lower())

    @classmethod
    def format_bilingual_label(
        cls,
        term_key: str,
        prefer_transliteration_if_ascii_only: bool = True,
    ) -> str:
        """
        Format a safe bilingual label for PDF generation.
        If ReportLab is using standard Type1 Helvetica (ASCII only),
        returns English with Latin-transliterated Hindi to avoid missing glyph crashes.
        """
        term = cls.get_term(term_key)
        if not term:
            return term_key.replace("_", " ").title()

        if prefer_transliteration_if_ascii_only:
            return f"{term.english} [{term.hindi_transliteration}]"
        return f"{term.english} / {term.hindi_devanagari}"

    @classmethod
    def sanitize_for_pdf(cls, text: str) -> str:
        """
        Sanitize string for ReportLab Paragraph rendering:
        1. Replace Indian Rupee glyph ('₹') with 'Rs.'.
        2. Normalize Unicode (NFC).
        3. Escape XML/HTML special characters (&, <, >).
        """
        if not text:
            return ""

        # Normalize Unicode
        normalized = unicodedata.normalize("NFC", text)

        # Currency symbol replacement
        normalized = normalized.replace("₹", "Rs. ")
        normalized = normalized.replace("\u20B9", "Rs. ")

        # Clean non-printable control codes
        cleaned = "".join(ch for ch in normalized if ch == "\n" or ch == "\t" or ord(ch) >= 32)

        # XML entity escaping for ReportLab Paragraph
        cleaned = cleaned.replace("&", "&amp;")
        cleaned = cleaned.replace("<", "&lt;")
        cleaned = cleaned.replace(">", "&gt;")

        return cleaned

    @classmethod
    def create_statutory_declaration_row(
        cls,
        term_key: str,
        declared_value: Optional[str],
        is_compliant: bool,
        specific_defect: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Construct a structured declaration row with bilingual headings and statutory citation."""
        term = cls.get_term(term_key)
        label = term.format_heading(use_transliteration=True) if term else term_key.title()
        citation = term.statutory_rule_citation if term else "PCR 2011"

        return {
            "term_key": term_key,
            "bilingual_label": label,
            "citation": citation,
            "declared_value": declared_value or "NOT DETECTED",
            "is_compliant": is_compliant,
            "specific_defect": specific_defect,
        }
