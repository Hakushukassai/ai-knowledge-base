# [候補] Claude CodeのSessionEndフックは`matcher: "clear"`だけだと`/clear`以外で発動しない

status: candidate
observed_count: 1
observed_in: [knowledge-base]
tags: [claude-code, hooks]
date: 2026-08-23

## 何が起きたか
Claude CodeのSessionEndフックに`matcher: "clear"`とだけ書いていたら、ユーザーが`/clear`と入力した時にしか動かなかった。ターミナルを閉じる・Ctrl+Cで終了するといった普段の終わらせ方では、一度も発動していなかった。

## わかったこと・今の対応
`matcher`に`"clear|prompt_input_exit"`のようにパイプ区切りで複数の終了理由を書けば、両方のタイミングで発動するようになる。`matcher`は配列ではなく文字列でなければならない点にも注意が必要(`["clear", "prompt_input_exit"]`という配列指定は設定のバリデーションでエラーになる)。

## 詳しい経緯
SessionEndイベントの`matcher`が取りうる値は`clear`・`resume`・`logout`・`prompt_input_exit`・`other`の5種類。`clear`はユーザーが明示的に`/clear`した場合のみ発動し、ターミナルを閉じる・Ctrl+C・`/exit`はいずれも`prompt_input_exit`に分類される。複数の値を1つのhookエントリで拾いたい場合、PostToolUseのツール名マッチャーで使われる「パイプ区切り(`"Edit|Write"`)」や「カンマ区切り」の記法が、SessionEndの終了理由マッチングでもそのまま使える(公式ドキュメントのmatcherパターン表: 英数字・アンダースコア・ハイフン・スペース・カンマ・パイプのみで構成される値は「完全一致、または`|`か`,`区切りの複数完全一致」として評価される、との記述で確認)。配列形式は`settings.json`の実際のJSONスキーマで`matcher`が`type: string`と定義されているため使えず、保存時にエラーで弾かれる。

## まだ確認できていないこと
- ウィンドウの×ボタン(強制的に閉じる操作)が`prompt_input_exit`扱いになるかは、公式ドキュメントに明記が無く未確認
- VS Code拡張機能上で、チャットパネルだけを閉じた場合とVS Code自体を閉じた場合とで扱いに違いがあるかも未確認
