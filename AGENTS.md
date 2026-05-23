# AGENTS

Instructions for AI coding agents in this repository. For project overview, start with `README.md`.

## Project Context

- CodexMD3 is a repo-local Material Design 3 capability for Codex.
- Canonical skill source: `.agents/skills/material/`.
- Plugin bundle: `plugin/`.
- Deterministic MCP layer: `mcp/`.
- Release and packaging docs live under `docs/`.

## Working Rules

- Do not edit the bundled plugin skill first. Update `.agents/skills/material/` and then sync the bundle with `python scripts/sync_plugin_bundle.py`.
- Preserve the release model and validation flow documented in `docs/release-policy.md`, `docs/release-checklist.md`, and `docs/github-release-flow.md`.
- Keep changes small and reviewable.
- Run the smallest relevant validation for the changed layer.

## Graphify

- Graphify is optional. Use it for architecture, dependency, module-relationship, or large repository navigation tasks; do not run heavy graph generation automatically.
- Keep Graphify output narrow: prefer `graphify query "<specific question>" --budget 1200`, `graphify explain "<node>"`, or `graphify path "<A>" "<B>"` before reading full reports or doing broad source searches.
- If the graph answer is too broad, refine by feature, domain, package, path, or named component and rerun with a smaller budget; do not paste large raw Graphify output into final answers.
- For web/plugin code, scope Graphify to source-only paths such as `.agents/skills/material`, `plugin`, `mcp`, `scripts`, and relevant `docs`.
- Exclude web/build noise from Graphify corpora: `node_modules`, `.next`, `dist`, `build`, `out`, `coverage`, `playwright-report`, `test-results`, `storybook-static`, static/public asset dumps, generated files, screenshots, `graphify-out`, and local caches.
- Run Graphify on the smallest package/subtree that matches the task; widen only after the scoped graph and direct source reads are insufficient.
