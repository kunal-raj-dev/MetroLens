"""
Nirikshak API Services Package.
Provides ephemeral spooling, session lifecycle, and pipeline orchestration.
"""

from .spool_service import SpoolService, SpoolSession, spool_service
from .pipeline_orchestrator import (
    PipelineOrchestrator,
    pipeline_orchestrator,
    orchestrate_inspection,
)
from .leader_election import (
    LeaderElectionCoordinator,
    LeaseRecord,
    NodeRole,
    ElectionDiagnostics,
)
from .event_sourcing import (
    EventStore,
    InspectionAggregate,
    DomainEvent,
    InspectionState,
    ConcurrencyError,
)
from .adaptive_rate_limiter import (
    AdaptiveRateLimiter,
    ClientTier,
    RateLimitDecision,
    TierPolicy,
)

__all__ = [
    "SpoolService",
    "SpoolSession",
    "spool_service",
    "PipelineOrchestrator",
    "pipeline_orchestrator",
    "orchestrate_inspection",
    "LeaderElectionCoordinator",
    "LeaseRecord",
    "NodeRole",
    "ElectionDiagnostics",
    "EventStore",
    "InspectionAggregate",
    "DomainEvent",
    "InspectionState",
    "ConcurrencyError",
    "AdaptiveRateLimiter",
    "ClientTier",
    "RateLimitDecision",
    "TierPolicy",
]

