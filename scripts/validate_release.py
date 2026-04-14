from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp"))

from domain import check_md3_release_consistency  # noqa: E402
from release_helpers import bump_version, get_current_version, parse_version  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate release readiness and emit RC1-RC12 status.")
    parser.add_argument("--expected-version", help="Version that should currently be reflected in repo release surfaces.")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], help="Optional next-version planning check.")
    parser.add_argument("--prerelease", choices=["rc", "beta"], help="Optional prerelease suffix for the next-version planning check.")
    parser.add_argument("--release-notes", help="Path to the release notes draft.")
    parser.add_argument("--release-commit-message")
    parser.add_argument("--target-tag")
    args = parser.parse_args()

    current_version = get_current_version(ROOT)
    expected_version = args.expected_version or current_version
    parse_version(expected_version)
    next_version = bump_version(current_version, args.bump, args.prerelease) if args.bump else current_version

    release_commit_message = args.release_commit_message or f"release: v{expected_version}"
    target_tag = args.target_tag or f"v{expected_version}"
    consistency = check_md3_release_consistency(
        repo_root=str(ROOT),
        expected_version=expected_version,
        target_tag=target_tag,
        release_commit_message=release_commit_message,
        release_notes_path=args.release_notes,
    )
    check_map = {item["id"]: item for item in consistency["checks"]}

    rc_results = [
        {"id": "RC1", "status": "PASS" if check_map["current_version_detected"]["status"] == "PASS" else "FAIL", "reason": check_map["current_version_detected"]["reason"]},
        {"id": "RC2", "status": "PASS", "reason": f"Next version plan is {next_version} from current version {current_version}."},
        {"id": "RC3", "status": "PASS" if check_map["version_surface_alignment"]["status"] == "PASS" and check_map["expected_version_alignment"]["status"] == "PASS" else "FAIL", "reason": "Version-bearing files align with the expected release surface." if check_map["version_surface_alignment"]["status"] == "PASS" and check_map["expected_version_alignment"]["status"] == "PASS" else "Version-bearing files are not aligned."},
        {"id": "RC4", "status": "PASS" if check_map["version_surface_alignment"]["status"] == "PASS" else "FAIL", "reason": "CHANGELOG contains the release version header." if check_map["version_surface_alignment"]["status"] == "PASS" else "CHANGELOG is missing or drifted."},
        {"id": "RC5", "status": "PASS" if check_map["release_commit_policy"]["status"] == "PASS" else "FAIL", "reason": check_map["release_commit_policy"]["reason"]},
        {"id": "RC6", "status": "PASS" if check_map["tag_policy"]["status"] == "PASS" else "FAIL", "reason": check_map["tag_policy"]["reason"]},
        {"id": "RC7", "status": "PASS" if check_map["release_notes"]["status"] == "PASS" else "FAIL", "reason": check_map["release_notes"]["reason"]},
        {"id": "RC8", "status": "PASS" if check_map["expected_version_alignment"]["status"] == "PASS" else "FAIL", "reason": "Plugin and MCP metadata are aligned with the expected release version." if check_map["expected_version_alignment"]["status"] == "PASS" else check_map["expected_version_alignment"]["reason"]},
        {"id": "RC9", "status": "PASS" if check_map["version_surface_alignment"]["status"] == "PASS" and check_map["bundle_sync"]["status"] == "PASS" else "FAIL", "reason": "No version or bundle drift detected across release surfaces." if check_map["version_surface_alignment"]["status"] == "PASS" and check_map["bundle_sync"]["status"] == "PASS" else "Version or bundle drift detected."},
        {"id": "RC10", "status": "PASS" if check_map["bundle_sync"]["status"] == "PASS" else "FAIL", "reason": check_map["bundle_sync"]["reason"]},
        {"id": "RC11", "status": "PASS" if (ROOT / "docs" / "github-release-flow.md").exists() and (ROOT / ".github" / "workflows" / "publish-release.yml").exists() else "FAIL", "reason": "GitHub release publication path is documented and workflow-backed." if (ROOT / "docs" / "github-release-flow.md").exists() and (ROOT / ".github" / "workflows" / "publish-release.yml").exists() else "GitHub release publication path is incomplete."},
        {"id": "RC12", "status": "PASS" if (ROOT / "docs" / "release-policy.md").exists() and (ROOT / "docs" / "release-checklist.md").exists() else "FAIL", "reason": "Post-release verification is defined in release policy and checklist." if (ROOT / "docs" / "release-policy.md").exists() and (ROOT / "docs" / "release-checklist.md").exists() else "Post-release verification definition is incomplete."}
    ]

    overall_status = "PASS" if all(item["status"] == "PASS" for item in rc_results) else "FAIL"
    payload = {
        "status": overall_status,
        "current_version": current_version,
        "expected_version": expected_version,
        "next_version_plan": next_version,
        "release_commit_message": release_commit_message,
        "target_tag": target_tag,
        "release_consistency": consistency,
        "release_checks": rc_results,
    }
    print(json.dumps(payload, indent=2))
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
