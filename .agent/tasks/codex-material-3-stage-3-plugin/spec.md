# Task: codex-material-3-stage-3-plugin

## Original task statement
Package the Material 3 skill and optional MCP into an installable Codex plugin while preserving the canonical skill as the sole editable source and treating the bundled copy as a derived packaging artifact.

## Scope
- Create `plugin/.codex-plugin/plugin.json`.
- Create `plugin/.mcp.json`.
- Create bundled skill files under `plugin/skills/material-3/`.
- Create install and internal distribution documentation plus marketplace entry.
- Define and implement a sync path from canonical skill to bundled plugin skill.

## Out of scope
- Publishing to an official public plugin directory.
- Treating bundled files as the primary authoring surface.
- Runtime dependency management outside the repo-local plugin bundle.

## Acceptance criteria
- AC3.1: A plugin manifest exists and represents the repository as an MD3 workflow plugin for Codex.
- AC3.2: A bundled skill copy exists under `plugin/skills/material-3/`.
- AC3.3: The bundled skill copy is explicitly documented and treated as a packaging artifact derived from the canonical source skill.
- AC3.4: MCP config is bundled in `plugin/.mcp.json` or explicitly documented as optional while remaining release-consistent.
- AC3.5: A local/internal marketplace example exists under `.agents/plugins/marketplace.json`.
- AC3.6: Packaging sync rules are documented and verifiable with repo-local commands/artifacts.

## Constraints
- Canonical behavior changes must land in `.agents/skills/material-3/` first.
- Bundled plugin files must be synchronized, not hand-maintained as normal workflow.
- No stale bundled files may remain after sync.
- Install/upgrade/rollback concepts must be explicit enough for internal distribution use.

## Assumptions
- A repo-local plugin directory at `plugin/` is acceptable even though the bootstrap helper defaults to `plugins/<name>`.
- Marketplace metadata can reference the local plugin path deterministically.
- Sync can be implemented with a repo-local script rather than external packaging tools.

## Risks
- Plugin manifest metadata may diverge from release docs or `.mcp.json`.
- Bundled skill copies may go stale if sync is not script-driven and validated.
- Marketplace entry shape may be incomplete if installation/auth/category fields are omitted.

## Verification plan
- V1: Inspect plugin manifest, bundled skill tree, `.mcp.json`, and marketplace metadata for required structure and MD3-specific positioning.
- V2: Run sync and verification commands that compare canonical and bundled skill states and detect stale files.
- V3: Produce fresh verifier mappings from AC3.x criteria to manifest files, sync outputs, and marketplace artifacts.

## Evidence expectations
- E1: Raw artifacts prove packaging sync, manifest presence, marketplace entry presence, and bundled MCP configuration.
- E2: Evidence clearly distinguishes canonical source files from bundled packaging artifacts.
- E3: Verifier identifies any stale bundle, missing metadata, or undocumented sync boundary.

## Minimal safe implementation boundary
Implement only the plugin files, sync mechanism, and install/distribution documentation needed to ship the MD3 capability as an installable bundle. Avoid adding unrelated plugins or distribution channels.
