from datetime import UTC, datetime
from pathlib import Path

from forakilo.intelligence import (
    ForeightConversation,
    ResearchDocument,
    ResearchRepository,
    SQLiteConversationMemory,
)
from forakilo.portfolio import PortfolioLedger
from forakilo.queries import ApplicationQueryBackend, QueryService
from forakilo.signals import SignalStore


def _conversation(tmp_path: Path) -> ForeightConversation:
    repository = ResearchRepository()
    repository.add(
        ResearchDocument(
            "macro-1",
            "Central bank policy",
            "https://example.test/policy",
            None,
            datetime(2026, 8, 8, tzinfo=UTC),
            "Interest-rate policy can affect currency valuation and volatility.",
            True,
        )
    )
    queries = QueryService(ApplicationQueryBackend(SignalStore(), PortfolioLedger()))
    return ForeightConversation(
        queries, repository, SQLiteConversationMemory(tmp_path / "conversation.sqlite")
    )


def test_conversation_uses_verified_queries_and_memory(tmp_path: Path) -> None:
    conversation = _conversation(tmp_path)
    response = conversation.ask("one", "What is the system health status?")
    assert response.grounded
    assert "healthy" in response.text


def test_research_answer_has_citation(tmp_path: Path) -> None:
    response = _conversation(tmp_path).ask("one", "How can interest rate policy affect currency?")
    assert response.grounded
    assert response.citations[0].document_id == "macro-1"


def test_conversation_cannot_execute_or_accept_credentials(tmp_path: Path) -> None:
    conversation = _conversation(tmp_path)
    for question in ("Execute this trade", "Store my broker credential"):
        assert "cannot authorize or execute" in conversation.ask("one", question).text


def test_unverified_question_is_truthfully_unsupported(tmp_path: Path) -> None:
    response = _conversation(tmp_path).ask("one", "Tell me something unknowable")
    assert not response.grounded
