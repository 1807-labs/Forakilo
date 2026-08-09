"""Query backend over the local signal, portfolio, and provider projections."""

from __future__ import annotations

from datetime import UTC, datetime

from foreightkillo.portfolio import PortfolioLedger
from foreightkillo.signals import SignalStore

from .services import Availability, QueryResult


class ApplicationQueryBackend:
    def __init__(self, signals: SignalStore, portfolio: PortfolioLedger) -> None:
        self._signals = signals
        self._portfolio = portfolio

    def execute(self, query: str, arguments: tuple[str, ...]) -> QueryResult:
        if query == "ListRecentSignals":
            signals = self._signals.active_at(datetime.now(UTC))
            return QueryResult(
                Availability.AVAILABLE,
                f"{len(signals)} active signal(s).",
                tuple((item.identity.event_id, item.status) for item in signals),
            )
        if query == "GetSignalDetails":
            if not arguments:
                return QueryResult(Availability.NOT_AVAILABLE, "Signal identifier is required.")
            match = next(
                (
                    item
                    for item in self._signals.active_at(datetime.now(UTC))
                    if item.identity.event_id == arguments[0]
                ),
                None,
            )
            if match is None:
                return QueryResult(Availability.NOT_AVAILABLE, "Signal was not found or expired.")
            return QueryResult(
                Availability.AVAILABLE,
                f"{match.instrument_id.symbol} {match.side.value}; {match.status}.",
                (
                    ("timeframe", match.timeframe),
                    ("regime", match.market_regime),
                    ("expiry", match.expires_at.isoformat()),
                ),
            )
        if query == "ListPaperPositions":
            positions = self._portfolio.positions()
            return QueryResult(
                Availability.AVAILABLE,
                f"{len(positions)} open paper position(s).",
                tuple(
                    (item.position_id, f"{item.instrument_id.symbol} {item.unrealized_pnl}")
                    for item in positions
                ),
                True,
            )
        if query in {"GetPaperAccountStatus", "GetStrategyPerformance"}:
            performance = self._portfolio.performance()
            return QueryResult(
                Availability.AVAILABLE,
                f"Paper realized P&L {performance.realized_pnl}; "
                f"unrealized P&L {performance.unrealized_pnl}.",
                (("closed_trades", str(performance.closed_trades)),),
                True,
            )
        if query == "GetSystemHealth":
            return QueryResult(Availability.AVAILABLE, "For8killo local runtime is healthy.")
        if query == "ListStrategies":
            return QueryResult(
                Availability.AVAILABLE,
                "1 validated local strategy.",
                (("foreight-market-structure", "1.0.0"),),
            )
        if query == "GetStrategySummary":
            return QueryResult(
                Availability.AVAILABLE,
                "Foreight market structure combines regime, liquidity and imbalance evidence.",
            )
        if query == "ListModelVersions":
            return QueryResult(
                Availability.AVAILABLE,
                "Deterministic scorer active; trained ML model not installed.",
                (("deterministic", "1.0.0"),),
            )
        return QueryResult(Availability.NOT_AVAILABLE, f"{query} has no local data yet.")
