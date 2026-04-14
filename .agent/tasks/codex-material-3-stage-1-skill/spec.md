# Task: codex-material-3-stage-1-skill

## Original task statement
Create the canonical editable Codex skill for Material Design 3 at `.agents/skills/material-3/`, preserving the functional baseline of the source material-3 skill while making it production-ready for Codex and the repo-task-proof-loop.

## Scope
- Create `.agents/skills/material-3/SKILL.md`.
- Create required MD3 reference documents and `agents/openai.yaml`.
- Encode component, theme, layout, scaffold, and audit modes.
- Document Compose-first, Flutter-secondary, and Web-limited strategy.
- Define MD3-specific audit rubric, remediation policy, and output contract.
- Add only optional scripts or usage notes that directly support MD3 workflows.

## Out of scope
- Generic frontend helper guidance divorced from MD3.
- Full design assets or visual mockups.
- Non-MD3 component systems or CSS frameworks beyond limited web token guidance.
- Plugin packaging, release metadata, or MCP implementation except where referenced as integration points.

## Acceptance criteria
- AC1.1: `SKILL.md` exists at `.agents/skills/material-3/SKILL.md` and is explicitly Material Design 3 specific rather than generic UI guidance.
- AC1.2: The skill defines `component`, `theme`, `layout`, `scaffold`, and `audit` modes with a decision path for selecting them.
- AC1.3: Reference docs cover tokens, components, theming, layout, audit, remediation, release readiness, and platform matrix under `.agents/skills/material-3/references/`.
- AC1.4: Support boundaries for Jetpack Compose (primary), Flutter (secondary), and Web (limited) are explicitly documented.
- AC1.5: The audit rubric is MD3-specific and produces structured findings with required fields and severity model.
- AC1.6: A remediation policy exists and prefers the smallest safe MD3-correct fixes over refactors.
- AC1.7: The skill defines an audit-mode output contract covering scorecard, findings, quick wins, remediation sequence, and unresolved risks.

## Constraints
- Keep the skill concise enough for progressive disclosure and move detailed guidance into references.
- Preserve MD3 specificity across philosophy, token guidance, component guidance, layouts, and audits.
- Do not rely on plugin bundle copies as the primary authoring surface.
- Avoid adding skill documentation that does not directly help another Codex instance perform MD3 work.

## Assumptions
- Reference documents can carry most domain detail while `SKILL.md` stays procedural.
- UI metadata in `agents/openai.yaml` can be authored manually if bootstrap scripts are not used.
- Optional helper scripts are only needed if they improve deterministic reuse.

## Risks
- `SKILL.md` becoming too large or duplicative can reduce usability.
- Web guidance may accidentally expand beyond the limited path.
- Audit outputs may become generic if the rubric is not tied to MD3 tokens/components/layout rules.

## Verification plan
- V1: Inspect skill files and confirm all required references and metadata exist in the canonical skill path.
- V2: Validate that the skill text explicitly names the five modes, platform boundaries, audit structure, and remediation policy.
- V3: Map each stage acceptance criterion to authoritative files and evidence snippets in a fresh verifier pass.

## Evidence expectations
- E1: Raw artifacts capture existence/content checks for the skill, reference corpus, and agent metadata.
- E2: Evidence maps each AC1.x item to canonical skill files instead of bundled plugin copies.
- E3: Verifier records failures or gaps in MD3 specificity, output contract structure, or platform boundaries.

## Minimal safe implementation boundary
Deliver only the canonical MD3 skill with the required references, metadata, and optional direct-support files. Do not add nonessential assets, release-only surfaces, or framework-general design docs here.
