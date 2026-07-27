# ADR 0009: OANDA Practice plugin selection process

**Status: Accepted**  
**Approval date:** 2026-07-26  
**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

The pinned LEAN checkout exposes OANDA model/configuration hooks but does not contain the brokerage implementation. Practice integration is a later phase and must not introduce an unverified dependency or allow Practice/Live confusion.

## Decision being considered

Define the process for selecting, verifying and isolating a compatible OANDA Practice brokerage plugin.

## Available options

- Formal later review of an official/trusted LEAN-compatible plugin/package.
- Install the first discoverable OANDA package now.
- Implement a direct OANDA client in Chainna.
- Defer OANDA and select another broker.

## Recommended option

OANDA Practice is the first broker target. Initially, only official QuantConnect and OANDA sources are trusted. Do not fetch or install a plugin in Phase 0. Before Phase 7, create a review record containing:

1. official/trusted source and exact repository/package identity;
2. version/commit/tag and immutable download location;
3. license and redistribution/deployment obligations;
4. compatibility with LEAN commit `cd52034dd` and its runtime/API versions;
5. publisher/signature, checksum/SBOM and full provenance chain;
6. transitive dependencies, vulnerability scan and remediation disposition;
7. maintenance status, release cadence, issue/security-reporting process and bus factor;
8. required account ID, environment, token and endpoint metadata;
9. proof that Practice and Live endpoints/account metadata cannot be silently confused;
10. proof the dependency and credentials are absent from research/signal-only builds and hosts;
11. isolated build and tests using mocks/sandboxes first, then an explicitly authorized OANDA Practice account;
12. order lifecycle, reconnect, rate-limit, partial-fill, cancel/amend and reconciliation compatibility.

Require an isolated Practice identity, credentials, deployment profile and account allowlist; explicit environment enumeration; and startup rejection for unknown/mismatched metadata. Pin exact artifacts and verify checksums on build/deploy. Strategy code never calls OANDA directly.

## Reasons

Brokerage plugins are security- and capital-sensitive dependencies. A formal process protects the LEAN boundary and makes later practice enablement auditable.

## Consequences

Practice work cannot begin until a candidate passes review. Plugin upgrades repeat compatibility/security evidence. Signal-only deployments use a dependency graph that excludes the plugin.

## Risks

No compatible maintained candidate may exist for the pinned fork. Package identity/supply chain can change. Even a verified plugin can contain runtime/order-semantics defects.

## Alternatives rejected

Installing now violates Phase 0. Direct OANDA integration violates the LEAN boundary. Another broker is not rejected permanently but is outside the proposed first target.

## Questions requiring human approval

OANDA Practice, official QuantConnect/OANDA sources and isolated Practice identity/deployment are approved. The exact evidence duration and order-sample requirements remain deferred and must be pre-registered in a Phase 7 entrance decision.

## Evidence required before acceptance

A completed candidate dossier covering all twelve review items, reproducible isolated compatibility results, dependency/SBOM scan, license approval, Practice/Live separation tests and signed owner/security approval.

## Explicit implementation impact

If accepted, it creates a future procurement/verification gate only. It does not select, download, install or connect any plugin, and it grants no trading authority.
