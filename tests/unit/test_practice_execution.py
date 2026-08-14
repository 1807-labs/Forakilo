from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from foreightkillo.brokers.local import LocalBroker
from foreightkillo.domain import EventIdentity, InstrumentId, OrderProposal, Side
from foreightkillo.execution import Authorization, PracticeExecutionService
from foreightkillo.risk import RiskDecision, RiskOutcome

NOW = datetime(2026, 8, 8, tzinfo=UTC)


def _proposal(mode: str = "sandbox-manual") -> OrderProposal:
    identity = EventIdentity("proposal", NOW, NOW, NOW, "test", "corr", "signal", "1")
    return OrderProposal(
        identity,
        "signal",
        InstrumentId("local", "EUR_USD"),
        Side.BUY,
        Decimal("10"),
        Decimal("1.1"),
        Decimal("1.09"),
        NOW + timedelta(minutes=5),
        mode,
    )


def test_practice_submission_is_authorized_audited_and_idempotent() -> None:
    proposal = _proposal()
    decision = RiskDecision(RiskOutcome.APPROVED, (), proposal.proposal_hash)
    authorization = Authorization(
        "auth", proposal.proposal_hash, "operator", NOW + timedelta(minutes=2)
    )
    service = PracticeExecutionService(LocalBroker())
    first = service.submit(proposal, decision, authorization, NOW)
    second = service.submit(proposal, decision, authorization, NOW)
    assert first == second
    assert service.audit()[0].provider_order_id == first.order_id


def test_practice_service_rejects_live_mode_and_bad_risk() -> None:
    proposal = _proposal()
    authorization = Authorization(
        "auth", proposal.proposal_hash, "operator", NOW + timedelta(minutes=2)
    )
    rejected = RiskDecision(RiskOutcome.REJECTED, ("limit",), proposal.proposal_hash)
    service = PracticeExecutionService(LocalBroker())
    with pytest.raises(PermissionError):
        service.submit(proposal, rejected, authorization, NOW)
    live = replace(proposal, mode="live")
    approved = RiskDecision(RiskOutcome.APPROVED, (), live.proposal_hash)
    with pytest.raises(PermissionError):
        service.submit(live, approved, authorization, NOW)
