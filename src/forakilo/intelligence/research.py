"""Policy-controlled ingestion for approved news, macro, and sentiment sources."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Protocol
from urllib.parse import urlparse

from .conversation import ResearchDocument, ResearchRepository


@dataclass(frozen=True, slots=True)
class FeedItem:
    external_id: str
    title: str
    url: str
    published_at: datetime
    content: str


class ResearchFeed(Protocol):
    @property
    def name(self) -> str: ...

    def fetch(self, since: datetime) -> tuple[FeedItem, ...]: ...


@dataclass(frozen=True, slots=True)
class ResearchIngestionPolicy:
    allowed_domains: frozenset[str]
    maximum_age: timedelta = timedelta(days=7)
    maximum_content_characters: int = 20_000


@dataclass(frozen=True, slots=True)
class IngestionReport:
    accepted: int
    rejected: int
    reasons: tuple[str, ...]


class ResearchIngestor:
    def __init__(self, repository: ResearchRepository, policy: ResearchIngestionPolicy) -> None:
        self._repository = repository
        self._policy = policy

    def ingest(self, feed: ResearchFeed, now: datetime) -> IngestionReport:
        accepted = 0
        rejected = 0
        reasons: list[str] = []
        since = now - self._policy.maximum_age
        for item in feed.fetch(since):
            domain = (urlparse(item.url).hostname or "").lower()
            reason: str | None = None
            if domain not in self._policy.allowed_domains:
                reason = "domain_not_allowlisted"
            elif item.published_at.tzinfo is None or item.published_at.utcoffset() is None:
                reason = "timestamp_not_aware"
            elif item.published_at.astimezone(UTC) < since.astimezone(UTC):
                reason = "source_stale"
            elif not item.content.strip():
                reason = "content_empty"
            if reason:
                rejected += 1
                reasons.append(f"{item.external_id}:{reason}")
                continue
            self._repository.add(
                ResearchDocument(
                    f"{feed.name}:{item.external_id}",
                    item.title[:300],
                    item.url,
                    item.published_at,
                    now,
                    item.content[: self._policy.maximum_content_characters],
                    True,
                )
            )
            accepted += 1
        return IngestionReport(accepted, rejected, tuple(reasons))
