# UI Quality Matrix

Select only applicable rows, but do not skip a category merely because the happy path works.

| Category | Required observations |
| --- | --- |
| Primary flow | Entry, completion, cancellation, back behavior, persistence, interruption, recovery |
| States | Loading, empty, error, disabled, success, offline, permission denied, destructive confirmation |
| Responsive layout | Narrow, representative, and wide widths; zoom/text growth; safe areas; orientation where applicable |
| Input | Pointer, touch, keyboard, controller, stylus, or spatial input as applicable; visible focus; no traps |
| Accessibility | Semantics, names, roles, reading/focus order, contrast, non-color cues, target size, announcements |
| Content | Long strings, localization expansion, truncation, wrapping, missing media, dates/numbers, error copy |
| Visual system | Tokens, hierarchy, alignment, spacing, typography, icon treatment, state consistency |
| Motion | Purpose, interruption, repeated animation, reduced-motion behavior, no content-obscuring transitions |
| Performance feedback | Initial response, progress, duplicate-action prevention, perceived completion, slow/failure behavior |
| Platform fit | Native conventions, system surfaces, navigation, permissions, input model, platform-specific accessibility |

## Finding Record

```text
ID / severity:
Surface and state:
Reproduction:
Expected:
Observed:
Evidence:
User impact:
Recommended correction:
Retest:
```

When an item cannot be exercised, label it `not observed` and explain the missing fixture, account, device, permission, or environment.
