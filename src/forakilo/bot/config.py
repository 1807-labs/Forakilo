"""Disabled-by-default bot configuration with redacted secrets."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


def _bool(value: str | None) -> bool:
    return value is not None and value.strip().lower() in {"1", "true", "yes", "on"}


def _ids(value: str | None) -> frozenset[str]:
    return frozenset(item.strip() for item in (value or "").split(",") if item.strip())


@dataclass(frozen=True, slots=True)
class TelegramConfig:
    enabled: bool = False
    token: str | None = field(default=None, repr=False)
    allowed_chat_ids: frozenset[str] = frozenset()
    signal_chat_id: str | None = None
    risk_chat_id: str | None = None
    system_chat_id: str | None = None

    def validate(self) -> None:
        if self.enabled and (not self.token or not self.allowed_chat_ids):
            raise ValueError("enabled Telegram requires token and allowed chat IDs")


@dataclass(frozen=True, slots=True)
class DiscordConfig:
    enabled: bool = False
    token: str | None = field(default=None, repr=False)
    application_id: str | None = None
    allowed_guild_ids: frozenset[str] = frozenset()
    allowed_channel_ids: frozenset[str] = frozenset()
    signal_channel_id: str | None = None
    risk_channel_id: str | None = None
    system_channel_id: str | None = None

    def validate(self) -> None:
        if self.enabled and (
            not self.token
            or not self.application_id
            or not self.allowed_guild_ids
            or not self.allowed_channel_ids
        ):
            raise ValueError(
                "enabled Discord requires token, application, guild and channel allowlists"
            )


@dataclass(frozen=True, slots=True)
class BotSettings:
    installation_id: str
    telegram: TelegramConfig
    discord: DiscordConfig

    @classmethod
    def from_environment(cls) -> BotSettings:
        telegram_enabled = _bool(os.getenv("FORAKILO_TELEGRAM_ENABLED"))
        discord_enabled = _bool(os.getenv("FORAKILO_DISCORD_ENABLED"))
        telegram = TelegramConfig(
            enabled=telegram_enabled,
            token=(os.getenv("FORAKILO_TELEGRAM_BOT_TOKEN") if telegram_enabled else None),
            allowed_chat_ids=_ids(os.getenv("FORAKILO_TELEGRAM_ALLOWED_CHAT_IDS")),
            signal_chat_id=os.getenv("FORAKILO_TELEGRAM_SIGNAL_CHAT_ID"),
            risk_chat_id=os.getenv("FORAKILO_TELEGRAM_RISK_CHAT_ID"),
            system_chat_id=os.getenv("FORAKILO_TELEGRAM_SYSTEM_CHAT_ID"),
        )
        discord = DiscordConfig(
            enabled=discord_enabled,
            token=os.getenv("FORAKILO_DISCORD_BOT_TOKEN") if discord_enabled else None,
            application_id=os.getenv("FORAKILO_DISCORD_APPLICATION_ID"),
            allowed_guild_ids=_ids(os.getenv("FORAKILO_DISCORD_ALLOWED_GUILD_IDS")),
            allowed_channel_ids=_ids(os.getenv("FORAKILO_DISCORD_ALLOWED_CHANNEL_IDS")),
            signal_channel_id=os.getenv("FORAKILO_DISCORD_SIGNAL_CHANNEL_ID"),
            risk_channel_id=os.getenv("FORAKILO_DISCORD_RISK_CHANNEL_ID"),
            system_channel_id=os.getenv("FORAKILO_DISCORD_SYSTEM_CHANNEL_ID"),
        )
        telegram.validate()
        discord.validate()
        return cls(os.getenv("FORAKILO_INSTALLATION_ID", "local"), telegram, discord)


def redact(value: str, secrets: tuple[str | None, ...]) -> str:
    result = value
    for secret in secrets:
        if secret:
            result = result.replace(secret, "[REDACTED]")
    return result
