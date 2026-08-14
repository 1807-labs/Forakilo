# Canonical workspace activation

Date: 2026-07-29  
Status: **ACTIVE**

The canonical development checkout at `<FOREIGHTKILLO_WORKTREE>` was created by a
fresh clone of `https://github.com/1807-labs/Foreightkillo.git`. It was not copied
from a legacy or cloud-synced workspace.

## Repository verification

| Check | Result |
|---|---|
| Root | `<FOREIGHTKILLO_WORKTREE>` |
| Origin | canonical public Foreightkillo repository |
| Branch/upstream | `main` / `origin/main` |
| HEAD and remote main | `2697a22e09a34070e1382ef8f5fd0a14ce404bb1` |
| Worktree | clean |
| Unexpected nested `.git` directories | 0 |
| Untracked files after clone | 0 |
| Private metadata and source identity matches | 0 |
| Secret-pattern matches | 0 |

## Reproduction commands

The following commands were run from `<FOREIGHTKILLO_WORKTREE>`:

```text
scripts\setup_dev.ps1    # Windows: run in PowerShell
scripts/setup_dev.sh     # Unix: run in a POSIX shell
python -m json.tool docs/migration/SOURCE_PRESERVATION_MANIFEST.json
python -m pytest -p no:cacheprovider
ruff check .
pyright
```

Results: six tests passed, Ruff passed, Pyright strict reported zero errors,
and the preservation manifest parsed successfully.

## Source comparison

The old and canonical checkouts each contained 156 tracked index entries.
`git ls-files -s` output matched exactly, proving path-independent Git object
identity for every tracked file. Neither checkout had required untracked
source. No ignored configuration, fixture, dataset, model, notebook, or
experiment artifact required for reproduction existed only in the old
checkout.

Generated environments and caches were excluded from the comparison. The old
checkout remains preserved and is not canonical.

