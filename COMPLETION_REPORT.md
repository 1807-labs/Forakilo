# For8killo MVP Completion Report

Verified: 2026-08-08

## Delivered system

For8killo is a working self-hosted, paper/practice-first market-intelligence system operated by
Foreight. The implementation includes immutable time-aware market contracts, deterministic local
data, market-structure and technical-strategy research, signal ranking, backtesting, deterministic
risk decisions, paper and manually authorized practice execution, portfolio accounting,
reconciliation, grounded conversation, governed research, notification delivery, operational
controls, and an authenticated API and browser console.

The public distribution and command are `for8killo`; the canonical Python namespace is
`foreightkillo`. Configuration accepts the product-prefixed `FOR8KILLO_*` variables and the fully
spelled `FOREIGHTKILLO_*` equivalents.

## Safety position

- There is no live-money execution mode or live broker adapter.
- New installations start with the persistent kill switch active.
- A practice order requires a matching unexpired proposal, approving deterministic risk decision,
  and one-time human authorization.
- Telegram, Discord, and conversation interfaces cannot mutate trading state.
- Model versions cannot self-promote; promotion requires approved evidence and a named human actor.
- Synthetic data is identified as synthetic and is unsuitable as a real decision feed.
- No performance, profitability, accuracy, or return is guaranteed.

## Verification evidence

- 74 unit tests passed.
- 13 executable behavior scenarios and 35 steps passed.
- Ruff formatting and lint passed.
- Strict Pyright passed with zero errors and warnings.
- Dependency audit reported no known third-party vulnerabilities; the two local distributions were
  skipped because they are not published on PyPI.
- The Linux container image built successfully and imported the application as its non-root user.
- GitHub Actions passed on Python 3.11 and 3.12 before the final strategy and specification
  increments; every later increment is required to pass the same workflow before release sign-off.

## External deployment prerequisites

Operators must supply and approve their own licensed market-data account, practice broker account,
Telegram or Discord application, optional language-provider endpoint, credentials, jurisdictional
review, and hosting environment. Those third-party accounts and approvals cannot be embedded in a
source release. Live trading remains a separate post-MVP decision governed by
[`docs/roadmap/BETA_LIVE_TRADING_GATES.md`](docs/roadmap/BETA_LIVE_TRADING_GATES.md).

The requirement-level evidence and remaining external gates are recorded in
[`docs/product/MVP_IMPLEMENTATION_EVIDENCE.md`](docs/product/MVP_IMPLEMENTATION_EVIDENCE.md).
