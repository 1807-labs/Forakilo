"""MVP application service joining verified data to explainable analysis."""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from foreightkillo.intelligence.market import SmartMoneyAnalyzer
from foreightkillo.intelligence.strategies import TechnicalStrategyEngine
from foreightkillo.marketdata.contracts import MarketDataProvider
from foreightkillo.portfolio import PortfolioLedger
from foreightkillo.queries import ApplicationQueryBackend, QueryService
from foreightkillo.signals import SignalPipeline, SignalStore


class ForeightService:
    def __init__(self, market_data: MarketDataProvider) -> None:
        self._market_data = market_data
        self._analyzer = SmartMoneyAnalyzer()
        self._strategies = TechnicalStrategyEngine()
        self._pipeline = SignalPipeline()
        self._signals = SignalStore()
        self._portfolio = PortfolioLedger()

    def queries(self) -> QueryService:
        return QueryService(ApplicationQueryBackend(self._signals, self._portfolio))

    def portfolio(self) -> dict[str, Any]:
        return {
            "positions": tuple(asdict(item) for item in self._portfolio.positions()),
            "closed_trades": tuple(asdict(item) for item in self._portfolio.closed_trades()),
            "performance": asdict(self._portfolio.performance()),
            "mode": "paper",
        }

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

    def strategy_research(self, symbol: str) -> dict[str, Any]:
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
        histories = tuple(
            (interval, self._market_data.get_history(instrument.instrument_id, interval, 100))
            for interval in (900, 3600, 14400)
        )
        candidates = self._strategies.evaluate(histories[1][1])
        assessment = self._strategies.assess_timeframes(histories)
        return {
            "instrument": symbol,
            "candidates": tuple(asdict(item) for item in candidates),
            "multi_timeframe": asdict(assessment),
            "execution_authority": False,
            "disclaimer": "Strategy research only; candidates are not trade instructions.",
        }

    def generate_signal(self, symbol: str, interval_seconds: int = 3600) -> dict[str, Any]:
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
        history = self._market_data.get_history(instrument.instrument_id, interval_seconds, 100)
        evidence = self._analyzer.analyze(history)
        signal = self._pipeline.create(
            instrument,
            self._market_data.get_quote(instrument.instrument_id),
            evidence,
            f"{interval_seconds}s",
            datetime.now(UTC),
        )
        self._signals.append(signal)
        return asdict(signal)

    def ranked_signals(self) -> tuple[dict[str, Any], ...]:
        active = self._signals.active_at(datetime.now(UTC))
        return tuple(asdict(item) for item in self._pipeline.rank(active))

    def prepare_paper_proposal(
        self,
        signal_id: str,
        account_id: str,
        equity: Decimal,
        risk_fraction: Decimal,
    ) -> dict[str, Any]:
        ranked = self._pipeline.rank(self._signals.active_at(datetime.now(UTC)))
        selected = next(
            (item for item in ranked if item.signal.identity.event_id == signal_id), None
        )
        if selected is None:
            raise KeyError(signal_id)
        proposal = self._pipeline.prepare_paper_proposal(
            selected, account_id, equity, risk_fraction, datetime.now(UTC)
        )
        return asdict(proposal)
