#!/bin/bash
# 別のパソコンでのセットアップをできる範囲で1コマンドにまとめたスクリプト。
#
# 使い方(先に `git clone https://github.com/Hakushukassai/ai-knowledge-base.git ~/knowledge-base` を実行してから):
#   bash ~/knowledge-base/claude-config/install.sh
#
# このスクリプトが終わったあとも、以下の2つだけは手動で行う必要がある
# (詳細は SETUP.md 参照):
#   - gh auth login   ブラウザでの認可が必要なため自動化できない
#   - ~/.claude/settings.json が既に存在した場合の中身のマージ
#     (このスクリプトは安全のため、既存ファイルを上書きしない)
set -e

KB_DIR="$HOME/knowledge-base"

if [ ! -d "$KB_DIR" ]; then
  echo "エラー: $KB_DIR が見つかりません。先に以下を実行してください。"
  echo "  git clone https://github.com/Hakushukassai/ai-knowledge-base.git ~/knowledge-base"
  exit 1
fi

echo "[1/4] skills / hooks / commands を配置..."
mkdir -p "$HOME/.claude/skills" "$HOME/.claude/hooks" "$HOME/.claude/commands"
[ -d "$KB_DIR/claude-config/skills" ] && cp -r "$KB_DIR/claude-config/skills/." "$HOME/.claude/skills/"
[ -d "$KB_DIR/claude-config/hooks" ] && cp -r "$KB_DIR/claude-config/hooks/." "$HOME/.claude/hooks/"
[ -d "$KB_DIR/claude-config/commands" ] && cp -r "$KB_DIR/claude-config/commands/." "$HOME/.claude/commands/"

echo "[2/4] gitのpre-commitフック(機密情報チェック)を有効化..."
(cd "$KB_DIR" && git config core.hooksPath .githooks)

echo "[3/4] ダッシュボードの数字を初期化..."
bash "$KB_DIR/scripts/generate_stats.sh"

echo "[4/4] Claude Codeの設定 (~/.claude/settings.json) を配置..."
if [ -f "$HOME/.claude/settings.json" ]; then
  echo "  既に ~/.claude/settings.json が存在するため、上書きせずスキップしました。"
  echo "  中身を見比べて手動でマージしてください:"
  echo "    diff \"$KB_DIR/claude-config/settings.json\" \"$HOME/.claude/settings.json\""
else
  cp "$KB_DIR/claude-config/settings.json" "$HOME/.claude/settings.json"
  echo "  配置しました。"
fi

echo ""
echo "自動化できるところは完了しました。残りは以下の1ステップです:"
echo "  gh auth login   ← GitHubへのpush認証。ブラウザでの認可が必要なため手動で実行してください。"
echo ""
echo "終わったら ~/knowledge-base/docs/index.html を開いて表示を確認してください。"
