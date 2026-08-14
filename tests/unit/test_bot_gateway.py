from datetime import UTC, datetime

import pytest

from foreightkillo.bot.adapters.local import LocalBotAdapter
from foreightkillo.bot.contracts import (
    BotCommand,
    BotCommandContext,
    BotDestination,
    BotIdentity,
    BotProvider,
    BotRole,
    DeliveryRequest,
)
from foreightkillo.bot.gateway import BotGateway
from foreightkillo.bot.permissions import AllowlistPermissionPolicy
from foreightkillo.notifications.events import Visibility
from foreightkillo.notifications.projections import Notification, NotificationPriority
from foreightkillo.queries.services import QueryService

NOW = datetime(2026, 7, 29, tzinfo=UTC)


def context(role: BotRole = BotRole.OPERATOR, destination: str = "allowed") -> BotCommandContext:
    return BotCommandContext(
        BotIdentity(BotProvider.LOCAL, "actor-hash", role),
        BotDestination(BotProvider.LOCAL, destination, "installation-1"),
        "corr-1",
        NOW,
    )


def gateway() -> BotGateway:
    return BotGateway(
        AllowlistPermissionPolicy("installation-1", frozenset({"allowed"})),
        QueryService(),
    )


@pytest.mark.parametrize(
    "command", ["buy", "sell", "approve", "execute", "change-risk", "promote-model"]
)
def test_mutating_commands_are_impossible(command: str) -> None:
    response = gateway().handle(BotCommand("cmd", command, ()), context(BotRole.ADMINISTRATOR))
    assert response.outcome == "denied"
    assert "mutating_commands_prohibited" in response.text


def test_destination_and_role_are_enforced() -> None:
    assert gateway().handle(BotCommand("c", "risk", ()), context(destination="bad")).outcome == (
        "denied"
    )
    assert (
        gateway().handle(BotCommand("c", "risk", ()), context(BotRole.PUBLIC_SUBSCRIBER)).outcome
        == "denied"
    )


def test_missing_argument_and_unavailable_data_are_truthful() -> None:
    bot = gateway()
    assert bot.handle(BotCommand("c", "signal", ()), context()).outcome == "invalid"
    response = bot.handle(BotCommand("c", "signal", ("signal-1",)), context())
    assert response.outcome == "not_available"


def test_local_delivery_and_disabled_provider() -> None:
    bot = gateway()
    adapter = LocalBotAdapter(frozenset({"allowed"}))
    bot.adapters[BotProvider.LOCAL] = adapter
    message = Notification(
        "m",
        "e",
        "system",
        NotificationPriority.NORMAL,
        "Status",
        "Healthy",
        (),
        NOW,
        None,
        Visibility.MEMBER,
        "installation",
        None,
        "m",
        False,
    )
    result = bot.deliver(DeliveryRequest("r", context().destination, message, "idempotent"))
    assert result.accepted
    with pytest.raises(ValueError):
        BotGateway(bot.policy, bot.queries).deliver(
            DeliveryRequest("r2", context().destination, message, "idempotent-2")
        )
