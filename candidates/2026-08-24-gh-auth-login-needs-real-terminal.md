# [候補] `gh auth login`はClaude Code経由ではなく独立したターミナルで実行する必要がある

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [claude-code, git, github, 環境構築]
date: 2026-08-24

## 何が起きたか
`gh auth login`をClaude Codeのチャット上(コードブロックのRunボタン経由)で実行してもらったところ、ユーザーは完了したつもりでも`gh auth status`は未ログインのままだった。

## わかったこと・今の対応
Macの通常のターミナル(Terminal.appなど)で直接`gh auth login`を実行し直してもらったところ、ブラウザでの認可まできちんと完了し、`gh auth status`で認証済みと確認できた。ブラウザを開いて対話的にコードを入力する必要があるコマンドは、Claude Code経由の実行だと完了しないことがある、という前提で案内した方がよい。

## 詳しい経緯
1回目は「終わった」という申告を受けて`gh auth status`を確認したが`You are not logged into any GitHub hosts`のままだった。`~/.config/gh`ディレクトリ自体が存在しておらず、認証情報が一切保存されていなかった。原因は明言できていないが、Claude Code経由の実行環境(Bashツール/Runボタン)では、`gh auth login`が要求するブラウザでの対話的な認可フローが正しく完了しなかったと推測される。ユーザーに「Claude Codeのこのチャット上ではなく、Macの通常のターミナルで直接実行してほしい」と案内し直したところ、2回目で`gh auth status`が正常に認証済み(keyring経由)と表示された。

## まだ確認できていないこと
- 具体的にどの段階(ブラウザが開かない/コード入力ができない/トークン保存ができない等)で失敗していたのかは未確認。
- SSH認証方式や`--web`オプションなし等、他の`gh auth login`の選択肢でも同様の問題が起きるかは未確認。
