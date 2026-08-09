"""Deterministic market-structure analysis and opportunity ranking."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from statistics import fmean

from foreightkillo.domain import Candle, Side


@dataclass(frozen=True, slots=True)
class MarketEvidence:
    regime: str
    direction: Side
    structure: str
    liquidity_event: str
    imbalance: Decimal
    volatility: Decimal
    confidence: Decimal
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Opportunity:
    signal_id: str
    expected_value: Decimal
    reward_to_risk: Decimal
    transaction_cost: Decimal
    freshness: Decimal
    regime_compatibility: Decimal
    portfolio_penalty: Decimal
    model_uncertainty: Decimal

    @property
    def score(self) -> Decimal:
        gross = self.expected_value * self.reward_to_risk
        quality = (self.freshness + self.regime_compatibility) / Decimal("2")
        return (
            gross * quality
            - self.transaction_cost
            - self.portfolio_penalty
            - self.model_uncertainty
        )


class SmartMoneyAnalyzer:
    """Explainable SMC-style heuristics; never a source of market truth."""

    def analyze(self, candles: tuple[Candle, ...]) -> MarketEvidence:
        if len(candles) < 20 or any(not candle.complete for candle in candles):
            raise ValueError("at least 20 complete candles are required")
        closes = [float(candle.close) for candle in candles]
        fast = fmean(closes[-5:])
        slow = fmean(closes[-20:])
        direction = Side.BUY if fast >= slow else Side.SELL
        regime = "trending" if abs(fast - slow) / slow >= 0.001 else "ranging"
        prior = candles[-6:-1]
        last = candles[-1]
        prior_high = max(candle.high for candle in prior)
        prior_low = min(candle.low for candle in prior)
        if last.low < prior_low and last.close > prior_low:
            liquidity = "sell_side_sweep"
        elif last.high > prior_high and last.close < prior_high:
            liquidity = "buy_side_sweep"
        else:
            liquidity = "none"
        ranges = [float(candle.high - candle.low) for candle in candles[-20:]]
        volatility = Decimal(str(fmean(ranges)))
        imbalance = abs(last.close - last.open)
        structure = "bullish" if direction is Side.BUY else "bearish"
        evidence = [f"{structure} moving-average structure", f"{regime} market regime"]
        if liquidity != "none":
            evidence.append(liquidity.replace("_", " "))
        confidence = Decimal("0.50")
        confidence += Decimal("0.20") if regime == "trending" else Decimal("0.05")
        confidence += Decimal("0.15") if liquidity != "none" else Decimal("0")
        confidence += min(Decimal("0.15"), imbalance / max(last.close, Decimal("0.000001")) * 10)
        return MarketEvidence(
            regime,
            direction,
            structure,
            liquidity,
            imbalance,
            volatility,
            min(confidence, Decimal("0.95")),
            tuple(evidence),
        )


class OpportunityRanker:
    def rank(
        self, opportunities: tuple[Opportunity, ...], minimum_score: Decimal = Decimal("0")
    ) -> tuple[Opportunity, ...]:
        return tuple(
            sorted(
                (item for item in opportunities if item.score >= minimum_score),
                key=lambda item: (item.score, item.signal_id),
                reverse=True,
            )
        )
