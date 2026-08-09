"""Transactional SQLite notification outbox with bounded retry and leases."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from .projections import Notification


class Clock(Protocol):
    def now(self) -> datetime: ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class OutboxState(StrEnum):
    QUEUED = "queued"
    CLAIMED = "claimed"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    RETRY_WAIT = "retry_wait"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"
    SUPPRESSED = "suppressed"
    EXPIRED = "expired"


class FailureClass(StrEnum):
    TRANSIENT = "transient"
    PERMANENT = "permanent"
    RATE_LIMIT = "rate_limit"
    AUTHORIZATION = "authorization"


@dataclass(frozen=True, slots=True)
class OutboxRecord:
    outbox_id: str
    message_id: str
    destination_id: str
    provider: str
    state: OutboxState
    attempt_count: int
    next_attempt_at: datetime
    created_at: datetime
    updated_at: datetime
    delivered_at: datetime | None
    failure_classification: FailureClass | None
    redacted_failure_detail: str | None
    idempotency_key: str
    lease_owner: str | None
    lease_expires_at: datetime | None
    expires_at: datetime | None
    notification_json: str


def _iso(value: datetime | None) -> str | None:
    return value.astimezone(UTC).isoformat() if value else None


def _dt(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


class SQLiteOutbox:
    def __init__(
        self,
        path: Path,
        clock: Clock | None = None,
        max_attempts: int = 5,
        base_backoff: timedelta = timedelta(seconds=5),
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        self._path = path
        self._clock = clock or SystemClock()
        self._max_attempts = max_attempts
        self._base_backoff = base_backoff
        path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path, isolation_level=None, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS notification_outbox (
                    outbox_id TEXT PRIMARY KEY,
                    message_id TEXT NOT NULL,
                    destination_id TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    state TEXT NOT NULL,
                    attempt_count INTEGER NOT NULL,
                    next_attempt_at TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    delivered_at TEXT,
                    failure_classification TEXT,
                    redacted_failure_detail TEXT,
                    idempotency_key TEXT NOT NULL UNIQUE,
                    lease_owner TEXT,
                    lease_expires_at TEXT,
                    expires_at TEXT,
                    notification_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_outbox_claim
                    ON notification_outbox(state, next_attempt_at);
                CREATE TABLE IF NOT EXISTS notification_delivery_audit (
                    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    outbox_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    detail TEXT
                );
                """
            )

    def enqueue(
        self,
        notification: Notification,
        destination_id: str,
        provider: str,
        idempotency_key: str,
    ) -> str:
        now = self._clock.now()
        outbox_id = str(uuid4())
        serialized = json.dumps(asdict(notification), default=str, sort_keys=True)
        with self._connect() as connection:
            try:
                connection.execute(
                    """INSERT INTO notification_outbox VALUES
                    (?, ?, ?, ?, ?, 0, ?, ?, ?, NULL, NULL, NULL, ?, NULL, NULL, ?, ?)""",
                    (
                        outbox_id,
                        notification.message_id,
                        destination_id,
                        provider,
                        OutboxState.QUEUED,
                        _iso(now),
                        _iso(now),
                        _iso(now),
                        idempotency_key,
                        _iso(notification.expires_at),
                        serialized,
                    ),
                )
                self._audit(connection, outbox_id, OutboxState.QUEUED, "enqueued")
            except sqlite3.IntegrityError:
                row = connection.execute(
                    "SELECT outbox_id FROM notification_outbox WHERE idempotency_key = ?",
                    (idempotency_key,),
                ).fetchone()
                if row is None:
                    raise
                return str(row["outbox_id"])
        return outbox_id

    def claim(self, worker: str, limit: int, lease: timedelta) -> tuple[OutboxRecord, ...]:
        now = self._clock.now()
        lease_expiry = now + lease
        claimed: list[OutboxRecord] = []
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            self._expire_due(connection, now)
            rows = connection.execute(
                """SELECT * FROM notification_outbox
                   WHERE (
                     state IN (?, ?) AND next_attempt_at <= ?
                   ) OR (
                     state IN (?, ?) AND lease_expires_at < ?
                   )
                   ORDER BY next_attempt_at, created_at LIMIT ?""",
                (
                    OutboxState.QUEUED,
                    OutboxState.RETRY_WAIT,
                    _iso(now),
                    OutboxState.CLAIMED,
                    OutboxState.DELIVERING,
                    _iso(now),
                    limit,
                ),
            ).fetchall()
            for row in rows:
                connection.execute(
                    """UPDATE notification_outbox SET state = ?, lease_owner = ?,
                       lease_expires_at = ?, updated_at = ? WHERE outbox_id = ?""",
                    (
                        OutboxState.CLAIMED,
                        worker,
                        _iso(lease_expiry),
                        _iso(now),
                        row["outbox_id"],
                    ),
                )
                self._audit(connection, str(row["outbox_id"]), OutboxState.CLAIMED, worker)
            connection.execute("COMMIT")
            for row in rows:
                updated = connection.execute(
                    "SELECT * FROM notification_outbox WHERE outbox_id = ?",
                    (row["outbox_id"],),
                ).fetchone()
                claimed.append(self._record(updated))
        return tuple(claimed)

    def mark_delivering(self, outbox_id: str, worker: str) -> None:
        self._transition_owned(outbox_id, worker, OutboxState.DELIVERING)

    def mark_delivered(self, outbox_id: str, worker: str) -> None:
        now = self._clock.now()
        with self._connect() as connection:
            changed = connection.execute(
                """UPDATE notification_outbox SET state = ?, delivered_at = ?,
                   updated_at = ?, lease_owner = NULL, lease_expires_at = NULL
                   WHERE outbox_id = ? AND lease_owner = ?""",
                (OutboxState.DELIVERED, _iso(now), _iso(now), outbox_id, worker),
            ).rowcount
            if changed != 1:
                raise PermissionError("worker does not own outbox lease")
            self._audit(connection, outbox_id, OutboxState.DELIVERED, "delivered")

    def mark_failed(
        self,
        outbox_id: str,
        worker: str,
        failure: FailureClass,
        redacted_detail: str,
    ) -> OutboxState:
        if len(redacted_detail) > 200:
            redacted_detail = redacted_detail[:200]
        now = self._clock.now()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT attempt_count FROM notification_outbox "
                "WHERE outbox_id = ? AND lease_owner = ?",
                (outbox_id, worker),
            ).fetchone()
            if row is None:
                raise PermissionError("worker does not own outbox lease")
            attempt = int(row["attempt_count"]) + 1
            permanent = failure in {FailureClass.PERMANENT, FailureClass.AUTHORIZATION}
            state = (
                OutboxState.DEAD_LETTER
                if permanent or attempt >= self._max_attempts
                else OutboxState.RETRY_WAIT
            )
            delay = self._base_backoff * (2 ** (attempt - 1))
            connection.execute(
                """UPDATE notification_outbox SET state = ?, attempt_count = ?,
                   next_attempt_at = ?, updated_at = ?, failure_classification = ?,
                   redacted_failure_detail = ?, lease_owner = NULL,
                   lease_expires_at = NULL WHERE outbox_id = ?""",
                (
                    state,
                    attempt,
                    _iso(now + delay),
                    _iso(now),
                    failure,
                    redacted_detail,
                    outbox_id,
                ),
            )
            self._audit(connection, outbox_id, state, failure)
            return state

    def replay_dead_letter(self, outbox_id: str) -> None:
        now = self._clock.now()
        with self._connect() as connection:
            changed = connection.execute(
                """UPDATE notification_outbox SET state = ?, next_attempt_at = ?,
                   updated_at = ?, failure_classification = NULL,
                   redacted_failure_detail = NULL WHERE outbox_id = ? AND state = ?""",
                (
                    OutboxState.QUEUED,
                    _iso(now),
                    _iso(now),
                    outbox_id,
                    OutboxState.DEAD_LETTER,
                ),
            ).rowcount
            if changed != 1:
                raise ValueError("record is not dead-lettered")
            self._audit(connection, outbox_id, OutboxState.QUEUED, "manual replay")

    def get(self, outbox_id: str) -> OutboxRecord:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM notification_outbox WHERE outbox_id = ?", (outbox_id,)
            ).fetchone()
        if row is None:
            raise KeyError(outbox_id)
        return self._record(row)

    def counts(self) -> dict[OutboxState, int]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT state, COUNT(*) count FROM notification_outbox GROUP BY state"
            ).fetchall()
        return {OutboxState(row["state"]): int(row["count"]) for row in rows}

    def _transition_owned(self, outbox_id: str, worker: str, state: OutboxState) -> None:
        now = self._clock.now()
        with self._connect() as connection:
            changed = connection.execute(
                """UPDATE notification_outbox SET state = ?, updated_at = ?
                   WHERE outbox_id = ? AND lease_owner = ?""",
                (state, _iso(now), outbox_id, worker),
            ).rowcount
            if changed != 1:
                raise PermissionError("worker does not own outbox lease")
            self._audit(connection, outbox_id, state, worker)

    @staticmethod
    def _expire_due(connection: sqlite3.Connection, now: datetime) -> None:
        connection.execute(
            """UPDATE notification_outbox SET state = ?, updated_at = ?,
               lease_owner = NULL, lease_expires_at = NULL
               WHERE expires_at IS NOT NULL AND expires_at <= ?
               AND state NOT IN (?, ?, ?, ?)""",
            (
                OutboxState.EXPIRED,
                _iso(now),
                _iso(now),
                OutboxState.DELIVERED,
                OutboxState.DEAD_LETTER,
                OutboxState.SUPPRESSED,
                OutboxState.EXPIRED,
            ),
        )

    def _audit(
        self, connection: sqlite3.Connection, outbox_id: str, state: OutboxState, detail: object
    ) -> None:
        connection.execute(
            """INSERT INTO notification_delivery_audit(outbox_id, state, occurred_at, detail)
               VALUES (?, ?, ?, ?)""",
            (outbox_id, state, _iso(self._clock.now()), str(detail)[:200]),
        )

    @staticmethod
    def _record(row: sqlite3.Row) -> OutboxRecord:
        return OutboxRecord(
            outbox_id=str(row["outbox_id"]),
            message_id=str(row["message_id"]),
            destination_id=str(row["destination_id"]),
            provider=str(row["provider"]),
            state=OutboxState(row["state"]),
            attempt_count=int(row["attempt_count"]),
            next_attempt_at=_dt(row["next_attempt_at"]) or datetime.min.replace(tzinfo=UTC),
            created_at=_dt(row["created_at"]) or datetime.min.replace(tzinfo=UTC),
            updated_at=_dt(row["updated_at"]) or datetime.min.replace(tzinfo=UTC),
            delivered_at=_dt(row["delivered_at"]),
            failure_classification=(
                FailureClass(row["failure_classification"])
                if row["failure_classification"]
                else None
            ),
            redacted_failure_detail=row["redacted_failure_detail"],
            idempotency_key=str(row["idempotency_key"]),
            lease_owner=row["lease_owner"],
            lease_expires_at=_dt(row["lease_expires_at"]),
            expires_at=_dt(row["expires_at"]),
            notification_json=str(row["notification_json"]),
        )
