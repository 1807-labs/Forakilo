"""Immutable local registry with evidence-gated manual promotion."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class ValidationEvidence:
    dataset_fingerprint: str
    backtest_fingerprint: str
    trades: int
    total_return: Decimal
    maximum_drawdown: Decimal
    approved: bool
    reviewer: str


@dataclass(frozen=True, slots=True)
class ModelVersion:
    version_id: str
    strategy_id: str
    artifact_digest: str
    created_at: datetime
    status: str
    evidence: ValidationEvidence


@dataclass(frozen=True, slots=True)
class PromotionEvent:
    event_id: str
    version_id: str
    actor: str
    reason: str
    occurred_at: datetime


class ModelRegistry:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._path = path
        with self._connect() as connection:
            connection.executescript(
                """CREATE TABLE IF NOT EXISTS model_versions (
                version_id TEXT PRIMARY KEY, strategy_id TEXT NOT NULL,
                artifact_digest TEXT NOT NULL,
                created_at TEXT NOT NULL, status TEXT NOT NULL,
                dataset_fingerprint TEXT NOT NULL, backtest_fingerprint TEXT NOT NULL,
                trades INTEGER NOT NULL, total_return TEXT NOT NULL, maximum_drawdown TEXT NOT NULL,
                approved INTEGER NOT NULL, reviewer TEXT NOT NULL,
                UNIQUE(strategy_id, artifact_digest));
                CREATE TABLE IF NOT EXISTS model_promotions (
                event_id TEXT PRIMARY KEY, version_id TEXT NOT NULL, actor TEXT NOT NULL,
                reason TEXT NOT NULL, occurred_at TEXT NOT NULL);"""
            )

    def register(
        self, strategy_id: str, artifact_digest: str, evidence: ValidationEvidence
    ) -> ModelVersion:
        if not strategy_id.strip() or len(artifact_digest) < 32:
            raise ValueError("strategy identifier and strong artifact digest are required")
        if not evidence.dataset_fingerprint or not evidence.backtest_fingerprint:
            raise ValueError("dataset and backtest fingerprints are required")
        if evidence.trades < 0 or not Decimal("0") <= evidence.maximum_drawdown <= Decimal("1"):
            raise ValueError("validation metrics are invalid")
        version = ModelVersion(
            str(uuid4()),
            strategy_id,
            artifact_digest,
            datetime.now(UTC),
            "validated" if evidence.approved else "candidate",
            evidence,
        )
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO model_versions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    version.version_id,
                    version.strategy_id,
                    version.artifact_digest,
                    version.created_at.isoformat(),
                    version.status,
                    evidence.dataset_fingerprint,
                    evidence.backtest_fingerprint,
                    evidence.trades,
                    str(evidence.total_return),
                    str(evidence.maximum_drawdown),
                    int(evidence.approved),
                    evidence.reviewer,
                ),
            )
        return version

    def promote(self, version_id: str, actor: str, reason: str) -> ModelVersion:
        if not actor.strip() or len(reason.strip()) < 8:
            raise ValueError("human actor and promotion reason are required")
        version = self.get(version_id)
        if version is None:
            raise KeyError(version_id)
        if not version.evidence.approved:
            raise PermissionError("only independently approved validation evidence can be promoted")
        now = datetime.now(UTC)
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """UPDATE model_versions SET status = 'validated'
                WHERE strategy_id = ? AND status = 'active'""",
                (version.strategy_id,),
            )
            connection.execute(
                "UPDATE model_versions SET status = 'active' WHERE version_id = ?", (version_id,)
            )
            connection.execute(
                "INSERT INTO model_promotions VALUES (?, ?, ?, ?, ?)",
                (str(uuid4()), version_id, actor, reason.strip(), now.isoformat()),
            )
        promoted = self.get(version_id)
        if promoted is None:
            raise RuntimeError("promoted version disappeared")
        return promoted

    def get(self, version_id: str) -> ModelVersion | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM model_versions WHERE version_id = ?", (version_id,)
            ).fetchone()
        return self._decode(row) if row else None

    def list(self, strategy_id: str | None = None) -> tuple[ModelVersion, ...]:
        with self._connect() as connection:
            if strategy_id:
                rows = connection.execute(
                    "SELECT * FROM model_versions WHERE strategy_id = ? ORDER BY created_at DESC",
                    (strategy_id,),
                ).fetchall()
            else:
                rows = connection.execute(
                    "SELECT * FROM model_versions ORDER BY created_at DESC"
                ).fetchall()
        return tuple(self._decode(row) for row in rows)

    def promotions(self) -> tuple[PromotionEvent, ...]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM model_promotions ORDER BY occurred_at DESC"
            ).fetchall()
        return tuple(
            PromotionEvent(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                datetime.fromisoformat(str(row[4])),
            )
            for row in rows
        )

    @staticmethod
    def _decode(row: sqlite3.Row | tuple[object, ...]) -> ModelVersion:
        evidence = ValidationEvidence(
            str(row[5]),
            str(row[6]),
            int(str(row[7])),
            Decimal(str(row[8])),
            Decimal(str(row[9])),
            bool(row[10]),
            str(row[11]),
        )
        return ModelVersion(
            str(row[0]),
            str(row[1]),
            str(row[2]),
            datetime.fromisoformat(str(row[3])),
            str(row[4]),
            evidence,
        )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path)
