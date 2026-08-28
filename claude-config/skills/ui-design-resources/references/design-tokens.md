# design tokens の統一ルール

> design tokens = 色や余白などの値に名前を付けて1か所にまとめたもの。
> `#3b82f6` と直接書く代わりに `--color-primary` と書く。値を1か所変えれば全体に反映される。

**プロジェクトに既存のトークンがあれば、それが唯一の正解。** ここに書いてある値で上書きしない。
無いときだけ、以下を出発点として最小限を定義する。

共通の原則: **段階の数を絞る。** 選択肢が多いほどバラつく。
「足りなければ足す」であって、「とりあえず全部定義しておく」ではない。

---

## 色

セマンティックな名前(役割の名前)を付ける。`blue-500` ではなく `primary` にする。
役割で名前を付けておくと、後からブランドカラーを変えるときに1か所で済み、ダークモード対応も同じ仕組みで書ける。

最小セット(shadcn/ui の命名に合わせておくと、shadcn 由来の部品がそのまま動く):

| トークン | 役割 |
|---|---|
| `background` / `foreground` | ページの地の色 / その上の文字色 |
| `card` / `card-foreground` | カード等の面 / その上の文字色 |
| `primary` / `primary-foreground` | 主要アクション(主ボタン等) / その上の文字色 |
| `secondary` / `secondary-foreground` | 副次的なアクション |
| `muted` / `muted-foreground` | 控えめな背景 / 補助テキスト |
| `accent` / `accent-foreground` | ホバー時の背景など |
| `destructive` / `destructive-foreground` | 削除など危険な操作 |
| `border` / `input` / `ring` | 境界線 / 入力欄の枠 / フォーカスリング |

必ず `xxx` と `xxx-foreground` をペアで定義する。背景色だけ決めて文字色を決めないと、
組み合わせによって読めないコントラストが生まれるため。

コントラスト比は本文 4.5:1 以上、大きい文字・UI部品の境界は 3:1 以上を確保する(WCAG AA)。

## 余白(spacing)

**4px グリッド**に乗せる。使う値は `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64`(px)。
Tailwind のデフォルトの spacing スケール(`1`=4px, `2`=8px, `3`=12px, `4`=16px, `6`=24px,
`8`=32px, `12`=48px, `16`=64px)がそのままこれなので、Tailwind なら追加定義は不要。

`p-[13px]` のような任意の値を書き始めた時点でルールが壊れる。既存の段階から選ぶ。

関連する要素どうしは近く、無関係な要素とは遠く配置する(近接の原則)。
見出しとその本文の間隔より、セクションどうしの間隔を明確に大きくする。

## タイポグラフィ

- **フォントは2種類まで**(見出し用 + 本文用)。1種類でも成立する
- **サイズの段階は5〜6個に絞る。** 例: `12 / 14 / 16 / 20 / 24 / 32`(px)
  Tailwind なら `text-xs / text-sm / text-base / text-lg / text-2xl / text-3xl`
- 本文の行間(line-height)は 1.5 前後、見出しは 1.2 前後。文字が大きいほど行間は詰める
- ウェイトは3種類まで。例: `400`(本文) / `500`(強調) / `700`(見出し)
- 本文の1行は 45〜75文字程度に収める(`max-w-prose` 等)。長すぎると目が行を追えなくなる

## 角丸(radius)

**基準値を1つ決めて、そこから派生させる。** これが揃っていないのが「寄せ集め感」の主犯になりやすい。

```
--radius: 0.5rem;            /* 基準 */
--radius-sm: calc(var(--radius) - 4px);
--radius-md: calc(var(--radius) - 2px);
--radius-lg: var(--radius);
```

外側の要素の角丸は、内側の要素より大きくする(カードの中のボタンはカードより小さい角丸)。
逆にすると入れ子の境界が不自然に見える。

## シャドウ(elevation)

**3段階まで。** 例: `sm`(境界の補助) / `md`(カード・ドロップダウン) / `lg`(モーダル)。
段階が多いと「どれが手前か」の情報が伝わらなくなる。影は浮いている高さを表す情報なので、
装飾として増やさない。

## モーション

| トークン | 値 | 用途 |
|---|---|---|
| `duration-fast` | 150ms | ホバー、色の変化 |
| `duration-base` | 200ms | 小さい要素の開閉 |
| `duration-slow` | 300ms | モーダル、ドロワーなど大きい要素 |

- 入場は `ease-out`、退場は `ease-in`
- 動かすのは `transform` と `opacity` を基本にする(`width` / `top` などはカクつきの原因になりやすい)
- `prefers-reduced-motion: reduce` のとき、動きを止める記述を必ず入れる

---

## 書き方の例

### Tailwind v4(`@theme` を使う場合)

```css
/* globals.css */
@import "tailwindcss";

@theme {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.15 0 0);
  --color-primary: oklch(0.55 0.2 260);
  --color-primary-foreground: oklch(0.99 0 0);
  --color-border: oklch(0.9 0 0);

  --radius: 0.5rem;
}
```

### Tailwind v3(`tailwind.config` を使う場合)

CSS変数で値を持ち、config から参照する。この2段構えにするとダークモードを
`:root` と `.dark` の変数の切り替えだけで実現できる。

```css
:root {
  --background: 0 0% 100%;
  --foreground: 0 0% 9%;
  --primary: 260 80% 55%;
  --primary-foreground: 0 0% 99%;
  --radius: 0.5rem;
}
.dark {
  --background: 0 0% 9%;
  --foreground: 0 0% 98%;
}
```

```js
// tailwind.config.js
theme: {
  extend: {
    colors: {
      background: 'hsl(var(--background))',
      foreground: 'hsl(var(--foreground))',
      primary: {
        DEFAULT: 'hsl(var(--primary))',
        foreground: 'hsl(var(--primary-foreground))',
      },
    },
    borderRadius: {
      lg: 'var(--radius)',
      md: 'calc(var(--radius) - 2px)',
      sm: 'calc(var(--radius) - 4px)',
    },
  },
}
```

### 素のCSS

```css
:root {
  --color-bg: #ffffff;
  --color-fg: #171717;
  --color-primary: #4f46e5;
  --space-2: 8px;
  --space-4: 16px;
  --radius: 8px;
  --duration-base: 200ms;
}
```

---

## 取り込んだ部品を書き換えるときのチェック

外部から持ってきたコードに以下が残っていたら、統合が終わっていない:

- [ ] `#` から始まる色コード、`rgb(...)`、`hsl(...)` の直書き
- [ ] `p-[13px]` / `gap-[7px]` のような角括弧の任意値
- [ ] `rounded-[10px]` のような角丸の直書き
- [ ] `duration-[450ms]` のような時間の直書き
- [ ] そのライブラリ独自のフォント指定
