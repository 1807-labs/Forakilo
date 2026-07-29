from datetime import UTC, datetime, timedelta

import pytest

from forakilo.notifications.events import (
    EventEnvelope,
    EventSeverity,
    EventType,
    HealthEventPayload,
    RiskEventPayload,
    SignalEventPayload,
    Visibility,
)
from forakilo.notifications.projections import NotificationProjector

NOW = datetime(2026, 7, 29, tzinfo=UTC)


def signal_event(event_type: EventType = EventType.SIGNAL_ELIGIBLE) -> EventEnvelope:
    payload = SignalEventPayload(
        signal_id="signal-1",
        strategy_id="sandy_parity_v1",
        strategy_version="1",
        instrument="EUR_USD",
        asset_class="fx",
        timeframe="1h",
        direction="long",
        detected_time=NOW,
        confirmed_time=NOW + timedelta(hours=5),
        expires_at=NOW + timedelta(hours=6),
        status="eligible",
        evidence_summary="confirmed harmonic fixture",
        invalidation_state="active",
        risk_status="pending",
    )
    return EventEnvelope(
        event_id="event-1",
        event_type=event_type,
        schema_version="1.0.0",
        event_time=NOW,
        known_time=NOW + timedelta(hours=5),
        recorded_time=NOW + timedelta(hours=5),
        source="signal-engine",
        aggregate_type="signal",
        aggregate_id="signal-1",
        correlation_id="corr-1",
        causation_id=None,
        severity=EventSeverity.INFO,
        visibility=Visibility.MEMBER,
        payload=payload,
        payload_schema_version="1.0.0",
    )


def test_event_serialization_is_versioned() -> None:
    serialized = signal_event().to_dict()
    assert serialized["event_type"] == "signal.eligible"
    assert serialized["payload_kind"] == "signal"
    assert serialized["schema_version"] == "1.0.0"


def test_invalid_payload_discriminator_is_rejected() -> None:
    event = signal_event()
    with pytest.raises(TypeError):
        EventEnvelope(
            event_id=event.event_id,
            event_type=EventType.RISK_APPROVED,
            schema_version=event.schema_version,
            event_time=event.event_time,
            known_time=event.known_time,
            recorded_time=event.recorded_time,
            source=event.source,
            aggregate_type=event.aggregate_type,
            aggregate_id=event.aggregate_id,
            correlation_id=event.correlation_id,
            causation_id=None,
            severity=event.severity,
            visibility=event.visibility,
            payload=event.payload,
            payload_schema_version="1.0.0",
        )


def test_projection_preserves_expiry_status_and_paper_label() -> None:
    notification = NotificationProjector().project(signal_event())
    assert notification.expires_at is not None
    assert notification.paper_only
    assert "status eligible" in notification.body
    assert ("risk_status", "pending") in notification.fields


def test_risk_rejection_reasons_are_not_hidden() -> None:
    event = EventEnvelope(
        event_id="risk-event",
        event_type=EventType.RISK_REJECTED,
        schema_version="1.0.0",
        event_time=NOW,
        known_time=NOW,
        recorded_time=NOW,
        source="risk",
        aggregate_type="risk_decision",
        aggregate_id="risk-1",
        correlation_id="corr",
        causation_id="proposal-1",
        severity=EventSeverity.WARNING,
        visibility=Visibility.OPERATOR,
        payload=RiskEventPayload("risk-1", "rejected", ("spread_too_wide",), "account"),
        payload_schema_version="1.0.0",
    )
    notification = NotificationProjector().project(event)
    assert "spread_too_wide" in notification.body


def test_health_event_requires_health_payload() -> None:
    with pytest.raises(TypeError):
        EventEnvelope(
            "bad",
            EventType.SYSTEM_HALTED,
            "1.0.0",
            NOW,
            NOW,
            NOW,
            "system",
            "system",
            "system",
            "corr",
            None,
            EventSeverity.CRITICAL,
            Visibility.OPERATOR,
            RiskEventPayload("r", "rejected", (), "system"),
            "1.0.0",
        )
    assert HealthEventPayload("worker", "healthy", "ok").status == "healthy"
