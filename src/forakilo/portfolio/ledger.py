"""Deterministic paper position ledger with broker reconciliation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal

from forakilo.brokers.interface import BrokerPosition
from forakilo.domain import InstrumentId, Side
from forakilo.execution import PaperOrder


@dataclass(frozen=True, slots=True)
class Position:
    position_id: str
    instrument_id: InstrumentId
    side: Side
    quantity: Decimal
    average_entry: Decimal
    mark_price: Decimal
    opened_at: datetime
    updated_at: datetime
    strategy_id: str
    signal_id: str
    transaction_costs: Decimal = Decimal("0")

    @property
    def unrealized_pnl(self) -> Decimal:
        movement = self.mark_price - self.average_entry
        direction = Decimal("1") if self.side is Side.BUY else Decimal("-1")
        return movement * self.quantity * direction - self.transaction_costs


@dataclass(frozen=True, slots=True)
class ClosedTrade:
    position_id: str
    instrument_id: InstrumentId
    side: Side
    quantity: Decimal
    entry_price: Decimal
    exit_price: Decimal
    opened_at: datetime
    closed_at: datetime
    realized_pnl: Decimal
    transaction_costs: Decimal
    strategy_id: str
    signal_id: str


@dataclass(frozen=True, slots=True)
class PerformanceSummary:
    closed_trades: int
    winning_trades: int
    losing_trades: int
    realized_pnl: Decimal
    unrealized_pnl: Decimal
    total_transaction_costs: Decimal
    win_rate: Decimal | None
    average_trade_pnl: Decimal | None


@dataclass(frozen=True, slots=True)
class ReconciliationResult:
    reconciled: bool
    missing_locally: tuple[str, ...]
    missing_at_broker: tuple[str, ...]
    quantity_mismatches: tuple[str, ...]
    checked_at: datetime


class PortfolioLedger:
    def __init__(self) -> None:
        self._positions: dict[str, Position] = {}
        self._closed: list[ClosedTrade] = []

    def open_from_fill(
        self,
        order: PaperOrder,
        instrument_id: InstrumentId,
        side: Side,
        now: datetime,
        strategy_id: str,
        signal_id: str,
        transaction_costs: Decimal = Decimal("0"),
    ) -> Position:
        if transaction_costs < 0:
            raise ValueError("transaction costs cannot be negative")
        position_id = f"position-{order.order_id}"
        existing = self._positions.get(position_id)
        if existing:
            return existing
        position = Position(
            position_id,
            instrument_id,
            side,
            order.quantity,
            order.fill_price,
            order.fill_price,
            now,
            now,
            strategy_id,
            signal_id,
            transaction_costs,
        )
        self._positions[position_id] = position
        return position

    def mark(self, position_id: str, price: Decimal, now: datetime) -> Position:
        if price <= 0:
            raise ValueError("mark price must be positive")
        position = replace(self._positions[position_id], mark_price=price, updated_at=now)
        self._positions[position_id] = position
        return position

    def close(
        self,
        position_id: str,
        exit_price: Decimal,
        now: datetime,
        exit_costs: Decimal = Decimal("0"),
    ) -> ClosedTrade:
        if exit_price <= 0 or exit_costs < 0:
            raise ValueError("exit price and costs are invalid")
        position = self._positions.pop(position_id)
        direction = Decimal("1") if position.side is Side.BUY else Decimal("-1")
        costs = position.transaction_costs + exit_costs
        pnl = (exit_price - position.average_entry) * position.quantity * direction - costs
        trade = ClosedTrade(
            position.position_id,
            position.instrument_id,
            position.side,
            position.quantity,
            position.average_entry,
            exit_price,
            position.opened_at,
            now,
            pnl,
            costs,
            position.strategy_id,
            position.signal_id,
        )
        self._closed.append(trade)
        return trade

    def positions(self) -> tuple[Position, ...]:
        return tuple(sorted(self._positions.values(), key=lambda item: item.position_id))

    def closed_trades(self) -> tuple[ClosedTrade, ...]:
        return tuple(self._closed)

    def performance(self) -> PerformanceSummary:
        realized = sum((trade.realized_pnl for trade in self._closed), Decimal("0"))
        unrealized = sum((item.unrealized_pnl for item in self._positions.values()), Decimal("0"))
        costs = sum((trade.transaction_costs for trade in self._closed), Decimal("0"))
        costs += sum((item.transaction_costs for item in self._positions.values()), Decimal("0"))
        count = len(self._closed)
        wins = sum(1 for trade in self._closed if trade.realized_pnl > 0)
        losses = sum(1 for trade in self._closed if trade.realized_pnl < 0)
        return PerformanceSummary(
            count,
            wins,
            losses,
            realized,
            unrealized,
            costs,
            Decimal(wins) / Decimal(count) if count else None,
            realized / Decimal(count) if count else None,
        )

    def reconcile(
        self, broker_positions: tuple[BrokerPosition, ...], checked_at: datetime
    ) -> ReconciliationResult:
        local = {item.position_id: item for item in self._positions.values()}
        remote = {item.position_id: item for item in broker_positions}
        missing_locally = tuple(sorted(set(remote) - set(local)))
        missing_at_broker = tuple(sorted(set(local) - set(remote)))
        mismatches = tuple(
            sorted(
                key
                for key in set(local) & set(remote)
                if local[key].quantity != remote[key].quantity
                or local[key].instrument_id != remote[key].instrument_id
                or local[key].side is not remote[key].side
            )
        )
        reconciled = not (missing_locally or missing_at_broker or mismatches)
        return ReconciliationResult(
            reconciled, missing_locally, missing_at_broker, mismatches, checked_at
        )
