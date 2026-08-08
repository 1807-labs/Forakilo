from datetime import UTC, datetime, timedelta
from decimal import Decimal

from forakilo.brokers.interface import BrokerPosition
from forakilo.domain import InstrumentId, Side
from forakilo.execution import PaperOrder
from forakilo.portfolio import PortfolioLedger

NOW = datetime(2026, 8, 8, 12, tzinfo=UTC)


def _open(ledger: PortfolioLedger):
    order = PaperOrder("one", "hash", Decimal("100"), Decimal("2"))
    return ledger.open_from_fill(
        order,
        InstrumentId("local", "XAU_USD"),
        Side.BUY,
        NOW,
        "strategy-1",
        "signal-1",
        Decimal("1"),
    )


def test_position_mark_close_and_performance() -> None:
    ledger = PortfolioLedger()
    position = _open(ledger)
    assert ledger.mark(position.position_id, Decimal("105"), NOW).unrealized_pnl == Decimal("9")
    trade = ledger.close(
        position.position_id, Decimal("106"), NOW + timedelta(hours=1), Decimal("1")
    )
    assert trade.realized_pnl == Decimal("10")
    summary = ledger.performance()
    assert summary.realized_pnl == Decimal("10")
    assert summary.win_rate == Decimal("1")


def test_reconciliation_detects_and_clears_mismatch() -> None:
    ledger = PortfolioLedger()
    position = _open(ledger)
    assert not ledger.reconcile((), NOW).reconciled
    broker = BrokerPosition(
        position.position_id,
        position.instrument_id,
        position.side,
        position.quantity,
        position.average_entry,
        Decimal("0"),
        Decimal("10"),
    )
    assert ledger.reconcile((broker,), NOW).reconciled


def test_open_fill_is_idempotent() -> None:
    ledger = PortfolioLedger()
    first = _open(ledger)
    second = _open(ledger)
    assert first == second
    assert len(ledger.positions()) == 1
