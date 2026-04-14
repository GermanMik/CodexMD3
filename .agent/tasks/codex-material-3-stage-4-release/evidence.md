# Evidence for codex-material-3-stage-4-release

## Build summary
Implemented versioning, release, packaging sync, hotfix, and GitHub publication policies; added changelog and release helper scripts; and validated RC1-RC12 against the current repo release surface.

## Commands run
- `python scripts/prepare_release.py --bump patch --dry-run`
- `python scripts/prepare_release.py --version 1.0.0 --dry-run --notes-out .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`
- `python scripts/sync_plugin_bundle.py --check`
- `python scripts/validate_release.py --expected-version 1.0.0 --bump patch --release-notes .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`
- `rg -n "^## \\[1\\.0\\.0\\] - 2026-04-14$|^### Added$|^### Changed$|^### Fixed$|^### Removed$|^### Security$|^### Migration Notes$" CHANGELOG.md`

## Raw artifacts
- `raw/release-version-check.txt`
- `raw/changelog-check.txt`
- `raw/tag-check.txt`
- `raw/packaging-sync-check.txt`
- `raw/release-notes-draft.md`
- `raw/release-validation.json`

## Acceptance criteria mapping
- AC4.1 -> evidence: [versioning-policy.md](/C:/Develop/Projects/CodexMD3/docs/versioning-policy.md), [plugin.json](/C:/Develop/Projects/CodexMD3/plugin/.codex-plugin/plugin.json)
- AC4.2 -> evidence: [release-policy.md](/C:/Develop/Projects/CodexMD3/docs/release-policy.md), [release-checklist.md](/C:/Develop/Projects/CodexMD3/docs/release-checklist.md), `raw/release-validation.json`
- AC4.3 -> evidence: [CHANGELOG.md](/C:/Develop/Projects/CodexMD3/CHANGELOG.md), `raw/changelog-check.txt`
- AC4.4 -> evidence: [versioning-policy.md](/C:/Develop/Projects/CodexMD3/docs/versioning-policy.md), `raw/tag-check.txt`, `raw/release-validation.json`
- AC4.5 -> evidence: [github-release-flow.md](/C:/Develop/Projects/CodexMD3/docs/github-release-flow.md), [.github/workflows/publish-release.yml](/C:/Develop/Projects/CodexMD3/.github/workflows/publish-release.yml)
- AC4.6 -> evidence: [packaging-sync-policy.md](/C:/Develop/Projects/CodexMD3/docs/packaging-sync-policy.md), `raw/packaging-sync-check.txt`
- AC4.7 -> evidence: `raw/release-validation.json`, [mcp/manifest.json](/C:/Develop/Projects/CodexMD3/mcp/manifest.json), [plugin.json](/C:/Develop/Projects/CodexMD3/plugin/.codex-plugin/plugin.json)

## Known limitations
- GitHub publication path is documented and workflow-backed but not executed in this local session.
- RC2 is proven via dry-run next-version planning rather than an actual bump application.

## Release evidence
- current version: `1.0.0`
- target version: `1.0.0`
- changelog updated: yes
- release commit draft: `release: v1.0.0`
- tag draft: `v1.0.0`
- release notes draft: `raw/release-notes-draft.md`
