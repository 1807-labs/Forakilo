"""Strict immutable contracts for time-aware research and paper execution."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from hashlib import sha256
from typing import Any, cast

SCHEMA_VERSION = "1.0.0"


def _utc(value: datetime, field: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat()
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, dict):
        mapping = cast(dict[str, Any], value)
        return {key: _canonical(item) for key, item in sorted(mapping.items())}
    if isinstance(value, (tuple, list)):
        sequence = cast(tuple[Any, ...] | list[Any], value)
        return [_canonical(item) for item in sequence]
    return value


def stable_hash(value: Any) -> str:
    payload = json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


class AssetClass(StrEnum):
    CRYPTO = "crypto"
    FX = "fx"


class Side(StrEnum):
    BUY = "buy"
    SELL = "sell"


@dataclass(frozen=True, slots=True)
class EventIdentity:
    event_id: str
    event_time: datetime
    known_time: datetime
    recorded_time: datetime
    provenance: str
    correlation_id: str
    causation_id: str | None
    configuration_version: str
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        for field in ("event_time", "known_time", "recorded_time"):
            _utc(getattr(self, field), field)
        if self.known_time < self.event_time:
            raise ValueError("known_time cannot precede event_time")
        if self.recorded_time < self.known_time:
            raise ValueError("recorded_time cannot precede known_time")
        required = (
            self.event_id,
            self.provenance,
            self.correlation_id,
            self.configuration_version,
        )
        if any(not item.strip() for item in required):
            raise ValueError("identity fields cannot be blank")


@dataclass(frozen=True, slots=True)
class InstrumentId:
    venue: str
    symbol: str

    def __post_init__(self) -> None:
        if not self.venue or not self.symbol:
            raise ValueError("venue and symbol are required")


@dataclass(frozen=True, slots=True)
class Instrument:
    instrument_id: InstrumentId
    asset_class: AssetClass
    base_currency: str
    quote_currency: str
    price_increment: Decimal
    quantity_increment: Decimal
    properties_version: str

    def __post_init__(self) -> None:
        if self.price_increment <= 0 or self.quantity_increment <= 0:
            raise ValueError("increments must be positive")


@dataclass(frozen=True, slots=True)
class MarketDataProvenance:
    source: str
    source_record_id: str
    content_hash: str
    revision: int = 0

    def __post_init__(self) -> None:
        if self.revision < 0:
            raise ValueError("revision cannot be negative")


@dataclass(frozen=True, slots=True)
class Quote:
    identity: EventIdentity
    instrument_id: InstrumentId
    bid: Decimal
    ask: Decimal
    provenance: MarketDataProvenance

    def __post_init__(self) -> None:
        if self.bid <= 0 or self.ask <= 0:
            raise ValueError("bid and ask must be positive")
        if self.ask < self.bid:
            raise ValueError("ask cannot be below bid")


@dataclass(frozen=True, slots=True)
class Candle:
    identity: EventIdentity
    instrument_id: InstrumentId
    interval_seconds: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    complete: bool
    provenance: MarketDataProvenance

    def __post_init__(self) -> None:
        if self.interval_seconds <= 0:
            raise ValueError("interval must be positive")
        if min(self.open, self.high, self.low, self.close) <= 0:
            raise ValueError("OHLC prices must be positive")
        if self.high < max(self.open, self.close) or self.low > min(self.open, self.close):
            raise ValueError("invalid OHLC boundary")
        if self.volume < 0:
            raise ValueError("volume cannot be negative")


@dataclass(frozen=True, slots=True)
class Signal:
    identity: EventIdentity
    strategy_id: str
    strategy_version: str
    instrument_id: InstrumentId
    side: Side
    expires_at: datetime
    evidence: tuple[str, ...]
    candidate_id: str

    def __post_init__(self) -> None:
        _utc(self.expires_at, "expires_at")
        if self.expires_at <= self.identity.known_time:
            raise ValueError("signal must expire after it becomes known")
        if not self.evidence:
            raise ValueError("signal evidence is required")


@dataclass(frozen=True, slots=True)
class OrderProposal:
    identity: EventIdentity
    signal_id: str
    instrument_id: InstrumentId
    side: Side
    quantity: Decimal
    reference_price: Decimal
    stop_price: Decimal
    expires_at: datetime
    mode: str

    def __post_init__(self) -> None:
        _utc(self.expires_at, "expires_at")
        if self.quantity <= 0 or self.reference_price <= 0 or self.stop_price <= 0:
            raise ValueError("quantity and prices must be positive")
        if self.side is Side.BUY and self.stop_price >= self.reference_price:
            raise ValueError("buy stop must be below reference price")
        if self.side is Side.SELL and self.stop_price <= self.reference_price:
            raise ValueError("sell stop must be above reference price")

    @property
    def proposal_hash(self) -> str:
        return stable_hash(asdict(self))
