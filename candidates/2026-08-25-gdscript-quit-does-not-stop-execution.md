# [候補] GDScript: `SceneTree.quit()`は即座に処理を中断しない(呼んだ後も関数の残りが実行され続け、後続の`quit()`呼び出しが終了コードを上書きする)

status: candidate
observed_count: 1
observed_in: [resodive]
tags: [godot, gdscript, testing]
date: 2026-08-25

## 何が起きたか

Godot 4のGDScriptで、`--headless --script`実行用の簡易テストランナー(`extends SceneTree`)を書いた。成功時と失敗時で終了コードを分けるために、次のような構造にした:

```gdscript
if _failures.is_empty():
    print("PASS: %d checks" % _count)
    quit(0)

for failure in _failures:
    print("MISMATCH: %s" % failure)
print("FAILED: %d of %d checks" % [_failures.size(), _count])
quit(1)
```

実行してみると、13件のチェックが全て通っており`PASS: 13 checks`と正しく出力されているにもかかわらず、その直後に`FAILED: 0 of 13 checks`という(内容的には正しいが意図しない)行まで出力され、プロセスの終了コードは1になった(本来は0を期待していた)。

## わかったこと・今の対応

`SceneTree.quit(exit_code)`は「次のフレーム(またはイテレーション)の終わりにメインループを終了する」という**予約**を行うだけで、呼び出した時点でGDScriptの現在の関数の実行を即座に中断するわけではない。上記のコードでは`if`ブロックの中で`quit(0)`を呼んだ後に`return`が無いため、処理はそのまま`if`ブロックを抜けて後続のコード(空の`_failures`をループするだけの無害な処理だが、その後にある`print(...)` と `quit(1)`)まで実行してしまう。`quit()`を2回呼ぶと、後から呼んだ方の終了コードが有効になるため、最終的にプロセスは1で終了する。

対策は単純で、`quit()`の直後に成功パスであれば必ず`return`を置き、それ以降のコードへ処理が落ちないようにする。

```gdscript
if _failures.is_empty():
    print("PASS: %d checks" % _count)
    quit(0)
    return  # ← これが無いと下まで実行され続ける

...
quit(1)
```

## 詳しい経緯

`--headless --script`ベースの自動テストをCI(このプロジェクトではGodotのSmoke Test)に組み込んでいる過程で発覚した。Smoke Test側は「exit codeが0以外なら失敗」という判定をしており、この不具合を正しく検知して停止した——ただし停止理由の実体は、テスト対象のコードのバグではなく、テストランナー自身の制御フローのバグだった、という点が紛らわしい。ログ上は`PASS: 13 checks`という一見成功に見える行が出力されているため、exit codeだけでなく実際の出力内容も併せて確認しないと原因の切り分けに時間がかかる可能性がある。

## まだ確認できていないこと

- `_process()`や通常の`Node._ready()`等、`SceneTree._initialize()`以外のコンテキストでも同じ「`quit()`は即座に中断しない」という性質が成り立つか(GDScriptの言語仕様として`quit()`が特別扱いされていないことの直接的な裏付けまでは未確認)
- Godot 4.6以外のバージョンでも同じ挙動か未確認
