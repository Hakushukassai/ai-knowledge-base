# Refero research handoff

Use this structure after research has produced a credible recommendation. Keep it short enough that the next design skill can act on it without rereading every source.

## Brief

```text
Product and platform:
Primary user goal:
Desired feeling:
Decision being researched:
Existing constraints:
```

## Candidate comparison

For a major open-ended direction, present up to three choices:

| Option | Reference | Best contribution | Adapt for this product | Main risk |
| --- | --- | --- | --- | --- |
| 1 | Name + URL | Concrete trait | Bounded adaptation | What could misfit |

Do not make the options cosmetic recolors. Each should represent a meaningfully different hierarchy, density, typography, composition, or interaction approach.

## Reference lock

After the user chooses—or when one direction is already clearly implied—record:

```text
Primary reference:
Source URL and access date:
Preserve: 3–5 signature traits that must survive
Borrow only: at most 2 details from named secondary references
Token roles: background, text, accent, action, border, radius, shadow
Layout and hierarchy commitments:
Interaction or journey commitments:
Media strategy: existing, licensed, generated, stock, or code-native
Reject: defaults, copied brand expression, and conflicting traits
Open question: only if it still blocks the next stage
```

## Routing the result

- Send an unresolved set of visual directions to Product Design exploration.
- Send a selected direction to `$design-director` before implementation when material flow, state, or responsive decisions remain.
- Apply `$apple-platform-design` only for native Apple targets; Refero evidence never overrides current platform rules or Apple resource licensing.
- After implementation, use the specialized visual comparison check when applicable, then `$ui-quality-gate` for release readiness.
