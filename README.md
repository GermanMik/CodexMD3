# CodexMD3

Repo-local Material Design 3 capability for Codex.

CodexMD3 packages three layers that work together:

- a canonical `material` skill for MD3-specific reasoning
- a deterministic MCP layer for lookups, scaffolds, scoring, and release checks
- a local plugin bundle that makes the capability installable in Codex

The project is designed for internal or repo-local use. It is not a generic design-system plugin and it does not try to replace product judgment with static rules.

## What You Use It For

Use CodexMD3 when you want Codex to stay grounded in Material Design 3 instead of falling back to generic UI advice.

Typical use cases:

- choose the right MD3 component for a screen or flow
- scaffold a Compose-first MD3 screen or shell
- generate or tune an MD3 theme from a seed color
- adapt navigation and layout for compact, medium, and expanded widths
- audit an existing UI for MD3 compliance and get remediation steps

## How To Use CodexMD3

### 1. Keep the repo local

Clone this repository and keep the plugin inside the repo so the bundled MCP config can resolve the local server path.

### 2. Install the local plugin

The local marketplace entry lives in `.agents/plugins/marketplace.json` and points to `./plugin`.

In Codex:

1. keep or add the marketplace entry from this repo
2. install the local plugin `material-3-md3-workflows`
3. keep the repository path stable so `plugin/.mcp.json` can resolve `../mcp/server.py`

### 3. Trigger the skill when the task is MD3-specific

Use `$material` when the request is explicitly about Material Design 3 or Material You.

Good examples:

- `$material build a Compose Material 3 settings screen`
- `$material generate an MD3 theme from seed color #6750A4`
- `$material adapt this tablet shell to use navigation rail at medium width`
- `$material audit this screen for MD3 compliance`

Do not use it for generic frontend cleanup, brand work unrelated to MD3, or broad UI opinions with no Material 3 target.

### 4. Work in one primary mode

The skill is structured around five modes:

- `component`: pick or validate MD3 components
- `theme`: generate or refine theme tokens and visual roles
- `layout`: choose responsive rules, insets, and navigation adaptation
- `scaffold`: assemble a screen or app shell
- `audit`: score an existing UI and propose the smallest safe fixes

If a task spans multiple areas, choose one primary mode and keep the second one secondary.

## Architecture

### Canonical skill

- Source of truth: `.agents/skills/material/`
- Purpose: MD3-specific reasoning, decisions, tradeoffs, and user-facing recommendations

### Deterministic MCP layer

- Path: `mcp/`
- Purpose: file-backed lookups, theme scaffolds, audit scorecards, and release-consistency checks

Run the MCP server locally:

```powershell
python mcp/server.py
```

Use the CLI harness for deterministic local checks:

```powershell
python mcp/cli.py lookup-token --category color --token-name primary
python mcp/cli.py lookup-component --component navigation-rail --platform compose
python mcp/cli.py theme-scaffold --seed-color "#6750A4"
python mcp/cli.py check-release-consistency --expected-version 1.0.3 --release-notes path/to/release-notes.md
```

### Plugin bundle

- Path: `plugin/skills/material/`
- Purpose: installable packaging artifact for Codex

Do not edit the bundled skill first. Update the canonical skill and then sync the bundle:

```powershell
python scripts/sync_plugin_bundle.py
```

## Repo Layout

- `.agents/skills/material/`: canonical skill and references
- `plugin/`: installable local plugin bundle
- `mcp/`: deterministic support layer and contracts
- `scripts/`: sync, validation, and release tooling
- `docs/`: release, versioning, and packaging policies

## Release Model

Versioned releases are published on GitHub. The release flow is proof-oriented:

1. prepare and validate the release in dry-run mode
2. create the release commit and tag
3. publish the GitHub Release
4. run stage-4 post-release proof and verification

See:

- `docs/github-release-flow.md`
- `docs/release-policy.md`
- `docs/release-checklist.md`

## Current Version

- MCP manifest version: `1.0.3`
- Latest published tag: `v1.0.3`

## Short Answer

If you just want to use CodexMD3:

1. clone the repo
2. install the local plugin from `./plugin`
3. call `$material` for MD3-specific work
4. let the skill handle reasoning and use the MCP layer for deterministic facts
