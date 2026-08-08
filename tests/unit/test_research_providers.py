from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from forakilo.intelligence import (
    FeedItem,
    HttpLanguageProvider,
    ResearchIngestionPolicy,
    ResearchIngestor,
    ResearchRepository,
)

NOW = datetime(2026, 8, 8, tzinfo=UTC)


@dataclass
class Feed:
    name: str
    items: tuple[FeedItem, ...]

    def fetch(self, since: datetime) -> tuple[FeedItem, ...]:
        return self.items


class Transport:
    def post(
        self, endpoint: str, payload: dict[str, Any], headers: dict[str, str]
    ) -> dict[str, Any]:
        assert payload["evidence"]
        assert headers["Authorization"].startswith("Bearer ")
        return {"text": "Evidence indicates uncertainty remains."}


def test_research_ingestion_enforces_domain_and_freshness() -> None:
    repository = ResearchRepository()
    ingestor = ResearchIngestor(
        repository, ResearchIngestionPolicy(frozenset({"approved.example"}))
    )
    feed = Feed(
        "macro",
        (
            FeedItem("ok", "Policy", "https://approved.example/a", NOW, "Verified policy."),
            FeedItem("bad", "Rumor", "https://untrusted.example/a", NOW, "Rumor."),
            FeedItem(
                "old",
                "Old",
                "https://approved.example/old",
                NOW - timedelta(days=8),
                "Old.",
            ),
        ),
    )
    report = ingestor.ingest(feed, NOW)
    assert report.accepted == 1 and report.rejected == 2
    assert len(repository.search(("policy",))) == 1


def test_language_provider_is_grounded_and_redacts_repr() -> None:
    token = "provider-" + "test-secret"
    provider = HttpLanguageProvider(
        "https://language.example/respond",
        "buyer-model",
        token,
        Transport(),
        frozenset({"language.example"}),
    )
    assert token not in repr(provider)
    assert "uncertainty" in provider.explain("Explain", ("verified evidence",))
    with pytest.raises(ValueError):
        provider.explain("Explain", ())


def test_language_provider_rejects_unapproved_endpoint() -> None:
    with pytest.raises(ValueError):
        HttpLanguageProvider("http://untrusted.example", "model", "long-enough-secret", Transport())
