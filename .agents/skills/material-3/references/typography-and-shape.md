# Typography and Shape

## Typography

Use the MD3 type scale as a semantic hierarchy, not as a decorative menu. Favor consistent roles across screens.

## Expected roles

- `display-large`, `display-medium`, `display-small`
- `headline-large`, `headline-medium`, `headline-small`
- `title-large`, `title-medium`, `title-small`
- `body-large`, `body-medium`, `body-small`
- `label-large`, `label-medium`, `label-small`

## Guidance

- Reserve display and large headline roles for clear moments of emphasis.
- Use title roles for app bars, cards, section headers, and key summaries.
- Use body roles for primary reading copy and supporting descriptions.
- Use label roles for buttons, chips, tabs, and compact metadata.
- Do not create ad hoc text sizes when an MD3 role already fits.

## Shape tokens

Use shape tokens at the system level:

- `corner-extra-small`
- `corner-small`
- `corner-medium`
- `corner-large`
- `corner-extra-large`
- `corner-full`

## Shape guidance

- Match shape changes to meaning: more prominent or expressive surfaces may use larger corners.
- Keep component families consistent; do not mix unrelated radii in the same hierarchy.
- Use full shape for chips and highly rounded pills only when the pattern calls for it.

## Elevation interplay

- Elevation, surface tone, and shape work together.
- Do not compensate for missing tonal contrast by adding arbitrary shadows.
- When a surface reads ambiguously, first check surface role and shape, then elevation.
