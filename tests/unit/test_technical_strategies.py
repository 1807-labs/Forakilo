from forakilo.intelligence.strategies import TechnicalStrategyEngine
from forakilo.marketdata.local import LocalMarketDataProvider


def test_strategy_suite_is_explainable_and_covers_brief_strategies() -> None:
    provider = LocalMarketDataProvider(seed=11)
    instrument = provider.discover_instruments()[0].instrument_id
    candles = provider.get_history(instrument, 3600, 100)
    candidates = TechnicalStrategyEngine().evaluate(candles)
    assert {item.strategy for item in candidates} == {
        "trend-following",
        "momentum",
        "volatility-breakout",
        "mean-reversion",
        "harmonic",
    }
    assert all(item.reasons and 0 <= item.confidence <= 1 for item in candidates)


def test_multi_timeframe_assessment_reports_consensus() -> None:
    provider = LocalMarketDataProvider(seed=11)
    instrument = provider.discover_instruments()[0].instrument_id
    histories = tuple(
        (interval, provider.get_history(instrument, interval, 100))
        for interval in (900, 3600, 14400)
    )
    assessment = TechnicalStrategyEngine().assess_timeframes(histories)
    assert len(assessment.timeframes) == 3
    assert assessment.agreement >= 0.5
    assert assessment.reasons
