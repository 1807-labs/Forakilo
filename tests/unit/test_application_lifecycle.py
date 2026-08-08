from decimal import Decimal

from forakilo.application import ForeightService
from forakilo.marketdata.local import LocalMarketDataProvider


def test_application_generates_and_ranks_complete_signals() -> None:
    service = ForeightService(LocalMarketDataProvider(seed=4))
    signal = service.generate_signal("EUR_USD")
    assert signal["instrument_id"]["symbol"] == "EUR_USD"
    assert signal["entry_zone"] and signal["stop_price"] and signal["target_prices"]
    ranked = service.ranked_signals()
    if signal["status"] == "eligible":
        assert ranked


def test_application_proposal_never_creates_live_mode() -> None:
    service = ForeightService(LocalMarketDataProvider(seed=4))
    signal = service.generate_signal("XAU_USD")
    if signal["status"] != "eligible":
        return
    proposal = service.prepare_paper_proposal(
        signal["identity"]["event_id"], "paper", Decimal("10000"), Decimal("0.01")
    )
    assert proposal["proposal"]["mode"] == "paper"
    assert proposal["authorization_required"] is True
