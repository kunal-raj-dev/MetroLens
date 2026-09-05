"""
Integration Tests for Advanced Services (Audit Chain, Task Queue, Cache)
========================================================================
Tests Merkle audit chain verification, prioritized task queue execution,
and two-tier perceptual image cache retrieval.
"""

import io
import time
from PIL import Image
import pytest

from apps.api.services.audit_chain import AuditChain, AuditLogBlock
from apps.api.services.task_queue import (
    PrioritizedInspectionQueue,
    TaskPriority,
    TaskStatus,
)
from apps.api.services.inspection_cache import TwoTierInspectionCache


def _create_sample_jpeg_bytes() -> bytes:
    img = Image.new("RGB", (200, 200), color=(220, 220, 220))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# 1. Audit Chain & Merkle Ledger Tests
# ---------------------------------------------------------------------------

def test_audit_chain_append_and_merkle_integrity():
    """Verify sequential event appending, Merkle root calculation, and tamper proofing."""
    chain = AuditChain(inspection_id="INS-AUDIT-001")

    # Append 3 lifecycle events
    b0 = chain.append_event("INGESTION_SECURITY", "VALIDATION_PASSED", b"RAW_IMAGE_BYTES")
    b1 = chain.append_event("OCR_EXTRACTION", "TOKENS_EXTRACTED", {"token_count": 8})
    b2 = chain.append_event("STATUTORY_RULES_EVAL", "EVAL_COMPLETE", {"violations": 0})

    assert len(chain.chain) == 3
    assert b0.block_index == 0
    assert b1.block_index == 1
    assert b2.block_index == 2
    assert b1.previous_block_hash == b0.block_hash
    assert b2.previous_block_hash == b1.block_hash

    # Merkle root calculation
    root = chain.compute_merkle_root()
    assert isinstance(root, str)
    assert len(root) == 64

    # Verify integrity
    is_valid, notes = chain.verify_integrity()
    assert is_valid is True
    assert any("verified" in n.lower() for n in notes)


def test_audit_chain_detects_tampered_history():
    """Verify that tampering with an intermediate block causes integrity failure."""
    chain = AuditChain(inspection_id="INS-AUDIT-TAMPER")
    chain.append_event("STAGE_1", "EVENT_1", "PAYLOAD_1")
    chain.append_event("STAGE_2", "EVENT_2", "PAYLOAD_2")
    chain.append_event("STAGE_3", "EVENT_3", "PAYLOAD_3")

    # Simulate unauthorized database modification on block 1
    tampered_block = AuditLogBlock(
        block_index=1,
        timestamp_utc=chain._chain[1].timestamp_utc,
        stage_name="FORGED_STAGE",  # Tampered field
        event_type=chain._chain[1].event_type,
        actor_or_system=chain._chain[1].actor_or_system,
        payload_sha256=chain._chain[1].payload_sha256,
        previous_block_hash=chain._chain[1].previous_block_hash,
        block_hash=chain._chain[1].block_hash,  # Non-matching hash now
        details=chain._chain[1].details,
    )
    chain._chain[1] = tampered_block

    is_valid, notes = chain.verify_integrity()
    assert is_valid is False
    assert any("altered" in n.lower() or "broken" in n.lower() for n in notes)


# ---------------------------------------------------------------------------
# 2. Prioritized Task Queue Tests
# ---------------------------------------------------------------------------

def test_task_queue_priority_and_worker_execution():
    """Verify task submission, prioritized execution, and results retrieval."""
    queue = PrioritizedInspectionQueue(max_workers=2)
    queue.start()

    try:
        def sample_work(x: int, multiplier: int = 2) -> int:
            return x * multiplier

        # Submit task with NORMAL priority
        t_id = queue.submit(sample_work, 21, multiplier=2, priority=TaskPriority.NORMAL)
        assert t_id.startswith("TASK-")

        # Wait briefly for completion
        time.sleep(0.15)

        record = queue.get_task(t_id)
        assert record is not None
        assert record.status == TaskStatus.COMPLETED
        assert record.result == 42
        assert record.progress_percent == 100

        metrics = queue.get_queue_metrics()
        assert metrics["completed_count"] >= 1
    finally:
        queue.stop()


def test_task_queue_cancellation():
    """Verify cancelling a queued task before execution."""
    queue = PrioritizedInspectionQueue(max_workers=1)
    # Don't start workers so task remains in QUEUED state
    t_id = queue.submit(lambda: 100, priority=TaskPriority.BATCH)

    record_before = queue.get_task(t_id)
    assert record_before.status == TaskStatus.QUEUED

    cancelled = queue.cancel_task(t_id)
    assert cancelled is True

    record_after = queue.get_task(t_id)
    assert record_after.status == TaskStatus.CANCELLED


# ---------------------------------------------------------------------------
# 3. Two-Tier Inspection Cache Tests
# ---------------------------------------------------------------------------

def test_two_tier_inspection_cache_sha_and_phash(tmp_path):
    """Verify exact SHA hits, perceptual pHash hits, and misses."""
    cache = TwoTierInspectionCache(disk_cache_dir=tmp_path, stripe_capacity=64)
    raw_img = _create_sample_jpeg_bytes()

    declarations = {"mrp": "Rs. 99", "net_quantity": "500g"}

    # Initial lookup should miss
    entry_miss, hit_type = cache.lookup(raw_img)
    assert entry_miss is None
    assert hit_type == "MISS"

    # Store entry
    stored = cache.put(
        image_bytes=raw_img,
        commodity_type="FMCG_Snacks",
        canonical_declarations=declarations,
        compliance_verdict="COMPLIANT",
    )
    assert stored.sha256_hash is not None

    # Immediate lookup by exact same image -> SHA_HIT
    entry_sha, hit_sha = cache.lookup(raw_img)
    assert entry_sha is not None
    assert hit_sha == "SHA_HIT"
    assert entry_sha.canonical_declarations["mrp"] == "Rs. 99"

    # Re-encode slightly to change SHA while keeping visual structure
    with Image.open(io.BytesIO(raw_img)) as img:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        recomp_bytes = buf.getvalue()

    # Perceptual lookup should match via PHASH_HIT
    entry_phash, hit_phash = cache.lookup(recomp_bytes)
    assert entry_phash is not None
    assert hit_phash == "PHASH_HIT"

    stats = cache.get_stats()
    assert stats["hits_sha"] >= 1
    assert stats["hits_phash"] >= 1
    assert stats["hit_ratio"] > 0.5
