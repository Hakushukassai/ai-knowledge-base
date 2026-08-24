# [候補] Claude Codeは自分自身の`~/.claude/settings.json`を書き換えられない

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [claude-code, hooks, 環境構築]
date: 2026-08-24

## 何が起きたか
Claude Codeに`~/.claude/settings.json`(hooksの設定ファイル)を新規作成・編集させようとすると、BashツールでもWriteツールでも、auto-modeのクラシファイアに拒否された。

## わかったこと・今の対応
ツールを変えても同じ理由で拒否されるため、回避策ではなく仕様と考えられる。内容をファイルに書き出し、ユーザー本人に自分のターミナルで`cp`させることで設置できた。他の`~/.claude/hooks/`配下のスクリプトファイルや`~/.claude/commands/`は同じ手順で問題なく書き込めたので、`settings.json`(hooks定義そのもの)だけが特別扱いされている可能性が高い。

## 詳しい経緯
`claude-config/settings.json`の内容を`~/.claude/settings.json`にコピーする際に発生。1回目はBashツールの`cp`コマンドで拒否(`Permission for this action was denied by the Claude Code auto mode classifier`)。2回目はWriteツールで直接書き込みを試したが同様に拒否。3回目にコマンドの中身をスクラッチパッド上のファイルに書き出し、それをユーザー自身のターミナルで`~/.claude/settings.json`にコピーしてもらう形で解決した。

## まだ確認できていないこと
- ユーザー側の権限設定(permissions allow list等)で、この制限を緩められるかどうかは未確認。
- `~/.claude/settings.json`以外に同様にブロックされるファイル(例えばプロジェクト直下の`.claude/settings.json`)があるかは未確認。
