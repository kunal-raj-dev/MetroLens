"""
Unit Test Suite for Enterprise Distributed Services Subsystem
============================================================
Tests distributed leader election, monotonic fencing tokens, majority quorum,
cryptographic event sourcing & Merkle log replay, and adaptive rate limiting with IP reputation.
"""

import datetime
import time
import pytest

from apps.api.services.leader_election import (
    LeaderElectionCoordinator,
    LeaseRecord,
    NodeRole,
    ElectionDiagnostics,
)
from apps.api.services.event_sourcing import (
    EventStore,
    InspectionAggregate,
    DomainEvent,
    InspectionState,
    ConcurrencyError,
    AggregateType,
)
from apps.api.services.adaptive_rate_limiter import (
    AdaptiveRateLimiter,
    ClientTier,
    RateLimitDecision,
    TIER_POLICIES,
)


# =============================================================================
# 1. Distributed Leader Election & Fencing Tests
# =============================================================================

class TestLeaderElectionCoordinator:
    """Test suite for cluster leadership, leasing, and split-brain fencing tokens."""

    def test_single_node_leadership_acquisition(self):
        coord = LeaderElectionCoordinator(
            local_node_id="gateway-node-01",
            lease_ttl_seconds=5.0,
        )
        acquired, lease = coord.try_acquire_or_renew_lease()

        assert acquired is True
        assert isinstance(lease, LeaseRecord)
        assert lease.leader_node_id == "gateway-node-01"
        assert lease.fencing_token > 1000

        # Validate fencing token
        assert coord.validate_fencing_token(lease.fencing_token) is True
        # Stale fencing token is rejected
        assert coord.validate_fencing_token(lease.fencing_token - 1) is False

    def test_multi_node_quorum_abdication(self):
        # Cluster of 3 nodes: node-01, node-02, node-03
        coord = LeaderElectionCoordinator(
            local_node_id="node-01",
            cluster_peers=["node-02", "node-03"],
            lease_ttl_seconds=3.0,
            heartbeat_interval_seconds=1.0,
        )

        # Peer heartbeats initially active -> quorum achieved
        coord.record_peer_heartbeat("node-02")
        coord.record_peer_heartbeat("node-03")

        acquired, lease = coord.try_acquire_or_renew_lease()
        assert acquired is True
        assert lease is not None

        # Simulate total network partition: node-02 and node-03 disappear
        # Artificially age the peer heartbeats
        stale_time = datetime.datetime.now() - datetime.timedelta(seconds=10)
        coord._nodes["node-02"].last_heartbeat = stale_time
        coord._nodes["node-03"].last_heartbeat = stale_time

        # Attempt renew: quorum lost (1/3 nodes active, need 2)
        acquired_after_partition, _ = coord.try_acquire_or_renew_lease()
        assert acquired_after_partition is False

        diag = coord.get_diagnostics()
        assert diag.quorum_achieved is False
        assert diag.local_node_role == NodeRole.QUORUM_LOST

    def test_voluntary_step_down(self):
        coord = LeaderElectionCoordinator(local_node_id="node-01", lease_ttl_seconds=5.0)
        acquired, lease = coord.try_acquire_or_renew_lease()
        assert acquired is True

        coord.step_down()
        assert coord.validate_fencing_token(lease.fencing_token) is False
        assert coord.get_diagnostics().local_node_role == NodeRole.FOLLOWER


# =============================================================================
# 2. Cryptographic Event Sourcing & Merkle Log Tests
# =============================================================================

class TestEventSourcing:
    """Test suite for append-only event streams, Merkle chains, and time-travel replay."""

    @pytest.fixture
    def store(self):
        return EventStore()

    def test_aggregate_lifecycle_and_event_application(self):
        agg = InspectionAggregate(inspection_id="INSP-EV-001")
        assert agg.version == 0
        assert agg.state.status == "INITIALIZED"

        # 1. Submit inspection
        agg.submit_inspection(raw_image_sha256="A" * 64)
        assert agg.version == 1
        assert agg.state.status == "SUBMITTED"
        assert agg.state.raw_image_sha256 == "A" * 64

        # 2. Sanitize image
        agg.record_sanitization(sanitized_sha256="B" * 64)
        assert agg.version == 2
        assert agg.state.status == "SANITIZED"

        # 3. Forensics
        agg.record_forensics(tamper_score=0.02, is_authentic=True)
        assert agg.version == 3
        assert agg.state.status == "FORENSICS_VERIFIED"

        # 4. OCR
        agg.record_ocr(declarations={"mrp": "₹150", "net_quantity": "500g"})
        assert agg.version == 4
        assert agg.state.ocr_declarations["mrp"] == "₹150"

        # 5. Rules
        agg.record_rule_evaluation(violations=["Rule 6(1)(e) - USP Missing"])
        assert agg.version == 5
        assert agg.state.overall_verdict == "NON_COMPLIANT"

        events = agg.get_uncommitted_events()
        assert len(events) == 5

    def test_event_store_append_and_rehydration(self, store):
        agg = InspectionAggregate(inspection_id="INSP-EV-002")
        agg.submit_inspection(raw_image_sha256="1" * 64)
        agg.record_sanitization(sanitized_sha256="2" * 64)

        uncommitted = agg.get_uncommitted_events()
        store.append_events(aggregate_id="INSP-EV-002", events=uncommitted, expected_version=0)
        agg.mark_events_committed()

        # Rehydrate from store
        reloaded = store.load_aggregate("INSP-EV-002")
        assert reloaded is not None
        assert reloaded.version == 2
        assert reloaded.state.status == "SANITIZED"
        assert reloaded.state.sanitized_image_sha256 == "2" * 64

    def test_optimistic_concurrency_conflict(self, store):
        agg = InspectionAggregate(inspection_id="INSP-EV-003")
        agg.submit_inspection(raw_image_sha256="C" * 64)
        store.append_events("INSP-EV-003", agg.get_uncommitted_events(), expected_version=0)

        # Attempt to append second event expecting version 0 instead of version 1
        agg2 = InspectionAggregate(inspection_id="INSP-EV-003")
        agg2.submit_inspection(raw_image_sha256="D" * 64)
        with pytest.raises(ConcurrencyError, match="Optimistic concurrency conflict"):
            store.append_events("INSP-EV-003", agg2.get_uncommitted_events(), expected_version=0)

    def test_time_travel_replay(self, store):
        agg = InspectionAggregate(inspection_id="INSP-EV-004")
        agg.submit_inspection(raw_image_sha256="E" * 64) # v1
        agg.record_sanitization(sanitized_sha256="F" * 64) # v2
        agg.record_rule_evaluation(violations=["Rule 7 violation"]) # v3

        store.append_events("INSP-EV-004", agg.get_uncommitted_events(), expected_version=0)

        # Replay back to version 1: state must be SUBMITTED
        v1_state = store.replay_to_version("INSP-EV-004", target_version=1)
        assert v1_state.version == 1
        assert v1_state.status == "SUBMITTED"
        assert v1_state.sanitized_image_sha256 is None

        # Replay to version 3: state is EVALUATED
        v3_state = store.replay_to_version("INSP-EV-004", target_version=3)
        assert v3_state.version == 3
        assert v3_state.status == "EVALUATED"

    def test_cryptographic_integrity_and_tamper_detection(self, store):
        agg = InspectionAggregate(inspection_id="INSP-EV-005")
        agg.submit_inspection(raw_image_sha256="G" * 64)
        agg.record_sanitization(sanitized_sha256="H" * 64)
        store.append_events("INSP-EV-005", agg.get_uncommitted_events(), expected_version=0)

        # Intact stream verifies cleanly
        intact, msg = store.verify_stream_integrity("INSP-EV-005")
        assert intact is True
        assert "Stream intact" in msg

        # Maliciously modify event payload in stream
        store._streams["INSP-EV-005"][0].payload["raw_image_sha256"] = "TAMPERED"
        intact_after_hack, hack_msg = store.verify_stream_integrity("INSP-EV-005")
        assert intact_after_hack is False
        assert "tampering detected" in hack_msg


# =============================================================================
# 3. Adaptive Rate Limiter & IP Reputation Tests
# =============================================================================

class TestAdaptiveRateLimiter:
    """Test suite for sliding window rate limiting and IP reputation penalties."""

    @pytest.fixture
    def limiter(self):
        return AdaptiveRateLimiter(window_size_seconds=60.0)

    def test_tier_quota_and_token_consumption(self, limiter):
        client_ip = "192.168.1.50"
        # Anonymous tier has 20 requests per minute
        decision = limiter.check_rate_limit(client_ip, tier=ClientTier.ANONYMOUS_UNTRUSTED)
        assert isinstance(decision, RateLimitDecision)
        assert decision.is_allowed is True
        assert decision.remaining_tokens == 19
        assert decision.reputation_score == 100.0

    def test_exceeding_rate_limit_blocks_with_retry_after(self, limiter):
        client_ip = "10.0.0.99"
        # Exhaust quota for Anonymous (20 req/min)
        for _ in range(20):
            limiter.check_rate_limit(client_ip, tier=ClientTier.ANONYMOUS_UNTRUSTED)

        # 21st request must be blocked
        blocked = limiter.check_rate_limit(client_ip, tier=ClientTier.ANONYMOUS_UNTRUSTED)
        assert blocked.is_allowed is False
        assert blocked.remaining_tokens == 0
        assert blocked.retry_after_seconds > 0.0
        assert "Retry-After" in blocked.headers

    def test_reputation_penalty_and_quarantine(self, limiter):
        client_ip = "203.0.113.42"
        # Record malicious security events: e.g. 2 steganographic / exploit upload attempts
        score1 = limiter.record_security_event(client_ip, event_type="tamper_detected")
        assert score1 == 55.0  # 100 - 45

        # Record second exploit attempt -> triggers quarantine (< 15.0)
        score2 = limiter.record_security_event(client_ip, event_type="tamper_detected")
        assert score2 == 10.0  # 55 - 45

        # Next request must be quarantined
        decision = limiter.check_rate_limit(client_ip)
        assert decision.is_allowed is False
        assert decision.is_quarantined is True
        assert decision.headers.get("X-Reputation-Status") == "QUARANTINED"
