# [候補] GDScript: 比較式の右辺に`[...] as Array[T]`を書くと「Invalid cast. Cannot convert from "bool"」のパースエラーになる(castを変数へ出す)

status: candidate
observed_count: 1
observed_in: [dotgameinisie]
tags: [godot, gdscript]
date: 2026-08-29

## 何が起きたか

テストコードで「関数の戻り値が特定の型付き配列と等しいか」を1行で書いた:

```gdscript
if ClassData.unlocked_classes() != [&"kenei", &"yugeki"] as Array[StringName]:
```

これがパースエラー `Parse Error: Invalid cast. Cannot convert from "bool" to "Array[StringName]".` でスクリプト自体が読み込めなくなった(実行時エラーではなくロード失敗)。

## わかったこと・今の対応

GDScriptでは`as`の優先順位が比較演算子(`!=`)より低く、`(a != [...]) as Array[StringName]`と解釈される。比較結果のboolを型付き配列へキャストしようとするため「boolからArray[StringName]へ変換できない」というエラーになる。

対応は、キャストを式の中に書かずに変数へ出すか、そもそも配列同値比較をやめて要素検査にする:

```gdscript
var expected: Array[StringName] = [&"kenei", &"yugeki"]
if ClassData.unlocked_classes() != expected:
```

(今回は`size()`と`has()`での検査に書き換えた。)

パースエラーなのでそのスクリプトを読み込むテストランナーごと失敗し、エラーメッセージが「boolからのキャスト」と表示されるため、比較演算子との優先順位問題だと気づきにくい。

## 詳しい経緯

BU13のclass_shield_test.gdで職業の初期解放リストを検証しようとして発生。`--headless --script`実行時に`Failed to load script ... Parse error`となり、行番号からこの1行を特定。括弧で`(… as Array[StringName])`と囲んでも読みにくいだけなので、変数へ出す形へ統一した。

## まだ確認できていないこと

- Godot 4.6以外での挙動(演算子優先順位は言語仕様なので同じはずだが未確認)
- `is`にも同様の優先順位の罠があるか
