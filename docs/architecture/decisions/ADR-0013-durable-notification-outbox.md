# ADR-0013: Durable notification outbox

- Status: Accepted
- Date: 2026-07-29

Notifications use a repository interface with a transactional SQLite backend
for local operation. Workers atomically claim bounded batches using leases.
Retries use bounded exponential backoff; expiry, permanent failure, maximum
attempts, dead letters, duplicate suppression, recovery, replay, and delivery
auditing are explicit states. Provider failures are redacted before storage.

The outbox is an application reliability boundary, not authorization.

