---
name: design-director
description: Convert an already selected UI direction into an implementation-ready design contract covering flows, states, hierarchy, interaction, responsive behavior, and acceptance criteria. Use after exploration has produced a direction and before implementation; do not use for open-ended ideation, broad UX audits, pixel matching, or post-build QA.
---

# Design Director

Produce a compact design contract that removes consequential ambiguity before code or production design begins. Preserve the user's chosen direction; do not reopen visual exploration unless the direction is internally inconsistent or cannot satisfy the stated outcome.

## Boundary and Routing

- If no visual or interaction direction has been selected and alternatives are needed, use Product Design `get-context` and `ideate` first.
- If the task is primarily a critique or research request, use Product Design `audit` or `research`.
- If the target is a browser game, let Game Studio's `game-ui-frontend` own HUD/playfield constraints; this skill owns the implementation contract that follows.
- If the target is a native Apple platform, apply `$apple-platform-design` as the platform-conformance layer.
- After implementation, use `$ui-quality-gate`; do not claim this contract proves the built result.

## Workflow

1. Confirm from available context that the user outcome, target platform, and selected direction are sufficiently clear. Make reversible assumptions explicit; ask only when a missing choice would materially change the product.
2. Inspect existing code, tokens, components, screenshots, and platform constraints that the implementation must preserve.
3. Resolve the smallest set of decisions needed to build without improvising the product during implementation.
4. Write the design contract using [references/design-contract.md](references/design-contract.md). Omit sections that genuinely do not apply.
5. Record meaningful tradeoffs and rejected alternatives only when they explain a non-obvious decision.
6. End with observable acceptance criteria and identify any unresolved decision that still blocks implementation.

## Decision Standard

- Optimize the primary user outcome before novelty, decoration, or information density.
- Specify normal, loading, empty, error, disabled, success, focus, hover, pressed, and interrupted states when the surface can enter them.
- Describe hierarchy and behavior before exact pixels. Use exact values only when a source design, token system, platform rule, or implementation constraint justifies them.
- Reuse established components and tokens unless the chosen direction requires a deliberate exception.
- Include keyboard, touch, controller, screen-reader, reduced-motion, localization, and responsive implications that apply to the target.
- Separate requirements from recommendations so implementation knows what may vary.

Read [references/decision-heuristics.md](references/decision-heuristics.md) only when resolving competing layout, disclosure, navigation, or feedback options.
