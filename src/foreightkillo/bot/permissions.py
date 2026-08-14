"""Fail-closed, installation-local bot permissions."""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import BotCommandContext, BotPermissionDecision, BotRole

READ_ONLY_COMMANDS = frozenset(
    {
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
    }
)
MUTATING_COMMANDS = frozenset({"buy", "sell", "approve", "execute", "change-risk", "promote-model"})

ROLE_RANK = {
    BotRole.PUBLIC_SUBSCRIBER: 0,
    BotRole.AUTHENTICATED_MEMBER: 1,
    BotRole.OPERATOR: 2,
    BotRole.ADMINISTRATOR: 3,
}
REQUIRED_ROLE = {
    "help": BotRole.PUBLIC_SUBSCRIBER,
    "status": BotRole.PUBLIC_SUBSCRIBER,
    "signals": BotRole.PUBLIC_SUBSCRIBER,
    "signal": BotRole.AUTHENTICATED_MEMBER,
    "strategies": BotRole.PUBLIC_SUBSCRIBER,
    "strategy": BotRole.PUBLIC_SUBSCRIBER,
    "performance": BotRole.AUTHENTICATED_MEMBER,
    "risk": BotRole.OPERATOR,
    "paper": BotRole.OPERATOR,
    "positions": BotRole.OPERATOR,
    "models": BotRole.OPERATOR,
    "health": BotRole.OPERATOR,
}


@dataclass(frozen=True, slots=True)
class AllowlistPermissionPolicy:
    installation_id: str
    allowed_destinations: frozenset[str]

    def decide(self, context: BotCommandContext, command: str) -> BotPermissionDecision:
        if context.destination.installation_id != self.installation_id:
            return BotPermissionDecision(False, "installation_mismatch")
        if context.destination.destination_id not in self.allowed_destinations:
            return BotPermissionDecision(False, "destination_not_allowlisted")
        if command in MUTATING_COMMANDS:
            return BotPermissionDecision(False, "mutating_commands_prohibited")
        if command not in READ_ONLY_COMMANDS:
            return BotPermissionDecision(False, "unknown_command")
        required = REQUIRED_ROLE[command]
        if ROLE_RANK[context.identity.role] < ROLE_RANK[required]:
            return BotPermissionDecision(False, "insufficient_role")
        return BotPermissionDecision(True, "allowed")
