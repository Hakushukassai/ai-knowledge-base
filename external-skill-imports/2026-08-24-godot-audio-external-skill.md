# [候補] 外部Skill `godot-audio`を試験導入

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [godot, オーディオ, external-skill]
date: 2026-08-24
source: external
source_url: https://github.com/gamedev-skills/awesome-gamedev-agent-skills

## 何が起きたか
DEPTH//で実際に発生した「シーン切り替え時の音声バス切り替えで音が途切れる」という既存の候補(`2026-08-example-candidate.md`)に関連する分野として、`awesome-gamedev-agent-skills`リポジトリの`godot-audio`Skillを`EXTERNAL-SKILL-GUIDE.md`の手順に沿って試験導入した。AudioStreamPlayerの使い分け・バス経由のルーティング・dB変換・ビート同期などをまとめたもの。

## わかったこと・今の対応
`godot-testing-deploy`等と同じリポジトリ由来で、フロントマター完備・参照ファイル1件のみのシンプルな構成。機密情報スキャンも設置元・設置先とも問題なし。Apache-2.0ライセンスなので、`frontend-design`のような特殊な扱いは不要。

## 詳しい経緯
`EXTERNAL-SKILL-GUIDE.md`の手順1〜4を実施: (1)スコープ判定→単純なSkill構成で対象内、(2)ユーザー自身に`git clone`してもらい取得、(3)`SKILL.md`内容確認・`scan_secrets.py`実行(問題なし)・同梱`references/buses-and-effects.md`も目視確認(コードスニペットのみ、ネットワーク通信やeval等は無し)、(4)`~/.claude/skills/godot-audio/`に配置し再スキャン。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。

## まだ確認できていないこと
- 実際のGodot開発作業での有用性(まだ発動確認前)
- 既存の音声関連の候補(DEPTH//のバス切り替えバグ)との組み合わせで、実際に役立つか
