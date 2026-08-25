# [候補] Godot: `--script`実行のSceneTreeエントリスクリプトから、autoloadを参照するスクリプトを読み込むと`_init()`ではまだautoloadが登録されておらず失敗する(`_initialize()`でも、エントリスクリプト自身がbareなautoload識別子を直接書いていればダメ)

status: candidate
observed_count: 1
observed_in: [resodive]
tags: [godot, gdscript, testing, ci, headless]
date: 2026-08-25

## 何が起きたか

Godot 4のプロジェクトで、`godot --headless --path . --script <エントリスクリプト.gd>`という形でヘッドレスの自動テストスクリプト(`extends SceneTree`)を書き、GDScriptの純粋関数(例: ボスのHPフェーズ判定)を検証しようとした。

1回目: エントリスクリプトの`_init()`(コンストラクタ)の中で、autoload(`GameState`等)を参照する別スクリプト(例: `enemy_boss.gd`。継承元の`enemy.gd`が`GameState`をbare識別子で参照している)を`preload()`/`load()`すると、`SCRIPT ERROR: Compile Error: Identifier not found: GameState`という偽陽性のエラーが毎回(3/3回再現)出た。ただし直後にGodotの既にコンパイル済みのクラスキャッシュへのフォールバックが働くらしく、最終的なテスト結果自体(`quit(0)`/`quit(1)`)は正しく出ることが多かった——しかしこの「SCRIPT ERROR:」等のノイズは、exit codeが信用できないGodotでよく使われる「出力に決まったエラー文言が含まれていないか」ベースのCI/Smoke Test判定を誤って失敗させてしまう。

2回目(別関数のテストで発生): 1回目の教訓を踏まえ、対象スクリプトの読み込みを`_init()`から`_initialize()`(SceneTreeのライフサイクルフック、autoload登録後に呼ばれる)に移したところ、この時は解消した。しかし別の日にさらに別のテストを書いた際、**エントリスクリプト自身の中で`GameState.selected_weapon_index = 4`のようにautoloadをbareな識別子で直接参照した**ところ、`_initialize()`の中に書いていたにもかかわらず同じ`SCRIPT ERROR: Compile Error: Identifier not found: GameState`が再発した(今度はexit codeも0のまま何も実行されず、フォールバックも効かなかった)。

## わかったこと・今の対応

Godotのスクリプトコンパイルには、性質の異なる2種類のグローバル識別子解決がある:
- `class_name`で宣言されたグローバルクラス(例: `Enemy`, `Weapon`)は、`.godot/global_script_class_cache.cfg`(プロジェクトの初回インポートで構築される)経由で早期に解決できるため、`--script`のエントリスクリプトから直接`Weapon.new()`のように書いても問題ない。
- autoload(`project.godot`の`[autoload]`セクションで登録されるシングルトン、例: `GameState`)は、実際のエンジン起動シーケンスの中でautoloadノードがルート以下に追加されるタイミングでのみ解決できる識別子で、これは`_init()`(スクリプトのコンストラクタ、エンジン初期化のかなり早い段階で呼ばれる)より後、`_initialize()`(SceneTreeのライフサイクルフック)より前後どちらか際どいタイミングになる。

重要なのは、**「autoloadを参照する識別子が、どのスクリプトのどこに書かれているか」で挙動が変わる**という点:
1. **別スクリプトの中**(例: `enemy.gd`内の`GameState`参照)を`load()`/`preload()`で読み込む場合: その別スクリプトの実際のコンパイルは`load()`が呼ばれた時点まで遅延されるため、`load()`を呼ぶ場所を`_init()`から`_initialize()`に移すだけで解決する。
2. **エントリスクリプト自身の中**にbareなautoload識別子を直接書く場合(`_initialize()`の中に書いていても): エントリスクリプト自体は`--script`実行時に「クラス全体を1つの単位」としてまるごとコンパイルされ、これはどのライフサイクルメソッドが実際に呼ばれるより前に完了する必要がある。そのため`_initialize()`の中に書いても手遅れで、コンパイル自体が失敗する。

対策:
- 別スクリプトを`load()`する場合は、その`load()`呼び出しを`_init()`ではなく`_initialize()`の中に置く。
- エントリスクリプト自身の中でautoloadの値を読み書きしたい場合は、bareな識別子(`GameState.foo`)ではなく、`root.get_node("GameState").foo`のような実行時の動的参照にする(`SceneTree.root`はautoloadノードが追加されている実際のルートノードを指すため、これはいつ呼んでも安全)。

## 詳しい経緯

このプロジェクトでは、`.orchestrator/`配下に`--headless --script`で実行するヘッドレステスト(GDScriptの純粋関数の回帰テスト)を複数追加する作業を行っており、Smoke Test(fail_patternsとして`"SCRIPT ERROR:"`等の文字列を出力からスキャンする方式)がこの2つのパターンをどちらも正しく検知して停止させた——1つ目は自動化パイプラインの実行中(そのままでは動くには動いたが偽陽性ノイズが出ていたため後で手直し)、2つ目は実際にテストの実行自体が失敗する形で。いずれもGodotエンジン自体のバグではなく、テスト対象のコード(`enemy_boss.gd`, `inventory_panel.gd`)側の問題でもない——ヘッドレステストのハーネス(エントリスクリプト)の書き方の問題だった。

## まだ確認できていないこと

- `_initialize()`より後、かつ`_process()`より前の、より正確なautoload登録完了タイミング(Godotエンジン内部の正確なコード経路)までは未調査
- Godot 4.6以外のバージョンでも同じ挙動か未確認
- `Engine.get_singleton()`など他のアクセス方法でも同様に安全か(`root.get_node()`以外の代替手段)は未検証
