"""Authorized practice-account execution with audit and idempotency."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from forakilo.brokers.interface import Broker, BrokerOrder
from forakilo.domain import OrderProposal
from forakilo.risk import RiskDecision

from .paper import Authorization


@dataclass(frozen=True, slots=True)
class ExecutionAudit:
    event_type: str
    proposal_hash: str
    authorization_id: str
    provider_order_id: str | None
    occurred_at: datetime
    outcome: str


class PracticeExecutionService:
    """Routes only explicitly authorized sandbox-manual proposals."""

    def __init__(self, broker: Broker) -> None:
        self._broker = broker
        self._orders: dict[str, BrokerOrder] = {}
        self._used_authorizations: set[str] = set()
        self._audit: list[ExecutionAudit] = []

    def submit(
        self,
        proposal: OrderProposal,
        decision: RiskDecision,
        authorization: Authorization,
        now: datetime,
    ) -> BrokerOrder:
        if proposal.mode != "sandbox-manual":
            raise PermissionError("practice service accepts sandbox-manual mode only")
        if not decision.approved or decision.proposal_hash != proposal.proposal_hash:
            raise PermissionError("current approving risk decision required")
        if authorization.proposal_hash != proposal.proposal_hash:
            raise PermissionError("authorization does not match proposal")
        if now >= proposal.expires_at or now >= authorization.expires_at:
            raise PermissionError("authorization or proposal expired")
        existing = self._orders.get(proposal.proposal_hash)
        if existing:
            return existing
        if authorization.authorization_id in self._used_authorizations:
            raise PermissionError("authorization already used")
        try:
            order = self._broker.submit_order(
                proposal.instrument_id,
                proposal.side,
                proposal.quantity,
                proposal.reference_price,
                proposal.stop_price,
                proposal.mode,
            )
        except Exception as error:
            self._audit.append(
                ExecutionAudit(
                    "practice.order_rejected",
                    proposal.proposal_hash,
                    authorization.authorization_id,
                    None,
                    now,
                    type(error).__name__,
                )
            )
            raise
        self._used_authorizations.add(authorization.authorization_id)
        self._orders[proposal.proposal_hash] = order
        self._audit.append(
            ExecutionAudit(
                "practice.order_submitted",
                proposal.proposal_hash,
                authorization.authorization_id,
                order.order_id,
                now,
                order.status,
            )
        )
        return order

    def audit(self) -> tuple[ExecutionAudit, ...]:
        return tuple(self._audit)
