from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from domain import (
    check_md3_release_consistency,
    generate_theme_scaffold,
    get_layout_rule,
    get_platform_matrix,
    lookup_md3_component,
    lookup_md3_token,
    score_md3_audit,
)


mcp = FastMCP(
    name="material-3-mcp",
    instructions=(
        "Deterministic Material Design 3 lookup, scaffold, scoring, and release-consistency support. "
        "Use these tools for facts, repeatable scaffolds, and machine-readable checks. "
        "Keep design judgment and remediation prioritization in the calling skill."
    ),
)


@mcp.tool(name="lookup_md3_token", description="Return deterministic MD3 token guidance by category and token.", structured_output=True)
def tool_lookup_md3_token(
    category: str,
    token_name: str | None = None,
    platform: str = "compose",
    include_related: bool = True,
) -> dict:
    return lookup_md3_token(category=category, token_name=token_name, platform=platform, include_related=include_related)


@mcp.tool(name="lookup_md3_component", description="Return canonical MD3 component guidance with required states and platform notes.", structured_output=True)
def tool_lookup_md3_component(component_id: str, platform: str = "compose") -> dict:
    return lookup_md3_component(component_id=component_id, platform=platform)


@mcp.tool(name="get_platform_matrix", description="Return Compose, Flutter, and Web support boundaries for MD3 workflows.", structured_output=True)
def tool_get_platform_matrix(topic: str | None = None) -> dict:
    return get_platform_matrix(topic=topic)


@mcp.tool(name="get_layout_rule", description="Return deterministic MD3 layout and navigation adaptation rules.", structured_output=True)
def tool_get_layout_rule(rule_id: str, platform: str = "compose", window_class: str | None = None) -> dict:
    return get_layout_rule(rule_id=rule_id, platform=platform, window_class=window_class)


@mcp.tool(name="generate_theme_scaffold", description="Generate a deterministic MD3 token scaffold from seed inputs.", structured_output=True)
def tool_generate_theme_scaffold(
    seed_color: str,
    platform: str = "compose",
    dark_mode: str = "paired",
    contrast: str = "standard",
    dynamic_color: str = "allowed",
) -> dict:
    return generate_theme_scaffold(
        seed_color=seed_color,
        platform=platform,
        dark_mode=dark_mode,
        contrast=contrast,
        dynamic_color=dynamic_color,
    )


@mcp.tool(name="score_md3_audit", description="Score structured MD3 audit findings into a reproducible scorecard.", structured_output=True)
def tool_score_md3_audit(findings: list[dict]) -> dict:
    return score_md3_audit(findings=findings)


@mcp.tool(name="check_md3_release_consistency", description="Check version, changelog, bundle sync, and release metadata consistency.", structured_output=True)
def tool_check_md3_release_consistency(
    expected_version: str | None = None,
    target_tag: str | None = None,
    release_commit_message: str | None = None,
    release_notes_path: str | None = None,
) -> dict:
    return check_md3_release_consistency(
        expected_version=expected_version,
        target_tag=target_tag,
        release_commit_message=release_commit_message,
        release_notes_path=release_notes_path,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
