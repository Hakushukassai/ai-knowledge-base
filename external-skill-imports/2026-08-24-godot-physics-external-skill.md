# [候補] 外部Skill `godot-physics`を試験導入

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [godot, 物理演算, external-skill]
date: 2026-08-24
source: external
source_url: https://github.com/gamedev-skills/awesome-gamedev-agent-skills

## 何が起きたか
RESODIVE・DEPTH//とも敵や弾丸の大量発生・衝突が絡む設計で、既存の`godot-optimization`(MultiMeshInstance3D)と相性が良い分野として、`awesome-gamedev-agent-skills`リポジトリの`godot-physics`Skillを`EXTERNAL-SKILL-GUIDE.md`の手順に沿って試験導入した。RigidBody/StaticBody/Area/CharacterBodyの使い分け・衝突レイヤーとマスク・オーバーラップ検出・レイキャストをまとめたもの。

## わかったこと・今の対応
`godot-audio`と同じリポジトリ由来で、フロントマター完備・参照ファイル1件のみのシンプルな構成。機密情報スキャンも設置元・設置先とも問題なし。Apache-2.0ライセンス。

## 詳しい経緯
`EXTERNAL-SKILL-GUIDE.md`の手順1〜4を実施: (1)スコープ判定→単純なSkill構成で対象内、(2)ユーザーが既に`git clone`済みの同リポジトリから取得、(3)`SKILL.md`内容確認・`scan_secrets.py`実行(問題なし)・同梱`references/bodies-and-queries.md`も目視確認(コードスニペットと表のみ、ネットワーク通信やeval等は無し)、(4)`~/.claude/skills/godot-physics/`に配置し再スキャン。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。

## まだ確認できていないこと
- 実際のGodot開発作業での有用性(まだ発動確認前)
