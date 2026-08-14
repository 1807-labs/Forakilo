"""Fail-closed risk gates. AI output is intentionally absent from this API."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from typing import cast

from foreightkillo.domain import OrderProposal


class RiskOutcome(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class RiskLimits:
    max_notional: Decimal
    max_open_risk: Decimal
    max_daily_loss: Decimal
    max_drawdown_fraction: Decimal
    max_spread_fraction: Decimal
    max_market_data_age: timedelta
    allowed_modes: frozenset[str] = frozenset({"paper", "sandbox-manual"})


@dataclass(frozen=True, slots=True)
class RiskContext:
    now: datetime
    execution_enabled: bool
    reconciled: bool
    kill_switch_active: bool
    market_data_time: datetime | None
    bid: Decimal | None
    ask: Decimal | None
    account_equity: Decimal | None
    daily_pnl: Decimal | None
    drawdown_fraction: Decimal | None
    current_open_risk: Decimal | None


@dataclass(frozen=True, slots=True)
class RiskDecision:
    outcome: RiskOutcome
    reasons: tuple[str, ...]
    proposal_hash: str

    @property
    def approved(self) -> bool:
        return self.outcome is RiskOutcome.APPROVED


class RiskEngine:
    def __init__(self, limits: RiskLimits) -> None:
        self._limits = limits

    def evaluate(self, proposal: OrderProposal, context: RiskContext) -> RiskDecision:
        reasons: list[str] = []
        if proposal.mode not in self._limits.allowed_modes:
            reasons.append("mode_not_allowed")
        if not context.execution_enabled:
            reasons.append("execution_disabled")
        if not context.reconciled:
            reasons.append("reconciliation_unhealthy")
        if context.kill_switch_active:
            reasons.append("kill_switch_active")
        if context.now >= proposal.expires_at:
            reasons.append("proposal_expired")

        required = (
            context.market_data_time,
            context.bid,
            context.ask,
            context.account_equity,
            context.daily_pnl,
            context.drawdown_fraction,
            context.current_open_risk,
        )
        if any(value is None for value in required):
            reasons.append("required_state_missing")
            return self._decision(proposal, reasons)

        market_data_time = cast(datetime, context.market_data_time)
        bid = cast(Decimal, context.bid)
        ask = cast(Decimal, context.ask)
        account_equity = cast(Decimal, context.account_equity)
        daily_pnl = cast(Decimal, context.daily_pnl)
        drawdown_fraction = cast(Decimal, context.drawdown_fraction)
        current_open_risk = cast(Decimal, context.current_open_risk)

        if context.now - market_data_time > self._limits.max_market_data_age:
            reasons.append("market_data_stale")
        midpoint = (ask + bid) / 2
        spread_fraction = (ask - bid) / midpoint if midpoint > 0 else Decimal("Infinity")
        if spread_fraction > self._limits.max_spread_fraction:
            reasons.append("spread_too_wide")
        notional = proposal.quantity * proposal.reference_price
        proposed_risk = proposal.quantity * abs(proposal.reference_price - proposal.stop_price)
        if notional > self._limits.max_notional:
            reasons.append("notional_limit")
        if current_open_risk + proposed_risk > self._limits.max_open_risk:
            reasons.append("open_risk_limit")
        if daily_pnl <= -self._limits.max_daily_loss:
            reasons.append("daily_loss_limit")
        if drawdown_fraction >= self._limits.max_drawdown_fraction:
            reasons.append("drawdown_limit")
        if account_equity <= 0:
            reasons.append("invalid_equity")
        return self._decision(proposal, reasons)

    @staticmethod
    def _decision(proposal: OrderProposal, reasons: list[str]) -> RiskDecision:
        return RiskDecision(
            outcome=RiskOutcome.REJECTED if reasons else RiskOutcome.APPROVED,
            reasons=tuple(sorted(set(reasons))),
            proposal_hash=proposal.proposal_hash,
        )
