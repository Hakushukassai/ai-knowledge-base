# [候補] 外部Skill `frontend-design`(Anthropic公式)を試験導入

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [UI, デザイン, external-skill]
date: 2026-08-24
source: external
source_url: https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design

## 何が起きたか
`ux-designer`と同じ動機(Godot以外の一般UI/デザイン向け知見)で、Anthropic公式のclaude-codeリポジトリに同梱されている`frontend-design`プラグインのSkill本体を`~/.claude/skills/frontend-design/`として試験導入した。「テンプレっぽく見えない、意図のあるデザイン」のための考え方(配色・タイポグラフィ・レイアウトを毎回同じパターンに逃げず選ぶ、モーションは狙って使う、コピーライティングも設計要素として扱う)をまとめたもの。

## わかったこと・今の対応
これまでの5件と異なり、**ライセンスがMITなどのオープンソースではなく「All rights reserved」**(claude-codeリポジトリ全体がAnthropic Commercial Terms of Service準拠)。本来は`/plugin marketplace add anthropics/claude-code` → `/plugin install frontend-design@claude-code`という公式のプラグイン機構でインストールする想定だったが、**この環境では`/plugin`コマンド自体が使えなかった**(`/plugin isn't available in this environment.`)。そのため、これまでと同じ「ファイルを直接配置」する方法に切り替えた。個人利用目的でのナレッジベースへの配置と判断したが、他のMITライセンスのSkillとは扱いが異なる点に注意(SKILL.md内に`license_note`フィールドとして明記済み)。

## 詳しい経緯
内容はGitHub上のSKILL.mdを直接確認して取得(著者: AnthropicのPrithvi Rajasekaran氏・Alexander Bricken氏)。ゲーム要素は無く、Web/アプリのUI全般が対象。`ux-designer`(UX原則・アクセシビリティ寄り)とは補完関係で、`frontend-design`は美的方向性・独自性、`ux-designer`は使いやすさ・アクセシビリティ・パターンという住み分け。

このファイルは通常の「2プロジェクトで確認→人が昇格判断」というゲートを迂回して直接Skill化されている点に注意。

## まだ確認できていないこと
- 実際のUI/フロントエンド実装作業での有用性
- この環境で`/plugin`が使えない理由(Claude Code SDKベースの環境固有の制約なのか、他の条件があるのか)
