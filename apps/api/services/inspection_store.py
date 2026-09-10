"""Bounded, expiring canonical inspection records for one API process."""

import hashlib
import hmac
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable

from fastapi import HTTPException

from apps.api.schemas import InspectionResponse
from apps.api.identifiers import validate_inspection_id
from nirikshak_rules_engine.schemas import ComplianceEvaluationResult


@dataclass(frozen=True)
class InspectionRecord:
    inspection_id: str
    principal_id: str
    response: InspectionResponse
    compliance_result: ComplianceEvaluationResult
    raw_sha256: str
    sanitized_sha256: str
    raw_size_bytes: int
    sanitized_size_bytes: int
    created_at: float


class InspectionStore:
    def __init__(self, max_records: int = 128, ttl_seconds: float = 3600,
                 clock: Callable[[], float] = time.monotonic):
        if max_records < 1 or ttl_seconds <= 0:
            raise ValueError("Inspection storage requires positive capacity and TTL.")
        self.max_records = max_records
        self.ttl_seconds = ttl_seconds
        self._clock = clock
        self._records: OrderedDict[str, InspectionRecord] = OrderedDict()
        self._lock = threading.Lock()

    def put(self, response: InspectionResponse, compliance_result: ComplianceEvaluationResult,
            principal_id: str, raw_sha256: str, sanitized_sha256: str,
            raw_size_bytes: int, sanitized_size_bytes: int) -> InspectionRecord:
        inspection_id = validate_inspection_id(response.inspection_id)
        if compliance_result.inspection_id != inspection_id:
            raise ValueError("Canonical assessment and response IDs must match.")
        record = InspectionRecord(
            inspection_id=inspection_id, principal_id=principal_id,
            response=response.model_copy(deep=True),
            compliance_result=compliance_result.model_copy(deep=True),
            raw_sha256=raw_sha256, sanitized_sha256=sanitized_sha256,
            raw_size_bytes=raw_size_bytes, sanitized_size_bytes=sanitized_size_bytes,
            created_at=self._clock(),
        )
        with self._lock:
            self._expire()
            if inspection_id in self._records:
                raise ValueError("An inspection record cannot be replaced.")
            while len(self._records) >= self.max_records:
                self._records.popitem(last=False)
            self._records[inspection_id] = record
        return record

    def _expire(self) -> None:
        now = self._clock()
        expired = [key for key, record in self._records.items()
                   if now - record.created_at >= self.ttl_seconds]
        for key in expired:
            del self._records[key]

    def get(self, inspection_id: str, principal_id: str) -> InspectionRecord | None:
        validate_inspection_id(inspection_id)
        with self._lock:
            self._expire()
            record = self._records.get(inspection_id)
            if record is None or not hmac.compare_digest(record.principal_id, principal_id):
                return None
            return record

    def clear(self) -> None:
        with self._lock:
            self._records.clear()


inspection_store = InspectionStore()


def require_inspection(inspection_id: str, principal_id: str) -> InspectionRecord:
    try:
        record = inspection_store.get(inspection_id, principal_id)
    except ValueError:
        record = None
    if record is None:
        raise HTTPException(404, "Inspection not found or its retention period has expired.")
    return record


def verify_retained_evidence(record: InspectionRecord, spooler) -> dict[str, bool]:
    """Compare retained files to ingestion hashes; this is not identity certification."""
    try:
        session = spooler.get_session(record.inspection_id)
    except (ValueError, OSError):
        return {"raw_image_matches": False, "sanitized_image_matches": False}
    if session is None:
        raise HTTPException(404, "Inspection evidence has expired or is unavailable.")
    checks = {}
    for label, path, expected_hash, expected_size in (
        ("raw_image_matches", session.raw_image_path, record.raw_sha256, record.raw_size_bytes),
        ("sanitized_image_matches", session.sanitized_image_path, record.sanitized_sha256,
         record.sanitized_size_bytes),
    ):
        matches = False
        try:
            if path is not None:
                path = spooler._checked_path(path, record.inspection_id)
            if path is not None and not path.is_symlink() and path.is_file() and path.stat().st_size == expected_size:
                digest = hashlib.sha256()
                with path.open("rb") as stream:
                    remaining = expected_size
                    while remaining:
                        chunk = stream.read(min(65536, remaining))
                        if not chunk:
                            break
                        digest.update(chunk)
                        remaining -= len(chunk)
                    matches = remaining == 0 and not stream.read(1) and hmac.compare_digest(digest.hexdigest(), expected_hash)
        except (ValueError, OSError):
            pass
        checks[label] = bool(matches)
    return checks
