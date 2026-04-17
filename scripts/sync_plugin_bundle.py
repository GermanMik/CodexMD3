from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".agents" / "skills" / "material"
TARGET = ROOT / "plugin" / "skills" / "material"


def _hash_directory(path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    if not path.exists():
        return hashes
    for file_path in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        hashes[file_path.relative_to(path).as_posix()] = hashlib.sha256(file_path.read_bytes()).hexdigest()
    return hashes


def _compare() -> dict:
    source_hashes = _hash_directory(SOURCE)
    target_hashes = _hash_directory(TARGET)
    return {
        "source_exists": SOURCE.exists(),
        "target_exists": TARGET.exists(),
        "matches": source_hashes == target_hashes and bool(source_hashes),
        "source_files": sorted(source_hashes.keys()),
        "target_files": sorted(target_hashes.keys()),
        "missing_in_target": sorted(set(source_hashes) - set(target_hashes)),
        "extra_in_target": sorted(set(target_hashes) - set(source_hashes)),
        "content_mismatches": sorted(
            relative
            for relative in set(source_hashes).intersection(target_hashes)
            if source_hashes[relative] != target_hashes[relative]
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize canonical Material 3 skill into the plugin bundle.")
    parser.add_argument("--check", action="store_true", help="Only verify sync state.")
    args = parser.parse_args()

    if not SOURCE.exists():
        raise SystemExit("Canonical skill source does not exist.")

    if not args.check:
        if TARGET.exists():
            shutil.rmtree(TARGET)
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(SOURCE, TARGET)

    comparison = _compare()
    comparison["mode"] = "check" if args.check else "sync"
    comparison["status"] = "PASS" if comparison["matches"] else "FAIL"
    print(json.dumps(comparison, indent=2))
    return 0 if comparison["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
