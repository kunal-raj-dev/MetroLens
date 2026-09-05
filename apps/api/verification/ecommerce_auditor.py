"""
E-Commerce Marketplace & Quick-Commerce Packaging Compliance Auditor
===================================================================
Validates digital product display pages (PDPs) and quick-commerce listings
against Rule 6(10) of the Legal Metrology (Packaged Commodities) Rules, 2011,
the Consumer Protection (E-Commerce) Rules, 2020, and CCPA Dark Pattern Guidelines.

Statutory Mandate (Rule 6(10) & 6(11)):
    "Every e-commerce entity shall ensure that the mandatory declarations specified
    in sub-rule (1) of rule 6, along with the Unit Sale Price (USP), are displayed
    on the digital and electronic network used for e-commerce transactions."

Dark Pattern Detection (CCPA Guidelines, 2023):
    1. False Urgency: Artificial scarcity timers on standard FMCG commodities.
    2. Basket Sneaking: Automatic inclusion of optional add-ons / carry bags.
    3. Drip Pricing: Concealing non-optional processing fees until the payment stage.
    4. Hidden Unit Sale Price: Presenting large MRP while concealing USP.
"""

from __future__ import annotations

import datetime
import enum
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


class DarkPatternType(str, enum.Enum):
    """Classifications under Central Consumer Protection Authority (CCPA) Guidelines, 2023."""

    FALSE_URGENCY = "FALSE_URGENCY"            # "Only 1 left!", artificial countdown timer
    BASKET_SNEAKING = "BASKET_SNEAKING"        # Automatic addition of donation/handling/bag fee
    DRIP_PRICING = "DRIP_PRICING"              # Unannounced delivery/convenience fees added at final step
    HIDDEN_USP = "HIDDEN_USP"                  # Unit Sale Price absent or printed in unreadable micro-font
    CONFIRMACTION_SHAMING = "CONFIRM_SHAMING"  # Guilt-inducing opt-out buttons ("No, I hate saving money")
    TRICK_PRICING = "TRICK_PRICING"            # Misleading comparison strike-through prices


class ECommercePlatformType(str, enum.Enum):
    MARKETPLACE = "MARKETPLACE"                # Amazon, Flipkart
    QUICK_COMMERCE = "QUICK_COMMERCE"          # Blinkit, Zepto, Instamart, Swiggy
    VERTICAL_GROCERY = "VERTICAL_GROCERY"      # BigBasket, JioMart
    DIRECT_TO_CONSUMER = "D2C_BRAND"           # Brand official webstore


@dataclass(frozen=True)
class DarkPatternFinding:
    """Represents a discovered deceptive design practice on the e-commerce listing."""

    pattern_type: DarkPatternType
    severity: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    element_snippet: str
    statutory_violation: str
    remediation_required: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_type": self.pattern_type.value,
            "severity": self.severity,
            "element_snippet": self.element_snippet,
            "statutory_violation": self.statutory_violation,
            "remediation_required": self.remediation_required,
        }


@dataclass(frozen=True)
class DigitalPDPDeclarations:
    """Structured fields extracted from an e-commerce Product Display Page."""

    title: str
    declared_mrp: Optional[float] = None
    declared_selling_price: Optional[float] = None
    declared_usp: Optional[float] = None
    usp_unit_denominator: Optional[str] = None
    net_quantity_str: Optional[str] = None
    country_of_origin: Optional[str] = None
    manufacturer_details: Optional[str] = None
    packer_details: Optional[str] = None
    importer_details: Optional[str] = None
    consumer_care_details: Optional[str] = None
    expiry_or_best_before: Optional[str] = None
    is_imported: bool = False
    raw_text_payload: str = ""


@dataclass(frozen=True)
class ECommerceAuditResult:
    """Comprehensive compliance assessment of an e-commerce commodity listing."""

    is_compliant: bool
    platform_type: ECommercePlatformType
    listing_title: str
    missing_mandatory_declarations: List[str]
    rule6_10_compliant: bool
    usp_rule6_11_compliant: bool
    dark_patterns_detected: List[DarkPatternFinding] = field(default_factory=list)
    statutory_defects: List[str] = field(default_factory=list)
    statutory_citations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_compliant": self.is_compliant,
            "platform_type": self.platform_type.value,
            "listing_title": self.listing_title,
            "missing_mandatory_declarations": self.missing_mandatory_declarations,
            "rule6_10_compliant": self.rule6_10_compliant,
            "usp_rule6_11_compliant": self.usp_rule6_11_compliant,
            "dark_patterns_count": len(self.dark_patterns_detected),
            "dark_patterns": [dp.to_dict() for dp in self.dark_patterns_detected],
            "statutory_defects": self.statutory_defects,
            "statutory_citations": self.statutory_citations,
        }


class ECommerceMarketplaceComplianceAuditor:
    """
    Audits e-commerce listings against Rule 6(10) & 6(11) and Consumer Protection rules.
    """

    # False Urgency triggers
    URGENCY_REGEX = re.compile(
        r"(only\s+\d+\s+left\b|hurry\b|deal\s+expires\s+in|ends\s+in\s+\d+\s*(?:m|min|s|sec|hours)|flash\s+sale\s+ending)",
        re.IGNORECASE,
    )

    # Basket Sneaking triggers
    BASKET_SNEAK_REGEX = re.compile(
        r"(convenience\s+fee|handling\s+charge|packaging\s+charge|bag\s+fee|tip\s+for\s+partner)",
        re.IGNORECASE,
    )

    # Confirm Shaming triggers
    SHAMING_REGEX = re.compile(
        r"(no,\s*i\s*don['’]t\s*want\s*to\s*save|i\s*prefer\s*paying\s*full\s*price|no\s*thanks,\s*i\s*hate\s*deals)",
        re.IGNORECASE,
    )

    def audit_listing(
        self,
        pdp: DigitalPDPDeclarations,
        platform: ECommercePlatformType = ECommercePlatformType.MARKETPLACE,
        announced_price_breakdown: Optional[Dict[str, float]] = None,
    ) -> ECommerceAuditResult:
        """
        Audit a digital product display page.

        Args:
            pdp: DigitalPDPDeclarations object.
            platform: Platform classification.
            announced_price_breakdown: Price items at final cart checkout (for drip pricing check).
        """
        missing: List[str] = []
        defects: List[str] = []
        citations: List[str] = []
        dark_findings: List[DarkPatternFinding] = []

        # 1. Rule 6(10) Mandatory Declarations Audit
        if not pdp.declared_mrp or pdp.declared_mrp <= 0.0:
            missing.append("Maximum Retail Price (MRP)")
            defects.append("Listing fails to declare statutory Maximum Retail Price (MRP).")
            citations.append("Rule 6(1)(e) read with Rule 6(10)")

        if not pdp.net_quantity_str:
            missing.append("Net Quantity")
            defects.append("Listing fails to declare standardized net quantity.")
            citations.append("Rule 6(1)(c) read with Rule 6(10)")

        if not pdp.country_of_origin:
            missing.append("Country of Origin")
            defects.append("Country of Origin omitted from digital listing. Violation of Rule 6(10).")
            citations.append("Rule 6(1)(d) read with Rule 6(10)")

        if not pdp.manufacturer_details and not pdp.packer_details:
            missing.append("Manufacturer or Packer Details")
            defects.append("Manufacturer or packer legal identity and postal address omitted.")
            citations.append("Rule 6(1)(a) read with Rule 6(10)")

        if not pdp.consumer_care_details:
            missing.append("Consumer Care Details")
            defects.append("Consumer grievance redressal email or phone number omitted.")
            citations.append("Rule 6(1)(h) read with Rule 6(10)")

        if pdp.is_imported and not pdp.importer_details:
            missing.append("Indian Importer Name and Address")
            defects.append("Imported commodity listing lacks Indian importer legal metrology details.")
            citations.append("Rule 6(1)(a) read with Rule 6(10)")

        rule6_10_pass = len(missing) == 0

        # 2. Rule 6(11) Unit Sale Price (USP) Audit
        usp_pass = True
        if pdp.declared_usp is None or pdp.declared_usp <= 0.0:
            usp_pass = False
            defects.append(
                "Digital listing fails to display statutory Unit Sale Price (USP). Violation of GSR 881(E)."
            )
            citations.append("Rule 6(11) (Unit Sale Price Mandate)")
            dark_findings.append(
                DarkPatternFinding(
                    pattern_type=DarkPatternType.HIDDEN_USP,
                    severity="HIGH",
                    element_snippet="MRP displayed without adjoining Unit Sale Price",
                    statutory_violation="Rule 6(11) of Legal Metrology (Packaged Commodities) Rules, 2011",
                    remediation_required="Display Unit Sale Price in bold adjacent to MRP on digital shelf.",
                )
            )

        # 3. Dark Pattern Scans (CCPA 2023 Guidelines)
        raw_text = pdp.raw_text_payload or f"{pdp.title} {pdp.net_quantity_str or ''}"

        # False Urgency Check
        urgency_match = self.URGENCY_REGEX.search(raw_text)
        if urgency_match:
            dark_findings.append(
                DarkPatternFinding(
                    pattern_type=DarkPatternType.FALSE_URGENCY,
                    severity="MEDIUM",
                    element_snippet=urgency_match.group(0),
                    statutory_violation="CCPA Dark Pattern Guidelines 2023, Section 4",
                    remediation_required="Cease artificial urgency cues on standard pre-packaged staples.",
                )
            )
            defects.append(f"Deceptive False Urgency detected: '{urgency_match.group(0)}'.")

        # Confirm Shaming Check
        shaming_match = self.SHAMING_REGEX.search(raw_text)
        if shaming_match:
            dark_findings.append(
                DarkPatternFinding(
                    pattern_type=DarkPatternType.CONFIRMACTION_SHAMING,
                    severity="LOW",
                    element_snippet=shaming_match.group(0),
                    statutory_violation="CCPA Dark Pattern Guidelines 2023, Section 7",
                    remediation_required="Provide neutral opt-out language.",
                )
            )

        # Drip Pricing Check (if checkout breakdown provided)
        if announced_price_breakdown and pdp.declared_selling_price:
            base_p = pdp.declared_selling_price
            final_p = announced_price_breakdown.get("total_payable", base_p)
            unannounced_fees = final_p - base_p

            if unannounced_fees > (base_p * 0.15) and unannounced_fees > 20.0:
                dark_findings.append(
                    DarkPatternFinding(
                        pattern_type=DarkPatternType.DRIP_PRICING,
                        severity="CRITICAL",
                        element_snippet=f"Base: Rs.{base_p} -> Final: Rs.{final_p} (+Rs.{unannounced_fees:.2f})",
                        statutory_violation="CCPA Dark Pattern Guidelines 2023, Section 6",
                        remediation_required="Incorporate all mandatory handling charges into primary displayed price.",
                    )
                )
                defects.append(
                    f"Drip Pricing identified: Unannounced charges (+Rs.{unannounced_fees:.2f}) added at final payment step."
                )

        # Overall Verdict
        is_overall_compliant = rule6_10_pass and usp_pass and len(dark_findings) == 0

        return ECommerceAuditResult(
            is_compliant=is_overall_compliant,
            platform_type=platform,
            listing_title=pdp.title,
            missing_mandatory_declarations=missing,
            rule6_10_compliant=rule6_10_pass,
            usp_rule6_11_compliant=usp_pass,
            dark_patterns_detected=dark_findings,
            statutory_defects=defects,
            statutory_citations=list(set(citations)),
        )
