"""Versioned internal events; provider message types never enter this module."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, TypeAlias


class EventType(StrEnum):
    SIGNAL_CANDIDATE_DETECTED = "signal.candidate_detected"
    SIGNAL_ELIGIBLE = "signal.eligible"
    SIGNAL_REJECTED = "signal.rejected"
    SIGNAL_EXPIRED = "signal.expired"
    SIGNAL_INVALIDATED = "signal.invalidated"
    RISK_APPROVED = "risk.approved"
    RISK_REJECTED = "risk.rejected"
    RISK_LIMIT_WARNING = "risk.limit_warning"
    RISK_HALT_ACTIVATED = "risk.halt_activated"
    RISK_HALT_CLEARED = "risk.halt_cleared"
    PAPER_PROPOSAL_CREATED = "paper.proposal_created"
    PAPER_PROPOSAL_EXPIRED = "paper.proposal_expired"
    PAPER_ORDER_SUBMITTED = "paper.order_submitted"
    PAPER_ORDER_REJECTED = "paper.order_rejected"
    PAPER_ORDER_ACCEPTED = "paper.order_accepted"
    PAPER_ORDER_PARTIALLY_FILLED = "paper.order_partially_filled"
    PAPER_ORDER_FILLED = "paper.order_filled"
    PAPER_ORDER_CANCELLED = "paper.order_cancelled"
    PAPER_POSITION_OPENED = "paper.position_opened"
    PAPER_POSITION_CLOSED = "paper.position_closed"
    PAPER_RECONCILIATION_FAILED = "paper.reconciliation_failed"
    DATA_FEED_STALE = "data.feed_stale"
    DATA_GAP_DETECTED = "data.gap_detected"
    DATA_FEED_RECOVERED = "data.feed_recovered"
    MODEL_DRIFT_WARNING = "model.drift_warning"
    MODEL_UNAVAILABLE = "model.unavailable"
    MODEL_RECOVERED = "model.recovered"
    SYSTEM_STARTED = "system.started"
    SYSTEM_DEGRADED = "system.degraded"
    SYSTEM_HALTED = "system.halted"
    SYSTEM_RECOVERED = "system.recovered"

    @property
    def category(self) -> str:
        return self.value.split(".", 1)[0]


class EventSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Visibility(StrEnum):
    PUBLIC_DELAYED = "public_delayed"
    MEMBER = "member"
    OPERATOR = "operator"
    ADMINISTRATOR = "administrator"


def _aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class SignalEventPayload:
    signal_id: str
    strategy_id: str
    strategy_version: str
    instrument: str
    asset_class: str
    timeframe: str
    direction: str
    detected_time: datetime
    confirmed_time: datetime
    expires_at: datetime
    status: str
    evidence_summary: str
    invalidation_state: str
    risk_status: str
    paper_only: bool = True
    entry_zone: str | None = None
    invalidation_level: str | None = None
    model_score: str | None = None

    def __post_init__(self) -> None:
        for name in ("detected_time", "confirmed_time", "expires_at"):
            _aware(getattr(self, name), name)
        if self.confirmed_time < self.detected_time:
            raise ValueError("confirmed_time cannot precede detected_time")
        if self.expires_at <= self.confirmed_time:
            raise ValueError("signal expiry must follow confirmation")


@dataclass(frozen=True, slots=True)
class RiskEventPayload:
    decision_id: str
    status: str
    reasons: tuple[str, ...]
    scope: str


@dataclass(frozen=True, slots=True)
class PaperEventPayload:
    paper_id: str
    status: str
    instrument: str
    summary: str


@dataclass(frozen=True, slots=True)
class HealthEventPayload:
    component: str
    status: str
    summary: str


EventPayload: TypeAlias = (
    SignalEventPayload | RiskEventPayload | PaperEventPayload | HealthEventPayload
)


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    event_id: str
    event_type: EventType
    schema_version: str
    event_time: datetime
    known_time: datetime
    recorded_time: datetime
    source: str
    aggregate_type: str
    aggregate_id: str
    correlation_id: str
    causation_id: str | None
    severity: EventSeverity
    visibility: Visibility
    payload: EventPayload
    payload_schema_version: str

    def __post_init__(self) -> None:
        for name in ("event_time", "known_time", "recorded_time"):
            _aware(getattr(self, name), name)
        if not self.schema_version.startswith("1.") or not self.payload_schema_version:
            raise ValueError("supported schema and payload schema versions are required")
        if self.known_time < self.event_time or self.recorded_time < self.known_time:
            raise ValueError("event temporal ordering is invalid")
        expected = {
            "signal": SignalEventPayload,
            "risk": RiskEventPayload,
            "paper": PaperEventPayload,
            "data": HealthEventPayload,
            "model": HealthEventPayload,
            "system": HealthEventPayload,
        }[self.event_type.category]
        if type(self.payload) is not expected:
            raise TypeError(f"{self.event_type} requires {expected.__name__}")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key in ("event_time", "known_time", "recorded_time"):
            data[key] = getattr(self, key).astimezone(UTC).isoformat()
        payload = data["payload"]
        if self.event_type.category == "signal":
            signal_payload = self.payload
            if not isinstance(signal_payload, SignalEventPayload):
                raise TypeError("signal event payload validation failed")
            for key in ("detected_time", "confirmed_time", "expires_at"):
                payload[key] = getattr(signal_payload, key).astimezone(UTC).isoformat()
        data["event_type"] = self.event_type.value
        data["severity"] = self.severity.value
        data["visibility"] = self.visibility.value
        data["payload_kind"] = self.event_type.category
        return data
