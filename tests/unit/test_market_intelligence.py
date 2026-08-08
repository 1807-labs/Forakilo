from decimal import Decimal

import pytest

from forakilo.application import ForeightService
from forakilo.intelligence.market import Opportunity, OpportunityRanker
from forakilo.marketdata.local import LocalMarketDataProvider


def test_analysis_is_explainable_and_paper_only() -> None:
    body = ForeightService(LocalMarketDataProvider()).analyze("EUR_USD")
    assert body["paper_only"] is True
    assert body["reasons"]
    assert "guaranteed" in body["disclaimer"]


def test_ranker_uses_cost_risk_and_uncertainty() -> None:
    strong = Opportunity(
        "gold",
        Decimal("0.6"),
        Decimal("2.8"),
        Decimal("0.1"),
        Decimal("1"),
        Decimal("1"),
        Decimal("0.1"),
        Decimal("0.1"),
    )
    weak = Opportunity(
        "crypto",
        Decimal("0.3"),
        Decimal("1.9"),
        Decimal("0.2"),
        Decimal("0.8"),
        Decimal("0.5"),
        Decimal("0.2"),
        Decimal("0.2"),
    )
    assert OpportunityRanker().rank((weak, strong))[0].signal_id == "gold"


def test_unknown_instrument_is_truthful() -> None:
    with pytest.raises(KeyError):
        ForeightService(LocalMarketDataProvider()).analyze("UNKNOWN")
