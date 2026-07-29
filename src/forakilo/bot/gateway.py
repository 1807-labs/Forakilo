"""Read-only command routing and provider-neutral delivery."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from hashlib import sha256

from forakilo.queries.services import QueryService

from .contracts import (
    BotAdapter,
    BotCommand,
    BotCommandContext,
    BotProvider,
    BotResponse,
    DeliveryRequest,
    DeliveryResult,
)
from .permissions import AllowlistPermissionPolicy

COMMAND_QUERIES = {
    "status": "GetSystemHealth",
    "signals": "ListRecentSignals",
    "signal": "GetSignalDetails",
    "risk": "GetRiskStatus",
    "paper": "GetPaperAccountStatus",
    "positions": "ListPaperPositions",
    "strategies": "ListStrategies",
    "strategy": "GetStrategySummary",
    "performance": "GetStrategyPerformance",
    "models": "ListModelVersions",
    "health": "GetSystemHealth",
}
ARGUMENT_REQUIRED = frozenset({"signal", "strategy", "performance"})


@dataclass(slots=True)
class BotAuditRecord:
    provider: BotProvider
    destination_hash: str
    command_id: str
    actor_hash: str
    authorization: str
    command_type: str
    outcome: str
    occurred_at: datetime
    correlation_id: str


@dataclass(slots=True)
class BotGateway:
    policy: AllowlistPermissionPolicy
    queries: QueryService
    adapters: dict[BotProvider, BotAdapter] = field(
        default_factory=lambda: dict[BotProvider, BotAdapter]()
    )
    audit: list[BotAuditRecord] = field(default_factory=lambda: list[BotAuditRecord]())
    metrics: dict[str, int] = field(default_factory=lambda: dict[str, int]())

    def handle(self, command: BotCommand, context: BotCommandContext) -> BotResponse:
        name = command.name.removeprefix("/").lower()
        decision = self.policy.decide(context, name)
        if not decision.allowed:
            self._record(command, context, decision.reason, "denied")
            self._increment("unauthorized_commands")
            return BotResponse(command.command_id, "denied", f"Command denied: {decision.reason}.")
        if name == "help":
            response = BotResponse(
                command.command_id,
                "ok",
                "Read-only commands: /status /signals /signal /risk /paper "
                "/positions /strategies /strategy /performance /models /health",
            )
        elif name in ARGUMENT_REQUIRED and not command.arguments:
            response = BotResponse(command.command_id, "invalid", f"Usage: /{name} <identifier>.")
        else:
            result = self.queries.execute(COMMAND_QUERIES[name], command.arguments)
            response = BotResponse(
                command.command_id,
                result.state,
                result.summary,
                result.sensitive,
            )
        self._record(command, context, "allowed", response.outcome)
        self._increment("commands")
        return response

    def deliver(self, request: DeliveryRequest) -> DeliveryResult:
        adapter = self.adapters.get(request.destination.provider)
        if adapter is None:
            raise ValueError("provider is disabled")
        if not adapter.validate_destination(request.destination):
            raise PermissionError("destination is not allowlisted")
        result = adapter.deliver(request)
        self._increment("delivered_messages" if result.accepted else "provider_failures")
        return result

    def _record(
        self,
        command: BotCommand,
        context: BotCommandContext,
        authorization: str,
        outcome: str,
    ) -> None:
        self.audit.append(
            BotAuditRecord(
                provider=context.identity.provider,
                destination_hash=sha256(context.destination.destination_id.encode()).hexdigest()[
                    :16
                ],
                command_id=command.command_id,
                actor_hash=context.identity.protected_actor_id,
                authorization=authorization,
                command_type=command.name,
                outcome=outcome,
                occurred_at=datetime.now(UTC),
                correlation_id=context.correlation_id,
            )
        )

    def _increment(self, metric: str) -> None:
        self.metrics[metric] = self.metrics.get(metric, 0) + 1
