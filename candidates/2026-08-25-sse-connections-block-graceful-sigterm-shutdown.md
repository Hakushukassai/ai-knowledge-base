# [候補] Node/ExpressでSSE(Server-Sent Events)を使うと、繋ぎっぱなしの接続が`server.close()`の完了を妨げる

status: candidate
observed_count: 1
observed_in: [kabu-simurator-app]
tags: [node, express, sse, graceful-shutdown, railway]
date: 2026-08-25

## 何が起きたか
価格更新をポーリングからSSEのプッシュ配信に変更した。既存のSIGTERMハンドラは`server.close(callback)`でコールバックが呼ばれるのを待ってから`process.exit(0)`する作りだったが、SSEクライアントが接続したままの状態で再デプロイ(SIGTERM)すると、正常終了が完了しなくなる懸念があった。

## わかったこと・今の対応
`server.close()`は「新規接続の受付を止め、既存のアクティブな接続がすべて自然に終了してから」コールバックを呼ぶ。SSEは意図的に接続を張りっぱなしにする仕組みのため、クライアントが自分から切断しない限り`server.close()`は永久に完了しない。これを放置すると、SIGTERM後10秒のタイムアウトで強制`exit(1)`になり、正常終了ではなく異常終了として扱われてしまう。対応として、SSEルート側で接続中の`Response`オブジェクトを`Set`で保持しておき、SIGTERMハンドラの先頭で`server.close()`を呼ぶ前に、保持している全レスポンスに対して明示的に`res.end()`を呼んで接続を閉じるようにした。これにより`server.close()`のコールバックがすぐ呼ばれるようになった。

## 詳しい経緯
SSE機能を実装する時点でこの問題を予見し、実装と同時に対策(`activeConnections`セットの追跡+`closeAllStreams()`のエクスポート+SIGTERMハンドラからの呼び出し)を組み込んだ。あわせて、切断競合(`req.on("close")`と`res.on("error")`の両方でクリーンアップを走らせる、`res.writableEnded`をチェックしてから`write`する)も入れて、瞬断時にプロセスがクラッシュしないようにした。ローカルで実際に取引を発火させてSSEでプッシュが届くこと、Railway本番でも同様に動くことを確認済み。

## まだ確認できていないこと
- WebSocketなど他の「繋ぎっぱなし」系プロトコルでも同じ対策(明示的な接続追跡+シャットダウン時のclose)が必要になるはずだが、実際にWebSocketで検証はしていない
- 大量の同時SSE接続(数百〜数千)がある場合に、シャットダウン時の一斉`res.end()`がボトルネックにならないかは未検証(今回は個人利用規模のため実害なし)
