# Private annotation source to Forakilo matrix

Source: `<PRIVATE_ANNOTATION_SOURCE_REPOSITORY>` at commit
`6e461471eb4d18fafe9690953ca1edd3d227817b`.

| Source behavior | Classification | Forakilo treatment |
|---|---|---|
| Deterministic seeded dataset splitting | adapted | chronological/purged market datasets replace random image splitting |
| Model-generated labels | adapted | immutable proposals with confidence and provenance; never truth |
| Validation and duplicate suppression | adopted | schema validation and stable proposal identities |
| Human-review export concept | adapted | explicit review state and reviewer decision contracts |
| YOLO/OpenCV image preprocessing | rejected | unrelated to quantitative market annotation MVP |
| COCO/YOLO/Label Studio exporters | archived | reference only; market annotations use versioned JSON contracts |
| API keys embedded in configuration | rejected | provider secrets are external and redacted |
| Import-time hard dependency exits | rejected | optional adapters fail locally and do not prevent local-only operation |

