# Evidence for codex-material-3-stage-4-release

## Build summary
Collected repo-local release artifacts, captured published GitHub release state, and recorded a builder-only evidence pass that still requires a distinct fresh verifier.

## Proof policy
- builder identity: `stage4-release-builder`
- builder outputs are evidence only, not certification
- release notes are stored as markdown and all other raw checks are stored as structured JSON
- verifier identity must differ from builder identity
- fresh verification is required after evidence collection

## Commands run
- `python scripts/prepare_release.py --version 1.0.3 --dry-run`
- `Copy release notes from .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-v1.0.3.md into raw/release-notes-draft.md and raw/release-notes-v1.0.3.md`
- `python scripts/sync_plugin_bundle.py --check`
- `python scripts/validate_release.py --expected-version 1.0.3 --release-notes .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`
- `Get-Content -Raw CHANGELOG.md`
- `git rev-parse v1.0.3^{} && git ls-remote --tags origin refs/tags/v1.0.3 refs/tags/v1.0.3^{}`
- `gh release view v1.0.3 --json body,isDraft,isPrerelease,name,publishedAt,tagName,targetCommitish,url`
- `git merge-base --is-ancestor $(git rev-parse v1.0.3^{}) origin/main`

## Raw artifacts
- `.agent/tasks/codex-material-3-stage-4-release/raw/release-version-check.json` (`c57406a43be4`)
- `.agent/tasks/codex-material-3-stage-4-release/raw/changelog-check.json` (`f91f808ca2d3`)
- `.agent/tasks/codex-material-3-stage-4-release/raw/tag-check.json` (`2ae45b878516`)
- `.agent/tasks/codex-material-3-stage-4-release/raw/packaging-sync-check.json` (`b453e6d359bc`)
- `.agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md` (`4f5e5fbd7165`)
- `.agent/tasks/codex-material-3-stage-4-release/raw/release-notes-v1.0.3.md` (`4f5e5fbd7165`)
- `.agent/tasks/codex-material-3-stage-4-release/raw/release-validation.json` (`81818c1d1cdf`)
- `.agent/tasks/codex-material-3-stage-4-release/raw/github-release-view.json` (`9c66f5f7db92`)
- `.agent/tasks/codex-material-3-stage-4-release/raw/github-release-url.txt` (`79269507b65a`)
- `.agent/tasks/codex-material-3-stage-4-release/raw/post-release-check.json` (`9d5aa14b9247`)

## Acceptance criteria mapping
- AC4.1 -> `docs/versioning-policy.md`, `plugin/.codex-plugin/plugin.json`, `mcp/manifest.json`, `mcp/contracts/tool-contracts.json`, `raw/release-version-check.json`
- AC4.2 -> `docs/release-policy.md`, `docs/release-checklist.md`, `raw/release-validation.json`, `raw/post-release-check.json`
- AC4.3 -> `CHANGELOG.md`, `raw/changelog-check.json`
- AC4.4 -> `docs/versioning-policy.md`, `raw/tag-check.json`, `raw/release-validation.json`
- AC4.5 -> `docs/github-release-flow.md`, `.github/workflows/publish-release.yml`, `raw/release-notes-v<version>.md`, `raw/github-release-view.json`, `raw/post-release-check.json`
- AC4.6 -> `docs/packaging-sync-policy.md`, `raw/packaging-sync-check.json`
- AC4.7 -> `raw/release-validation.json`, `plugin/.codex-plugin/plugin.json`, `mcp/manifest.json`, `mcp/contracts/tool-contracts.json`, `CHANGELOG.md`

## Release evidence
- current version: `1.0.3`
- target version: `1.0.3`
- release commit: `release: v1.0.3`
- tag: `v1.0.3`
- release URL: `https://github.com/GermanMik/CodexMD3/releases/tag/v1.0.3`
