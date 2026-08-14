# Source repository inventory

Remote metadata was verified through the authenticated GitHub application on
2026-07-29. Chainna and Chains were subsequently fetched with all branches and
tags. The private annotation source was cloned as an authenticated mirror. All
three have a single `main` branch and no tags.

| Repository | Visibility | Default | Connector branches | HEAD | Size (KiB) | Access | Destination | Delete eligibility |
|---|---|---|---|---|---:|---|---|---|
| `1807-labs/Foreightkillo` | public | `main` | `main` | `a86faeb8dd878309865f0bfa3902206402780096` | 151 | push | canonical product | never |
| `vebbaybi/Chainna` | public | `main` | `main`; no tags | `ca663f8c250a175273a7243e424c19fa1069bb85` | 65 | admin | bundle verified; archive ref pending | blocked |
| `<PRIVATE_ANNOTATION_SOURCE_REPOSITORY>` | private | `main` | `main`; no tags | `6e461471eb4d18fafe9690953ca1edd3d227817b` | 10 | admin | mirror and bundle verified; archive ref pending | blocked |
| `vebbaybi/Chains` | public | `main` | `main`; no tags | `6ada073d6793431c376b942ef45a73000fe781f2` | 870 | admin | bundle verified; archive ref pending | prohibited |
| `vebbaybi/Lean` | public | `master` | 16 observed | `cd52034ddf55c0c9aa57264d2a148e563924100f` | 585979 | admin | external pinned dependency | prohibited |

The local Chainna and Chains commits equal their fetched remote heads. Neither
contains uncommitted work, local-only commits, stashes, submodules, additional
worktrees, untracked files, or important ignored files. The private annotation
source has no local checkout in the legacy workspace; its authenticated mirror
is the preservation source.

LEAN exposes 16 remote branches through the connected GitHub application.
Its local checkout is pinned to remote/default `master` commit
`cd52034ddf55c0c9aa57264d2a148e563924100f`; a complete cloud-synced worktree
status scan remains unresolved and blocks any claim that it is reconstructible
without local loss.

