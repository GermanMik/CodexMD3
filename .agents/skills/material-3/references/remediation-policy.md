# Remediation Policy

## Default strategy

Fix the smallest safe MD3 violation first. Use local, token-level, or component-level changes before considering layout rewrites.

## Smallest safe fix hierarchy

1. correct token mapping or role usage
2. swap to the correct MD3 component or variant
3. fix missing component states or accessibility semantics
4. adjust layout, navigation adaptation, or insets
5. restructure the shell only when earlier fixes cannot restore MD3 correctness

## Required remediation output

For each proposed fix, state:

- the finding ID being fixed
- the minimal code or design surface to change
- why the fix restores MD3 correctness
- any follow-up verification needed

## Forbidden shortcuts

- full-screen redesigns to solve token mistakes
- ad hoc one-off colors when role tokens exist
- replacing MD3 components with custom widgets without proof
- marking findings as resolved without fresh verification

## Escalation triggers

Escalate instead of patching when:

- product constraints directly conflict with MD3 guidance
- required evidence is missing
- the only fix path is a major information architecture change
- repeated small fixes fail the same acceptance criterion
