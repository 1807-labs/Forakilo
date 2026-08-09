"""Grounded conversational intelligence with local memory and cited research."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from foreightkillo.queries import Availability, QueryService


@dataclass(frozen=True, slots=True)
class ResearchDocument:
    document_id: str
    title: str
    source_url: str
    published_at: datetime | None
    retrieved_at: datetime
    content: str
    approved: bool


@dataclass(frozen=True, slots=True)
class Citation:
    document_id: str
    title: str
    source_url: str


@dataclass(frozen=True, slots=True)
class ConversationResponse:
    response_id: str
    text: str
    citations: tuple[Citation, ...]
    grounded: bool
    generated_at: datetime
    disclaimer: str = "Market research only; not a promise of returns or financial advice."


class LanguageProvider(Protocol):
    def explain(self, question: str, evidence: tuple[str, ...]) -> str: ...


class ResearchRepository:
    def __init__(self) -> None:
        self._documents: dict[str, ResearchDocument] = {}

    def add(self, document: ResearchDocument) -> None:
        if not document.approved:
            raise PermissionError("research source must be approved")
        if not document.source_url.startswith("https://"):
            raise ValueError("research source must use HTTPS")
        self._documents[document.document_id] = document

    def search(self, terms: tuple[str, ...], limit: int = 5) -> tuple[ResearchDocument, ...]:
        normalized = tuple(term.lower() for term in terms if len(term) > 2)
        scored: list[tuple[int, str, ResearchDocument]] = []
        for document in self._documents.values():
            haystack = f"{document.title} {document.content}".lower()
            score = sum(haystack.count(term) for term in normalized)
            if score:
                scored.append((score, document.document_id, document))
        return tuple(item[2] for item in sorted(scored, reverse=True)[:limit])


class SQLiteConversationMemory:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._path = path
        with self._connect() as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS conversation_turns (
                turn_id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL, role TEXT NOT NULL,
                content TEXT NOT NULL, created_at TEXT NOT NULL)"""
            )

    def append(self, conversation_id: str, role: str, content: str, now: datetime) -> None:
        if role not in {"user", "assistant"}:
            raise ValueError("unsupported conversation role")
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO conversation_turns VALUES (?, ?, ?, ?, ?)",
                (str(uuid4()), conversation_id, role, content[:4000], now.isoformat()),
            )

    def recent(self, conversation_id: str, limit: int = 10) -> tuple[tuple[str, str], ...]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT role, content FROM conversation_turns
                WHERE conversation_id = ? ORDER BY created_at DESC LIMIT ?""",
                (conversation_id, limit),
            ).fetchall()
        return tuple((str(row[0]), str(row[1])) for row in reversed(rows))

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path)


class ForeightConversation:
    def __init__(
        self,
        queries: QueryService,
        research: ResearchRepository,
        memory: SQLiteConversationMemory,
        language_provider: LanguageProvider | None = None,
    ) -> None:
        self._queries = queries
        self._research = research
        self._memory = memory
        self._language_provider = language_provider

    def ask(self, conversation_id: str, question: str) -> ConversationResponse:
        if not question.strip() or len(question) > 2000:
            raise ValueError("question must contain between 1 and 2000 characters")
        lowered = question.lower()
        forbidden = ("execute", "buy ", "sell ", "approve trade", "broker credential")
        now = datetime.now(UTC)
        self._memory.append(conversation_id, "user", question, now)
        if any(term in lowered for term in forbidden):
            text = "I cannot authorize or execute trades through conversation."
            response = ConversationResponse(str(uuid4()), text, (), True, now)
            self._memory.append(conversation_id, "assistant", text, now)
            return response
        query_name = self._intent(lowered)
        result = self._queries.execute(query_name) if query_name else None
        documents = self._research.search(tuple(lowered.split()))
        evidence = tuple(
            [result.summary] if result and result.state is Availability.AVAILABLE else []
        ) + tuple(document.content[:500] for document in documents)
        if not evidence:
            text = "I do not have verified local data or approved research to answer that yet."
            grounded = False
        elif self._language_provider:
            text = self._language_provider.explain(question, evidence)
            grounded = True
        else:
            text = " ".join(evidence)
            grounded = True
        citations = tuple(
            Citation(item.document_id, item.title, item.source_url) for item in documents
        )
        response = ConversationResponse(str(uuid4()), text, citations, grounded, now)
        self._memory.append(conversation_id, "assistant", text, now)
        return response

    @staticmethod
    def _intent(question: str) -> str | None:
        if "position" in question:
            return "ListPaperPositions"
        if "performance" in question or "p&l" in question:
            return "GetStrategyPerformance"
        if "signal" in question:
            return "ListRecentSignals"
        if "health" in question or "status" in question:
            return "GetSystemHealth"
        if "strategy" in question:
            return "ListStrategies"
        return None
