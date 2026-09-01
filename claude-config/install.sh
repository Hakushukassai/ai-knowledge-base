#!/bin/bash

set -e

KB_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[1/4] Claude Code と Codex に KB スキルを配置します"
mkdir -p "$HOME/.claude/skills" "$HOME/.agents/skills"
cp -R "$KB_DIR/agent-skills/." "$HOME/.claude/skills/"
cp -R "$KB_DIR/agent-skills/." "$HOME/.agents/skills/"

# Codex専用のデザインスキルと共通ルールを安全に追加する。
if [ -x "$KB_DIR/codex-config/install.sh" ]; then
  bash "$KB_DIR/codex-config/install.sh"
fi

# 既存の Godot / UI 系 Claude Code スキルも引き続き使えるようにする。
if [ -d "$KB_DIR/claude-config/skills" ]; then
  cp -R "$KB_DIR/claude-config/skills/." "$HOME/.claude/skills/"
fi

echo "[2/4] 旧 SessionEnd KB フックだけを安全に解除します"
sh "$KB_DIR/scripts/pyrun.sh" "$KB_DIR/scripts/migrate_claude_settings.py" --apply

echo "[3/4] コミット前の機密情報チェックを有効にします"
(cd "$KB_DIR" && git config core.hooksPath .githooks)

echo "[4/4] KB を検証し、ダッシュボードを更新します"
KB_DIR="$KB_DIR" sh "$KB_DIR/scripts/pyrun.sh" "$KB_DIR/scripts/validate_kb.py"
KB_DIR="$KB_DIR" bash "$KB_DIR/scripts/generate_stats.sh"

echo "セットアップ完了。新しい Claude Code / Codex のチャットを開始してください。"
echo "GitHub 同期時に未認証と言われた場合だけ gh auth login を実行してください。"
