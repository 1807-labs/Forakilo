# Deletion readiness

Status: **BLOCKED**

No repository or workspace is authorized for deletion in this work unit.

## Passing preservation evidence

- Chainna, private annotation-source, and Chains all-ref bundles verify.
- Bundle SHA-256 hashes and source commit maps are recorded.
- Chainna and Chains local repositories are clean and match fetched remotes.
- A private authenticated annotation-source mirror is retained outside the
  worktree.
- Public Chainna and Chains archive refs and tags resolve to their preserved
  commits.
- The canonical workspace was freshly cloned, compared, and validated.
- No destructive Git or filesystem operation was performed.

## Blocking conditions

- LEAN cloud-synced worktree cleanliness cannot be established because status
  scans stall.
- The complete migration and feature acceptance gates are not yet satisfied.
- A separate product-owner deletion authorization has not been given after
  evidence review.

## Source-specific status

- **Chainna:** preservation gates pass, but accepted-document and feature
  migration, final source map, and separate deletion approval remain required.
- **Private annotation source:** private preservation passes without public
  history disclosure; remaining parity gaps, final local-only review, and
  separate deletion approval remain required.
- **Chains:** not deletion-eligible; preserved strategy/reference source.
- **LEAN:** not deletion-eligible; external pinned runtime/reference with
  unresolved local cleanliness.

Chains, LEAN, the legacy wrapper, the prior Foreightkillo checkout, Chainna, and the
private annotation source repository must all remain preserved.

