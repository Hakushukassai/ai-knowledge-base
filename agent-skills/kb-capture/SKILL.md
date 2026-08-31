---
name: kb-capture
description: Save a reusable technical discovery to the personal knowledge base. Use only when the user explicitly asks to remember, record, or add a finding to the KB.
---

# Capture knowledge

Capture one reusable technical finding without ending the current session. Do not use this for ordinary project status, personal notes, speculative ideas, or secrets.

1. Summarize the finding as a specific, falsifiable title and run:
   `sh ~/knowledge-base/scripts/pyrun.sh ~/knowledge-base/scripts/kb_capture.py check "<title>"`
2. Read plausible matches.
   - If the same finding exists, use `kb_capture.py observe <candidate-path> --project <project> --note <new evidence>`.
   - Otherwise, use `kb_capture.py new` with a short ASCII `--slug`, title, project, tags, summary, resolution, details, and unknowns. Add `--confirm-new` only after the duplicate check.
3. For a current external fact, verify it using a primary source and pass its URL with `--source`. Otherwise leave it explicitly unverified.
4. Run `sh ~/knowledge-base/scripts/pyrun.sh ~/knowledge-base/scripts/validate_kb.py` and fix structural problems in the new or updated entry.
5. Report the path written. Do not commit or push; syncing is a separate explicit action.

Never add credentials, customer identities, private contracts, unpublished project details, or copied proprietary material.
