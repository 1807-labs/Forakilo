"""Future capability contracts shared by Noesis and third-party clients."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

SCHEMA_VERSION = "1.0.0"


@dataclass(frozen=True, slots=True)
class EventSubscriptionRequest:
    schema_version: str
    subscription_id: str
    event_categories: tuple[str, ...]
    visibility_ceiling: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class SignalQueryRequest:
    schema_version: str
    request_id: str
    signal_id: str
    evidence_requested: bool


@dataclass(frozen=True, slots=True)
class RiskExplanationQuery:
    schema_version: str
    request_id: str
    decision_id: str


@dataclass(frozen=True, slots=True)
class HealthQueryRequest:
    schema_version: str
    request_id: str
    components: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DeliveryAcknowledgement:
    schema_version: str
    message_id: str
    destination_id: str
    received_at: datetime
    outcome: str
