# GitHub Release Flow

## Dry-run preparation

1. run `python scripts/prepare_release.py --bump <major|minor|patch|rc|beta> --dry-run --notes-out <path>`
2. run `python scripts/validate_release.py --expected-version <target-version> --release-notes <path>`
3. confirm RC1-RC12 pass

## Publication sequence

1. create or verify `release: vX.Y.Z` commit
2. create tag `vX.Y.Z`
3. push commit and tag
4. create GitHub Release titled `vX.Y.Z`
5. use the validated release notes draft
6. run post-release verification

## Reproducibility

The flow is reproducible if version-bearing files, tag, release notes draft, bundle sync, and validation outputs match.

## Non-goal

This document does not assume public Codex plugin directory publication. GitHub Releases plus local/internal plugin distribution are the required target.
