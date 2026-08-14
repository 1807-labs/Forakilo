"""Typed read-only application queries."""

from .application import ApplicationQueryBackend
from .services import Availability, QueryResult, QueryService

__all__ = ["ApplicationQueryBackend", "Availability", "QueryResult", "QueryService"]
