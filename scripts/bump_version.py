from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

from release_helpers import get_repo_root, load_json, parse_version, save_json


def _ensure_changelog_entry(changelog_path: Path, version: str, entry_date: str) -> None:
    changelog = changelog_path.read_text(encoding="utf-8")
    header = f"## [{version}] - {entry_date}"
    if header in changelog:
        return
    insertion = "\n".join(
        [
            header,
            "### Added",
            "- TODO",
            "",
            "### Changed",
            "- TODO",
            "",
            "### Fixed",
            "- TODO",
            "",
            "### Removed",
            "- None.",
            "",
            "### Security",
            "- None.",
            "",
            "### Migration Notes",
            "- TODO",
            "",
        ]
    )
    if re.search(r"^## \[", changelog, re.MULTILINE):
        changelog = re.sub(r"(^## \[)", insertion + r"\n\1", changelog, count=1, flags=re.MULTILINE)
    else:
        changelog += "\n" + insertion
    changelog_path.write_text(changelog, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update version-bearing files for a target release version.")
    parser.add_argument("--version", required=True)
    parser.add_argument("--date", default=str(date.today()))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    parse_version(args.version)
    root = get_repo_root()
    plugin_manifest_path = root / "plugin" / ".codex-plugin" / "plugin.json"
    mcp_manifest_path = root / "mcp" / "manifest.json"
    changelog_path = root / "CHANGELOG.md"

    if args.dry_run:
        print(f"Would set plugin and MCP manifest versions to {args.version} and ensure changelog entry on {args.date}.")
        return 0

    plugin_manifest = load_json(plugin_manifest_path)
    plugin_manifest["version"] = args.version
    save_json(plugin_manifest_path, plugin_manifest)

    mcp_manifest = load_json(mcp_manifest_path)
    mcp_manifest["version"] = args.version
    save_json(mcp_manifest_path, mcp_manifest)

    _ensure_changelog_entry(changelog_path, args.version, args.date)
    print(f"Updated version-bearing files to {args.version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
