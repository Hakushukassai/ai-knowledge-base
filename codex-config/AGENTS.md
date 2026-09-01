# Design Capability Routing

This workspace uses a layered design workflow. Load only the skill that owns the current decision, plus a platform or domain overlay when applicable.

## Routing

- Use `$refero-research` before Product Design when an open-ended visual direction, unfamiliar screen pattern, competitor-informed decision, or multi-step journey would materially benefit from external product evidence. It supplies research and a reference lock only; skip it when the user already provided or selected a source, for small local changes, and after implementation begins.
- Use Product Design for UX research, broad audits, visual exploration, source-driven prototypes, and prototype sharing.
- Use `$design-director` after a direction is selected to produce an implementation-ready design contract. It does not ideate or audit.
- Use Figma when a Figma file, library, component system, or Figma-to-code/code-to-Figma workflow is the source or destination.
- Use Game Studio for browser-game architecture, HUD/menu design, asset pipelines, and playtesting. Its `game-ui-frontend` skill owns playfield protection and game-specific UI density.
- Use `$apple-platform-design` only for native iOS, iPadOS, macOS, watchOS, tvOS, or visionOS work. It overlays Apple conventions on the product or game workflow and may reference locally licensed Apple Design Resources.
- Use `$ui-quality-gate` after implementation for evidence-based release readiness. Product Design `design-qa` still owns pixel/source comparison; Game Studio `game-playtest` still owns game feel.
- Use ImageGen for original raster concepts and assets. Use Sites only for building or publishing a site/prototype when requested.

## Sequence

Typical new UI work follows:

```text
refero-research when external evidence helps -> Product Design exploration
-> selected direction -> design-director contract
-> Figma or implementation -> specialized QA -> ui-quality-gate
```

For games, insert Game Studio as the domain owner. For native Apple targets, apply Apple Platform Design as an overlay. An explicit user-selected skill wins; do not invoke every design skill merely because a task mentions UI.

Build Web Apps is intentionally not installed in this workspace because its broad frontend generation and testing triggers overlap with Product Design, Game Studio, Browser, and the local quality gate. Reconsider it only when a conventional application implementation task needs its React, shadcn, Stripe, or Supabase guidance.
