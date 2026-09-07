"""
Immutable Event Sourcing & Audit Replay Subsystem
=================================================
Provides cryptographic append-only event sourcing, hash-chained Merkle logs,
optimistic concurrency control, aggregate projections, and time-travel replay
for Legal Metrology inspection records under Section 63 of Bharatiya Sakshya Adhiniyam, 2023.

Architectural Rationale:
-----------------------
In statutory court prosecutions, defense counsel frequently challenges digital inspection
records by arguing that the database was retrospectively modified by the inspecting agency.
Event sourcing guarantees that every state transition—from initial upload, through forensic
cleaning, OCR parsing, rule violation detection, compounding notice issuance, to court
docket sealing—is recorded as an immutable, cryptographically chained domain event.
"""

from __future__ import annotations

import datetime
import enum
import hashlib
import json
import logging
import threading
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger("metrolens.services.event_sourcing")


class AggregateType(str, enum.Enum):
    """Supported domain aggregate roots."""
    INSPECTION = "InspectionAggregate"
    COMPOUNDING = "CompoundingAggregate"
    PROSECUTION = "ProsecutionAggregate"


@dataclass
class DomainEvent:
    """
    Immutable domain event representing a completed business fact.
    
    Attributes:
        event_id: Unique identifier for this specific event.
        aggregate_id: Identifier of the entity stream (e.g. inspection_id).
        aggregate_type: Type of aggregate root.
        sequence_number: Monotonically increasing 1-indexed version number.
        event_type: Domain identifier (e.g. "InspectionSubmitted", "OCRCompleted").
        timestamp_utc: ISO timestamp when event occurred.
        payload: Structured dictionary of domain facts.
        previous_event_hash: SHA-256 hash of the preceding event in the stream (or "GENESIS").
        event_hash: Cryptographic SHA-256 hash over all fields of this event.
    """
    event_id: str
    aggregate_id: str
    aggregate_type: AggregateType
    sequence_number: int
    event_type: str
    timestamp_utc: str
    payload: Dict[str, Any]
    previous_event_hash: str
    event_hash: str = ""

    def calculate_hash(self) -> str:
        """Computes deterministic SHA-256 hash over event fields."""
        data = {
            "event_id": self.event_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type.value,
            "sequence_number": self.sequence_number,
            "event_type": self.event_type,
            "timestamp_utc": self.timestamp_utc,
            "payload": self.payload,
            "previous_event_hash": self.previous_event_hash,
        }
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest().upper()


@dataclass
class InspectionState:
    """Read-model projection materialized purely from replaying domain events."""
    inspection_id: str
    version: int = 0
    created_at_utc: Optional[str] = None
    status: str = "INITIALIZED"
    raw_image_sha256: Optional[str] = None
    sanitized_image_sha256: Optional[str] = None
    forensic_tamper_score: float = 0.0
    is_authentic: bool = True
    ocr_declarations: Dict[str, Any] = field(default_factory=dict)
    rule_violations: List[str] = field(default_factory=list)
    overall_verdict: str = "PENDING"
    compounding_case_id: Optional[str] = None
    court_docket_id: Optional[str] = None
    docket_sha256_seal: Optional[str] = None
    last_event_hash: str = "GENESIS"


class InspectionAggregate:
    """
    Domain aggregate root managing inspection state transitions and business invariants.
    """

    def __init__(self, inspection_id: str):
        self.inspection_id = inspection_id
        self.state = InspectionState(inspection_id=inspection_id)
        self._uncommitted_events: List[DomainEvent] = []

    @property
    def version(self) -> int:
        return self.state.version

    def get_uncommitted_events(self) -> List[DomainEvent]:
        return list(self._uncommitted_events)

    def mark_events_committed(self) -> None:
        self._uncommitted_events.clear()

    # -------------------------------------------------------------------------
    # Event Application / Reducer Pattern
    # -------------------------------------------------------------------------

    def apply(self, event: DomainEvent) -> None:
        """Deterministically mutates the projection based on incoming domain event."""
        self.state.version = event.sequence_number
        self.state.last_event_hash = event.event_hash

        if event.event_type == "InspectionSubmitted":
            self.state.created_at_utc = event.timestamp_utc
            self.state.status = "SUBMITTED"
            self.state.raw_image_sha256 = event.payload.get("raw_image_sha256")

        elif event.event_type == "ImageSanitized":
            self.state.status = "SANITIZED"
            self.state.sanitized_image_sha256 = event.payload.get("sanitized_sha256")

        elif event.event_type == "ForensicsEvaluated":
            self.state.status = "FORENSICS_VERIFIED"
            self.state.forensic_tamper_score = float(event.payload.get("tamper_score", 0.0))
            self.state.is_authentic = bool(event.payload.get("is_authentic", True))

        elif event.event_type == "OCRCompleted":
            self.state.status = "OCR_EXTRACTED"
            self.state.ocr_declarations = event.payload.get("declarations", {})

        elif event.event_type == "RulesEvaluated":
            self.state.status = "EVALUATED"
            self.state.rule_violations = event.payload.get("violations", [])
            self.state.overall_verdict = "NON_COMPLIANT" if self.state.rule_violations else "COMPLIANT"

        elif event.event_type == "CompoundingNoticeIssued":
            self.state.status = "COMPOUNDING_PENDING"
            self.state.compounding_case_id = event.payload.get("case_number")

        elif event.event_type == "CourtDocketSealed":
            self.state.status = "COURT_DOCKET_SEALED"
            self.state.court_docket_id = event.payload.get("docket_id")
            self.state.docket_sha256_seal = event.payload.get("docket_seal")

    # -------------------------------------------------------------------------
    # Command Methods
    # -------------------------------------------------------------------------

    def submit_inspection(self, raw_image_sha256: str) -> None:
        self._record_event(
            event_type="InspectionSubmitted",
            payload={"raw_image_sha256": raw_image_sha256},
        )

    def record_sanitization(self, sanitized_sha256: str) -> None:
        self._record_event(
            event_type="ImageSanitized",
            payload={"sanitized_sha256": sanitized_sha256},
        )

    def record_forensics(self, tamper_score: float, is_authentic: bool) -> None:
        self._record_event(
            event_type="ForensicsEvaluated",
            payload={"tamper_score": tamper_score, "is_authentic": is_authentic},
        )

    def record_ocr(self, declarations: Dict[str, Any]) -> None:
        self._record_event(
            event_type="OCRCompleted",
            payload={"declarations": declarations},
        )

    def record_rule_evaluation(self, violations: List[str]) -> None:
        self._record_event(
            event_type="RulesEvaluated",
            payload={"violations": violations},
        )

    def record_compounding_notice(self, case_number: str, fee_inr: float) -> None:
        self._record_event(
            event_type="CompoundingNoticeIssued",
            payload={"case_number": case_number, "fee_inr": fee_inr},
        )

    def record_court_docket_seal(self, docket_id: str, docket_seal: str) -> None:
        self._record_event(
            event_type="CourtDocketSealed",
            payload={"docket_id": docket_id, "docket_seal": docket_seal},
        )

    def _record_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        next_seq = self.state.version + 1
        prev_hash = self.state.last_event_hash

        event = DomainEvent(
            event_id=str(uuid.uuid4()),
            aggregate_id=self.inspection_id,
            aggregate_type=AggregateType.INSPECTION,
            sequence_number=next_seq,
            event_type=event_type,
            timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            payload=payload,
            previous_event_hash=prev_hash,
        )
        event.event_hash = event.calculate_hash()
        self.apply(event)
        self._uncommitted_events.append(event)


class ConcurrencyError(Exception):
    """Raised when an optimistic lock conflict occurs in event appending."""


class EventStore:
    """
    Append-only, thread-safe Event Store with cryptographic Merkle chain validation
    and time-travel replay.
    """

    def __init__(self):
        self._lock = threading.RLock()
        # Key: aggregate_id -> List[DomainEvent]
        self._streams: Dict[str, List[DomainEvent]] = {}
        # Snapshots: aggregate_id -> (version, InspectionState)
        self._snapshots: Dict[str, Tuple[int, InspectionState]] = {}

    def append_events(
        self,
        aggregate_id: str,
        events: List[DomainEvent],
        expected_version: int,
    ) -> None:
        """
        Appends new uncommitted events to the aggregate stream under optimistic concurrency.
        """
        with self._lock:
            stream = self._streams.setdefault(aggregate_id, [])
            current_version = stream[-1].sequence_number if stream else 0

            if current_version != expected_version:
                raise ConcurrencyError(
                    f"Optimistic concurrency conflict for aggregate '{aggregate_id}'. "
                    f"Expected version: {expected_version}, actual current version: {current_version}."
                )

            prev_hash = stream[-1].event_hash if stream else "GENESIS"
            for ev in events:
                if ev.previous_event_hash != prev_hash:
                    raise ValueError(
                        f"Cryptographic hash chain broken! Event #{ev.sequence_number} declares "
                        f"prev_hash '{ev.previous_event_hash}', expected '{prev_hash}'."
                    )
                # Verify self-hash
                if ev.event_hash != ev.calculate_hash():
                    raise ValueError(f"Event #{ev.sequence_number} hash is invalid or tampered.")

                stream.append(ev)
                prev_hash = ev.event_hash

    def load_aggregate(self, aggregate_id: str) -> Optional[InspectionAggregate]:
        """Loads and rehydrates aggregate by replaying all domain events from genesis."""
        with self._lock:
            if aggregate_id not in self._streams:
                return None

            stream = self._streams[aggregate_id]
            aggregate = InspectionAggregate(inspection_id=aggregate_id)

            # Check snapshot for acceleration
            start_idx = 0
            if aggregate_id in self._snapshots:
                snap_ver, snap_state = self._snapshots[aggregate_id]
                aggregate.state = snap_state
                start_idx = snap_ver

            for ev in stream[start_idx:]:
                aggregate.apply(ev)

            return aggregate

    def replay_to_version(self, aggregate_id: str, target_version: int) -> Optional[InspectionState]:
        """
        Time-travel debugging: rehydrates state exactly as it existed at `target_version`.
        """
        with self._lock:
            if aggregate_id not in self._streams:
                return None

            stream = self._streams[aggregate_id]
            aggregate = InspectionAggregate(inspection_id=aggregate_id)

            for ev in stream:
                if ev.sequence_number > target_version:
                    break
                aggregate.apply(ev)

            return aggregate.state

    def verify_stream_integrity(self, aggregate_id: str) -> Tuple[bool, str]:
        """
        Validates cryptographic tamper-evidence of entire event stream.
        Confirms SHA-256 Merkle chain continuity and event body signatures.
        """
        with self._lock:
            if aggregate_id not in self._streams:
                return False, f"Stream '{aggregate_id}' not found."

            stream = self._streams[aggregate_id]
            expected_prev = "GENESIS"

            for idx, ev in enumerate(stream, start=1):
                if ev.sequence_number != idx:
                    return False, f"Sequence gap at index {idx}: event has version {ev.sequence_number}."
                if ev.previous_event_hash != expected_prev:
                    return False, f"Hash chain break at event #{ev.sequence_number}."
                if ev.event_hash != ev.calculate_hash():
                    return False, f"Data tampering detected at event #{ev.sequence_number}."
                expected_prev = ev.event_hash

            return True, f"Stream intact. {len(stream)} events verified cryptographically."
