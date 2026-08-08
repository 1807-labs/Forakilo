from decimal import Decimal
from pathlib import Path

import pytest

from forakilo.models import ModelRegistry, ValidationEvidence


def _evidence(approved: bool = True) -> ValidationEvidence:
    return ValidationEvidence(
        "dataset-v1", "backtest-v1", 100, Decimal("0.08"), Decimal("0.05"), approved, "reviewer"
    )


def test_registry_requires_approved_evidence_and_human_promotion(tmp_path: Path) -> None:
    registry = ModelRegistry(tmp_path / "models.sqlite3")
    candidate = registry.register("strategy", "a" * 64, _evidence(False))
    with pytest.raises(PermissionError):
        registry.promote(candidate.version_id, "owner", "candidate not approved")
    validated = registry.register("strategy", "b" * 64, _evidence())
    active = registry.promote(validated.version_id, "owner", "approved release rehearsal")
    assert active.status == "active"
    assert registry.promotions()[0].actor == "owner"


def test_registry_keeps_only_one_active_version_per_strategy(tmp_path: Path) -> None:
    registry = ModelRegistry(tmp_path / "models.sqlite3")
    first = registry.register("strategy", "a" * 64, _evidence())
    second = registry.register("strategy", "b" * 64, _evidence())
    registry.promote(first.version_id, "owner", "first approved version")
    registry.promote(second.version_id, "owner", "second approved version")
    versions = {item.version_id: item for item in registry.list("strategy")}
    assert versions[first.version_id].status == "validated"
    assert versions[second.version_id].status == "active"
