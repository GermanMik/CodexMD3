from __future__ import annotations

import argparse
import json
from pathlib import Path

from release_helpers import build_release_notes, bump_version, get_current_version, get_repo_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a release plan and notes draft.")
    parser.add_argument("--version", help="Explicit target version.")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], help="Calculate the next version from the current one.")
    parser.add_argument("--prerelease", choices=["rc", "beta"], help="Optional prerelease suffix for calculated version.")
    parser.add_argument("--notes-out", help="Write release notes draft to the given path.")
    parser.add_argument("--dry-run", action="store_true", help="Report the release plan without mutating repo files.")
    args = parser.parse_args()

    if not args.version and not args.bump:
        raise SystemExit("Provide either --version or --bump.")

    root = get_repo_root()
    current_version = get_current_version(root)
    target_version = args.version or bump_version(current_version, args.bump, args.prerelease)
    release_commit_message = f"release: v{target_version}"
    tag = f"v{target_version}"

    notes = build_release_notes(target_version)
    notes_path = None
    if args.notes_out:
        notes_path = Path(args.notes_out)
        notes_path.parent.mkdir(parents=True, exist_ok=True)
        notes_path.write_text(notes, encoding="utf-8")

    plan = {
        "dry_run": args.dry_run,
        "current_version": current_version,
        "target_version": target_version,
        "bump": args.bump,
        "prerelease": args.prerelease,
        "release_commit_message": release_commit_message,
        "tag": tag,
        "notes_path": str(notes_path) if notes_path else None,
    }
    print(json.dumps(plan, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
