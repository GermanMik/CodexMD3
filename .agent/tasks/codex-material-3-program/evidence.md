# Evidence for codex-material-3-program

## Build summary
Implemented the four required stages: canonical MD3 skill, deterministic MD3 MCP layer, installable plugin packaging, and versioned release workflow. Synchronized the bundled plugin skill from the canonical source and collected stage-local raw evidence.

## Commands run
- `python scripts/sync_plugin_bundle.py`
- `python C:\Users\tikta\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents/skills/material-3`
- `python mcp/cli.py lookup-token --category color --token-name primary`
- `python mcp/cli.py theme-scaffold --seed-color "#6750A4" --platform compose --dark-mode paired --contrast standard --dynamic-color allowed`
- `python scripts/prepare_release.py --version 1.0.0 --dry-run --notes-out .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`
- `python scripts/validate_release.py --expected-version 1.0.0 --bump patch --release-notes .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`

## Raw artifacts
- `raw/program-file-tree.txt`
- `raw/program-summary.txt`
- `raw/git-status.txt`
- `.agent/tasks/codex-material-3-stage-1-skill/raw/*`
- `.agent/tasks/codex-material-3-stage-2-mcp/raw/*`
- `.agent/tasks/codex-material-3-stage-3-plugin/raw/*`
- `.agent/tasks/codex-material-3-stage-4-release/raw/*`

## Acceptance criteria mapping
- AC1 -> evidence: `.agent/tasks/codex-material-3-program/spec.md`, `raw/program-file-tree.txt`
- AC2 -> evidence: `.agent/tasks/codex-material-3-stage-1-skill/evidence.md`, `.agent/tasks/codex-material-3-stage-2-mcp/evidence.md`, `.agent/tasks/codex-material-3-stage-3-plugin/evidence.md`, `.agent/tasks/codex-material-3-stage-4-release/evidence.md`
- AC3 -> evidence: [SKILL.md](/C:/Develop/Projects/CodexMD3/.agents/skills/material-3/SKILL.md), [plugin.json](/C:/Develop/Projects/CodexMD3/plugin/.codex-plugin/plugin.json), [packaging-sync-policy.md](/C:/Develop/Projects/CodexMD3/docs/packaging-sync-policy.md)
- AC4 -> evidence: `.agent/tasks/*/spec.md`, `.agent/tasks/*/evidence.md`, `.agent/tasks/*/raw/*`
- AC5 -> evidence: `.agent/tasks/codex-material-3-stage-3-plugin/raw/packaging-sync-check.txt`
- AC6 -> evidence: `.agent/tasks/codex-material-3-stage-4-release/raw/release-validation.json`, [versioning-policy.md](/C:/Develop/Projects/CodexMD3/docs/versioning-policy.md), [release-policy.md](/C:/Develop/Projects/CodexMD3/docs/release-policy.md)
- AC7 -> evidence: [SKILL.md](/C:/Develop/Projects/CodexMD3/.agents/skills/material-3/SKILL.md), `.agent/tasks/codex-material-3-stage-2-mcp/raw/token-lookup-check.json`, `.agent/tasks/codex-material-3-stage-2-mcp/raw/md3-audit-score.json`

## Known limitations
- GitHub publication was prepared and workflow-backed but not executed in this session.
- The plugin `.mcp.json` is repo-relative for internal distribution; extracted standalone installs must rewrite the MCP path.

## Release evidence
- current version: `1.0.0`
- target version: `1.0.0`
- changelog updated: yes
- release commit draft: `release: v1.0.0`
- tag draft: `v1.0.0`
- release notes draft: `.agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md`
