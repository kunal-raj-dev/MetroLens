"""
Nirikshak Ephemeral Spool Manager & Session Lifecycle Service.
Implements the zero-permanent storage architecture mandated by ADR-014 and docs/API_CONTRACT.md:
1. In-memory io.BytesIO streaming priority with on-demand isolated disk spooling.
2. Per-inspection directory isolation (/tmp/metrolens_uploads/<uuid>/).
3. Atomic file writes with temporary suffix and os.replace semantics.
4. Background TTL garbage collection thread (default 60 minutes retention).
5. Server startup sweep purging orphaned temporary files from prior crashes.
6. Disk quota monitoring and emergency high-watermark pruning.
7. Cross-platform support (Windows, Linux, macOS).
"""

import os
import re
import shutil
import stat
import tempfile
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from apps.api.identifiers import validate_crop_name, validate_inspection_id


DEFAULT_TTL_SECONDS: int = 3600  # 60 Minutes retention
DEFAULT_CLEANUP_INTERVAL_SECONDS: int = 60  # Sweep every 60 seconds
MAX_SPOOL_DISK_USAGE_BYTES: int = 2 * 1024 * 1024 * 1024  # 2.0 GB quota cap
MIN_FREE_DISK_SPACE_BYTES: int = 100 * 1024 * 1024       # 100 MB safety floor


@dataclass
class SpoolSession:
    """Represents an isolated ephemeral workspace for a single packaging inspection run."""
    inspection_id: str
    session_dir: Path
    created_at_utc: float = field(default_factory=time.time)
    last_accessed_utc: float = field(default_factory=time.time)
    raw_image_path: Optional[Path] = None
    sanitized_image_path: Optional[Path] = None
    pdf_report_path: Optional[Path] = None
    crop_paths: Dict[str, Path] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def age_seconds(self) -> float:
        return time.time() - self.created_at_utc

    def is_expired(self, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> bool:
        return self.age_seconds > ttl_seconds

    def touch(self) -> None:
        self.last_accessed_utc = time.time()


class SpoolService:
    """
    Thread-safe ephemeral spooling service managing inspection session files.
    """

    _instance: Optional["SpoolService"] = None
    _lock: threading.Lock = threading.Lock()

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
        cleanup_interval_seconds: int = DEFAULT_CLEANUP_INTERVAL_SECONDS,
        max_quota_bytes: int = MAX_SPOOL_DISK_USAGE_BYTES,
        auto_start_daemon: bool = True,
    ):
        if base_dir is None:
            env_path = os.environ.get("METROLENS_SPOOL_DIR")
            base_path = Path(env_path) if env_path else Path(tempfile.gettempdir()) / "metrolens_uploads"
        else:
            base_path = Path(base_dir)
        self._reject_link(base_path)
        self.base_dir = base_path.resolve()

        self.ttl_seconds = ttl_seconds
        self.cleanup_interval_seconds = cleanup_interval_seconds
        self.max_quota_bytes = max_quota_bytes

        # Active session registry
        self._sessions: Dict[str, SpoolSession] = {}
        self._session_lock = threading.RLock()

        # Background daemon controls
        self._daemon_thread: Optional[threading.Thread] = None
        self._stop_event: threading.Event = threading.Event()

        # Initialize storage directory
        self._checked_root()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._checked_root()

        if auto_start_daemon:
            self.start_cleanup_daemon()

    @staticmethod
    def _reject_link(path: Path) -> None:
        """Reject symlinks and Windows reparse points, including junctions."""
        try:
            info = path.lstat()
        except FileNotFoundError:
            return
        if stat.S_ISLNK(info.st_mode) or (
            getattr(info, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        ):
            raise ValueError("Spool paths must not contain links or reparse points")

    def _checked_path(self, path: Path, inspection_id: Optional[str] = None) -> Path:
        """Check lexical and resolved containment before touching a spool path.

        Existing components are checked individually so even links pointing back
        inside the spool cannot alias another inspection's files.
        """
        path = Path(path)
        self._checked_root()
        try:
            relative = path.relative_to(self.base_dir)
        except ValueError as error:
            raise ValueError("Path is outside the spool root") from error
        if not relative.parts or any(part in {".", ".."} for part in relative.parts):
            raise ValueError("Path must identify a child of the spool root")
        validate_inspection_id(relative.parts[0])
        if inspection_id is not None and relative.parts[0] != validate_inspection_id(inspection_id):
            raise ValueError("Path belongs to a different inspection")
        component = self.base_dir
        for part in relative.parts:
            if (
                re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,254}", part) is None
                or part.endswith(".")
                or PureWindowsPath(part).is_reserved()
            ):
                raise ValueError("Spool path contains an unsafe filename")
            component /= part
            self._reject_link(component)
        try:
            resolved_relative = path.resolve().relative_to(self.base_dir)
        except (ValueError, RuntimeError) as error:
            raise ValueError("Resolved path is outside the spool root") from error
        if resolved_relative != relative:
            raise ValueError("Spool path changed its resolved location")
        return path

    def _checked_root(self) -> Path:
        self._reject_link(self.base_dir)
        if self.base_dir.resolve() != self.base_dir:
            raise ValueError("Spool root changed its resolved location")
        return self.base_dir

    def _session_path(self, inspection_id: str) -> Path:
        validate_inspection_id(inspection_id)
        return self._checked_path(self.base_dir / inspection_id, inspection_id)

    def _checked_session(self, session: SpoolSession, inspection_id: str) -> Path:
        expected = self._session_path(inspection_id)
        if session.inspection_id != inspection_id or session.session_dir != expected:
            raise ValueError("Session directory does not match its inspection ID")
        return expected

    def _ensure_directory(self, path: Path) -> Path:
        path = self._checked_path(path)
        path.mkdir(parents=True, exist_ok=True)
        return self._checked_path(path)

    @staticmethod
    def _image_extension(extension: str) -> str:
        if not isinstance(extension, str) or re.fullmatch(r"\.?[A-Za-z0-9]{1,10}", extension) is None:
            raise ValueError("Image extension must be a single alphanumeric suffix")
        return "." + extension.lstrip(".").lower()

    def _remove_session_directory(self, inspection_id: str) -> bool:
        """Validate the entire tree before recursive deletion, without following links."""
        session_dir = self._session_path(inspection_id)
        if not session_dir.is_dir():
            return False
        pending = [session_dir]
        while pending:
            directory = self._checked_path(pending.pop(), inspection_id)
            for entry in directory.iterdir():
                entry = self._checked_path(entry, inspection_id)
                if entry.is_dir():
                    pending.append(entry)
        # Recheck the entry point immediately before recursive deletion. Python's
        # rmtree also refuses a top-level symlink and does not traverse junctions.
        session_dir = self._session_path(inspection_id)
        try:
            shutil.rmtree(session_dir)
        except OSError:
            return False
        return True

    @classmethod
    def get_instance(cls, **kwargs) -> "SpoolService":
        """Singleton accessor for SpoolService."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(**kwargs)
            return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Resets singleton state, terminating background daemon (useful in tests)."""
        with cls._lock:
            if cls._instance is not None:
                cls._instance.stop_cleanup_daemon()
                cls._instance = None

    def startup_sweep(self) -> int:
        """
        Executes on server boot: clears stale directories from prior runs or crashes.
        Returns count of removed directories.
        """
        with self._session_lock:
            removed_count = 0
            self._checked_root()
            if not self.base_dir.exists():
                return 0

            for entry in list(self.base_dir.iterdir()):
                try:
                    if self._remove_session_directory(entry.name):
                        removed_count += 1
                except (OSError, ValueError):
                    continue

            self._sessions.clear()
            return removed_count

    def create_session(self, inspection_id: Optional[str] = None) -> SpoolSession:
        """
        Creates a new isolated session directory under the base spool root.
        """
        if inspection_id is None:
            now_str = datetime.now(timezone.utc).strftime("%Y%m%d")
            rand_suffix = uuid.uuid4().hex[:8].upper()
            inspection_id = f"INSP-{now_str}-{rand_suffix}"

        with self._session_lock:
            session_dir = self._ensure_directory(self._session_path(inspection_id))
            session = SpoolSession(
                inspection_id=inspection_id,
                session_dir=session_dir,
            )
            self._sessions[inspection_id] = session

        return session

    def get_session(self, inspection_id: str) -> Optional[SpoolSession]:
        """Retrieves session record if it exists and has not expired."""
        with self._session_lock:
            session_dir = self._session_path(inspection_id)
            session = self._sessions.get(inspection_id)
            if session:
                self._checked_session(session, inspection_id)
                if session.is_expired(self.ttl_seconds):
                    self._purge_session_internal(inspection_id)
                    return None
                session.touch()
                return session

            # Check if directory exists on disk even if not in memory (e.g. after worker restart)
            if session_dir.is_dir():
                self._checked_path(session_dir, inspection_id)
                mtime = session_dir.stat().st_mtime
                age = time.time() - mtime
                if age > self.ttl_seconds:
                    self._remove_session_directory(inspection_id)
                    return None

                recovered_session = SpoolSession(
                    inspection_id=inspection_id,
                    session_dir=session_dir,
                    created_at_utc=mtime,
                    last_accessed_utc=time.time(),
                )
                report_path = self._checked_path(
                    session_dir / f"metrolens_report_{inspection_id}.pdf", inspection_id
                )
                if report_path.is_file():
                    recovered_session.pdf_report_path = report_path
                self._sessions[inspection_id] = recovered_session
                return recovered_session

            return None

    def _write_file_atomically(self, target_path: Path, content: bytes) -> Path:
        """
        Writes data to a temporary file in the same directory and executes
        an atomic rename (os.replace) to prevent partial reads by concurrent processes.
        """
        with self._session_lock:
            target_path = self._checked_path(target_path)
            self._ensure_directory(target_path.parent)
            temp_path = target_path.with_name(f"{target_path.name}.{uuid.uuid4().hex}.tmp")
            created = False
            try:
                self._checked_path(temp_path)
                with open(temp_path, "xb") as f:
                    created = True
                    f.write(content)
                    f.flush()
                    os.fsync(f.fileno())
                self._checked_path(temp_path)
                self._checked_path(target_path)
                os.replace(temp_path, target_path)
                return target_path
            finally:
                if created:
                    try:
                        self._checked_path(temp_path)
                        temp_path.unlink(missing_ok=True)
                    except (OSError, ValueError):
                        pass

    def save_raw_image(self, inspection_id: str, content: bytes, extension: str = ".jpg") -> Path:
        """Saves original raw uploaded image bytes into the session spool."""
        ext = self._image_extension(extension)
        with self._session_lock:
            session = self.get_session(inspection_id) or self.create_session(inspection_id)
            target_path = session.session_dir / f"raw_image{ext}"
            self._write_file_atomically(target_path, content)
            session.raw_image_path = target_path
            session.touch()
            return target_path

    def save_sanitized_image(self, inspection_id: str, content: bytes, extension: str = ".jpg") -> Path:
        """Saves EXIF-stripped sanitized image bytes into the session spool."""
        ext = self._image_extension(extension)
        with self._session_lock:
            session = self.get_session(inspection_id) or self.create_session(inspection_id)
            target_path = session.session_dir / f"sanitized_image{ext}"
            self._write_file_atomically(target_path, content)
            session.sanitized_image_path = target_path
            session.touch()
            return target_path

    def save_crop(self, inspection_id: str, field_name: str, content: bytes) -> Path:
        """Saves a single evidence crop into the session spool."""
        safe_field = validate_crop_name(field_name)
        with self._session_lock:
            session = self.get_session(inspection_id) or self.create_session(inspection_id)
            crops_dir = self._ensure_directory(session.session_dir / "crops")
            target_path = crops_dir / f"{safe_field}.jpg"
            self._write_file_atomically(target_path, content)
            session.crop_paths[field_name] = target_path
            session.touch()
            return target_path

    def save_pdf_report(self, inspection_id: str, pdf_bytes: bytes) -> Path:
        """Saves generated tamper-evident assessment report PDF into the session spool."""
        with self._session_lock:
            session = self.get_session(inspection_id) or self.create_session(inspection_id)
            target_path = session.session_dir / f"metrolens_report_{inspection_id}.pdf"
            self._write_file_atomically(target_path, pdf_bytes)
            session.pdf_report_path = target_path
            session.touch()
            return target_path

    def get_pdf_report(self, inspection_id: str) -> Optional[bytes]:
        """Retrieves PDF report binary if within the TTL retention window."""
        with self._session_lock:
            session = self.get_session(inspection_id)
            if not session or not session.pdf_report_path:
                return None
            report_path = self._checked_path(session.pdf_report_path, inspection_id)
            if not report_path.is_file():
                return None
            return self._checked_path(report_path, inspection_id).read_bytes()

    def purge_session(self, inspection_id: str) -> bool:
        """Explicitly purges and deletes an inspection session directory."""
        with self._session_lock:
            return self._purge_session_internal(inspection_id)

    def _purge_session_internal(self, inspection_id: str) -> bool:
        """Internal helper running within _session_lock."""
        self._session_path(inspection_id)
        session = self._sessions.get(inspection_id)
        if session is not None:
            self._checked_session(session, inspection_id)
        removed = self._remove_session_directory(inspection_id)
        if removed or not self._session_path(inspection_id).exists():
            self._sessions.pop(inspection_id, None)
        return removed

    def purge_expired_sessions(self) -> int:
        """
        Sweeps through active sessions and disk directories, removing any exceeding TTL.
        Returns count of purged sessions.
        """
        purged = 0
        now = time.time()

        with self._session_lock:
            # 1. Sweep in-memory registry
            expired_ids = [
                iid for iid, s in self._sessions.items()
                if (now - s.created_at_utc) > self.ttl_seconds
            ]
            for iid in expired_ids:
                try:
                    if self._purge_session_internal(iid):
                        purged += 1
                except (OSError, ValueError):
                    continue

            # 2. Sweep disk directory for untracked or orphaned directories
            self._checked_root()
            if self.base_dir.exists():
                for entry in list(self.base_dir.iterdir()):
                    try:
                        entry = self._session_path(entry.name)
                        if entry.is_dir() and entry.name not in self._sessions:
                            mtime = entry.stat().st_mtime
                            if (now - mtime) > self.ttl_seconds:
                                if self._remove_session_directory(entry.name):
                                    purged += 1
                    except (OSError, ValueError):
                        continue

        return purged

    def get_total_spool_size_bytes(self) -> int:
        """Computes total disk storage consumed by current spool directory."""
        with self._session_lock:
            total = 0
            self._checked_root()
            if not self.base_dir.exists():
                return 0
            pending = list(self.base_dir.iterdir())
            while pending:
                try:
                    entry = self._checked_path(pending.pop())
                    if entry.is_dir():
                        pending.extend(entry.iterdir())
                    elif entry.is_file():
                        total += self._checked_path(entry).stat().st_size
                except (OSError, ValueError):
                    continue
            return total

    def enforce_quota(self) -> int:
        """
        If total spool storage exceeds max_quota_bytes, prunes oldest sessions first.
        Returns count of sessions pruned.
        """
        pruned_count = 0
        total_size = self.get_total_spool_size_bytes()

        if total_size <= self.max_quota_bytes:
            return 0

        with self._session_lock:
            # Sort sessions by oldest created
            sorted_sessions = sorted(
                self._sessions.values(),
                key=lambda s: s.created_at_utc
            )
            for session in sorted_sessions:
                if self.get_total_spool_size_bytes() <= (self.max_quota_bytes * 0.8):
                    break
                try:
                    if self._purge_session_internal(session.inspection_id):
                        pruned_count += 1
                except (OSError, ValueError):
                    continue

        return pruned_count

    def start_cleanup_daemon(self) -> None:
        """Launches the background TTL cleanup worker daemon."""
        if self._daemon_thread is not None and self._daemon_thread.is_alive():
            return

        self._stop_event.clear()
        self._daemon_thread = threading.Thread(
            target=self._run_cleanup_loop,
            daemon=True,
            name="MetroLens-Spool-TTL-Cleaner",
        )
        self._daemon_thread.start()

    def stop_cleanup_daemon(self) -> None:
        """Signals background daemon to terminate and waits for thread exit."""
        self._stop_event.set()
        if self._daemon_thread is not None and self._daemon_thread.is_alive():
            self._daemon_thread.join(timeout=2.0)
            self._daemon_thread = None

    def _run_cleanup_loop(self) -> None:
        """Background daemon polling loop executed every cleanup_interval_seconds."""
        while not self._stop_event.is_set():
            try:
                self.purge_expired_sessions()
                self.enforce_quota()
            except Exception:
                pass
            # Sleep with interrupt check
            self._stop_event.wait(timeout=self.cleanup_interval_seconds)


spool_service = SpoolService.get_instance()
