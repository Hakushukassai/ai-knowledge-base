# Codexスキルを別端末へ導入する

このフォルダには、KBで管理するCodex用スキルと共通ルールが入っています。
Appleが配布するデザイン素材そのものは含みません。

## 初回だけ行うこと

通常のターミナルで実行します。

```bash
git clone https://github.com/Hakushukassai/ai-knowledge-base.git ~/knowledge-base
bash ~/knowledge-base/codex-config/install.sh
```

すでにKBをclone済みなら、2行目だけで構いません。

この処理は、KB内の各スキルを `~/.agents/skills/` から参照するショートカットと、
共通ルールを `~/.codex/AGENTS.md` から参照するショートカットを作ります。
既存ファイルがある場合は上書きせず、`SKIP` と警告して残りのセットアップを続けます。

## 更新

```bash
git -C ~/knowledge-base pull
```

ショートカット方式なので、pull後の再インストールは通常不要です。
スキルが表示されない場合はCodexを再起動してください。

## Codexプラグイン

Product DesignなどのCodexプラグイン本体は、このKBには含まれません。
別端末のCodexで利用できない場合は、Skills / Plugins画面で同じプラグインを導入してください。

## Apple Design Resources

Apple Design Resourcesは各端末でApple公式から取得し、GitHubには追加しません。
使う場合は、その端末の素材フォルダを `APPLE_DESIGN_RESOURCES_DIR` で指定します。

```bash
export APPLE_DESIGN_RESOURCES_DIR="/absolute/path/to/AppleDesignResources"
```

## 既存ファイルがあり `SKIP` された場合

- `~/.agents/skills/<スキル名>` が既にある場合は、内容を確認してから手動で整理します。
- `~/.codex/AGENTS.md` が既にある場合は、既存内容を消さずに `codex-config/AGENTS.md` のルールを統合します。
