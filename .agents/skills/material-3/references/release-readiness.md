# MD3 Capability Release Readiness

## Release boundary

The release artifact is the plugin bundle plus its aligned MCP configuration and release metadata. The canonical skill remains the editable source; the bundled skill is derived.

## Required checks before release

- canonical skill updated first
- bundled skill synchronized and proven equivalent
- MCP metadata aligned with plugin version
- changelog entry present
- release notes draft present
- tag and release commit follow policy
- fresh verifier pass completed

## Proof expectations

- store raw evidence in `.agent/tasks/<TASK_ID>/raw/`
- map every AC and RC to files or command outputs
- fail the release on version drift, stale bundle content, or missing notes

## Dry-run rule

Prepare and validate release metadata in dry-run mode before any tag or publication action.
