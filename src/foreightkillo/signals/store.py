"""In-memory immutable signal projection for deterministic tests and local MVP."""

from __future__ import annotations

from datetime import datetime

from foreightkillo.domain import Signal


class SignalStore:
    def __init__(self) -> None:
        self._signals: dict[str, Signal] = {}

    def append(self, signal: Signal) -> bool:
        existing = self._signals.get(signal.identity.event_id)
        if existing is not None and existing != signal:
            raise ValueError("signal identity collision")
        if existing is not None:
            return False
        self._signals[signal.identity.event_id] = signal
        return True

    def active_at(self, known_time: datetime) -> tuple[Signal, ...]:
        return tuple(
            signal
            for signal in self._signals.values()
            if signal.identity.known_time <= known_time < signal.expires_at
        )
