---
description: 会話を終了せずに、今すぐ知識ベースへの書き出しとGitHubへのpushを実行する
---
セッションを終了せず、今すぐ以下を順番に実行して。終わったら会話はそのまま続ける。

1. このセッションの内容を、現在のプロジェクトディレクトリの HANDOFF.md に knowledge-base/HANDOFF-TEMPLATE.md の形式で書き出す(上書きではなく追記)。既存のHANDOFF.mdが無ければ新規作成する。

2. この会話で、他プロジェクトでも再利用できそうな技術的発見(バグの直し方・設計判断・ライブラリの癖など)があれば、まず knowledge-base/candidates/*.md を確認し、内容的に同じ発見を指す既存ファイルが無いか探す。既存ファイルに同じ発見があれば、そのファイルの observed_count を1増やし、observed_in に今回のプロジェクト名が無ければ追加し、「## 詳しい経緯」の末尾に「(YYYY-MM-DD、プロジェクト名で再確認)」と追記する(新規ファイルは作らない)。既存ファイルに無ければ、knowledge-base/candidates/ に YYYY-MM-DD-短い説明.md というファイル名で新規作成する。フォーマットは status: candidate / observed_count: 1 / observed_in: [プロジェクト名] / tags: [関連する技術領域やジャンルを1〜3個] / date、に続けて本文は「## 何が起きたか」「## わかったこと・今の対応」「## 詳しい経緯」「## まだ確認できていないこと」の見出し構成。再利用性のある発見が無ければこの手順はスキップする。

3. knowledge-base/candidates/ の中の全ファイルを読み、以下のいずれかに該当する候補があれば knowledge-base/PROMOTION-SUGGESTIONS.md に昇格の提案を追記する: (1) 内容的に同じ発見が異なるプロジェクト(observed_inが異なる)にまたがって複数存在する、(2) 1件の observed_count が3以上、(3) 1件に endorsed: true が付いている。該当ごとに『## 候補: ファイル名』の見出し・該当理由・昇格前チェックリスト(3件目が出ても驚かないほど一般的か/プロジェクトごとの前提条件の違いが大きすぎないか/「いつ・何をすべきか」を一言で言えるか)を追記する(既存内容は消さず追記、重複追加はしない)。該当が無ければ何もしない。

4. knowledge-base/candidates/ の中の全ファイルを読み、observed_inが同じ・重なっているのに内容的に同じ発見を指す別ファイルが無いか探す(異なるプロジェクトの組み合わせは手順3の対象なのでここでは扱わない)。該当すれば knowledge-base/MERGE-SUGGESTIONS.md に『## 統合候補: ファイルA と ファイルB』の見出し・理由・統合の提案を追記する(既存内容は消さず追記、重複追加はしない)。該当が無ければ何もしない。

5. この会話中にSkillが使われていたか ~/knowledge-base/.skill_usage.log の末尾を確認する。使われていたSkillがあれば、会話の流れから実際に役立ったかを有効・微妙・不明で判定し、~/knowledge-base/.skill_effectiveness.log に1行(日時・Skill名・判定・理由の4項目をタブ区切りで)追記する。使われていなければ何もしない。

6. この会話中に knowledge-base/rules/ や knowledge-base/candidates/ の内容を(Skillとしての自動発動以外で)実際に参照・活用した場面があったか振り返る。あれば ~/knowledge-base/.reference_usage.log に1行(日時・カテゴリ・ファイル名・判定(役立った/参考程度/不明)・理由の5項目をタブ区切りで)追記する。無ければ何もしない。

7. Bashツールで以下を順番に実行する:
   - python3 ~/.claude/hooks/archive_stale_candidates.py
   - bash ~/knowledge-base/scripts/generate_stats.sh
   - mkdir -p ~/knowledge-base/claude-config/skills ~/knowledge-base/claude-config/hooks && cp ~/.claude/settings.json ~/knowledge-base/claude-config/settings.json && rm -rf ~/knowledge-base/claude-config/skills/* && cp -r ~/.claude/skills/* ~/knowledge-base/claude-config/skills/ && cp -r ~/.claude/hooks/* ~/knowledge-base/claude-config/hooks/
   - python3 ~/.claude/hooks/scan_and_push.py

すべて終わったら「知識ベースに反映してpushしました」と一言だけ報告する。
