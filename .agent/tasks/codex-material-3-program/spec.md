# Task: codex-material-3-program

## Original task statement
Design and implement a production-ready Codex Material Design 3 capability that matches the functional baseline of `hamen/material-3-skill` while adding repo-local proof discipline, an optional deterministic MCP layer, installable plugin packaging, and a versioned GitHub release lifecycle. The capability must remain explicitly Material Design 3 specific, Compose-first, Flutter-secondary, and Web-limited.

## Scope
- Define the repo-task-proof-loop control plane and stage topology for the MD3 program.
- Create canonical repo-local Material 3 skill artifacts under `.agents/skills/material-3/`.
- Create MD3-specific deterministic MCP tooling and contracts under `mcp/`.
- Create installable plugin packaging under `plugin/` plus local marketplace metadata.
- Create release/versioning documentation, scripts, and validation surfaces.
- Produce repo-local evidence, verifier verdicts, and problem logs for the parent task and each stage task.

## Out of scope
- Generic frontend design guidance not anchored to MD3 rules.
- Public publication into an official Codex plugin directory.
- Full runtime integration with external design tools or live app stores.
- Non-MD3 design systems, non-Material token systems, or framework-agnostic UI audits.
- Large refactors unrelated to establishing the MD3 capability and its proof/release surfaces.

## Acceptance criteria
- AC1: Parent and stage task directories exist under `.agent/tasks/` with frozen specs that follow the required template and preserve scope/acceptance boundaries.
- AC2: The repository contains an MD3-specific canonical skill, deterministic optional MCP layer, installable plugin bundle, and release-management surfaces aligned to the four required stages.
- AC3: Source-of-truth boundaries are explicit: canonical editable skill under `.agents/skills/material-3/`, bundled packaging artifact under `plugin/skills/material-3/`, and release metadata surfaces under plugin/docs/changelog/script surfaces.
- AC4: The repo-task-proof-loop is implemented as the control plane with evidence, raw artifacts, fresh verification, verdicts, and problem logs stored in repo-local task directories.
- AC5: Packaging synchronization from canonical skill to bundled plugin skill is defined, executable, and verified by evidence rather than narrative.
- AC6: Release readiness includes SemVer policy, changelog/tag/commit policy, GitHub release flow, dry-run support, post-release verification, and version-drift checks.
- AC7: Final repo state supports MD3-specific component/theme/layout/scaffold/audit workflows without collapsing into a generic frontend helper.

## Constraints
- Follow `spec freeze -> build -> evidence -> fresh verify -> minimal fix -> fresh verify`.
- Do not write production implementation before frozen specs exist.
- Do not allow builder outputs to self-certify correctness.
- Treat plugin bundle files as derived packaging artifacts, not the primary authoring surface.
- Keep the task tree shallow and use only the required stage IDs unless a bounded child task is proven necessary.

## Assumptions
- The repository starts nearly empty and can adopt the required structure cleanly.
- Python 3 is available for validation, sync, and release helper scripts.
- No existing plugin marketplace or MCP server must be preserved.
- Repo-local proof artifacts are acceptable as the system of record for this implementation pass.

## Risks
- Over-scoping into generic UI guidance would break the MD3-specific requirement.
- Version drift between canonical skill, plugin bundle, scripts, and docs could invalidate release readiness.
- Evidence may become stale if build outputs change after collection.
- A nominal MCP scaffold without deterministic contracts would fail verification intent.

## Verification plan
- V1: Verify existence and required contents of stage deliverables, source-of-truth boundaries, and proof-loop artifacts by repository inspection and raw command outputs.
- V2: Run deterministic validation scripts for skill sync, MCP contracts/lookups, and release consistency; record outputs in raw artifacts and evidence manifests.
- V3: Perform a fresh verifier pass that maps each acceptance criterion to authoritative files/commands and emits `verdict.json` plus `problems.md`.

## Evidence expectations
- E1: Repo-local raw artifacts show checks for token lookup, component lookup, platform matrix, layout rules, theme scaffolding, audit scoring, packaging sync, and release consistency.
- E2: `evidence.md` and `evidence.json` exist for the parent task and each stage task, with command outputs and AC-to-artifact mappings.
- E3: `verdict.json` and `problems.md` exist for the parent task and each stage task, produced after a fresh verification pass.

## Minimal safe implementation boundary
Implement only the artifacts required to deliver an MD3-specific Codex capability with deterministic lookup/scoring support, plugin packaging, and release proof surfaces. Do not add unrelated product features, runtime services, or non-MD3 design-system content.
