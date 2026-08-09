"""Optional provider adapters."""

from .discord import DiscordAdapter
from .local import LocalBotAdapter
from .telegram import TelegramAdapter

__all__ = ["DiscordAdapter", "LocalBotAdapter", "TelegramAdapter"]
