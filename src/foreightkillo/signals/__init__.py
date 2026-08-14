"""Auditable signal handling and paper-proposal preparation."""

from .pipeline import PaperProposalView, RankedSignal, SignalPipeline, StrategyPolicy
from .store import SignalStore

__all__ = [
    "PaperProposalView",
    "RankedSignal",
    "SignalPipeline",
    "SignalStore",
    "StrategyPolicy",
]
