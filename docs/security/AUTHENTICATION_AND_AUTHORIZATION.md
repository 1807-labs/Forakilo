# Authentication and Authorization

Purpose: define identity, authentication, authorization, and access-control requirements.
Scope: users, roles, sessions, service identities, and high-impact actions.
Audience: backend engineers, security reviewers, QA, and product owners.
Assumptions: no protected service may be used before authentication.
Dependencies: [Account Lifecycle](ACCOUNT_AND_SESSION_LIFECYCLE.md), [Security Requirements](SECURITY_REQUIREMENTS.md), [Sources](../research/SOURCES.md).
Unresolved decisions: identity-provider build versus buy, passkey launch timing, and exact MFA policy.

## Roles

| Role | Purpose | Example permissions |
| --- | --- | --- |
| User | Own account and paper/live settings. | View own dashboard, manage own profile, manage own approved credentials. |
| Operator | Monitor system health. | View operational dashboards, acknowledge alerts. |
| Risk administrator | Manage risk policy. | Change risk limits, activate kill switch, approve gates. |
| Security administrator | Manage security controls. | Investigate incidents, revoke sessions/credentials. |
| Platform administrator | Manage platform settings. | Limited admin actions with approval and audit. |
| Read-only auditor | Review evidence. | Read audit and compliance records. |
| Service identity | Internal automation. | Narrow machine-to-machine permissions. |

## Requirements

- Authentication MUST be required before protected dashboard, API, data, model, and trading services.
- Authorization MUST be enforced server-side for every object and function.
- MFA or passkeys SHOULD be supported for users and MUST be required for privileged roles.
- Sessions MUST be revocable, expiring, device-aware, and auditable.
- Service identities MUST use least privilege and rotatable credentials.

## Step-Up Actions

Step-up authentication MUST be required for adding/replacing provider keys, enabling live trading, increasing risk limits, disabling a kill switch, changing execution policies, promoting a model, exporting sensitive data, deleting an account, and changing any withdrawal-related permission if such permission is ever supported.
