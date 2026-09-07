"""
Tests for Section 36(1) and Section 48/48A Penalty Compounding & Recidivism Auditor.
Verifies multi-year penalty escalation ladders under the Jan Vishwas Act, 2026.
"""

import time
import pytest
from nirikshak_rules_engine.penalties import (
    PenaltyCalculator,
    OffenseTier,
    EnforcementAction,
)
from nirikshak_rules_engine.notice_builder import ImprovementNoticeBuilder


@pytest.fixture
def penalty_calc():
    return PenaltyCalculator()


def test_first_offense_within_cure_period(penalty_calc):
    """Verifies first offense prompts a 15-day Improvement Notice with compounding range."""
    assessment = penalty_calc.calculate_penalty(
        prior_offenses_count=0,
        days_since_last_offense=None,
        is_cure_period_expired=False,
    )
    assert assessment.offense_tier == OffenseTier.FIRST_OFFENSE
    assert assessment.is_compoundable is True
    assert assessment.recommended_action == EnforcementAction.IMPROVEMENT_NOTICE_15_DAYS
    assert assessment.cure_period_days == 15
    assert assessment.statutory_fine_min_inr == 10000.0
    assert assessment.statutory_fine_max_inr == 25000.0
    assert assessment.is_decriminalized is True


def test_first_offense_expired_cure_period(penalty_calc):
    """Verifies expired cure window transitions to compounding proceeding."""
    assessment = penalty_calc.calculate_penalty(
        prior_offenses_count=0,
        days_since_last_offense=None,
        is_cure_period_expired=True,
    )
    assert assessment.offense_tier == OffenseTier.FIRST_OFFENSE
    assert assessment.is_compoundable is True
    assert assessment.recommended_action == EnforcementAction.COMPOUNDING_PROCEEDING
    assert assessment.cure_period_days is None
    assert assessment.statutory_fine_min_inr == 10000.0
    assert assessment.statutory_fine_max_inr == 25000.0


def test_second_offense_within_three_years(penalty_calc):
    """Verifies second offense within 3 years (1095 days) is barred from compounding under Section 48(2)."""
    assessment = penalty_calc.calculate_penalty(
        prior_offenses_count=1,
        days_since_last_offense=180,  # ~6 months
    )
    assert assessment.offense_tier == OffenseTier.SECOND_OFFENSE
    assert assessment.is_compoundable is False
    assert "Section 48(2)" in assessment.compounding_barred_reason
    assert assessment.recommended_action == EnforcementAction.ADJUDICATING_OFFICER_REFERRAL
    assert assessment.statutory_fine_min_inr == 25000.0
    assert assessment.statutory_fine_max_inr == 50000.0


def test_subsequent_offense_within_three_years(penalty_calc):
    """Verifies third/subsequent offense escalates to ₹1,00,000 maximum penalty."""
    assessment = penalty_calc.calculate_penalty(
        prior_offenses_count=2,
        days_since_last_offense=400,
    )
    assert assessment.offense_tier == OffenseTier.SUBSEQUENT_OFFENSE
    assert assessment.is_compoundable is False
    assert assessment.recommended_action == EnforcementAction.ADJUDICATING_OFFICER_REFERRAL
    assert assessment.statutory_fine_min_inr == 50000.0
    assert assessment.statutory_fine_max_inr == 100000.0


def test_recidivism_window_reset_after_three_years(penalty_calc):
    """Verifies that offenses older than 3 years (1095 days) reset to First Offense tier per Section 48(2)."""
    assessment = penalty_calc.calculate_penalty(
        prior_offenses_count=1,
        days_since_last_offense=1200,  # > 3 years
        is_cure_period_expired=False,
    )
    assert assessment.offense_tier == OffenseTier.FIRST_OFFENSE
    assert assessment.is_compoundable is True
    assert assessment.statutory_fine_max_inr == 25000.0


def test_penalty_decriminalization_purity(penalty_calc):
    """Verifies that all generated penalty summaries pass the strict zero-criminal terminology audit."""
    scenarios = [
        {"prior_offenses_count": 0, "days_since_last_offense": None, "is_cure_period_expired": False},
        {"prior_offenses_count": 0, "days_since_last_offense": None, "is_cure_period_expired": True},
        {"prior_offenses_count": 1, "days_since_last_offense": 100},
        {"prior_offenses_count": 2, "days_since_last_offense": 200},
        {"prior_offenses_count": 5, "days_since_last_offense": 50},
    ]
    for s in scenarios:
        assessment = penalty_calc.calculate_penalty(**s)
        # Verify audit raises no exception
        ImprovementNoticeBuilder.audit_text_decriminalization(assessment.legal_summary)
        # Additional assert on forbidden words
        forbidden = ["jail", "imprisonment", "arrest", "cognizable", "custody"]
        for word in forbidden:
            assert word not in assessment.legal_summary.lower()


def test_penalty_calc_latency(penalty_calc):
    """Verifies penalty calculation takes < 0.1ms."""
    start = time.perf_counter()
    for _ in range(200):
        _ = penalty_calc.calculate_penalty(prior_offenses_count=1, days_since_last_offense=300)
    elapsed_ms = (time.perf_counter() - start) * 1000
    avg_ms = elapsed_ms / 200.0
    assert avg_ms < 0.1, f"Penalty latency too high: {avg_ms:.4f}ms"
