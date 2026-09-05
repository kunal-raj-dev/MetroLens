"""
Tests for Section 36(1) Jan Vishwas Improvement Notice Builder.
Verifies Gate 6 / CP-6 compliance under Jan Vishwas (Amendment of Provisions) Act, 2026.
Validates 15-day cure window, exact legal citations, eMaap sync payload,
and strictly audits zero occurrences of criminal or imprisonment terminology.
"""

import pytest
from nirikshak_rules_engine import (
    StatutoryRuleEngine,
    ImprovementNoticeBuilder,
    CanonicalDeclaration,
    RuleEvaluationRecord,
    UnitType,
    ComplianceState,
)


@pytest.fixture
def builder():
    return ImprovementNoticeBuilder()


@pytest.fixture
def engine():
    return StatutoryRuleEngine()


def test_notice_not_recommended_when_compliant(builder):
    """Compliant package evaluations must not recommend an Improvement Notice."""
    decl = CanonicalDeclaration(commodity_name="Cashews", manufacturer_name="CleanPack Ltd")
    passing_records = [
        RuleEvaluationRecord(
            rule_id="LMPC-R06-MRP-001",
            rule_title="MRP Declaration",
            statutory_reference="Rule 6(1)(e)",
            status="PASS",
            is_compliant=True,
            statutory_citation="Rule 6(1)(e)",
        )
    ]
    notice = builder.build_notice(decl, passing_records)
    assert notice.recommended is False
    assert notice.cure_period_days == 15
    assert notice.notice_text is None


def test_notice_recommended_when_non_compliant(builder):
    """Non-compliant package evaluations must recommend an Improvement Notice under Section 36(1)."""
    decl = CanonicalDeclaration(
        commodity_name="Potato Chips",
        manufacturer_name="SnackCo Foods Ltd, Okhla, New Delhi 110020",
    )
    failing_records = [
        RuleEvaluationRecord(
            rule_id="LMPC-R06-MRP-001",
            rule_title="MRP Tax Qualifier Missing",
            statutory_reference="Rule 6(1)(e)",
            status="FAIL",
            is_compliant=False,
            observed_value="₹ 20.00 (qualifier missing)",
            required_value="inclusive of all taxes",
            statutory_citation="Rule 6(1)(e) of LM(PC) Rules, 2011",
        ),
        RuleEvaluationRecord(
            rule_id="LMPC-R06-USP-001",
            rule_title="Unit Sale Price Mandate",
            statutory_reference="Rule 6(11)",
            status="FAIL",
            is_compliant=False,
            observed_value="Not declared",
            required_value="₹ 0.40 / g",
            statutory_citation="Rule 6(11) as amended by G.S.R. 226(E)",
        ),
    ]
    notice = builder.build_notice(decl, failing_records, inspection_id="INSP-TEST-001")
    assert notice.recommended is True
    assert notice.cure_period_days == 15
    assert "Section 36(1)" in notice.act_provision
    assert "Jan Vishwas" in notice.act_provision
    assert len(notice.itemized_violations) == 2
    assert notice.notice_text is not None


def test_strict_zero_criminal_terminology(builder):
    """
    STRICT STATUTORY AUDIT: The generated notice text must contain ZERO occurrences
    of obsolete criminal penalty terms under the Jan Vishwas Act 2026.
    """
    decl = CanonicalDeclaration(
        commodity_name="Atta",
        manufacturer_name="WheatGrains Ltd",
    )
    failing_records = [
        RuleEvaluationRecord(
            rule_id="LMPC-R06-QTY-001",
            rule_title="Non-standard unit Gms",
            statutory_reference="Rule 6(1)(c)",
            status="FAIL",
            is_compliant=False,
            observed_value="500 Gms",
            required_value="Standard SI unit 'g'",
            statutory_citation="Rule 6(1)(c) read with Rule 13",
        )
    ]
    notice = builder.build_notice(decl, failing_records, inspection_id="INSP-ZERO-CRIMINAL")
    assert notice.notice_text is not None

    text_lower = notice.notice_text.lower()
    for criminal_term in builder.PROHIBITED_CRIMINAL_TERMS:
        assert criminal_term not in text_lower, (
            f"Statutory audit failure: Prohibited criminal term '{criminal_term}' found in legal notice text!"
        )


def test_audit_text_decriminalization_guard():
    """Verify that the anti-criminal audit guard actively raises an exception if a prohibited term appears."""
    with pytest.raises(ValueError, match="Statutory Decriminalization Violation"):
        ImprovementNoticeBuilder.audit_text_decriminalization(
            "The offender shall be liable to imprisonment for a term of six months."
        )


def test_emaap_mock_sync_payload_generation(engine, builder):
    """Verify export of standardized eMaap mock sync payload matching docs/API_CONTRACT.md."""
    decl_non_compliant = CanonicalDeclaration(
        commodity_name="Biscuits",
        manufacturer_name="BakeHouse Ltd",
        mrp_inr=50.0,
        tax_qualifier_present=False,  # Violation
        net_quantity_value=100.0,
        net_quantity_unit=UnitType.GRAM,
    )
    res = engine.evaluate(decl_non_compliant, inspection_id="INSP-EMAAP-999")
    assert res.overall_verdict == ComplianceState.NON_COMPLIANT
    assert res.improvement_notice is not None
    assert res.improvement_notice.recommended is True

    emaap_payload = builder.build_emaap_sync_payload(
        res, officer_id="LMO-DELHI-42", jurisdiction_code="DL-01-CENTRAL"
    )
    assert emaap_payload["inspection_id"] == "INSP-EMAAP-999"
    assert emaap_payload["jurisdiction_code"] == "DL-01-CENTRAL"
    assert emaap_payload["officer_id"] == "LMO-DELHI-42"
    assert emaap_payload["compliance_state"] in ["POTENTIAL_NON_COMPLIANCE", "NON_COMPLIANT"]
    assert emaap_payload["improvement_notice_issued"] is True
    assert emaap_payload["cure_period_days"] == 15
    assert emaap_payload["defects_count"] >= 1


def test_engine_evaluate_populates_improvement_notice(engine):
    """Verify StatutoryRuleEngine.evaluate creates an ImprovementNotice on non-compliant results."""
    decl = CanonicalDeclaration(
        commodity_name="Spice Powder",
        manufacturer_name="PureSpices Ltd",
        country_of_origin="India",
        net_quantity_value=100.0,
        net_quantity_unit=UnitType.GRAM,
        mfg_month=9,
        mfg_year=2026,
        mrp_inr=80.0,
        tax_qualifier_present=False,  # Missing qualifier
        consumer_care_phone="1800-99-8877",
        declared_usp_value=0.80,
        declared_usp_unit="g",
    )
    result = engine.evaluate(decl, inspection_id="INSP-INT-NOTICE")
    assert result.overall_verdict == ComplianceState.NON_COMPLIANT
    assert result.improvement_notice is not None
    assert result.improvement_notice.recommended is True
    assert result.improvement_notice.cure_period_days == 15
    assert "Rule 6(1)(e)" in result.improvement_notice.statutory_grounds
