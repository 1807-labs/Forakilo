"""Local paper broker for MVP testing and order lifecycle simulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from forakilo.brokers.interface import (
    Broker,
    BrokerAccount,
    BrokerHealth,
    BrokerOrder,
    BrokerPosition,
)
from forakilo.domain import InstrumentId, Side


@dataclass(frozen=True, slots=True)
class LocalBroker(Broker):
    name: str = "local-paper"
    _account_id: str = "paper-001"
    _currency: str = "USD"
    _balance: Decimal = Decimal("100000")
    _margin_multiplier: Decimal = Decimal("0.02")
    _positions: dict[str, BrokerPosition] = field(init=False, repr=False, compare=False)
    _orders: dict[str, BrokerOrder] = field(init=False, repr=False, compare=False)
    _last_updated: datetime = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_positions", {})
        object.__setattr__(self, "_orders", {})
        object.__setattr__(self, "_last_updated", datetime.now(UTC))

    def health(self) -> BrokerHealth:
        return BrokerHealth(self.name, True, "local paper broker", datetime.now(UTC))

    def get_account(self) -> BrokerAccount:
        return BrokerAccount(
            account_id=self._account_id,
            balance=self._balance,
            equity=self._balance,
            currency=self._currency,
            open_positions=len(self._positions),
            mode="paper",
        )

    def discover_instruments(self) -> tuple[InstrumentId, ...]:
        return tuple(
            sorted(
                {position.instrument_id for position in self._positions.values()},
                key=lambda item: (item.venue, item.symbol),
            )
        )

    def submit_order(
        self,
        instrument_id: InstrumentId,
        side: Side,
        quantity: Decimal,
        price: Decimal,
        stop_price: Decimal | None,
        mode: str,
    ) -> BrokerOrder:
        if mode not in {"paper", "sandbox-manual"}:
            raise PermissionError("live orders not permitted")
        order_id = str(uuid4())
        self._orders[order_id] = BrokerOrder(
            order_id=order_id,
            instrument_id=instrument_id,
            side=side,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
            status="filled",
            filled_quantity=quantity,
            executed_at=datetime.now(UTC),
        )
        position_id = f"pos-{order_id[:8]}"
        self._positions[position_id] = BrokerPosition(
            position_id=position_id,
            instrument_id=instrument_id,
            side=side,
            quantity=quantity,
            entry_price=price,
            unrealized_pnl=Decimal("0"),
            margin_required=quantity * price * self._margin_multiplier,
        )
        return self._orders[order_id]

    def list_positions(self) -> tuple[BrokerPosition, ...]:
        return tuple(self._positions.values())

    def list_orders(self) -> tuple[BrokerOrder, ...]:
        return tuple(self._orders.values())
