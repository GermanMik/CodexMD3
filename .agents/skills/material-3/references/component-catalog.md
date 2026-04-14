# MD3 Component Catalog

## Selection posture

Choose MD3 components by task intent, prominence, density, and adaptation needs. Do not substitute older Material 2 patterns when MD3 components already fit.

## Core catalog

| Component | Use when | Required checks | Platform notes |
| --- | --- | --- | --- |
| Buttons | primary, secondary, tertiary, or text actions | enabled, disabled, icon/no-icon, loading if relevant | Compose path is authoritative; Flutter naming may differ |
| Icon buttons | compact icon action or toggle action | selected/unselected, filled/tonal/outlined variants, touch target | Avoid unlabeled critical actions |
| Text fields | structured user input | label, placeholder, error, helper, prefix/suffix, focus | Prefer MD3 field styling over custom underline forms |
| Cards | grouped related content | elevated/filled/outlined choice, focus order, click target | Use tonal surfaces before custom backgrounds |
| Chips | filtering, suggestion, assist, input selections | selected, removable, icon support, wrap behavior | Avoid overloading chips as navigation when tabs or nav components fit |
| Tabs | peer view switching in one context | scroll/fixed choice, indicator, content coupling | Use with top-level view groups, not global navigation |
| Top app bar | screen title, actions, scroll behavior | small/medium/large/center-aligned, edge-to-edge offsets | Compose offers strongest MD3 parity |
| Bottom app bar | bottom-bound actions and FAB pairing | FAB cutout, overflow, inset spacing | Use sparingly when navigation bar is not the better fit |
| Navigation bar | primary compact-width navigation | 3-5 destinations, labels, selected state | Default compact pattern |
| Navigation rail | medium-width navigation | destination count, label policy, FAB adjacency | Default medium pattern |
| Navigation drawer | expanded-width or high-destination navigation | modal vs permanent, hierarchy, grouping | Prefer permanent drawer on large widths when justified |
| FAB | highest-priority creation or forward action | size, expanded/standard, visibility rules | One primary FAB per screen region |
| Dialog | blocking confirmation or short task | focus trap, title, action order, dismiss semantics | Escalate to full screen only when task outgrows dialog |
| Bottom sheet | supplemental or task-focused surface | modal vs standard, snap points, back behavior | Avoid using as generic menu replacement |
| Snackbar | brief transient feedback | action, duration, stacking, a11y announcement | Use inverse roles carefully |
| Lists | dense content collections | row height, supporting text, leading/trailing content | Prefer standard list patterns before bespoke cards |
| Menus | anchored action lists | selected state, grouping, dismissal, overflow | Keep actions concise and mutually scannable |
| Progress indicators | wait/progress state | linear/circular, determinate/indeterminate, reduced motion | Tie copy to task state |
| Date and time pickers | date or time selection | locale, validation, keyboard fallback, timezone cues | Use only when date/time is central, not casual metadata |
| Data display patterns | dense metrics, tables, key-value summaries | hierarchy, scan path, tokenized emphasis | Keep typography and spacing tokenized |

## Minimum component decision rules

- Use buttons for actions, not navigation destinations.
- Use chips for lightweight selection or suggestion, not persistent app routing.
- Use tabs for sibling content panes inside one location.
- Use navigation bar, rail, or drawer based on width class and destination count.
- Use cards to group content, not to emulate every list row.

## Required state coverage

All selected components must verify:

- default
- focused
- pressed or active
- disabled when relevant
- error or invalid when relevant
- selected or toggled when relevant

## Compose-first rule

When guidance conflicts across frameworks, prefer the Compose Material 3 interpretation unless product constraints force a different implementation.
