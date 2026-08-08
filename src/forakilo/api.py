"""Authenticated FastAPI surface for the self-hosted, paper-only MVP."""

from __future__ import annotations

import os
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from forakilo.application import ForeightService
from forakilo.dashboard import DASHBOARD_HTML
from forakilo.marketdata.local import LocalMarketDataProvider
from forakilo.security import ApiKeyAuthenticator, Principal

app = FastAPI(
    title="For8killo", version="0.1.0", description="Foreight paper-trading market intelligence"
)
service = ForeightService(LocalMarketDataProvider())
authenticator = ApiKeyAuthenticator()
configured_key = os.getenv("FOR8KILLO_API_KEY")
if configured_key:
    key_id, separator, secret = configured_key.partition(".")
    if separator:
        authenticator.register(
            key_id,
            secret,
            Principal(
                "local-operator",
                "operator",
                frozenset({"market:read", "portfolio:read", "conversation:use"}),
            ),
        )


class ConversationRequest(BaseModel):
    conversation_id: str = Field(min_length=1, max_length=128)
    question: str = Field(min_length=1, max_length=2000)


def require_scope(scope: str):
    def dependency(
        authorization: Annotated[str | None, Header()] = None,
    ) -> Principal:
        if not configured_key:
            raise HTTPException(status_code=503, detail="API authentication is not configured")
        scheme, _, presented = (authorization or "").partition(" ")
        principal = (
            authenticator.authenticate(presented, scope) if scheme.lower() == "bearer" else None
        )
        if principal is None:
            raise HTTPException(status_code=401, detail="invalid credentials or scope")
        return principal

    return dependency


MarketReader = Annotated[Principal, Depends(require_scope("market:read"))]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "mode": "paper", "agent": "Foreight"}


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    return DASHBOARD_HTML


@app.get("/api/v1/instruments")
def instruments(_principal: MarketReader) -> tuple[dict[str, str], ...]:
    return service.instruments()


@app.get("/api/v1/analysis/{symbol}")
def analyze(
    symbol: str, _principal: MarketReader, timeframe_seconds: int = 3600
) -> dict[str, object]:
    try:
        return service.analyze(symbol.upper(), timeframe_seconds)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="instrument not supported") from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
