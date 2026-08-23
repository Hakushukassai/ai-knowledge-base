# [候補] AudioStreamPlayerのバス切り替えタイミング

status: candidate
observed_count: 1
observed_in: [DEPTH//]
tags: [godot, オーディオ, ゲーム開発]
date: 2026-08-20

## 何が起きたか
シーン切り替えの直前に音声のバス(出力先)を切り替えると、音が一瞬途切れることがある。

## わかったこと・今の対応
シーン切り替えが終わってから切り替えれば発生しない。今のところこの回避策のみで、根本原因(別の現象「OGG/PhaseLoopMusicの音切れ」と同じ原因かどうか)は未確認。

## まだ確認できていないこと
- Polypulseの時にあった「OGG/PhaseLoopMusicの音切れ」と同一原因か未確認
- 他のプロジェクトでも再現するか未確認

## 昇格の条件
別のプロジェクトでも同じ現象が確認されたら rules/ に昇格し、
incidents/ に詳細ログを残す。
