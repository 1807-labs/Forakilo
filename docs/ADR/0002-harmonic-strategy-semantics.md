# ADR 0002: Harmonic strategy semantics

**Status: Accepted**  
**Approval date:** 2026-07-26  
**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

Sandy contains useful legacy classification rules but delayed confirmation, lossy D-only deduplication, same-type adjacent pivots, an impossible alert, and display-only PRZ/targets. Parity and production research must not be silently conflated.

## Decision being considered

Define immutable `sandy_parity_v1` behavior for characterization and reserve new strategy IDs for corrected/researched semantics.

## Available options

- Reproduce every Sandy quirk, including raw pivot arrays and lossy precedence.
- Preserve Sandy ratio classification but normalize pivot input and explicitly document differences.
- Reject same-type adjacent pivots instead of normalization.
- Immediately replace Sandy rules with ratio ranges and genuine PRZ confluence.

## Recommended option

`sandy_parity_v1` preserves Sandy's point targets, absolute ratio tolerance, Gartley/Bat/Butterfly rules and parity signal precedence. It separately records `event_time` and closed-bar `known_time` and never acts before `known_time`.

Normalize consecutive pivots of the same type by retaining the more extreme price (higher high or lower low); if equally extreme, retain the earliest pivot deterministically. Treat a bar that confirms both a high and low as ambiguous: retain both in diagnostics, but do not allow both in one eligible normalized sequence without a future explicit tie-break rule.

Retain every valid candidate sharing D internally. A versioned eligibility selector chooses at most one parity signal using Gartley > Bat > Butterfly, with a deterministic final tie-break on canonical candidate identity. Future corrected strategies may use ranges, confluence, invalidation and quality scoring under a new strategy ID.

Stable signal identity is a canonical hash of schema version, strategy ID/version, market/symbol, resolution, direction, X/A/B/C/D event timestamps and prices in canonical precision, D known time, pivot parameters, pattern, tolerance and parameter-set ID. Run ID and creation time are excluded so replay is stable. Duplicate suppression is idempotent by this identity; repeated observations update no semantic fields.

Use decimal/canonical fixed-point values derived from instrument precision, never binary-float equality for identities. Tolerance is an absolute dimensionless ratio delta (for example `0.03`, not 3% of the target). Require completed input bars and a completed confirmation bar. Warm-up must cover at least the configured retained pivot history plus the right confirmation window, and eligibility remains blocked until five normalized confirmed pivots exist.

## Reasons

Normalization gives a coherent XABCD stream while retaining a named parity classifier. Keeping all candidates prevents detection-time information loss. Stable identity and known-time rules make replay and deduplication testable.

## Consequences

Parity will intentionally differ from Sandy on malformed same-type/simultaneous pivot cases and must report those differences. Sandy precedence affects eligibility only, not stored candidates. A future corrected strategy can evolve without rewriting parity history.

Sandy's D-centered “PRZ” is not confluence and its 38.2%/61.8% lines have no validated entry, stop or invalidation semantics. They are not execution rules. Stops and targets require separate strategy hypotheses, cost-aware research and risk approval.

## Risks

Normalization may change candidate counts materially. Canonical decimal conversion could hide upstream precision differences if underspecified. One-signal selection may discard simultaneous opportunities at the eligibility stage even though candidates remain stored.

## Alternatives rejected

Raw Sandy reproduction is rejected for eligible signals because malformed sequences remain ambiguous. Rejecting all same-type pivots is simpler but loses a standard zigzag correction behavior. Immediate “corrected” harmonics are rejected because they prevent clean legacy characterization.

## Questions requiring human approval

None. The Product Owner approved more-extreme replacement, earliest retention for equal extremes, diagnostic-but-ineligible simultaneous pivots, retention of all candidates sharing D, parity-only Sandy precedence, fixed-point/Decimal identities, closed bars, stable deduplication and documented warm-up.

## Evidence required before acceptance

Truth tables and synthetic fixtures covering ratio boundaries, same-type replacement, equal extremes, simultaneous pivots, multiple candidates, replay identity, closed-bar timing and default `minLegLength=5`; a written table of intentional Sandy differences.

## Explicit implementation impact

If accepted later, this fixes detector inputs, candidate schema, dedupe keys, parity selector, numeric representation, warm-up and test fixtures. It does not authorize implementing Sandy or any strategy now.
