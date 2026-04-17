# Evidence for codex-material-3-stage-4-release

## Build summary
Validated the `v1.0.1` release contour end-to-end: version-bearing files were aligned, packaging sync remained clean, the GitHub Release was published, and repo-local post-release evidence was captured.

## Commands run
- `python scripts/prepare_release.py --version 1.0.1 --dry-run`
- `python scripts/prepare_release.py --version 1.0.1 --dry-run --notes-out .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`
- `python scripts/sync_plugin_bundle.py --check`
- `python scripts/validate_release.py --expected-version 1.0.1 --release-notes .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`
- `rg -n "^## \[1\.0\.1\] - 2026-04-17$|^### Added$|^### Changed$|^### Fixed$|^### Removed$|^### Security$|^### Migration Notes$" CHANGELOG.md`
- `gh release view v1.0.1 --json body,isDraft,isPrerelease,name,publishedAt,tagName,targetCommitish,url`
- `git rev-list -n 1 v1.0.1`

## Raw artifacts
- `raw/release-version-check.txt`
- `raw/changelog-check.txt`
- `raw/tag-check.txt`
- `raw/packaging-sync-check.txt`
- `raw/release-notes-draft.md`
- `raw/release-validation.json`
- `raw/github-release-url.txt`
- `raw/github-release-view.json`
- `raw/post-release-check.txt`

## Acceptance criteria mapping
- AC4.1 -> evidence: [versioning-policy.md](/C:/Develop/Projects/CodexMD3/docs/versioning-policy.md), [plugin.json](/C:/Develop/Projects/CodexMD3/plugin/.codex-plugin/plugin.json), [tool-contracts.json](/C:/Develop/Projects/CodexMD3/mcp/contracts/tool-contracts.json)
- AC4.2 -> evidence: [release-policy.md](/C:/Develop/Projects/CodexMD3/docs/release-policy.md), [release-checklist.md](/C:/Develop/Projects/CodexMD3/docs/release-checklist.md), `raw/release-validation.json`, `raw/post-release-check.txt`
- AC4.3 -> evidence: [CHANGELOG.md](/C:/Develop/Projects/CodexMD3/CHANGELOG.md), `raw/changelog-check.txt`
- AC4.4 -> evidence: [versioning-policy.md](/C:/Develop/Projects/CodexMD3/docs/versioning-policy.md), `raw/tag-check.txt`, `raw/release-validation.json`
- AC4.5 -> evidence: [github-release-flow.md](/C:/Develop/Projects/CodexMD3/docs/github-release-flow.md), [.github/workflows/publish-release.yml](/C:/Develop/Projects/CodexMD3/.github/workflows/publish-release.yml), `raw/github-release-view.json`
- AC4.6 -> evidence: [packaging-sync-policy.md](/C:/Develop/Projects/CodexMD3/docs/packaging-sync-policy.md), `raw/packaging-sync-check.txt`
- AC4.7 -> evidence: `raw/release-validation.json`, [plugin.json](/C:/Develop/Projects/CodexMD3/plugin/.codex-plugin/plugin.json), [mcp/manifest.json](/C:/Develop/Projects/CodexMD3/mcp/manifest.json), [tool-contracts.json](/C:/Develop/Projects/CodexMD3/mcp/contracts/tool-contracts.json)

## Known limitations
- `validate_release.py` proves repository alignment and policy compliance, but GitHub publication details remain in separate raw artifacts instead of being folded into RC1-RC12.

## Release evidence
- current version: `1.0.1`
- target version: `1.0.1`
- release commit: `release: v1.0.1`
- tag: `v1.0.1`
- release URL: `https://github.com/GermanMik/CodexMD3/releases/tag/v1.0.1`
