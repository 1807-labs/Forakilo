"""Fail-closed runtime controls backed by an installation-local SQLite journal."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class OperationalStatus:
    kill_switch_active: bool
    execution_permitted: bool
    mode: str
    updated_at: datetime
    updated_by: str
    reason: str


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_id: str
    event_type: str
    actor: str
    reason: str
    occurred_at: datetime


class OperationalControls:
    """Stores safety state durably; unknown or corrupt state never permits execution."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._path = path
        with self._connect() as connection:
            connection.executescript(
                """CREATE TABLE IF NOT EXISTS operational_state (
                singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                kill_switch_active INTEGER NOT NULL CHECK (kill_switch_active IN (0, 1)),
                updated_at TEXT NOT NULL, updated_by TEXT NOT NULL, reason TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS operational_audit (
                event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, actor TEXT NOT NULL,
                reason TEXT NOT NULL, occurred_at TEXT NOT NULL);"""
            )
            now = datetime.now(UTC).isoformat()
            connection.execute(
                """INSERT OR IGNORE INTO operational_state
                VALUES (1, 1, ?, 'system', 'safe default on first startup')""",
                (now,),
            )

    def status(self) -> OperationalStatus:
        with self._connect() as connection:
            row = connection.execute(
                """SELECT kill_switch_active, updated_at, updated_by, reason
                FROM operational_state WHERE singleton = 1"""
            ).fetchone()
        if row is None:
            now = datetime.now(UTC)
            return OperationalStatus(True, False, "paper", now, "system", "state unavailable")
        active = bool(row[0])
        return OperationalStatus(
            active,
            not active,
            "paper",
            datetime.fromisoformat(str(row[1])),
            str(row[2]),
            str(row[3]),
        )

    def set_kill_switch(self, active: bool, actor: str, reason: str) -> OperationalStatus:
        if not actor.strip():
            raise ValueError("actor is required")
        if len(reason.strip()) < 8 or len(reason) > 500:
            raise ValueError("reason must contain between 8 and 500 characters")
        now = datetime.now(UTC)
        event_type = (
            "operations.kill_switch_activated" if active else "operations.kill_switch_cleared"
        )
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """UPDATE operational_state SET kill_switch_active = ?, updated_at = ?,
                updated_by = ?, reason = ? WHERE singleton = 1""",
                (int(active), now.isoformat(), actor, reason.strip()),
            )
            connection.execute(
                "INSERT INTO operational_audit VALUES (?, ?, ?, ?, ?)",
                (str(uuid4()), event_type, actor, reason.strip(), now.isoformat()),
            )
        return self.status()

    def audit(self, limit: int = 100) -> tuple[AuditEvent, ...]:
        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT event_id, event_type, actor, reason, occurred_at
                FROM operational_audit ORDER BY occurred_at DESC LIMIT ?""",
                (limit,),
            ).fetchall()
        return tuple(
            AuditEvent(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                datetime.fromisoformat(str(row[4])),
            )
            for row in rows
        )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path)
