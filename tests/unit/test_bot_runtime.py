from dataclasses import dataclass, field
from typing import Any

from foreightkillo.bot.adapters.http import HttpResponse
from foreightkillo.bot.adapters.telegram import TelegramAdapter
from foreightkillo.bot.config import TelegramConfig
from foreightkillo.bot.contracts import BotProvider
from foreightkillo.bot.gateway import BotGateway
from foreightkillo.bot.permissions import AllowlistPermissionPolicy
from foreightkillo.bot.runtime import OffsetStore, TelegramPollingRuntime
from foreightkillo.queries.services import QueryService


@dataclass
class Transport:
    responses: list[HttpResponse]
    calls: list[tuple[str, dict[str, Any] | None]] = field(
        default_factory=lambda: list[tuple[str, dict[str, Any] | None]]()
    )

    def request(
        self, url: str, body: dict[str, Any] | None, headers: dict[str, str]
    ) -> HttpResponse:
        self.calls.append((url, body))
        return self.responses.pop(0)


def test_telegram_polling_advances_offset_and_routes_command() -> None:
    transport = Transport(
        [
            HttpResponse(
                200,
                {
                    "result": [
                        {
                            "update_id": 7,
                            "message": {"text": "/help", "chat": {"id": 10}, "from": {"id": 20}},
                        }
                    ]
                },
            ),
            HttpResponse(200, {"result": {"message_id": 1}}),
        ]
    )
    config = TelegramConfig(
        True, "test-token", frozenset({"10"}), command_chat_ids=frozenset({"10"})
    )
    adapter = TelegramAdapter(config, transport)
    gateway = BotGateway(
        AllowlistPermissionPolicy("local", frozenset({"10"})),
        QueryService(),
        {BotProvider.TELEGRAM: adapter},
    )
    runtime = TelegramPollingRuntime(adapter, transport, gateway, "local", OffsetStore())
    assert runtime.poll_once() == 1
    assert runtime.offsets.load() == 8
    assert len(transport.calls) == 2


def test_telegram_polling_ignores_duplicate_and_denied_chat() -> None:
    transport = Transport(
        [
            HttpResponse(
                200,
                {"result": [{"update_id": 2, "message": {"text": "/help", "chat": {"id": 99}}}]},
            )
        ]
    )
    config = TelegramConfig(
        True, "test-token", frozenset({"10"}), command_chat_ids=frozenset({"10"})
    )
    runtime = TelegramPollingRuntime(
        TelegramAdapter(config, transport),
        transport,
        BotGateway(AllowlistPermissionPolicy("local", frozenset({"10"})), QueryService()),
        "local",
        OffsetStore(_offset=3),
    )
    assert runtime.poll_once() == 0
