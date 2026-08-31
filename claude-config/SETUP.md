# 初回セットアップ

## 1. 通常のターミナルで実行

```bash
git clone https://github.com/Hakushukassai/ai-knowledge-base.git ~/knowledge-base
bash ~/knowledge-base/claude-config/install.sh
```

すでにclone済みなら次だけ実行します。

```bash
cd ~/knowledge-base
git pull
bash claude-config/install.sh
```

インストーラーは次を行います。

- `kb-recall`、`kb-capture`、`kb-review`、`kb-sync` をClaude CodeとCodexへ配置
- 旧KBのSessionEnd自動処理だけをバックアップ後に解除
- このリポジトリのcommit前機密情報チェックを有効化
- KB検証とダッシュボード更新

既存の無関係なClaude設定やフックは残します。

## 2. 新しいチャットを開始

スキルを認識させるため、Claude CodeまたはCodexで新しいチャットを開始します。

以後は次のように依頼できます。

- `KBで過去の類似問題を探して`
- `今の発見をKBに記録して`
- `KBを整理して`
- `KBをGitHubに同期して`

GitHub同期時に認証を求められた場合だけ、通常のターミナルで `gh auth login` を実行してください。

## Obsidianで見る場合（任意）

Obsidianの「Open folder as vault」で `~/knowledge-base` を選びます。
専用プラグインは不要です。
