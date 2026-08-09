# Private source preservation policy

The source identified publicly as
`<PRIVATE_ANNOTATION_SOURCE_REPOSITORY>` is intentionally excluded from public
Foreightkillo history, archive refs, and tags.

Its complete history is retained in a verified private all-ref bundle. Exact
repository identity, clone URL, source path, bundle path, and local mapping
remain only in private evidence outside Foreightkillo. Public records may contain
the approved source commit fingerprint, bundle checksum, classifications,
verification outcome, and migrated behavior.

## Publicly migrated behavior

- immutable annotation proposals;
- deterministic, local-model, and optional provider proposal sources;
- confidence, provenance, dataset linkage, and usage accounting;
- human review with immutable reviewer decisions;
- disagreement retention and stable proposal identity.

## Rejected or deferred behavior

- image-specific YOLO and OpenCV preprocessing;
- COCO, YOLO, and Label Studio exporters;
- configuration-embedded API keys;
- import-time hard dependency termination;
- provider proposals, retry state, redaction, and budget enforcement beyond
  the current provider-neutral contracts remain implementation gaps.

No private source branch, tag, bundle, commit tree, remote name, or backup ref
may be pushed to the public Foreightkillo repository.

