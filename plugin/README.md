# Material 3 MD3 Workflows Plugin

This plugin packages the repo-local Material Design 3 capability for Codex.

## Boundary

- Canonical editable skill: `.agents/skills/material-3/`
- Bundled packaging artifact: `plugin/skills/material-3/`
- Optional deterministic MCP config: `plugin/.mcp.json`

Do not treat `plugin/skills/material-3/` as the primary authoring surface. Sync it from the canonical skill.

## Install

1. Keep the plugin inside this repository so `plugin/.mcp.json` can resolve `../mcp/server.py`.
2. Add or keep the marketplace entry in `.agents/plugins/marketplace.json`.
3. Install the local plugin from `./plugin`.

## Upgrade

1. Update `.agents/skills/material-3/` first.
2. Run `python scripts/sync_plugin_bundle.py`.
3. Run release validation in dry-run mode before tagging or publication.

## Rollback

1. Revert the canonical skill and release surfaces together.
2. Re-run `python scripts/sync_plugin_bundle.py`.
3. Re-run release validation to prove the rollback state is internally consistent.

## Internal distribution

The intended target is repo-local or internal marketplace distribution. If you extract the plugin outside the repo, update `.mcp.json` so its server path resolves correctly or copy the `mcp/` directory alongside the plugin and rewrite the command path.
