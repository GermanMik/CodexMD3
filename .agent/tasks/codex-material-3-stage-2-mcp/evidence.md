# Evidence for codex-material-3-stage-2-mcp

## Build summary
Collected deterministic MD3 MCP raw JSON artifacts with a repo-local builder pass. A distinct fresh-verifier pass is required before treating the stage as complete.

## Proof policy
- builder identity: `stage2-mcp-builder`
- builder outputs are evidence only, not certification
- raw MCP artifacts are stored as JSON under `raw/`
- verifier identity must differ from builder identity
- fresh verification is required after evidence collection

## Commands run
- `python mcp/cli.py lookup-token --category color --token-name primary`
- `python mcp/cli.py lookup-component --component navigation-rail --platform compose`
- `python mcp/cli.py platform-matrix --topic dynamic-color`
- `python mcp/cli.py layout-rule --rule adaptive-navigation --platform compose --window-class medium`
- `python mcp/cli.py theme-scaffold --seed-color "#6750A4" --platform compose --dark-mode paired --contrast standard --dynamic-color allowed`
- `python mcp/cli.py score-audit --findings-file .agent/tasks/codex-material-3-stage-2-mcp/raw/sample-findings.json`
- `python mcp/cli.py check-release-consistency --expected-version 1.0.1 --release-notes .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`

## Raw artifacts
- `.agent/tasks/codex-material-3-stage-2-mcp/raw/token-lookup-check.json` (`008b8f33adb0`)
- `.agent/tasks/codex-material-3-stage-2-mcp/raw/component-catalog-check.json` (`9e5fde25f6b4`)
- `.agent/tasks/codex-material-3-stage-2-mcp/raw/platform-matrix-check.json` (`150840bd8118`)
- `.agent/tasks/codex-material-3-stage-2-mcp/raw/layout-rule-check.json` (`8c8ac699c267`)
- `.agent/tasks/codex-material-3-stage-2-mcp/raw/theme-scaffold-check.json` (`d162cd022676`)
- `.agent/tasks/codex-material-3-stage-2-mcp/raw/md3-audit-score.json` (`19d34b0d77db`)
- `.agent/tasks/codex-material-3-stage-2-mcp/raw/release-consistency-check.json` (`e9cc0526b81d`)

## Acceptance criteria mapping
- AC2.1 -> `mcp/README.md`, `mcp/contracts/tool-contracts.json`
- AC2.2 -> `mcp/server.py`, `raw/*.json`
- AC2.3 -> `mcp/README.md`, `.agents/skills/material-3/SKILL.md`, `mcp/contracts/tool-contracts.json`
- AC2.4 -> `evidence.json`, `raw/*.json`, `mcp/cli.py`
- AC2.5 -> `raw/release-consistency-check.json`, `mcp/domain.py`

## Release evidence
- current version: `1.0.1`
- target version: `1.0.1`
- tag draft: `v1.0.1`
- release commit draft: `release: v1.0.1`
- release notes draft: `.agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`
