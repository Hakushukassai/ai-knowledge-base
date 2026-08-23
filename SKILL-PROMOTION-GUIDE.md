# ルール → Skill化 の手順

`rules/` にある確定ルールを、実際にClaude Codeが自動で使える「Skill」に変換するときの手順。
2026-08-23に godot-optimization ルールで試作し、正常に動作することを確認済み。

## 事前確認

- 対象のルールが `status: confirmed`(候補ではなく確定済み)であること
- `confirmed_in` に2つ以上のプロジェクトが入っていること(=汎用性がある証拠)

## 置き場所を決める

- **全プロジェクト共通**にすべきもの(今回のGodot最適化のように、複数プロジェクトで再現した一般的な知見)
  → `%USERPROFILE%\.claude\skills\<スキル名>\`
- **特定のプロジェクトでしか通用しない**もの
  → そのプロジェクト自身の `.claude\skills\<スキル名>\`

## 手順

1. `<スキル名>`フォルダを上記のどちらかに作る(kebab-case、例: `godot-optimization`)
2. その中に `SKILL.md` を作成する
   - フロントマター(`---`で囲む部分)に `name` と `description` を書く
   - `description` には「いつ発動すべきか」を具体的かつ強めに書く(発動し忘れを防ぐため)
   - 本文には、ルールの中身(判断基準・理由・具体的な数値・根拠になった事例)を簡潔にまとめる
3. 元のルールファイル(`rules/<ファイル名>.md`)のフロントマターに `skill: <スキル名>` を追記する
   → これでダッシュボード上に「Skill化済み」と表示されるようになる
4. **新しいClaude Codeセッションを開始して**動作確認する(今の会話中に作ったSkillは、今の会話では認識されない)
5. 意図通りに発動するか、関係ない話題で誤発動しないかを確認する
   - うまくいかない場合は `description` を調整する

## 参考にした実例

- ルール: `rules/godot-optimization.md`
- Skill: `%USERPROFILE%\.claude\skills\godot-optimization\SKILL.md`

## Skillを引退させたいとき

古くなった・別のSkillに統合したい・誤発動が多いなどの理由でSkillを
使わなくしたい場合は、Claude Codeに次のように頼む:

「`<スキル名>` のSkillを引退させて」

内部では `python3 ~/.claude/hooks/retire_skill.py <スキル名>` が実行され、
- `~/.claude/skills/<スキル名>/` が `knowledge-base/claude-config/skills-archive/`
  に移動される(削除ではないので中身は残る。Claude Codeは以後自動使用しない)
- 対応する `rules/*.md` に `skill_status: retired` が追記される

ダッシュボードのSkill一覧画面の下部「引退済み」に表示されるようになる。
判断自体(引退させるかどうか)は昇格と同じく人が決めることで、自動化はしない。
