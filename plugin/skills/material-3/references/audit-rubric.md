# MD3 Audit Rubric

## Audit categories

- `color_tokens`
- `typography`
- `shape`
- `elevation_and_tonal_surfaces`
- `component_correctness`
- `layout_and_responsiveness`
- `navigation_patterns`
- `motion_and_interaction_guidance`
- `accessibility`
- `theming_consistency`

## Scorecard contract

Return:

- overall score from 0 to 100
- grade
- category scores
- severity counts
- quick wins
- remediation sequence
- unresolved risks

## Finding contract

Each finding must include:

- `id`
- `title`
- `severity`
- `evidence`
- `impact`
- `recommended_fix`
- `confidence`
- `affected_files_or_surfaces`

## Severity meanings

- `Critical`: blocks safe release or breaks core MD3/a11y behavior
- `High`: major MD3 deviation or systemic inconsistency
- `Medium`: noticeable deviation with bounded scope
- `Low`: minor deviation or polish issue
- `Note`: informational or future-looking observation

## Quick wins

A quick win should be:

- low-risk
- localized
- likely to improve multiple audit categories
- feasible without changing product intent

## Remediation sequence

Order fixes by:

1. correctness and accessibility blockers
2. systemic token or theme problems
3. navigation and layout mismatches
4. component-level misuse
5. lower-risk polish gaps

## Non-goals

- Do not downgrade MD3 issues into generic styling opinions.
- Do not prescribe full redesigns when a token, component, state, or layout correction is enough.
