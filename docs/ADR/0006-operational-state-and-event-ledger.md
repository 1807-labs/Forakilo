# ADR 0006: Operational state and event ledger

**Status: Accepted**  
**Approval date:** 2026-07-26  
**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

Signals, approvals, orders, fills, health and kill switches must survive restarts and support reconciliation. ChainCrawlr's JSON/cache state demonstrates why caches cannot authorize execution.

## Decision being considered

Choose the authoritative model and future storage technology for signal and practice services.

## Available options

- Append-only ledger in PostgreSQL with transactional projections/outbox.
- SQLite for all modes.
- JSON/event files plus caches.
- Treat LEAN/broker state as the only authority.

## Recommended option

Use append-only audit/domain events covering signal candidates/eligibility, proposals, approvals/rejections/expiry, authorizations, submissions, broker acknowledgements, fills/cancels, reconciliation, health transitions and kill-switch changes, together with transactional normalized current-state tables. Full event sourcing is not required for every internal object. Pair relevant state/event writes with a transactional notifier outbox.

Use PostgreSQL for future multi-process signal and practice services. Permit SQLite only for local research or isolated non-execution prototypes with explicit non-production markers. JSON manifests remain authoritative for immutable experiments, not operational execution. Caches are disposable accelerators.

Use stable event IDs, aggregate IDs, monotonic aggregate versions, UTC occurrence/record times, causation/correlation IDs, actor/policy identity, schema versions and idempotency keys. Never mutate prior facts; corrections are new events. Restart must reload durable loss-limit, approval, reconciliation and kill-switch state before accepting work.

## Reasons

PostgreSQL provides transactions, concurrency, durability and operational tooling. An append-only ledger gives the audit and recovery semantics required for authorization and uncertain broker outcomes.

## Consequences

Schema evolution, migrations, retention, backup/restore, projections and privacy/redaction need design. PostgreSQL is not needed for the earliest pure research core but becomes a gate before signal/practice services.

## Risks

Event-sourcing complexity can be overbuilt. Incorrect projection/version logic can block or duplicate work. Database availability becomes a health gate, and sensitive operational metadata needs protection.

## Alternatives rejected

SQLite is rejected for future concurrent execution services, not for local experiments. JSON/cache is rejected as authoritative state. LEAN/broker-only history cannot represent proposals, approvals, risk decisions or internal kill switches.

## Questions requiring human approval

The storage technology and append-only-events-plus-current-state model are approved. Retention, backup and access-control details remain future operational evidence, not Phase 0 architecture decisions.

## Evidence required before acceptance

Event taxonomy and state-transition diagrams; idempotency/concurrency design; transaction/outbox proof; backup/restore and replay plan; restart and reconciliation scenarios; privacy/threat review.

## Explicit implementation impact

If accepted in a later phase, it determines operational schemas, repositories, projections, outbox and restart gates. Phase 0 creates no database and no schema files.
