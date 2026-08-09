"""Contracts for provider-neutral trading broker interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Protocol

from foreightkillo.domain import InstrumentId, Side


@dataclass(frozen=True, slots=True)
class BrokerHealth:
    provider: str
    healthy: bool
    detail: str
    checked_at: datetime


@dataclass(frozen=True, slots=True)
class BrokerAccount:
    account_id: str
    balance: Decimal
    equity: Decimal
    currency: str
    open_positions: int
    mode: str


@dataclass(frozen=True, slots=True)
class BrokerPosition:
    position_id: str
    instrument_id: InstrumentId
    side: Side
    quantity: Decimal
    entry_price: Decimal
    unrealized_pnl: Decimal
    margin_required: Decimal


@dataclass(frozen=True, slots=True)
class BrokerOrder:
    order_id: str
    instrument_id: InstrumentId
    side: Side
    quantity: Decimal
    price: Decimal
    stop_price: Decimal | None
    status: str
    filled_quantity: Decimal
    executed_at: datetime | None


class Broker(Protocol):
    name: str

    def health(self) -> BrokerHealth: ...

    def get_account(self) -> BrokerAccount: ...

    def discover_instruments(self) -> tuple[InstrumentId, ...]: ...

    def submit_order(
        self,
        instrument_id: InstrumentId,
        side: Side,
        quantity: Decimal,
        price: Decimal,
        stop_price: Decimal | None,
        mode: str,
    ) -> BrokerOrder: ...

    def list_positions(self) -> tuple[BrokerPosition, ...]: ...

    def list_orders(self) -> tuple[BrokerOrder, ...]: ...
