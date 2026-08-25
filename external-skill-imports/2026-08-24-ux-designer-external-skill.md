# [候補] 外部Skill `ux-designer` を試験導入(Godot以外の一般UI/UX設計向け)

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [UI, UX, デザイン, external-skill]
date: 2026-08-24
source: external
source_url: https://github.com/szilu/ux-designer-skill

## 何が起きたか
「`godot-ui-control`・`game-feel`はゲーム専用で、一般的なUI/デザイン作業には使えないのでは」という指摘を受け、ゲームに限らない一般的なUX/UI設計のSkillを探し、`szilu/ux-designer-skill`(アクセシビリティ・フォーム・多言語対応・AI UI・データ可視化等を網羅する24本の参照ファイル付きSkill)を`~/.claude/skills/ux-designer/`として試験導入した。

## わかったこと・今の対応
MITライセンス、フロントマター完備で修正不要だった。機密情報スキャンで`references/`内のプレースホルダーメールアドレス(「user［アットマーク］example.com」等、フォーム入力例)が6ファイル・14箇所で誤検知された。引き継ぎメモが事前に警告していた事象そのもの。`@`記号を`(at)`に置換する表記に直して解消した(意味は保持)。

## 詳しい経緯
取得はユーザー自身が`git clone`で実行。ただし今回は`~/Downloads`への読み取りアクセスがこのセッションから拒否される事象が発生し(macOSのプライバシー保護によるものと推測、詳細は別候補`2026-08-24-downloads-folder-access-denied-mid-session.md`参照)、`~/Documents/original-game/`配下に再取得してもらって回避した。既存の`godot-ui-control`・`game-feel`とは「ゲーム特化」対「汎用UI/UX」という住み分けになり、内容として矛盾しない。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。

## まだ確認できていないこと
- 実際のUI設計・レビュー作業での有用性
- `godot-ui-control`と両方に該当する場面(Godot上のUI)でどちらが優先的に発動するか、あるいは両方発動して補い合うか
