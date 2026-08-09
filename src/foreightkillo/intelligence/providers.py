"""Provider-neutral language model adapter constrained to supplied evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol
from urllib.parse import urlparse


class LanguageTransport(Protocol):
    def post(
        self, endpoint: str, payload: dict[str, Any], headers: dict[str, str]
    ) -> dict[str, Any]: ...


@dataclass(frozen=True, slots=True)
class HttpLanguageProvider:
    endpoint: str
    model: str
    token: str = field(repr=False)
    transport: LanguageTransport = field(repr=False)
    allowed_domains: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        parsed = urlparse(self.endpoint)
        if parsed.scheme != "https" or parsed.hostname not in self.allowed_domains:
            raise ValueError("language endpoint must be HTTPS and allowlisted")
        if not self.model or len(self.token) < 12:
            raise ValueError("language provider model and secret are required")

    def explain(self, question: str, evidence: tuple[str, ...]) -> str:
        if not evidence:
            raise ValueError("language provider requires grounded evidence")
        bounded_evidence = tuple(item[:2000] for item in evidence[:10])
        response = self.transport.post(
            self.endpoint,
            {
                "model": self.model,
                "instructions": (
                    "Explain only from EVIDENCE. Do not invent prices, performance or facts. "
                    "Do not authorize or execute trades. State uncertainty clearly."
                ),
                "question": question[:2000],
                "evidence": bounded_evidence,
            },
            {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
        )
        text = response.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("language provider returned no usable explanation")
        return text[:8000]
