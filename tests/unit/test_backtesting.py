from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from foreightkillo.backtesting import BacktestConfig, BacktestEngine
from foreightkillo.domain import Candle, EventIdentity, InstrumentId, MarketDataProvenance, Side


def _candles(count: int = 35) -> tuple[Candle, ...]:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    instrument = InstrumentId("test", "EUR_USD")
    result: list[Candle] = []
    for index in range(count):
        time = start + timedelta(hours=index)
        price = Decimal("100") + Decimal(index)
        identity = EventIdentity(str(index), time, time, time, "test", "run", None, "1")
        provenance = MarketDataProvenance("test", str(index), str(index))
        result.append(
            Candle(
                identity,
                instrument,
                3600,
                price,
                price + 1,
                price - 1,
                price + Decimal("0.5"),
                Decimal("1"),
                True,
                provenance,
            )
        )
    return tuple(result)


@dataclass
class RecordingStrategy:
    lengths: list[int]

    def decide(self, history: tuple[Candle, ...]) -> Side:
        self.lengths.append(len(history))
        return Side.BUY


def test_backtest_uses_only_prior_history_and_charges_costs() -> None:
    strategy = RecordingStrategy([])
    report = BacktestEngine().run(_candles(), strategy, BacktestConfig(holding_bars=2))
    assert strategy.lengths[0] == 20
    assert all(
        trade.entry_time > _candles()[length - 1].identity.event_time
        for trade, length in zip(report.trades, strategy.lengths, strict=True)
    )
    assert all(trade.costs > 0 and trade.net_pnl < trade.gross_pnl for trade in report.trades)
    assert report.final_equity == report.initial_equity + report.net_pnl
    assert "simulated" in report.assumptions[-1]


def test_backtest_rejects_insufficient_or_incomplete_data() -> None:
    strategy = RecordingStrategy([])
    try:
        BacktestEngine().run(_candles(10), strategy, BacktestConfig())
    except ValueError as error:
        assert "at least" in str(error)
    else:
        raise AssertionError("insufficient history should be rejected")
