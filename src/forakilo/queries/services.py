"""Query DTOs used by every bot provider."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class Availability(StrEnum):
    AVAILABLE = "available"
    NOT_AVAILABLE = "not_available"
    NOT_IMPLEMENTED = "not_implemented"


@dataclass(frozen=True, slots=True)
class QueryResult:
    state: Availability
    summary: str
    items: tuple[tuple[str, str], ...] = ()
    sensitive: bool = False


class QueryBackend(Protocol):
    def execute(self, query: str, arguments: tuple[str, ...]) -> QueryResult: ...


class QueryService:
    """Explicitly truthful default until product stores are implemented."""

    _KNOWN = frozenset(
        {
            "ListRecentSignals",
            "GetSignalDetails",
            "GetRiskStatus",
            "GetPaperAccountStatus",
            "ListPaperPositions",
            "ListStrategies",
            "GetStrategySummary",
            "GetStrategyPerformance",
            "ListModelVersions",
            "GetModelHealth",
            "GetSystemHealth",
        }
    )

    def execute(self, query: str, arguments: tuple[str, ...] = ()) -> QueryResult:
        if query not in self._KNOWN:
            return QueryResult(Availability.NOT_IMPLEMENTED, "Unknown query.")
        return QueryResult(
            Availability.NOT_AVAILABLE,
            f"{query} is not available in this installation.",
        )
