from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from domain import (
    check_md3_release_consistency,
    generate_theme_scaffold,
    get_layout_rule,
    get_platform_matrix,
    lookup_md3_component,
    lookup_md3_token,
    score_md3_audit,
)


def _load_findings(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "findings" in data and isinstance(data["findings"], list):
        return data["findings"]
    raise ValueError("Findings file must contain a JSON array or an object with a 'findings' array.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic Material Design 3 MCP CLI harness.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    token_parser = subparsers.add_parser("lookup-token")
    token_parser.add_argument("--category", required=True)
    token_parser.add_argument("--token-name")
    token_parser.add_argument("--platform", default="compose")
    token_parser.add_argument("--no-related", action="store_true")

    component_parser = subparsers.add_parser("lookup-component")
    component_parser.add_argument("--component", required=True)
    component_parser.add_argument("--platform", default="compose")

    matrix_parser = subparsers.add_parser("platform-matrix")
    matrix_parser.add_argument("--topic")

    layout_parser = subparsers.add_parser("layout-rule")
    layout_parser.add_argument("--rule", required=True)
    layout_parser.add_argument("--platform", default="compose")
    layout_parser.add_argument("--window-class")

    theme_parser = subparsers.add_parser("theme-scaffold")
    theme_parser.add_argument("--seed-color", required=True)
    theme_parser.add_argument("--platform", default="compose")
    theme_parser.add_argument("--dark-mode", default="paired")
    theme_parser.add_argument("--contrast", default="standard")
    theme_parser.add_argument("--dynamic-color", default="allowed")

    audit_parser = subparsers.add_parser("score-audit")
    audit_parser.add_argument("--findings-file", required=True)

    release_parser = subparsers.add_parser("check-release-consistency")
    release_parser.add_argument("--repo-root")
    release_parser.add_argument("--expected-version")
    release_parser.add_argument("--target-tag")
    release_parser.add_argument("--release-commit-message")
    release_parser.add_argument("--release-notes")

    args = parser.parse_args()

    try:
        if args.command == "lookup-token":
            result = lookup_md3_token(
                category=args.category,
                token_name=args.token_name,
                platform=args.platform,
                include_related=not args.no_related,
            )
        elif args.command == "lookup-component":
            result = lookup_md3_component(component_id=args.component, platform=args.platform)
        elif args.command == "platform-matrix":
            result = get_platform_matrix(topic=args.topic)
        elif args.command == "layout-rule":
            result = get_layout_rule(rule_id=args.rule, platform=args.platform, window_class=args.window_class)
        elif args.command == "theme-scaffold":
            result = generate_theme_scaffold(
                seed_color=args.seed_color,
                platform=args.platform,
                dark_mode=args.dark_mode,
                contrast=args.contrast,
                dynamic_color=args.dynamic_color,
            )
        elif args.command == "score-audit":
            result = score_md3_audit(_load_findings(args.findings_file))
        else:
            result = check_md3_release_consistency(
                repo_root=args.repo_root,
                expected_version=args.expected_version,
                target_tag=args.target_tag,
                release_commit_message=args.release_commit_message,
                release_notes_path=args.release_notes,
            )
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:  # pragma: no cover - CLI path
        print(json.dumps({"status": "ERROR", "error": str(exc)}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
