# Source repository inventory

Remote metadata was verified through the authenticated GitHub application on
2026-07-29. Branch results are connector-visible branches; tags remain to be
fetched through Git before preservation.

| Repository | Visibility | Default | Connector branches | HEAD | Size (KiB) | Access | Destination | Delete eligibility |
|---|---|---|---|---|---:|---|---|---|
| `1807-labs/Forakilo` | public | `main` | `main` | `a86faeb8dd878309865f0bfa3902206402780096` | 151 | push | canonical product | never |
| `vebbaybi/Chainna` | public | `main` | `main` | `ca663f8c250a175273a7243e424c19fa1069bb85` | 65 | admin | docs, clean-room implementation, archive ref | blocked |
| `<PRIVATE_ANNOTATION_SOURCE_REPOSITORY>` | private | `main` | `main` | `6e461471eb4d18fafe9690953ca1edd3d227817b` | 10 | admin | annotation contracts and archive ref | blocked |
| `vebbaybi/Chains` | public | `main` | `main` | `6ada073d6793431c376b942ef45a73000fe781f2` | 870 | admin | attributed Sandy fixtures/specification, archive ref | prohibited |
| `vebbaybi/Lean` | public | `master` | 16 observed | `cd52034ddf55c0c9aa57264d2a148e563924100f` | 585979 | admin | external pinned dependency | prohibited |

The local Chainna and Chains commits equal their remote heads. The private
annotation source has no verified local checkout. License, tags, ignored
assets, secret scans, and full all-ref inventories remain required before
bundle or deletion readiness.

