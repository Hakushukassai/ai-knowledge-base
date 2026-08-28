# [候補] Godot: `parse_input_event`で合成したパッド入力は`Input.get_connected_joypads()`系のポーリングに映らない──「パッド操作か」の判定は`_input()`でイベント種別を記録する

status: candidate
observed_count: 1
observed_in: [dotgameinisie]
tags: [godot, input, testing]
date: 2026-08-29

## 何が起きたか

インベントリUIで「同じ決定ボタンでも、パッド(A)なら『持つ』、キーボード(Enter)なら『装備』」と挙動を分けるため、最初は次のポーリングで判定していた:

```gdscript
for device in Input.get_connected_joypads():
    if Input.is_joy_button_pressed(device, JOY_BUTTON_A):
        return true
```

実パッドでは動くが、自動テストから`Input.parse_input_event(InputEventJoypadButton...)`で合成イベントを流しても、物理パッドが接続されていないと`get_connected_joypads()`が空のままなのでパッド判定が常にfalseになり、この機能を実入力で自動テストできなかった。

## わかったこと・今の対応

判定を「デバイスのポーリング」から「**直前に届いた入力イベントの種別の記録**」へ変えた。UIコントロールがイベントを消費する前に必ず通る`_input()`で記録する:

```gdscript
var _last_input_pad := false

func _input(event: InputEvent) -> void:
    if event is InputEventJoypadButton or event is InputEventJoypadMotion:
        _last_input_pad = true
    elif event is InputEventKey or event is InputEventMouseButton:
        _last_input_pad = false
```

これなら実パッドでも合成イベントでも同じ経路で判定でき、`parse_input_event`ベースの自動テスト(PAD_CARRY_TEST)がそのまま通る。フォーカス中のButtonがA(ui_accept)を消費しても、`_input()`は消費前に全イベントを見られるため取りこぼさない(`_unhandled_input`だと消費後なので不可)。

副次の教訓: ポーリングでの実装は「実機がないと自動テストできない」を招きやすい。入力元の識別はイベント駆動で持つ方がテスタブル。

## 詳しい経緯

BU13でパッドのドラッグ代替(A2回=持つ→Aで置く)を実装した際、実JoypadButtonイベントの回帰テストを書こうとして判明。さらにこのテストが「空の倉庫グリッドは全スロットdisabled+FOCUS_NONEで、パッドでは最初の1個を置く先が存在しない」という実UIバグまで検出した(運搬中だけ空きスロットをフォーカス可能な受け皿にして解決)。合成イベントで自動化できたからこそ見つかったバグ。

## まだ確認できていないこと

- `InputEventJoypadMotion`(スティック)だけで操作している間の判定粒度(今回はボタン中心で十分だった)
- 複数入力デバイスを同時に使う環境(パッド+マウス併用)での切り替わりの体感
