# AI開発ナレッジベース

Claude Code と Codex が共通で使う、Markdown製の個人向け技術KBです。
会話を終了しなくても、必要な時だけ「検索・記録・整理・同期」できます。

## 使い方

AIには自然な言葉で次のように依頼します。

- `KBで過去の類似問題を探して`
- `今の発見をKBに記録して`
- `KBを整理して`
- `KBをGitHubに同期して`

記録と同期は分離されています。記録しただけではGitHubへpushされません。
会話終了時の自動記録・自動pushも行いません。

## 何が保存されるか

| 場所 | 意味 | 信頼度 |
|---|---|---|
| `rules/` | 確認済みの再利用ルール | 高い |
| `incidents/` | 実際の問題と解決の事例 | 中〜高 |
| `candidates/` | まだ一般化・検証途中の発見 | 未確定 |
| `external-skill-imports/` | 外部Skillの導入記録 | 個別確認 |

`candidates/` は2プロジェクトでの観測、3回以上の観測、または人による確認の
いずれかを満たすと整理対象になります。昇格は自動では行いません。

## 構成

- `agent-skills/`: Claude Code / Codex 共通のKB操作スキル
- `scripts/kb_search.py`: 関連記録の検索
- `scripts/kb_capture.py`: 重複確認付きの明示的な記録
- `scripts/kb_review.py`: 整理候補の読み取り専用レポート
- `scripts/validate_kb.py`: 構造・リンク検証
- `scripts/generate_stats.sh`: `docs/` のダッシュボード更新
- `claude-config/`: セットアップと既存Claude向けスキル

## 初回セットアップ

詳しくは `claude-config/SETUP.md` を参照してください。

```bash
git clone https://github.com/Hakushukassai/ai-knowledge-base.git ~/knowledge-base
bash ~/knowledge-base/claude-config/install.sh
```

セットアップは既存のClaude設定を丸ごと上書きしません。旧KBのSessionEndフックだけを
バックアップ後に除去し、共通スキルを `~/.claude/skills/` と `~/.agents/skills/` に配置します。

## Obsidianとの関係

このリポジトリ自体がMarkdownの保管庫なので、`~/knowledge-base` をObsidianのVaultとして
開けます。Obsidianは人が読む・リンクする・整理するための画面、KBスクリプトとSkillは
AIが検索・記録・検証するための仕組みです。別の知識を二重保存する必要はありません。

## 安全性

- 認証情報、顧客情報、非公開契約、私的データは保存しない
- 時点で変わる外部情報は一次資料で再確認する
- `candidates/` は事実として断定しない
- push前に検証と機密情報スキャンを実行する

定期確認には `PRIVACY-CHECKLIST.md` を使います。
