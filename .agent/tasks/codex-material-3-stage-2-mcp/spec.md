# Task: codex-material-3-stage-2-mcp

## Original task statement
Create an optional MD3-specific MCP layer that provides deterministic lookup, theme scaffolding, audit scoring, and release consistency checks for Material Design 3 workflows without replacing the skill's reasoning layer.

## Scope
- Implement MCP server files under `mcp/`.
- Define tool contracts and, where useful, JSON schemas under `mcp/contracts/`.
- Provide the minimum MD3-specific tool set.
- Keep outputs machine-readable and reusable by verifiers and release scripts.
- Document deterministic boundaries, idempotency, and error models in `mcp/README.md`.

## Out of scope
- Generic repository tooling unrelated to MD3.
- LLM-style design reasoning inside MCP tools.
- Networked services, databases, or remote dependency on external APIs.
- Rich GUI surfaces for the MCP server.

## Acceptance criteria
- AC2.1: The MCP layer is clearly scoped to Material Design 3 workflows and data rather than generic frontend reasoning.
- AC2.2: The minimum tool set exists or is scaffolded with executable contracts for `lookup_md3_token`, `lookup_md3_component`, `get_platform_matrix`, `get_layout_rule`, `generate_theme_scaffold`, `score_md3_audit`, and `check_md3_release_consistency`.
- AC2.3: Tool boundaries explicitly separate deterministic facts/scoring from skill-layer reasoning and remediation judgment.
- AC2.4: Tool outputs are machine-readable and reusable by verification/evidence scripts.
- AC2.5: Release consistency checking is implemented or scaffolded in a way that can prove version/changelog/sync alignment.

## Constraints
- Keep the server deterministic and file-backed.
- Ensure inputs and outputs remain stable enough for scripted verification.
- Avoid coupling the server to plugin-only paths when canonical repo paths are authoritative.
- Make failure modes explicit for missing keys, unsupported platforms, malformed payloads, and version drift.

## Assumptions
- Python is available for a lightweight deterministic MCP implementation.
- Static JSON knowledge bases are sufficient for token/component/layout/platform facts and scoring rules.
- Release checks can read repo-local files directly.

## Risks
- Tool schemas may become ambiguous if not tightly bounded.
- Theme scaffolding could drift into creative reasoning instead of deterministic derivation from inputs.
- Release consistency logic may miss version-bearing files unless the policy is centralized.

## Verification plan
- V1: Run representative commands or test harnesses for each required tool and capture machine-readable raw outputs.
- V2: Inspect contracts and README documentation for boundary, idempotency, and error-model coverage.
- V3: Verify that release consistency checks can detect or affirm alignment across plugin/docs/tag-oriented surfaces.

## Evidence expectations
- E1: Raw artifacts exist for token lookup, component lookup, platform matrix, layout rule, theme scaffold, audit score, and release consistency.
- E2: `evidence.json` records commands and artifact paths for each required tool.
- E3: `verdict.json` explicitly maps AC2.x criteria to raw tool outputs and contract files.

## Minimal safe implementation boundary
Provide a deterministic, file-backed MCP server and contract set sufficient to support MD3 lookup/scaffolding/scoring/release checks. Do not implement non-MD3 tools or speculative reasoning features.
