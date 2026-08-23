# Godot 4 最適化ルール

status: confirmed
promoted_from: candidates/2026-06-multimesh-discovery.md
confirmed_in: [RESODIVE, DEPTH//]
confirmed_count: 2
tags: [godot, ゲーム開発, パフォーマンス最適化]
skill: godot-optimization

## ルール
敵や弾丸など同一メッシュの大量インスタンスは、個別の Node ではなく
MultiMeshInstance3D を使う。個別 Node は 200 体を超えたあたりから
_process のオーバーヘッドで明確にフレームが落ちる。

## 判断基準
- 「同じ見た目のオブジェクトが同時に50体以上存在しうるか」で判定する
- 存在しうるなら最初から MultiMeshInstance3D 設計にする
  (後から個別Node実装を移行するコストの方が高い)

## 根拠になった事例
- incidents/2026-05-resodive-enemy-lag.md
- incidents/2026-06-depth-bullet-lag.md
