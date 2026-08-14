"""Telegram Bot API adapter with allowlists and normalized failures."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape

from ..config import TelegramConfig
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
class TelegramAdapter:
    config: TelegramConfig
    transport: HttpTransport
    stopped: bool = False

    def __post_init__(self) -> None:
        self.config.validate()

    @property
    def provider(self) -> BotProvider:
        return BotProvider.TELEGRAM

    def validate_destination(self, destination: BotDestination) -> bool:
        return (
            self.config.enabled
            and destination.provider is self.provider
            and destination.destination_id in self.config.allowed_chat_ids
        )

    @staticmethod
    def format_message(request: DeliveryRequest) -> tuple[str, ...]:
        notification = request.notification
        fields = "\n".join(f"<b>{escape(k)}</b>: {escape(v)}" for k, v in notification.fields)
        paper = "\n<b>PAPER ONLY</b>" if notification.paper_only else ""
        text = f"<b>{escape(notification.title)}</b>\n{escape(notification.body)}{paper}" + (
            f"\n{fields}" if fields else ""
        )
        return tuple(text[index : index + 4096] for index in range(0, len(text), 4096))

    def deliver(self, request: DeliveryRequest) -> DeliveryResult:
        if self.stopped:
            return self._failure(request, "stopped", False)
        if not self.validate_destination(request.destination):
            return self._failure(request, "invalid_chat", False)
        message_id: str | None = None
        for chunk in self.format_message(request):
            response = self.transport.request(
                f"https://api.telegram.org/bot{self.config.token}/sendMessage",
                {
                    "chat_id": request.destination.destination_id,
                    "text": chunk,
                    "parse_mode": "HTML",
                },
                {"Content-Type": "application/json"},
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
                return self._failure(request, "blocked_or_unauthorized", False)
            if response.status >= 400:
                return self._failure(request, "invalid_chat", False)
            message_id = str(response.body.get("result", {}).get("message_id", "accepted"))
        return DeliveryResult(request.request_id, True, message_id, None)

    def health(self) -> BotHealthStatus:
        if not self.config.enabled:
            return BotHealthStatus(self.provider, False, True, "disabled")
        if self.stopped:
            return BotHealthStatus(self.provider, True, False, "stopped")
        response = self.transport.request(
            f"https://api.telegram.org/bot{self.config.token}/getMe", None, {}
        )
        return BotHealthStatus(self.provider, True, response.status == 200, "verified")

    def shutdown(self) -> None:
        self.stopped = True

    @staticmethod
    def _failure(request: DeliveryRequest, kind: str, retryable: bool) -> DeliveryResult:
        return DeliveryResult(
            request.request_id, False, None, DeliveryFailure(kind, retryable, kind)
        )
