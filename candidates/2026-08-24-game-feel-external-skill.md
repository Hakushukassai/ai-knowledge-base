# [候補] 外部Skill `game-feel` を試験導入

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [godot, ゲーム開発, external-skill]
date: 2026-08-24
source: external
source_url: https://github.com/gamedev-skills/awesome-gamedev-agent-skills

## 何が起きたか
`外部Skill導入_引き継ぎ.md`のUI・game feel向け推奨に従い、`awesome-gamedev-agent-skills`リポジトリの`game-feel`(画面シェイク・ヒットストップ・イージング・スクワッシュ&ストレッチ等、動きの気持ちよさに関する知見)を`~/.claude/skills/game-feel/`として試験導入した。

## わかったこと・今の対応
元のSKILL.mdは`godot-code-gen`と異なり、最初から`name`/`description`のフロントマターが揃っており、そのまま配置できた(修正不要)。`references/feedback-recipes.md`という参照ファイルも本体が明示的に読み込む前提のため、あわせて配置した。機密情報スキャンは本体・参照ファイルともクリーン。設置直後にSkill一覧へ即座に反映されることを確認(godot-code-genの時と同様の挙動)。

## 詳しい経緯
取得はユーザー自身が`git clone`で実行。エンジン非依存の設計で、Godot 4.7とUnity 6.3 LTS両方のコード例が併記されている。既存の`godot-optimization`・`godot-code-gen`とは話題が異なり衝突しない。SKILL.md内で`camera-systems`・`audio-design`・`physics-tuning`・`godot-animation`など、同じ元リポジトリの**未導入の他Skill**への言及が複数あるが、それらは今回導入していないため、参照されても実体が無い状態になる(動作は壊れないが、案内通りには追従できない場面がありうる)。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。

## まだ確認できていないこと
- 実際のゲーム開発作業(RESODIVE等)での有用性
- 言及されている未導入の関連Skill(`camera-systems`等)を追加導入すべきか
