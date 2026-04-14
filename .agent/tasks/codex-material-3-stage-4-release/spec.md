# Task: codex-material-3-stage-4-release

## Original task statement
Design and implement the versioned release lifecycle for the MD3 Codex capability, including SemVer policy, changelog/tag/commit conventions, GitHub release flow, dry-run support, packaging sync checks, and post-release verification.

## Scope
- Define versioning, release, hotfix, packaging sync, and GitHub publication policies in `docs/`.
- Create `CHANGELOG.md`.
- Define canonical public version surface in `plugin/.codex-plugin/plugin.json`.
- Add scripts and optional workflows for bumping/preparing/validating releases.
- Require release verification against RC1-RC12 and version-drift checks.

## Out of scope
- Actually publishing to GitHub unless credentials and explicit user request make it appropriate.
- Maintaining an independent public version stream for the canonical skill.
- Automated rollout to external package registries.

## Acceptance criteria
- AC4.1: A versioning policy exists and defines SemVer, canonical public version surface, and version inheritance/mapping expectations.
- AC4.2: A release policy and checklist exist, including dry-run mode and post-release verification.
- AC4.3: A changelog policy exists and `CHANGELOG.md` is present with the required entry skeleton.
- AC4.4: Tag policy and release commit policy exist and align with the required formats.
- AC4.5: A GitHub Release flow is documented for reproducible publication.
- AC4.6: Packaging sync is an explicit part of the release flow.
- AC4.7: Release verification explicitly checks for version drift across all required release surfaces.

## Constraints
- `plugin/.codex-plugin/plugin.json` is the canonical public release version surface.
- Release cannot be considered complete without post-release proof.
- RC1-RC12 must be representable via repo state, command output, or structured artifacts.
- Do not assume public directory publication; target GitHub Releases plus local/internal distribution.

## Assumptions
- Release scripts can operate in dry-run mode by default.
- GitHub publication may be documented and prepared even if not executed in this session.
- The initial version can be established as part of bootstrapping the capability.

## Risks
- Version drift across plugin manifest, changelog, docs, scripts, and release notes.
- Release automation being too implicit to verify.
- Lack of dry-run or rollback guidance leading to unsafe publication behavior.

## Verification plan
- V1: Inspect policy docs, changelog, version-bearing files, and release scripts/workflows for required policy coverage.
- V2: Run release validation in dry-run mode and capture raw artifacts for version detection, changelog checks, tag checks, release notes draft, packaging sync, and drift validation.
- V3: Perform a fresh verifier pass that evaluates AC4.x and RC1-RC12 against authoritative files and command outputs.

## Evidence expectations
- E1: Raw artifacts include release version, changelog, tag, packaging sync, and release notes draft checks.
- E2: `evidence.md` and `evidence.json` capture current version, target version, planned tag, and release commit metadata.
- E3: `verdict.json` contains AC4.x and RC1-RC12 statuses with remediation notes in `problems.md` when needed.

## Minimal safe implementation boundary
Provide a complete release-management contour, dry-run validation path, and repo-local proof surfaces for versioned shipping of the MD3 plugin. Do not claim live publication without corresponding Git/GitHub evidence.
