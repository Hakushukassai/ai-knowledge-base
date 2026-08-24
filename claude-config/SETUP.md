# 別のパソコンでのセットアップ手順

このフォルダ(`claude-config/`)には、`knowledge-base` を使うために必要な
Claude Codeの設定(hooks)とSkillのコピーが、変更のたびに自動で反映されます。
別のパソコンで同じ環境を作るには、以下の手順を行ってください。

## 手順

1. このリポジトリを `~/knowledge-base` に clone する
   ```bash
   git clone https://github.com/Hakushukassai/ai-knowledge-base.git ~/knowledge-base
   ```

2. セットアップスクリプトを実行する(skills・hooks・commandsの配置、
   pre-commitフックの有効化、ダッシュボードの初期化、`~/.claude/settings.json`の配置を
   まとめて行う)
   ```bash
   bash ~/knowledge-base/claude-config/install.sh
   ```
   - `~/.claude/settings.json` が既に存在する場合は、安全のため上書きされません。
     スクリプトの案内に従って手動でマージしてください(既存の設定を消さないよう注意)。

3. GitHubへのpush認証を行う
   ```bash
   gh auth login
   ```
   `GitHub.com` → `HTTPS` → `Login with a web browser` を選び、表示されたコードを
   ブラウザで入力すれば完了です。

4. `~/knowledge-base/docs/index.html` をダブルクリックして開けば、
   同じ内容が表示されるはずです。

## 注意: 手順2・3はClaude Codeのチャット上ではなく、Macの通常のターミナルで実行する

これは実際にハマった落とし穴です(詳細は `candidates/` 内の関連ファイル参照)。

- **`~/.claude/settings.json` への書き込み**は、Claude Code自身のBash/Writeツールからは
  安全のためブロックされます(auto-modeクラシファイアによる制限)。これが `install.sh` を
  「Claude Codeに実行させる」のではなく、ユーザー自身がターミナルで実行する設計にしている理由です。
- **`gh auth login`** はブラウザでの対話的な認可が必要なコマンドです。Claude Codeのチャット上
  (コードブロックのRunボタンなど)経由で実行すると、認可が正しく完了しないことがあります。
  必ずMacの通常のターミナル(Terminal.appなど)を直接開いて実行してください。

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
- 複数のPCでほぼ同時に更新すると、自動pushが競合(コンフリクト)して
  失敗することがあります。その場合は `~/knowledge-base/SYNC-CONFLICT.md`
  が作られ、次にセッションを開いた時に警告として表示されます
  (ファイル内に手動での解決手順が書かれています)。

## `~/.claude/settings.json` の適用範囲について

`claude-config/settings.json` に含まれる `model` / `effortLevel` の指定は、
このknowledge-baseに関係する作業だけでなく、**このパソコン上の全てのプロジェクトの
Claude Codeセッションに共通のデフォルト設定として適用されます**。
他のプロジェクトで異なる設定を使いたい場合は、`~/.claude/settings.json` の
該当行を直接編集(または削除)してください。
