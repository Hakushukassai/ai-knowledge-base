---
name: refero-research
description: Research Refero styles, product screens, and user flows when an open-ended UI direction, redesign, product pattern, or multi-step journey needs external evidence before design exploration. Use as a research layer before Product Design; do not use for small visual fixes, exact source matching, implementation, design contracts, Apple-platform conformance, or post-build QA.
---

# Refero Research

Find relevant real-product references, extract bounded lessons, and hand a clear evidence package to the skill that owns the next design decision. This skill researches; it does not become the design authority.

## When to Use

Use automatically when the user asks for a new visual direction, a substantial redesign, unfamiliar product UI patterns, competitor-informed UX, or a multi-step flow and no sufficient source has already been selected.

Skip it when:

- the user already supplied or selected a visual target and the task is to match or implement it;
- the change is a small, local visual or copy adjustment;
- the task is already in design-contract, implementation, or release-QA stage;
- evidence from the existing product design system already resolves the decision.

An explicit Refero URL or `$refero-research` request always activates this skill. Preserve the user's stated direction and do not reopen a settled choice unless the reference exposes a concrete conflict.

## Scope and Handoff

- Refero Research owns external reference discovery and synthesis.
- Product Design owns visual exploration, UX research deliverables, audits, and source-driven prototypes.
- `$design-director` owns the implementation-ready contract after a direction is selected.
- `$apple-platform-design` owns native Apple conformance and licensed Apple resource use.
- `$ui-quality-gate` owns final release readiness after implementation.

For games, let Game Studio own game UI constraints and use Refero only for bounded product-pattern evidence.

## Research Route

1. Form a short brief from available context: product, platform, primary user goal, desired feeling, and the visual, screen, or journey decision that needs evidence. Ask only if a missing answer would materially change the search.
2. Use the best available source:
   - Prefer callable Refero MCP tools when they are already available and authorized.
   - Otherwise search public pages on `styles.refero.design` and open the actual style pages. Do not rely on search-result snippets alone.
   - When the user supplies a Refero URL, inspect that exact page first.
3. Match the research depth to the decision:
   - visual language: styles;
   - screen structure, components, states, or copy: screens;
   - onboarding, checkout, settings changes, or another sequence: flows.
4. For an open-ended direction, inspect enough distinct references to avoid copying a single product. Three strong candidates are normally sufficient; stop when additional results no longer change the decision.
5. Compare what each reference contributes. Choose one primary foundation and at most two narrow secondary details. Do not average conflicting styles into a generic middle.
6. Present concise options in the user's language. For a major direction with several credible choices, let the user choose by number. If one direction is already clearly implied, recommend it and state the assumption without forcing another decision round.
7. After selection, create the reference lock in [references/research-handoff.md](references/research-handoff.md) and pass it to Product Design or the relevant next owner.

## Refero Tool Mapping

When live Refero tools are callable, prefer:

- `refero_search_styles` and `refero_get_style` for tone, typography, color roles, spacing, radius, elevation, surfaces, and imagery treatment;
- `refero_search_screens`, `refero_get_screen`, and `refero_get_similar_screens` for concrete page and component patterns;
- `refero_search_flows` and `refero_get_flow` for multi-step journey logic;
- raw screen images only when visual inspection materially changes the conclusion.

If live tools require a paid plan or sign-in and are unavailable, continue with public Refero Styles where possible. Explain the limitation only when it reduces confidence or blocks the requested depth. Do not install connectors, start subscriptions, or sign in without the user's authorization.

## Evidence and Rights

- Name and link every reference used, and record the access date when producing a durable design contract.
- Extract principles, token roles, hierarchy, and interaction patterns. Do not copy another product's complete composition, copywriting, trade dress, or distinctive brand expression.
- Do not bundle the Refero catalogue, bulk-download screenshots, or store third-party logos, proprietary fonts, or product imagery in this skill.
- Treat custom fonts, logos, screenshots, and downloadable assets as separately licensed. Substitute appropriately unless the user has valid rights.
- Keep colors and component tokens in their source roles. A CTA accent stays an action color; decorative media does not become interface chrome.

## Quality Standard

The research is ready to hand off only when:

- each recommendation cites a real opened reference;
- the primary direction is distinguishable rather than a generic average;
- the proposed adaptation fits the user's product, platform, and audience;
- the reference lock states what to preserve, what may be borrowed, and what must be rejected;
- no downstream skill's role has been duplicated or overridden.
