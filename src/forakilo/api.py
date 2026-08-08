"""FastAPI surface for the self-hosted, paper-only MVP."""

from fastapi import FastAPI, HTTPException

from forakilo.application import ForeightService
from forakilo.marketdata.local import LocalMarketDataProvider

app = FastAPI(
    title="For8killo", version="0.1.0", description="Foreight paper-trading market intelligence"
)
service = ForeightService(LocalMarketDataProvider())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "mode": "paper", "agent": "Foreight"}


@app.get("/api/v1/instruments")
def instruments() -> tuple[dict[str, str], ...]:
    return service.instruments()


@app.get("/api/v1/analysis/{symbol}")
def analyze(symbol: str, timeframe_seconds: int = 3600) -> dict[str, object]:
    try:
        return service.analyze(symbol.upper(), timeframe_seconds)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="instrument not supported") from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
