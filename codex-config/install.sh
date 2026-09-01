#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target_root="${CODEX_SETUP_TARGET_ROOT:-${HOME:?HOME is not set}}"
skills_source="$script_dir/skills"
skills_target="$target_root/.agents/skills"
codex_target="$target_root/.codex"
guidance_source="$script_dir/AGENTS.md"
guidance_target="$codex_target/AGENTS.md"
conflicts=0

mkdir -p "$skills_target" "$codex_target"

for source_dir in "$skills_source"/*; do
  [[ -f "$source_dir/SKILL.md" ]] || continue
  skill_name="$(basename "$source_dir")"
  target_dir="$skills_target/$skill_name"

  if [[ -L "$target_dir" ]]; then
    if [[ "$(readlink "$target_dir")" == "$source_dir" ]]; then
      echo "OK: $skill_name"
    else
      echo "SKIP: $target_dir is linked somewhere else" >&2
      conflicts=1
    fi
  elif [[ -e "$target_dir" ]]; then
    echo "SKIP: $target_dir already exists; existing files were not changed" >&2
    conflicts=1
  else
    ln -s "$source_dir" "$target_dir"
    echo "INSTALLED: $skill_name"
  fi
done

if [[ -L "$guidance_target" ]]; then
  if [[ "$(readlink "$guidance_target")" == "$guidance_source" ]]; then
    echo "OK: global AGENTS.md"
  else
    echo "SKIP: $guidance_target is linked somewhere else" >&2
    conflicts=1
  fi
elif [[ -e "$guidance_target" ]]; then
  echo "SKIP: $guidance_target already exists; merge $guidance_source manually" >&2
  conflicts=1
else
  ln -s "$guidance_source" "$guidance_target"
  echo "INSTALLED: global AGENTS.md"
fi

if [[ "$conflicts" -ne 0 ]]; then
  echo "Setup finished with skips. No existing files were overwritten." >&2
  echo "Review the SKIP messages and merge those items manually." >&2
else
  echo "Codex design skills are ready. Restart Codex if they do not appear automatically."
fi
