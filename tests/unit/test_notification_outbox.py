from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from foreightkillo.notifications.events import Visibility
from foreightkillo.notifications.outbox import FailureClass, OutboxState, SQLiteOutbox
from foreightkillo.notifications.projections import Notification, NotificationPriority


@dataclass
class FakeClock:
    value: datetime

    def now(self) -> datetime:
        return self.value

    def advance(self, delta: timedelta) -> None:
        self.value += delta


NOW = datetime(2026, 7, 29, tzinfo=UTC)


def notification(expires: datetime | None = None) -> Notification:
    return Notification(
        "message-1",
        "event-1",
        "signal",
        NotificationPriority.NORMAL,
        "Signal eligible",
        "EUR_USD long; paper only.",
        (("status", "eligible"),),
        NOW,
        expires,
        Visibility.MEMBER,
        "installation",
        None,
        "dedupe-1",
        True,
    )


def outbox(path: Path, clock: FakeClock, max_attempts: int = 3) -> SQLiteOutbox:
    return SQLiteOutbox(path / "outbox.db", clock, max_attempts, timedelta(seconds=1))


def test_enqueue_and_duplicate_suppression(tmp_path: Path) -> None:
    store = outbox(tmp_path, FakeClock(NOW))
    first = store.enqueue(notification(), "chat-1", "local", "same")
    second = store.enqueue(notification(), "chat-1", "local", "same")
    assert first == second
    assert store.counts()[OutboxState.QUEUED] == 1


def test_atomic_claim_and_successful_delivery(tmp_path: Path) -> None:
    store = outbox(tmp_path, FakeClock(NOW))
    outbox_id = store.enqueue(notification(), "chat-1", "local", "one")
    claimed = store.claim("worker-1", 10, timedelta(seconds=10))
    assert [record.outbox_id for record in claimed] == [outbox_id]
    assert store.claim("worker-2", 10, timedelta(seconds=10)) == ()
    store.mark_delivering(outbox_id, "worker-1")
    store.mark_delivered(outbox_id, "worker-1")
    assert store.get(outbox_id).state is OutboxState.DELIVERED


def test_lease_recovery(tmp_path: Path) -> None:
    clock = FakeClock(NOW)
    store = outbox(tmp_path, clock)
    outbox_id = store.enqueue(notification(), "chat-1", "local", "lease")
    store.claim("crashed", 1, timedelta(seconds=2))
    clock.advance(timedelta(seconds=3))
    recovered = store.claim("replacement", 1, timedelta(seconds=2))
    assert recovered[0].outbox_id == outbox_id
    assert recovered[0].lease_owner == "replacement"


def test_transient_retry_and_maximum_attempts(tmp_path: Path) -> None:
    clock = FakeClock(NOW)
    store = outbox(tmp_path, clock, max_attempts=2)
    outbox_id = store.enqueue(notification(), "chat-1", "local", "retry")
    store.claim("worker", 1, timedelta(seconds=5))
    assert (
        store.mark_failed(outbox_id, "worker", FailureClass.TRANSIENT, "network")
        is OutboxState.RETRY_WAIT
    )
    clock.advance(timedelta(seconds=2))
    store.claim("worker", 1, timedelta(seconds=5))
    assert (
        store.mark_failed(outbox_id, "worker", FailureClass.TRANSIENT, "network")
        is OutboxState.DEAD_LETTER
    )


def test_permanent_failure_and_replay(tmp_path: Path) -> None:
    store = outbox(tmp_path, FakeClock(NOW))
    outbox_id = store.enqueue(notification(), "chat-1", "local", "permanent")
    store.claim("worker", 1, timedelta(seconds=5))
    state = store.mark_failed(outbox_id, "worker", FailureClass.PERMANENT, "invalid chat")
    assert state is OutboxState.DEAD_LETTER
    store.replay_dead_letter(outbox_id)
    assert store.get(outbox_id).state is OutboxState.QUEUED


def test_expired_message_is_not_claimed(tmp_path: Path) -> None:
    clock = FakeClock(NOW)
    store = outbox(tmp_path, clock)
    outbox_id = store.enqueue(
        notification(NOW + timedelta(seconds=1)), "chat-1", "local", "expires"
    )
    clock.advance(timedelta(seconds=2))
    assert store.claim("worker", 1, timedelta(seconds=5)) == ()
    assert store.get(outbox_id).state is OutboxState.EXPIRED


def test_non_owner_cannot_transition(tmp_path: Path) -> None:
    store = outbox(tmp_path, FakeClock(NOW))
    outbox_id = store.enqueue(notification(), "chat-1", "local", "owner")
    store.claim("worker", 1, timedelta(seconds=5))
    with pytest.raises(PermissionError):
        store.mark_delivered(outbox_id, "attacker")
