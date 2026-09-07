"""
Unit Tests for Chunk 2: Ephemeral Spool Manager & Session Lifecycle Service.
Verifies:
1. Isolated session directory creation (/tmp/metrolens_uploads/<uuid>/).
2. Atomic file persistence for raw image, sanitized image, evidence crops, and PDF reports.
3. Safe atomic write semantics preventing partial file corruption.
4. 60-minute TTL expiration logic and automated session purging.
5. Server startup sweep purging stale directories from previous runs.
6. Explicit session purging and memory cleanup.
7. Total spool disk usage calculation and quota enforcement.
8. Background cleanup daemon lifecycle (clean start and stop).
"""

import os
import time
import shutil
import tempfile
from pathlib import Path
import pytest

from apps.api.services.spool_service import (
    SpoolService,
    SpoolSession,
    DEFAULT_TTL_SECONDS,
)


@pytest.fixture
def temp_spool_dir():
    """Provides an isolated temporary directory for test spool operations."""
    test_dir = Path(tempfile.mkdtemp(prefix="metrolens_test_spool_"))
    yield test_dir
    # Cleanup after test
    shutil.rmtree(test_dir, ignore_errors=True)


@pytest.fixture
def test_spool_service(temp_spool_dir):
    """Initializes a SpoolService instance pointing to isolated test temp directory."""
    service = SpoolService(
        base_dir=temp_spool_dir,
        ttl_seconds=2,  # 2-second TTL for fast automated expiration testing
        cleanup_interval_seconds=1,
        auto_start_daemon=False,  # Control manually in tests
    )
    yield service
    service.stop_cleanup_daemon()


def test_create_session(test_spool_service):
    """Verifies that create_session allocates an isolated directory on disk."""
    session = test_spool_service.create_session("INSP-TEST-001")
    assert session.inspection_id == "INSP-TEST-001"
    assert session.session_dir.exists()
    assert session.session_dir.is_dir()
    assert session.session_dir.name == "INSP-TEST-001"


def test_atomic_file_persistence(test_spool_service):
    """Verifies atomic write of raw image, sanitized image, crops, and PDF reports."""
    session_id = "INSP-ATOMIC-002"
    raw_bytes = b"\xff\xd8\xff\xe0" + b"RAW_PIXEL_DATA" * 50
    sanitized_bytes = b"\xff\xd8\xff\xe0" + b"SANITIZED_DATA" * 50
    crop_bytes = b"\xff\xd8\xff\xe0" + b"NET_QTY_CROP" * 10
    pdf_bytes = b"%PDF-1.7" + b"MOCK_ASSESSMENT_REPORT" * 20

    # Save raw
    raw_path = test_spool_service.save_raw_image(session_id, raw_bytes, extension=".jpg")
    assert raw_path.exists()
    assert raw_path.read_bytes() == raw_bytes

    # Save sanitized
    sanitized_path = test_spool_service.save_sanitized_image(session_id, sanitized_bytes, extension=".jpg")
    assert sanitized_path.exists()
    assert sanitized_path.read_bytes() == sanitized_bytes

    # Save crop
    crop_path = test_spool_service.save_crop(session_id, "net_quantity", crop_bytes)
    assert crop_path.exists()
    assert crop_path.read_bytes() == crop_bytes
    assert crop_path.parent.name == "crops"

    # Save PDF report
    pdf_path = test_spool_service.save_pdf_report(session_id, pdf_bytes)
    assert pdf_path.exists()
    assert pdf_path.read_bytes() == pdf_bytes

    # Retrieve PDF report via service
    retrieved_pdf = test_spool_service.get_pdf_report(session_id)
    assert retrieved_pdf == pdf_bytes


def test_atomic_file_cleans_temporary_swap_file(test_spool_service):
    """Verifies that atomic write leaves no dangling .tmp files on disk."""
    session = test_spool_service.create_session("INSP-TMP-CLEAN")
    target_file = session.session_dir / "test_file.bin"

    test_spool_service._write_file_atomically(target_file, b"HELLO_ATOMIC_METROLENS")
    assert target_file.exists()
    assert target_file.read_bytes() == b"HELLO_ATOMIC_METROLENS"

    # Verify no .tmp files remain in directory
    tmp_files = list(session.session_dir.glob("*.tmp"))
    assert len(tmp_files) == 0


def test_session_ttl_expiration(test_spool_service):
    """Verifies that a session past its TTL is recognized as expired and purged upon retrieval."""
    session = test_spool_service.create_session("INSP-EXPIRY-003")
    assert not session.is_expired(ttl_seconds=2)

    # Wait for TTL to lapse (2-second test TTL)
    time.sleep(2.1)
    assert session.is_expired(ttl_seconds=2)

    # get_session should return None and purge the directory from disk
    retrieved = test_spool_service.get_session("INSP-EXPIRY-003")
    assert retrieved is None
    assert not session.session_dir.exists()


def test_purge_expired_sessions_sweep(test_spool_service):
    """Verifies purge_expired_sessions deletes all expired sessions from both memory and disk."""
    s1 = test_spool_service.create_session("INSP-SWEEP-001")
    s2 = test_spool_service.create_session("INSP-SWEEP-002")
    test_spool_service.save_raw_image("INSP-SWEEP-001", b"DATA_1")
    test_spool_service.save_raw_image("INSP-SWEEP-002", b"DATA_2")

    time.sleep(2.1)
    purged_count = test_spool_service.purge_expired_sessions()
    assert purged_count >= 2
    assert not s1.session_dir.exists()
    assert not s2.session_dir.exists()


def test_startup_sweep(test_spool_service):
    """Verifies that startup_sweep completely purges all leftover session directories."""
    # Create multiple sessions simulating prior crashes
    s1 = test_spool_service.create_session("CRASHED-001")
    s2 = test_spool_service.create_session("CRASHED-002")
    test_spool_service.save_raw_image("CRASHED-001", b"CRASHED_DATA_1")
    test_spool_service.save_raw_image("CRASHED-002", b"CRASHED_DATA_2")

    assert s1.session_dir.exists()
    assert s2.session_dir.exists()

    removed = test_spool_service.startup_sweep()
    assert removed >= 2
    assert not s1.session_dir.exists()
    assert not s2.session_dir.exists()
    assert len(list(test_spool_service.base_dir.iterdir())) == 0


def test_explicit_session_purge(test_spool_service):
    """Verifies that explicit purge_session deletes the session directory immediately."""
    session = test_spool_service.create_session("EXPLICIT-PURGE-001")
    test_spool_service.save_raw_image("EXPLICIT-PURGE-001", b"SOME_DATA")
    assert session.session_dir.exists()

    result = test_spool_service.purge_session("EXPLICIT-PURGE-001")
    assert result is True
    assert not session.session_dir.exists()


def test_disk_quota_enforcement(test_spool_service):
    """Verifies that enforce_quota prunes the oldest session when quota limit is reached."""
    # Set a tiny quota of 500 bytes for testing
    test_spool_service.max_quota_bytes = 500

    s1 = test_spool_service.create_session("OLD-SESSION-001")
    test_spool_service.save_raw_image("OLD-SESSION-001", b"A" * 400)

    time.sleep(0.05)  # Ensure s2 has newer timestamp
    s2 = test_spool_service.create_session("NEW-SESSION-002")
    test_spool_service.save_raw_image("NEW-SESSION-002", b"B" * 400)

    total_size = test_spool_service.get_total_spool_size_bytes()
    assert total_size >= 800

    pruned = test_spool_service.enforce_quota()
    assert pruned >= 1
    # Oldest session should have been pruned first
    assert not s1.session_dir.exists()


def test_daemon_lifecycle(temp_spool_dir):
    """Verifies that the background TTL cleaner thread starts and stops gracefully."""
    service = SpoolService(
        base_dir=temp_spool_dir,
        ttl_seconds=1,
        cleanup_interval_seconds=1,
        auto_start_daemon=True,
    )
    assert service._daemon_thread is not None
    assert service._daemon_thread.is_alive()

    # Create a session and verify the daemon purges it
    s = service.create_session("DAEMON-EXPIRY-001")
    service.save_raw_image("DAEMON-EXPIRY-001", b"PAYLOAD")
    assert s.session_dir.exists()

    # Wait for daemon sweep
    time.sleep(2.5)
    assert not s.session_dir.exists()

    # Stop daemon
    service.stop_cleanup_daemon()
    assert service._daemon_thread is None
