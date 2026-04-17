# Evidence for codex-material-3-stage-3-plugin

## Build summary
Collected repo-local plugin packaging artifacts, synchronized the bundled Material 3 skill from the canonical source, and recorded a builder-only evidence pass that still requires a distinct fresh verifier.

## Proof policy
- builder identity: `stage3-plugin-builder`
- builder outputs are evidence only, not certification
- raw plugin packaging artifacts are stored as JSON under `raw/`
- verifier identity must differ from builder identity
- fresh verification is required after evidence collection

## Commands run
- `python scripts/sync_plugin_bundle.py`
- `python scripts/sync_plugin_bundle.py --check`
- `Get-Content -Raw plugin/.codex-plugin/plugin.json`
- `Get-Content -Raw plugin/.mcp.json`
- `Get-Content -Raw .agents/plugins/marketplace.json`
- `Get-ChildItem -Recurse .agents/skills/material-3,plugin/skills/material-3`

## Raw artifacts
- `.agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-run.json` (`466c7e9aaa94`)
- `.agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-check.json` (`b453e6d359bc`)
- `.agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-manifest-check.json` (`e1c08d4e6da3`)
- `.agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-mcp-check.json` (`e9918d102184`)
- `.agent/tasks/codex-material-3-stage-3-plugin/raw/marketplace-check.json` (`c69e225d8109`)
- `.agent/tasks/codex-material-3-stage-3-plugin/raw/canonical-bundle-hashes.json` (`b43a7a58c773`)

## Acceptance criteria mapping
- AC3.1 -> `plugin/.codex-plugin/plugin.json`, `raw/plugin-manifest-check.json`
- AC3.2 -> `raw/canonical-bundle-hashes.json`
- AC3.3 -> `plugin/README.md`, `docs/packaging-sync-policy.md`
- AC3.4 -> `plugin/.mcp.json`, `raw/plugin-mcp-check.json`
- AC3.5 -> `.agents/plugins/marketplace.json`, `raw/marketplace-check.json`
- AC3.6 -> `scripts/sync_plugin_bundle.py`, `raw/bundle-sync-run.json`, `raw/bundle-sync-check.json`, `raw/canonical-bundle-hashes.json`, `docs/packaging-sync-policy.md`

## Release evidence
- current version: `1.0.2`
- target version: `1.0.2`
- tag draft: `v1.0.2`
- release commit draft: `release: v1.0.2`
