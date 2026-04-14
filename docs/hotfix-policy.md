# Hotfix Policy

## When to hotfix

Hotfix when a released version has a production-impacting issue that can be resolved without redesigning the capability boundary.

## Hotfix flow

1. branch from the released tag
2. apply the smallest safe fix
3. synchronize the bundled skill if the canonical skill changed
4. update `CHANGELOG.md` with a patch release entry
5. run full release validation
6. publish a patch tag and GitHub Release

## Rollback policy

- Prefer rollback when the failure is not well-bounded or proof is incomplete.
- Roll back manifest, changelog, MCP manifest, and bundled skill together.
- Re-run validation after rollback to prove the restored release state.
