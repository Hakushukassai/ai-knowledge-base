# Apple Resource Policy

This operational summary is not legal advice. Recheck the current official terms when the license, intended use, or distribution model matters.

## Separate Guidance from Assets

- HIG pages are authoritative references. Link to and consult them live; do not mirror the complete text, images, or site into this skill.
- Apple Design Resources are user-obtained files governed by their license. Keep them in a user-controlled local directory outside distributable skill or project assets unless the license expressly permits the intended placement.
- Official Figma and Sketch shares may remain remote and be used through their respective connected tools; do not repackage them into this skill.
- The local inventory script proves only that files are present. It does not prove the user's right to use them.

## Permitted Workflow Boundary

Use locally obtained Apple Design Resources to create mockups of interfaces designed for the Apple platforms covered by the resource license. Keep source files local and reference their provenance and version in the handoff.

Do not:

- redistribute, sublicense, or publish the resource packages;
- embed template assets into shipped software merely because they appear in a UI kit;
- use Apple resource files to make non-Apple OS mockups;
- extract or repackage template content as stock artwork or clip art;
- copy the Apple HIG site wholesale into a knowledge base.

For production UI, prefer native framework components, documented system APIs, and SF Symbols used according to their current terms. If a requested use falls outside the clear mockup boundary, stop and ask the user to resolve permission or provide an independently licensed asset.

Official terms:

- [Apple Design Resources License](https://developer.apple.com/support/downloads/terms/apple-design-resources/Apple-Design-Resources-License-20230621-English.pdf)
- [Apple Website Terms of Use](https://www.apple.com/legal/internet-services/terms/site.html)
- [Apple Design Resources](https://developer.apple.com/design/resources/)

## Local Configuration

Point the skill at one explicit directory using either:

```bash
python3 scripts/check_apple_resources.py --root /absolute/path/to/AppleDesignResources
```

or the task-specific environment variable:

```bash
APPLE_DESIGN_RESOURCES_DIR=/absolute/path/to/AppleDesignResources python3 scripts/check_apple_resources.py
```

Never scan a home directory or filesystem root as a substitute for an explicit resource directory.
