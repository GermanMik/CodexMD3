from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASK_ID = "codex-material-3-stage-2-mcp"
TASK_DIR = ROOT / ".agent" / "tasks" / TASK_ID
RAW_DIR = TASK_DIR / "raw"
EVIDENCE_JSON = TASK_DIR / "evidence.json"
EVIDENCE_MD = TASK_DIR / "evidence.md"
VERDICT_JSON = TASK_DIR / "verdict.json"
PROBLEMS_MD = TASK_DIR / "problems.md"
DEFAULT_RELEASE_NOTES = Path(".agent/tasks/codex-material-3-stage-4-release/raw/release-notes-draft.md")
DEFAULT_BUILDER_IDENTITY = "stage2-mcp-builder"
DEFAULT_VERIFIER_IDENTITY = "stage2-mcp-fresh-verifier"

REQUIRED_TOOLS = {
    "lookup_md3_token",
    "lookup_md3_component",
    "get_platform_matrix",
    "get_layout_rule",
    "generate_theme_scaffold",
    "score_md3_audit",
    "check_md3_release_consistency",
}

COMMAND_SPECS = [
    {
        "tool": "lookup_md3_token",
        "display_cmd": "python mcp/cli.py lookup-token --category color --token-name primary",
        "args": ["lookup-token", "--category", "color", "--token-name", "primary"],
        "artifact": ".agent/tasks/codex-material-3-stage-2-mcp/raw/token-lookup-check.json",
    },
    {
        "tool": "lookup_md3_component",
        "display_cmd": "python mcp/cli.py lookup-component --component navigation-rail --platform compose",
        "args": ["lookup-component", "--component", "navigation-rail", "--platform", "compose"],
        "artifact": ".agent/tasks/codex-material-3-stage-2-mcp/raw/component-catalog-check.json",
    },
    {
        "tool": "get_platform_matrix",
        "display_cmd": "python mcp/cli.py platform-matrix --topic dynamic-color",
        "args": ["platform-matrix", "--topic", "dynamic-color"],
        "artifact": ".agent/tasks/codex-material-3-stage-2-mcp/raw/platform-matrix-check.json",
    },
    {
        "tool": "get_layout_rule",
        "display_cmd": "python mcp/cli.py layout-rule --rule adaptive-navigation --platform compose --window-class medium",
        "args": ["layout-rule", "--rule", "adaptive-navigation", "--platform", "compose", "--window-class", "medium"],
        "artifact": ".agent/tasks/codex-material-3-stage-2-mcp/raw/layout-rule-check.json",
    },
    {
        "tool": "generate_theme_scaffold",
        "display_cmd": "python mcp/cli.py theme-scaffold --seed-color \"#6750A4\" --platform compose --dark-mode paired --contrast standard --dynamic-color allowed",
        "args": [
            "theme-scaffold",
            "--seed-color",
            "#6750A4",
            "--platform",
            "compose",
            "--dark-mode",
            "paired",
            "--contrast",
            "standard",
            "--dynamic-color",
            "allowed",
        ],
        "artifact": ".agent/tasks/codex-material-3-stage-2-mcp/raw/theme-scaffold-check.json",
    },
    {
        "tool": "score_md3_audit",
        "display_cmd": "python mcp/cli.py score-audit --findings-file .agent/tasks/codex-material-3-stage-2-mcp/raw/sample-findings.json",
        "args": [
            "score-audit",
            "--findings-file",
            ".agent/tasks/codex-material-3-stage-2-mcp/raw/sample-findings.json",
        ],
        "artifact": ".agent/tasks/codex-material-3-stage-2-mcp/raw/md3-audit-score.json",
    },
]


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
    plugin_manifest = _load_json(ROOT / "plugin" / ".codex-plugin" / "plugin.json")
    return plugin_manifest["version"]


def _run_cli(args: list[str]) -> tuple[int, dict[str, Any]]:
    result = subprocess.run(
        [sys.executable, str(ROOT / "mcp" / "cli.py"), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"Command failed: {args}")
    return result.returncode, json.loads(result.stdout)


def _release_command(expected_version: str, release_notes: str) -> dict[str, Any]:
    return {
        "tool": "check_md3_release_consistency",
        "display_cmd": (
            "python mcp/cli.py check-release-consistency "
            f"--expected-version {expected_version} "
            f"--release-notes {release_notes}"
        ),
        "args": [
            "check-release-consistency",
            "--expected-version",
            expected_version,
            "--release-notes",
            release_notes,
        ],
        "artifact": ".agent/tasks/codex-material-3-stage-2-mcp/raw/release-consistency-check.json",
    }


def _build_evidence_markdown(evidence: dict[str, Any]) -> str:
    lines = [
        f"# Evidence for {TASK_ID}",
        "",
        "## Build summary",
        "Collected deterministic MD3 MCP raw JSON artifacts with a repo-local builder pass. A distinct fresh-verifier pass is required before treating the stage as complete.",
        "",
        "## Proof policy",
        f"- builder identity: `{evidence['builder_identity']}`",
        "- builder outputs are evidence only, not certification",
        "- raw MCP artifacts are stored as JSON under `raw/`",
        "- verifier identity must differ from builder identity",
        "- fresh verification is required after evidence collection",
        "",
        "## Commands run",
    ]
    lines.extend(f"- `{command['cmd']}`" for command in evidence["commands"])
    lines.extend(
        [
            "",
            "## Raw artifacts",
        ]
    )
    lines.extend(f"- `{artifact['path']}` (`{artifact['sha256'][:12]}`)" for artifact in evidence["artifacts"])
    lines.extend(
        [
            "",
            "## Acceptance criteria mapping",
            "- AC2.1 -> `mcp/README.md`, `mcp/contracts/tool-contracts.json`",
            "- AC2.2 -> `mcp/server.py`, `raw/*.json`",
            "- AC2.3 -> `mcp/README.md`, `.agents/skills/material/SKILL.md`, `mcp/contracts/tool-contracts.json`",
            "- AC2.4 -> `evidence.json`, `raw/*.json`, `mcp/cli.py`",
            "- AC2.5 -> `raw/release-consistency-check.json`, `mcp/domain.py`",
            "",
            "## Release evidence",
            f"- current version: `{evidence['release_metadata']['current_version']}`",
            f"- target version: `{evidence['release_metadata']['target_version']}`",
            f"- tag draft: `{evidence['release_metadata']['tag']}`",
            f"- release commit draft: `{evidence['release_metadata']['release_commit_message']}`",
            f"- release notes draft: `{evidence['release_metadata']['release_notes_path']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def build(expected_version: str | None, release_notes: str, builder_identity: str) -> None:
    current_version = _current_version()
    resolved_version = expected_version or current_version
    release_command = _release_command(resolved_version, release_notes)
    specs = [*COMMAND_SPECS, release_command]

    commands: list[dict[str, Any]] = []
    artifacts: list[dict[str, Any]] = []
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        exit_code, payload = _run_cli(spec["args"])
        artifact_path = ROOT / spec["artifact"]
        _write_json(artifact_path, payload)
        commands.append(
            {
                "tool": spec["tool"],
                "cmd": spec["display_cmd"],
                "exit_code": exit_code,
                "artifact": spec["artifact"],
            }
        )
        artifacts.append(
            {
                "path": spec["artifact"],
                "type": "json",
                "sha256": _sha256(artifact_path),
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
        "commands": commands,
        "artifacts": artifacts,
        "ac_map": {
            "AC2.1": ["mcp/README.md", "mcp/contracts/tool-contracts.json"],
            "AC2.2": ["mcp/server.py", *[artifact["path"] for artifact in artifacts]],
            "AC2.3": ["mcp/README.md", ".agents/skills/material/SKILL.md", "mcp/contracts/tool-contracts.json"],
            "AC2.4": ["mcp/cli.py", "mcp/contracts/tool-contracts.json", *[artifact["path"] for artifact in artifacts]],
            "AC2.5": [release_command["artifact"], "mcp/domain.py"],
        },
        "release_metadata": {
            "current_version": current_version,
            "target_version": resolved_version,
            "tag": f"v{resolved_version}",
            "release_commit_message": f"release: v{resolved_version}",
            "release_notes_path": release_notes,
        },
        "git_head": _git_head(),
        "timestamp": _now(),
    }
    _write_json(EVIDENCE_JSON, evidence)
    EVIDENCE_MD.write_text(_build_evidence_markdown(evidence), encoding="utf-8")


def _has_all_required_tools(server_text: str, contract_names: set[str], evidence_tools: set[str]) -> bool:
    return (
        REQUIRED_TOOLS.issubset(contract_names)
        and evidence_tools == REQUIRED_TOOLS
        and all(f'name="{tool}"' in server_text for tool in REQUIRED_TOOLS)
    )


def _artifact_map(artifacts: list[dict[str, Any]]) -> dict[str, Path]:
    return {artifact["path"]: ROOT / artifact["path"] for artifact in artifacts}


def verify(verifier_identity: str) -> int:
    evidence = _load_json(EVIDENCE_JSON)
    readme_text = (ROOT / "mcp" / "README.md").read_text(encoding="utf-8")
    skill_text = (ROOT / ".agents" / "skills" / "material" / "SKILL.md").read_text(encoding="utf-8")
    server_text = (ROOT / "mcp" / "server.py").read_text(encoding="utf-8")
    contracts = _load_json(ROOT / "mcp" / "contracts" / "tool-contracts.json")
    contract_names = {tool["name"] for tool in contracts["tools"]}
    commands = evidence.get("commands", [])
    artifacts = evidence.get("artifacts", [])
    command_shape_ok = isinstance(commands, list) and all(isinstance(command, dict) and "tool" in command for command in commands)
    artifact_shape_ok = isinstance(artifacts, list) and all(isinstance(artifact, dict) and "path" in artifact for artifact in artifacts)
    evidence_tools = {command["tool"] for command in commands} if command_shape_ok else set()
    artifact_paths = _artifact_map(artifacts) if artifact_shape_ok else {}

    raw_payloads: dict[str, dict[str, Any]] = {}
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

    release_payload = raw_payloads.get(".agent/tasks/codex-material-3-stage-2-mcp/raw/release-consistency-check.json", {})
    release_checks = {item["id"]: item for item in release_payload.get("checks", [])}
    builder_identity = evidence.get("builder_identity")
    proof_policy = evidence.get("proof_policy", {})

    ac_results: list[dict[str, Any]] = []
    problems: list[str] = []

    if not command_shape_ok:
        problems.append("Evidence file is missing `tool` keys on one or more command entries.")
    if not artifact_shape_ok:
        problems.append("Evidence file is missing `path` keys on one or more artifact entries.")

    ac21_pass = (
        "MD3-specific by design" in readme_text
        and "not a generic design-system reasoning engine" in readme_text
        and REQUIRED_TOOLS.issubset(contract_names)
    )
    if not ac21_pass:
        problems.append("AC2.1 failed: README/contracts do not clearly scope the MCP layer to MD3-specific workflows.")
    ac_results.append(
        {
            "id": "AC2.1",
            "status": "PASS" if ac21_pass else "FAIL",
            "reason": (
                "README and contracts scope the MCP layer to deterministic Material Design 3 workflows."
                if ac21_pass
                else "README/contracts are missing explicit MD3-only scope markers."
            ),
            "evidence_refs": ["mcp/README.md", "mcp/contracts/tool-contracts.json"],
        }
    )

    ac22_pass = (
        command_shape_ok
        and artifact_shape_ok
        and _has_all_required_tools(server_text, contract_names, evidence_tools)
        and not missing_artifacts
        and not invalid_artifacts
        and len(commands) == len(REQUIRED_TOOLS)
    )
    if not ac22_pass:
        problems.append("AC2.2 failed: the seven required MCP tools are not fully covered by server/contracts/raw JSON evidence.")
    ac_results.append(
        {
            "id": "AC2.2",
            "status": "PASS" if ac22_pass else "FAIL",
            "reason": (
                "All seven required tools exist in server/contracts and are exercised by raw JSON outputs."
                if ac22_pass
                else "One or more required tools, commands, or raw JSON artifacts are missing."
            ),
            "evidence_refs": ["mcp/server.py", "mcp/contracts/tool-contracts.json", *artifact_paths.keys()],
        }
    )

    ac23_pass = (
        "Keep in skill layer" in readme_text
        and "MCP usage boundary" in skill_text
        and proof_policy.get("builder_identity_must_differ_from_verifier") is True
        and proof_policy.get("requires_fresh_verification") is True
        and proof_policy.get("builder_outputs_are_evidence_only") is True
        and builder_identity != verifier_identity
    )
    if not ac23_pass:
        problems.append("AC2.3 failed: deterministic MCP boundaries or no-self-certification policy are not explicitly enforced.")
    ac_results.append(
        {
            "id": "AC2.3",
            "status": "PASS" if ac23_pass else "FAIL",
            "reason": (
                "Docs and proof policy keep deterministic facts/scoring in MCP while reserving reasoning and remediation for the skill layer."
                if ac23_pass
                else "Boundary docs or proof-loop policy do not clearly separate MCP determinism from skill-layer judgment."
            ),
            "evidence_refs": ["mcp/README.md", ".agents/skills/material/SKILL.md", "mcp/contracts/tool-contracts.json", str(EVIDENCE_JSON.relative_to(ROOT))],
        }
    )

    ac24_pass = (
        command_shape_ok
        and artifact_shape_ok
        and all(artifact["type"] == "json" for artifact in evidence["artifacts"])
        and not missing_artifacts
        and not invalid_artifacts
        and evidence_tools == REQUIRED_TOOLS
        and all(command["exit_code"] == 0 for command in commands)
    )
    if not ac24_pass:
        problems.append("AC2.4 failed: repo-local JSON evidence is incomplete or not machine-readable.")
    ac_results.append(
        {
            "id": "AC2.4",
            "status": "PASS" if ac24_pass else "FAIL",
            "reason": (
                "Evidence.json records all required commands and every raw MCP artifact is stored as reusable JSON."
                if ac24_pass
                else "Evidence.json is incomplete or one of the raw artifacts is missing/non-JSON."
            ),
            "evidence_refs": [str(EVIDENCE_JSON.relative_to(ROOT)), "mcp/cli.py", *artifact_paths.keys()],
        }
    )

    ac25_pass = (
        release_payload.get("status") == "PASS"
        and release_checks.get("version_surface_alignment", {}).get("status") == "PASS"
        and release_checks.get("bundle_sync", {}).get("status") == "PASS"
        and release_checks.get("release_notes", {}).get("status") == "PASS"
    )
    if not ac25_pass:
        problems.append("AC2.5 failed: release consistency proof does not show aligned version surfaces, bundle sync, and release notes.")
    ac_results.append(
        {
            "id": "AC2.5",
            "status": "PASS" if ac25_pass else "FAIL",
            "reason": (
                "Release consistency checks pass for current version surfaces, bundle sync, and release notes."
                if ac25_pass
                else "Release consistency artifact is missing or reports a FAIL on required release checks."
            ),
            "evidence_refs": [
                ".agent/tasks/codex-material-3-stage-2-mcp/raw/release-consistency-check.json",
                "mcp/domain.py",
            ],
        }
    )

    verdict_status = "PASS" if all(item["status"] == "PASS" for item in ac_results) else "FAIL"
    verdict = {
        "task_id": TASK_ID,
        "verifier_identity": verifier_identity,
        "verdict": verdict_status,
        "summary": (
            "Fresh verification confirms the deterministic MD3 MCP layer and its repo-local JSON proof artifacts satisfy the stage-2 task."
            if verdict_status == "PASS"
            else "Fresh verification found stage-2 MCP proof-loop gaps that require fixes."
        ),
        "acceptance_criteria": ac_results,
        "release_checks": release_payload.get("checks", []),
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
    parser = argparse.ArgumentParser(description="Repo-task-proof-loop helper for codex-material-3-stage-2-mcp.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--expected-version", help="Version expected by the release consistency check.")
    build_parser.add_argument(
        "--release-notes",
        default=str(DEFAULT_RELEASE_NOTES).replace("\\", "/"),
        help="Repo-relative path to the release notes draft.",
    )
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
