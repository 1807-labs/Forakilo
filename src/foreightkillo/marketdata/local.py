"""A local provider for synthetic market data and development use."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from random import Random

from foreightkillo.domain import (
    AssetClass,
    Candle,
    EventIdentity,
    Instrument,
    InstrumentId,
    MarketDataProvenance,
    Quote,
)

from .contracts import MarketDataProvider, ProviderHealth


@dataclass(frozen=True, slots=True)
class LocalMarketDataProvider(MarketDataProvider):
    name: str = "local"
    seed: int = 0
    _rand: Random = field(init=False, repr=False, compare=False)
    _instruments: tuple[Instrument, ...] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_rand", Random(self.seed))  # noqa: S311 - synthetic fixture
        object.__setattr__(self, "_instruments", self._build_instruments())

    def _build_instruments(self) -> tuple[Instrument, ...]:
        return (
            Instrument(
                instrument_id=InstrumentId("local", "EUR_USD"),
                asset_class=AssetClass.FX,
                base_currency="EUR",
                quote_currency="USD",
                price_increment=Decimal("0.00001"),
                quantity_increment=Decimal("0.001"),
                properties_version="1",
            ),
            Instrument(
                instrument_id=InstrumentId("local", "XAU_USD"),
                asset_class=AssetClass.COMMODITY,
                base_currency="XAU",
                quote_currency="USD",
                price_increment=Decimal("0.01"),
                quantity_increment=Decimal("0.01"),
                properties_version="1",
            ),
            Instrument(
                instrument_id=InstrumentId("local", "BTC_USD"),
                asset_class=AssetClass.CRYPTO,
                base_currency="BTC",
                quote_currency="USD",
                price_increment=Decimal("0.01"),
                quantity_increment=Decimal("0.0001"),
                properties_version="1",
            ),
        )

    def discover_instruments(self) -> tuple[Instrument, ...]:
        return self._instruments

    def get_quote(self, instrument_id: InstrumentId) -> Quote:
        now = datetime.now(UTC)
        price = self._price_for(instrument_id)
        spread = Decimal("0.0003") if instrument_id.symbol == "EUR_USD" else Decimal("0.5")
        bid = price - spread / 2
        ask = price + spread / 2
        identity = EventIdentity(
            event_id=f"quote-{instrument_id.symbol}-{int(now.timestamp())}",
            event_time=now,
            known_time=now,
            recorded_time=now,
            provenance="local.synthetic",
            correlation_id="local",
            causation_id=None,
            configuration_version="1.0.0",
        )
        provenance = MarketDataProvenance("local", identity.event_id, "local", 0)
        return Quote(identity, instrument_id, bid, ask, provenance)

    def get_history(
        self, instrument_id: InstrumentId, interval_seconds: int, count: int
    ) -> tuple[Candle, ...]:
        now = datetime.now(UTC)
        base = self._price_for(instrument_id)
        candles: list[Candle] = []
        for index in range(count):
            close = base + Decimal(str((self._rand.random() - 0.5) * 2 * 0.05))
            high = close + Decimal("0.02")
            low = close - Decimal("0.02")
            open_price = close + Decimal(str((self._rand.random() - 0.5) * 0.01))
            volume = Decimal(str(self._rand.uniform(100, 1000)))
            ts = now - timedelta(seconds=interval_seconds * (count - index))
            identity = EventIdentity(
                event_id=f"candle-{instrument_id.symbol}-{int(ts.timestamp())}",
                event_time=ts,
                known_time=ts,
                recorded_time=ts,
                provenance="local.synthetic",
                correlation_id="local",
                causation_id=None,
                configuration_version="1.0.0",
            )
            provenance = MarketDataProvenance("local", identity.event_id, "local", 0)
            candles.append(
                Candle(
                    identity=identity,
                    instrument_id=instrument_id,
                    interval_seconds=interval_seconds,
                    open=Decimal(open_price.quantize(Decimal("0.01"))),
                    high=Decimal(high.quantize(Decimal("0.01"))),
                    low=Decimal(low.quantize(Decimal("0.01"))),
                    close=Decimal(close.quantize(Decimal("0.01"))),
                    volume=volume.quantize(Decimal("0.01")),
                    complete=True,
                    provenance=provenance,
                )
            )
        return tuple(candles)

    def health(self) -> ProviderHealth:
        return ProviderHealth(self.name, True, "local synthetic provider", datetime.now(UTC))

    def _price_for(self, instrument_id: InstrumentId) -> Decimal:
        if instrument_id.symbol == "EUR_USD":
            return Decimal("1.0800")
        if instrument_id.symbol == "XAU_USD":
            return Decimal("1975.0")
        if instrument_id.symbol == "BTC_USD":
            return Decimal("46000.0")
        raise ValueError("unknown instrument")
