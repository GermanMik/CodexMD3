from __future__ import annotations

import colorsys
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(__file__).resolve().parent / "data"


def _load_json(name: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def _normalize_key(value: str) -> str:
    return value.strip().lower().replace("_", "-").replace(" ", "-")


def _validate_platform(platform: str) -> str:
    normalized = _normalize_key(platform)
    if normalized not in {"compose", "flutter", "web"}:
        raise ValueError(f"Unsupported platform '{platform}'. Use compose, flutter, or web.")
    return normalized


def lookup_md3_token(
    category: str,
    token_name: str | None = None,
    platform: str = "compose",
    include_related: bool = True,
) -> dict[str, Any]:
    platform = _validate_platform(platform)
    data = _load_json("tokens.json")
    categories = data["categories"]
    category_key = _normalize_key(category)
    if category_key not in categories:
        raise ValueError(f"Unknown token category '{category}'.")
    category_data = categories[category_key]
    if token_name is None:
        return {
            "category": category_key,
            "description": category_data["description"],
            "platform": platform,
            "tokens": [
                {
                    "id": token_id,
                    "summary": token["summary"],
                    "platform_note": token["platform_notes"][platform],
                }
                for token_id, token in sorted(category_data["tokens"].items())
            ],
        }

    token_key = _normalize_key(token_name)
    tokens = category_data["tokens"]
    if token_key not in tokens:
        raise ValueError(f"Unknown token '{token_name}' in category '{category_key}'.")
    token = tokens[token_key]
    response = {
        "category": category_key,
        "token": token_key,
        "summary": token["summary"],
        "platform": platform,
        "platform_note": token["platform_notes"][platform],
    }
    if include_related:
        response["related"] = token["related"]
    return response


def lookup_md3_component(component_id: str, platform: str = "compose") -> dict[str, Any]:
    platform = _validate_platform(platform)
    components = _load_json("components.json")["components"]
    key = _normalize_key(component_id)
    if key not in components:
        raise ValueError(f"Unknown component '{component_id}'.")
    component = components[key]
    return {
        "component": key,
        "summary": component["summary"],
        "use_when": component["use_when"],
        "avoid_when": component["avoid_when"],
        "required_states": component["required_states"],
        "accessibility_notes": component["accessibility_notes"],
        "related_tokens": component["related_tokens"],
        "platform": platform,
        "platform_note": component["platform_notes"][platform],
    }


def get_platform_matrix(topic: str | None = None) -> dict[str, Any]:
    data = _load_json("platform-matrix.json")
    if topic is None:
        return data
    key = _normalize_key(topic)
    if key in data["topics"]:
        return {"topic": key, "matrix": data["topics"][key]}
    if key in data["platforms"]:
        return {"platform": key, **data["platforms"][key]}
    raise ValueError(f"Unknown matrix topic '{topic}'.")


def get_layout_rule(
    rule_id: str,
    platform: str = "compose",
    window_class: str | None = None,
) -> dict[str, Any]:
    platform = _validate_platform(platform)
    rules = _load_json("layout-rules.json")["rules"]
    key = _normalize_key(rule_id)
    if key not in rules:
        raise ValueError(f"Unknown layout rule '{rule_id}'.")
    rule = rules[key]
    response = {
        "rule": key,
        "summary": rule["summary"],
        "platform": platform,
        "platform_note": rule["platform_notes"][platform],
        "window_class_guidance": rule["window_class_guidance"],
    }
    if window_class:
        wc_key = _normalize_key(window_class)
        if wc_key not in rule["window_class_guidance"]:
            raise ValueError(f"Unknown window class '{window_class}' for rule '{key}'.")
        response["selected_window_class"] = wc_key
        response["selected_guidance"] = rule["window_class_guidance"][wc_key]
    return response


def _hex_to_rgb(seed_color: str) -> tuple[float, float, float]:
    value = seed_color.strip().lstrip("#")
    if len(value) != 6 or any(ch not in "0123456789abcdefABCDEF" for ch in value):
        raise ValueError("seed_color must be a 6-digit hex color such as '#6750A4'.")
    return tuple(int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def _rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{round(max(0, min(1, channel)) * 255):02X}" for channel in rgb)


def _build_palette(hue: float, saturation: float) -> dict[str, str]:
    tones = [0, 4, 6, 10, 12, 17, 20, 22, 24, 30, 40, 50, 60, 70, 80, 87, 90, 92, 94, 95, 96, 98, 99, 100]
    palette: dict[str, str] = {}
    for tone in tones:
        lightness = 0.0 if tone == 0 else 1.0 if tone == 100 else tone / 100.0
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        palette[str(tone)] = _rgb_to_hex(rgb)
    return palette


def generate_theme_scaffold(
    seed_color: str,
    platform: str = "compose",
    dark_mode: str = "paired",
    contrast: str = "standard",
    dynamic_color: str = "allowed",
) -> dict[str, Any]:
    platform = _validate_platform(platform)
    dark_mode = _normalize_key(dark_mode)
    contrast = _normalize_key(contrast)
    dynamic_color = _normalize_key(dynamic_color)
    if dark_mode not in {"paired", "light-only", "dark-only"}:
        raise ValueError("dark_mode must be paired, light-only, or dark-only.")
    if contrast not in {"standard", "high"}:
        raise ValueError("contrast must be standard or high.")
    if dynamic_color not in {"required", "allowed", "forbidden"}:
        raise ValueError("dynamic_color must be required, allowed, or forbidden.")

    r, g, b = _hex_to_rgb(seed_color)
    hue, _, saturation = colorsys.rgb_to_hls(r, g, b)
    primary = _build_palette(hue, max(saturation, 0.45))
    secondary = _build_palette(hue, max(min(saturation * 0.55, 0.55), 0.18))
    tertiary = _build_palette((hue + 0.08) % 1.0, max(min(saturation * 0.65, 0.6), 0.22))
    neutral = _build_palette(hue, 0.08)
    neutral_variant = _build_palette(hue, 0.18)
    error = _build_palette(0.01, 0.65)

    light_roles = {
        "primary": primary["40"],
        "onPrimary": primary["100"],
        "primaryContainer": primary["90"],
        "onPrimaryContainer": primary["10"],
        "secondary": secondary["40"],
        "onSecondary": secondary["100"],
        "secondaryContainer": secondary["90"],
        "onSecondaryContainer": secondary["10"],
        "tertiary": tertiary["40"],
        "onTertiary": tertiary["100"],
        "tertiaryContainer": tertiary["90"],
        "onTertiaryContainer": tertiary["10"],
        "error": error["40"],
        "onError": error["100"],
        "errorContainer": error["90"],
        "onErrorContainer": error["10"],
        "surface": neutral["99"],
        "onSurface": neutral["10"],
        "surfaceDim": neutral["87"],
        "surfaceBright": neutral["98"],
        "surfaceContainerLowest": neutral["100"],
        "surfaceContainerLow": neutral["96"],
        "surfaceContainer": neutral["94"],
        "surfaceContainerHigh": neutral["92"],
        "surfaceContainerHighest": neutral["90"],
        "outline": neutral_variant["50"],
        "outlineVariant": neutral_variant["80"],
        "surfaceTint": primary["40"],
        "inverseSurface": neutral["20"],
        "inverseOnSurface": neutral["95"],
        "inversePrimary": primary["80"]
    }
    dark_roles = {
        "primary": primary["80"],
        "onPrimary": primary["20"],
        "primaryContainer": primary["30"],
        "onPrimaryContainer": primary["90"],
        "secondary": secondary["80"],
        "onSecondary": secondary["20"],
        "secondaryContainer": secondary["30"],
        "onSecondaryContainer": secondary["90"],
        "tertiary": tertiary["80"],
        "onTertiary": tertiary["20"],
        "tertiaryContainer": tertiary["30"],
        "onTertiaryContainer": tertiary["90"],
        "error": error["80"],
        "onError": error["20"],
        "errorContainer": error["30"],
        "onErrorContainer": error["90"],
        "surface": neutral["10"],
        "onSurface": neutral["90"],
        "surfaceDim": neutral["6"],
        "surfaceBright": neutral["24"],
        "surfaceContainerLowest": neutral["4"],
        "surfaceContainerLow": neutral["10"],
        "surfaceContainer": neutral["12"],
        "surfaceContainerHigh": neutral["17"],
        "surfaceContainerHighest": neutral["22"],
        "outline": neutral_variant["60"],
        "outlineVariant": neutral_variant["30"],
        "surfaceTint": primary["80"],
        "inverseSurface": neutral["90"],
        "inverseOnSurface": neutral["20"],
        "inversePrimary": primary["40"]
    }

    return {
        "seed_color": seed_color.upper(),
        "platform": platform,
        "dynamic_color": dynamic_color,
        "dark_mode": dark_mode,
        "contrast": contrast,
        "palettes": {
            "primary": primary,
            "secondary": secondary,
            "tertiary": tertiary,
            "neutral": neutral,
            "neutralVariant": neutral_variant,
            "error": error
        },
        "roles": {
            "light": light_roles,
            "dark": dark_roles if dark_mode != "light-only" else {}
        },
        "typography": {
            "headline": "headline-small",
            "title": "title-large",
            "body": "body-medium",
            "label": "label-large"
        },
        "shape": {
            "small": "corner-small",
            "medium": "corner-medium",
            "large": "corner-large",
            "full": "corner-full"
        },
        "elevation": {
            "surface": "level0",
            "raised": "level1",
            "dialog": "level3"
        },
        "notes": [
            "This scaffold is deterministic and token-oriented.",
            "Use the skill layer for product-specific emphasis, dynamic-color policy, and final aesthetic judgment."
        ]
    }


def score_md3_audit(findings: list[dict[str, Any]]) -> dict[str, Any]:
    weights = _load_json("audit-weights.json")
    penalties = weights["severity_penalties"]
    severity_order = weights["severity_order"]
    category_weights = weights["category_weights"]
    category_scores = {category: 100.0 for category in category_weights}
    severity_counts = {severity: 0 for severity in penalties}

    for finding in findings:
        severity = finding.get("severity", "Note")
        category = finding.get("category", "theming_consistency")
        if severity not in penalties:
            raise ValueError(f"Unknown severity '{severity}'.")
        if category not in category_scores:
            raise ValueError(f"Unknown audit category '{category}'.")
        severity_counts[severity] += 1
        category_scores[category] = max(0.0, category_scores[category] - penalties[severity])

    weighted_total = sum(category_scores[category] * weight for category, weight in category_weights.items())
    weighted_max = sum(100.0 * weight for weight in category_weights.values())
    overall_score = round((weighted_total / weighted_max) * 100.0, 1)

    if overall_score >= 95:
        grade = "A"
    elif overall_score >= 85:
        grade = "B"
    elif overall_score >= 70:
        grade = "C"
    elif overall_score >= 50:
        grade = "D"
    else:
        grade = "F"

    sorted_findings = sorted(
        findings,
        key=lambda finding: (
            severity_order[finding.get("severity", "Note")],
            float(finding.get("confidence", 0.0)),
        ),
        reverse=True,
    )
    quick_wins = [
        {
            "id": finding["id"],
            "title": finding["title"],
            "recommended_fix": finding["recommended_fix"],
        }
        for finding in sorted_findings
        if finding.get("severity") in {"Medium", "Low"} and float(finding.get("confidence", 0.0)) >= 0.7
    ][:5]
    remediation_sequence = [
        {
            "id": finding["id"],
            "severity": finding["severity"],
            "title": finding["title"],
            "recommended_fix": finding["recommended_fix"],
        }
        for finding in sorted_findings
    ]
    unresolved_risks = [
        {
            "id": finding["id"],
            "title": finding["title"],
            "impact": finding["impact"],
        }
        for finding in sorted_findings
        if finding.get("severity") in {"Critical", "High"}
    ]

    return {
        "overall_score": overall_score,
        "grade": grade,
        "category_scores": {category: round(score, 1) for category, score in category_scores.items()},
        "severity_counts": severity_counts,
        "quick_wins": quick_wins,
        "remediation_sequence": remediation_sequence,
        "unresolved_risks": unresolved_risks,
    }


def _extract_version(path: Path) -> str | None:
    if not path.exists():
        return None
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("version")
    if path.name == "CHANGELOG.md":
        match = re.search(r"^## \[(?P<version>[^\]]+)\] - \d{4}-\d{2}-\d{2}$", path.read_text(encoding="utf-8"), re.MULTILINE)
        return match.group("version") if match else None
    return None


def _hash_directory(path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    if not path.exists():
        return hashes
    for file_path in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        relative = file_path.relative_to(path).as_posix()
        hashes[relative] = hashlib.sha256(file_path.read_bytes()).hexdigest()
    return hashes


def check_md3_release_consistency(
    repo_root: str | None = None,
    expected_version: str | None = None,
    target_tag: str | None = None,
    release_commit_message: str | None = None,
    release_notes_path: str | None = None,
) -> dict[str, Any]:
    root = Path(repo_root).resolve() if repo_root else ROOT
    config = json.loads((root / "mcp" / "data" / "release-surface.json").read_text(encoding="utf-8"))
    current_version = _extract_version(root / config["canonical_version_file"])
    mcp_version = _extract_version(root / "mcp" / "manifest.json")
    changelog_version = _extract_version(root / "CHANGELOG.md")
    release_commit_message = release_commit_message or (f"release: v{expected_version or current_version}" if current_version else None)
    target_tag = target_tag or (f"v{expected_version or current_version}" if current_version else None)

    checks: list[dict[str, Any]] = []

    def add_check(check_id: str, status: str, reason: str) -> None:
        checks.append({"id": check_id, "status": status, "reason": reason})

    if current_version:
        add_check("current_version_detected", "PASS", f"Detected plugin version {current_version}.")
    else:
        add_check("current_version_detected", "FAIL", "Could not detect current plugin version.")

    if expected_version:
        if expected_version == current_version == mcp_version:
            add_check("expected_version_alignment", "PASS", f"Expected version {expected_version} matches plugin and MCP metadata.")
        else:
            add_check("expected_version_alignment", "FAIL", f"Expected version {expected_version} does not match plugin ({current_version}) and MCP ({mcp_version}) metadata.")
    else:
        add_check("expected_version_alignment", "PASS", "No explicit expected version was requested.")

    if current_version and current_version == mcp_version == changelog_version:
        add_check("version_surface_alignment", "PASS", "Plugin manifest, MCP manifest, and CHANGELOG are aligned.")
    else:
        add_check("version_surface_alignment", "FAIL", f"Version drift detected: plugin={current_version}, mcp={mcp_version}, changelog={changelog_version}.")

    missing_docs = [doc for doc in config["required_docs"] if not (root / doc).exists()]
    if missing_docs:
        add_check("required_release_docs", "FAIL", f"Missing release docs: {missing_docs}.")
    else:
        add_check("required_release_docs", "PASS", "All required release docs are present.")

    if (root / config["plugin_mcp_config"]).exists():
        add_check("plugin_mcp_present", "PASS", "Bundled plugin MCP config exists.")
    else:
        add_check("plugin_mcp_present", "FAIL", "Bundled plugin MCP config is missing.")

    if (root / config["marketplace_file"]).exists():
        add_check("marketplace_present", "PASS", "Marketplace metadata exists.")
    else:
        add_check("marketplace_present", "FAIL", "Marketplace metadata is missing.")

    source_hashes = _hash_directory(root / config["canonical_skill"])
    bundle_hashes = _hash_directory(root / config["bundled_skill"])
    if source_hashes and source_hashes == bundle_hashes:
        add_check("bundle_sync", "PASS", "Bundled skill matches the canonical skill.")
    else:
        add_check("bundle_sync", "FAIL", "Bundled skill does not match the canonical skill.")

    commit_pattern = re.compile(config["release_commit_pattern"])
    if release_commit_message and commit_pattern.match(release_commit_message):
        add_check("release_commit_policy", "PASS", f"Release commit message '{release_commit_message}' matches policy.")
    else:
        add_check("release_commit_policy", "FAIL", f"Release commit message '{release_commit_message}' does not match policy.")

    tag_pattern = re.compile(config["tag_pattern"])
    if target_tag and tag_pattern.match(target_tag):
        add_check("tag_policy", "PASS", f"Tag '{target_tag}' matches policy.")
    else:
        add_check("tag_policy", "FAIL", f"Tag '{target_tag}' does not match policy.")

    release_notes_status = "PASS"
    release_notes_reason = "No release notes path supplied."
    if release_notes_path:
        release_notes_file = (root / release_notes_path).resolve()
        if release_notes_file.exists():
            release_notes_text = release_notes_file.read_text(encoding="utf-8")
            version_for_notes = expected_version or current_version
            if version_for_notes and version_for_notes in release_notes_text:
                release_notes_reason = f"Release notes draft references version {version_for_notes}."
            else:
                release_notes_status = "FAIL"
                release_notes_reason = "Release notes draft does not mention the expected version."
        else:
            release_notes_status = "FAIL"
            release_notes_reason = f"Release notes file '{release_notes_path}' does not exist."
    add_check("release_notes", release_notes_status, release_notes_reason)

    overall_status = "PASS" if all(check["status"] == "PASS" for check in checks) else "FAIL"
    return {
        "status": overall_status,
        "current_version": current_version,
        "expected_version": expected_version,
        "target_tag": target_tag,
        "checks": checks,
        "drift_detected": any(check["id"] == "version_surface_alignment" and check["status"] == "FAIL" for check in checks),
    }
