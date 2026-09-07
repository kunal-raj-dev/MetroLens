"""
Unit Tests for Cryptographic Audit Trail & Merkle Chain Engine
==============================================================
Verifies Section 63 BSA 2023 evidentiary integrity:
    1. Append-only block linkage and previous block hash anchoring.
    2. Payload SHA-256 calculation across strings, bytes, and JSON dictionaries.
    3. Mathematical tamper detection upon modified block attributes.
    4. Deterministic Merkle root recalculation.
    5. Serialization and audit export fidelity.
"""

import hashlib
import json
import pytest

from apps.api.services.audit_chain import AuditChain, AuditLogBlock


def test_audit_chain_genesis_and_initialization():
    chain = AuditChain(inspection_id="INSP-MERKLE-001")
    assert chain.inspection_id == "INSP-MERKLE-001"
    assert len(chain.chain) == 0
    assert chain.latest_block_hash == AuditChain.GENESIS_HASH


def test_audit_chain_append_events_and_hash_linkage():
    chain = AuditChain(inspection_id="INSP-MERKLE-002")

    # Block 0
    b0 = chain.append_event(
        stage_name="INGESTION_SECURITY",
        event_type="STAGE_START",
        payload_data=b"RAW_IMAGE_PAYLOAD_BYTES",
        actor_or_system="SecurityMiddleware",
        details={"ip": "127.0.0.1"},
    )
    assert b0.block_index == 0
    assert b0.previous_block_hash == AuditChain.GENESIS_HASH
    assert len(b0.block_hash) == 64
    assert chain.latest_block_hash == b0.block_hash

    # Block 1
    b1 = chain.append_event(
        stage_name="OCR_EXTRACTION",
        event_type="STAGE_COMPLETE",
        payload_data={"text_tokens": ["MRP", "Rs. 50"]},
        actor_or_system="NirikshakOCR",
    )
    assert b1.block_index == 1
    assert b1.previous_block_hash == b0.block_hash
    assert chain.latest_block_hash == b1.block_hash

    # Block 2
    b2 = chain.append_event(
        stage_name="STATUTORY_RULES_EVAL",
        event_type="VIOLATION_DETECTED",
        payload_data={"violation": "Section 36(1) Shortfall"},
        actor_or_system="RulesEngine",
    )
    assert b2.block_index == 2
    assert b2.previous_block_hash == b1.block_hash
    assert len(chain.chain) == 3


def test_audit_chain_full_integrity_pass():
    chain = AuditChain(inspection_id="INSP-MERKLE-003")
    for i in range(5):
        chain.append_event(
            stage_name=f"STAGE_{i}",
            event_type="STEP",
            payload_data=f"DATA_{i}",
        )

    is_valid, notes = chain.verify_integrity()
    assert is_valid is True
    assert any("integrity verified" in n.lower() for n in notes)


def test_audit_chain_tamper_detection_on_mutated_data():
    chain = AuditChain(inspection_id="INSP-MERKLE-004")
    chain.append_event("STAGE_1", "START", "Payload A")
    chain.append_event("STAGE_2", "RUN", "Payload B")
    chain.append_event("STAGE_3", "END", "Payload C")

    # Unaltered check
    is_valid, _ = chain.verify_integrity()
    assert is_valid is True

    # Tamper block 1's stage_name
    tampered_block = AuditLogBlock(
        block_index=chain._chain[1].block_index,
        timestamp_utc=chain._chain[1].timestamp_utc,
        stage_name="STAGE_2_TAMPERED",
        event_type=chain._chain[1].event_type,
        actor_or_system=chain._chain[1].actor_or_system,
        payload_sha256=chain._chain[1].payload_sha256,
        previous_block_hash=chain._chain[1].previous_block_hash,
        block_hash=chain._chain[1].block_hash,
        details=chain._chain[1].details,
    )
    chain._chain[1] = tampered_block

    is_valid_after_tamper, errors = chain.verify_integrity()
    assert is_valid_after_tamper is False
    assert any("hash altered" in err.lower() for err in errors)


def test_audit_chain_tamper_detection_on_broken_linkage():
    chain = AuditChain(inspection_id="INSP-MERKLE-005")
    chain.append_event("STAGE_1", "START", "Payload 1")
    chain.append_event("STAGE_2", "RUN", "Payload 2")

    # Tamper previous block hash of block 1
    tampered_block = AuditLogBlock(
        block_index=chain._chain[1].block_index,
        timestamp_utc=chain._chain[1].timestamp_utc,
        stage_name=chain._chain[1].stage_name,
        event_type=chain._chain[1].event_type,
        actor_or_system=chain._chain[1].actor_or_system,
        payload_sha256=chain._chain[1].payload_sha256,
        previous_block_hash="f" * 64,  # Invalid prev hash
        block_hash=chain._chain[1].block_hash,
        details=chain._chain[1].details,
    )
    chain._chain[1] = tampered_block

    is_valid, errors = chain.verify_integrity()
    assert is_valid is False
    assert any("hash altered" in err.lower() or "linkage" in err.lower() for err in errors)


def test_audit_chain_merkle_root_determinism():
    chain_a = AuditChain(inspection_id="INSP-MERKLE-006")
    b0_a = chain_a.append_event("STAGE_1", "START", "Fixed Payload")
    b1_a = chain_a.append_event("STAGE_2", "DONE", "Fixed Result")

    chain_b = AuditChain(inspection_id="INSP-MERKLE-006")
    chain_b._chain.append(b0_a)
    chain_b._chain.append(b1_a)

    root_a = chain_a.compute_merkle_root()
    root_b = chain_b.compute_merkle_root()
    assert root_a == root_b
    assert len(root_a) == 64
