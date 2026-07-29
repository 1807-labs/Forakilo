"""Provider-neutral contracts migrated from a private annotation source."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from forakilo.domain import EventIdentity


class AnnotationSource(StrEnum):
    DETERMINISTIC = "deterministic"
    LOCAL_MODEL = "local_model"
    OPENAI_PROPOSAL = "openai_proposal"
    GEMINI_PROPOSAL = "gemini_proposal"


class ReviewDecision(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


@dataclass(frozen=True, slots=True)
class AnnotationProposal:
    identity: EventIdentity
    dataset_version: str
    subject_id: str
    label_schema_version: str
    label: str
    source: AnnotationSource
    confidence: Decimal
    evidence: tuple[str, ...]
    prompt_version: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if not Decimal("0") <= self.confidence <= Decimal("1"):
            raise ValueError("confidence must be between zero and one")
        if self.input_tokens < 0 or self.output_tokens < 0 or self.cost < 0:
            raise ValueError("usage accounting cannot be negative")
        if not self.evidence:
            raise ValueError("annotation evidence is required")


@dataclass(frozen=True, slots=True)
class AnnotationRecord:
    proposal: AnnotationProposal
    decision: ReviewDecision
    reviewer_id: str | None
    reviewed_at: datetime | None
    review_reason: str | None

    def __post_init__(self) -> None:
        if self.decision is ReviewDecision.PENDING:
            if self.reviewer_id is not None or self.reviewed_at is not None:
                raise ValueError("pending annotations cannot carry a review")
        elif not self.reviewer_id or self.reviewed_at is None:
            raise ValueError("completed review requires reviewer and time")
