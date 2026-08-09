from datetime import UTC, datetime
from decimal import Decimal

import pytest

from foreightkillo.domain import EventIdentity
from foreightkillo.intelligence.annotation import (
    AnnotationProposal,
    AnnotationSource,
    AnnotationStore,
    ReviewDecision,
)

NOW = datetime(2026, 7, 29, tzinfo=UTC)


def proposal(event_id: str, label: str, source: AnnotationSource) -> AnnotationProposal:
    identity = EventIdentity(
        event_id=event_id,
        event_time=NOW,
        known_time=NOW,
        recorded_time=NOW,
        provenance=source,
        correlation_id="experiment-1",
        causation_id=None,
        configuration_version="annotation-v1",
    )
    return AnnotationProposal(
        identity=identity,
        dataset_version="dataset-1",
        subject_id="window-1",
        label_schema_version="labels-v1",
        label=label,
        source=source,
        confidence=Decimal("0.8"),
        evidence=("fixture",),
    )


def test_ai_proposal_does_not_overwrite_human_review() -> None:
    store = AnnotationStore()
    proposed = proposal("p1", "risk_on", AnnotationSource.OPENAI_PROPOSAL)
    store.propose(proposed)
    store.review("p1", ReviewDecision.REJECTED, "human-1", NOW, "unsupported")
    with pytest.raises(ValueError):
        store.review("p1", ReviewDecision.ACCEPTED, "human-2", NOW, "overwrite")


def test_disagreement_is_preserved() -> None:
    store = AnnotationStore()
    store.propose(proposal("p1", "risk_on", AnnotationSource.DETERMINISTIC))
    store.propose(proposal("p2", "risk_off", AnnotationSource.LOCAL_MODEL))
    assert len(store.disagreements("window-1")) == 2
