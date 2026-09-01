---
name: apple-platform-design
description: Design or review native UI for iOS, iPadOS, macOS, watchOS, tvOS, or visionOS using the current Apple Human Interface Guidelines and locally licensed Apple Design Resources. Use for Apple-platform interaction, component, layout, input, accessibility, or mockup decisions; do not use Apple templates or assets for Apple-inspired web, browser-game, Android, or other non-Apple interfaces.
---

# Apple Platform Design

Apply Apple platform conventions as a specialized layer over the product's selected direction. Aim for platform-native behavior and coherent product character, not superficial imitation of Apple styling.

## Scope and Precedence

1. Preserve the user's outcome, explicit requirements, and existing product identity.
2. Follow supported platform capabilities and the current Apple HIG. Surface conflicts instead of silently overriding requirements.
3. Reuse the project's native components, tokens, and established patterns when they remain conformant.
4. Use Apple Design Resources only under their license and only for Apple-platform UI mockups.

For an Apple-platform game, Game Studio owns playfield, HUD density, and game interaction; this skill overlays system navigation, accessibility, safe areas, device inputs, permissions, and native settings or purchase surfaces.

## Required Workflow

1. Identify the exact platform and supported versions, device classes, windowing model, input modes, orientation, and whether the artifact is production UI, code, or a mockup.
2. Browse the current official HIG before making material platform decisions. Use [references/hig-source-map.md](references/hig-source-map.md) to select relevant sections and record the access date. Prefer Apple primary sources for APIs, platform behavior, and design resources.
3. Read [references/platform-routing.md](references/platform-routing.md) for the selected platform only.
4. Before using Apple-provided visual files, read [references/resource-policy.md](references/resource-policy.md). Consult [references/official-resource-catalog.md](references/official-resource-catalog.md) for verified official Figma, Sketch, and download entry points, then run `scripts/check_apple_resources.py` against any user-controlled resource directory. Never infer permission from file availability.
5. Choose native patterns and semantic components before custom replicas. In production code, prefer platform APIs and SF Symbols through their supported mechanisms rather than exporting template artwork into the product.
6. Specify or inspect applicable accessibility, text scaling, localization, safe-area/window resizing, dark appearance, contrast, motion, privacy/permission, and alternate-input behavior.
7. Deliver decisions with platform/version assumptions, HIG sections consulted, resource provenance, deliberate exceptions, and observable acceptance criteria.

## Resource Discovery

Run one of:

```bash
python3 scripts/check_apple_resources.py --root /absolute/path/to/AppleDesignResources
python3 scripts/check_apple_resources.py
```

The second form reads `APPLE_DESIGN_RESOURCES_DIR`. The script inventories files only; it never downloads, copies, extracts, modifies, or redistributes them. If no licensed local resource directory is configured, continue with live HIG guidance and native components, then clearly state that official template-level visual verification was unavailable.

## Non-Apple Boundary

For web or non-Apple products, abstract principles such as clarity, feedback, accessibility, and restraint may inform reasoning, but do not copy Apple component geometry, templates, icons, materials, or branded visual treatment. Route the actual design to Product Design, Game Studio, or the relevant implementation skill.
