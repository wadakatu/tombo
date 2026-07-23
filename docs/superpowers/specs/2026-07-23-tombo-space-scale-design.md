# TOMBO space scale + `.tombo-flow` — 設計 (2026-07-23)

## 背景・目的

TOMBO は憲法 §1「すべてを測る」/ §6「その場サイズ禁止」を掲げるが、**spacing だけは未計測**のまま出荷されている。実測すると:

- **tombo.css 自身はブロック間の縦リズムを持たない。** margin/padding/gap の直接宣言はコンポーネント**内部** padding のみ。ブロック同士の間隔は 4 つの example が各自 `<style>` で手打ち（計 53 宣言）。共有する utility も token も無い。
- **example の spacing 語彙は約 19 個に発散**: 4,8,10,12,14,16,18,20,22,24,26,28,32,40,48,52,56,64,76。同じ「セクション律動」が 48/52/56/64/76 とバラバラで、spec §7 が謳う 64/96 は実際には守られていない（96 は一度も使われていない）。
- **spec §7 は意図だけ宣言済み**（4px 基準・24px 方眼固定・セクション律動 docs 64 / LP 96）。数値の意図はあるのに token が無い。かつ `.tombo-gutters` は 24px の repeating-gradient で**可視の製図グリッド**を描いている。

**目的:** `--tombo-space-*`（4px 基準の token scale）と `.tombo-flow`（縦リズム utility）を追加し、example の手打ち spacing をそれに移行する。「すべてを測る」を spacing にも及ぼし、本文リズムを可視グリッドに一致させる。

## スコープ

- **今回 (A・純追加/非破壊):** token 追加 + `.tombo-flow` 追加 + 4 example の移行。消費者は opt-in。
- **今回やらない (B・別リリース):** tombo.css の**コンポーネント内部 padding**（5/7/9/11/22/26… の非グリッド値）を scale に正規化する破壊的変更。scale は B でも使える刻みで設計するが、適用は次の独立リリース（v0.8 系の後）に切る。
- **対象外:** forms、`@media print`、`text-autospace`/`palt`（別ロードマップ項目）。

ベストプラクティス根拠: Nathan Curtis「Space in Design Systems」(EightShapes)、Every Layout「Stack」、Andy Bell「Managing Flow and Rhythm with CSS Custom Properties」(24ways)。1 本の scale が inset(padding) と stack(律動) の両方を駆動するのが正、ゆえに A で作る scale を B も使う。

## 設計

### 1. `--tombo-space-*` scale（`@layer tombo.tokens`、px）

4px 基準・**小さい端は密（sub-cell padding 用）／大きい端は 24px グリッド整列（律動用）**・**pixel-encoded 命名**（名前 = 実測値、憲法②「数字とラベルは mono」の計器思想に一致）。

```css
--tombo-space-4:   4px;   /* hairline gap / tight inset */
--tombo-space-8:   8px;   /* chip / row padding */
--tombo-space-12:  12px;  /* button padding-y / tight rhythm */
--tombo-space-16:  16px;  /* callout・code inset / card gap / 本文リズム */
--tombo-space-24:  24px;  /* 方眼 1 セル。既定のブロック律動 */
--tombo-space-32:  32px;  /* medium gap（component 間） */
--tombo-space-48:  48px;  /* 2 セル。sidebar gap / 小セクション */
--tombo-space-72:  72px;  /* 3 セル。セクション律動（docs） */
--tombo-space-96:  96px;  /* 4 セル。セクション律動（LP） */
```

- **9 ステップ**（研究の推奨 8–12 に収まる。純 linear の「近すぎる選択肢過多」を避け、24 以上は幾何的に疎）。
- **24 以上はすべて 24 の倍数**（24/48/72/96）= 可視グリッドに乗る。TOMBO 固有の payoff（本文律動が製図グリッドに一致）。
- **px 単位**（型スケール・tombo.css 全体が px 基準。製図グリッドは絶対寸法で意味を持つ）。
- pixel-encoded の唯一の弱点（値を変えると名前が嘘になる）は、これらが製図グリッドの固定寸法で将来変えない前提のため許容。

### 2. `.tombo-flow`（縦リズム utility、`@layer tombo.utilities`）

Every Layout の Stack / Andy Bell の `.flow` = **owl セレクタ + custom property**。既定はグリッド 1 セル。

```css
.tombo-flow { --tombo-flow-space: var(--tombo-space-24); }
.tombo-flow > * + * { margin-block-start: var(--tombo-flow-space); }
```

- `margin-block-start`（論理プロパティ・**先頭要素に余白が残らない**）。
- 文脈別上書きは cascade で: 見出し前を広げる `h2 { --tombo-flow-space: var(--tombo-space-48); }`、詰めたい本文は `--tombo-space-16` 等。要素側に `--tombo-flow-space` を宣言すると owl が拾う。
- 直接の子のみ（`>`）。ネストした `.tombo-flow` は各自のリズムを持つ。

### 3. `.tombo-flow` と `gap` の使い分け

- **縦に積むコンテンツのリズム** → `.tombo-flow`（sibling margin）。
- **grid / flex のレイアウト gap**（sidebar 列間、button 行、metrics/feature グリッド、footer）→ 直接 token 参照 `gap: var(--tombo-space-*)`。sibling margin ではないので flow の対象外。

## example 移行方針（原則。行単位マッピングは実装計画で確定）

現状値 → 最近接 token に丸める（example は自前資産なので微小なドリフトは許容・むしろリズムが原理化される）:

- **本文リズム**（段落 margin-top 14）→ `--tombo-space-16`（読みの air、ブロック律動 24 より詰める）。
- **ブロック律動**（h3・callout・code・table 前の 24）→ `--tombo-space-24`（`.tombo-flow` 既定）。
- **セクション律動** → docs ≈ `--tombo-space-72`、LP（loud）= `--tombo-space-96`（現状の 52/56/64/76 を整理）。
- **レイアウト gap**: sidebar 56 → `-48`／モバイル折返し 28 → `-24`or`-32`／footer 18 → `-16`／button 行 14 → `-16`／metrics 20 → `-24`／feature 18 → `-16`。
- **微小 gap**: dimlab margin-top 7 → `-8`／brand small 4 → `-4`。

縦に積む本文列には `.tombo-flow` を付け、個別 margin-top を除去。レイアウト gap は token 参照に置換。

## spec §7 更新

- 「基本単位 4px。方眼セル 24px 固定、セクション律動は docs 64px / LP 96px」を、**token が存在する現実**に更新: `--tombo-space-*`（4–96px、24 以上はセル整列）を導入、セクション律動は **docs ≈72px（3 セル）/ LP 96px（4 セル）**、縦リズムは `.tombo-flow` で管理、と記す。旧「64」は 72 へ（グリッド整列のため）。

## README

新設「Space scale」節: token 一覧、`.tombo-flow` の使い方（既定・cascade 上書き・`gap` との使い分け）。既存の container / type scale 節と並ぶ公開 API として文書化。

## リリース

- **v0.8.0**（公開 token + utility class の追加 = 純追加のマイナー）。banner を tombo.css・tombo.js とも v0.8.0 に、README vendoring pin も v0.8.0 に。
- **ローカル ff-merge + lightweight tag v0.8.0 + push**（E と同じ手順。v0.6.0 のマージコミット事故を避けリニア維持）。すべてユーザーゲート。

## 検証

- **contrast gate**: 色に無関係 → PASS（hygiene で実行）。
- **`node --check tombo.js`**: banner のみ変更 → clean。
- **ブラウザ（chrome-devtools・両テーマ）**: 4 example を tombo/hotaru で確認。**example のドリフトは意図的**（リズムの原理化）なので「同一」ではなく「意図通り整っているか」を検証。特に (a) `.tombo-flow` で先頭要素に余分な余白が出ていないこと、(b) セクション律動が 24 グリッドに乗って見えること、(c) レイアウト gap 置換で崩れが無いこと。
- **grep**: example の `<style>` から生の px spacing が消え token/flow 参照に置換されたこと。

## 非対象（follow-up として記録）

- **B**: tombo.css component 内部 padding の scale 正規化（破壊的・次リリース）。
- forms / `@media print` / `text-autospace`（別ロードマップ項目）。
