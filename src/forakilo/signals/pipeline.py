"""Explainable strategy qualification, ranking, and paper proposal preparation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import ROUND_DOWN, Decimal
from uuid import uuid4

from forakilo.domain import EventIdentity, Instrument, OrderProposal, Quote, Side, Signal
from forakilo.intelligence.market import MarketEvidence, Opportunity, OpportunityRanker


@dataclass(frozen=True, slots=True)
class StrategyPolicy:
    strategy_id: str = "foreight-market-structure"
    strategy_version: str = "1.0.0"
    model_version: str = "deterministic-1.0.0"
    minimum_confidence: Decimal = Decimal("0.58")
    minimum_reward_to_risk: Decimal = Decimal("1.5")
    signal_lifetime: timedelta = timedelta(hours=4)
    stop_volatility_multiple: Decimal = Decimal("1.5")
    target_reward_multiple: Decimal = Decimal("2")


@dataclass(frozen=True, slots=True)
class RankedSignal:
    signal: Signal
    expected_value: Decimal
    rank: int
    explanation: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PaperProposalView:
    proposal: OrderProposal
    account_id: str
    provider: str
    order_type: str
    targets: tuple[Decimal, ...]
    estimated_maximum_loss: Decimal
    account_risk_fraction: Decimal
    expected_value: Decimal
    transaction_cost_estimate: Decimal
    strategy_version: str
    model_version: str
    authorization_required: bool = True


class SignalPipeline:
    def __init__(self, policy: StrategyPolicy | None = None) -> None:
        self.policy = policy or StrategyPolicy()

    def create(
        self,
        instrument: Instrument,
        quote: Quote,
        evidence: MarketEvidence,
        timeframe: str,
        now: datetime,
    ) -> Signal:
        midpoint = (quote.bid + quote.ask) / Decimal("2")
        stop_distance = max(
            instrument.price_increment,
            evidence.volatility * self.policy.stop_volatility_multiple,
        )
        stop = (
            midpoint - stop_distance if evidence.direction is Side.BUY else midpoint + stop_distance
        )
        target = (
            midpoint + stop_distance * self.policy.target_reward_multiple
            if evidence.direction is Side.BUY
            else midpoint - stop_distance * self.policy.target_reward_multiple
        )
        spread = quote.ask - quote.bid
        reward_to_risk = self.policy.target_reward_multiple
        probability = evidence.confidence
        expected_value = probability * reward_to_risk - (Decimal("1") - probability)
        expected_value -= spread / midpoint
        eligible = (
            probability >= self.policy.minimum_confidence
            and reward_to_risk >= self.policy.minimum_reward_to_risk
        )
        event_id = f"signal-{uuid4()}"
        identity = EventIdentity(
            event_id,
            now,
            now,
            now,
            quote.provenance.source,
            event_id,
            quote.identity.event_id,
            self.policy.strategy_version,
        )
        reasons = (*evidence.reasons, f"expected value {expected_value:.4f}")
        return Signal(
            identity,
            self.policy.strategy_id,
            self.policy.strategy_version,
            instrument.instrument_id,
            instrument.asset_class,
            timeframe,
            evidence.direction,
            now,
            now,
            now + self.policy.signal_lifetime,
            f"{quote.bid}-{quote.ask}",
            stop,
            stop,
            (target,),
            reward_to_risk,
            spread,
            evidence.regime,
            probability,
            expected_value,
            "eligible" if eligible else "rejected",
            None if eligible else "minimum evidence threshold not met",
            reasons,
            evidence.reasons,
            f"candidate-{event_id}",
        )

    def rank(
        self,
        signals: tuple[Signal, ...],
        portfolio_penalties: dict[str, Decimal] | None = None,
    ) -> tuple[RankedSignal, ...]:
        penalties = portfolio_penalties or {}
        opportunities = tuple(
            Opportunity(
                signal.identity.event_id,
                signal.ranking_score or Decimal("-1"),
                signal.reward_to_risk or Decimal("0"),
                signal.estimated_transaction_costs,
                Decimal("1"),
                Decimal("1") if signal.market_regime == "trending" else Decimal("0.7"),
                penalties.get(signal.instrument_id.symbol, Decimal("0")),
                Decimal("1") - (signal.confidence or Decimal("0")),
            )
            for signal in signals
            if signal.status == "eligible"
        )
        ranked = OpportunityRanker().rank(opportunities)
        by_id = {signal.identity.event_id: signal for signal in signals}
        return tuple(
            RankedSignal(
                by_id[item.signal_id],
                item.expected_value,
                index,
                (f"net rank score {item.score:.4f}", "cost and portfolio penalties applied"),
            )
            for index, item in enumerate(ranked, start=1)
        )

    def prepare_paper_proposal(
        self,
        ranked: RankedSignal,
        account_id: str,
        equity: Decimal,
        risk_fraction: Decimal,
        now: datetime,
    ) -> PaperProposalView:
        signal = ranked.signal
        if signal.status != "eligible" or signal.stop_price is None:
            raise PermissionError("only eligible signals can become proposals")
        if not Decimal("0") < risk_fraction <= Decimal("0.02"):
            raise ValueError("paper account risk fraction must be in (0, 0.02]")
        entry = (
            (Decimal(signal.entry_zone.split("-")[0]) + Decimal(signal.entry_zone.split("-")[1]))
            / 2
            if signal.entry_zone
            else Decimal("0")
        )
        risk_per_unit = abs(entry - signal.stop_price)
        quantity = (equity * risk_fraction / risk_per_unit).quantize(
            Decimal("0.0001"), rounding=ROUND_DOWN
        )
        identity = EventIdentity(
            f"proposal-{uuid4()}",
            now,
            now,
            now,
            "foreight",
            ranked.signal.identity.correlation_id,
            signal.identity.event_id,
            self.policy.strategy_version,
        )
        proposal = OrderProposal(
            identity,
            signal.identity.event_id,
            signal.instrument_id,
            signal.side,
            quantity,
            entry,
            signal.stop_price,
            min(signal.expires_at, now + timedelta(minutes=15)),
            "paper",
        )
        return PaperProposalView(
            proposal,
            account_id,
            "local-paper",
            "market",
            signal.target_prices,
            quantity * risk_per_unit,
            risk_fraction,
            ranked.expected_value,
            signal.estimated_transaction_costs * quantity,
            signal.strategy_version,
            self.policy.model_version,
        )
