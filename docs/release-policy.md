# Release Policy

## Required contour

1. freeze scope and target version
2. update canonical source
3. synchronize bundled skill
4. update version-bearing files
5. update changelog and release notes draft
6. collect evidence
7. run fresh verification
8. create release commit and tag
9. publish GitHub Release
10. run post-release verification

## Control plane

All release work follows `spec freeze -> build -> evidence -> fresh verify -> minimal fix -> fresh verify`.

## Hard stops

- No release without changelog alignment.
- No release with bundle drift.
- No release without a release notes draft.
- No release with unresolved FAIL on required release checks.

## Dry-run default

Prepare and validate in dry-run mode before any commit, tag, push, or GitHub publication step.
