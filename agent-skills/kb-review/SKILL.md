---
name: kb-review
description: Review the personal knowledge-base backlog for promotion, duplication, staleness, and missing verification. Use when the user asks to organize, curate, clean up, or assess the KB.
---

# Review the KB

Keep this workflow read-only until the user chooses specific changes.

1. Run `sh ~/knowledge-base/scripts/pyrun.sh ~/knowledge-base/scripts/kb_review.py --json`.
2. Inspect only the reported promotion-ready, stale, or unverified candidates.
3. Present a compact decision list with one recommendation per item: keep as candidate, verify, merge, promote, or archive.
4. Explain the evidence and uncertainty. A high observation count is not proof of technical correctness.
5. Apply changes only after the user selects the items or explicitly authorizes the proposed batch.

Do not automatically promote candidates to rules. Do not push changes; use the separate KB sync workflow.
