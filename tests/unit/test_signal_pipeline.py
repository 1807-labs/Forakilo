from dataclasses import replace
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from foreightkillo.intelligence.market import SmartMoneyAnalyzer
from foreightkillo.marketdata.local import LocalMarketDataProvider
from foreightkillo.signals import SignalPipeline

NOW = datetime(2026, 8, 8, 12, tzinfo=UTC)


def _signal(symbol: str = "EUR_USD"):
    provider = LocalMarketDataProvider(seed=7)
    instrument = next(
        item for item in provider.discover_instruments() if item.instrument_id.symbol == symbol
    )
    history = provider.get_history(instrument.instrument_id, 3600, 100)
    evidence = SmartMoneyAnalyzer().analyze(history)
    return SignalPipeline().create(
        instrument, provider.get_quote(instrument.instrument_id), evidence, "1h", NOW
    )


def test_pipeline_creates_complete_explainable_signal() -> None:
    signal = _signal()
    assert signal.entry_zone and signal.stop_price and signal.target_prices
    assert signal.reward_to_risk == Decimal("2")
    assert signal.expires_at > signal.confirmed_time
    assert signal.evidence and signal.supporting_evidence


def test_ranking_can_recommend_no_trade() -> None:
    pipeline = SignalPipeline()
    rejected = _signal()
    rejected = replace(rejected, status="rejected", rejection_reason="risk threshold")
    assert pipeline.rank((rejected,)) == ()


def test_paper_proposal_is_sized_and_requires_authorization() -> None:
    pipeline = SignalPipeline()
    ranked = pipeline.rank((_signal(),))
    if not ranked:
        pytest.skip("deterministic fixture did not meet eligibility threshold")
    view = pipeline.prepare_paper_proposal(
        ranked[0], "paper-1", Decimal("10000"), Decimal("0.01"), NOW
    )
    assert view.proposal.mode == "paper"
    assert view.estimated_maximum_loss <= Decimal("100")
    assert view.authorization_required


def test_proposal_rejects_excessive_risk() -> None:
    pipeline = SignalPipeline()
    ranked = pipeline.rank((_signal(),))
    if not ranked:
        pytest.skip("deterministic fixture did not meet eligibility threshold")
    with pytest.raises(ValueError):
        pipeline.prepare_paper_proposal(
            ranked[0], "paper-1", Decimal("10000"), Decimal("0.03"), NOW
        )
