# Local workspace inventory

| Path | Kind | Observed state | Disposition |
|---|---|---|---|
| `<FOREIGHTKILLO_WORKTREE>` | canonical candidate | clean at preflight; canonical public remote | active implementation |
| `<LOCAL_SOURCE_PATH>` | duplicate checkout | requires commit and dirty-state comparison | preserve |
| `<LEGACY_WORKSPACE>` | uncommitted wrapper repo | no commits; three untracked trees | preserve; deletion blocked |
| `<EXTERNAL_LEAN_CHECKOUT>` | nested LEAN repo | `master` at `cd52034ddf55c0c9aa57264d2a148e563924100f`; status scan stalls on cloud-synced storage | pinned external runtime; cleanliness unresolved; never vendor |
| `<LOCAL_SOURCE_PATH>` | Chainna product-policy repo | clean `main`; no tags, stashes, submodules, extra worktrees, local-only commits, untracked files, or important ignored files | bundled; archive pending |
| `<LOCAL_SOURCE_PATH>` | Chains reference repo | clean `main`; Sandy and ChainCrawlr material; no local-only state | bundled; preserve; do not delete |
| `<PRIVATE_BACKUP_PATH>` | authenticated bare mirror | complete `main` at `6e461471...`; no tags | retained private annotation source |
| `<MIGRATION_BACKUP_ROOT>` | migration backup | three verified all-ref bundles | preserve outside product repository |

## Wrapper classification and notable content

- Outer `.git`: 22 files, 26,392 bytes, unborn `master`, no remote or commits.
  Its three untracked directory entries are containers, not product changes.
- `engine`: 6,270 files, 893,259,727 bytes. It contains the LEAN checkout and
  two checked-in market-data ZIP fixtures larger than 10 MB:
  `Data/future/comex/tick/gc/20131009_quote.zip` (13,447,331 bytes) and
  `20131008_quote.zip` (10,905,457 bytes).
- `forex-engine`: 146 files, 836,620 bytes. It is the clean Chainna repository.
- `legacy`: 72 files, 2,576,242 bytes. It contains the clean Chains repository.
- Sandy: `legacy\chains\sandy.pine`.
- ChainCrawlr material: `legacy\chains\CC`, including Python/JavaScript source,
  configuration templates, cached bytecode, and a historical log.
- No local private annotation source checkout was found in the legacy workspace; the private
  repository was mirrored directly into the backup root.
- No wrapper-root files exist outside the three nested directory trees.
- No source filenames matching common secret, credential, account, private-key,
  or `.env` patterns were found outside Git metadata. File contents and secret
  values were not inspected.
- No local datasets, models, experiment outputs, or project notebooks were
  found outside the pinned LEAN tree; LEAN contains its normal test notebooks
  and market-data fixtures.

Recursive Git status checks repeatedly stall on the cloud-synced LEAN checkout,
even with untracked scanning disabled. Its remote, branch, upstream, and exact
HEAD are confirmed, but its tracked/untracked/ignored cleanliness remains an
explicit preservation risk. LEAN is not eligible for deletion.
