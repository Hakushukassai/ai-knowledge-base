# [候補] `npm run start` でラップしたNode常駐プロセスは、アプリ側のSIGTERM正常終了とは別にnpm自身がSIGTERMをエラーとしてログ出力し、PaaSの「クラッシュ」判定を誤爆させる

status: candidate
observed_count: 1
observed_in: [kabu-simurator-app]
tags: [node, deployment, railway, process-management]
date: 2026-08-24

## 何が起きたか
Railway上のExpressサーバーで、`process.on("SIGTERM", ...)` によるgraceful shutdown(サーバーclose→DB close→`process.exit(0)`)を実装したにもかかわらず、再デプロイのたびにRailwayが「Deployment crashed」通知を出し続けた。

## わかったこと・今の対応
実際のDeploy Logsを確認すると、アプリ自身のシャットダウンログは正常に出ている一方で、`npm error signal SIGTERM` という行が別途出力されていた。原因は起動コマンドが `npm run start:server`(内部で `tsx server/index.ts` を呼ぶ)になっており、npm自身がSIGTERMを受け取った際に、子プロセス(tsx/Node)の終了とは無関係に「エラーとして」ログを出す仕様だったため。Railwayの起動コマンドを `npm run start:server` から `node_modules/.bin/tsx server/index.ts`(npmを介さず直接バイナリを起動)に変更したところ、`npm error signal SIGTERM` の行は完全に消え、アプリ側の正常終了ログのみが残るようになった。ただし、Railwayの「Deployment crashed」通知自体は、実際のexit codeやログ内容に関係なく「デプロイが置き換えられたこと」を示す汎用ラベルであることも別途確認しており、通知自体は消えない(無害と判断して無視する運用にした)。

## 詳しい経緯
最適化監査の一環でSIGTERMハンドラを追加した後、手動でRedeployをトリガーして新旧コマンドそれぞれのDeploy Logsを直接比較することで、npm起因のエラー出力だと特定した。Railwayのダッシュボード設定変更(Settings → Deploy → Custom Start Command)は「CI/CDパイプラインの変更」に該当するため、変更前にユーザーへ明示的に確認を取ってから実施した。

## まだ確認できていないこと
- Railway以外のPaaS(Render、Fly.io等)でも同様に「Deployment crashed」的な通知が誤爆するか未確認
- `npm run start` ではなく `npm start`(package.jsonのstartスクリプト)でも同じ現象が起きるか未確認(おそらく同じnpm実装なので起きると推測されるが未検証)
