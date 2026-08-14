"""Authenticated FastAPI surface for the self-hosted, paper-only MVP."""

from __future__ import annotations

import os
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from foreightkillo.application import ForeightService
from foreightkillo.dashboard import DASHBOARD_HTML
from foreightkillo.intelligence.conversation import (
    ForeightConversation,
    ResearchRepository,
    SQLiteConversationMemory,
)
from foreightkillo.marketdata.local import LocalMarketDataProvider
from foreightkillo.operations import OperationalControls
from foreightkillo.security import ApiKeyAuthenticator, Principal

app = FastAPI(
    title="For8killo", version="0.1.0", description="Foreight paper-trading market intelligence"
)
service = ForeightService(LocalMarketDataProvider())
state_path = Path(os.getenv("FOR8KILLO_STATE_PATH", ".state"))
controls = OperationalControls(state_path / "operations.sqlite3")
conversation = ForeightConversation(
    service.queries(),
    ResearchRepository(),
    SQLiteConversationMemory(state_path / "conversation.sqlite3"),
)
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
                frozenset(
                    {
                        "market:read",
                        "portfolio:read",
                        "conversation:use",
                        "operations:read",
                        "operations:control",
                    }
                ),
            ),
        )


class ConversationRequest(BaseModel):
    conversation_id: str = Field(min_length=1, max_length=128)
    question: str = Field(min_length=1, max_length=2000)


class ProposalRequest(BaseModel):
    signal_id: str = Field(min_length=1, max_length=128)
    account_id: str = Field(min_length=1, max_length=128)
    equity: Decimal = Field(gt=0)
    risk_fraction: Decimal = Field(gt=0, le=Decimal("0.02"))


class KillSwitchRequest(BaseModel):
    active: bool
    reason: str = Field(min_length=8, max_length=500)


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
PortfolioReader = Annotated[Principal, Depends(require_scope("portfolio:read"))]
OperationsReader = Annotated[Principal, Depends(require_scope("operations:read"))]
OperationsController = Annotated[Principal, Depends(require_scope("operations:control"))]
ConversationUser = Annotated[Principal, Depends(require_scope("conversation:use"))]


@app.get("/health")
def health() -> dict[str, str]:
    status = controls.status()
    return {
        "status": "healthy",
        "mode": status.mode,
        "agent": "Foreight",
        "kill_switch": "active" if status.kill_switch_active else "clear",
    }


@app.get("/api/v1/operations/status")
def operational_status(_principal: OperationsReader) -> dict[str, object]:
    return asdict(controls.status())


@app.get("/api/v1/operations/audit")
def operational_audit(
    _principal: OperationsReader, limit: int = 100
) -> tuple[dict[str, object], ...]:
    try:
        return tuple(asdict(event) for event in controls.audit(limit))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.put("/api/v1/operations/kill-switch")
def set_kill_switch(
    request: KillSwitchRequest, principal: OperationsController
) -> dict[str, object]:
    return asdict(controls.set_kill_switch(request.active, principal.principal_id, request.reason))


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


@app.get("/api/v1/strategy-research/{symbol}")
def strategy_research(symbol: str, _principal: MarketReader) -> dict[str, object]:
    try:
        return service.strategy_research(symbol.upper())
    except KeyError as error:
        raise HTTPException(status_code=404, detail="instrument not supported") from error


@app.post("/api/v1/signals/{symbol}")
def generate_signal(symbol: str, _principal: MarketReader) -> dict[str, object]:
    try:
        return service.generate_signal(symbol.upper())
    except KeyError as error:
        raise HTTPException(status_code=404, detail="instrument not supported") from error


@app.get("/api/v1/signals")
def ranked_signals(_principal: MarketReader) -> tuple[dict[str, object], ...]:
    return service.ranked_signals()


@app.get("/api/v1/portfolio")
def portfolio(_principal: PortfolioReader) -> dict[str, object]:
    return service.portfolio()


@app.post("/api/v1/conversations/ask")
def ask_foreight(request: ConversationRequest, _principal: ConversationUser) -> dict[str, object]:
    try:
        return asdict(conversation.ask(request.conversation_id, request.question))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.post("/api/v1/paper-proposals")
def prepare_paper_proposal(
    request: ProposalRequest, _principal: PortfolioReader
) -> dict[str, object]:
    try:
        return service.prepare_paper_proposal(
            request.signal_id, request.account_id, request.equity, request.risk_fraction
        )
    except KeyError as error:
        raise HTTPException(status_code=404, detail="eligible ranked signal not found") from error
