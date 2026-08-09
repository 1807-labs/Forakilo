# Source preservation report

Date: 2026-07-29  
Result: **PASS for Chainna, the private annotation source, and Chains history
bundles**

All required migration-source histories were fetched or mirrored before bundle
creation. `git bundle verify` reports complete history and `okay` for each
bundle.

| Bundle | Source HEAD | Bytes | SHA-256 | Verify |
|---|---|---:|---|---|
| `<MIGRATION_BACKUP_ROOT>/Chainna-all-refs.bundle` | `ca663f8c250a175273a7243e424c19fa1069bb85` | 67,727 | `C2A72EFB0950A07274C84F91656A1429F1E97FA567511F58D1BE1A6FDF733591` | PASS |
| `<PRIVATE_BACKUP_PATH>` | `6e461471eb4d18fafe9690953ca1edd3d227817b` | 9,445 | `9D60B27A5315AE5588B8C2C636C952A113A3D943F74518F5955922660D91F7CE` | PASS |
| `<MIGRATION_BACKUP_ROOT>/Chains-all-refs.bundle` | `6ada073d6793431c376b942ef45a73000fe781f2` | 849,915 | `89C8A190E122D9C08BB05C1609718CB8D1E7B59D4E96FF2305251F22387E93A0` | PASS |

The private annotation-source bundle was created from a retained authenticated
bare mirror. Bundle binaries are external and are not committed to Foreightkillo.

LEAN was not bundled. It remains an external fork pinned at
`cd52034ddf55c0c9aa57264d2a148e563924100f`. Because its cloud-synced status
scan stalls, it must remain untouched and its worktree cleanliness is
unresolved.

## Public archive publication

Only the two public source histories were imported. No history was merged into
`main`.

| Source | Archive ref | Tag | Commit | Push |
|---|---|---|---|---|
| Chainna | `archive/chainna-final` | `migration/chainna-final` | `ca663f8c250a175273a7243e424c19fa1069bb85` | PASS |
| Chains | `archive/chains-reference` | `migration/chains-reference` | `6ada073d6793431c376b942ef45a73000fe781f2` | PASS |

The private annotation-source bundle was verified again but its history,
branch, tag, bundle, backup ref, and exact identity were not pushed.

## Private evidence integrity

Exact local paths, private repository identity, clone URLs, and bundle
locations are retained only in private evidence outside the repository. Public
integrity checks:

| Private evidence file | SHA-256 |
|---|---|
| `PRIVATE_BUNDLE_LOCATION_MANIFEST.json` | `BEC167CB72EE7F58669C537C8688AB9717FB60DB665C5452D8313284DE2631D1` |
| `PRIVATE_LOCAL_WORKSPACE_INVENTORY.md` | `0B86B76120BA8F64C5E79F49170C32293F8A6652894139070CC5F22A30F1EC2A` |
| `PRIVATE_MIGRATION_PATH_MAP.md` | `D5149ACE79384C89E37C9B5E0841D6064F6F7B0810B181EF5C97CA2CBBF28BB6` |
| `PRIVATE_SOURCE_REPOSITORY_MAP.md` | `667BE828CDAEC267873FFC9B2D20DA48A8A516D4B76A5B2BEB61EF5C87A4B0A9` |

