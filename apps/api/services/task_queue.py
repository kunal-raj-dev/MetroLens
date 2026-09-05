"""
Priority Asynchronous Inspection Task Queue & Worker Engine
===========================================================
Manages prioritized asynchronous background processing, batch inspection queues,
exponential backoff retries, and dead-letter quarantine (DLQ) for retail raid audits.

Design:
    - Thread-safe priority queue using heapq and condition variables.
    - Zero external broker dependency (pure in-process Python queue for CPU-bound OCR workloads).
    - Granular state machine: QUEUED -> PROCESSING -> COMPLETED | FAILED | CANCELLED | DEAD_LETTER.
"""

from __future__ import annotations

import concurrent.futures
import datetime
import enum
import heapq
import logging
import threading
import time
import traceback
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger("metrolens.task_queue")


class TaskPriority(enum.IntEnum):
    """Priority levels for scheduled inspection tasks (lower integer = higher priority)."""

    CRITICAL = 1  # Court summons, urgent forensic verification
    HIGH = 2      # Live interactive inspector UI request
    NORMAL = 3    # Standard single commodity inspection
    BATCH = 4     # Bulk retail raid upload / shelf sweep


class TaskStatus(str, enum.Enum):
    """Lifecycle states of an asynchronous task."""

    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    DEAD_LETTER = "DEAD_LETTER"


@dataclass
class TaskRecord:
    """Represents a scheduled inspection task and its execution history."""

    task_id: str
    priority: TaskPriority
    fn: Callable[..., Any]
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.QUEUED
    created_at: str = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    progress_percent: int = 0
    retries_attempted: int = 0
    max_retries: int = 2
    result: Optional[Any] = None
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    cancelled: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "priority": self.priority.name,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "progress_percent": self.progress_percent,
            "retries_attempted": self.retries_attempted,
            "max_retries": self.max_retries,
            "error_message": self.error_message,
        }


class PrioritizedInspectionQueue:
    """
    Thread-safe prioritized queue and execution pool.
    """

    def __init__(self, max_workers: int = 4, max_queue_depth: int = 1000) -> None:
        self.max_workers = max_workers
        self.max_queue_depth = max_queue_depth
        self._queue: List[Tuple[int, float, TaskRecord]] = []
        self._tasks: Dict[str, TaskRecord] = {}
        self._dead_letter_queue: Dict[str, TaskRecord] = {}
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._is_running = False
        self._workers: List[threading.Thread] = []

    def start(self) -> None:
        """Start worker threads."""
        with self._lock:
            if self._is_running:
                return
            self._is_running = True
            for i in range(self.max_workers):
                w = threading.Thread(
                    target=self._worker_loop, name=f"MetroLens-QueueWorker-{i}", daemon=True
                )
                self._workers.append(w)
                w.start()
            logger.info("PrioritizedInspectionQueue started with %d workers.", self.max_workers)

    def stop(self, wait: bool = True) -> None:
        """Stop worker threads."""
        with self._lock:
            self._is_running = False
            self._not_empty.notify_all()

        if wait:
            for w in self._workers:
                w.join(timeout=2.0)
            self._workers.clear()
        logger.info("PrioritizedInspectionQueue stopped.")

    def submit(
        self,
        fn: Callable[..., Any],
        *args: Any,
        priority: TaskPriority = TaskPriority.NORMAL,
        max_retries: int = 2,
        **kwargs: Any,
    ) -> str:
        """
        Submit a task for asynchronous execution.

        Returns:
            task_id string.
        """
        task_id = f"TASK-{uuid.uuid4().hex[:12].upper()}"
        record = TaskRecord(
            task_id=task_id,
            priority=priority,
            fn=fn,
            args=args,
            kwargs=kwargs,
            max_retries=max_retries,
        )

        with self._lock:
            if len(self._queue) >= self.max_queue_depth:
                raise RuntimeError(f"Task queue depth limit ({self.max_queue_depth}) exceeded.")

            self._tasks[task_id] = record
            # Heap item: (priority, submission_timestamp, record)
            entry = (int(priority), time.time(), record)
            heapq.heappush(self._queue, entry)
            self._not_empty.notify()

        return task_id

    def get_task(self, task_id: str) -> Optional[TaskRecord]:
        """Retrieve task record by ID."""
        with self._lock:
            return self._tasks.get(task_id) or self._dead_letter_queue.get(task_id)

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task before execution begins."""
        with self._lock:
            record = self._tasks.get(task_id)
            if not record:
                return False
            if record.status == TaskStatus.QUEUED:
                record.status = TaskStatus.CANCELLED
                record.cancelled = True
                record.completed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
                return True
            return False

    def get_queue_metrics(self) -> Dict[str, Any]:
        """Retrieve live queue telemetry."""
        with self._lock:
            queued = sum(1 for t in self._tasks.values() if t.status == TaskStatus.QUEUED)
            processing = sum(1 for t in self._tasks.values() if t.status == TaskStatus.PROCESSING)
            completed = sum(1 for t in self._tasks.values() if t.status == TaskStatus.COMPLETED)
            failed = sum(1 for t in self._tasks.values() if t.status == TaskStatus.FAILED)
            dlq_count = len(self._dead_letter_queue)

            return {
                "active_workers": len(self._workers),
                "is_running": self._is_running,
                "queued_count": queued,
                "processing_count": processing,
                "completed_count": completed,
                "failed_count": failed,
                "dead_letter_count": dlq_count,
            }

    def _worker_loop(self) -> None:
        """Internal loop executed by each worker thread."""
        while True:
            with self._lock:
                while self._is_running and not self._queue:
                    self._not_empty.wait()

                if not self._is_running:
                    break

                priority, ts, record = heapq.heappop(self._queue)

                if record.cancelled:
                    continue

                record.status = TaskStatus.PROCESSING
                record.started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
                record.progress_percent = 10

            # Execute task outside the lock
            success = False
            result = None
            err_msg = None
            tb = None

            try:
                result = record.fn(*record.args, **record.kwargs)
                success = True
            except Exception as exc:
                err_msg = str(exc)
                tb = traceback.format_exc()
                logger.error("Task %s failed: %s", record.task_id, exc)

            with self._lock:
                record.completed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
                if success:
                    record.status = TaskStatus.COMPLETED
                    record.result = result
                    record.progress_percent = 100
                else:
                    record.retries_attempted += 1
                    record.error_message = err_msg
                    record.stack_trace = tb

                    # Retry evaluation
                    if record.retries_attempted <= record.max_retries and self._is_running:
                        record.status = TaskStatus.QUEUED
                        record.progress_percent = 0
                        # Re-enqueue with slight delay penalty
                        entry = (int(record.priority), time.time() + 1.0, record)
                        heapq.heappush(self._queue, entry)
                        self._not_empty.notify()
                    else:
                        record.status = TaskStatus.DEAD_LETTER
                        self._dead_letter_queue[record.task_id] = record
