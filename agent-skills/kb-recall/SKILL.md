---
name: kb-recall
description: Search the personal technical knowledge base for prior fixes, incidents, rules, and candidates. Use when a problem may have happened before, during troubleshooting, or when the user asks what the KB knows.
---

# Recall knowledge

Use the local Markdown KB as a retrieval source, not as unquestioned truth.

1. Run `sh ~/knowledge-base/scripts/pyrun.sh ~/knowledge-base/scripts/kb_search.py "<problem or query>" --json`.
2. Read only the most relevant 3-5 returned files. Do not load the whole KB.
3. Treat `rules/` as confirmed local guidance, `incidents/` as concrete evidence, and `candidates/` as unconfirmed observations.
4. For time-sensitive product, API, pricing, or tool behavior, verify against current primary documentation before relying on an old entry.
5. In the answer, name the KB files actually used and identify candidate-level uncertainty.

Do not modify the KB during recall. If a retrieved item materially helped and the user asks to record that fact, use `kb_log_reference.py`.
