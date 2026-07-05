# Backlog Gap Analysis

Purpose: identify remaining backlog gaps after normalization.
Scope: foundation, MVP, controlled beta, and later phases.
Audience: product owners, maintainers, and delivery leads.
Assumptions: backlog is a planning baseline, not a full implementation plan.
Dependencies: [User Story Audit](USER_STORY_AUDIT.md), [Epic and Release Map](EPIC_AND_RELEASE_MAP.md).
Unresolved decisions: story owners, exact estimates after technical spikes, and release dates.

## Remaining Gaps

- Email provider and verification delivery story.
- Administrative support tooling story.
- Privacy export/deletion implementation story.
- Local development environment and dependency manifest story.
- CI workflow implementation story.
- Provider-specific OANDA/Coinbase/Kraken adapter stories after spikes.
- Legal review and user-consent implementation story.
- Backup/restore implementation story.
- Incident-response tabletop story.
- Accessibility audit story.

## Contradictions Resolved

- Live execution was removed from early provider story.
- Model training was decoupled from live trading.
- OCO/bracket orders were moved behind provider capability checks.
- Backtesting no longer claims proof of future performance.
