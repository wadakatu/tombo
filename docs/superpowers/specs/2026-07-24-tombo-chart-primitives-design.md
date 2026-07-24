# TOMBO 図版(チャート)プリミティブ — 設計 (2026-07-24)

Issue: <https://github.com/wadakatu/tombo/issues/15>

## 背景・目的

studio-internal の週次アクティビティページ(`pages/employee/wadakatu/index.html`、TOMBO v0.12.0 を vendor)が棒グラフ 2 枚(日次内訳・週次推移)を実装した際、チャート系の部品が tombo.css に存在せず、図版枠・軸・バー・値ラベル・朱の現在地・ツールチップ・数表の全てがページ側 CSS の手組みになった。

仕様 §4 の S-03 目盛は適用範囲に「箇条書きの点・進捗・**グラフ軸**」を挙げているが、実装は単値の計器(`.tombo-ruler`)止まりで、グラフ軸を組む語彙がない。ダッシュボード/レポート系ページは今後も増えるため、**部品と規範**を tombo.css 側に持たせる。色・太さは既存トークンで全て賄えることが手組みで実証済み — **新トークン・新色は不要**。

**目的:** 消費側がページ CSS ゼロで tombo 流の棒グラフ + ツールチップ + 数表を組めるようにし、チャートの規範(軸は 1 本・単系列は green 一色・値ラベルは選択的・朱は現在地のみ)をコード化する。

## 命名 — `.tombo-fig` は使えない(issue からの変更点)

issue は図版枠を `.tombo-fig` と提案しているが、**`.tombo-fig` は v0.1 から S-04(通し番号)の「図版の銘」**(`FIG. 01 — …` の mono 大文字キャプション、`tombo.css` の components 層)として存在する。studio-internal のページ自身も `.tombo-fig` を銘に、手組みの `.fig` を枠に使い分けており、catalog c05 にも「図版の銘は .tombo-fig」と明文化済み。リネームは breaking かつ既存消費側を壊すので不採用。

**枠は `.tombo-plate` と命名する。** 図版=版(plate)は製版・印刷の語彙で、トンボ/見当/裁ち落とし(`.tombo-trim`)というシステムの語彙系に載る。`.tombo-figure` 案は `.tombo-fig` と一字違いで、まさに本 issue 起票時に起きた混同を誘発するため不採用。`.tombo-chart` 案はチャート専用に見えるが、枠自体は「hairline 罫 + padding + 枠内横スクロール」の図版一般の枠なので不採用。

## スコープ

### 今回やる(純追加・非破壊 = v0.13.0)

- **`.tombo-plate`** — 図版枠: hairline 罫 + padding 24 + `position:relative`(ツールチップの基準)+ 枠内横スクロール。配下の `svg` は幅 100%・`min-inline-size` で最小幅を保証(超えたら枠内スクロール)。
- **SVG チャート内部クラス**(`.tombo-plate` 配下に scoped): `.axis` / `.base` / `.bar`(+`.is-zero`)/ `.val` / `.now` / `text` の既定造形。
- **`.tombo-tip`** — ホバー読み取り用ツールチップの**パネル造形のみ**(surface + ink 罫 + mono note 段)。表示と位置決めは消費側 JS(後述)。
- **`.tombo-numbers`** — 図版に対になる数表開閉(`<details>` + mono label 段の summary)。
- **print 硬化** — `.tombo-plate` を改ページ分割禁止リストへ、`.tombo-tip` を非印刷リストへ追加。
- **example**: components.html カタログに「19 — 図版」節(静的 SVG の実演 + 規範の明文化 + コピペ用スニペット)。
- **README**: 「Charts (図版)」節(クラス一覧 + markup 契約 + 規範)。

### 今回やらない

- **多系列チャートの色分け語彙** — 規範は「単系列は green 一色」。系列を並べたくなったら図を分けるのが tombo 流で、カテゴリカルパレットは設計思想(色は green/shu の 2 役)と衝突するため作らない(YAGNI)。
- **折れ線・円・面グラフ専用の語彙** — `.axis`/`.base`/`.now` は stroke 系なので折れ線にもそのまま使えるが、専用クラス(点・面・凡例)は需要が出るまで作らない。
- **ツールチップの表示・追従 JS** — tombo.js は state-only(テーマ + コピー)の方針([[tombo-direction]])。チャートを SVG で描く消費側には既に JS があり、位置決めだけ tombo.js が持つ意味がない。
- **`.tombo-ruler` の変更** — 単値の計器はそのまま。

## 設計判断

> 本 spec は /goal による自律モードで確定した。open questions(枠名・最小幅・hover)は下記の根拠で自己決定し、ユーザーレビューは spec/実装のレビューで受ける。

1. **枠 = `.tombo-plate`、チャート内部は枠配下の短名クラス。** グローバルな `.bar`/`.axis` は作らず、`.tombo-metric > .k` や `.tombo-logo > .h` と同じ「コンポーネント配下の内部短名」パターンに揃える。手組み版(`.fig .bar`)と同型なので移行も機械的。
2. **`text` 要素は枠配下で一律 mono・label 段・ink-faint。** 憲法②「銘は等幅」— 軸ラベル・目盛値は全て銘。`text` は SVG 専用要素なので要素セレクタで安全に効かせられる。強調したい値ラベルだけ `.val`(ink・600)を付ける。
3. **最小幅は `var(--tombo-plate-min, 560px)`。** viewBox + 幅 100% だけでは SVG が縮み続けて枠内スクロールが発動しない。既定 560px(手組み版の実測値)、上書きは**消費側スタイルシートで**行う(インライン custom property は `--tombo-ruler-value` だけという既存規範を維持)。
4. **`.bar:hover { opacity: .82 }` は既定で入れる。** 手組み版の実装を踏襲。ツールチップ読み取りの合図として機能し、静的な図でホバーしても「薄くなるだけ」で誤アフォーダンスの実害が小さい。
5. **ツールチップはパネルだけ CSS、可視化は消費側 JS。** 既定 `display:none`。`role="presentation"` + `pointer-events:none` の視覚専用チャネルであり、アクセシブルなデータ経路は数表(と bar の `aria-label`)が担う — JS 無しでもデータに到達できる(PE 方針と一致)。
6. **数表 = `.tombo-numbers`(`<details>`)。** チャートの text alternative の置き場。summary は mono label 段・ink-faint(手組み版踏襲)。ネイティブの開閉マーカーは残す(native-first)。中身は既存の `.tombo-table-wrap` + `.tombo-table` を使う。
7. **朱の規範はコードでも守られる。** `.now` は stroke 専用(2px の線)。面塗りの朱クラスは存在しない — 「朱は塗った瞬間に朱でなくなる」(憲法③)。

## 設計(CSS)

`@layer tombo.components` の新ブロックとして、checkbox/radio ブロックの後・print 節の前に追加する。

```css
@layer tombo.components {
  /* 図版 — S-03「グラフ軸」の部品化 (spec 2026-07-24, issue #15)。
     枠 = plate(版)。.tombo-fig(図版の銘)とは別物: 銘は figcaption に載せる。
     チャート内部(.axis/.base/.bar/.val/.now)は枠配下でだけ効く。 */
  .tombo-plate {
    position: relative; /* .tombo-tip の基準 */
    border: 1px solid var(--tombo-hairline);
    padding: var(--tombo-space-24);
    overflow-x: auto; /* 溢れたら枠内だけスクロール(ページは動かさない) */
  }
  /* viewBox だけだと縮み続けてスクロールが発動しない — 最小幅で読み取り可能性を守る。
     上書きは消費側スタイルシートで(インライン custom property は --tombo-ruler-value のみ)。 */
  .tombo-plate svg { inline-size: 100%; block-size: auto; min-inline-size: var(--tombo-plate-min, 560px); }
  .tombo-plate .axis { stroke: var(--tombo-hairline); stroke-width: 1; }   /* 目盛線 */
  .tombo-plate .base { stroke: var(--tombo-ink); stroke-width: 1.5; }      /* 基線 — 軸はこの 1 本 */
  .tombo-plate .now  { stroke: var(--tombo-shu); stroke-width: 2; }        /* 朱の現在地 — 線専用 */
  .tombo-plate .bar  { fill: var(--tombo-green); }                         /* 単系列は green 一色 */
  .tombo-plate .bar.is-zero { fill: var(--tombo-hairline); }               /* ゼロ値の 2px スタブ */
  .tombo-plate .bar:hover { opacity: .82; }                                /* 読み取りの合図 */
  .tombo-plate text  { font-family: var(--tombo-font-mono); font-size: var(--tombo-text-label);
    letter-spacing: .08em; fill: var(--tombo-ink-faint); }                 /* 銘は等幅(憲法②) */
  .tombo-plate .val  { fill: var(--tombo-ink); font-weight: 600; }         /* 選択的な値ラベル */

  /* ツールチップ — パネルの造形だけ。表示(display)と位置(transform)は消費側 JS。
     視覚専用チャネル(role="presentation")なので pointer-events:none、
     アクセシブルなデータ経路は数表と bar の aria-label が担う。 */
  .tombo-tip {
    position: absolute; inset-block-start: 0; inset-inline-start: 0;
    display: none; z-index: 2; pointer-events: none;
    background: var(--tombo-surface); border: 1px solid var(--tombo-ink);
    padding: var(--tombo-space-8) var(--tombo-space-12);
    font-family: var(--tombo-font-mono);
    font-size: var(--tombo-text-note); line-height: var(--tombo-lh-note);
    color: var(--tombo-ink-sub); white-space: pre;
  }
  .tombo-tip > b { display: block; color: var(--tombo-ink); font-weight: 600; } /* 見出し行 */

  /* 数表 — 図版と対になるアクセシブルなテーブル代替の開閉 */
  .tombo-numbers > summary {
    cursor: pointer;
    font-family: var(--tombo-font-mono);
    font-size: var(--tombo-text-label); line-height: var(--tombo-lh-label);
    letter-spacing: .12em; color: var(--tombo-ink-faint);
  }
  .tombo-numbers[open] > summary { margin-block-end: var(--tombo-space-12); }
}
```

print 節(unlayered)への追記 2 行:

- 改ページ分割禁止: `.tombo-metric, .tombo-callout, .tombo-code, figure, tr, .tombo-check` に **`.tombo-plate`** を加える(div で使われた場合の保険 — `<figure>` 内なら既に守られる)。
- 非印刷: `.tombo-themes, .tombo-copy` に **`.tombo-tip`** を加える(JS で開いたまま印刷された場合の保険)。

## markup 契約(README と catalog に明記。CSS では強制できない)

```html
<figure>
  <figcaption class="tombo-fig">FIG. 01 — DAILY CONTRIBUTIONS</figcaption>
  <div class="tombo-plate">
    <svg viewBox="0 0 720 200" role="img" aria-label="日別コントリビューション数の棒グラフ">
      <line class="axis" … /><text x="…" text-anchor="end">40</text>
      <rect class="bar" … tabindex="0" aria-label="07/21 MON: 21" />
      <rect class="bar is-zero" … />
      <text class="val" …>21</text>
      <line class="now" … />
      <line class="base" … />
    </svg>
    <div class="tombo-tip" role="presentation"><b>07/21 MON — 21</b>COMMITS      18</div>
  </div>
  <details class="tombo-numbers">
    <summary>NUMBERS — 数表を開く</summary>
    <div class="tombo-table-wrap" role="region" aria-label="日次の数表" tabindex="0">
      <table class="tombo-table">…</table>
    </div>
  </details>
</figure>
```

- 銘(`.tombo-fig`)は `<figcaption>` に載せ、枠の**外**(上)に置く — studio-internal・catalog c05 と同じ形。
- SVG には `role="img"` + `aria-label`(または銘への `aria-labelledby`)。
- **数表が正式なテキスト代替。** ツールチップは視覚の補助で、スクリーンリーダー経路ではない。インタラクティブなバーには `tabindex="0"` + `aria-label` を振る。
- 枠がスクロールし得るのに中にフォーカス可能要素が無い図では、`.tombo-table-wrap` と同じ作法(`role="region"` + アクセシブル名 + `tabindex="0"`)を枠に付ける。バーがフォーカス可能ならスクロールはフォーカス追従で足りる。
- ツールチップの表示は消費側 JS の責務: `display` を切り替え、`transform: translate(x, y)` で置く(studio-internal の実装がリファレンス)。

## 規範(catalog #c19 に明文化)

1. **軸は 1 本** — ink 1.5px の基線(`.base`)だけ。第 2 軸は作らない。
2. **目盛線は hairline**(`.axis`) — 図の主役はデータ。
3. **単系列は green 一色** — ゼロ値だけ hairline(`.is-zero`)。多系列の色分けはしない — 系列が増えたら図を分ける。
4. **値ラベルは選択的**(`.val`) — ピークなど読み取りの要所だけ。全バーへの記入は数表の仕事。
5. **朱は現在地のみ**(`.now`) — 選択中の週・今日を指す 1 本の線。データ系列には使わない。

## 色・コントラスト

新色・新トークンなし。使用ペアは全て既存ゲート対象(`ink-sub/surface`・`ink-faint/paper,surface`・`ink/paper`・`green/paper`)。`.is-zero` の hairline バーは装飾(値ゼロは高さ 2px のスタブ形状と数表が伝える)。コントラストゲートは構造的に不変(37 PASS のまま)。

## example(components.html)

- toc に「19 — 図版」を追加、`#c19` 節を印刷(c18)の後に追加。
- 実演は**静的 SVG**(catalog はページ JS ゼロを維持)。7 本バー・ゼロ値 1 本・ピークの `.val` 1 個・`.now` 1 本・axis 3 本 + base、ツールチップはデモ用に可視化して静置(catalog の `<style>` で `display:block; position:static` に上書き)。数表は 2〜3 行で開いた状態を見せる。
- note に規範 5 項と markup 契約(数表が text alternative であること・ツールチップは JS 表示であること)を書く。

## README

「Charts (図版)」節を Forms と Print の間に追加: クラス一覧表(`.tombo-plate` / 内部クラス / `.tombo-tip` / `.tombo-numbers`)+ markup 契約 + 規範 + `--tombo-plate-min` の上書き例。

## リリース

- **v0.13.0**(feat・純追加・非破壊)。banner(tombo.css/tombo.js)と README の vendoring pins 3 箇所を chore commit で bump(check_banner.py がタグ時に強制)。
- リリースフロー: feature ブランチ → ff-merge → lightweight tag `v0.13.0` → push(linear history 維持、PR は作らない)。
- サイズ予算: 追加 ~1.4KB raw ≈ +0.4KB gzip 見込み。ceiling 12KiB に対し現在 ~10.2KB → 余裕。

## 検証

- `npm run check`(stylelint Baseline / contrast / size / banner / node --check)が green。
- chrome-devtools で catalog #c19 を**昼夜 2 テーマ**スクリーンショット + computed style 検証(`.bar` fill = green、`.now` stroke = shu、`text` の font-family/size、`.tombo-tip` の border/padding、`min-inline-size` 発動時の枠内スクロール)。
- 狭幅(<600px 相当)で枠内スクロールが発動し、ページ本体が横に動かないこと。
- `details` の開閉が JS ゼロで機能すること。
