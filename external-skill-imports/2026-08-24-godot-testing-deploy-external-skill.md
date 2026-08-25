# [候補] 外部Skill `godot-testing-deploy`(元名`godot`)を試験導入

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [godot, ゲーム開発, テスト, CI/CD, external-skill]
date: 2026-08-24
source: external
source_url: https://github.com/Randroids-Dojo/Godot-Claude-Skills

## 何が起きたか
`外部Skill導入_引き継ぎ.md`の次点候補、`Randroids-Dojo/Godot-Claude-Skills`(GdUnit4テスト・PlayGodotによるE2E自動化・エクスポート・CI/CD・Vercel等へのデプロイ)を`~/.claude/skills/godot-testing-deploy/`として試験導入した。

## わかったこと・今の対応
これまでの3件と異なり、4本のPythonスクリプト(`run_tests.py`/`parse_results.py`/`validate_project.py`/`export_build.py`)が同梱されていたため、実行可能コードとして通常より丁寧にレビューした。内容はいずれも`subprocess`でGodot CLIを呼び出すだけの素直な実装で、ネットワーク通信・`eval`/`exec`・難読化・認証情報の収集など不審な処理は見当たらなかった。機密情報スキャンもフォルダ全体でクリーン。

元のfrontmatterは`name: godot`という汎用的すぎる名前だったため、`godot-testing-deploy`にリネームして配置した(内容は変更なし)。

## 詳しい経緯
取得はユーザー自身が`git clone`で実行。PlayGodot部分は`Randroids-Dojo/godot`のカスタムフォーク(automationブランチ)をソースからビルドする必要があり、GdUnit4テスト単体より導入コストが高い(このリポジトリが引き継ぎメモで「次点」扱いだった理由と合致)。既存の4件のSkillとは話題が重複しない(実装ではなくテスト・ビルド・デプロイが対象)。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。

## まだ確認できていないこと
- 実際にGdUnit4やPlayGodotをRESODIVE等に導入して使う場面での有用性(現時点では設置のみ)
- PlayGodot用カスタムGodotフォークのビルドは未実施(重量級の追加セットアップが必要なため、GdUnit4部分から先に試すのが現実的)
