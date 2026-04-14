# Evidence for codex-material-3-stage-3-plugin

## Build summary
Created the installable plugin bundle, bundled MCP config, marketplace metadata, and a script-driven packaging sync path from the canonical skill into `plugin/skills/material-3/`.

## Commands run
- `python scripts/sync_plugin_bundle.py`
- `python scripts/sync_plugin_bundle.py --check`
- `Get-Content -Raw plugin/.codex-plugin/plugin.json`
- `Get-Content -Raw plugin/.mcp.json`
- `Get-Content -Raw .agents/plugins/marketplace.json`
- `Get-ChildItem -Recurse plugin/skills/material-3`

## Raw artifacts
- `raw/packaging-sync-check.txt`
- `raw/plugin-manifest-check.json`
- `raw/plugin-mcp-check.json`
- `raw/marketplace-check.json`
- `raw/bundled-skill-file-list.txt`

## Acceptance criteria mapping
- AC3.1 -> evidence: [plugin.json](/C:/Develop/Projects/CodexMD3/plugin/.codex-plugin/plugin.json), `raw/plugin-manifest-check.json`
- AC3.2 -> evidence: `raw/bundled-skill-file-list.txt`
- AC3.3 -> evidence: [plugin/README.md](/C:/Develop/Projects/CodexMD3/plugin/README.md), [packaging-sync-policy.md](/C:/Develop/Projects/CodexMD3/docs/packaging-sync-policy.md)
- AC3.4 -> evidence: [plugin/.mcp.json](/C:/Develop/Projects/CodexMD3/plugin/.mcp.json), `raw/plugin-mcp-check.json`
- AC3.5 -> evidence: [marketplace.json](/C:/Develop/Projects/CodexMD3/.agents/plugins/marketplace.json), `raw/marketplace-check.json`
- AC3.6 -> evidence: [packaging-sync-policy.md](/C:/Develop/Projects/CodexMD3/docs/packaging-sync-policy.md), `raw/packaging-sync-check.txt`, [sync_plugin_bundle.py](/C:/Develop/Projects/CodexMD3/scripts/sync_plugin_bundle.py)

## Known limitations
- The plugin distribution path is repo-local and uses `./plugin` rather than the generic `./plugins/<name>` helper convention because the task fixed the bundle root explicitly.

## Release evidence
- current version: `1.0.0`
- target version: `1.0.0`
- changelog updated: indirectly relevant
- release commit draft: not stage-relevant
- tag draft: not stage-relevant
- release notes draft: not stage-relevant
