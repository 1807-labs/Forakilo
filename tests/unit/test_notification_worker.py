from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

from foreightkillo.bot.contracts import DeliveryFailure, DeliveryResult
from foreightkillo.notifications.events import Visibility
from foreightkillo.notifications.outbox import OutboxRecord, OutboxState, SQLiteOutbox
from foreightkillo.notifications.projections import Notification, NotificationPriority
from foreightkillo.notifications.worker import OutboxWorker


@dataclass
class FixedClock:
    current: datetime

    def now(self) -> datetime:
        return self.current


@dataclass
class Handler:
    fail_message_id: str | None = None
    stopped: bool = False

    def deliver(self, record: OutboxRecord) -> DeliveryResult:
        if record.message_id == self.fail_message_id:
            return DeliveryResult(
                record.outbox_id,
                False,
                None,
                DeliveryFailure("permanent", False, "invalid destination"),
            )
        return DeliveryResult(record.outbox_id, True, "provider-message", None)

    def shutdown(self) -> None:
        self.stopped = True


def _notification(message_id: str) -> Notification:
    now = datetime(2026, 7, 29, tzinfo=UTC)
    return Notification(
        message_id,
        f"event-{message_id}",
        "system",
        NotificationPriority.NORMAL,
        "Health",
        "Healthy",
        (),
        now,
        None,
        Visibility.OPERATOR,
        "installation",
        None,
        message_id,
        True,
    )


def test_worker_isolates_destination_failure_and_stops(tmp_path: Path) -> None:
    clock = FixedClock(datetime(2026, 7, 29, tzinfo=UTC))
    outbox = SQLiteOutbox(tmp_path / "outbox.sqlite", clock)
    failed_id = outbox.enqueue(_notification("bad"), "one", "local", "key-one")
    delivered_id = outbox.enqueue(_notification("good"), "two", "local", "key-two")
    handler = Handler("bad")
    worker = OutboxWorker(outbox, handler, "worker", timedelta(seconds=30))

    assert worker.run_once() == 2
    assert outbox.get(failed_id).state is OutboxState.DEAD_LETTER
    assert outbox.get(delivered_id).state is OutboxState.DELIVERED

    worker.shutdown()
    assert handler.stopped
