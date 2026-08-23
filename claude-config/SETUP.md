# 別のパソコンでのセットアップ手順

このフォルダ(`claude-config/`)には、`knowledge-base` を使うために必要な
Claude Codeの設定(hooks)とSkillのコピーが、変更のたびに自動で反映されます。
別のパソコンで同じ環境を作るには、以下の手順を行ってください。

## 手順

1. このリポジトリを `%USERPROFILE%\knowledge-base` に clone する
   ```bash
   git clone https://github.com/Hakushukassai/ai-knowledge-base.git ~/knowledge-base
   ```

2. `claude-config/settings.json` の中身を `%USERPROFILE%\.claude\settings.json` に反映する
   - まだ `~/.claude/settings.json` が無ければ、そのままコピーする
   - 既にある場合は、中身をマージする(既存の設定を消さないよう注意)
   ```bash
   cp ~/knowledge-base/claude-config/settings.json ~/.claude/settings.json
   ```

3. Skill・hook用の補助スクリプト・カスタムコマンドをコピーする
   ```bash
   mkdir -p ~/.claude/skills ~/.claude/hooks ~/.claude/commands
   cp -r ~/knowledge-base/claude-config/skills/* ~/.claude/skills/
   cp -r ~/knowledge-base/claude-config/hooks/* ~/.claude/hooks/
   cp -r ~/knowledge-base/claude-config/commands/* ~/.claude/commands/
   ```
   (`hooks/`には、機密情報チェックやSkill使用回数の記録に使う
   Pythonスクリプトが入っています。無いとhookの一部が動きません。
   `commands/`には `/kb-sync` などのカスタムコマンドが入っています)

4. ダッシュボードの数字を初期化する
   ```bash
   bash ~/knowledge-base/scripts/generate_stats.sh
   ```

5. `~/knowledge-base/docs/index.html` をダブルクリックして開けば、
   同じ内容が表示されるはずです。

## 動作の仕組み(参考)

- 作業が終わったら `/exit` と打ってから閉じる(×ボタンでいきなり
  閉じない)。`/clear`でも同様に動くが、その場合は会話がリセットされる。
  どちらの場合も、自動でHANDOFF.md書き出し→知識ベースへの反映→
  GitHubへのpushまで行われる
- 会話を終わらせずに今すぐ反映したい場合は `/kb-sync` と打つ
  (セッションはそのまま続く)
- 別のパソコン側では、作業を始める前に `git pull` すれば最新の
  知識ベース・設定・Skill・コマンドを取り込めます(このパソコン側の
  `/exit`や`/clear`が自動で`git pull`もしてくれますが、他のパソコンから
  戻ってきた直後は念のため手動で`git pull`しておくと確実です)
