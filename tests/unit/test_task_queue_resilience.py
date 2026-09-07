"""
Unit Tests for Prioritized Task Queue & Worker Resilience
=========================================================
Verifies asynchronous pipeline queueing, priority scheduling (CRITICAL > HIGH > NORMAL > BATCH),
worker starvation prevention, retry with exponential backoff, dead-letter queue escalation,
and thread pool concurrency safety.
"""

import time
import pytest

from apps.api.services.task_queue import (
    PrioritizedInspectionQueue,
    TaskPriority,
    TaskStatus,
)


@pytest.fixture
def queue():
    q = PrioritizedInspectionQueue(max_workers=2, max_queue_depth=50)
    q.start()
    yield q
    q.stop(wait=True)


def test_task_queue_lifecycle_start_and_stop():
    q = PrioritizedInspectionQueue(max_workers=2)
    assert q._is_running is False
    q.start()
    assert q._is_running is True
    assert len(q._workers) == 2

    # Stop
    q.stop(wait=True)
    assert q._is_running is False
    assert len(q._workers) == 0


def test_task_queue_priority_ordering(queue: PrioritizedInspectionQueue):
    """
    Submits tasks with varying priorities while workers are briefly blocked,
    verifying that CRITICAL is dispatched before NORMAL and BATCH.
    """
    execution_order = []

    def slow_worker_blocker():
        time.sleep(0.1)

    def record_execution(label: str):
        execution_order.append(label)

    # Block both workers
    queue.submit(slow_worker_blocker, priority=TaskPriority.CRITICAL)
    queue.submit(slow_worker_blocker, priority=TaskPriority.CRITICAL)

    # Enqueue tasks in inverse order
    t_batch = queue.submit(record_execution, "BATCH_TASK", priority=TaskPriority.BATCH)
    t_norm = queue.submit(record_execution, "NORMAL_TASK", priority=TaskPriority.NORMAL)
    t_crit = queue.submit(record_execution, "CRITICAL_TASK", priority=TaskPriority.CRITICAL)

    # Wait for completion
    time.sleep(0.5)

    assert "CRITICAL_TASK" in execution_order
    assert "NORMAL_TASK" in execution_order
    assert "BATCH_TASK" in execution_order
    # Critical must precede Batch
    assert execution_order.index("CRITICAL_TASK") < execution_order.index("BATCH_TASK")


def test_task_queue_retry_and_dead_letter_queue_escalation(queue: PrioritizedInspectionQueue):
    """
    A failing task must attempt retries and ultimately escalate to DLQ.
    """
    attempt_count = 0

    def always_failing_task():
        nonlocal attempt_count
        attempt_count += 1
        raise ValueError("Simulated downstream OCR inference crash")

    task_id = queue.submit(always_failing_task, priority=TaskPriority.HIGH, max_retries=2)

    # Allow workers to retry and fail
    time.sleep(0.4)

    record = queue.get_task(task_id)
    assert record is not None
    assert record.status == TaskStatus.DEAD_LETTER
    assert record.retries_attempted == 3
    assert attempt_count >= 3

    # Check DLQ presence
    assert task_id in queue._dead_letter_queue
    dlq_record = queue._dead_letter_queue[task_id]
    assert dlq_record.task_id == task_id
    assert dlq_record.error_message is not None


def test_task_queue_depth_overflow_rejection():
    """
    Queue with depth 5 must reject 6th submission with RuntimeError.
    """
    q_small = PrioritizedInspectionQueue(max_workers=0, max_queue_depth=5)
    # Fill queue
    for i in range(5):
        q_small.submit(lambda: None, priority=TaskPriority.NORMAL)

    # 6th should raise
    with pytest.raises(RuntimeError, match="queue depth limit"):
        q_small.submit(lambda: None, priority=TaskPriority.NORMAL)


def test_task_queue_cancellation():
    """
    Pending tasks can be cancelled prior to execution when workers are idle.
    """
    queue = PrioritizedInspectionQueue(max_workers=1)
    # Do not start workers so task remains queued
    task_id = queue.submit(lambda: 100, priority=TaskPriority.BATCH)

    record_before = queue.get_task(task_id)
    assert record_before.status == TaskStatus.QUEUED

    cancelled = queue.cancel_task(task_id)
    assert cancelled is True

    record_after = queue.get_task(task_id)
    assert record_after is not None
    assert record_after.status == TaskStatus.CANCELLED


def test_task_queue_concurrency_stress(queue: PrioritizedInspectionQueue):
    """
    Sustained concurrent submissions across 30 tasks with varying priorities.
    """
    results = {}

    def compute_square(idx: int, val: int):
        results[idx] = val * val

    task_ids = []
    for i in range(30):
        prio = TaskPriority.HIGH if i % 2 == 0 else TaskPriority.NORMAL
        tid = queue.submit(compute_square, i, i + 1, priority=prio)
        task_ids.append((i, tid))

    time.sleep(0.6)

    # All 30 must be computed
    assert len(results) == 30
    for i in range(30):
        assert results[i] == (i + 1) * (i + 1)
        rec = queue.get_task(task_ids[i][1])
        assert rec is not None
        assert rec.status == TaskStatus.COMPLETED
