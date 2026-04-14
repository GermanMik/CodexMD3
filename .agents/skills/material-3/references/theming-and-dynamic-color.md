# Theming and Dynamic Color

## Theme inputs

Start from explicit inputs:

- seed color or branded source palette
- product dynamic-color policy
- light/dark requirement
- contrast sensitivity or accessibility needs
- platform target

## Theme outputs

A complete MD3 theme response should cover:

- color roles
- tonal surface strategy
- typography scale
- shape tokens
- elevation model
- state-layer expectations
- dark theme behavior
- platform notes

## Seed color workflow

1. Accept one seed color unless brand rules require more.
2. Derive role-level palettes for primary, secondary, tertiary, neutral, neutral-variant, and error.
3. Map roles to component usage before tuning isolated surfaces.
4. Verify contrast-sensitive pairs and surface steps.

## Dynamic color policy

- `required`: use system-derived colors where platform support exists and provide token fallbacks.
- `allowed`: support dynamic color behind a product flag or user preference.
- `forbidden`: keep a static seeded theme and explain why.

## Dark theme guidance

- Keep tonal hierarchy intact; do not flatten all surfaces.
- Verify top app bar, sheets, dialogs, cards, and snackbars against surrounding surfaces.
- Preserve clear active/selected emphasis without over-reliance on pure white.

## Theme adaptation boundaries

- Compose: strongest support for MD3 dynamic color and tonal surfaces.
- Flutter: map theme roles carefully and confirm component parity.
- Web: expose role tokens and document missing runtime dynamic-color parity when applicable.

## Reasoning boundary

The deterministic MCP scaffold may propose role tokens from a seed color, but the skill must still decide:

- whether dynamic color is appropriate
- whether a branded override is justified
- which roles need emphasis or de-emphasis for a particular product flow
