# 別のパソコンでのセットアップ手順

このフォルダ(`claude-config/`)には、`knowledge-base` を使うために必要な
Claude Codeの設定(hooks)とSkillのコピーが、変更のたびに自動で反映されます。
別のパソコンで同じ環境を作るには、以下の手順を行ってください。

## 手順

1. このリポジトリを `%USERPROFILE%\knowledge-base` に clone する
   ```bash
   git clone <このリポジトリのURL> ~/knowledge-base
   ```

2. `claude-config/settings.json` の中身を `%USERPROFILE%\.claude\settings.json` に反映する
   - まだ `~/.claude/settings.json` が無ければ、そのままコピーする
   - 既にある場合は、中身をマージする(既存の設定を消さないよう注意)
   ```bash
   cp ~/knowledge-base/claude-config/settings.json ~/.claude/settings.json
   ```

3. Skillをコピーする
   ```bash
   mkdir -p ~/.claude/skills
   cp -r ~/knowledge-base/claude-config/skills/* ~/.claude/skills/
   ```

4. ダッシュボードの数字を初期化する
   ```bash
   bash ~/knowledge-base/scripts/generate_stats.sh
   ```

5. `~/knowledge-base/dashboard/index.html` をダブルクリックして開けば、
   同じ内容が表示されるはずです。

## 動作の仕組み(参考)

- `knowledge-base`の中身(rules/candidates/incidents等)を変更すると、
  `/clear`するたびに自動でこのリポジトリにコミットされます
  (Gitでの履歴管理。プッシュは自動ではしないので、他のパソコンに
  反映したい時は `git push` を手動で行ってください)
- 別のパソコン側では、作業を始める前に `git pull` すれば最新の
  知識ベース・設定・Skillを取り込めます
