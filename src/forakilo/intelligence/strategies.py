"""Explainable multi-strategy technical research without execution authority."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from itertools import pairwise

from forakilo.domain import Candle, Side


@dataclass(frozen=True, slots=True)
class TechnicalSnapshot:
    fast_ema: Decimal
    slow_ema: Decimal
    relative_strength_index: Decimal
    average_true_range: Decimal
    z_score: Decimal
    breakout_high: Decimal
    breakout_low: Decimal


@dataclass(frozen=True, slots=True)
class StrategyCandidate:
    strategy: str
    side: Side | None
    status: str
    confidence: Decimal
    reasons: tuple[str, ...]
    invalidation_level: Decimal | None


@dataclass(frozen=True, slots=True)
class MultiTimeframeAssessment:
    direction: Side | None
    agreement: Decimal
    timeframes: tuple[tuple[int, Side | None], ...]
    reasons: tuple[str, ...]


class TechnicalStrategyEngine:
    """Produces research candidates; it cannot create proposals or orders."""

    def snapshot(self, candles: tuple[Candle, ...]) -> TechnicalSnapshot:
        self._validate(candles, 30)
        closes = tuple(item.close for item in candles)
        fast = self._ema(closes, 9)
        slow = self._ema(closes, 21)
        rsi = self._rsi(closes, 14)
        true_ranges: list[Decimal] = []
        for previous, current in zip(candles[-15:-1], candles[-14:], strict=True):
            true_ranges.append(
                max(
                    current.high - current.low,
                    abs(current.high - previous.close),
                    abs(current.low - previous.close),
                )
            )
        atr = sum(true_ranges, Decimal("0")) / Decimal(len(true_ranges))
        window = closes[-20:]
        mean = sum(window, Decimal("0")) / Decimal(len(window))
        variance = sum(((item - mean) ** 2 for item in window), Decimal("0")) / Decimal(len(window))
        standard_deviation = variance.sqrt()
        z_score = (closes[-1] - mean) / standard_deviation if standard_deviation else Decimal("0")
        return TechnicalSnapshot(
            fast,
            slow,
            rsi,
            atr,
            z_score,
            max(item.high for item in candles[-21:-1]),
            min(item.low for item in candles[-21:-1]),
        )

    def evaluate(self, candles: tuple[Candle, ...]) -> tuple[StrategyCandidate, ...]:
        snapshot = self.snapshot(candles)
        last = candles[-1]
        trend_side = Side.BUY if snapshot.fast_ema > snapshot.slow_ema else Side.SELL
        trend_gap = abs(snapshot.fast_ema - snapshot.slow_ema) / snapshot.slow_ema
        trend = self._candidate(
            "trend-following",
            trend_side,
            min(Decimal("0.95"), Decimal("0.50") + trend_gap * 20),
            (
                "9-period EMA is above 21-period EMA"
                if trend_side is Side.BUY
                else "9-period EMA is below 21-period EMA",
            ),
            snapshot.slow_ema,
            trend_gap >= Decimal("0.0005"),
        )
        if snapshot.relative_strength_index >= 55:
            momentum_side: Side | None = Side.BUY
        elif snapshot.relative_strength_index <= 45:
            momentum_side = Side.SELL
        else:
            momentum_side = None
        momentum = self._candidate(
            "momentum",
            momentum_side,
            Decimal("0.50") + abs(snapshot.relative_strength_index - 50) / 100,
            (f"RSI(14) is {snapshot.relative_strength_index:.2f}",),
            last.low if momentum_side is Side.BUY else last.high if momentum_side else None,
            momentum_side is not None,
        )
        if last.close > snapshot.breakout_high:
            breakout_side: Side | None = Side.BUY
        elif last.close < snapshot.breakout_low:
            breakout_side = Side.SELL
        else:
            breakout_side = None
        breakout = self._candidate(
            "volatility-breakout",
            breakout_side,
            Decimal("0.70") if breakout_side else Decimal("0.30"),
            ("close tested the prior 20-bar price boundary",),
            snapshot.breakout_high
            if breakout_side is Side.BUY
            else snapshot.breakout_low
            if breakout_side
            else None,
            breakout_side is not None and snapshot.average_true_range > 0,
        )
        if snapshot.z_score <= Decimal("-1.5"):
            reversion_side: Side | None = Side.BUY
        elif snapshot.z_score >= Decimal("1.5"):
            reversion_side = Side.SELL
        else:
            reversion_side = None
        reversion = self._candidate(
            "mean-reversion",
            reversion_side,
            min(Decimal("0.90"), Decimal("0.45") + abs(snapshot.z_score) / 10),
            (f"20-bar close z-score is {snapshot.z_score:.2f}",),
            snapshot.slow_ema,
            reversion_side is not None and trend_gap < Decimal("0.02"),
        )
        harmonic = self._harmonic(candles)
        return trend, momentum, breakout, reversion, harmonic

    def assess_timeframes(
        self, histories: tuple[tuple[int, tuple[Candle, ...]], ...]
    ) -> MultiTimeframeAssessment:
        if len(histories) < 2:
            raise ValueError("at least two timeframes are required")
        directions = tuple(
            (
                interval,
                Side.BUY
                if self.snapshot(candles).fast_ema > self.snapshot(candles).slow_ema
                else Side.SELL,
            )
            for interval, candles in histories
        )
        buy_count = sum(1 for _, side in directions if side is Side.BUY)
        sell_count = len(directions) - buy_count
        winning = max(buy_count, sell_count)
        agreement = Decimal(winning) / Decimal(len(directions))
        direction = (
            Side.BUY if buy_count > sell_count else Side.SELL if sell_count > buy_count else None
        )
        return MultiTimeframeAssessment(
            direction,
            agreement,
            directions,
            (f"{winning} of {len(directions)} timeframes agree",),
        )

    def _harmonic(self, candles: tuple[Candle, ...]) -> StrategyCandidate:
        closes = tuple(item.close for item in candles[-25:])
        pivots = [closes[0]]
        for previous, current, following in zip(closes[:-2], closes[1:-1], closes[2:], strict=True):
            if (current > previous and current > following) or (
                current < previous and current < following
            ):
                pivots.append(current)
        pivots.append(closes[-1])
        if len(pivots) < 5:
            return self._candidate(
                "harmonic", None, Decimal("0.20"), ("fewer than five price pivots",), None, False
            )
        x, a, b, c, d = pivots[-5:]
        xa = abs(a - x)
        ab = abs(b - a)
        bc = abs(c - b)
        cd = abs(d - c)
        if min(xa, ab, bc) == 0:
            valid = False
        else:
            valid = (
                Decimal("0.55") <= ab / xa <= Decimal("0.82")
                and Decimal("0.38") <= bc / ab <= Decimal("0.90")
                and Decimal("1.13") <= cd / bc <= Decimal("1.90")
            )
        side = Side.BUY if valid and d < c else Side.SELL if valid else None
        return self._candidate(
            "harmonic",
            side,
            Decimal("0.65") if valid else Decimal("0.20"),
            (
                "XABCD retracement ratios are within configured research ranges"
                if valid
                else "no qualifying XABCD ratio sequence",
            ),
            d if valid else None,
            valid,
        )

    @staticmethod
    def _candidate(
        name: str,
        side: Side | None,
        confidence: Decimal,
        reasons: tuple[str, ...],
        invalidation: Decimal | None,
        eligible: bool,
    ) -> StrategyCandidate:
        return StrategyCandidate(
            name, side, "candidate" if eligible else "rejected", confidence, reasons, invalidation
        )

    @staticmethod
    def _validate(candles: tuple[Candle, ...], minimum: int) -> None:
        if len(candles) < minimum or any(not item.complete for item in candles):
            raise ValueError(f"at least {minimum} complete candles are required")
        times = tuple(item.identity.event_time for item in candles)
        if times != tuple(sorted(times)) or len(times) != len(set(times)):
            raise ValueError("candles must be unique and event-time ordered")

    @staticmethod
    def _ema(values: tuple[Decimal, ...], period: int) -> Decimal:
        multiplier = Decimal("2") / Decimal(period + 1)
        value = sum(values[:period], Decimal("0")) / Decimal(period)
        for item in values[period:]:
            value = (item - value) * multiplier + value
        return value

    @staticmethod
    def _rsi(values: tuple[Decimal, ...], period: int) -> Decimal:
        changes = tuple(current - previous for previous, current in pairwise(values))[-period:]
        gains = sum((max(item, Decimal("0")) for item in changes), Decimal("0")) / Decimal(period)
        losses = sum((max(-item, Decimal("0")) for item in changes), Decimal("0")) / Decimal(period)
        if losses == 0:
            return Decimal("100")
        strength = gains / losses
        return Decimal("100") - Decimal("100") / (Decimal("1") + strength)
