# Failure Modes and Edge Cases

Purpose: define expected behavior under high-risk failures.
Scope: provider, data, model, database, cache, queue, network, and execution failures.
Audience: engineers, QA, risk reviewers, and operators.
Assumptions: unknown safety state means no new execution.
Dependencies: [Order Execution](ORDER_EXECUTION_AND_RECONCILIATION.md), [Incident Response](../operations/INCIDENT_RESPONSE_PLAN.md).
Unresolved decisions: provider-specific runbooks and thresholds.

## Required Behaviors

| Failure | Required behavior |
| --- | --- |
| Network timeout after possible order acceptance | Query provider state; block duplicate order until resolved. |
| Duplicate order submission | Idempotency key prevents or detects duplicate; reconcile and alert. |
| Out-of-order provider events | Buffer/order by sequence where supported; otherwise mark uncertain and reconcile. |
| Provider rate limiting | Back off, alert if persistent, and reject new execution if state becomes stale. |
| Exchange maintenance or broker outage | Stop new execution and show degraded state. |
| WebSocket disconnect | Attempt reconnect; REST fallback for state; expire stale signals. |
| REST/WebSocket disagreement | Block new execution until reconciliation resolves. |
| Stale balances or positions | Reject new execution. |
| API key revocation | Disable provider connection, alert user, and audit event. |
| Insufficient funds or margin | Reject order and update risk state. |
| Precision rejection | Correct adapter metadata; reject until fixed. |
| Partial fills | Update position and remaining order state; reconcile. |
| Delisting | Stop new orders, mark instrument inactive, and notify operator/user. |
| Extreme spread or abnormal volatility | Circuit breaker rejects new execution. |
| Model-service failure | No model-dependent orders; risk rejects. |
| Database failure | Stop state-changing actions; alert and recover. |
| Cache or queue failure | Continue only if durable state and audit safety are preserved. |
| Clock skew | Reject time-sensitive decisions and alert operations. |
| Reconciliation mismatch | Block new execution and escalate. |
