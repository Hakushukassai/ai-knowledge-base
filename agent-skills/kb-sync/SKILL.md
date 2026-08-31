---
name: kb-sync
description: Validate, commit, and push intentional knowledge-base changes to GitHub. Use only when the user explicitly asks to sync or push the KB.
---

# Sync the KB

The user's explicit request to sync authorizes committing and pushing the current intentional KB changes, but not unrelated files or global agent configuration.

1. In `~/knowledge-base`, run `git status --short` and inspect every changed path.
2. Stop and ask if any change is unrelated, surprising, secret, or generated from private material.
3. Run:
   - `sh scripts/pyrun.sh scripts/validate_kb.py`
   - `sh scripts/pyrun.sh claude-config/hooks/scan_secrets.py .`
   - `bash scripts/generate_stats.sh`
4. Recheck the diff. Stage only the reviewed KB paths; never copy or stage the contents of `~/.claude`, `~/.agents`, or `~/.codex`.
5. Commit with a concise message, run `git pull --rebase`, then `git push`.
6. Report the commit and whether the push succeeded. On conflicts, preserve both sides and ask the user rather than guessing.
