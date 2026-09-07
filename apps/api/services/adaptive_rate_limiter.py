"""
Adaptive Rate Limiter & IP Reputation Throttling Subsystem
=========================================================
Provides enterprise-grade sliding-window rate limiting, token-bucket burst management,
client tier quotas, dynamic IP reputation scoring, and anti-abuse defense for the
MetroLens API Gateway.

Security Objectives:
--------------------
Public legal metrology APIs are prime targets for automated web scraping by gray-market
sellers, reconnaissance probes seeking unredacted audit trails, and volumetric DDoS.
This subsystem dynamically penalizes hostile scanning behavior (HTTP 401s, 403s, and
steganographic exploit uploads) while granting dedicated high-throughput pipelines to
verified enforcement officers and customs officials.
"""

from __future__ import annotations

import collections
import datetime
import enum
import logging
import math
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("metrolens.services.adaptive_rate_limiter")


class ClientTier(str, enum.Enum):
    """SLA tiers determining request rate quotas and burst headroom."""
    ENTERPRISE_CUSTOMS = "enterprise_customs"
    ENFORCEMENT_OFFICER = "enforcement_officer"
    COMMERCIAL_RETAILER = "commercial_retailer"
    PUBLIC_CITIZEN = "public_citizen"
    ANONYMOUS_UNTRUSTED = "anonymous_untrusted"


@dataclass(frozen=True)
class TierPolicy:
    """Rate limit configuration for an SLA tier."""
    requests_per_minute: int
    burst_capacity: int
    reputation_floor: float = 20.0


TIER_POLICIES: Dict[ClientTier, TierPolicy] = {
    ClientTier.ENTERPRISE_CUSTOMS: TierPolicy(requests_per_minute=1200, burst_capacity=100),
    ClientTier.ENFORCEMENT_OFFICER: TierPolicy(requests_per_minute=600, burst_capacity=50),
    ClientTier.COMMERCIAL_RETAILER: TierPolicy(requests_per_minute=180, burst_capacity=20),
    ClientTier.PUBLIC_CITIZEN: TierPolicy(requests_per_minute=60, burst_capacity=10),
    ClientTier.ANONYMOUS_UNTRUSTED: TierPolicy(requests_per_minute=20, burst_capacity=5),
}


@dataclass
class ClientReputationRecord:
    """Historical behavior profile of an IP address / client identifier."""
    client_key: str
    reputation_score: float = 100.0  # 0.0 (Malicious) to 100.0 (Pristine)
    total_requests: int = 0
    bad_requests_count: int = 0
    auth_failures_count: int = 0
    security_violations_count: int = 0
    is_quarantined: bool = False
    quarantine_until: Optional[datetime.datetime] = None
    last_seen: datetime.datetime = field(default_factory=datetime.datetime.now)
    last_reputation_decay: datetime.datetime = field(default_factory=datetime.datetime.now)


@dataclass
class RateLimitDecision:
    """Result of rate limit and reputation evaluation."""
    is_allowed: bool
    remaining_tokens: int
    retry_after_seconds: float
    tier: ClientTier
    reputation_score: float
    penalty_delay_ms: float
    is_quarantined: bool
    headers: Dict[str, str] = field(default_factory=dict)


class AdaptiveRateLimiter:
    """
    High-performance sliding-window counter and dynamic reputation throttling engine.
    """

    def __init__(
        self,
        default_tier: ClientTier = ClientTier.ANONYMOUS_UNTRUSTED,
        window_size_seconds: float = 60.0,
    ):
        self.default_tier = default_tier
        self.window_size_seconds = window_size_seconds
        self._lock = threading.RLock()

        # Sliding window timestamps: client_key -> deque of monotonic timestamps
        self._request_windows: Dict[str, collections.deque] = {}

        # Client reputation profiles: client_key -> ClientReputationRecord
        self._reputation_db: Dict[str, ClientReputationRecord] = {}

    # -------------------------------------------------------------------------
    # Evaluation API
    # -------------------------------------------------------------------------

    def check_rate_limit(
        self,
        client_key: str,
        tier: Optional[ClientTier] = None,
    ) -> RateLimitDecision:
        """
        Evaluates incoming request against tier quotas, sliding window, and IP reputation.
        """
        with self._lock:
            now_mono = time.monotonic()
            now_dt = datetime.datetime.now()
            effective_tier = tier or self.default_tier
            policy = TIER_POLICIES.get(effective_tier, TIER_POLICIES[ClientTier.ANONYMOUS_UNTRUSTED])

            # 1. Fetch or initialize reputation record
            rep = self._get_or_create_reputation(client_key, now_dt)
            self._apply_passive_reputation_recovery(rep, now_dt)

            # 2. Check quarantine / ban status
            if rep.is_quarantined and rep.quarantine_until and now_dt < rep.quarantine_until:
                retry_after = max(1.0, (rep.quarantine_until - now_dt).total_seconds())
                return RateLimitDecision(
                    is_allowed=False,
                    remaining_tokens=0,
                    retry_after_seconds=retry_after,
                    tier=effective_tier,
                    reputation_score=rep.reputation_score,
                    penalty_delay_ms=2000.0,
                    is_quarantined=True,
                    headers={
                        "X-RateLimit-Limit": str(policy.requests_per_minute),
                        "X-RateLimit-Remaining": "0",
                        "Retry-After": str(int(retry_after)),
                        "X-Reputation-Status": "QUARANTINED",
                    },
                )
            elif rep.is_quarantined and rep.quarantine_until and now_dt >= rep.quarantine_until:
                # Release from quarantine with probation score
                rep.is_quarantined = False
                rep.quarantine_until = None
                rep.reputation_score = 30.0

            # 3. Clean expired timestamps from sliding window
            window = self._request_windows.setdefault(client_key, collections.deque())
            cutoff = now_mono - self.window_size_seconds
            while window and window[0] < cutoff:
                window.popleft()

            # 4. Apply reputation-based quota throttling factor
            if rep.reputation_score >= 70.0:
                throttle_multiplier = 1.0
                penalty_delay = 0.0
            elif rep.reputation_score >= 40.0:
                throttle_multiplier = 0.50
                penalty_delay = 200.0  # 200ms penalty
            else:
                throttle_multiplier = 0.20
                penalty_delay = 800.0  # 800ms penalty

            effective_limit = max(1, int(policy.requests_per_minute * throttle_multiplier))
            current_count = len(window)

            # 5. Check if quota exceeded
            if current_count >= effective_limit:
                earliest = window[0]
                retry_after = max(0.5, (earliest + self.window_size_seconds) - now_mono)
                # Slight penalty for hitting hard rate limit
                self.record_security_event(client_key, event_type="rate_limit_exceeded")

                return RateLimitDecision(
                    is_allowed=False,
                    remaining_tokens=0,
                    retry_after_seconds=retry_after,
                    tier=effective_tier,
                    reputation_score=rep.reputation_score,
                    penalty_delay_ms=penalty_delay,
                    is_quarantined=False,
                    headers={
                        "X-RateLimit-Limit": str(effective_limit),
                        "X-RateLimit-Remaining": "0",
                        "Retry-After": str(int(math.ceil(retry_after))),
                        "X-Reputation-Score": f"{rep.reputation_score:.1f}",
                    },
                )

            # Request allowed: register timestamp
            window.append(now_mono)
            rep.total_requests += 1
            rep.last_seen = now_dt
            remaining = max(0, effective_limit - len(window))

            return RateLimitDecision(
                is_allowed=True,
                remaining_tokens=remaining,
                retry_after_seconds=0.0,
                tier=effective_tier,
                reputation_score=rep.reputation_score,
                penalty_delay_ms=penalty_delay,
                is_quarantined=False,
                headers={
                    "X-RateLimit-Limit": str(effective_limit),
                    "X-RateLimit-Remaining": str(remaining),
                    "X-Reputation-Score": f"{rep.reputation_score:.1f}",
                },
            )

    # -------------------------------------------------------------------------
    # Reputation Management & Telemetry
    # -------------------------------------------------------------------------

    def record_security_event(
        self,
        client_key: str,
        event_type: str,  # "bad_request", "auth_failure", "tamper_detected", "rate_limit_exceeded"
    ) -> float:
        """
        Deducts reputation score based on suspicious client activity.
        """
        with self._lock:
            now_dt = datetime.datetime.now()
            rep = self._get_or_create_reputation(client_key, now_dt)

            if event_type == "bad_request":
                penalty = 2.0
                rep.bad_requests_count += 1
            elif event_type == "auth_failure":
                penalty = 5.0
                rep.auth_failures_count += 1
            elif event_type == "rate_limit_exceeded":
                penalty = 1.5
            elif event_type == "tamper_detected":
                penalty = 45.0
                rep.security_violations_count += 1
            else:
                penalty = 1.0

            rep.reputation_score = max(0.0, rep.reputation_score - penalty)

            # Auto-quarantine if reputation plummets below critical threshold
            if rep.reputation_score < 15.0 and not rep.is_quarantined:
                rep.is_quarantined = True
                rep.quarantine_until = now_dt + datetime.timedelta(minutes=15)
                logger.warning(
                    f"Client '{client_key}' QUARANTINED for 15 minutes due to critical "
                    f"reputation drop ({rep.reputation_score:.1f}/100.0)."
                )

            return rep.reputation_score

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    def _get_or_create_reputation(self, client_key: str, now: datetime.datetime) -> ClientReputationRecord:
        if client_key not in self._reputation_db:
            self._reputation_db[client_key] = ClientReputationRecord(
                client_key=client_key,
                reputation_score=100.0,
                last_seen=now,
                last_reputation_decay=now,
            )
        return self._reputation_db[client_key]

    def _apply_passive_reputation_recovery(self, rep: ClientReputationRecord, now: datetime.datetime) -> None:
        """Gradually restores reputation score by +5.0 points per clean hour."""
        elapsed_hours = (now - rep.last_reputation_decay).total_seconds() / 3600.0
        if elapsed_hours >= 1.0 and rep.reputation_score < 100.0:
            recovery = min(100.0 - rep.reputation_score, elapsed_hours * 5.0)
            rep.reputation_score += recovery
            rep.last_reputation_decay = now
