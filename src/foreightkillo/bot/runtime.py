"""Standalone provider ingress and lifecycle coordination."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from typing import Any, cast

from foreightkillo.notifications.events import Visibility
from foreightkillo.notifications.projections import Notification, NotificationPriority

from .adapters.discord import DiscordAdapter
from .adapters.http import HttpTransport
from .adapters.telegram import TelegramAdapter
from .commands import parse_command
from .contracts import (
    BotCommandContext,
    BotDestination,
    BotIdentity,
    BotProvider,
    BotRole,
    DeliveryRequest,
)
from .gateway import BotGateway


class RuntimeState(StrEnum):
    DISABLED = "disabled"
    STARTING = "starting"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    STOPPED = "stopped"


@dataclass(frozen=True, slots=True)
class RuntimeHealth:
    provider: BotProvider
    state: RuntimeState
    detail: str
    last_success_at: datetime | None = None


@dataclass(slots=True)
class OffsetStore:
    path: Path | None = None
    _offset: int = 0

    def load(self) -> int:
        if self.path and self.path.exists():
            value = self.path.read_text(encoding="utf-8").strip()
            self._offset = int(value or "0")
        return self._offset

    def save(self, offset: int) -> None:
        self._offset = max(self._offset, offset)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.path.with_suffix(".tmp")
            temporary.write_text(str(self._offset), encoding="utf-8")
            temporary.replace(self.path)


@dataclass(slots=True)
class TelegramPollingRuntime:
    adapter: TelegramAdapter
    transport: HttpTransport
    gateway: BotGateway
    installation_id: str
    offsets: OffsetStore
    stopped: bool = False
    last_success_at: datetime | None = None

    def poll_once(self) -> int:
        if self.stopped or not self.adapter.config.enabled:
            return 0
        offset = self.offsets.load()
        response = self.transport.request(
            f"https://api.telegram.org/bot{self.adapter.config.token}/getUpdates",
            {"offset": offset, "timeout": self.adapter.config.polling_timeout_seconds},
            {"Content-Type": "application/json"},
        )
        if response.status != 200:
            return 0
        raw_updates = response.body.get("result", [])
        if not isinstance(raw_updates, list):
            return 0
        handled = 0
        for raw in cast("list[object]", raw_updates):
            if not isinstance(raw, dict):
                continue
            update = cast("dict[str, Any]", raw)
            update_id = update.get("update_id")
            if not isinstance(update_id, int) or update_id < offset:
                continue
            self.offsets.save(update_id + 1)
            if self._handle(update):
                handled += 1
        self.last_success_at = datetime.now(UTC)
        return handled

    def _handle(self, update: dict[str, Any]) -> bool:
        message = update.get("message") or update.get("channel_post")
        if not isinstance(message, dict):
            return False
        typed = cast("dict[str, Any]", message)
        text = typed.get("text")
        chat = typed.get("chat")
        actor = typed.get("from", {})
        if not isinstance(text, str) or not text.startswith("/") or not isinstance(chat, dict):
            return False
        chat_id = str(cast("dict[str, Any]", chat).get("id", ""))
        allowed = self.adapter.config.command_chat_ids or self.adapter.config.allowed_chat_ids
        if chat_id not in allowed:
            return False
        actor_id = str(cast("dict[str, Any]", actor).get("id", "channel"))
        command = parse_command(text, f"telegram-{update['update_id']}")
        destination = BotDestination(BotProvider.TELEGRAM, chat_id, self.installation_id)
        context = BotCommandContext(
            BotIdentity(
                BotProvider.TELEGRAM, sha256(actor_id.encode()).hexdigest(), BotRole.OPERATOR
            ),
            destination,
            command.command_id,
            datetime.now(UTC),
        )
        result = self.gateway.handle(command, context)
        now = datetime.now(UTC)
        notification = Notification(
            result.command_id,
            result.command_id,
            "command",
            NotificationPriority.NORMAL,
            "Foreight",
            result.text,
            (),
            now,
            None,
            Visibility.OPERATOR,
            "installation",
            None,
            result.command_id,
            True,
        )
        self.gateway.deliver(
            DeliveryRequest(result.command_id, destination, notification, result.command_id)
        )
        return True

    def health(self) -> RuntimeHealth:
        if not self.adapter.config.enabled:
            return RuntimeHealth(BotProvider.TELEGRAM, RuntimeState.DISABLED, "disabled")
        state = RuntimeState.STOPPED if self.stopped else RuntimeState.HEALTHY
        return RuntimeHealth(BotProvider.TELEGRAM, state, state, self.last_success_at)

    def shutdown(self) -> None:
        self.stopped = True
        self.adapter.shutdown()


READ_ONLY_SLASH_COMMANDS = (
    "help",
    "status",
    "signals",
    "signal",
    "risk",
    "paper",
    "positions",
    "strategies",
    "strategy",
    "performance",
    "models",
    "health",
)


@dataclass(slots=True)
class DiscordInteractionRuntime:
    adapter: DiscordAdapter
    transport: HttpTransport
    gateway: BotGateway
    installation_id: str
    stopped: bool = False

    def synchronize(self) -> bool:
        config = self.adapter.config
        if not config.enabled or not config.command_sync_enabled or self.stopped:
            return False
        scope = f"/guilds/{config.development_guild_id}" if config.development_guild_id else ""
        response = self.transport.request(
            f"https://discord.com/api/v10/applications/{config.application_id}{scope}/commands",
            {
                "commands": [
                    {"name": name, "description": f"Foreight {name}"}
                    for name in READ_ONLY_SLASH_COMMANDS
                ]
            },
            {"Authorization": f"Bot {config.token}", "Content-Type": "application/json"},
        )
        return response.status < 400

    def shutdown(self) -> None:
        self.stopped = True
        self.adapter.shutdown()


@dataclass(slots=True)
class BotRuntimeCoordinator:
    telegram: TelegramPollingRuntime | None = None
    discord: DiscordInteractionRuntime | None = None
    errors: dict[BotProvider, str] = field(default_factory=lambda: dict[BotProvider, str]())

    def start_once(self) -> None:
        if self.telegram:
            try:
                self.telegram.poll_once()
            except Exception as error:
                self.errors[BotProvider.TELEGRAM] = type(error).__name__
        if self.discord:
            try:
                self.discord.synchronize()
            except Exception as error:
                self.errors[BotProvider.DISCORD] = type(error).__name__

    def shutdown(self) -> None:
        if self.telegram:
            self.telegram.shutdown()
        if self.discord:
            self.discord.shutdown()
