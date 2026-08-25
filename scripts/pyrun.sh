#!/bin/sh
# python3コマンドがWindows(Git Bash)で壊れたMicrosoft Storeスタブに
# なることがある問題(candidates/2026-08-23-windows-python3-stub-broken.md)を
# 吸収する薄いラッパー。knowledge-base内のスクリプト呼び出しはすべて
# python3を直接叩かず、このラッパー経由にする。
#
# 使い方:
#   sh pyrun.sh script.py [args...]   … スクリプトファイルを実行
#   sh pyrun.sh < script.py           … heredoc等、標準入力から実行(引数無し)

if python3 -c "" >/dev/null 2>&1; then
  exec python3 "$@"
elif command -v py >/dev/null 2>&1; then
  exec py -3 "$@"
else
  echo "pyrun.sh: 実行可能なPython(python3 / py -3)が見つかりません" >&2
  exit 1
fi
