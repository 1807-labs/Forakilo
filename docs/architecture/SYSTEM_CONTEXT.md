# System Context

Purpose: show Foreightkillo's external actors and systems.
Scope: users, providers, data sources, email/notification services, and operations tooling.
Audience: engineers, security reviewers, legal counsel, and operators.
Assumptions: external services are not yet contracted or implemented.
Dependencies: [Integration Architecture](INTEGRATION_ARCHITECTURE.md), [API Provider Matrix](../research/API_AND_DATA_PROVIDER_MATRIX.md).
Unresolved decisions: final providers, email vendor, and hosting environment.

```mermaid
flowchart TB
    User[User] --> Foreightkillo[Foreightkillo Platform]
    Admin[Operator/Admin] --> Foreightkillo
    Auditor[Read-only Auditor] --> Foreightkillo
    Foreightkillo --> FX[FX Broker Demo/Live API]
    Foreightkillo --> Crypto[Crypto Exchange API]
    Foreightkillo --> Macro[Macro Data APIs]
    Foreightkillo --> Notify[Email/Notification Provider]
    Foreightkillo --> Observability[Logs Metrics Traces Alerts]
    Foreightkillo --> ObjectStore[Object and Model Artifact Storage]
```

## External Boundaries

- Users authenticate through Foreightkillo, not directly into internal services.
- Providers remain third-party systems with their own terms, status, and failure modes.
- Foreightkillo does not hold user funds in the MVP.
- General-purpose hosted LLM APIs are not part of the real-time market, risk, or execution path.
