# Packaging Sync Policy

## Source of truth

- Canonical skill: `.agents/skills/material/`
- Bundled plugin skill: `plugin/skills/material/`

## Rules

- Make behavior changes in the canonical skill first.
- Synchronize the bundled skill with `python scripts/sync_plugin_bundle.py`.
- Do not hand-edit bundled skill files during normal authoring.
- Fail release validation when the bundled skill differs from canonical source.

## Proof

- The sync script must remove stale bundle files.
- The sync check must compare file content hashes, not only filenames.
- Fresh verification must prove sync before release signoff.
