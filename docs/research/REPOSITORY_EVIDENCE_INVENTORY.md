# Repository Evidence Inventory

Purpose: classify repository evidence before implementation begins.
Scope: files and capabilities present in the local repository on 2026-07-04.
Audience: maintainers, reviewers, and product owners.
Assumptions: untracked files and deletions in `.github` are treated as user-side working tree state; no production code exists outside the inspected repository.
Dependencies: `README.md`, `LICENSE`, `.github/ISSUES_STORIES_TODO/`, Git history.
Unresolved decisions: whether to preserve the historical misspelled `.github/ISSUES_TEMPLATE` path in Git history only.
Related documents: [Technology Evaluation](TECHNOLOGY_EVALUATION.md), [User Story Audit](../product/USER_STORY_AUDIT.md).

## Inspection Summary

- Branch: `main`.
- Recent history: five commits, all documentation or story-template oriented.
- Tracked files before this baseline: `README.md`, `LICENSE`, and `.github/ISSUES_TEMPLATE/*`.
- Working tree before this baseline: four tracked `.github/ISSUES_TEMPLATE/*` files already deleted; four untracked `.github/ISSUES_STORIES_TODO/*` backlog files present.
- Verified source directories: none.
- Verified dependency manifests: none.
- Verified workflows, Docker files, scripts, tests, environment files, architecture docs: none.

## Evidence Classification

| Capability | Evidence | Classification | Notes |
| --- | --- | --- | --- |
| Product vision | Old `README.md` | Documentation only | The README claimed an AI trading platform but contained cloud-sandbox wrapper text and unsupported claims. |
| License | `LICENSE` | Verified implemented | GPL-3.0 text is present. Old README incorrectly claimed MIT. |
| Application API | None | Missing | No API framework, routes, auth, schemas, or service code exists. |
| Dashboard | None | Missing | No web app or UI assets exist. |
| Authentication | Old README only | Aspirational | No identity implementation exists. |
| Market data ingestion | Old README and stories | Aspirational | No connectors, accounts, keys, manifests, or adapters exist. |
| Backtesting | Story files | Planned | No engine or test harness exists. |
| ML modeling | Old README and stories | Aspirational | No feature pipeline, model code, artifacts, or training jobs exist. |
| Trading execution | Old README and risk story | Aspirational | No broker or exchange integration exists. |
| Risk controls | Story only | Planned | No deterministic risk engine exists. |
| Paper trading | Old README intent | Planned | No simulator exists. |
| Live trading | Old README claims | Contradictory | Live trading must remain disabled until gates are satisfied. |
| Security policy | None before baseline | Missing | Created as part of this baseline. |
| CI/CD | None | Missing | No GitHub Actions workflows exist. |
| Tests | None | Missing | No test framework or test files exist. |
| Infrastructure | None | Missing | No IaC, containers, or deployed resources exist. |
| Documentation governance | Old issue template | Scaffold only | Template path was misspelled as `ISSUES_TEMPLATE`; proper `ISSUE_TEMPLATE` is added. |
| Backlog | Four story files | Partially implemented | Stories were useful but incomplete, oversized, and missing security/data/risk/ops requirements. |

## Contradictions Removed or Corrected

- The old README claimed MIT while the repository contains GPL-3.0.
- The old README described a planned directory tree as if it existed.
- The old README used unsupported marketing, ownership, latency, and readiness claims.
- The old README implied live automated execution before any evidence of provider contracts, risk controls, reconciliation, security review, or release gates.

## Repository Baseline Decision

The repository MUST be treated as pre-development. Any future status statement MUST distinguish verified implementation from planned capability.
