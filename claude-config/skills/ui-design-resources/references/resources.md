# リソース一覧

フェーズごとの使い分けは SKILL.md 本体を参照。ここは URL とライセンス区分の台帳。

## 1. 部品調達(コンポーネントライブラリ)

npm でインストールするのではなく、**コードをコピーして自分のプロジェクトの一部にする**前提のサイト群。
だから自由に改造できるし、プロジェクトのトークンに合わせて書き換えるのが前提。

| サイト | 特徴 | 優先度 |
|---|---|---|
| ui.shadcn.com | デファクトスタンダード。Tailwind + Radix ベース。アクセシビリティが作り込まれている | **第一候補** |
| beautifului.dev | 装飾性の高い汎用コンポーネント | 補完 |
| beui.dev | 同上 | 補完 |
| rareui.com | 同上 | 補完 |
| reui.io/components | 同上 | 補完 |
| ui-skills.com | 同上 | 補完 |
| coss.com/ui | 同上 | 補完 |
| kinetics.colorion.co | モーション効果。OSSでコピペ前提 | 動きが必要なとき |
| animatedbuttons.colorion.co | アニメーション付きボタン集 | ボタンに動きが欲しいとき |

使い方: 一覧をフェッチ → 要件に合う部品を選ぶ → コードを読んで安全性とライセンスを確認 →
トークンに書き換えて統合。手順の詳細は SKILL.md のフェーズ2。

ライセンス注意: shadcn/ui は MIT。その他は**サイトごとに条件が異なるため、組み込み前に個別確認**する。
商用利用・再配布の可否が読み取れない場合、または有料キット由来と疑われる場合は、統合前にユーザーへ確認する。

## 2. 統一ルール / レビュー

| サイト | 用途 |
|---|---|
| designsystemchecklist.com | 実装後のセルフレビュー用チェックリスト。コンポーネント集ではない |

同伴の `review-checklist.md` に、この観点でのレビュー項目をまとめてある。

## 3. 設計思想のインプット

部品そのものではなく、「なぜこう動くべきか」の判断基準を得るためのソース。実装前に軽く参照する。

| サイト | 内容 |
|---|---|
| transitions.dev | アニメーション / トランジションの実装パターン |
| emilkowal.ski/ui/ | Emil Kowalski(Vercel/shadcn 周辺のアニメーション領域で著名)の思想寄りの記事群 |

## 4. ツール(都度生成系)

| サイト | 用途 | 注意 |
|---|---|---|
| iconcreator.dev | アイコンをその場で生成 | 既存セットに無いものだけ |
| vibeprompts.dev | UIプロンプト集 | コードではなくプロンプト。品質は中身次第、使用前に内容確認 |

## 5. アイコン

### 無料・OSS(優先)

| サイト | 特徴 |
|---|---|
| lucide.dev | shadcn/ui との相性◎。shadcn 系なら基本これ |
| phosphoricons.com | ウェイトのバリエーションが豊富 |
| Heroicons | Tailwind 制作元。Tailwind プロジェクトと馴染む |
| Tabler Icons | 4000点以上、OSS |
| Radix Icons | Radix ベースのプロジェクトなら最も馴染む |
| Iconoir | OSS |

**1プロジェクト1セットが原則。** 線の太さや角の処理がセットごとに違うため、混ぜると並べたとき違和感が出る。

#### lucide のSVGを直接取得する

サイトをフェッチして探すより、CDNから生のSVGを1本ずつ取る方が速い。

```
https://unpkg.com/lucide-static@latest/icons/<アイコン名>.svg
```

例: `.../icons/film.svg`、`.../icons/chevron-down.svg`。
`24x24` / `stroke-width: 2` / `stroke-linecap: round` に統一された状態で返ってくるので、
`stroke="currentColor"` のまま使えば文字色に追従する。ライセンス本文は
`https://unpkg.com/lucide-static@latest/LICENSE` で確認できる(ISC / 一部MIT、商用可・再配布可)。

数が多いときは、SVGスプライト(`<symbol>` にまとめて `<use href="#id">` で参照する方法)にすると
HTML本文が読みやすくなる。

### 商用利用前にライセンス確認が必要

- iconsax.io
- iconly.pro
- hugeicons.com
- nucleoapp.com

**使う前に必ずユーザーに確認を取る。** 確認なしで組み込むと、後からライセンス違反や差し替えコストが発生する。

### ニッチ系(汎用UIには不向き)

- morphicons.com — アイソメトリック(立体的な図法のイラスト)
- isocons.app — アイソメトリック

## 対象外

- invoicegenerator.io — UI/UXデザインの参考にならないため対象外
