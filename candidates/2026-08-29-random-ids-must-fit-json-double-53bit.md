# [候補] 乱数ベースの永続ID(int)は、JSON保存・通信を挟むなら53bit以内に収める(倍精度doubleで正確に往復できる範囲に設計する)

status: candidate
observed_count: 1
observed_in: [dotgameinisie]
tags: [serialization, json, game-dev]
date: 2026-08-29

## 何が起きたか

アイテムの永続個体ID(instance_id)を導入する際、「袋・装備・倉庫・地面・セーブ(JSON)・ネットワーク通信のすべてで同じIDを使う」仕様にした。IDは衝突回避のため乱数合成のintにしたかったが、GodotのJSONは数値をdoubleとして扱うため、64bit intをそのまま使うと保存→ロードでIDが化ける(下位bitが落ちる)恐れがあった。

## わかったこと・今の対応

IDの採番を最初から**53bit未満に収まる構成**で設計した(乱数30bit + マイクロ秒下位10bit + 連番10bit + 識別用の1bit = 51bit)。

```gdscript
static func new_instance_id() -> int:
    _uid_serial += 1
    return ((randi() & 0x3FFFFFFF) << 20) | ((Time.get_ticks_usec() & 0x3FF) << 10) \
        | (_uid_serial & 0x3FF) | (1 << 50)
```

倍精度doubleは整数を2^53まで正確に表現できるので、この範囲ならJSON.stringify→parse_stringの往復でも、ネットワークのDictionaryペイロードでもIDが変化しない。実際にセーブ往復・通信往復でID集合が完全一致することをテストで確認した(ITEM_UID_TEST)。

一般則: 「一意なID」を作るとき、経路のどこかにJSON・JavaScript・doubleベースのシリアライズが挟まるなら、**64bitフルの乱数IDは最初から使わない**。53bit制約は言語をまたいで頻出する(JSの`Number.MAX_SAFE_INTEGER`と同じ話)。後からIDが化けると「複製・消失」として現れ、原因がシリアライズ層だと気づきにくい。

## 詳しい経緯

灰灯の迷宮のBU13で、アイテム操作を「要求→ホスト検証→確定→全peer反映」のtransactionへ統一する際に導入。曖昧照合(テンプレートID+レア度一致)を廃止して個体ID一致に置き換えるため、IDが1bitでも化けると装備の複製/消失に直結する。設計時点で53bit制約を織り込んだため、実装後の往復テスト(生成300個の一意性・to_net往復・セーブ往復・操作400手の保存則)は一発で通った。

## まだ確認できていないこと

- 51bit中の乱数実効量(30bit+時刻10bit)での実運用衝突率の長期観測(理論上は端末2台×数千個で実用上問題ない見積り)
- Godot以外のエンジン/言語のJSON実装でint64をそのまま保持するものとの相互運用(今回は同一エンジン間のみ)
