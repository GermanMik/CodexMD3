# Layout and Responsive Guidance

## Window size classes

Use MD3-adjacent adaptive behavior:

- `compact`: single-column focus, bottom navigation, condensed chrome
- `medium`: rail-capable shell, more generous margins, optional supporting pane
- `expanded`: drawer or multi-pane shell, explicit content hierarchy, large-screen optimization

## Layout rules

- Establish content hierarchy before adding decorative surfaces.
- Use consistent outer margins and content gutters per width class.
- Keep supporting surfaces subordinate to the primary task.
- Switch navigation patterns deliberately at width boundaries; do not duplicate multiple primary nav systems in one state.

## Edge-to-edge and insets

- Treat status bar, navigation bar, IME, and gesture insets as first-class layout inputs.
- Use padding or safe drawing rules instead of hard-coded magic numbers.
- Verify top app bars, bottom bars, sheets, dialogs, and FABs against inset collisions.

## Large screens and foldables

- Add panes only when they reduce context switching.
- Promote lists into list-detail or supporting-pane layouts on medium/expanded widths when the information density supports it.
- Keep posture-specific logic separate from width logic when foldable states matter.

## Scaffold patterns

- screen skeleton: app bar + primary content + contextual action
- list-detail shell: navigation + list pane + detail pane
- dashboard shell: app bar + summary blocks + action region + adaptive navigation

Keep shells sparse until task hierarchy is proven.
