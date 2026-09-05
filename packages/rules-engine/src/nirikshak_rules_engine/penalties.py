"""
Nirikshak Rules Engine: Section 36(1) & Section 48/48A Multi-Year Recidivism & Penalty Auditor.
Codifies compounding guidelines, multi-year repeat offender escalation ladders, and statutory
jurisdictional routing under the Legal Metrology Act, 2009 (as amended by Jan Vishwas Act, 2026).
"""

from enum import Enum
from typing import Optional, List, Tuple
from pydantic import BaseModel, Field, ConfigDict

from .notice_builder import ImprovementNoticeBuilder


class OffenseTier(str, Enum):
    """Statutory offense classification tier under Section 36(1)."""
    FIRST_OFFENSE = "FIRST_OFFENSE"
    SECOND_OFFENSE = "SECOND_OFFENSE"
    SUBSEQUENT_OFFENSE = "SUBSEQUENT_OFFENSE"


class EnforcementAction(str, Enum):
    """Recommended statutory administrative or adjudication procedure."""
    IMPROVEMENT_NOTICE_15_DAYS = "IMPROVEMENT_NOTICE_15_DAYS"
    COMPOUNDING_PROCEEDING = "COMPOUNDING_PROCEEDING"
    ADJUDICATING_OFFICER_REFERRAL = "ADJUDICATING_OFFICER_REFERRAL"


class PenaltyAssessment(BaseModel):
    """
    Statutory penalty determination and enforcement routing under Section 36(1)
    read with Sections 48 and 48A of the Legal Metrology Act, 2009 (amended 2026).
    """
    offense_tier: OffenseTier = Field(..., description="Offense recurrence classification")
    is_compoundable: bool = Field(..., description="Whether offense is eligible for compounding under Section 48")
    compounding_barred_reason: Optional[str] = Field(
        None, description="Legal ground if compounding is barred under Section 48(2)"
    )
    statutory_fine_min_inr: float = Field(..., ge=0.0, description="Minimum statutory fine/compounding amount")
    statutory_fine_max_inr: float = Field(..., ge=0.0, description="Maximum statutory fine/compounding amount")
    statutory_citations: List[str] = Field(..., description="Statutory enactments and sections cited")
    recommended_action: EnforcementAction = Field(..., description="Prescribed procedural action")
    cure_period_days: Optional[int] = Field(
        None,
        description="Reasonable cure period specified in the Improvement Notice; 15 days is the current configurable demonstration default",
    )
    legal_summary: str = Field(..., description="Statutory narrative summarizing the penalty assessment")
    is_decriminalized: bool = Field(
        default=True, description="Confirms zero criminal/jail liability under 2026 Jan Vishwas amendments"
    )

    model_config = ConfigDict(extra="ignore")


class PenaltyCalculator:
    """
    100% deterministic penalty calculator and statutory enforcement router.
    Strictly free from generative LLM hallucination and obsolete imprisonment penalties.
    """

    # System Workflow Configuration (Modeled after Section 48(2) Compounding Bar):
    # Section 48(2) prescribes a 3-year (1095 days) bar on compounding repeat offenses.
    # Note: Section 36(1) itself does not establish a generic 3-year reset for offense tiers;
    # RECIDIVISM_WINDOW_DAYS is a configurable workflow parameter modeled on the Section 48(2) timeline.
    RECIDIVISM_WINDOW_DAYS = 1095
    DEFAULT_CURE_PERIOD_DAYS = 15  # Configurable demonstration default; not a universal statutory period

    # Statutory Penalty Limits under Substituted Section 36(1) (Jan Vishwas Act, 2026):
    # 1st Offense: Improvement Notice (no initial fine during cure period)
    FIRST_OFFENSE_MIN_INR = 0.0
    FIRST_OFFENSE_MAX_INR = 0.0
    FIRST_OFFENSE_EXPIRED_MIN_INR = 10000.0
    FIRST_OFFENSE_EXPIRED_MAX_INR = 50000.0

    # 2nd Offense: Penalty up to ₹5,00,000 (Section 36(1) r/w Section 48A)
    SECOND_OFFENSE_MIN_INR = 100000.0
    SECOND_OFFENSE_MAX_INR = 500000.0

    # 3rd or Subsequent Offense: Penalty not less than ₹25,00,000 extending up to ₹50,00,000
    SUBSEQUENT_OFFENSE_MIN_INR = 2500000.0
    SUBSEQUENT_OFFENSE_MAX_INR = 5000000.0

    def calculate_penalty(
        self,
        prior_offenses_count: int = 0,
        days_since_last_offense: Optional[int] = None,
        is_cure_period_expired: bool = False,
        custom_cure_period_days: Optional[int] = None,
    ) -> PenaltyAssessment:
        """
        Calculates penalty bracket and statutory procedure based on offense history.

        Args:
            prior_offenses_count: Number of verified prior compounding or conviction orders.
            days_since_last_offense: Elapsed calendar days since the immediate previous offense.
            is_cure_period_expired: Whether the reasonable Improvement Notice cure period has lapsed.
            custom_cure_period_days: Optional officer-specified reasonable period in days (15 days demonstration default).

        Returns:
            PenaltyAssessment adhering to substituted Section 36(1) under Jan Vishwas Act, 2026.
        """
        # Workflow Configuration (Modeled after Section 48(2) compounding timeline):
        # If last offense occurred > 3 years (1095 days) ago, the workflow tier resets to first offense.
        is_repeat_within_3_years = (
            prior_offenses_count > 0
            and days_since_last_offense is not None
            and days_since_last_offense <= self.RECIDIVISM_WINDOW_DAYS
        )

        effective_prior_count = prior_offenses_count if is_repeat_within_3_years else 0

        if effective_prior_count == 0:
            # First Offense Tier
            offense_tier = OffenseTier.FIRST_OFFENSE
            is_compoundable = True
            barred_reason = None

            if not is_cure_period_expired:
                # Under Substituted Section 36(1), 1st offense initiates with an Improvement Notice
                action = EnforcementAction.IMPROVEMENT_NOTICE_15_DAYS
                cure_days = custom_cure_period_days or self.DEFAULT_CURE_PERIOD_DAYS
                min_fine = self.FIRST_OFFENSE_MIN_INR
                max_fine = self.FIRST_OFFENSE_MAX_INR
                summary = (
                    "First statutory non-compliance under Section 36(1). Action: Mandatory Improvement Notice. "
                    "Monetary penalty: NOT APPLICABLE during cure window. "
                    "Statutory basis: Reasonable cure period specified by the authorized officer in the Improvement Notice. "
                    f"System configuration: {cure_days} days (demonstration default only; not a statutory period). "
                    "If unrectified within the cure window, compounding proceedings under Section 48 apply."
                )
            else:
                action = EnforcementAction.COMPOUNDING_PROCEEDING
                cure_days = None
                min_fine = self.FIRST_OFFENSE_EXPIRED_MIN_INR
                max_fine = self.FIRST_OFFENSE_EXPIRED_MAX_INR
                summary = (
                    "Cure period expired for first offense under Section 36(1). Proceeding to compounding "
                    f"under Section 48(1) with statutory compounding assessment (₹{int(min_fine):,} to ₹{int(max_fine):,})."
                )

            citations = [
                "Legal Metrology Act, 2009, Section 36(1) (as substituted by Jan Vishwas Act, 2026)",
                "Legal Metrology Act, 2009, Section 48(1)",
                "Jan Vishwas (Amendment of Provisions) Act, 2026",
            ]

        elif effective_prior_count == 1:
            # Second Offense Tier (Within 3 years)
            offense_tier = OffenseTier.SECOND_OFFENSE
            min_fine = self.SECOND_OFFENSE_MIN_INR
            max_fine = self.SECOND_OFFENSE_MAX_INR
            is_compoundable = False
            barred_reason = (
                "Section 48(2) bar: Offense committed within 3 years (1095 days) of prior compounding/order. "
                "Second offense under substituted Section 36(1) is non-compoundable and referred to Adjudicating Officer."
            )
            action = EnforcementAction.ADJUDICATING_OFFICER_REFERRAL
            cure_days = None
            citations = [
                "Legal Metrology Act, 2009, Section 36(1) (as substituted by Jan Vishwas Act, 2026)",
                "Legal Metrology Act, 2009, Section 48(2) (Compounding Bar)",
                "Legal Metrology Act, 2009, Section 48A (Adjudication by Legal Metrology Officer)",
                "Jan Vishwas (Amendment of Provisions) Act, 2026",
            ]
            summary = (
                f"Second offense committed within {days_since_last_offense} days (< 3 years). "
                "Compounding is legally barred under Section 48(2). Referred to Adjudicating Officer "
                f"under Section 48A with statutory penalty extending up to ₹{int(max_fine):,} "
                f"(minimum ₹{int(min_fine):,}) under substituted Section 36(1)."
            )

        else:
            # Subsequent Offense Tier (>= 2 prior offenses within 3 years)
            offense_tier = OffenseTier.SUBSEQUENT_OFFENSE
            min_fine = self.SUBSEQUENT_OFFENSE_MIN_INR
            max_fine = self.SUBSEQUENT_OFFENSE_MAX_INR
            is_compoundable = False
            barred_reason = (
                f"Section 48(2) bar: Habitual repeat violation ({effective_prior_count} prior offenses within 3 years). "
                "Compounding strictly prohibited; statutory adjudication mandated."
            )
            action = EnforcementAction.ADJUDICATING_OFFICER_REFERRAL
            cure_days = None
            citations = [
                "Legal Metrology Act, 2009, Section 36(1) (as substituted by Jan Vishwas Act, 2026)",
                "Legal Metrology Act, 2009, Section 48(2) (Compounding Bar)",
                "Legal Metrology Act, 2009, Section 48A (Adjudication by Legal Metrology Officer)",
                "Jan Vishwas (Amendment of Provisions) Act, 2026",
            ]
            summary = (
                f"Subsequent repeat offense ({effective_prior_count} prior offenses within {days_since_last_offense} days). "
                "Compounding barred under Section 48(2). Adjudicating Officer inquiry under Section 48A "
                f"with statutory penalty of not less than ₹{int(min_fine):,} and extending up to ₹{int(max_fine):,} "
                "under substituted Section 36(1)."
            )

        # Audit against obsolete criminal terminology (raises ValueError on violation)
        ImprovementNoticeBuilder.audit_text_decriminalization(summary)

        return PenaltyAssessment(
            offense_tier=offense_tier,
            is_compoundable=is_compoundable,
            compounding_barred_reason=barred_reason,
            statutory_fine_min_inr=min_fine,
            statutory_fine_max_inr=max_fine,
            statutory_citations=citations,
            recommended_action=action,
            cure_period_days=cure_days,
            legal_summary=summary,
            is_decriminalized=True,
        )
