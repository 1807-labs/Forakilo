"""Lease-aware outbox delivery loop with destination-level failure isolation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from threading import Event
from typing import Protocol

from foreightkillo.bot.contracts import DeliveryFailure, DeliveryResult

from .outbox import FailureClass, OutboxRecord, SQLiteOutbox


class OutboxDeliveryHandler(Protocol):
    def deliver(self, record: OutboxRecord) -> DeliveryResult: ...


def classify_failure(failure: DeliveryFailure) -> FailureClass:
    try:
        return FailureClass(failure.classification)
    except ValueError:
        return FailureClass.TRANSIENT if failure.retryable else FailureClass.PERMANENT


@dataclass(slots=True)
class OutboxWorker:
    outbox: SQLiteOutbox
    handler: OutboxDeliveryHandler
    worker_id: str
    lease: timedelta = timedelta(seconds=30)
    batch_size: int = 20
    _stop: Event = field(default_factory=Event, init=False, repr=False)

    def run_once(self) -> int:
        records = self.outbox.claim(self.worker_id, self.batch_size, self.lease)
        for record in records:
            self._deliver_one(record)
        return len(records)

    def run(self, idle_wait_seconds: float = 1.0) -> None:
        if idle_wait_seconds < 0:
            raise ValueError("idle wait cannot be negative")
        while not self._stop.is_set():
            if self.run_once() == 0:
                self._stop.wait(idle_wait_seconds)

    def shutdown(self) -> None:
        self._stop.set()
        shutdown = getattr(self.handler, "shutdown", None)
        if callable(shutdown):
            shutdown()

    def _deliver_one(self, record: OutboxRecord) -> None:
        self.outbox.mark_delivering(record.outbox_id, self.worker_id)
        try:
            result = self.handler.deliver(record)
        except Exception as error:  # destination failures must not block the batch
            self.outbox.mark_failed(
                record.outbox_id,
                self.worker_id,
                FailureClass.TRANSIENT,
                f"delivery handler exception: {type(error).__name__}",
            )
            return
        if result.accepted:
            self.outbox.mark_delivered(record.outbox_id, self.worker_id)
            return
        failure = result.failure or DeliveryFailure(
            FailureClass.TRANSIENT,
            True,
            "provider rejected delivery without a failure classification",
        )
        self.outbox.mark_failed(
            record.outbox_id,
            self.worker_id,
            classify_failure(failure),
            failure.redacted_detail,
        )
