# [事例] DEPTH// 弾丸大量発生時のフレーム低下

date: 2026-06-15
project: DEPTH//
related_rule: rules/godot-optimization.md

## 何が起きたか
雑魚敵を30体以上同時に倒すと、弾丸ノードが同時に150個近く発生し、
フレームレートが60→22まで落ちた。

## 原因
弾丸を個別の RigidBody3D ノードとして生成していたため、
_physics_process のオーバーヘッドが線形に増加していた。

## 解決
MultiMeshInstance3D + 独自の当たり判定計算に置き換え、
150個発生時でも58fps以上を維持できるようになった。

## 汎用化できそうな知見
「同一見た目のインスタンスが50体を超えうる設計」は
最初からMultiMeshInstance3Dを前提にすべき、という判断基準が立った。
→ RESODIVEの敵AI実装(同様の課題)でも同じ判断が有効だった。
→ 2案件で確認されたため rules/godot-optimization.md に昇格。
