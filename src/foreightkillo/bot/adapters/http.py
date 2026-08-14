"""Minimal injectable JSON HTTP transport for optional provider adapters."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Protocol, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True, slots=True)
class HttpResponse:
    status: int
    body: dict[str, Any]
    retry_after_seconds: int | None = None


class HttpTransport(Protocol):
    def request(
        self, url: str, body: dict[str, Any] | None, headers: dict[str, str]
    ) -> HttpResponse: ...


class UrllibJsonTransport:
    def request(
        self, url: str, body: dict[str, Any] | None, headers: dict[str, str]
    ) -> HttpResponse:
        payload = json.dumps(body).encode() if body is not None else None
        request = Request(  # noqa: S310
            url, data=payload, headers=headers, method="POST" if body else "GET"
        )
        try:
            with urlopen(request, timeout=10) as response:  # noqa: S310
                content = json.loads(response.read().decode())
                return HttpResponse(response.status, content)
        except HTTPError as error:
            raw = error.read().decode(errors="replace")
            try:
                content = json.loads(raw)
            except json.JSONDecodeError:
                content = {"description": "provider HTTP error"}
            parameters = content.get("parameters")
            retry_after: int | None = None
            if isinstance(parameters, dict):
                raw_retry_after = cast("dict[str, object]", parameters).get("retry_after")
                if isinstance(raw_retry_after, int):
                    retry_after = raw_retry_after
            return HttpResponse(error.code, content, retry_after)
        except URLError:
            return HttpResponse(503, {"description": "network unavailable"})
