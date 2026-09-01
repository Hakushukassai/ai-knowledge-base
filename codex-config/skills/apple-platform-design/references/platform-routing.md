# Apple Platform Routing

Read only the target platform section, then verify current details in Apple's HIG and API documentation.

## iOS

Prioritize one-handed touch reach, Dynamic Type, safe areas, clear navigation hierarchy, interruption recovery, permission timing, and system presentation behavior. Test compact widths, rotation when supported, keyboard appearance, and larger accessibility text sizes.

## iPadOS

Design for resizable windows and multiple size classes rather than treating iPad as a large phone. Cover keyboard, pointer, touch, drag and drop, multitasking, sidebars or split navigation where appropriate, and state preservation across resizing.

## macOS

Treat windowing, menu commands, keyboard shortcuts, pointer precision, focus, selection, drag and drop, toolbars, sidebars, and document behavior as first-class. Avoid importing touch-first density or modal flows without a Mac-specific reason.

## watchOS

Keep interactions brief, glanceable, and resilient to interruption. Prioritize high-value information, Digital Crown/touch input, large targets, concise navigation, complications or live surfaces where applicable, and minimal text entry.

## tvOS

Design for distance viewing, focus-driven navigation, remote/controller input, overscan-safe composition where relevant, legible type, and obvious focus transitions. Every action must remain reachable without touch assumptions.

## visionOS

Design for windows, volumes, or immersive spaces deliberately. Support eye/hand targeting, comfortable scale and depth, stable placement, accessible alternatives, and clear transitions between immersion levels. Avoid dense targets, excessive depth, or motion that conflicts with comfort.

## Cross-Platform Products

Share product semantics and design tokens where useful, but specify navigation, density, presentation, and input behavior per platform. Do not force identical layouts when native behavior differs.
