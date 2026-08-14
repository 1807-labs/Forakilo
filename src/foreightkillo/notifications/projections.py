"""Convert internal events to redacted provider-neutral notifications."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from hashlib import sha256

from .events import (
    EventEnvelope,
    PaperEventPayload,
    RiskEventPayload,
    SignalEventPayload,
    Visibility,
)


class NotificationPriority(StrEnum):
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class Notification:
    message_id: str
    source_event_id: str
    category: str
    priority: NotificationPriority
    title: str
    body: str
    fields: tuple[tuple[str, str], ...]
    generated_at: datetime
    expires_at: datetime | None
    audience: Visibility
    sensitivity: str
    dashboard_link: str | None
    deduplication_key: str
    paper_only: bool


@dataclass(frozen=True, slots=True)
class SignalNotification(Notification):
    pass


@dataclass(frozen=True, slots=True)
class RiskNotification(Notification):
    pass


@dataclass(frozen=True, slots=True)
class PaperExecutionNotification(Notification):
    pass


@dataclass(frozen=True, slots=True)
class HealthNotification(Notification):
    pass


@dataclass(frozen=True, slots=True)
class DailySummaryNotification(Notification):
    pass


class NotificationProjector:
    def project(self, event: EventEnvelope, dashboard_link: str | None = None) -> Notification:
        payload = event.payload
        title = event.event_type.value.replace(".", " · ").replace("_", " ").title()
        fields: tuple[tuple[str, str], ...]
        expiry: datetime | None = None
        paper_only = False
        if isinstance(payload, SignalEventPayload):
            body = (
                f"{payload.instrument} {payload.direction}; status {payload.status}. "
                f"Strategy {payload.strategy_id} {payload.strategy_version}. "
                f"Expires {payload.expires_at.isoformat()}."
            )
            fields = (
                ("instrument", payload.instrument),
                ("timeframe", payload.timeframe),
                ("risk_status", payload.risk_status),
                ("evidence", payload.evidence_summary),
                ("invalidation", payload.invalidation_state),
            )
            expiry = payload.expires_at
            paper_only = payload.paper_only
        elif isinstance(payload, RiskEventPayload):
            body = f"Risk status {payload.status}. Reasons: {', '.join(payload.reasons) or 'none'}."
            fields = (("scope", payload.scope),)
        elif isinstance(payload, PaperEventPayload):
            body = f"Paper-only {payload.instrument}: {payload.summary}"
            fields = (("status", payload.status),)
            paper_only = True
        else:
            body = f"{payload.component}: {payload.summary}"
            fields = (("status", payload.status),)
        message_id = sha256(f"notification:{event.event_id}".encode()).hexdigest()
        priority = {
            "info": NotificationPriority.NORMAL,
            "warning": NotificationPriority.HIGH,
            "critical": NotificationPriority.CRITICAL,
        }[event.severity.value]
        notification_type: type[Notification]
        if isinstance(payload, SignalEventPayload):
            notification_type = SignalNotification
        elif isinstance(payload, RiskEventPayload):
            notification_type = RiskNotification
        elif isinstance(payload, PaperEventPayload):
            notification_type = PaperExecutionNotification
        else:
            notification_type = HealthNotification
        return notification_type(
            message_id=message_id,
            source_event_id=event.event_id,
            category=event.event_type.category,
            priority=priority,
            title=title,
            body=body,
            fields=fields,
            generated_at=event.recorded_time,
            expires_at=expiry,
            audience=event.visibility,
            sensitivity="installation",
            dashboard_link=dashboard_link,
            deduplication_key=message_id,
            paper_only=paper_only,
        )
