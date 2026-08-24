# [候補] 外部Skill `godot-signals-groups`を試験導入

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [godot, アーキテクチャ, external-skill]
date: 2026-08-24
source: external
source_url: https://github.com/gamedev-skills/awesome-gamedev-agent-skills

## 何が起きたか
シグナル(イベント駆動)はGodot開発の土台になる基礎分野として、`awesome-gamedev-agent-skills`リポジトリの`godot-signals-groups`Skillを`EXTERNAL-SKILL-GUIDE.md`の手順に沿って試験導入した。カスタムシグナルの宣言・発行・Callableでの接続(bind/one-shot含む)・グループでの一斉制御・Godot 3.x→4.x移行時のconnect構文の違いをまとめたもの。

## わかったこと・今の対応
`godot-audio`・`godot-physics`と同じリポジトリ由来で、フロントマター完備・参照ファイル1件のみのシンプルな構成。機密情報スキャンも設置元・設置先とも問題なし。Apache-2.0ライセンス。

## 詳しい経緯
`EXTERNAL-SKILL-GUIDE.md`の手順1〜4を実施: (1)スコープ判定→単純なSkill構成で対象内、(2)ユーザーが既に`git clone`済みの同リポジトリから取得、(3)`SKILL.md`内容確認・`scan_secrets.py`実行(問題なし)・同梱`references/signal-patterns.md`も目視確認(コードスニペットのみ、ネットワーク通信やeval等は無し)、(4)`~/.claude/skills/godot-signals-groups/`に配置し再スキャン。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。

## まだ確認できていないこと
- 実際のGodot開発作業での有用性(まだ発動確認前)
