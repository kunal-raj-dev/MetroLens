"""
Distributed Leader Election, Lease Management & Split-Brain Fencing Subsystem
=============================================================================
Provides distributed high-availability leader election, heartbeat leasing,
monotonically increasing fencing tokens, and split-brain mitigation for multi-node
MetroLens API Gateway clusters.

Architectural Design:
--------------------
In high-throughput legal metrology enforcement networks across multiple state data centers,
critical state mutations—such as assigning sequential compounding case numbers, sealing
judicial dockets, and reconciling cyber treasury receipts—must be executed by exactly ONE
active leader node at any instant.

Features:
---------
1. Heartbeat-backed lease coordinator with configurable TTL (default 15.0s).
2. Monotonically increasing 64-bit fencing tokens to prevent zombie leader split-brain writes.
3. Majority Quorum requirement: Leadership is automatically relinquished if node loses
   contact with > 50% of the active cluster peers.
4. Thread-safe atomic lease CAS (Compare-And-Swap) in memory with persistence hooks.
"""

from __future__ import annotations

import datetime
import enum
import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("metrolens.services.leader_election")


class NodeRole(str, enum.Enum):
    """Cluster role of an individual gateway instance."""
    LEADER = "leader"
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    QUORUM_LOST = "quorum_lost"


@dataclass
class LeaseRecord:
    """Active distributed lease holding cluster leadership."""
    leader_node_id: str
    fencing_token: int
    lease_epoch: int
    acquired_at: datetime.datetime
    expires_at: datetime.datetime
    lease_ttl_seconds: float
    renew_count: int = 0

    def is_valid_at(self, current_time: datetime.datetime) -> bool:
        """Evaluates whether the lease remains unexpired."""
        return current_time < self.expires_at


@dataclass
class ClusterNodeInfo:
    """Diagnostic state of a participating cluster node."""
    node_id: str
    host_address: str
    port: int
    role: NodeRole
    last_heartbeat: datetime.datetime
    is_active: bool = True


@dataclass
class ElectionDiagnostics:
    """Telemetry report describing cluster leadership state."""
    current_leader_id: Optional[str]
    active_fencing_token: int
    lease_time_remaining_seconds: float
    local_node_role: NodeRole
    active_cluster_nodes_count: int
    total_cluster_nodes_count: int
    quorum_achieved: bool


class LeaderElectionCoordinator:
    """
    Cluster leader election coordinator with monotonic fencing tokens
    and quorum heartbeat enforcement.
    """

    def __init__(
        self,
        local_node_id: str,
        cluster_peers: Optional[List[str]] = None,
        lease_ttl_seconds: float = 15.0,
        heartbeat_interval_seconds: float = 3.0,
        initial_fencing_token: int = 1000,
    ):
        self.local_node_id = local_node_id
        self.lease_ttl_seconds = max(2.0, lease_ttl_seconds)
        self.heartbeat_interval_seconds = heartbeat_interval_seconds

        self._lock = threading.RLock()
        self._current_lease: Optional[LeaseRecord] = None
        self._fencing_token_counter: int = initial_fencing_token  # Initial base epoch

        # Registered cluster nodes
        self._nodes: Dict[str, ClusterNodeInfo] = {}
        now = datetime.datetime.now()
        # Register local node
        self._nodes[local_node_id] = ClusterNodeInfo(
            node_id=local_node_id,
            host_address="127.0.0.1",
            port=8000,
            role=NodeRole.FOLLOWER,
            last_heartbeat=now,
        )
        if cluster_peers:
            for peer in cluster_peers:
                if peer != local_node_id:
                    self._nodes[peer] = ClusterNodeInfo(
                        node_id=peer,
                        host_address="127.0.0.1",
                        port=8001,
                        role=NodeRole.FOLLOWER,
                        last_heartbeat=now,
                    )

    # -------------------------------------------------------------------------
    # Lease Management API
    # -------------------------------------------------------------------------

    def try_acquire_or_renew_lease(self) -> Tuple[bool, Optional[LeaseRecord]]:
        """
        Attempts to acquire leadership or renew an existing lease.
        Enforces quorum check and atomic CAS.
        """
        with self._lock:
            now = datetime.datetime.now()

            # 1. Quorum verification: require majority (> 50%) active nodes
            active_count = self._count_active_nodes(now)
            total_nodes = max(len(self._nodes), 1)
            quorum_needed = (total_nodes // 2) + 1

            if active_count < quorum_needed:
                logger.warning(
                    f"Node {self.local_node_id} cannot acquire/renew lease: quorum lost "
                    f"({active_count}/{total_nodes} active, required {quorum_needed})."
                )
                self._nodes[self.local_node_id].role = NodeRole.QUORUM_LOST
                if self._current_lease and self._current_lease.leader_node_id == self.local_node_id:
                    # Relinquish immediately to avoid split brain
                    self._current_lease = None
                return False, None

            # 2. Check current lease
            if self._current_lease is None or not self._current_lease.is_valid_at(now):
                # Lease is free or expired: acquire leadership
                self._fencing_token_counter += 1
                new_lease = LeaseRecord(
                    leader_node_id=self.local_node_id,
                    fencing_token=self._fencing_token_counter,
                    lease_epoch=self._fencing_token_counter,
                    acquired_at=now,
                    expires_at=now + datetime.timedelta(seconds=self.lease_ttl_seconds),
                    lease_ttl_seconds=self.lease_ttl_seconds,
                    renew_count=0,
                )
                self._current_lease = new_lease
                self._nodes[self.local_node_id].role = NodeRole.LEADER
                logger.info(
                    f"Node {self.local_node_id} ACQUIRED leadership lease. "
                    f"Fencing token: {new_lease.fencing_token}, TTL: {self.lease_ttl_seconds}s."
                )
                return True, new_lease

            # 3. Existing lease is still valid: can we renew?
            if self._current_lease.leader_node_id == self.local_node_id:
                # Renew leadership lease
                self._current_lease.expires_at = now + datetime.timedelta(seconds=self.lease_ttl_seconds)
                self._current_lease.renew_count += 1
                self._nodes[self.local_node_id].role = NodeRole.LEADER
                return True, self._current_lease

            # Another node holds an active lease
            self._nodes[self.local_node_id].role = NodeRole.FOLLOWER
            return False, self._current_lease

    def step_down(self) -> None:
        """Voluntarily abdicates leadership."""
        with self._lock:
            if self._current_lease and self._current_lease.leader_node_id == self.local_node_id:
                logger.info(f"Node {self.local_node_id} stepping down from leadership.")
                self._current_lease = None
            self._nodes[self.local_node_id].role = NodeRole.FOLLOWER

    def record_peer_heartbeat(self, peer_node_id: str, is_leader: bool = False) -> None:
        """Updates liveness timestamp for a peer node."""
        with self._lock:
            now = datetime.datetime.now()
            if peer_node_id not in self._nodes:
                self._nodes[peer_node_id] = ClusterNodeInfo(
                    node_id=peer_node_id,
                    host_address="127.0.0.1",
                    port=8000,
                    role=NodeRole.LEADER if is_leader else NodeRole.FOLLOWER,
                    last_heartbeat=now,
                )
            else:
                node = self._nodes[peer_node_id]
                node.last_heartbeat = now
                node.is_active = True
                if is_leader:
                    node.role = NodeRole.LEADER

    def validate_fencing_token(self, presented_token: int) -> bool:
        """
        Guards state mutation against split-brain writes.
        Validates that presented token matches the CURRENT active leader token.
        """
        with self._lock:
            now = datetime.datetime.now()
            if self._current_lease is None or not self._current_lease.is_valid_at(now):
                return False
            return presented_token == self._current_lease.fencing_token

    def get_diagnostics(self) -> ElectionDiagnostics:
        """Returns comprehensive diagnostic telemetry."""
        with self._lock:
            now = datetime.datetime.now()
            active_count = self._count_active_nodes(now)
            total_nodes = max(len(self._nodes), 1)
            quorum_needed = (total_nodes // 2) + 1

            leader_id = None
            fencing_tok = 0
            time_remaining = 0.0

            if self._current_lease and self._current_lease.is_valid_at(now):
                leader_id = self._current_lease.leader_node_id
                fencing_tok = self._current_lease.fencing_token
                time_remaining = max(0.0, (self._current_lease.expires_at - now).total_seconds())

            return ElectionDiagnostics(
                current_leader_id=leader_id,
                active_fencing_token=fencing_tok,
                lease_time_remaining_seconds=time_remaining,
                local_node_role=self._nodes[self.local_node_id].role,
                active_cluster_nodes_count=active_count,
                total_cluster_nodes_count=total_nodes,
                quorum_achieved=(active_count >= quorum_needed),
            )

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    def _count_active_nodes(self, now: datetime.datetime) -> int:
        """Nodes are considered active if heartbeat was received within 3x interval."""
        active = 0
        threshold_seconds = self.heartbeat_interval_seconds * 3.5
        for nid, info in self._nodes.items():
            if nid == self.local_node_id:
                active += 1
            else:
                elapsed = (now - info.last_heartbeat).total_seconds()
                if elapsed <= threshold_seconds:
                    active += 1
                else:
                    info.is_active = False
        return active
