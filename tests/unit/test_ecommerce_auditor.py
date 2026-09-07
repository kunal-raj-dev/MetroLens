"""
Unit Tests for E-Commerce Marketplace & Dark-Pattern Compliance Auditor
=======================================================================
Verifies Rule 6(10) mandatory e-commerce declarations, Rule 6(11) Unit Sale Price,
and CCPA 2023 dark patterns (false urgency, drip pricing, confirm shaming).
"""

import pytest

from apps.api.verification.ecommerce_auditor import (
    ECommerceMarketplaceComplianceAuditor,
    DigitalPDPDeclarations,
    ECommercePlatformType,
    DarkPatternType,
)


def test_ecommerce_compliant_listing():
    """Verify clean e-commerce listing containing all mandatory declarations and valid USP."""
    auditor = ECommerceMarketplaceComplianceAuditor()

    pdp = DigitalPDPDeclarations(
        title="Organic Whole Wheat Flour 5kg",
        declared_mrp=280.0,
        declared_selling_price=245.0,
        declared_usp=49.0,
        usp_unit_denominator="kg",
        net_quantity_str="5 kg",
        country_of_origin="India",
        manufacturer_details="Organic Grains Ltd, Indore, MP - 452001",
        consumer_care_details="care@organicgrains.in | 1800-111-222",
        expiry_or_best_before="Best before 6 months from packaging",
    )

    result = auditor.audit_listing(pdp, platform=ECommercePlatformType.MARKETPLACE)

    assert result.is_compliant is True
    assert result.rule6_10_compliant is True
    assert result.usp_rule6_11_compliant is True
    assert len(result.dark_patterns_detected) == 0
    assert len(result.missing_mandatory_declarations) == 0


def test_ecommerce_missing_country_of_origin_and_usp():
    """Verify detection of missing country of origin and hidden USP on marketplace listing."""
    auditor = ECommerceMarketplaceComplianceAuditor()

    pdp = DigitalPDPDeclarations(
        title="Wireless Headphones Pro",
        declared_mrp=1999.0,
        declared_selling_price=1499.0,
        declared_usp=None,  # Missing USP
        country_of_origin=None,  # Missing Country of Origin
        manufacturer_details="Audio Tech Ltd, Shenzhen",
        consumer_care_details="support@audiotech.com",
    )

    result = auditor.audit_listing(pdp, platform=ECommercePlatformType.MARKETPLACE)

    assert result.is_compliant is False
    assert result.rule6_10_compliant is False
    assert "Country of Origin" in result.missing_mandatory_declarations
    assert result.usp_rule6_11_compliant is False
    assert any(dp.pattern_type == DarkPatternType.HIDDEN_USP for dp in result.dark_patterns_detected)


def test_ecommerce_dark_pattern_false_urgency_and_drip_pricing():
    """Verify detection of false urgency countdowns and hidden checkout drip fees."""
    auditor = ECommerceMarketplaceComplianceAuditor()

    pdp = DigitalPDPDeclarations(
        title="Premium Almonds 500g",
        declared_mrp=500.0,
        declared_selling_price=399.0,
        declared_usp=0.798,
        usp_unit_denominator="g",
        net_quantity_str="500 g",
        country_of_origin="India",
        manufacturer_details="NutriFoods, Mumbai",
        consumer_care_details="care@nutrifoods.in",
        raw_text_payload="Hurry! Only 2 left in stock. Flash sale ending soon!",
    )

    # Drip pricing at checkout: base Rs. 399 -> final Rs. 479 (unannounced +Rs. 80 fee)
    checkout_breakdown = {
        "item_price": 399.0,
        "handling_fee": 40.0,
        "platform_charge": 40.0,
        "total_payable": 479.0,
    }

    result = auditor.audit_listing(
        pdp,
        platform=ECommercePlatformType.QUICK_COMMERCE,
        announced_price_breakdown=checkout_breakdown,
    )

    assert result.is_compliant is False
    assert len(result.dark_patterns_detected) >= 2

    pattern_types = [dp.pattern_type for dp in result.dark_patterns_detected]
    assert DarkPatternType.FALSE_URGENCY in pattern_types
    assert DarkPatternType.DRIP_PRICING in pattern_types
