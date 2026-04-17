# Material 3 MCP

Deterministic support layer for the repo-local Material Design 3 capability. This MCP server is MD3-specific by design. It is not a generic design-system reasoning engine.

## Scope

- token lookup
- component lookup
- platform matrix lookup
- layout rule lookup
- theme scaffolding support
- audit scorecard support
- release consistency checks

## Non-scope

- subjective component composition
- product-specific design judgment
- narrative remediation prioritization
- generic frontend audits
- task verdict authorship or self-certification

## Tool contracts

The machine-readable source of truth is `mcp/contracts/tool-contracts.json`. Human-readable tool boundaries are summarized below.
Builder outputs are evidence, not certification. Store raw JSON outputs in repo-local task directories and require a fresh verifier pass before treating any stage as complete.

### `lookup_md3_token`

- Purpose: return structured MD3 token guidance by category and optional token name.
- Input: `category`, optional `token_name`, `platform`, `include_related`.
- Output: category summary or token detail with platform note.
- Deterministic boundary: file-backed lookup only.
- Error model: unknown category, unknown token, unsupported platform.
- Idempotency: pure lookup.
- Keep in skill layer: choosing token strategy for the product flow.

### `lookup_md3_component`

- Purpose: return canonical component usage guidance, required states, accessibility notes, and platform deltas.
- Input: `component_id`, optional `platform`.
- Output: machine-readable component guidance.
- Deterministic boundary: file-backed lookup only.
- Error model: unknown component, unsupported platform.
- Idempotency: pure lookup.
- Keep in skill layer: choosing between valid compositions.

### `get_platform_matrix`

- Purpose: return Compose/Flutter/Web support boundaries.
- Input: optional `topic`.
- Output: full matrix or topic slice.
- Deterministic boundary: static capability matrix only.
- Error model: unknown topic.
- Idempotency: pure lookup.
- Keep in skill layer: deciding how platform limits affect the recommendation.

### `get_layout_rule`

- Purpose: return responsive shell, navigation adaptation, inset, and foldable rules.
- Input: `rule_id`, optional `platform`, optional `window_class`.
- Output: rule summary, platform note, and class-specific guidance.
- Deterministic boundary: file-backed layout rules only.
- Error model: unknown rule, unsupported platform, unknown window class.
- Idempotency: pure lookup.
- Keep in skill layer: choosing the final shell for the user's task.

### `generate_theme_scaffold`

- Purpose: derive deterministic role tokens and palette scaffolds from seed inputs.
- Input: `seed_color`, optional `platform`, `dark_mode`, `contrast`, `dynamic_color`.
- Output: palettes, light/dark role scaffolds, typography/shape/elevation defaults.
- Deterministic boundary: mechanical token scaffold only.
- Error model: malformed hex color, unsupported enum values.
- Idempotency: pure transform.
- Keep in skill layer: product-specific visual judgment and dynamic-color policy decisions.

### `score_md3_audit`

- Purpose: convert structured findings into a reproducible scorecard.
- Input: `findings[]`.
- Output: overall score, grade, category scores, severity counts, quick wins, remediation sequence, unresolved risks.
- Deterministic boundary: scoring only; no repository inspection.
- Error model: unknown severity or category.
- Idempotency: pure scoring.
- Keep in skill layer: finding generation, evidence analysis, and remediation storytelling.

### `check_md3_release_consistency`

- Purpose: detect version drift, stale bundle state, missing release docs, invalid tag/commit format, and release-notes mismatches.
- Input: optional `expected_version`, `target_tag`, `release_commit_message`, `release_notes_path`.
- Output: machine-readable check set with pass/fail status.
- Deterministic boundary: repo-local file and metadata inspection only.
- Error model: missing files, drift, invalid patterns, bundle mismatch.
- Idempotency: pure repository check.
- Keep in skill layer: deciding bump semantics, rollout timing, and rollback strategy.

## Proof Loop

Use the stage-2 proof harness to keep raw JSON artifacts in repo and separate builder work from verifier work:

```powershell
python scripts/stage2_mcp_proof.py build --expected-version 1.0.1 --release-notes .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md
python scripts/stage2_mcp_proof.py verify
```

Proof-loop expectations:

- raw MCP artifacts stay as JSON under `.agent/tasks/codex-material-3-stage-2-mcp/raw/`
- the builder identity must differ from the verifier identity
- a fresh verifier pass is required after evidence collection
- skill-layer reasoning and remediation remain outside MCP, even when `score_md3_audit` or `check_md3_release_consistency` returns `PASS`

## CLI harness

Use the CLI for local proof artifacts:

```powershell
python mcp/cli.py lookup-token --category color --token-name primary
python mcp/cli.py lookup-component --component navigation-rail --platform compose
python mcp/cli.py platform-matrix --topic dynamic-color
python mcp/cli.py layout-rule --rule adaptive-navigation --window-class medium
python mcp/cli.py theme-scaffold --seed-color "#6750A4"
python mcp/cli.py score-audit --findings-file sample-findings.json
python mcp/cli.py check-release-consistency --expected-version 1.0.0 --release-notes .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md
```

## Server runtime

Run the FastMCP server over stdio:

```powershell
python mcp/server.py
```

The plugin-bundled `.mcp.json` points to this repo-local server path for internal distribution.
