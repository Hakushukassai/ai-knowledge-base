# [候補] Windows Git Bashでの`python3`コマンドはMicrosoft Storeスタブに化ける

status: candidate
observed_count: 2
observed_in: [ai-dev-knowledge-system]
tags: [windows, python, 環境構築]
date: 2026-08-23

## 何が起きたか
Windows(Git Bash)で`python3`と入力すると、本物のPythonではなく壊れたMicrosoft Storeの案内役が呼ばれてしまい、エラーで止まる。

## わかったこと・今の対応
本物のPythonは別の場所(`Python312`フォルダ)にあるので、そこにPATHを通すか、`python3`という名前のコピーを作ることで回避できる。

## 詳しい経緯
このマシン(Windows + Git Bash環境)で `python3` を実行すると、
実際のPythonではなく `C:\Users\owner\AppData\Local\Microsoft\WindowsApps\python3.exe`
(Microsoft Store の AppInstallerPythonRedirector.exe へのシンボリックリンク)が
呼ばれてしまい、正常に動作しない(`print()`すら実行できず、意味不明な
出力とexit code 49で終了する)。

一方 `python`(3ではなく)コマンドも同じWindowsAppsのstubを指しているが、
`py`ランチャーは正常に動作する。実体のPythonは
`C:\Users\owner\AppData\Local\Programs\Python\Python312\python.exe` にあり、
これを直接PATHに通す(またはシムスクリプトを作る)ことで回避できる。

シェルスクリプト(bashやhookコマンド)内で `python3` をハードコードしていると、
このマシン・この手のWindows環境では静かに失敗する、または不可解な出力になる
点に注意。

(2026-08-25、ai-dev-knowledge-systemで再確認: `python3 -c ""`の終了コードで
実体を判定し、失敗時は`py -3`にフォールバックする`scripts/pyrun.sh`を実装し、
knowledge-base内でpython3をハードコードしていた9箇所すべてに導入した。
実際にこのラッパー経由で`http.server`等を起動できることを確認しており、
`py -3`への統一が実用上十分な回避策であることが確認できた)

## まだ確認できていないこと
- 他のWindowsマシン/ユーザー環境でも同じスタブ配置になっているか未確認
  (Microsoft Store版Pythonのインストール有無に依存する可能性)
- `python3` を直接使わず `py -3` や絶対パス指定に統一するのが
  一般的な回避策として十分か未検証

## 昇格の条件
別のプロジェクト、または別セッションでも同じ現象(`python3`がスタブに
化けて動かない)が確認されたら rules/ に昇格する。
