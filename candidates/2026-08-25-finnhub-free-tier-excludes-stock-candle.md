# [候補] Finnhub無料枠は`/quote`(現在値)は使えるが`/stock/candle`(過去足)は使えない

status: candidate
observed_count: 1
observed_in: [kabu-simurator-app]
tags: [finance-api, finnhub, free-tier]
date: 2026-08-25

## 何が起きたか
株価シミュレーターでFinnhubを使い、現在値(`/quote`)と過去90日の日足(`/stock/candle`)の両方を取得する実装をしたところ、現在値は正常に取れるのにチャート用の過去足だけが常に502エラーになった。

## わかったこと・今の対応
バックエンドのエラーを直接curlで再現したところ、Finnhubから`{"error":"You don't have access to this resource."}`が返っていた。`/quote`エンドポイントは無料枠で問題なく使えるのに対し、`/stock/candle`(過去の日足データ)は有料プラン専用になっている。無料枠だからといって「基本的な機能は一通り使える」と思い込まず、エンドポイントごとに個別に無料枠の対象かを確認する必要がある。今回はYahoo Finance Chart API(`query1.finance.yahoo.com/v8/finance/chart/{symbol}`、[別候補]参照)に過去足取得だけ切り替えて解決し、現在値取得は引き続きFinnhubのまま併用した。

## 詳しい経緯
最初はFinnhub単体で「現在値+過去足」を賄う設計だったが、フロントエンドのチャートが「価格データを取得中、または未取得です」のまま進まないことに気づき、バックエンドのエラーログとcurlでの直接検証で原因を切り分けた。Finnhubの料金体系は変更されることがあるため、この制限が今後も続くとは限らない。

## まだ確認できていないこと
- Finnhubの有料プランでは実際に`/stock/candle`が使えるようになるか(公式ドキュメント上はそう読めるが実際に契約して確認はしていない)
- `/quote`以外の他のエンドポイント(例: 企業情報、決算カレンダー等)がそれぞれ無料枠の対象かどうかは未調査
