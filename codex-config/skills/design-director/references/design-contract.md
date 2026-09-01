# Design Contract

Use this structure to hand a selected direction to implementation. Keep it concise enough to remain the single source of truth for the pass.

## Outcome and Scope

- Primary user outcome
- Target platform, device classes, and input modes
- In scope and explicitly out of scope
- Selected visual/interaction direction and source references

## Experience Model

- Entry points and primary flow
- Screen or surface inventory
- Navigation and dismissal behavior
- Information hierarchy and progressive disclosure

## State Model

For each important surface, specify applicable normal, loading, empty, error, disabled, success, focus, hover, pressed, interrupted, offline, and permission-denied states. State what persists across transitions and what recovers after interruption.

## Component and Layout Rules

- Existing components or tokens to reuse
- New components that are actually required
- Responsive transformations, not merely breakpoints
- Content bounds, truncation, localization, safe-area, and density behavior
- Layering, modal, overlay, and playfield-protection rules

## Interaction and Motion

- Primary and alternate inputs
- Feedback timing and error prevention/recovery
- Focus order and keyboard/controller traversal
- Motion purpose, duration class, interruption behavior, and reduced-motion substitute

## Accessibility

- Semantic structure and accessible names
- Contrast and non-color cues
- Text scaling or zoom behavior
- Target sizes and input alternatives
- Announcements for asynchronous state changes

## Acceptance Criteria

Write observable statements tied to user outcomes and required states. Avoid implementation prescriptions unless they are constraints. Mark unresolved blockers separately from non-blocking recommendations.
