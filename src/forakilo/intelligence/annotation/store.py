"""Append-only annotation projection that preserves disagreement."""

from __future__ import annotations

from datetime import datetime

from .contracts import AnnotationProposal, AnnotationRecord, ReviewDecision


class AnnotationStore:
    def __init__(self) -> None:
        self._records: dict[str, AnnotationRecord] = {}

    def propose(self, proposal: AnnotationProposal) -> AnnotationRecord:
        existing = self._records.get(proposal.identity.event_id)
        if existing is not None and existing.proposal != proposal:
            raise ValueError("annotation identity collision")
        if existing is not None:
            return existing
        record = AnnotationRecord(proposal, ReviewDecision.PENDING, None, None, None)
        self._records[proposal.identity.event_id] = record
        return record

    def review(
        self,
        proposal_id: str,
        decision: ReviewDecision,
        reviewer_id: str,
        reviewed_at: datetime,
        reason: str,
    ) -> AnnotationRecord:
        if decision is ReviewDecision.PENDING:
            raise ValueError("review must be a final decision")
        existing = self._records[proposal_id]
        if existing.decision is not ReviewDecision.PENDING:
            raise ValueError("review decisions are immutable")
        reviewed = AnnotationRecord(existing.proposal, decision, reviewer_id, reviewed_at, reason)
        self._records[proposal_id] = reviewed
        return reviewed

    def disagreements(self, subject_id: str) -> tuple[AnnotationRecord, ...]:
        records = tuple(
            record for record in self._records.values() if record.proposal.subject_id == subject_id
        )
        return records if len({record.proposal.label for record in records}) > 1 else ()
