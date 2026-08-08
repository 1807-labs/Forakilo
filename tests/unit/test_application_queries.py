from forakilo.portfolio import PortfolioLedger
from forakilo.queries import ApplicationQueryBackend, Availability, QueryService
from forakilo.signals import SignalStore


def test_application_queries_report_real_empty_state() -> None:
    service = QueryService(ApplicationQueryBackend(SignalStore(), PortfolioLedger()))
    positions = service.execute("ListPaperPositions")
    assert positions.state is Availability.AVAILABLE
    assert positions.summary == "0 open paper position(s)."
    health = service.execute("GetSystemHealth")
    assert health.state is Availability.AVAILABLE


def test_unimplemented_query_remains_truthful() -> None:
    service = QueryService(ApplicationQueryBackend(SignalStore(), PortfolioLedger()))
    result = service.execute("GetRiskStatus")
    assert result.state is Availability.NOT_AVAILABLE
