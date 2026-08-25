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
元のSKILL.mdにはこのシステムが要求するフロントマター(`name`/`description`)が無かったため、既存Skillの慣習(強めのトリガー表現)に合わせて追加した。機密情報スキャンには引っかからないことを確認済み(`godot-code-gen/SKILL.md`単体をスキャンし異常なし)。設置直後の同一会話内で「プレイヤーキャラクターの待機・歩行・ジャンプのステートマシン」という自然な相談を投げたところ、明示指定なしで正しく自動発動し、実用的な実装例を生成できた(2026-08-24)。RESODIVEでの実作業での有用性はまだ未検証。

## 詳しい経緯
`外部Skill導入_引き継ぎ.md`の推奨に従い、まず1件のみを試験導入する方針とした。取得はユーザー自身が`git clone`で実行している(Claude Codeは外部リポジトリのダウンロードを自ら実行しない設計のため)。内容はGodot 4.xのGDScript構文(型ヒント・アノテーション・シグナル・ステートマシン・Resourceパターン・Tween等)のベストプラクティス集で、既存の`godot-optimization`(大量インスタンス最適化)とは話題が異なり衝突しない。ただし`CharacterBody2D/3D`移動のサンプルコード自体には「50体以上の量産時はMultiMeshInstance3Dを検討」という`godot-optimization`側の知見は含まれていないため、両方のSkillを踏まえた判断が必要な場面があることは留意点として残る。

設置直後の発動テストでは、`SKILL-PROMOTION-GUIDE.md`に記載の「同一会話中に作ったSkillはその会話では認識されない」という制約は再現しなかった(むしろ設置直後から利用可能だった)。環境やタイミングによって挙動が変わる可能性があるため、今後Skillを追加する際は都度確認すること。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。実際に使ってみて役立った場合は、他の気づきと同じ通常フロー(このファイルへの再観測記録、または`/kb-endorse`)で昇格を検討する。

## まだ確認できていないこと
- RESODIVEでの実作業での有用性(発動確認自体はknowledge-baseのセッション内で完了)
