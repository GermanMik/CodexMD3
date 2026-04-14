# Versioning Policy

## Canonical public version surface

`plugin/.codex-plugin/plugin.json` is the canonical public release version surface.

## Supporting version-bearing files

- `plugin/.codex-plugin/plugin.json`
- `mcp/manifest.json`
- `CHANGELOG.md`
- Git tag name
- GitHub Release title and notes draft

## Rule set

- The canonical source skill does not maintain an independent public version stream.
- MCP version inherits the plugin release version and must remain identical unless an explicit mapping policy is added.
- Version drift across release surfaces is a release failure.

## SemVer policy

- `MAJOR`: breaking changes to plugin contract, MCP contracts, or packaged capability behavior
- `MINOR`: backward-compatible capability additions
- `PATCH`: backward-compatible fixes, clarifications, and non-breaking improvements

## Pre-release tags

- `v2.0.0-rc.1`
- `v2.0.0-beta.1`

Use prerelease suffixes only when the release policy calls for pre-GA validation.
