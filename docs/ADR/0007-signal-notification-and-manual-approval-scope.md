# ADR 0007: Signal notification and manual approval scope

**Status: Accepted**  
**Approval date:** 2026-07-26  
**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

Research reporting, signal notifications and execution authorization have different trust requirements. Legacy chat notifications are useful delivery patterns but cannot be authoritative.

## Decision being considered

Define staged output, notifier and future manual-approval surfaces.

## Available options

- Structured files/console first, durable outbox later, authenticated local web approval later.
- Use Telegram/Discord messages as approval actions.
- CLI approval only.
- Build a hosted/mobile interface first.

## Recommended option

Stage the capability:

1. Research/backtest: structured artifacts and console/report summaries only.
2. Signal-only: authoritative durable event ledger plus transactional notifier outbox; Telegram is the first optional adapter and Discord is deferred.
3. Practice-manual: an authenticated local web interface is the starting recommendation. It displays the exact immutable proposal and binds approval to proposal hash, single-use nonce, actor, authentication context, UTC decision time and expiry.

Notifications are projections, not state and are a separate trust boundary from approval. Chat reactions/messages never authorize orders. External notifications must not expose account IDs, balances, margin, credentials or sensitive broker metadata. UI, notifier, database or network failure rejects or expires the proposal. Material changes create a new proposal/hash and require new approval. The execution gateway revalidates all volatile controls after approval.

## Reasons

This keeps research simple, makes notifications recoverable and separates human awareness from the security boundary. A local authenticated UI minimizes early public attack surface while providing a reviewable proposal.

## Consequences

Signal-only needs durable delivery status and dead-letter handling. Practice-manual later needs authentication, roles, CSRF/session protection, auditability, accessible UX and proposal-expiry behavior.

## Risks

Chat channels can leak sensitive signal/account context. A local UI can still be exposed by poor network binding. Operator latency and alert fatigue can make proposals stale.

## Alternatives rejected

Chat approval is rejected because identity, message mutation, replay and proposal binding are weak. CLI-only approval is less reviewable for routine operation. Hosted/mobile-first scope is premature.

## Questions requiring human approval

Telegram-first, Discord deferral, authenticated local web approval and separate notification/approval trust boundaries are approved. Detailed user roles and deployment topology remain subject to the later threat model. Sensitive account and broker metadata may not leave the local environment through notifications.

## Evidence required before acceptance

Operator workflow and threat model; proposal display requirements; authentication/authorization design; failure/expiry tests; channel privacy and rate-limit review; audit-event specification.

## Explicit implementation impact

If accepted later, it sequences reporting, outbox/channel adapters and approval UI. It authorizes no UI, notifier or service during Phase 0.
