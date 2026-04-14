# Navigation Patterns

## Primary navigation adaptation

Choose navigation by width class and destination complexity:

- compact width: navigation bar
- medium width: navigation rail by default
- expanded width: navigation drawer or rail-plus-pane layout

## Destination count

- 3-5 top-level destinations fit best in navigation bar or rail.
- Larger or grouped information architectures justify a drawer.
- Tabs do not replace global app navigation.

## App bar guidance

- Use top app bars to anchor title, context, and actions.
- Promote to medium or large top app bars when the screen benefits from stronger hierarchy or scroll transition.
- Use bottom app bars only when bottom actions matter more than persistent destination switching.

## Adaptive shells

- Compact shell: top app bar + content + navigation bar or FAB.
- Medium shell: top app bar + content + navigation rail.
- Expanded shell: top app bar + permanent drawer or rail + supporting pane when justified.

## Edge-to-edge

- Let top app bars, navigation bars, rails, and sheets coordinate with insets.
- Do not hide critical actions behind unsafe inset assumptions.

## Foldables and large screens

- Use split-pane or supporting-pane patterns only when content meaningfully benefits from simultaneous context.
- Avoid stretching compact layouts across expanded widths without rethinking navigation and pane structure.
