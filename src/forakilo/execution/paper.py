"""Idempotent, one-time-authorized paper execution with no live credential path."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from forakilo.domain import OrderProposal
from forakilo.risk import RiskDecision


class OrderState(StrEnum):
    FILLED = "filled"


@dataclass(frozen=True, slots=True)
class Authorization:
    authorization_id: str
    proposal_hash: str
    approved_by: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class PaperOrder:
    order_id: str
    proposal_hash: str
    fill_price: Decimal
    quantity: Decimal
    state: OrderState = OrderState.FILLED


class PaperBroker:
    """Local simulator. It cannot hold credentials or route to a provider."""

    def __init__(self) -> None:
        self._orders: dict[str, PaperOrder] = {}
        self._used_authorizations: set[str] = set()

    def submit(
        self,
        proposal: OrderProposal,
        decision: RiskDecision,
        authorization: Authorization,
        now: datetime,
        fill_price: Decimal,
    ) -> PaperOrder:
        if proposal.mode != "paper":
            raise PermissionError("paper broker accepts paper mode only")
        if not decision.approved or decision.proposal_hash != proposal.proposal_hash:
            raise PermissionError("current approving risk decision required")
        if authorization.proposal_hash != proposal.proposal_hash:
            raise PermissionError("authorization does not match proposal")
        if now >= authorization.expires_at or now >= proposal.expires_at:
            raise PermissionError("authorization or proposal expired")
        existing = self._orders.get(proposal.proposal_hash)
        if existing is not None:
            return existing
        if authorization.authorization_id in self._used_authorizations:
            raise PermissionError("authorization already used")
        if fill_price <= 0:
            raise ValueError("fill price must be positive")
        order = PaperOrder(
            order_id=f"paper-{proposal.proposal_hash[:24]}",
            proposal_hash=proposal.proposal_hash,
            fill_price=fill_price,
            quantity=proposal.quantity,
        )
        self._used_authorizations.add(authorization.authorization_id)
        self._orders[proposal.proposal_hash] = order
        return order
