from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from foreightkillo.domain import EventIdentity, InstrumentId, OrderProposal, Side
from foreightkillo.execution import Authorization, PaperBroker
from foreightkillo.risk import RiskContext, RiskEngine, RiskLimits

NOW = datetime(2026, 7, 29, 18, tzinfo=UTC)


def identity() -> EventIdentity:
    return EventIdentity(
        event_id="proposal-1",
        event_time=NOW,
        known_time=NOW,
        recorded_time=NOW,
        provenance="test",
        correlation_id="corr-1",
        causation_id="signal-1",
        configuration_version="risk-v1",
    )


def proposal(mode: str = "paper") -> OrderProposal:
    return OrderProposal(
        identity=identity(),
        signal_id="signal-1",
        instrument_id=InstrumentId("fixture", "EUR_USD"),
        side=Side.BUY,
        quantity=Decimal("100"),
        reference_price=Decimal("1.1000"),
        stop_price=Decimal("1.0900"),
        expires_at=NOW + timedelta(minutes=5),
        mode=mode,
    )


def engine() -> RiskEngine:
    return RiskEngine(
        RiskLimits(
            max_notional=Decimal("1000"),
            max_open_risk=Decimal("50"),
            max_daily_loss=Decimal("100"),
            max_drawdown_fraction=Decimal("0.10"),
            max_spread_fraction=Decimal("0.01"),
            max_market_data_age=timedelta(seconds=30),
        )
    )


def context(**changes: object) -> RiskContext:
    values: dict[str, object] = {
        "now": NOW,
        "execution_enabled": True,
        "reconciled": True,
        "kill_switch_active": False,
        "market_data_time": NOW,
        "bid": Decimal("1.0999"),
        "ask": Decimal("1.1001"),
        "account_equity": Decimal("10000"),
        "daily_pnl": Decimal("0"),
        "drawdown_fraction": Decimal("0"),
        "current_open_risk": Decimal("0"),
    }
    values.update(changes)
    return RiskContext(**values)  # type: ignore[arg-type]


def test_missing_state_fails_closed() -> None:
    result = engine().evaluate(proposal(), context(account_equity=None))
    assert not result.approved
    assert "required_state_missing" in result.reasons


def test_kill_switch_rejects() -> None:
    result = engine().evaluate(proposal(), context(kill_switch_active=True))
    assert not result.approved
    assert result.reasons == ("kill_switch_active",)


def test_live_mode_has_no_authorized_path() -> None:
    candidate = proposal("live")
    result = engine().evaluate(candidate, context())
    assert not result.approved
    broker = PaperBroker()
    authorization = Authorization("auth-1", candidate.proposal_hash, "operator", NOW + timedelta(1))
    with pytest.raises(PermissionError):
        broker.submit(candidate, result, authorization, NOW, Decimal("1.1000"))


def test_submission_is_idempotent() -> None:
    candidate = proposal()
    result = engine().evaluate(candidate, context())
    assert result.approved
    authorization = Authorization(
        "auth-1", candidate.proposal_hash, "operator", NOW + timedelta(minutes=1)
    )
    broker = PaperBroker()
    first = broker.submit(candidate, result, authorization, NOW, Decimal("1.1000"))
    second = broker.submit(candidate, result, authorization, NOW, Decimal("1.1000"))
    assert first == second
