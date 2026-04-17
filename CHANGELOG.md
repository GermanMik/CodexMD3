# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-04-17
### Added
- Repo-local `scripts/stage2_mcp_proof.py` builder/verifier harness for `codex-material-3-stage-2-mcp`.
- Machine-readable proof-loop expectations in `mcp/contracts/tool-contracts.json` for JSON-only artifacts, fresh verification, and builder/verifier separation.

### Changed
- Clarified MCP vs skill-layer boundaries in the canonical Material 3 skill and `mcp/README.md`.
- Extended release consistency checks to include `mcp/contracts/tool-contracts.json` as a version-bearing surface.

### Fixed
- Stage-2 MCP evidence now records all seven required tool commands, including platform matrix and layout rule checks.
- Release version bump tooling now keeps plugin, MCP manifest, and MCP contracts versions aligned.

### Removed
- None.

### Security
- No credentials or external tokens are stored in repo artifacts.

### Migration Notes
- Run `python scripts/stage2_mcp_proof.py build` followed by `python scripts/stage2_mcp_proof.py verify` before marking `codex-material-3-stage-2-mcp` complete.

## [1.0.0] - 2026-04-14
### Added
- Canonical Material Design 3 skill for Codex with component, theme, layout, scaffold, and audit modes.
- Deterministic Material 3 MCP layer with lookup, scaffolding, scoring, and release-consistency tools.
- Installable plugin bundle, marketplace entry, sync policy, and release-management scripts.

### Changed
- Established repo-task-proof-loop as the required control plane for MD3 capability delivery and release work.

### Fixed
- N/A for initial release.

### Removed
- None.

### Security
- No credentials or external tokens are stored in repo artifacts.

### Migration Notes
- Treat `.agents/skills/material-3/` as canonical source and `plugin/skills/material-3/` as derived packaging output.
