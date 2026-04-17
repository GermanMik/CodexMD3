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
TASK_ID = "codex-material-3-stage-3-plugin"
TASK_DIR = ROOT / ".agent" / "tasks" / TASK_ID
RAW_DIR = TASK_DIR / "raw"
EVIDENCE_JSON = TASK_DIR / "evidence.json"
EVIDENCE_MD = TASK_DIR / "evidence.md"
VERDICT_JSON = TASK_DIR / "verdict.json"
PROBLEMS_MD = TASK_DIR / "problems.md"

CANONICAL_SKILL = ROOT / ".agents" / "skills" / "material"
BUNDLED_SKILL = ROOT / "plugin" / "skills" / "material"
PLUGIN_MANIFEST = ROOT / "plugin" / ".codex-plugin" / "plugin.json"
PLUGIN_MCP = ROOT / "plugin" / ".mcp.json"
PLUGIN_README = ROOT / "plugin" / "README.md"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SYNC_POLICY = ROOT / "docs" / "packaging-sync-policy.md"
SYNC_SCRIPT = ROOT / "scripts" / "sync_plugin_bundle.py"

DEFAULT_BUILDER_IDENTITY = "stage3-plugin-builder"
DEFAULT_VERIFIER_IDENTITY = "stage3-plugin-fresh-verifier"


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _current_version() -> str:
    return _load_json(PLUGIN_MANIFEST)["version"]


def _run_sync(check: bool) -> tuple[int, dict[str, Any]]:
    args = [sys.executable, str(SYNC_SCRIPT)]
    if check:
        args.append("--check")
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "sync_plugin_bundle.py failed")
    return result.returncode, payload


def _directory_hashes(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return [
        {
            "path": file_path.relative_to(path).as_posix(),
            "sha256": hashlib.sha256(file_path.read_bytes()).hexdigest(),
        }
        for file_path in sorted(candidate for candidate in path.rglob("*") if candidate.is_file())
    ]


def _bundle_hash_report() -> dict[str, Any]:
    source_files = _directory_hashes(CANONICAL_SKILL)
    target_files = _directory_hashes(BUNDLED_SKILL)
    source_map = {item["path"]: item["sha256"] for item in source_files}
    target_map = {item["path"]: item["sha256"] for item in target_files}
    return {
        "source_root": str(CANONICAL_SKILL.relative_to(ROOT)).replace("\\", "/"),
        "target_root": str(BUNDLED_SKILL.relative_to(ROOT)).replace("\\", "/"),
        "source_exists": CANONICAL_SKILL.exists(),
        "target_exists": BUNDLED_SKILL.exists(),
        "matches": bool(source_files) and source_map == target_map,
        "source_files": source_files,
        "target_files": target_files,
        "missing_in_target": sorted(set(source_map) - set(target_map)),
        "extra_in_target": sorted(set(target_map) - set(source_map)),
        "content_mismatches": sorted(
            path for path in set(source_map).intersection(target_map) if source_map[path] != target_map[path]
        ),
    }


def _marketplace_entry() -> dict[str, Any]:
    payload = _load_json(MARKETPLACE)
    plugin_entries = payload.get("plugins", [])
    for entry in plugin_entries:
        if entry.get("name") == "material-3-md3-workflows":
            return entry
    return {}


def _build_evidence_markdown(evidence: dict[str, Any]) -> str:
    lines = [
        f"# Evidence for {TASK_ID}",
        "",
        "## Build summary",
        "Collected repo-local plugin packaging artifacts, synchronized the bundled Material 3 skill from the canonical source, and recorded a builder-only evidence pass that still requires a distinct fresh verifier.",
        "",
        "## Proof policy",
        f"- builder identity: `{evidence['builder_identity']}`",
        "- builder outputs are evidence only, not certification",
        "- raw plugin packaging artifacts are stored as JSON under `raw/`",
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
            "- AC3.1 -> `plugin/.codex-plugin/plugin.json`, `raw/plugin-manifest-check.json`",
            "- AC3.2 -> `raw/canonical-bundle-hashes.json`",
            "- AC3.3 -> `plugin/README.md`, `docs/packaging-sync-policy.md`",
            "- AC3.4 -> `plugin/.mcp.json`, `raw/plugin-mcp-check.json`",
            "- AC3.5 -> `.agents/plugins/marketplace.json`, `raw/marketplace-check.json`",
            "- AC3.6 -> `scripts/sync_plugin_bundle.py`, `raw/bundle-sync-run.json`, `raw/bundle-sync-check.json`, `raw/canonical-bundle-hashes.json`, `docs/packaging-sync-policy.md`",
            "",
            "## Release evidence",
            f"- current version: `{evidence['release_metadata']['current_version']}`",
            f"- target version: `{evidence['release_metadata']['target_version']}`",
            f"- tag draft: `{evidence['release_metadata']['tag']}`",
            f"- release commit draft: `{evidence['release_metadata']['release_commit_message']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def build(expected_version: str | None, builder_identity: str) -> None:
    if RAW_DIR.exists():
        shutil.rmtree(RAW_DIR)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    current_version = _current_version()
    target_version = expected_version or current_version

    sync_exit_code, sync_run = _run_sync(check=False)
    sync_check_exit_code, sync_check = _run_sync(check=True)
    plugin_manifest = _load_json(PLUGIN_MANIFEST)
    plugin_mcp = _load_json(PLUGIN_MCP)
    marketplace_entry = _marketplace_entry()
    bundle_hash_report = _bundle_hash_report()

    artifact_payloads = {
        ".agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-run.json": sync_run,
        ".agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-check.json": sync_check,
        ".agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-manifest-check.json": plugin_manifest,
        ".agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-mcp-check.json": plugin_mcp,
        ".agent/tasks/codex-material-3-stage-3-plugin/raw/marketplace-check.json": marketplace_entry,
        ".agent/tasks/codex-material-3-stage-3-plugin/raw/canonical-bundle-hashes.json": bundle_hash_report,
    }

    artifacts: list[dict[str, Any]] = []
    for relative_path, payload in artifact_payloads.items():
        absolute_path = ROOT / relative_path
        _write_json(absolute_path, payload)
        artifacts.append(
            {
                "path": relative_path,
                "type": "json",
                "sha256": _sha256(absolute_path),
            }
        )

    evidence = {
        "task_id": TASK_ID,
        "builder_identity": builder_identity,
        "proof_policy": {
            "raw_artifact_format": "json",
            "builder_outputs_are_evidence_only": True,
            "builder_identity_must_differ_from_verifier": True,
            "requires_fresh_verification": True,
        },
        "commands": [
            {
                "cmd": "python scripts/sync_plugin_bundle.py",
                "exit_code": sync_exit_code,
                "artifact": ".agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-run.json",
            },
            {
                "cmd": "python scripts/sync_plugin_bundle.py --check",
                "exit_code": sync_check_exit_code,
                "artifact": ".agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-check.json",
            },
            {
                "cmd": "Get-Content -Raw plugin/.codex-plugin/plugin.json",
                "exit_code": 0,
                "artifact": ".agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-manifest-check.json",
            },
            {
                "cmd": "Get-Content -Raw plugin/.mcp.json",
                "exit_code": 0,
                "artifact": ".agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-mcp-check.json",
            },
            {
                "cmd": "Get-Content -Raw .agents/plugins/marketplace.json",
                "exit_code": 0,
                "artifact": ".agent/tasks/codex-material-3-stage-3-plugin/raw/marketplace-check.json",
            },
            {
                "cmd": "Get-ChildItem -Recurse .agents/skills/material,plugin/skills/material",
                "exit_code": 0,
                "artifact": ".agent/tasks/codex-material-3-stage-3-plugin/raw/canonical-bundle-hashes.json",
            },
        ],
        "artifacts": artifacts,
        "ac_map": {
            "AC3.1": ["plugin/.codex-plugin/plugin.json", ".agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-manifest-check.json"],
            "AC3.2": [".agent/tasks/codex-material-3-stage-3-plugin/raw/canonical-bundle-hashes.json"],
            "AC3.3": ["plugin/README.md", "docs/packaging-sync-policy.md"],
            "AC3.4": ["plugin/.mcp.json", ".agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-mcp-check.json"],
            "AC3.5": [".agents/plugins/marketplace.json", ".agent/tasks/codex-material-3-stage-3-plugin/raw/marketplace-check.json"],
            "AC3.6": [
                "scripts/sync_plugin_bundle.py",
                ".agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-run.json",
                ".agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-check.json",
                ".agent/tasks/codex-material-3-stage-3-plugin/raw/canonical-bundle-hashes.json",
                "docs/packaging-sync-policy.md",
            ],
        },
        "release_metadata": {
            "current_version": current_version,
            "target_version": target_version,
            "tag": f"v{target_version}",
            "release_commit_message": f"release: v{target_version}",
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
    command_shape_ok = isinstance(commands, list) and all(isinstance(command, dict) and "cmd" in command for command in commands)
    artifact_shape_ok = isinstance(artifacts, list) and all(isinstance(artifact, dict) and "path" in artifact for artifact in artifacts)
    builder_identity = evidence.get("builder_identity")
    proof_policy = evidence.get("proof_policy", {})

    artifact_paths = {artifact["path"]: ROOT / artifact["path"] for artifact in artifacts} if artifact_shape_ok else {}
    raw_payloads: dict[str, Any] = {}
    missing_artifacts: list[str] = []
    invalid_artifacts: list[str] = []
    for artifact_path, absolute_path in artifact_paths.items():
        if not absolute_path.exists():
            missing_artifacts.append(artifact_path)
            continue
        try:
            raw_payloads[artifact_path] = _load_json(absolute_path)
        except json.JSONDecodeError:
            invalid_artifacts.append(artifact_path)

    manifest_payload = raw_payloads.get(".agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-manifest-check.json", {})
    mcp_payload = raw_payloads.get(".agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-mcp-check.json", {})
    marketplace_payload = raw_payloads.get(".agent/tasks/codex-material-3-stage-3-plugin/raw/marketplace-check.json", {})
    sync_run_payload = raw_payloads.get(".agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-run.json", {})
    sync_check_payload = raw_payloads.get(".agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-check.json", {})
    hash_payload = raw_payloads.get(".agent/tasks/codex-material-3-stage-3-plugin/raw/canonical-bundle-hashes.json", {})

    plugin_readme_text = PLUGIN_README.read_text(encoding="utf-8")
    sync_policy_text = SYNC_POLICY.read_text(encoding="utf-8")
    canonical_skill_text = (CANONICAL_SKILL / "SKILL.md").read_text(encoding="utf-8")
    bundled_skill_exists = BUNDLED_SKILL.exists()

    ac_results: list[dict[str, Any]] = []
    problems: list[str] = []

    if not command_shape_ok:
        problems.append("Evidence file is missing `cmd` keys on one or more command entries.")
    if not artifact_shape_ok:
        problems.append("Evidence file is missing `path` keys on one or more artifact entries.")
    if missing_artifacts:
        problems.append(f"Missing raw artifacts: {', '.join(missing_artifacts)}.")
    if invalid_artifacts:
        problems.append(f"Non-JSON raw artifacts: {', '.join(invalid_artifacts)}.")

    ac31_pass = (
        manifest_payload.get("name") == "material-3-md3-workflows"
        and manifest_payload.get("skills") == "./skills/"
        and manifest_payload.get("mcpServers") == "./.mcp.json"
        and manifest_payload.get("interface", {}).get("displayName") == "Material 3 MD3 Workflows"
        and manifest_payload.get("interface", {}).get("category") == "Productivity"
        and set(manifest_payload.get("interface", {}).get("capabilities", [])) == {"Read", "Write", "Audit"}
    )
    if not ac31_pass:
        problems.append("AC3.1 failed: plugin manifest is missing required MD3 workflow metadata.")
    ac_results.append(
        {
            "id": "AC3.1",
            "status": "PASS" if ac31_pass else "FAIL",
            "reason": (
                "The plugin manifest exists and positions the bundle as a Material 3 workflow plugin for Codex."
                if ac31_pass
                else "Plugin manifest metadata is incomplete or does not describe the MD3 workflow plugin correctly."
            ),
            "evidence_refs": ["plugin/.codex-plugin/plugin.json", ".agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-manifest-check.json"],
        }
    )

    ac32_pass = (
        bundled_skill_exists
        and hash_payload.get("target_exists") is True
        and hash_payload.get("matches") is True
        and any(item.get("path") == "SKILL.md" for item in hash_payload.get("target_files", []))
        and len(hash_payload.get("target_files", [])) >= 4
    )
    if not ac32_pass:
        problems.append("AC3.2 failed: bundled skill copy is missing or incomplete under plugin/skills/material.")
    ac_results.append(
        {
            "id": "AC3.2",
            "status": "PASS" if ac32_pass else "FAIL",
            "reason": (
                "The bundled skill copy exists under plugin/skills/material and is populated with the expected files."
                if ac32_pass
                else "Bundled skill files are missing, incomplete, or out of sync."
            ),
            "evidence_refs": [".agent/tasks/codex-material-3-stage-3-plugin/raw/canonical-bundle-hashes.json"],
        }
    )

    ac33_pass = (
        "Canonical editable skill" in plugin_readme_text
        and "Bundled packaging artifact" in plugin_readme_text
        and "Do not treat `plugin/skills/material/` as the primary authoring surface." in plugin_readme_text
        and "## Install" in plugin_readme_text
        and "## Upgrade" in plugin_readme_text
        and "## Rollback" in plugin_readme_text
        and "## Internal distribution" in plugin_readme_text
        and "Canonical skill: `.agents/skills/material/`" in sync_policy_text
        and "Bundled plugin skill: `plugin/skills/material/`" in sync_policy_text
        and "Do not treat plugin-bundled skill files as the canonical authoring surface." in canonical_skill_text
    )
    if not ac33_pass:
        problems.append("AC3.3 failed: source-of-truth and derived-bundle boundaries are not documented clearly enough.")
    ac_results.append(
        {
            "id": "AC3.3",
            "status": "PASS" if ac33_pass else "FAIL",
            "reason": (
                "Docs explicitly describe plugin/skills/material as a derived packaging artifact and preserve canonical authoring in .agents/skills/material."
                if ac33_pass
                else "Install or sync docs do not clearly document the canonical-vs-bundled boundary."
            ),
            "evidence_refs": ["plugin/README.md", "docs/packaging-sync-policy.md", ".agents/skills/material/SKILL.md"],
        }
    )

    material3_server = mcp_payload.get("mcpServers", {}).get("material-3", {})
    ac34_pass = (
        material3_server.get("type") == "stdio"
        and material3_server.get("command") == "python"
        and material3_server.get("args") == ["../mcp/server.py"]
        and material3_server.get("cwd") == ".."
        and "Optional deterministic Material Design 3 MCP server" in material3_server.get("note", "")
    )
    if not ac34_pass:
        problems.append("AC3.4 failed: bundled .mcp.json is missing or not aligned with the repo-local MD3 server path.")
    ac_results.append(
        {
            "id": "AC3.4",
            "status": "PASS" if ac34_pass else "FAIL",
            "reason": (
                "Bundled MCP configuration exists and remains explicitly optional while targeting the repo-local MD3 server."
                if ac34_pass
                else "Bundled MCP configuration is missing required repo-local server metadata."
            ),
            "evidence_refs": ["plugin/.mcp.json", ".agent/tasks/codex-material-3-stage-3-plugin/raw/plugin-mcp-check.json"],
        }
    )

    ac35_pass = (
        marketplace_payload.get("name") == "material-3-md3-workflows"
        and marketplace_payload.get("source", {}).get("source") == "local"
        and marketplace_payload.get("source", {}).get("path") == "./plugin"
        and marketplace_payload.get("policy", {}).get("installation") == "AVAILABLE"
        and marketplace_payload.get("policy", {}).get("authentication") == "ON_INSTALL"
        and marketplace_payload.get("category") == "Productivity"
    )
    if not ac35_pass:
        problems.append("AC3.5 failed: marketplace metadata is missing the expected local plugin entry.")
    ac_results.append(
        {
            "id": "AC3.5",
            "status": "PASS" if ac35_pass else "FAIL",
            "reason": (
                "A local marketplace entry exists and points to the repo-local plugin bundle."
                if ac35_pass
                else "Marketplace metadata is missing the expected local plugin entry or policy fields."
            ),
            "evidence_refs": [".agents/plugins/marketplace.json", ".agent/tasks/codex-material-3-stage-3-plugin/raw/marketplace-check.json"],
        }
    )

    proof_policy_ok = (
        proof_policy.get("raw_artifact_format") == "json"
        and proof_policy.get("builder_outputs_are_evidence_only") is True
        and proof_policy.get("builder_identity_must_differ_from_verifier") is True
        and proof_policy.get("requires_fresh_verification") is True
        and builder_identity != verifier_identity
    )
    sync_payloads_ok = (
        sync_run_payload.get("status") == "PASS"
        and sync_check_payload.get("status") == "PASS"
        and sync_run_payload.get("matches") is True
        and sync_check_payload.get("matches") is True
        and not sync_check_payload.get("missing_in_target")
        and not sync_check_payload.get("extra_in_target")
        and not sync_check_payload.get("content_mismatches")
        and hash_payload.get("matches") is True
        and not hash_payload.get("missing_in_target")
        and not hash_payload.get("extra_in_target")
        and not hash_payload.get("content_mismatches")
    )
    doc_policy_ok = (
        "Synchronize the bundled skill with `python scripts/sync_plugin_bundle.py`." in sync_policy_text
        and "The sync script must remove stale bundle files." in sync_policy_text
        and "The sync check must compare file content hashes, not only filenames." in sync_policy_text
        and "Fresh verification must prove sync before release signoff." in sync_policy_text
        and SYNC_SCRIPT.exists()
    )
    ac36_pass = command_shape_ok and artifact_shape_ok and proof_policy_ok and sync_payloads_ok and doc_policy_ok
    if not ac36_pass:
        problems.append("AC3.6 failed: sync policy, sync evidence, or fresh-verifier separation is incomplete.")
    ac_results.append(
        {
            "id": "AC3.6",
            "status": "PASS" if ac36_pass else "FAIL",
            "reason": (
                "Packaging sync rules are documented and fresh verification proves the bundled skill matches the canonical source with no stale files."
                if ac36_pass
                else "Sync rules, sync artifacts, or fresh verifier separation do not fully prove canonical-to-bundle synchronization."
            ),
            "evidence_refs": [
                "scripts/sync_plugin_bundle.py",
                ".agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-run.json",
                ".agent/tasks/codex-material-3-stage-3-plugin/raw/bundle-sync-check.json",
                ".agent/tasks/codex-material-3-stage-3-plugin/raw/canonical-bundle-hashes.json",
                "docs/packaging-sync-policy.md",
                str(EVIDENCE_JSON.relative_to(ROOT)),
            ],
        }
    )

    verdict_status = "PASS" if all(item["status"] == "PASS" for item in ac_results) else "FAIL"
    verdict = {
        "task_id": TASK_ID,
        "verifier_identity": verifier_identity,
        "verdict": verdict_status,
        "summary": (
            "Fresh verification confirms the installable MD3 plugin bundle, marketplace entry, optional MCP config, and canonical-to-bundle sync proof satisfy the stage-3 task."
            if verdict_status == "PASS"
            else "Fresh verification found stage-3 plugin proof-loop gaps that require fixes."
        ),
        "acceptance_criteria": ac_results,
        "release_checks": [],
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
    parser = argparse.ArgumentParser(description="Repo-task-proof-loop helper for codex-material-3-stage-3-plugin.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--expected-version", help="Version expected by the stage-3 packaging proof.")
    build_parser.add_argument("--builder-identity", default=DEFAULT_BUILDER_IDENTITY)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--verifier-identity", default=DEFAULT_VERIFIER_IDENTITY)

    args = parser.parse_args()
    if args.command == "build":
        build(expected_version=args.expected_version, builder_identity=args.builder_identity)
        return 0
    return verify(verifier_identity=args.verifier_identity)


if __name__ == "__main__":
    raise SystemExit(main())
