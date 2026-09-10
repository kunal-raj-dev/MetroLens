"""Storage boundary regressions; every filesystem target belongs to tmp_path."""

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import time

import pytest


@pytest.fixture
def storage(tmp_path, monkeypatch):
    # The production module starts a singleton at import time. Load a separate
    # module with an isolated root so collecting/running these tests never uses
    # the application's ambient spool or cleanup daemon.
    root = tmp_path.resolve(strict=True)
    monkeypatch.setenv("METROLENS_SPOOL_DIR", str(root / "import-spool"))
    module_name = "_spool_boundary_regression"
    source = Path(__file__).resolve().parents[2] / "apps/api/services/spool_service.py"
    spec = importlib.util.spec_from_file_location(module_name, source)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, module_name, module)
    spec.loader.exec_module(module)
    module.spool_service.stop_cleanup_daemon()
    service = module.SpoolService(base_dir=root / "spool", auto_start_daemon=False)
    victim = root / "victim"
    victim.mkdir()
    sentinel = victim / "sentinel.txt"
    sentinel.write_bytes(b"outside-spool sentinel")
    assert service.base_dir.resolve().is_relative_to(root)
    assert victim.resolve().is_relative_to(root)
    assert not victim.resolve().is_relative_to(service.base_dir.resolve())
    yield service, victim, sentinel
    service.stop_cleanup_daemon()


def test_expired_pdf_lookup_cannot_delete_sibling(storage):
    service, victim, sentinel = storage
    old = time.time() - service.ttl_seconds - 10
    os.utime(victim, (old, old))
    with pytest.raises(ValueError):
        service.get_pdf_report("../victim")
    assert sentinel.read_bytes() == b"outside-spool sentinel"


@pytest.mark.parametrize("operation", ["create", "get", "purge", "raw", "sanitized", "crop", "pdf"])
@pytest.mark.parametrize("absolute", [False, True])
def test_session_operations_reject_escaping_ids(storage, operation, absolute):
    service, victim, sentinel = storage
    identifier = str(victim.resolve()) if absolute else "../victim"
    operations = {
        "create": lambda: service.create_session(identifier),
        "get": lambda: service.get_session(identifier),
        "purge": lambda: service.purge_session(identifier),
        "raw": lambda: service.save_raw_image(identifier, b"changed"),
        "sanitized": lambda: service.save_sanitized_image(identifier, b"changed"),
        "crop": lambda: service.save_crop(identifier, "net_quantity", b"changed"),
        "pdf": lambda: service.save_pdf_report(identifier, b"changed"),
    }
    with pytest.raises(ValueError):
        operations[operation]()
    assert list(victim.iterdir()) == [sentinel]
    assert sentinel.read_bytes() == b"outside-spool sentinel"


@pytest.mark.parametrize("identifier", ["", ".", "..", "insp/child", "insp\\child", "insp:stream", "insp.", "insp ", "insp\x00", "CON", "com1", "LPT9", "inspection_é", "a" * 129])
def test_invalid_identifiers_are_rejected_before_creation(storage, identifier):
    service, _, _ = storage
    with pytest.raises(ValueError):
        service.create_session(identifier)
    assert list(service.base_dir.iterdir()) == []


@pytest.mark.parametrize("extension", [".jpg/../../victim/changed", "jpg\\..\\changed", ".jpg:stream", "..", "", ".jpg.exe", ".jpg\x00"])
@pytest.mark.parametrize("method", ["save_raw_image", "save_sanitized_image"])
def test_image_extensions_are_single_safe_suffixes(storage, extension, method):
    service, victim, sentinel = storage
    with pytest.raises(ValueError):
        getattr(service, method)("INSP-EXT", b"changed", extension)
    assert list(service.base_dir.iterdir()) == []
    assert list(victim.iterdir()) == [sentinel]


@pytest.mark.parametrize("field", ["", "..", "../net_quantity", "net/quantity", "net\\quantity", "net:quantity", "CON", "net quantity", "x" * 129])
def test_crop_names_are_validated_without_silent_collisions(storage, field):
    service, _, _ = storage
    with pytest.raises(ValueError):
        service.save_crop("INSP-CROP", field, b"changed")
    assert list(service.base_dir.iterdir()) == []


def _directory_link(link, target, owned_root):
    """Create only a link and destination within the already verified test root."""
    assert link.absolute().is_relative_to(owned_root)
    assert target.resolve(strict=True).is_relative_to(owned_root)
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError as error:
        if os.name != "nt":
            pytest.skip(f"Directory symlinks unavailable: {error}")
        # Windows junctions do not require Developer Mode / symlink privilege.
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True, text=True, check=False,
        )
        if result.returncode:
            pytest.skip(f"Directory junction unavailable: {result.stderr}")


@pytest.mark.parametrize("operation", ["get", "create", "write", "purge", "startup", "ttl", "quota", "size"])
def test_session_directory_link_never_reaches_sibling(storage, operation):
    service, victim, sentinel = storage
    link = service.base_dir / "INSP-LINK"
    _directory_link(link, victim, service.base_dir.parent)
    old = time.time() - service.ttl_seconds - 10
    os.utime(victim, (old, old))
    if operation in {"get", "create", "write", "purge"}:
        operations = {
            "get": lambda: service.get_session(link.name),
            "create": lambda: service.create_session(link.name),
            "write": lambda: service.save_raw_image(link.name, b"changed"),
            "purge": lambda: service.purge_session(link.name),
        }
        with pytest.raises(ValueError):
            operations[operation]()
    else:
        service.max_quota_bytes = 0
        operations = {
            "startup": service.startup_sweep,
            "ttl": service.purge_expired_sessions,
            "quota": service.enforce_quota,
            "size": service.get_total_spool_size_bytes,
        }
        assert operations[operation]() == 0
    assert sentinel.read_bytes() == b"outside-spool sentinel"
    assert list(victim.iterdir()) == [sentinel]


def test_cached_session_directory_is_rechecked(storage):
    service, victim, sentinel = storage
    session = service.create_session("INSP-CACHED")
    session.session_dir.rmdir()
    _directory_link(session.session_dir, victim, service.base_dir.parent)
    with pytest.raises(ValueError):
        service.get_session(session.inspection_id)
    with pytest.raises(ValueError):
        service.save_pdf_report(session.inspection_id, b"changed")
    assert sentinel.read_bytes() == b"outside-spool sentinel"


def test_pdf_read_rejects_cached_external_path(storage):
    service, _, sentinel = storage
    session = service.create_session("INSP-READ")
    session.pdf_report_path = sentinel
    with pytest.raises(ValueError):
        service.get_pdf_report(session.inspection_id)


def test_crop_directory_link_and_recursive_cleanup_are_rejected(storage):
    service, victim, sentinel = storage
    session = service.create_session("INSP-CROPS")
    _directory_link(session.session_dir / "crops", victim, service.base_dir.parent)
    with pytest.raises(ValueError):
        service.save_crop(session.inspection_id, "net_quantity", b"changed")
    with pytest.raises(ValueError):
        service.purge_session(session.inspection_id)
    assert service.startup_sweep() == 0
    assert sentinel.read_bytes() == b"outside-spool sentinel"


def test_atomic_write_cannot_target_external_file(storage):
    service, _, sentinel = storage
    with pytest.raises(ValueError):
        service._write_file_atomically(sentinel, b"changed")
    assert sentinel.read_bytes() == b"outside-spool sentinel"


@pytest.mark.parametrize("operation", ["read", "write", "startup", "ttl", "size"])
def test_replaced_spool_root_is_rejected(storage, operation):
    service, victim, sentinel = storage
    service.base_dir.rmdir()
    _directory_link(service.base_dir, victim, service.base_dir.parent)
    operations = {
        "read": lambda: service.get_pdf_report("INSP-ROOT"),
        "write": lambda: service.save_raw_image("INSP-ROOT", b"changed"),
        "startup": service.startup_sweep,
        "ttl": service.purge_expired_sessions,
        "size": service.get_total_spool_size_bytes,
    }
    with pytest.raises(ValueError):
        operations[operation]()
    assert list(victim.iterdir()) == [sentinel]


def test_preexisting_link_cannot_become_the_spool_root(storage):
    service, victim, sentinel = storage
    linked_root = service.base_dir.parent / "linked-root"
    _directory_link(linked_root, victim, service.base_dir.parent)
    with pytest.raises(ValueError):
        type(service)(base_dir=linked_root, auto_start_daemon=False)
    assert list(victim.iterdir()) == [sentinel]


@pytest.mark.parametrize("operation", ["startup", "ttl", "quota"])
def test_cleanup_skips_linked_entries_and_removes_owned_sessions(storage, operation):
    service, victim, sentinel = storage
    session = service.create_session("INSP-OWNED")
    service.save_raw_image(session.inspection_id, b"owned")
    session.created_at_utc = time.time() - service.ttl_seconds - 10
    _directory_link(service.base_dir / "INSP-LINK", victim, service.base_dir.parent)
    service.max_quota_bytes = 0
    operations = {
        "startup": service.startup_sweep,
        "ttl": service.purge_expired_sessions,
        "quota": service.enforce_quota,
    }
    assert operations[operation]() == 1
    assert not session.session_dir.exists()
    assert sentinel.read_bytes() == b"outside-spool sentinel"


def test_expired_orphan_cleanup_is_still_supported(storage):
    service, _, sentinel = storage
    session = service.create_session("INSP-ORPHAN")
    service.save_pdf_report(session.inspection_id, b"owned")
    service._sessions.clear()
    old = time.time() - service.ttl_seconds - 10
    os.utime(session.session_dir, (old, old))
    assert service.purge_expired_sessions() == 1
    assert not session.session_dir.exists()
    assert sentinel.exists()


def test_pdf_paths_cannot_read_a_different_inspection(storage):
    service, _, _ = storage
    session = service.create_session("INSP-FIRST")
    other = service.save_pdf_report("INSP-SECOND", b"other inspection")
    session.pdf_report_path = other
    with pytest.raises(ValueError):
        service.get_pdf_report(session.inspection_id)


def test_failed_delete_is_not_counted_or_removed_from_registry(storage, monkeypatch):
    service, _, sentinel = storage
    session = service.create_session("INSP-RETRY")
    module = sys.modules[service.__class__.__module__]

    def fail_delete(path):
        assert path.resolve().is_relative_to(service.base_dir.resolve())
        raise PermissionError("Simulated busy file")

    monkeypatch.setattr(module.shutil, "rmtree", fail_delete)
    assert service.purge_session(session.inspection_id) is False
    assert service.get_session(session.inspection_id) is session
    assert session.session_dir.exists()
    assert sentinel.exists()


def test_failed_atomic_replace_cleans_only_its_own_temporary_file(storage, monkeypatch):
    service, _, sentinel = storage
    session = service.create_session("INSP-ATOMIC")
    module = sys.modules[service.__class__.__module__]

    def fail_replace(source, destination):
        assert source.resolve().is_relative_to(service.base_dir.resolve())
        assert destination.resolve().is_relative_to(service.base_dir.resolve())
        raise OSError("Simulated rename failure")

    monkeypatch.setattr(module.os, "replace", fail_replace)
    with pytest.raises(OSError, match="rename failure"):
        service.save_raw_image(session.inspection_id, b"owned")
    assert list(session.session_dir.iterdir()) == []
    assert sentinel.read_bytes() == b"outside-spool sentinel"


@pytest.mark.parametrize("identifier", ["INSP-20260909-ABCDEF12", "insp_a5d3341a", "CRASHED-001", "EXPLICIT-PURGE-001"])
def test_legitimate_ids_write_recover_and_expire(storage, identifier):
    service, _, sentinel = storage
    service.save_raw_image(identifier, b"raw", "JPG")
    service.save_sanitized_image(identifier, b"sanitized", ".png")
    service.save_crop(identifier, "net_quantity", b"crop")
    service.save_pdf_report(identifier, b"%PDF-safe")
    assert service.get_pdf_report(identifier) == b"%PDF-safe"
    assert service.get_total_spool_size_bytes() == len(b"rawsanitizedcrop%PDF-safe")
    service._sessions.clear()
    assert service.get_pdf_report(identifier) == b"%PDF-safe"
    session = service.get_session(identifier)
    assert session is not None
    assert list(session.session_dir.rglob("*.tmp")) == []
    session.created_at_utc = time.time() - service.ttl_seconds - 10
    assert service.get_session(identifier) is None
    assert not session.session_dir.exists()
    assert sentinel.read_bytes() == b"outside-spool sentinel"
