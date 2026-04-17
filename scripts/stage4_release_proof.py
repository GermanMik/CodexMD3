from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "codex-material-3-stage-4-release"
TASK_DIR = ROOT / ".agent" / "tasks" / TASK_ID
RAW_DIR = TASK_DIR / "raw"
EVIDENCE_JSON = TASK_DIR / "evidence.json"
EVIDENCE_MD = TASK_DIR / "evidence.md"
VERDICT_JSON = TASK_DIR / "verdict.json"
PROBLEMS_MD = TASK_DIR / "problems.md"

PLUGIN_MANIFEST = ROOT / "plugin" / ".codex-plugin" / "plugin.json"
MCP_MANIFEST = ROOT / "mcp" / "manifest.json"
CONTRACTS = ROOT / "mcp" / "contracts" / "tool-contracts.json"
CHANGELOG = ROOT / "CHANGELOG.md"
VERSION_POLICY = ROOT / "docs" / "versioning-policy.md"
RELEASE_POLICY = ROOT / "docs" / "release-policy.md"
RELEASE_CHECKLIST = ROOT / "docs" / "release-checklist.md"
RELEASE_FLOW = ROOT / "docs" / "github-release-flow.md"
PACKAGING_SYNC_POLICY = ROOT / "docs" / "packaging-sync-policy.md"
PUBLISH_WORKFLOW = ROOT / ".github" / "workflows" / "publish-release.yml"

DEFAULT_BUILDER_IDENTITY = "stage4-release-builder"
DEFAULT_VERIFIER_IDENTITY = "stage4-release-fresh-verifier"
RELEASE_VIEW_FIELDS = "body,isDraft,isPrerelease,name,publishedAt,tagName,targetCommitish,url"
REQUIRED_CHANGELOG_SECTIONS = [
    "Added",
    "Changed",
    "Fixed",
    "Removed",
    "Security",
    "Migration Notes",
]


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalize_text(value: str) -> str:
    return value.replace("\r\n", "\n").strip()


def _run_process(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _run_json(args: list[str]) -> tuple[int, Any]:
    result = _run_process(args)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"Command failed: {' '.join(args)}")
    return result.returncode, json.loads(result.stdout)


def _run_text(args: list[str], allow_failure: bool = False) -> str:
    result = _run_process(args)
    if result.returncode != 0 and not allow_failure:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"Command failed: {' '.join(args)}")
    return result.stdout.strip()


def _git_head() -> str:
    return _run_text(["git", "rev-parse", "HEAD"])


def _is_ancestor(ancestor: str, ref_name: str) -> bool:
    result = _run_process(["git", "merge-base", "--is-ancestor", ancestor, ref_name])
    return result.returncode == 0


def _release_notes_candidates(expected_version: str, release_notes: str | None) -> list[Path]:
    candidates: list[Path] = []
    if release_notes:
        candidates.append(ROOT / release_notes)
    candidates.append(RAW_DIR / f"release-notes-v{expected_version}.md")
    candidates.append(RAW_DIR / "release-notes-draft.md")
    return candidates


def _read_release_notes(expected_version: str, release_notes: str | None) -> tuple[Path, str]:
    for candidate in _release_notes_candidates(expected_version, release_notes):
        if candidate.exists():
            return candidate, candidate.read_text(encoding="utf-8")
    raise FileNotFoundError(
        "No release notes source found. Create .agent/tasks/codex-material-3-stage-4-release/"
        f"raw/release-notes-v{expected_version}.md or pass --release-notes."
    )


def _current_version() -> str:
    return _load_json(PLUGIN_MANIFEST)["version"]


def _prepare_release_plan(expected_version: str) -> tuple[int, dict[str, Any]]:
    return _run_json(
        [
            sys.executable,
            str(ROOT / "scripts" / "prepare_release.py"),
            "--version",
            expected_version,
            "--dry-run",
        ]
    )


def _packaging_sync_check() -> tuple[int, dict[str, Any]]:
    return _run_json([sys.executable, str(ROOT / "scripts" / "sync_plugin_bundle.py"), "--check"])


def _validate_release(expected_version: str, release_notes_path: str) -> tuple[int, dict[str, Any]]:
    return _run_json(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_release.py"),
            "--expected-version",
            expected_version,
            "--release-notes",
            release_notes_path,
        ]
    )


def _extract_changelog_block(expected_version: str) -> tuple[str | None, str]:
    content = CHANGELOG.read_text(encoding="utf-8")
    lines = content.splitlines()
    header = None
    collected: list[str] = []
    inside = False
    for line in lines:
        if line.startswith("## ["):
            if line.startswith(f"## [{expected_version}] - "):
                header = line
                inside = True
                collected.append(line)
                continue
            if inside:
                break
        if inside:
            collected.append(line)
    return header, "\n".join(collected).strip()


def _build_changelog_check(expected_version: str) -> dict[str, Any]:
    header, block = _extract_changelog_block(expected_version)
    first_release_header = next(
        (line for line in CHANGELOG.read_text(encoding="utf-8").splitlines() if line.startswith("## [")),
        None,
    )
    sections = {section: f"### {section}" in block for section in REQUIRED_CHANGELOG_SECTIONS}
    return {
        "expected_version": expected_version,
        "header": header,
        "header_present": header is not None,
        "top_release_header": first_release_header,
        "expected_entry_is_latest": first_release_header == header,
        "required_sections": sections,
        "all_required_sections_present": all(sections.values()),
        "entry_block": block,
    }


def _build_tag_check(expected_version: str) -> dict[str, Any]:
    tag_name = f"v{expected_version}"
    local_tag_commit = _run_text(["git", "rev-parse", f"{tag_name}^{{}}"], allow_failure=True)
    tag_exists = bool(local_tag_commit)
    release_commit_subject = (
        _run_text(["git", "show", "-s", "--format=%s", local_tag_commit], allow_failure=True)
        if tag_exists
        else None
    )
    remote_tag_object = _run_text(["git", "ls-remote", "--tags", "origin", f"refs/tags/{tag_name}"], allow_failure=True)
    remote_tag_commit = _run_text(["git", "ls-remote", "--tags", "origin", f"refs/tags/{tag_name}^{{}}"], allow_failure=True)
    remote_object_sha = remote_tag_object.split()[0] if remote_tag_object else None
    remote_commit_sha = remote_tag_commit.split()[0] if remote_tag_commit else None
    return {
        "tag": tag_name,
        "local_tag_exists": tag_exists,
        "local_tag_commit": local_tag_commit or None,
        "release_commit_subject": release_commit_subject,
        "release_commit_matches_policy": release_commit_subject == f"release: {tag_name}",
        "remote_tag_object": remote_object_sha,
        "remote_tag_commit": remote_commit_sha,
        "remote_tag_exists": remote_object_sha is not None,
        "remote_tag_matches_local": bool(tag_exists and remote_commit_sha and remote_commit_sha == local_tag_commit),
    }


def _fetch_release_view(expected_version: str) -> tuple[int, dict[str, Any]]:
    return _run_json(
        [
            "gh",
            "release",
            "view",
            f"v{expected_version}",
            "--json",
            RELEASE_VIEW_FIELDS,
        ]
    )


def _build_post_release_check(
    expected_version: str,
    release_view: dict[str, Any],
    release_notes_text: str,
    tag_check: dict[str, Any],
) -> dict[str, Any]:
    tag_commit = tag_check.get("local_tag_commit")
    body_matches_notes = _normalize_text(release_view.get("body", "")) == _normalize_text(release_notes_text)
    current_versions = {
        "plugin": _load_json(PLUGIN_MANIFEST).get("version"),
        "mcp_manifest": _load_json(MCP_MANIFEST).get("version"),
        "contracts": _load_json(CONTRACTS).get("version"),
    }
    changelog_header, _ = _extract_changelog_block(expected_version)
    return {
        "expected_version": expected_version,
        "tag": f"v{expected_version}",
        "local_tag_commit": tag_commit,
        "local_main_contains_tag_commit": _is_ancestor(tag_commit, "main") if tag_commit else False,
        "origin_main_contains_tag_commit": _is_ancestor(tag_commit, "origin/main") if tag_commit else False,
        "release_url": release_view.get("url"),
        "release_published": bool(release_view.get("publishedAt")) and release_view.get("isDraft") is False,
        "release_is_prerelease": release_view.get("isPrerelease"),
        "release_body_matches_notes": body_matches_notes,
        "release_title_matches_tag": release_view.get("name") == f"v{expected_version}",
        "release_tag_matches_expected": release_view.get("tagName") == f"v{expected_version}",
        "version_surface_alignment": all(value == expected_version for value in current_versions.values()),
        "changelog_header_present": changelog_header is not None,
        "tag_commit_on_remote": tag_check.get("remote_tag_matches_local") is True,
    }


def _artifact_record(path: Path, artifact_type: str) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "type": artifact_type,
        "sha256": _sha256(path),
    }


def _build_evidence_markdown(evidence: dict[str, Any]) -> str:
    lines = [
        f"# Evidence for {TASK_ID}",
        "",
        "## Build summary",
        "Collected repo-local release artifacts, captured published GitHub release state, and recorded a builder-only evidence pass that still requires a distinct fresh verifier.",
        "",
        "## Proof policy",
        f"- builder identity: `{evidence['builder_identity']}`",
        "- builder outputs are evidence only, not certification",
        "- release notes are stored as markdown and all other raw checks are stored as structured JSON",
        "- verifier identity must differ from builder identity",
        "- fresh verification is required after evidence collection",
        "",
        "## Commands run",
    ]
    lines.extend(f"- `{command['cmd']}`" for command in evidence["commands"])
    lines.extend(["", "## Raw artifacts"])
    lines.extend(f"- `{artifact['path']}` (`{artifact['sha256'][:12]}`)" for artifact in evidence["artifacts"])
    lines.extend(
        [
            "",
            "## Acceptance criteria mapping",
            "- AC4.1 -> `docs/versioning-policy.md`, `plugin/.codex-plugin/plugin.json`, `mcp/manifest.json`, `mcp/contracts/tool-contracts.json`, `raw/release-version-check.json`",
            "- AC4.2 -> `docs/release-policy.md`, `docs/release-checklist.md`, `raw/release-validation.json`, `raw/post-release-check.json`",
            "- AC4.3 -> `CHANGELOG.md`, `raw/changelog-check.json`",
            "- AC4.4 -> `docs/versioning-policy.md`, `raw/tag-check.json`, `raw/release-validation.json`",
            "- AC4.5 -> `docs/github-release-flow.md`, `.github/workflows/publish-release.yml`, `raw/release-notes-v<version>.md`, `raw/github-release-view.json`, `raw/post-release-check.json`",
            "- AC4.6 -> `docs/packaging-sync-policy.md`, `raw/packaging-sync-check.json`",
            "- AC4.7 -> `raw/release-validation.json`, `plugin/.codex-plugin/plugin.json`, `mcp/manifest.json`, `mcp/contracts/tool-contracts.json`, `CHANGELOG.md`",
            "",
            "## Release evidence",
            f"- current version: `{evidence['release_metadata']['current_version']}`",
            f"- target version: `{evidence['release_metadata']['target_version']}`",
            f"- release commit: `{evidence['release_metadata']['release_commit_message']}`",
            f"- tag: `{evidence['release_metadata']['tag']}`",
            f"- release URL: `{evidence['release_metadata']['release_url']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def build(expected_version: str | None, release_notes: str | None, builder_identity: str) -> None:
    current_version = _current_version()
    target_version = expected_version or current_version
    notes_source_path, notes_text = _read_release_notes(target_version, release_notes)

    if RAW_DIR.exists():
        shutil.rmtree(RAW_DIR)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    draft_notes_path = RAW_DIR / "release-notes-draft.md"
    versioned_notes_path = RAW_DIR / f"release-notes-v{target_version}.md"
    _write_text(draft_notes_path, notes_text)
    _write_text(versioned_notes_path, notes_text)

    release_plan_exit, release_plan = _prepare_release_plan(target_version)
    packaging_exit, packaging_sync = _packaging_sync_check()
    validation_exit, validation = _validate_release(
        target_version,
        str(draft_notes_path.relative_to(ROOT)).replace("\\", "/"),
    )
    changelog_check = _build_changelog_check(target_version)
    tag_check = _build_tag_check(target_version)
    release_view_exit, release_view = _fetch_release_view(target_version)
    post_release_check = _build_post_release_check(target_version, release_view, notes_text, tag_check)

    json_artifacts = {
        RAW_DIR / "release-version-check.json": release_plan,
        RAW_DIR / "packaging-sync-check.json": packaging_sync,
        RAW_DIR / "release-validation.json": validation,
        RAW_DIR / "changelog-check.json": changelog_check,
        RAW_DIR / "tag-check.json": tag_check,
        RAW_DIR / "github-release-view.json": release_view,
        RAW_DIR / "post-release-check.json": post_release_check,
    }
    for path, payload in json_artifacts.items():
        _write_json(path, payload)

    release_url_path = RAW_DIR / "github-release-url.txt"
    _write_text(release_url_path, release_view.get("url", "") + "\n")

    artifacts = [
        _artifact_record(RAW_DIR / "release-version-check.json", "json"),
        _artifact_record(RAW_DIR / "changelog-check.json", "json"),
        _artifact_record(RAW_DIR / "tag-check.json", "json"),
        _artifact_record(RAW_DIR / "packaging-sync-check.json", "json"),
        _artifact_record(draft_notes_path, "markdown"),
        _artifact_record(versioned_notes_path, "markdown"),
        _artifact_record(RAW_DIR / "release-validation.json", "json"),
        _artifact_record(RAW_DIR / "github-release-view.json", "json"),
        _artifact_record(release_url_path, "text"),
        _artifact_record(RAW_DIR / "post-release-check.json", "json"),
    ]

    evidence = {
        "task_id": TASK_ID,
        "builder_identity": builder_identity,
        "proof_policy": {
            "builder_outputs_are_evidence_only": True,
            "builder_identity_must_differ_from_verifier": True,
            "requires_fresh_verification": True,
            "structured_checks_format": "json",
            "release_notes_format": "markdown",
        },
        "commands": [
            {
                "cmd": f"python scripts/prepare_release.py --version {target_version} --dry-run",
                "exit_code": release_plan_exit,
                "artifact": ".agent/tasks/codex-material-3-stage-4-release/raw/release-version-check.json",
            },
            {
                "cmd": f"Copy release notes from {notes_source_path.relative_to(ROOT).as_posix()} into raw/release-notes-draft.md and raw/release-notes-v{target_version}.md",
                "exit_code": 0,
                "artifact": f".agent/tasks/codex-material-3-stage-4-release/raw/release-notes-v{target_version}.md",
            },
            {
                "cmd": "python scripts/sync_plugin_bundle.py --check",
                "exit_code": packaging_exit,
                "artifact": ".agent/tasks/codex-material-3-stage-4-release/raw/packaging-sync-check.json",
            },
            {
                "cmd": (
                    "python scripts/validate_release.py "
                    f"--expected-version {target_version} "
                    "--release-notes .agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md"
                ),
                "exit_code": validation_exit,
                "artifact": ".agent/tasks/codex-material-3-stage-4-release/raw/release-validation.json",
            },
            {
                "cmd": "Get-Content -Raw CHANGELOG.md",
                "exit_code": 0,
                "artifact": ".agent/tasks/codex-material-3-stage-4-release/raw/changelog-check.json",
            },
            {
                "cmd": f"git rev-parse v{target_version}^{{}} && git ls-remote --tags origin refs/tags/v{target_version} refs/tags/v{target_version}^{{}}",
                "exit_code": 0,
                "artifact": ".agent/tasks/codex-material-3-stage-4-release/raw/tag-check.json",
            },
            {
                "cmd": f"gh release view v{target_version} --json {RELEASE_VIEW_FIELDS}",
                "exit_code": release_view_exit,
                "artifact": ".agent/tasks/codex-material-3-stage-4-release/raw/github-release-view.json",
            },
            {
                "cmd": f"git merge-base --is-ancestor $(git rev-parse v{target_version}^{{}}) origin/main",
                "exit_code": 0,
                "artifact": ".agent/tasks/codex-material-3-stage-4-release/raw/post-release-check.json",
            },
        ],
        "artifacts": artifacts,
        "ac_map": {
            "AC4.1": [
                "docs/versioning-policy.md",
                "plugin/.codex-plugin/plugin.json",
                "mcp/manifest.json",
                "mcp/contracts/tool-contracts.json",
                ".agent/tasks/codex-material-3-stage-4-release/raw/release-version-check.json",
            ],
            "AC4.2": [
                "docs/release-policy.md",
                "docs/release-checklist.md",
                ".agent/tasks/codex-material-3-stage-4-release/raw/release-validation.json",
                ".agent/tasks/codex-material-3-stage-4-release/raw/post-release-check.json",
                str(EVIDENCE_JSON.relative_to(ROOT)).replace("\\", "/"),
            ],
            "AC4.3": [
                "CHANGELOG.md",
                ".agent/tasks/codex-material-3-stage-4-release/raw/changelog-check.json",
            ],
            "AC4.4": [
                "docs/versioning-policy.md",
                ".agent/tasks/codex-material-3-stage-4-release/raw/tag-check.json",
                ".agent/tasks/codex-material-3-stage-4-release/raw/release-validation.json",
            ],
            "AC4.5": [
                "docs/github-release-flow.md",
                ".github/workflows/publish-release.yml",
                f".agent/tasks/codex-material-3-stage-4-release/raw/release-notes-v{target_version}.md",
                ".agent/tasks/codex-material-3-stage-4-release/raw/github-release-view.json",
                ".agent/tasks/codex-material-3-stage-4-release/raw/post-release-check.json",
            ],
            "AC4.6": [
                "docs/packaging-sync-policy.md",
                ".agent/tasks/codex-material-3-stage-4-release/raw/packaging-sync-check.json",
            ],
            "AC4.7": [
                ".agent/tasks/codex-material-3-stage-4-release/raw/release-validation.json",
                "plugin/.codex-plugin/plugin.json",
                "mcp/manifest.json",
                "mcp/contracts/tool-contracts.json",
                "CHANGELOG.md",
            ],
        },
        "release_metadata": {
            "current_version": current_version,
            "target_version": target_version,
            "tag": f"v{target_version}",
            "release_commit_message": f"release: v{target_version}",
            "release_notes_source": str(notes_source_path.relative_to(ROOT)).replace("\\", "/"),
            "release_url": release_view.get("url"),
        },
        "git_head": _git_head(),
        "timestamp": _now(),
    }
    _write_json(EVIDENCE_JSON, evidence)
    EVIDENCE_MD.write_text(_build_evidence_markdown(evidence), encoding="utf-8")


def verify(verifier_identity: str) -> int:
    evidence = _load_json(EVIDENCE_JSON)
    commands = evidence.get("commands", [])
    artifacts = evidence.get("artifacts", [])
    builder_identity = evidence.get("builder_identity")
    proof_policy = evidence.get("proof_policy", {})
    expected_version = evidence.get("release_metadata", {}).get("target_version")

    command_shape_ok = isinstance(commands, list) and all(isinstance(command, dict) and "cmd" in command for command in commands)
    artifact_shape_ok = isinstance(artifacts, list) and all(isinstance(artifact, dict) and "path" in artifact for artifact in artifacts)
    artifact_map = {artifact["path"]: ROOT / artifact["path"] for artifact in artifacts} if artifact_shape_ok else {}

    raw_payloads: dict[str, Any] = {}
    missing_artifacts: list[str] = []
    invalid_json_artifacts: list[str] = []
    for artifact in artifacts if artifact_shape_ok else []:
        artifact_path = artifact["path"]
        absolute_path = artifact_map[artifact_path]
        if not absolute_path.exists():
            missing_artifacts.append(artifact_path)
            continue
        if artifact["type"] == "json":
            try:
                raw_payloads[artifact_path] = _load_json(absolute_path)
            except json.JSONDecodeError:
                invalid_json_artifacts.append(artifact_path)
        else:
            raw_payloads[artifact_path] = absolute_path.read_text(encoding="utf-8")

    release_plan = raw_payloads.get(".agent/tasks/codex-material-3-stage-4-release/raw/release-version-check.json", {})
    changelog_check = raw_payloads.get(".agent/tasks/codex-material-3-stage-4-release/raw/changelog-check.json", {})
    tag_check = raw_payloads.get(".agent/tasks/codex-material-3-stage-4-release/raw/tag-check.json", {})
    packaging_check = raw_payloads.get(".agent/tasks/codex-material-3-stage-4-release/raw/packaging-sync-check.json", {})
    validation = raw_payloads.get(".agent/tasks/codex-material-3-stage-4-release/raw/release-validation.json", {})
    release_view = raw_payloads.get(".agent/tasks/codex-material-3-stage-4-release/raw/github-release-view.json", {})
    post_release = raw_payloads.get(".agent/tasks/codex-material-3-stage-4-release/raw/post-release-check.json", {})
    versioned_notes = raw_payloads.get(
        f".agent/tasks/codex-material-3-stage-4-release/raw/release-notes-v{expected_version}.md",
        "",
    )
    validation_checks = {
        item["id"]: item for item in validation.get("release_consistency", {}).get("checks", [])
    }

    version_policy_text = VERSION_POLICY.read_text(encoding="utf-8")
    release_policy_text = RELEASE_POLICY.read_text(encoding="utf-8")
    release_checklist_text = RELEASE_CHECKLIST.read_text(encoding="utf-8")
    release_flow_text = RELEASE_FLOW.read_text(encoding="utf-8")
    packaging_policy_text = PACKAGING_SYNC_POLICY.read_text(encoding="utf-8")

    problems: list[str] = []
    ac_results: list[dict[str, Any]] = []

    proof_policy_ok = (
        proof_policy.get("builder_outputs_are_evidence_only") is True
        and proof_policy.get("builder_identity_must_differ_from_verifier") is True
        and proof_policy.get("requires_fresh_verification") is True
        and builder_identity != verifier_identity
    )
    if not command_shape_ok:
        problems.append("Evidence file is missing `cmd` keys on one or more command entries.")
    if not artifact_shape_ok:
        problems.append("Evidence file is missing `path` keys on one or more artifact entries.")
    if missing_artifacts:
        problems.append(f"Missing raw artifacts: {', '.join(missing_artifacts)}.")
    if invalid_json_artifacts:
        problems.append(f"Invalid JSON raw artifacts: {', '.join(invalid_json_artifacts)}.")

    current_versions = {
        "plugin": _load_json(PLUGIN_MANIFEST).get("version"),
        "mcp_manifest": _load_json(MCP_MANIFEST).get("version"),
        "contracts": _load_json(CONTRACTS).get("version"),
    }
    ac41_pass = (
        expected_version is not None
        and release_plan.get("target_version") == expected_version
        and release_plan.get("tag") == f"v{expected_version}"
        and all(value == expected_version for value in current_versions.values())
        and "`plugin/.codex-plugin/plugin.json` is the canonical public release version surface." in version_policy_text
        and "mcp/contracts/tool-contracts.json" in version_policy_text
        and "Git tag name" in version_policy_text
        and "GitHub Release title and notes draft" in version_policy_text
    )
    if not ac41_pass:
        problems.append("AC4.1 failed: version policy or aligned version surfaces are incomplete.")
    ac_results.append(
        {
            "id": "AC4.1",
            "status": "PASS" if ac41_pass else "FAIL",
            "reason": (
                "Versioning policy defines the canonical release surface and all version-bearing files align with the expected release version."
                if ac41_pass
                else "Versioning policy is incomplete or version-bearing files do not align with the expected release version."
            ),
            "evidence_refs": [
                "docs/versioning-policy.md",
                "plugin/.codex-plugin/plugin.json",
                "mcp/manifest.json",
                "mcp/contracts/tool-contracts.json",
                ".agent/tasks/codex-material-3-stage-4-release/raw/release-version-check.json",
            ],
        }
    )

    ac42_pass = (
        proof_policy_ok
        and "Dry-run default" in release_policy_text
        and "No publication sign-off without fresh stage-4 build/verify proof" in release_policy_text
        and "python scripts/stage4_release_proof.py build --expected-version <version>" in release_checklist_text
        and "python scripts/stage4_release_proof.py verify" in release_checklist_text
        and validation.get("status") == "PASS"
        and post_release.get("release_published") is True
        and post_release.get("tag_commit_on_remote") is True
    )
    if not ac42_pass:
        problems.append("AC4.2 failed: release policy/checklist or post-release proof separation is incomplete.")
    ac_results.append(
        {
            "id": "AC4.2",
            "status": "PASS" if ac42_pass else "FAIL",
            "reason": (
                "Release policy and checklist define dry-run and post-release proof, and the published release is backed by a distinct fresh-verifier contour."
                if ac42_pass
                else "Dry-run policy, post-release proof commands, or builder/verifier separation are not fully proven."
            ),
            "evidence_refs": [
                "docs/release-policy.md",
                "docs/release-checklist.md",
                ".agent/tasks/codex-material-3-stage-4-release/raw/release-validation.json",
                ".agent/tasks/codex-material-3-stage-4-release/raw/post-release-check.json",
                str(EVIDENCE_JSON.relative_to(ROOT)).replace("\\", "/"),
            ],
        }
    )

    ac43_pass = (
        changelog_check.get("header_present") is True
        and changelog_check.get("expected_entry_is_latest") is True
        and changelog_check.get("all_required_sections_present") is True
    )
    if not ac43_pass:
        problems.append("AC4.3 failed: CHANGELOG entry is missing, stale, or incomplete.")
    ac_results.append(
        {
            "id": "AC4.3",
            "status": "PASS" if ac43_pass else "FAIL",
            "reason": (
                "CHANGELOG contains the latest release entry with the required section skeleton for the expected version."
                if ac43_pass
                else "CHANGELOG does not contain a complete latest entry for the expected release version."
            ),
            "evidence_refs": [
                "CHANGELOG.md",
                ".agent/tasks/codex-material-3-stage-4-release/raw/changelog-check.json",
            ],
        }
    )

    ac44_pass = (
        tag_check.get("local_tag_exists") is True
        and tag_check.get("remote_tag_matches_local") is True
        and tag_check.get("release_commit_matches_policy") is True
        and validation_checks.get("release_commit_policy", {}).get("status") == "PASS"
        and validation_checks.get("tag_policy", {}).get("status") == "PASS"
    )
    if not ac44_pass:
        problems.append("AC4.4 failed: tag or release commit policy is not proven by git state.")
    ac_results.append(
        {
            "id": "AC4.4",
            "status": "PASS" if ac44_pass else "FAIL",
            "reason": (
                "Git state proves that the release tag and release commit follow the documented naming policy."
                if ac44_pass
                else "The release tag or release commit does not match documented policy or is not fully published."
            ),
            "evidence_refs": [
                "docs/versioning-policy.md",
                ".agent/tasks/codex-material-3-stage-4-release/raw/tag-check.json",
                ".agent/tasks/codex-material-3-stage-4-release/raw/release-validation.json",
            ],
        }
    )

    ac45_pass = (
        PUBLISH_WORKFLOW.exists()
        and "create GitHub Release titled `vX.Y.Z`" in release_flow_text
        and "python scripts/stage4_release_proof.py build --expected-version <version>" in release_flow_text
        and "python scripts/stage4_release_proof.py verify" in release_flow_text
        and release_view.get("name") == f"v{expected_version}"
        and release_view.get("tagName") == f"v{expected_version}"
        and release_view.get("isDraft") is False
        and post_release.get("release_body_matches_notes") is True
        and _normalize_text(release_view.get("body", "")) == _normalize_text(versioned_notes)
    )
    if not ac45_pass:
        problems.append("AC4.5 failed: GitHub Release flow or published release body does not match the validated notes.")
    ac_results.append(
        {
            "id": "AC4.5",
            "status": "PASS" if ac45_pass else "FAIL",
            "reason": (
                "GitHub Release publication is documented, workflow-backed, and the published release matches the stored notes artifact."
                if ac45_pass
                else "GitHub Release publication is undocumented, unpublished, draft-only, or drifted from the stored release notes."
            ),
            "evidence_refs": [
                "docs/github-release-flow.md",
                ".github/workflows/publish-release.yml",
                f".agent/tasks/codex-material-3-stage-4-release/raw/release-notes-v{expected_version}.md",
                ".agent/tasks/codex-material-3-stage-4-release/raw/github-release-view.json",
                ".agent/tasks/codex-material-3-stage-4-release/raw/post-release-check.json",
            ],
        }
    )

    ac46_pass = (
        packaging_check.get("status") == "PASS"
        and packaging_check.get("matches") is True
        and "Synchronize the bundled skill with `python scripts/sync_plugin_bundle.py`." in packaging_policy_text
        and "Fresh verification must prove sync before release signoff." in packaging_policy_text
    )
    if not ac46_pass:
        problems.append("AC4.6 failed: packaging sync is not explicitly proven as part of the release flow.")
    ac_results.append(
        {
            "id": "AC4.6",
            "status": "PASS" if ac46_pass else "FAIL",
            "reason": (
                "Packaging synchronization remains an explicit release step and the bundle is proven clean at release time."
                if ac46_pass
                else "Packaging synchronization policy or raw sync evidence is missing or reports drift."
            ),
            "evidence_refs": [
                "docs/packaging-sync-policy.md",
                ".agent/tasks/codex-material-3-stage-4-release/raw/packaging-sync-check.json",
            ],
        }
    )

    ac47_pass = (
        validation.get("status") == "PASS"
        and validation_checks.get("version_surface_alignment", {}).get("status") == "PASS"
        and validation_checks.get("expected_version_alignment", {}).get("status") == "PASS"
        and validation_checks.get("bundle_sync", {}).get("status") == "PASS"
        and validation_checks.get("release_notes", {}).get("status") == "PASS"
    )
    if not ac47_pass:
        problems.append("AC4.7 failed: release verification does not prove aligned version surfaces, bundle sync, and release notes.")
    ac_results.append(
        {
            "id": "AC4.7",
            "status": "PASS" if ac47_pass else "FAIL",
            "reason": (
                "Release verification proves version-drift checks across plugin manifest, MCP manifest, MCP contracts, changelog, bundle sync, and release notes."
                if ac47_pass
                else "Release verification is missing required PASS checks for aligned version surfaces or supporting release artifacts."
            ),
            "evidence_refs": [
                ".agent/tasks/codex-material-3-stage-4-release/raw/release-validation.json",
                "plugin/.codex-plugin/plugin.json",
                "mcp/manifest.json",
                "mcp/contracts/tool-contracts.json",
                "CHANGELOG.md",
            ],
        }
    )

    verdict_status = "PASS" if all(item["status"] == "PASS" for item in ac_results) else "FAIL"
    verdict = {
        "task_id": TASK_ID,
        "verifier_identity": verifier_identity,
        "verdict": verdict_status,
        "summary": (
            f"Fresh verification confirms the v{expected_version} release contour, published GitHub release, and repo-local post-release proof satisfy the stage-4 task."
            if verdict_status == "PASS"
            else "Fresh verification found stage-4 release proof-loop gaps that require fixes."
        ),
        "acceptance_criteria": ac_results,
        "release_checks": validation.get("release_checks", []),
        "open_problems_count": len(problems),
        "requires_fix": verdict_status != "PASS",
        "source_evidence_timestamp": evidence.get("timestamp"),
        "source_git_head": evidence.get("git_head"),
        "timestamp": _now(),
    }
    _write_json(VERDICT_JSON, verdict)

    if problems:
        PROBLEMS_MD.write_text(
            "\n".join(
                [
                    f"# Problems for {TASK_ID}",
                    "",
                    "Fresh verification found the following issues:",
                    *[f"- {problem}" for problem in problems],
                    "",
                ]
            ),
            encoding="utf-8",
        )
    else:
        PROBLEMS_MD.write_text(
            f"# Problems for {TASK_ID}\n\nNo open problems at verification time.\n",
            encoding="utf-8",
        )
    return 0 if verdict_status == "PASS" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Repo-task-proof-loop helper for codex-material-3-stage-4-release.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--expected-version", help="Version expected by the stage-4 release proof.")
    build_parser.add_argument("--release-notes", help="Repo-relative release notes source to copy into raw artifacts.")
    build_parser.add_argument("--builder-identity", default=DEFAULT_BUILDER_IDENTITY)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--verifier-identity", default=DEFAULT_VERIFIER_IDENTITY)

    args = parser.parse_args()
    if args.command == "build":
        build(
            expected_version=args.expected_version,
            release_notes=args.release_notes,
            builder_identity=args.builder_identity,
        )
        return 0
    return verify(verifier_identity=args.verifier_identity)


if __name__ == "__main__":
    raise SystemExit(main())
