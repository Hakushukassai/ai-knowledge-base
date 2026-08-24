# [候補] 外部Skill `godot-code-gen` を試験導入

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [godot, ゲーム開発, external-skill]
date: 2026-08-24
source: external
source_url: https://github.com/alexmeckes/godot-claude-skills

## 何が起きたか
外部Skillマーケットプレイス由来のGDScript生成支援Skill(`godot-claude-skills`リポジトリの`godot-code-gen`)を、`~/.claude/skills/godot-code-gen/`として試験導入した。

## わかったこと・今の対応
元のSKILL.mdにはこのシステムが要求するフロントマター(`name`/`description`)が無かったため、既存Skillの慣習(強めのトリガー表現)に合わせて追加した。機密情報スキャンには引っかからないことを確認済み(`godot-code-gen/SKILL.md`単体をスキャンし異常なし)。実際にRESODIVE等での作業で発動し役立つかはまだ未検証。

## 詳しい経緯
`外部Skill導入_引き継ぎ.md`の推奨に従い、まず1件のみを試験導入する方針とした。取得はユーザー自身が`git clone`で実行している(Claude Codeは外部リポジトリのダウンロードを自ら実行しない設計のため)。内容はGodot 4.xのGDScript構文(型ヒント・アノテーション・シグナル・ステートマシン・Resourceパターン・Tween等)のベストプラクティス集で、既存の`godot-optimization`(大量インスタンス最適化)とは話題が異なり衝突しない。ただし`CharacterBody2D/3D`移動のサンプルコード自体には「50体以上の量産時はMultiMeshInstance3Dを検討」という`godot-optimization`側の知見は含まれていないため、両方のSkillを踏まえた判断が必要な場面があることは留意点として残る。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。実際に使ってみて役立った場合は、他の気づきと同じ通常フロー(このファイルへの再観測記録、または`/kb-endorse`)で昇格を検討する。

## まだ確認できていないこと
- 実際の会話でdescriptionの内容に合致した場面で正しく自動発動するか(同一会話中に作成したSkillはその会話では認識されないため、次回セッションでの確認が必要)
- RESODIVEでの実作業での有用性
