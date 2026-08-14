# ADR-0011: Python 3.11 baseline and external LEAN boundary

- Status: Accepted
- Date: 2026-07-29

## Decision

Foreightkillo supports Python `>=3.11,<3.13` and uses Python 3.11.11 as its release
and LEAN compatibility baseline. Deterministic domain, intelligence, strategy,
signal, risk, and portfolio packages must not import LEAN, QuantConnect, or
pythonnet. Only `adapters/lean` may translate across that boundary.

LEAN is pinned by exact commit in `third_party/lean/LEAN.lock.json`, fetched
into ignored `.external/lean`, and verified before use. A compatible OANDA
Practice plugin remains a separately reviewed and pinned dependency. No live
broker profile exists.

## Consequences

This supersedes the Python 3.13 selection in ADR-0002 while retaining FastAPI
as the planned API framework. It prevents nested repositories and allows the
deterministic product core to run and test without LEAN or a broker.

