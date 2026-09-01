---
name: ui-quality-gate
description: Inspect an implemented UI and issue an evidence-based release verdict against its stated design intent, required states, responsiveness, interaction behavior, and accessibility. Use for final handoff or release readiness; do not use for early ideation, general UX research, gameplay feel, or source-image pixel matching.
---

# UI Quality Gate

Act as the final cross-surface acceptance gate. Evaluate the observable implementation, not just source code or intended behavior.

## Boundary and Routing

- Use Product Design `audit` for broad user-facing critique of an existing flow.
- Use Product Design `design-qa` when a coded prototype must be compared specifically with a source image or frame.
- Use Game Studio `game-playtest` for game feel, controls, pacing, collision, or core-loop quality.
- Use this skill after those specialized checks when a release verdict across interaction, states, responsive behavior, accessibility, and visual-system consistency is needed.
- A review request is read-only. Apply fixes only when the user also asks to change the implementation; after changes, rerun affected checks.

## Workflow

1. Establish the acceptance source: a design contract, selected visual target, requirements, platform rules, or the user's stated intent. Report material ambiguity instead of silently inventing criteria.
2. Run or open the product and inspect it at representative viewports and input modes. Use rendered evidence whenever the environment allows it.
3. Exercise the applicable states and paths in [references/quality-matrix.md](references/quality-matrix.md). Mark each item `pass`, `fail`, `not observed`, or `not applicable`.
4. Record each finding with location, reproduction steps, expected behavior, observed behavior, evidence, impact, and severity.
5. Issue one verdict using the thresholds below. Do not call the UI ready when a required state was not observed.

## Severity and Verdict

- **P0 — Stop:** data loss, security/privacy exposure, inaccessible critical path, crash, or unusable primary flow.
- **P1 — Block:** primary task failure, severe responsive breakage, keyboard/controller trap, unreadable critical content, or misleading state.
- **P2 — Conditional:** meaningful quality defect with a practical workaround or limited scope.
- **P3 — Follow-up:** minor polish or consistency issue that does not impair the intended outcome.

Verdicts:

- **FAIL:** any open P0 or P1.
- **CONDITIONAL:** no P0/P1, but open P2 items or required scenarios remain `not observed`.
- **PASS:** no P0/P1/P2 and all required scenarios have observable evidence.

## Evidence Standard

- Prefer screenshots, recordings, browser state, console output, accessibility-tree evidence, or reproducible interaction steps over impressions.
- Distinguish implementation defects from optional taste changes.
- Group repeated symptoms under one root finding and list affected surfaces.
- State environmental limitations and reduce confidence accordingly; absence of evidence is not a pass.
- Keep the final report ordered by severity, followed by the verdict and the smallest retest set.
