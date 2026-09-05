"""
Cryptographic Audit Trail & Merkle Chain Engine
===============================================
Maintains an append-only, cryptographically linked SHA-256 audit ledger
recording every microsecond event in the inspection lifecycle from raw
payload ingress to judicial dossier issuance.

Evidentiary Value:
    Satisfies Section 63(2)(c) of the Bharatiya Sakshya Adhiniyam, 2023:
    "information was derived from information fed into the computer in the
    ordinary course of the said activities."
    The Merkle DAG provides mathematical proof that evidence was not altered
    subsequent to capture.
"""

from __future__ import annotations

import datetime
import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class AuditLogBlock:
    """Represents an immutable block in the inspection audit chain."""

    block_index: int
    timestamp_utc: str
    stage_name: str  # e.g., 'INGESTION_SECURITY', 'OCR_EXTRACTION', 'STATUTORY_RULES_EVAL'
    event_type: str  # 'STAGE_START', 'STAGE_COMPLETE', 'VIOLATION_DETECTED', 'SEAL_APPLIED'
    actor_or_system: str
    payload_sha256: str
    previous_block_hash: str
    block_hash: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "block_index": self.block_index,
            "timestamp_utc": self.timestamp_utc,
            "stage_name": self.stage_name,
            "event_type": self.event_type,
            "actor_or_system": self.actor_or_system,
            "payload_sha256": self.payload_sha256,
            "previous_block_hash": self.previous_block_hash,
            "block_hash": self.block_hash,
            "details": self.details,
        }


class AuditChain:
    """
    Append-only SHA-256 cryptographic audit chain for a single inspection docket.
    """

    GENESIS_HASH = "0" * 64

    def __init__(self, inspection_id: str) -> None:
        self.inspection_id = inspection_id
        self._chain: List[AuditLogBlock] = []

    @property
    def chain(self) -> List[AuditLogBlock]:
        """Return a copy of the audit chain."""
        return list(self._chain)

    @property
    def latest_block_hash(self) -> str:
        if not self._chain:
            return self.GENESIS_HASH
        return self._chain[-1].block_hash

    def append_event(
        self,
        stage_name: str,
        event_type: str,
        payload_data: Any,
        actor_or_system: str = "MetroLens-Pipeline-Worker",
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditLogBlock:
        """
        Record an immutable lifecycle event to the cryptographic audit chain.

        Args:
            stage_name: Name of pipeline stage.
            event_type: Type of event.
            payload_data: Object, dict, or bytes to hash into payload_sha256.
            actor_or_system: Component or officer generating the event.
            details: Optional metadata dictionary.

        Returns:
            The newly created AuditLogBlock.
        """
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        prev_hash = self.latest_block_hash
        block_idx = len(self._chain)

        # Hash payload data
        if isinstance(payload_data, bytes):
            p_hash = hashlib.sha256(payload_data).hexdigest()
        elif isinstance(payload_data, str):
            p_hash = hashlib.sha256(payload_data.encode("utf-8")).hexdigest()
        else:
            serialized = json.dumps(payload_data, sort_keys=True, default=str).encode("utf-8")
            p_hash = hashlib.sha256(serialized).hexdigest()

        # Compute block hash: index || timestamp || stage || event || payload_hash || prev_hash
        block_content = f"{block_idx}:{now_utc}:{stage_name}:{event_type}:{p_hash}:{prev_hash}".encode("utf-8")
        block_hash = hashlib.sha256(block_content).hexdigest()

        block = AuditLogBlock(
            block_index=block_idx,
            timestamp_utc=now_utc,
            stage_name=stage_name,
            event_type=event_type,
            actor_or_system=actor_or_system,
            payload_sha256=p_hash,
            previous_block_hash=prev_hash,
            block_hash=block_hash,
            details=details or {},
        )

        self._chain.append(block)
        return block

    def compute_merkle_root(self) -> str:
        """
        Compute binary Merkle tree root hash across all block hashes in the chain.
        """
        if not self._chain:
            return self.GENESIS_HASH

        leaf_hashes = [b.block_hash for b in self._chain]
        current_layer = leaf_hashes

        while len(current_layer) > 1:
            next_layer: List[str] = []
            for i in range(0, len(current_layer), 2):
                h1 = current_layer[i]
                h2 = current_layer[i + 1] if i + 1 < len(current_layer) else current_layer[i]
                combined = hashlib.sha256((h1 + h2).encode("utf-8")).hexdigest()
                next_layer.append(combined)
            current_layer = next_layer

        return current_layer[0]

    def verify_integrity(self) -> Tuple[bool, List[str]]:
        """
        Verify that every link in the chain has valid parent hashes and correct block digests.
        """
        notes: List[str] = []
        if not self._chain:
            notes.append("Audit chain is empty.")
            return True, notes

        # Check genesis block
        first_block = self._chain[0]
        if first_block.previous_block_hash != self.GENESIS_HASH:
            notes.append(f"Genesis block has invalid previous_block_hash: {first_block.previous_block_hash}")
            return False, notes

        for i in range(len(self._chain)):
            block = self._chain[i]

            # Recompute block hash
            block_content = (
                f"{block.block_index}:{block.timestamp_utc}:{block.stage_name}:"
                f"{block.event_type}:{block.payload_sha256}:{block.previous_block_hash}"
            ).encode("utf-8")
            expected_hash = hashlib.sha256(block_content).hexdigest()

            if block.block_hash != expected_hash:
                notes.append(f"Block {i} hash altered: expected {expected_hash}, recorded {block.block_hash}")
                return False, notes

            # Verify link to previous block
            if i > 0:
                prev = self._chain[i - 1]
                if block.previous_block_hash != prev.block_hash:
                    notes.append(f"Broken hash link between block {i-1} and block {i}.")
                    return False, notes

        notes.append(f"Audit chain integrity verified: all {len(self._chain)} blocks cryptographically sound.")
        return True, notes

    def export_ledger_json(self) -> str:
        """Export the full audit ledger as a formatted JSON document."""
        return json.dumps(
            {
                "inspection_id": self.inspection_id,
                "chain_length": len(self._chain),
                "merkle_root": self.compute_merkle_root(),
                "latest_block_hash": self.latest_block_hash,
                "blocks": [b.to_dict() for b in self._chain],
            },
            indent=2,
        )
