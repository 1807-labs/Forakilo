from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import pytest

from foreightkillo.bot.adapters.discord import DiscordAdapter
from foreightkillo.bot.adapters.http import HttpResponse
from foreightkillo.bot.adapters.telegram import TelegramAdapter
from foreightkillo.bot.config import BotSettings, DiscordConfig, TelegramConfig, redact
from foreightkillo.bot.contracts import BotDestination, BotProvider, DeliveryRequest
from foreightkillo.notifications.events import Visibility
from foreightkillo.notifications.projections import Notification, NotificationPriority


@dataclass
class FakeTransport:
    response: HttpResponse
    calls: list[tuple[str, dict[str, Any] | None, dict[str, str]]] = field(
        default_factory=lambda: list[tuple[str, dict[str, Any] | None, dict[str, str]]]()
    )

    def request(
        self, url: str, body: dict[str, Any] | None, headers: dict[str, str]
    ) -> HttpResponse:
        self.calls.append((url, body, headers))
        return self.response


NOW = datetime(2026, 7, 29, tzinfo=UTC)


def notification(body: str = "Evidence only.") -> Notification:
    return Notification(
        "m",
        "e",
        "signal",
        NotificationPriority.NORMAL,
        "Signal eligible",
        body,
        (("risk", "pending"),),
        NOW,
        None,
        Visibility.MEMBER,
        "installation",
        None,
        "m",
        True,
    )


def test_telegram_allowlist_formatting_and_rate_limit() -> None:
    transport = FakeTransport(HttpResponse(429, {}, 3))
    adapter = TelegramAdapter(TelegramConfig(True, "test-token", frozenset({"chat"})), transport)
    destination = BotDestination(BotProvider.TELEGRAM, "chat", "local")
    result = adapter.deliver(DeliveryRequest("r", destination, notification(), "i"))
    assert result.failure is not None and result.failure.retryable
    assert (
        "<b>PAPER ONLY</b>"
        in adapter.format_message(DeliveryRequest("r", destination, notification(), "i"))[0]
    )
    assert not adapter.validate_destination(BotDestination(BotProvider.TELEGRAM, "denied", "local"))


def test_telegram_long_messages_are_split() -> None:
    request = DeliveryRequest(
        "r",
        BotDestination(BotProvider.TELEGRAM, "chat", "local"),
        notification("x" * 9000),
        "i",
    )
    assert len(TelegramAdapter.format_message(request)) == 3


def test_discord_allowlists_embeds_and_permission_failure() -> None:
    transport = FakeTransport(HttpResponse(403, {}))
    adapter = DiscordAdapter(
        DiscordConfig(
            True,
            "test-token",
            "application",
            frozenset({"guild"}),
            frozenset({"channel"}),
        ),
        transport,
    )
    destination = BotDestination(BotProvider.DISCORD, "channel", "local", "guild")
    result = adapter.deliver(DeliveryRequest("r", destination, notification(), "i"))
    assert result.failure is not None and not result.failure.retryable
    payload = adapter.format_message(DeliveryRequest("r", destination, notification(), "i"))[0]
    assert payload["embeds"]
    assert not adapter.validate_destination(
        BotDestination(BotProvider.DISCORD, "channel", "local", "denied")
    )


def test_tokens_are_redacted_and_repr_hidden() -> None:
    token = "sensitive-" + "test-token"
    config = TelegramConfig(False, token)
    assert token not in repr(config)
    assert redact(f"failure {token}", (token,)) == "failure [REDACTED]"


def test_disabled_providers_do_not_require_or_read_tokens(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("FOREIGHTKILLO_TELEGRAM_ENABLED", "false")
    monkeypatch.setenv("FOREIGHTKILLO_DISCORD_ENABLED", "false")
    monkeypatch.setenv("FOREIGHTKILLO_TELEGRAM_BOT_TOKEN", "must-not-be-read")
    monkeypatch.setenv("FOREIGHTKILLO_DISCORD_BOT_TOKEN", "must-not-be-read")
    settings = BotSettings.from_environment()
    assert settings.telegram.token is None
    assert settings.discord.token is None
    TelegramConfig().validate()
    DiscordConfig().validate()


def test_for8killo_environment_names_take_precedence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("FOR8KILLO_INSTALLATION_ID", "new-name")
    monkeypatch.setenv("FOREIGHTKILLO_INSTALLATION_ID", "legacy-name")
    monkeypatch.setenv("FOR8KILLO_TELEGRAM_ENABLED", "false")
    monkeypatch.setenv("FOR8KILLO_DISCORD_ENABLED", "false")
    assert BotSettings.from_environment().installation_id == "new-name"
