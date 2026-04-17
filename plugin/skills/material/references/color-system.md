# MD3 Color System

## Role of color in Material You

Material Design 3 color is token-driven, contextual, and tonal. Favor semantic roles over hard-coded component colors.

## Required token categories

- `color roles`: `primary`, `on-primary`, `primary-container`, `on-primary-container`, `secondary`, `tertiary`, `error`, and their matching `on-*` roles
- `surface roles`: `surface`, `surface-dim`, `surface-bright`, `surface-container-lowest` through `surface-container-highest`
- `outline roles`: `outline`, `outline-variant`
- `state layers`: press, hover, focus, drag emphasis on top of role colors
- `inverse roles`: `inverse-surface`, `inverse-on-surface`, `inverse-primary`

## Guidance

- Use tonal surfaces instead of introducing ad hoc background shades.
- Use container roles when a component needs emphasis without switching the entire surface stack.
- Keep destructive intent on `error` roles unless a product rule explicitly requires another accent.
- Use `surface-tint` only as part of the MD3 elevation model, not as a manual decoration color.

## Contrast handling

- Preserve readable contrast for all `on-*` pairs.
- Prefer role changes before custom alpha overlays when contrast is poor.
- Increase emphasis by moving to a stronger role or container, not by mixing arbitrary colors.
- Treat low-contrast placeholder, helper, or supporting text as a bug when it undermines usability.

## Dynamic color

- On Android or Compose-first paths, dynamic color is allowed when the product permits system personalization.
- When dynamic color is enabled, preserve semantic role mapping and fallback tokens.
- Document whether dynamic color is `required`, `allowed`, or `forbidden`; do not leave it implicit.

## Dark theme

- Keep dark theme tokenized; do not invert the light theme manually.
- Maintain distinct surface steps so cards, sheets, and bars remain legible without heavy borders.
- Validate `inverse-*` roles and snackbar/sheet contrast separately in dark theme.

## Web-limited guidance

- Mirror MD3 roles as CSS custom properties.
- Keep the token architecture semantic: role tokens map to component aliases; component CSS should not own raw palette values.
- Do not claim full Material You dynamic color parity on web unless the implementation proves it.
