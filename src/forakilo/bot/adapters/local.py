"""Deterministic local provider for unit and integration tests."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..contracts import (
    BotDestination,
    BotHealthStatus,
    BotProvider,
    DeliveryRequest,
    DeliveryResult,
)


@dataclass(slots=True)
class LocalBotAdapter:
    allowed_destinations: frozenset[str]
    delivered: list[DeliveryRequest] = field(default_factory=lambda: list[DeliveryRequest]())
    stopped: bool = False

    @property
    def provider(self) -> BotProvider:
        return BotProvider.LOCAL

    def validate_destination(self, destination: BotDestination) -> bool:
        return (
            destination.provider is self.provider
            and destination.destination_id in self.allowed_destinations
        )

    def deliver(self, request: DeliveryRequest) -> DeliveryResult:
        if self.stopped:
            raise RuntimeError("adapter is stopped")
        self.delivered.append(request)
        return DeliveryResult(request.request_id, True, f"local-{len(self.delivered)}", None)

    def health(self) -> BotHealthStatus:
        return BotHealthStatus(self.provider, True, not self.stopped, "local")

    def shutdown(self) -> None:
        self.stopped = True
