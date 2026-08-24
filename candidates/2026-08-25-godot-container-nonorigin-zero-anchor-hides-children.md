# [候補] Godot: Container(VBoxContainerなど)に非原点のゼロサイズアンカーを直接設定すると、中身が最小サイズを持っていても描画されない

status: candidate
observed_count: 1
observed_in: [resodive]
tags: [godot, ui, control]
date: 2026-08-25

## 何が起きたか
Godot 4のGDScriptで、コードから動的にUIを組み立てる際、「画面下端中央の1点」にメニュー項目群(VBoxContainer)を配置し、項目数に応じて自動で高さが決まるようにしたかった。

```gdscript
var container := VBoxContainer.new()
container.anchor_left = 0.5
container.anchor_right = 0.5
container.anchor_top = 1.0
container.anchor_bottom = 1.0   # 4隅とも同じ点=ゼロサイズアンカー
add_child(container)
container.resized.connect(func():
    container.position = Vector2(-container.size.x * 0.5, -container.size.y - margin)
)
# この後 container に複数のButton相当のControlをadd_child
```

実行すると、ノード自体は存在し(`get_tree()`で辿れる)、`visible=true`にもかかわらず、画面上に中身のボタン群が一切表示されなかった。

## わかったこと・今の対応
Controlは通常、アンカーがゼロサイズ(4隅とも同じ座標)でも、`custom_minimum_size`や(Containerなら)子要素から計算される最小サイズがあればそれを尊重してサイズが確定する……という前提でこのコードを書いたが、実際には**VBoxContainerのようなContainerに、非原点(0,0,0,0以外)のゼロサイズアンカーを直接与えると、中身の最小サイズがあってもサイズが0のまま確定してしまい、結果として子要素も描画上潰れる**(生成場のロジックは通っているのにピクセル上は何も見えない、原因が非常に分かりにくいタイプの不具合)。
一方、同じセッション内で**別の場所(タイトルロゴ)では全く同じ「ゼロサイズアンカー+resizedで再配置」パターンが正しく動いていた**。違いは、動いていた方は「素のControl(ゼロサイズアンカー、位置決めの基準点としてのみ使う)」の**中に**「デフォルトアンカー(0,0,0,0、原点基準)のVBoxContainer」を**さらに1段ネスト**させていた点。原点基準アンカーのControl/Containerは最小サイズに基づいて素直にサイズが確定するため、これなら問題なく動く。
対策: Containerを画面上の任意の1点(原点以外)に配置したい場合、Container自身に直接その非原点アンカーを設定せず、①位置決め専用の素のControl(非原点ゼロサイズアンカー)を作り、②その子として、デフォルトアンカー(0,0,0,0)のContainerを置き、③内側のContainerの`resized`シグナルで自身の`position`を補正する、という二段構成にする。

## 詳しい経緯
ユーザーからの実機スクリーンショットで「タイトルとエンブレムは正しく表示されているのに、その下にあるはずのメニュー項目(3つのテキストボタン)が一切見えない」と報告されて発覚した。ヘッドレス実行では起動時のスクリプトエラーは一切出ておらず(ノードの生成自体は正常に完了していた)、静的な検証だけでは検出できなかった。デバッグprintでボタンの`global_rect`を出力したところ、`visible=true`かつ`size`は`(976, 140)`のような妥当な値を持っていた一方、実際の座標計算を追うと、問題のあったコンテナは「アンカー計算上のサイズが0のまま最小サイズが反映されていない」ことが根本原因だと分かった(同じセッション内の別の不具合調査で、`--headless`実行時はビューポートが実際の解像度ではなく既定の64x64になることも判明しており、絶対座標そのものではなく相対的な計算ロジックの整合性で判断した)。

## まだ確認できていないこと
- 「非原点ゼロサイズアンカー+Container」がなぜ最小サイズを無視するのか、Godotのレイアウトエンジンの正確な内部挙動(ソースコードレベルの根拠)までは確認していない
- HBoxContainer等、VBoxContainer以外のContainerでも同じ現象が起きるかは未検証(構造上同じ基底クラスなので起きると推測されるが未確認)
- Godotエディタ上(.tscnで直接アンカーを設定する場合)でも同じ現象になるか、コードから動的生成した場合特有の問題かは未確認
