"""Discord channel adapter using minimal bot permissions."""

from __future__ import annotations

from dataclasses import dataclass

from ..config import DiscordConfig
from ..contracts import (
    BotDestination,
    BotHealthStatus,
    BotProvider,
    DeliveryFailure,
    DeliveryRequest,
    DeliveryResult,
)
from .http import HttpTransport


@dataclass(slots=True)
class DiscordAdapter:
    config: DiscordConfig
    transport: HttpTransport
    stopped: bool = False

    def __post_init__(self) -> None:
        self.config.validate()

    @property
    def provider(self) -> BotProvider:
        return BotProvider.DISCORD

    def validate_destination(self, destination: BotDestination) -> bool:
        return (
            self.config.enabled
            and destination.provider is self.provider
            and destination.destination_id in self.config.allowed_channel_ids
            and destination.guild_id in self.config.allowed_guild_ids
        )

    @staticmethod
    def format_message(request: DeliveryRequest) -> tuple[dict[str, object], ...]:
        notification = request.notification
        description = notification.body + ("\n**PAPER ONLY**" if notification.paper_only else "")
        chunks = tuple(
            description[index : index + 2000] for index in range(0, len(description), 2000)
        )
        return tuple(
            {
                "content": chunk,
                "embeds": [
                    {
                        "title": notification.title[:256],
                        "fields": [
                            {"name": name[:256], "value": value[:1024], "inline": True}
                            for name, value in notification.fields[:25]
                        ],
                    }
                ],
            }
            for chunk in chunks
        )

    def deliver(self, request: DeliveryRequest) -> DeliveryResult:
        if self.stopped:
            return self._failure(request, "stopped", False)
        if not self.validate_destination(request.destination):
            return self._failure(request, "invalid_channel", False)
        message_id: str | None = None
        for payload in self.format_message(request):
            response = self.transport.request(
                "https://discord.com/api/v10/channels/"
                f"{request.destination.destination_id}/messages",
                payload,
                {
                    "Authorization": f"Bot {self.config.token}",
                    "Content-Type": "application/json",
                },
            )
            if response.status == 429:
                return DeliveryResult(
                    request.request_id,
                    False,
                    None,
                    DeliveryFailure(
                        "rate_limit", True, "provider rate limit", response.retry_after_seconds
                    ),
                )
            if response.status >= 500:
                return self._failure(request, "transient_network", True)
            if response.status in {401, 403}:
                return self._failure(request, "missing_permission_or_removed", False)
            if response.status >= 400:
                return self._failure(request, "invalid_channel", False)
            message_id = str(response.body.get("id", "accepted"))
        return DeliveryResult(request.request_id, True, message_id, None)

    def health(self) -> BotHealthStatus:
        if not self.config.enabled:
            return BotHealthStatus(self.provider, False, True, "disabled")
        if self.stopped:
            return BotHealthStatus(self.provider, True, False, "stopped")
        response = self.transport.request(
            "https://discord.com/api/v10/users/@me",
            None,
            {"Authorization": f"Bot {self.config.token}"},
        )
        return BotHealthStatus(self.provider, True, response.status == 200, "verified")

    def shutdown(self) -> None:
        self.stopped = True

    @staticmethod
    def _failure(request: DeliveryRequest, kind: str, retryable: bool) -> DeliveryResult:
        return DeliveryResult(
            request.request_id, False, None, DeliveryFailure(kind, retryable, kind)
        )
