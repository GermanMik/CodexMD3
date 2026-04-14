# Release Checklist

## Pre-build

- target scope frozen
- target version justified
- canonical skill updated

## Packaging

- `python scripts/sync_plugin_bundle.py`
- no stale bundled files remain
- bundled `.mcp.json` is still correct

## Metadata

- plugin manifest version correct
- MCP manifest version correct
- `CHANGELOG.md` updated
- release notes draft present

## Verification

- `python scripts/validate_release.py --expected-version <version> --release-notes <path>`
- verifier PASS on RC1-RC12

## Publication

- release commit message follows `release: vX.Y.Z`
- tag follows `vX.Y.Z`
- GitHub Release created from validated notes

## Post-release

- published tag matches manifest and changelog
- GitHub Release body matches draft
- rollback path recorded if a hotfix is needed
