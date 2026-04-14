# Evidence for codex-material-3-stage-2-mcp

## Build summary
Implemented a deterministic, file-backed MD3 MCP layer with the required seven tools, machine-readable contracts, and a CLI harness for proof artifacts. Tool boundaries keep design reasoning in the skill layer and reserve MCP for facts, scaffolds, scoring, and consistency checks.

## Commands run
- `python mcp/cli.py lookup-token --category color --token-name primary`
- `python mcp/cli.py lookup-component --component navigation-rail --platform compose`
- `python mcp/cli.py platform-matrix --topic dynamic-color`
- `python mcp/cli.py layout-rule --rule adaptive-navigation --platform compose --window-class medium`
- `python mcp/cli.py theme-scaffold --seed-color "#6750A4" --platform compose --dark-mode paired --contrast standard --dynamic-color allowed`
- `python mcp/cli.py score-audit --findings-file .agent/tasks/codex-material-3-stage-2-mcp/raw/sample-findings.json`
- `python mcp/cli.py check-release-consistency --expected-version 1.0.0 --release-notes .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`

## Raw artifacts
- `raw/token-lookup-check.json`
- `raw/component-catalog-check.json`
- `raw/platform-matrix-check.json`
- `raw/layout-rule-check.json`
- `raw/theme-scaffold-check.json`
- `raw/md3-audit-score.json`
- `raw/release-consistency-check.json`
- `raw/sample-findings.json`

## Acceptance criteria mapping
- AC2.1 -> evidence: [mcp/README.md](/C:/Develop/Projects/CodexMD3/mcp/README.md), [tool-contracts.json](/C:/Develop/Projects/CodexMD3/mcp/contracts/tool-contracts.json)
- AC2.2 -> evidence: [server.py](/C:/Develop/Projects/CodexMD3/mcp/server.py), `raw/token-lookup-check.json`, `raw/component-catalog-check.json`, `raw/platform-matrix-check.json`, `raw/layout-rule-check.json`, `raw/theme-scaffold-check.json`, `raw/md3-audit-score.json`, `raw/release-consistency-check.json`
- AC2.3 -> evidence: [mcp/README.md](/C:/Develop/Projects/CodexMD3/mcp/README.md), [tool-contracts.json](/C:/Develop/Projects/CodexMD3/mcp/contracts/tool-contracts.json)
- AC2.4 -> evidence: `raw/*.json`, [cli.py](/C:/Develop/Projects/CodexMD3/mcp/cli.py)
- AC2.5 -> evidence: `raw/release-consistency-check.json`, [domain.py](/C:/Develop/Projects/CodexMD3/mcp/domain.py)

## Known limitations
- Theme scaffolding is deterministic and token-oriented; final aesthetic judgment remains outside the MCP boundary.
- Release consistency checks are repo-local and do not publish or mutate git state.

## Release evidence
- current version: `1.0.0`
- target version: `1.0.0`
- changelog updated: indirectly checked by `raw/release-consistency-check.json`
- release commit draft: indirectly checked by `raw/release-consistency-check.json`
- tag draft: indirectly checked by `raw/release-consistency-check.json`
- release notes draft: `.agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`
