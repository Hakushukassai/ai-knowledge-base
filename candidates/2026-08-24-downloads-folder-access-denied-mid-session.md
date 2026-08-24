# [候補] セッション再開後、`~/Downloads`への読み取りアクセスが拒否されることがある

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [claude-code, macOS, 環境構築]
date: 2026-08-24

## 何が起きたか
同じ会話内で以前は`~/Downloads`配下のファイルを問題なく読み書きできていたのに、セッション再開(resume)後に`ls ~/Downloads`が`Operation not permitted`で失敗するようになった。`stat`ではディレクトリの存在自体は見えるが、中身の読み取り(`ls`、ファイルオープン)だけ拒否される状態だった。

## わかったこと・今の対応
macOSのプライバシー保護機能(TCC、Downloadsフォルダへのアクセスはアプリ単位で許可が必要)が、セッション再開で生成された新しいプロセスにはまだ許可されていないためと推測される。System Settingsでの許可し直しを試す前に、`~/Documents`配下(既にアクセスできていた場所)に対象ファイルを再取得してもらうことで回避できた。

## 詳しい経緯
`ux-designer-skill`リポジトリのcloneを`~/Downloads`に置いてもらった直後、`ls`が失敗した。`echo test > /tmp/...`や`stat ~/Downloads`は正常に動いたため、プロセス自体は生きているが特定のディレクトリだけアクセス拒否されている状況と判断した。`~/Documents/original-game/`配下への再cloneを依頼したところ、即座に正常に読み書きできた。

## まだ確認できていないこと
- System Settings → Privacy & Security → Files and Folders で該当アプリに許可を与えれば`~/Downloads`も復旧するのか(未検証、回避策で済ませたため)
- 毎回のセッション再開で必ず起きるのか、特定条件下でのみ起きるのか
