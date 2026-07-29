# Canonical workspace migration

Status: **BLOCKED before clone**

Requested canonical path: `<FORAKILO_WORKTREE>`  
Current active path: `<LOCAL_SOURCE_PATH>`

The backup root exists and all three required source bundles verify. The
canonical product directory has not been created because local Forakilo HEAD
`71bc343a65cd5ee607ca16ef06f3d4298f67958a` is not yet recoverable from public
`origin/main`. A fresh clone now would omit both approved implementation
commits and would not satisfy the migration gate.

After remote publication is approved and verified, clone fresh, validate,
compare Git object IDs and tracked-file hashes, inspect untracked/ignored
requirements, and only then activate this path. All pre-migration local copies
remain preserved.

