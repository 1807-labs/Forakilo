# Delivery Roadmap

Purpose: define progressive delivery phases for Forakilo.
Scope: foundation, MVP, controlled beta, and later releases.
Audience: product owners, engineers, risk reviewers, and maintainers.
Assumptions: live trading is unavailable until gates pass.
Dependencies: [MVP Scope](MVP_SCOPE_AND_EXIT_CRITERIA.md), [Beta Gates](BETA_LIVE_TRADING_GATES.md).
Unresolved decisions: dates, staffing, budget, and provider contracts.

## Foundation

Repository standards, documentation baseline, dependency strategy, secure SDLC, local development environment, CI, authentication design, secrets design, data contracts, and audit architecture.

## MVP

Authenticated user can register, connect approved sandbox/demo account, receive validated market data, view dashboard, run one approved strategy/model, generate auditable signals, apply deterministic risk controls, execute paper/sandbox orders, reconcile state, review performance, observe data/model health, trigger candidate retraining, evaluate without automatic live promotion, and activate kill switch.

## Controlled Beta

Limited live trading on one approved venue/instrument set with strict capital/exposure limits, manual model promotion, strong monitoring, incident response, rollback, user risk acknowledgement, and production security review.

## Later Releases

Additional venues, additional assets, advanced models, portfolio optimization, ensembles, advanced regimes, licensed sentiment sources, mobile support, and carefully governed automation.
