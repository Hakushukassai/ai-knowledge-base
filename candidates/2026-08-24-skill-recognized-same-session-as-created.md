# [候補] 同一会話中に作成したSkillも、その場で認識・発動することがある

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [claude-code, skill]
date: 2026-08-24

## 何が起きたか
`SKILL-PROMOTION-GUIDE.md`には「新しいClaude Codeセッションを開始して動作確認する(今の会話中に作ったSkillは、今の会話では認識されない)」と書かれていたが、実際に`~/.claude/skills/godot-code-gen/`を作成した直後、同じ会話内でSkill一覧に表示され、関連する相談を投げたところ明示指定なしで正しく自動発動した。

## わかったこと・今の対応
少なくとも今回の環境では、Skillの認識は「次回セッションを待つ必要がある」という従来の想定より早いタイミングで反映されることがある。ただし1回の観測に過ぎないため、常にそうなるのか、特定の条件(ファイル作成のタイミング、既存のSkillの有無など)に依存するのかは不明。Skillを追加した際は「新しいセッションでないと確認できない」と決めつけず、まず同一会話内で発動確認を試すのが早い。

## 詳しい経緯
`external-skill-imports/2026-08-24-godot-code-gen-external-skill.md`として外部Skillを試験導入した際、`~/.claude/skills/godot-code-gen/SKILL.md`をWriteツールで作成した直後のsystem-reminderに「godot-code-gen」がSkill一覧として表示された。半信半疑で同一会話内で関連する相談(GDScriptのステートマシン実装)を投げたところ、Skillツール経由で正しく発動し、内容も適切だった。

## まだ確認できていないこと
- 再現性(別のSkill作成時、別のタイミングでも同様に即時認識されるか)
- `SKILL-PROMOTION-GUIDE.md`の記載がいつの時点の挙動を元にしているか、環境差なのかタイミング差なのか
