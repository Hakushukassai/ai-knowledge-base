# [候補] 外部Skill `game-ai`を試験導入

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [ゲーム開発, AI設計, external-skill]
date: 2026-08-24
source: external
source_url: https://github.com/gamedev-skills/awesome-gamedev-agent-skills

## 何が起きたか
RESODIVE・DEPTH//とも「敵」が中心的な要素であることから、`awesome-gamedev-agent-skills`リポジトリの`game-ai`(discipline系、エンジン非依存)Skillを`EXTERNAL-SKILL-GUIDE.md`の手順に沿って試験導入した。有限状態機械・ビヘイビアツリー・操舵行動(steering)・A*経路探索の使い分けをまとめたもの。

## わかったこと・今の対応
これまでの4件(godot-audio/physics/signals-groups/3d-essentials)は`skills/godot/`配下だったが、今回は`skills/disciplines/`配下のエンジン非依存Skill。フロントマター完備・参照ファイル2件(`behavior-trees.md`・`pathfinding.md`、SKILL.md本文が指す2件とも一致)。機密情報スキャンも設置元・設置先とも問題なし。Apache-2.0ライセンス。

## 詳しい経緯
`EXTERNAL-SKILL-GUIDE.md`の手順1〜4を実施: (1)スコープ判定→単純なSkill構成で対象内、(2)ユーザーが既に`git clone`済みの同リポジトリから取得、(3)`SKILL.md`内容確認・`scan_secrets.py`実行(問題なし)・同梱2つの参照ファイルも目視確認(コードスニペットのみ、ネットワーク通信やeval等は無し)、(4)`~/.claude/skills/game-ai/`に配置し再スキャン。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。

## まだ確認できていないこと
- 実際のGodot開発作業での有用性(まだ発動確認前)
