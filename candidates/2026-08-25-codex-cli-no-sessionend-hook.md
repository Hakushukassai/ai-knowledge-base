# [候補] Codex CLIには(2026年8月時点で)Claude CodeのSessionEndに相当するフックが無い

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [codex, claude-code, hooks, 移植性]
date: 2026-08-25

## 何が起きたか
Claude Codeの知識ベース自動化(セッション終了時にAI自身が候補記録・HANDOFF更新・git pushまで行う仕組み)を、OpenAIのCodex CLIにも移植できるか調査した。Codexにも2026年に入って似た「フック」機能が追加されていたが、セッション終了のタイミングを捕まえる仕組み(Claude CodeのSessionEnd相当)が無いことが分かった。

## わかったこと・今の対応
CodexのフックにはSessionStart・UserPromptSubmit・PreToolUse・PostToolUse・Stopはあるが、Claude CodeのSessionEnd(`/clear`や終了時に自動発火し、AI自身に「会話を振り返って候補を書き出して」等の指示を出せるもの)に相当するものが無い(2026年8月時点、GitHub上でも追加要望がまだ未実装)。回避策として、セッション終了時の自動化は諦め、ユーザーが会話の最後に明示的に呼び出すSkill(Claude Codeの`/kb-sync`に相当)を用意する形にした。

## 詳しい経緯
Codexは2026年に入ってhooksエンジン(v0.114で初登場、v0.124で安定版)とSkills機能(SKILL.md、暗黙発動対応)を追加しており、読み込み側(セッション開始時にルールを自動で文脈に注入する、Skillを自動発動させる)はClaude Codeとほぼ同等のことができる。一方で書き込み側、特に「セッションが終わったタイミングを検知して、AI自身に振り返りタスクをやらせる」機能は無い。CodexのフックはJSON stdin/stdoutでテキストを注入する薄い仕組みで、Claude Codeの`"type": "prompt"`フックのように独立した1つのエージェントターン(ファイル書き込み・git操作を含む)を自動起動する設計ではない点も異なる。

## まだ確認できていないこと
- Codexの「Stop」イベントが本当に1ターンごとの停止なのか、セッション全体の終了に近いものなのか未検証(前者だと候補記録が毎ターン走ってしまい使えない)
- Stopイベントのフック内から`codex exec "プロンプト"`のように再帰的にCodex自身を非対話呼び出しすることで、Claude Codeの`"type": "prompt"`フックに近いことができるかは未検証
- Codex自体がまだこのマシンに導入されていないため、上記はすべてドキュメント調査に基づく机上の結論で実機未検証
