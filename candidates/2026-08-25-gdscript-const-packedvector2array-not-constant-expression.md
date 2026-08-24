# [候補] GDScript: `const`に`PackedVector2Array([Vector2(...), ...])`のようなネストした配列コンストラクタは使えない(定数式として畳み込めない)

status: candidate
observed_count: 1
observed_in: [resodive]
tags: [godot, gdscript]
date: 2026-08-25

## 何が起きたか
Godot 4のGDScriptで、アイコンを線画で描くカスタムControlに、頂点座標の固定リストを`const`で持たせようとした。

```gdscript
const HEX_POINTS: PackedVector2Array = PackedVector2Array([
    Vector2(13, 2), Vector2(23, 8), Vector2(23, 18),
    Vector2(13, 24), Vector2(3, 18), Vector2(3, 8),
])
```

このスクリプトを参照する別スクリプト(型ヒントとして使用)ごと、実行時に`Parse Error: Assigned value for constant "HEX_POINTS" isn't a constant expression.`でコンパイルが失敗した。

## わかったこと・今の対応
`Color(r,g,b,a)`のような単純な組み込み型コンストラクタは`const`の初期化式として問題なく使えるが(このプロジェクトの既存コードでも多用されていた)、`PackedVector2Array([Vector2(...), Vector2(...), ...])`のように「配列コンストラクタの中に、さらにVector2コンストラクタ呼び出しを複数並べる」形は、GDScriptのコンパイラが定数式として畳み込めず失敗する。単純なコンストラクタと、コンストラクタをネストした配列とで、定数式として許容されるかどうかに差がある。
対策: `const`ではなく`static var`にする。`static var`は実行時(クラス読み込み時)に一度だけ評価される変数で、定数式である必要が無いため、同じ初期化コードがそのまま動く。値を書き換えない前提なら、実用上`const`との違いはほぼ無い。

## 詳しい経緯
このエラーは、当該スクリプト自身だけでなく、そのクラスを型ヒント(`@onready var x: MyClass = ...`)として参照している別スクリプト(player.gd)の側で`Compile Error: Failed to compile depended scripts.`という連鎖的なエラーも引き起こし、さらにシーン側では「型不一致で代入できない」というランタイムエラーにまで波及した。原因のスクリプト自体のエラーメッセージ(`GDScript::reload`のParse Error)を見れば特定は早いが、連鎖エラーだけを見ていると原因箇所の特定に時間がかかる可能性がある。今回はheadless実行(`godot --headless <scene>`)でこれらのエラーメッセージを直接確認できたことで、原因を即座に特定できた。

## まだ確認できていないこと
- `PackedStringArray([...])`や`PackedFloat32Array([...])`など、他のPacked*Array型でも同様に「単純なリテラルのみ」なら`const`が通り、「コンストラクタ呼び出しを含む要素」だとダメなのか(要素がVector2等のコンストラクタではなく数値/文字列リテラルだけなら通るのか)は未検証
- Godot 4.6以外のバージョンでも同じ制約か未確認
