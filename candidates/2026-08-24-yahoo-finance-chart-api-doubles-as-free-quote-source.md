# [候補] Yahoo FinanceのChart API(`query1.finance.yahoo.com/v8/finance/chart/{symbol}`)は、日次終値だけでなくAPIキー不要のほぼリアルタイム気配値も`meta`フィールドから取れる

status: candidate
observed_count: 1
observed_in: [kabu-simurator-app]
tags: [finance-api, yahoo-finance, free-tier, no-auth]
date: 2026-08-24

## 何が起きたか
既存のFinnhub無料枠は米国取引所限定で暗号資産(BTC-USD等)のリアルタイム気配値が取得できなかった。日次終値取得には既に非公式のYahoo Finance Chart APIを使っていたが、これがリアルタイム気配値にも使えるかを検証する必要があった。

## わかったこと・今の対応
`https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD?range=1d&interval=1d` を叩くと、`chart.result[0].meta` オブジェクトに `regularMarketPrice`(現在値)・`chartPreviousClose`(前日終値)・`regularMarketDayHigh`/`regularMarketDayLow`・`regularMarketTime`(Unix秒)が含まれており、`indicators.quote[0].open[0]`から始値も取れる。APIキー不要・User-Agentヘッダーを付ければ200で返ってくる。株式・暗号資産(`XXX-USD`形式)どちらのシンボルでも同じレスポンス構造だった。これにより、日次終値とリアルタイム気配値を同一エンドポイント・同一実装パターンで取得でき、暗号資産用に新規の有料API契約が不要になった。

## 詳しい経緯
最初は「Finnhubの代わりに別の有料/無料APIを探す」方向で検討していたが、既存コードが日次終値取得に使っていたYahoo Chart APIのレスポンスを実際にcurlで確認したところ、`meta`部分に現在値相当のデータが既に含まれていることに気づいた。これは非公式(ドキュメント化されていない)エンドポイントのため、将来的に仕様変更や利用制限がかかるリスクは織り込み済みで採用した。

## まだ確認できていないこと
- レート制限の具体的な閾値(1分/1時間あたり何リクエストまで許容されるか)は未確認。今回は30〜60秒間隔のポーリングで問題は出ていないが、より高頻度・多銘柄での挙動は未検証
- 日本株(`7203.T`のような`.T`サフィックス)など米国外の取引所シンボルでも同じ`meta`構造が返るかは未検証(米国株・暗号資産でのみ確認済み)
