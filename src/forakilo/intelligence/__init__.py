"""Local-first intelligence plane."""

from .conversation import (
    Citation,
    ConversationResponse,
    ForeightConversation,
    ResearchDocument,
    ResearchRepository,
    SQLiteConversationMemory,
)
from .providers import HttpLanguageProvider, LanguageTransport
from .research import (
    FeedItem,
    IngestionReport,
    ResearchFeed,
    ResearchIngestionPolicy,
    ResearchIngestor,
)

__all__ = [
    "Citation",
    "ConversationResponse",
    "FeedItem",
    "ForeightConversation",
    "HttpLanguageProvider",
    "IngestionReport",
    "LanguageTransport",
    "ResearchDocument",
    "ResearchFeed",
    "ResearchIngestionPolicy",
    "ResearchIngestor",
    "ResearchRepository",
    "SQLiteConversationMemory",
]
