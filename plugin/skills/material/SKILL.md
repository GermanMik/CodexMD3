---
name: material
description: Design, scaffold, theme, adapt, and audit Material Design 3 / Material You user interfaces with a Compose-first workflow, Flutter-secondary implementation guidance, and limited Web token guidance. Use when Codex needs to choose or generate MD3 components, build or adapt MD3 themes, produce MD3 layout or navigation shells, scaffold MD3 screens, or run an MD3-specific compliance audit with concrete remediation.
---

# Material Design 3

Use this skill only for Material Design 3 or Material You work. Stay MD3-specific. Do not replace MD3 guidance with generic frontend advice.

## Default posture

- Prefer Jetpack Compose Material 3 APIs and patterns as the primary path.
- Support Flutter Material 3 as a secondary implementation path.
- Keep Web support limited to tokens, CSS architecture, and component guidance unless the user explicitly asks for a constrained web implementation.
- Do not imply full Web parity with Compose unless the repo-local implementation proves it.
- Treat MD3 as personal, adaptive, and expressive: start from task intent, state, context, and device class before choosing components.

## Mode selection

Choose one primary mode before producing output:

- `component`: Choose, adapt, or validate one or more MD3 components.
- `theme`: Generate or adjust MD3 theme tokens, tonal roles, dynamic color guidance, typography, shape, elevation, or contrast strategy.
- `layout`: Choose responsive layout rules, breakpoints, window size behavior, edge-to-edge handling, or adaptive navigation.
- `scaffold`: Assemble an app shell, screen skeleton, or navigation shell that follows MD3 structure.
- `audit`: Score an existing screen or code path for MD3 compliance and propose the smallest safe fixes.

If a request spans multiple areas, set a primary mode and a secondary mode. Example: a dashboard shell with theme polish is `scaffold` primary and `theme` secondary.

Use this decision path when the request is ambiguous:

- Existing screen, code path, or screenshot that needs scoring or gap analysis -> `audit`
- New app shell, screen skeleton, or navigation shell -> `scaffold`
- Window-size adaptation, navigation switching, insets, or responsive shell behavior -> `layout`
- Seed color, tokens, dynamic color, typography, shape, or elevation strategy -> `theme`
- Specific control, state model, or component choice -> `component`

## Reference loading map

Load only the references needed for the active mode:

- `references/color-system.md`: color roles, tonal surfaces, state layers, contrast.
- `references/component-catalog.md`: canonical component selection and state requirements.
- `references/theming-and-dynamic-color.md`: seed color, dynamic color, dark theme guidance.
- `references/typography-and-shape.md`: type scale, shape tokens, elevation interplay.
- `references/navigation-patterns.md`: navigation bar, rail, drawer, app bar adaptation.
- `references/layout-and-responsive.md`: window size classes, insets, foldables, adaptive shells.
- `references/audit-rubric.md`: MD3 compliance categories, scoring, finding contract.
- `references/platform-matrix.md`: Compose-first, Flutter-secondary, Web-limited boundaries.
- `references/remediation-policy.md`: smallest safe MD3-correct fix policy.
- `references/release-readiness.md`: release and packaging checks for the capability itself.

## Required output shape by mode

### Component mode

- Restate user intent, primary task, density, and emphasis level.
- Name the recommended MD3 component or composition.
- List required states, accessibility notes, and platform-specific deltas.
- Call out one minimal implementation path and one validation check.

### Theme mode

- State seed color input and whether dynamic color is allowed, required, or excluded.
- Produce role-level theme guidance: color roles, tonal surfaces, typography, shape, elevation, contrast, dark theme behavior.
- Separate deterministic token scaffolding from subjective visual tuning.
- Prefer token-level changes over per-screen overrides.

### Layout mode

- Identify target device classes and window size behavior.
- Choose navigation adaptation and edge-to-edge strategy.
- Specify inset handling, large-screen behavior, and any foldable-specific rule.
- Keep the layout shell MD3-compliant before tuning visual details.

### Scaffold mode

- Produce an MD3 app shell or screen skeleton.
- Include app bar, primary content region, supporting surfaces, primary action placement, and navigation shell.
- Respect window size adaptation and edge-to-edge handling.
- Favor the smallest shell that supports the task.

### Audit mode

Always return:

- `scorecard`
- `findings`
- `quick wins`
- `remediation sequence`
- `unresolved risks`

Every finding must include:

- `id`
- `title`
- `severity`
- `evidence`
- `impact`
- `recommended_fix`
- `confidence`
- `affected_files_or_surfaces`

Use only these severities:

- `Critical`
- `High`
- `Medium`
- `Low`
- `Note`

## Audit execution rules

- Audit against MD3 tokens, components, theming, layout, and navigation rules, not against personal taste.
- Prefer code or concrete UI evidence over assumptions.
- Call out missing evidence as `UNKNOWN` in reasoning, not as a hidden assumption.
- When proposing fixes, use the smallest safe change that restores MD3 correctness.
- Do not recommend a rewrite when a token, component swap, state fix, or layout adjustment is enough.

## MCP usage boundary

Use the optional MCP layer for deterministic lookups, theme scaffolds, scorecards, and release consistency checks. Keep these activities in the skill reasoning layer:

- choosing the best component composition for ambiguous product intent
- deciding between valid MD3 patterns
- prioritizing remediation sequence
- explaining tradeoffs to the user
- turning deterministic facts into context-aware design recommendations
- storing proof-loop raw JSON outputs and requiring a fresh verifier pass before marking the task complete
- treating `score_md3_audit` and `check_md3_release_consistency` as evidence inputs, not self-certifying verdicts

## Anti-drift rules

- Do not drift into generic design-system guidance.
- Do not invert platform priorities; Compose stays primary.
- Do not treat plugin-bundled skill files as the canonical authoring surface.
- Do not claim MD3 compliance without explicit evidence or an audit pass.
