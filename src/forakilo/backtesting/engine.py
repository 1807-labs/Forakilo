"""Deterministic event-ordered backtesting with explicit costs and no lookahead."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Protocol

from forakilo.domain import Candle, Side


class Strategy(Protocol):
    def decide(self, history: tuple[Candle, ...]) -> Side | None: ...


@dataclass(frozen=True, slots=True)
class BacktestConfig:
    initial_equity: Decimal = Decimal("10000")
    risk_fraction: Decimal = Decimal("0.01")
    stop_fraction: Decimal = Decimal("0.01")
    holding_bars: int = 5
    spread_fraction: Decimal = Decimal("0.0002")
    slippage_fraction: Decimal = Decimal("0.0001")
    warmup_bars: int = 20

    def __post_init__(self) -> None:
        if self.initial_equity <= 0:
            raise ValueError("initial equity must be positive")
        if not Decimal("0") < self.risk_fraction <= Decimal("0.02"):
            raise ValueError("risk fraction must be in (0, 0.02]")
        if not Decimal("0") < self.stop_fraction < Decimal("1"):
            raise ValueError("stop fraction must be in (0, 1)")
        if self.holding_bars < 1 or self.warmup_bars < 2:
            raise ValueError("holding and warmup bars are invalid")
        if self.spread_fraction < 0 or self.slippage_fraction < 0:
            raise ValueError("cost assumptions cannot be negative")


@dataclass(frozen=True, slots=True)
class BacktestTrade:
    side: Side
    entry_time: datetime
    exit_time: datetime
    entry_price: Decimal
    exit_price: Decimal
    quantity: Decimal
    gross_pnl: Decimal
    costs: Decimal
    net_pnl: Decimal


@dataclass(frozen=True, slots=True)
class BacktestReport:
    initial_equity: Decimal
    final_equity: Decimal
    net_pnl: Decimal
    total_return: Decimal
    maximum_drawdown: Decimal
    trades: tuple[BacktestTrade, ...]
    winning_trades: int
    losing_trades: int
    win_rate: Decimal | None
    profit_factor: Decimal | None
    assumptions: tuple[str, ...]


class BacktestEngine:
    def run(
        self, candles: tuple[Candle, ...], strategy: Strategy, config: BacktestConfig
    ) -> BacktestReport:
        minimum = config.warmup_bars + config.holding_bars + 1
        if len(candles) < minimum:
            raise ValueError(f"at least {minimum} complete candles are required")
        if any(not item.complete for item in candles):
            raise ValueError("backtests require complete candles")
        timestamps = tuple(item.identity.event_time for item in candles)
        if timestamps != tuple(sorted(timestamps)) or len(set(timestamps)) != len(timestamps):
            raise ValueError("candles must be unique and event-time ordered")

        equity = config.initial_equity
        peak = equity
        maximum_drawdown = Decimal("0")
        trades: list[BacktestTrade] = []
        index = config.warmup_bars - 1
        while index + config.holding_bars + 1 < len(candles):
            history = candles[: index + 1]
            side = strategy.decide(history)
            if side is None:
                index += 1
                continue
            entry = candles[index + 1]
            exit_candle = candles[index + 1 + config.holding_bars]
            half_spread = config.spread_fraction / Decimal("2")
            friction = half_spread + config.slippage_fraction
            direction = Decimal("1") if side is Side.BUY else Decimal("-1")
            entry_price = entry.open * (Decimal("1") + direction * friction)
            exit_price = exit_candle.close * (Decimal("1") - direction * friction)
            risk_budget = equity * config.risk_fraction
            quantity = risk_budget / (entry_price * config.stop_fraction)
            gross = (exit_candle.close - entry.open) * quantity * direction
            reference_cost = (entry.open + exit_candle.close) * quantity * friction
            net = gross - reference_cost
            equity += net
            peak = max(peak, equity)
            drawdown = (peak - equity) / peak
            maximum_drawdown = max(maximum_drawdown, drawdown)
            trades.append(
                BacktestTrade(
                    side,
                    entry.identity.event_time,
                    exit_candle.identity.event_time,
                    entry_price,
                    exit_price,
                    quantity,
                    gross,
                    reference_cost,
                    net,
                )
            )
            index += config.holding_bars + 1

        wins = tuple(item.net_pnl for item in trades if item.net_pnl > 0)
        losses = tuple(-item.net_pnl for item in trades if item.net_pnl < 0)
        net_pnl = equity - config.initial_equity
        return BacktestReport(
            config.initial_equity,
            equity,
            net_pnl,
            net_pnl / config.initial_equity,
            maximum_drawdown,
            tuple(trades),
            len(wins),
            len(losses),
            Decimal(len(wins)) / Decimal(len(trades)) if trades else None,
            sum(wins, Decimal("0")) / sum(losses, Decimal("0")) if losses else None,
            (
                "decisions use only candles known before the next-bar entry",
                "fills include configured spread and slippage assumptions",
                "results are simulated and do not predict future performance",
            ),
        )
