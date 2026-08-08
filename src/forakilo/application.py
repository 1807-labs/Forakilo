"""MVP application service joining verified data to explainable analysis."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from forakilo.intelligence.market import SmartMoneyAnalyzer
from forakilo.marketdata.contracts import MarketDataProvider


class ForeightService:
    def __init__(self, market_data: MarketDataProvider) -> None:
        self._market_data = market_data
        self._analyzer = SmartMoneyAnalyzer()

    def instruments(self) -> tuple[dict[str, str], ...]:
        return tuple(
            {
                "venue": item.instrument_id.venue,
                "symbol": item.instrument_id.symbol,
                "asset_class": item.asset_class.value,
            }
            for item in self._market_data.discover_instruments()
        )

    def analyze(self, symbol: str, interval_seconds: int = 3600) -> dict[str, Any]:
        instrument = next(
            (
                item
                for item in self._market_data.discover_instruments()
                if item.instrument_id.symbol == symbol
            ),
            None,
        )
        if instrument is None:
            raise KeyError(symbol)
        evidence = self._analyzer.analyze(
            self._market_data.get_history(instrument.instrument_id, interval_seconds, 100)
        )
        result = asdict(evidence)
        result.update(
            {
                "instrument": symbol,
                "asset_class": instrument.asset_class.value,
                "timeframe_seconds": interval_seconds,
                "strategy": "foreight-market-structure",
                "strategy_version": "1.0.0",
                "paper_only": True,
                "disclaimer": "Research evidence only; profitability is not guaranteed.",
            }
        )
        return result
