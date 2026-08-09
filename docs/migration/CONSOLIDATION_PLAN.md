# Consolidation plan

1. Complete bounded inventory of every local and remote source, including
   branches, tags, ignored files, licensing, secrets scan, and dirty state.
2. Create and verify external Git bundles. Preserve wrapper untracked content
   separately because an empty Git repository cannot bundle uncommitted files.
3. Push source commits as unrelated archival refs without merging them into
   `main`; record hashes and checksums.
4. Reconcile accepted Chainna decisions under Foreightkillo attribution and migrate
   Sandy/ChainCrawlr behavior through specifications, fixtures, and clean-room
   implementation.
5. Implement and verify the modular monolith in small work-unit commits.
6. Move the verified canonical checkout to the approved canonical worktree without an
   outer or nested repository.
7. Produce migration acceptance, data-loss, feature-parity, and deletion
   readiness evidence.
8. Only if deletion readiness is PASS, deprecate, re-bundle, verify, and delete
   Chainna and the private annotation source repository. Chains and Lean remain
   untouched.

