"""Provider types expressed without Telegram or Discord SDK objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from foreightkillo.notifications.projections import Notification


class BotProvider(StrEnum):
    LOCAL = "local"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    NOESIS = "noesis"


class BotRole(StrEnum):
    PUBLIC_SUBSCRIBER = "public_subscriber"
    AUTHENTICATED_MEMBER = "authenticated_member"
    OPERATOR = "operator"
    ADMINISTRATOR = "administrator"


@dataclass(frozen=True, slots=True)
class BotDestination:
    provider: BotProvider
    destination_id: str
    installation_id: str
    guild_id: str | None = None


@dataclass(frozen=True, slots=True)
class BotIdentity:
    provider: BotProvider
    protected_actor_id: str
    role: BotRole


@dataclass(frozen=True, slots=True)
class BotCommand:
    command_id: str
    name: str
    arguments: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BotCommandContext:
    identity: BotIdentity
    destination: BotDestination
    correlation_id: str
    received_at: datetime


@dataclass(frozen=True, slots=True)
class BotResponse:
    command_id: str
    outcome: str
    text: str
    sensitive: bool = False


@dataclass(frozen=True, slots=True)
class DeliveryRequest:
    request_id: str
    destination: BotDestination
    notification: Notification
    idempotency_key: str


@dataclass(frozen=True, slots=True)
class DeliveryFailure:
    classification: str
    retryable: bool
    redacted_detail: str
    retry_after_seconds: int | None = None


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    request_id: str
    accepted: bool
    provider_message_id: str | None
    failure: DeliveryFailure | None


@dataclass(frozen=True, slots=True)
class BotPermissionDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True, slots=True)
class BotHealthStatus:
    provider: BotProvider
    enabled: bool
    healthy: bool
    detail: str


class BotAdapter(Protocol):
    @property
    def provider(self) -> BotProvider: ...

    def validate_destination(self, destination: BotDestination) -> bool: ...

    def deliver(self, request: DeliveryRequest) -> DeliveryResult: ...

    def health(self) -> BotHealthStatus: ...

    def shutdown(self) -> None: ...


class BotCommandReceiver(Protocol):
    def receive(self) -> tuple[tuple[BotCommand, BotCommandContext], ...]: ...


class BotIdentityMapper(Protocol):
    def map_identity(
        self, provider_actor_id: str, destination: BotDestination
    ) -> BotIdentity | None: ...


class BotMessageFormatter(Protocol):
    def format(self, request: DeliveryRequest) -> tuple[object, ...]: ...


class ProviderRateLimiter(Protocol):
    def permit(self, destination: BotDestination, at: datetime) -> bool: ...
