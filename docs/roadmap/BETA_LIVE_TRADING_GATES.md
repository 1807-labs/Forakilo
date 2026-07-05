# Beta Live Trading Gates

Purpose: summarize gates for controlled beta live trading.
Scope: post-MVP live-trading readiness.
Audience: product owners, legal counsel, risk approvers, security reviewers, and operators.
Assumptions: beta live trading is optional and requires explicit approval.
Dependencies: [Paper to Live Gate](../trading/PAPER_TO_LIVE_TRADING_GATE.md), [Incident Response](../operations/INCIDENT_RESPONSE_PLAN.md).
Unresolved decisions: venue, instrument set, capital limits, and user eligibility.

## Gates

- Legal and provider approval.
- Production security review.
- Approved venue and account model.
- Strict capital, exposure, and order limits.
- Tested kill switch and credential revocation.
- Manual model promotion only.
- Monitoring, alerts, incident response, rollback, and support.
- User risk acknowledgement and live authorization.
- Reconciliation and unknown-order outcome runbooks.
