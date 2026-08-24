# AI開発ナレッジベース

複数のプロジェクト(Godotゲーム開発、画像処理、その他)をまたいで、
AIとの作業で得た知見を「候補→確定ルール→Skill」の3段階で蓄積し、
新しいセッションのたびに自動で読み込ませる仕組み。

## ディレクトリ構成

```
knowledge-base/
  rules/            確定ルール(2つ以上のプロジェクトで確認済み)
  candidates/       候補(1回だけ観測された仮説)
  incidents/        事例ログ(具体的なトラブルの記録)
  docs/             知識ベースを見るためのビジュアライザ(index.htmlをダブルクリック、またはGitHub Pagesで公開)
  scripts/          docsの数字を更新するスクリプト
  claude-config/    別のパソコンにセットアップするための設定コピー(自動更新される)
  PRIVACY-CHECKLIST.md     機密情報の定期確認手順
  SKILL-PROMOTION-GUIDE.md ルール→Skill化の手順
  HANDOFF-TEMPLATE.md      セッション引き継ぎメモの雛形
```

## 全体の流れ

```
作業する
  → 気づきを得る
  → candidates/ に仮説として自動記録(同じ発見が既にあれば新規作成せず証拠を積み増す)
  → 昇格条件(下記)のいずれかを満たす
  → PROMOTION-SUGGESTIONS.md に昇格提案が自動で出る(内容を理解した上での判断)
  → 手動で rules/ に昇格
  → Skill化して ~/.claude/skills/ に配置
  → 次からは関連する作業の時だけ自動で使われる
```

## 自動化の仕組み(hooks)

`~/.claude/settings.json` に設定されている。

| タイミング | 役割 |
|---|---|
| SessionStart | `rules/` の中身と、昇格提案があれば読み込ませる |
| SessionEnd(`/clear`時) | HANDOFF.md生成 → 候補の自動記録(証拠の積み増し含む) → 昇格提案・統合提案の判定 → 参照実績の記録 → dashboard更新 → `claude-config/`の同期 → Gitへの自動コミット |
| PostToolUse(Skillの利用時) | どのSkillが何回使われたかを記録 |

## 知識の昇格ルール(質のコントロール)

`candidates/` → `rules/` への昇格は意図的に自動化していない。
理由は、判断を全自動に任せると質の低い思いつきまでルール化されてしまうため。

以下のいずれかの証拠が揃うと、`PROMOTION-SUGGESTIONS.md` に昇格提案が出る(提案が出るだけで、`rules/`への移動は必ず人が行う):

- 最低2つの異なるプロジェクトで同じパターンが観測された(`observed_in`)
- 同じプロジェクト内で3回以上繰り返し観測された(`observed_count`)
- `/kb-endorse` で人が内容を確認済みとしてマークした(`endorsed: true`)

「別プロジェクトでの偶然の一致」だけに昇格条件を頼ると、Claude Code自体の癖のように
そもそも他分野のプロジェクトでは再現しにくい発見が永遠に昇格できなくなる。
上の3つはどれか1つで足りるOR条件にすることで、この抜け道をふさいでいる。

同じ発見を指す候補が別ファイルに分かれてしまった場合は `MERGE-SUGGESTIONS.md` に
統合の提案が自動で出る。また、`rules/`・`candidates/`が後のセッションで実際に
参照・活用されると `.reference_usage.log` に記録され、参照実績のある候補は
90日ルールでのアーカイブから除外される(使われているものを優先的に残す)。

## 別のパソコンでのセットアップ

`claude-config/SETUP.md` を参照。

## 定期メンテナンス

- 月1回: `PRIVACY-CHECKLIST.md` に沿って機密情報が紛れていないか確認
- 月1回(上記と同じタイミングでまとめて): `candidates/` を一通り眺めて、
  昇格できそうなものがないか検討する。`PROMOTION-SUGGESTIONS.md` は
  同じ発見が複数プロジェクトで見つかった時だけ自動で出るため、それ以外の
  候補は自分で見に行かないと埋もれたままになる
- 気づいた時: `PROMOTION-SUGGESTIONS.md` を見て、昇格を検討
- 気づいた時: `MERGE-SUGGESTIONS.md` を見て、同じ発見を指す候補が
  分かれていないか確認・統合する
- `~/knowledge-base/SYNC-CONFLICT.md` が存在する場合: 複数PC間の自動pushが
  競合して止まっているので、ファイル内の手順に従って手動で解決する
