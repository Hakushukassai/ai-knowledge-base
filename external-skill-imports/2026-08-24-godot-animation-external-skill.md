# [候補] 外部Skill `godot-animation` を試験導入

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [godot, ゲーム開発, external-skill]
date: 2026-08-24
source: external
source_url: https://github.com/gamedev-skills/awesome-gamedev-agent-skills

## 何が起きたか
`外部Skill導入_引き継ぎ.md`の次点候補、`awesome-gamedev-agent-skills`リポジトリの`godot-animation`(AnimationPlayer/AnimationTree/Tweenの使い分け)を`~/.claude/skills/godot-animation/`として試験導入した。`game-feel`・`godot-ui-control`と同じリポジトリから取得済みだったため、追加のcloneは不要だった。

## わかったこと・今の対応
`game-feel`・`godot-ui-control`と同様、フロントマター完備・機密情報スキャンともクリーン。`references/animation-tree-and-tween.md`をあわせて配置。既存の`godot-optimization`・`godot-code-gen`・`game-feel`・`godot-ui-control`のいずれとも話題が重複しない(アニメーション実装そのものに特化)。

## 詳しい経緯
取得はユーザー自身が`git clone`で実行済みの`awesome-gamedev-agent-skills`から。SKILL.md内で`godot-2d-movement`・`godot-3d-essentials`・`game-ai`など、同リポジトリの未導入の他Skillへの言及がある(`game-feel`・`godot-ui-control`と同様の留意点)。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。

## まだ確認できていないこと
- 実際のアニメーション実装作業(RESODIVE等)での有用性
