"""For8killo command-line launcher."""

import uvicorn


def main() -> None:
    uvicorn.run("foreightkillo.api:app", host="127.0.0.1", port=8000)
