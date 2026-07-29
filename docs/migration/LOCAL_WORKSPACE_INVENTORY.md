# Local workspace inventory

| Path | Kind | Observed state | Disposition |
|---|---|---|---|
| `<FORAKILO_WORKTREE>` | canonical candidate | clean at preflight; canonical public remote | active implementation |
| `<LOCAL_SOURCE_PATH>` | duplicate checkout | requires commit and dirty-state comparison | preserve |
| `<LEGACY_WORKSPACE>` | uncommitted wrapper repo | no commits; three untracked trees | preserve; deletion blocked |
| `<EXTERNAL_LEAN_CHECKOUT>` | nested LEAN repo | commit `cd52034ddf55c0c9aa57264d2a148e563924100f` | pin externally; never vendor |
| `<LOCAL_SOURCE_PATH>` | Chainna product-policy repo | documentation and compatibility spike present | migrate and archive |
| `<LOCAL_SOURCE_PATH>` | Chains reference repo | Sandy and ChainCrawlr material present | preserve; do not delete |

Recursive cloud-synced status checks can stall on the large LEAN checkout. Inventory
must use bounded, repository-specific checks and record ignored/untracked files
before any bundle or deletion decision.

