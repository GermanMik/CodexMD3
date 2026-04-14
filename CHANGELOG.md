# Changelog

All notable changes to this project will be documented in this file.

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
