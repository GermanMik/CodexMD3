from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


VERSION_RE = re.compile(
    r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:-(?P<label>rc|beta)\.(?P<label_num>\d+))?$"
)


@dataclass(frozen=True)
class SemVer:
    major: int
    minor: int
    patch: int
    label: str | None = None
    label_num: int | None = None

    def __str__(self) -> str:
        core = f"{self.major}.{self.minor}.{self.patch}"
        if self.label:
            return f"{core}-{self.label}.{self.label_num}"
        return core


def parse_version(version: str) -> SemVer:
    match = VERSION_RE.match(version)
    if not match:
        raise ValueError(f"Invalid semantic version '{version}'.")
    groups = match.groupdict()
    return SemVer(
        major=int(groups["major"]),
        minor=int(groups["minor"]),
        patch=int(groups["patch"]),
        label=groups["label"],
        label_num=int(groups["label_num"]) if groups["label_num"] else None,
    )


def bump_version(current_version: str, bump: str, prerelease: str | None = None) -> str:
    current = parse_version(current_version)
    if bump == "major":
        target = SemVer(current.major + 1, 0, 0)
    elif bump == "minor":
        target = SemVer(current.major, current.minor + 1, 0)
    elif bump == "patch":
        target = SemVer(current.major, current.minor, current.patch + 1)
    else:
        raise ValueError("bump must be one of: major, minor, patch.")

    if prerelease:
        if prerelease not in {"rc", "beta"}:
            raise ValueError("prerelease must be rc or beta.")
        target = SemVer(target.major, target.minor, target.patch, prerelease, 1)
    return str(target)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def get_current_version(root: Path | None = None) -> str:
    repo_root = root or get_repo_root()
    manifest = load_json(repo_root / "plugin" / ".codex-plugin" / "plugin.json")
    return manifest["version"]


def build_release_notes(version: str, summary: str | None = None) -> str:
    summary_line = summary or "Release-ready Material Design 3 capability update."
    return "\n".join(
        [
            f"# Release v{version}",
            "",
            "## Summary",
            f"- {summary_line}",
            "",
            "## Included surfaces",
            "- Canonical Material 3 skill",
            "- Deterministic MD3 MCP layer",
            "- Plugin bundle and marketplace metadata",
            "- Release policies, scripts, and validation artifacts",
            "",
            "## Verification",
            "- Packaging sync validated",
            "- Version-bearing files aligned",
            "- Release checks passed in dry-run validation",
            "",
        ]
    )
