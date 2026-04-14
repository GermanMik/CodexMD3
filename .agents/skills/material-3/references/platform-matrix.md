# Platform Matrix

## Support strategy

- Jetpack Compose Material 3: primary path
- Flutter Material 3: secondary path
- Web design systems and CSS tokens: limited path

## Capability matrix

| Capability | Compose | Flutter | Web |
| --- | --- | --- | --- |
| Component guidance | canonical | supported with adaptation notes | limited to guidance |
| Theme scaffolding | canonical | supported | token-oriented only |
| Dynamic color guidance | strongest support | supported with product validation | limited and implementation-dependent |
| Adaptive navigation | canonical | supported | guidance only |
| Edge-to-edge/insets | canonical | supported | guidance only |
| MD3 audit | canonical rubric | supported | limited to tokens/components/layout checks |

## Compose-first rule

When code examples or tradeoffs diverge, prefer Compose APIs, naming, and behavior as the source of truth.

## Flutter rule

Translate MD3 guidance into Flutter idioms without pretending complete parity where component APIs differ.

## Web-limited rule

Keep web support focused on:

- semantic token architecture
- component selection guidance
- CSS custom properties
- layout and navigation intent

Do not present the web path as equal in coverage to Compose unless the implementation proves it.
