"""Contracts for market data providers and discovery."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from forakilo.domain import Candle, Instrument, InstrumentId, Quote


@dataclass(frozen=True, slots=True)
class ProviderHealth:
    provider: str
    healthy: bool
    detail: str
    checked_at: datetime


class MarketDataProvider(Protocol):
    name: str

    def discover_instruments(self) -> tuple[Instrument, ...]: ...

    def get_quote(self, instrument_id: InstrumentId) -> Quote: ...

    def get_history(
        self, instrument_id: InstrumentId, interval_seconds: int, count: int
    ) -> tuple[Candle, ...]: ...

    def health(self) -> ProviderHealth: ...
