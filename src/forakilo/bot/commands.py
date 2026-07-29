"""Strict parsing for the provider-neutral, read-only command surface."""

from __future__ import annotations

from uuid import uuid4

from .contracts import BotCommand

MAX_COMMAND_LENGTH = 512


def parse_command(text: str, command_id: str | None = None) -> BotCommand:
    """Parse one command without accepting provider markup or free-form actions."""
    normalized = text.strip()
    if not normalized or len(normalized) > MAX_COMMAND_LENGTH:
        raise ValueError("command must contain between 1 and 512 characters")
    parts = normalized.split()
    name = parts[0].split("@", 1)[0].removeprefix("/").lower()
    if not name or not name.replace("_", "").isalnum():
        raise ValueError("command name is invalid")
    return BotCommand(command_id or str(uuid4()), name, tuple(parts[1:]))
