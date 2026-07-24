# TOMBO トップバー(.tombo-topbar) — 設計 (2026-07-24)

Issue: <https://github.com/wadakatu/tombo/issues/16>

## 背景・目的

アプリ/ダッシュボード音量のページは「hairline 下罫 + shell 内 flex + display 声のロゴ + mono の右肩ラベル」のトップバーで始まる。このレシピが examples/app.html(`.top`/`.logo`/`.me`)と studio-internal の週次アクティビティページ(`.top`/`.brand`/`.path`)の 2 箇所で手組み複製され、実装ごとにブレている:

| 項目 | app.html | studio-internal |
|---|---|---|
| ロゴ font-size | 14px(ad-hoc) | 15px(ad-hoc) |
| ロゴ letter-spacing | なし | -.015em |
| align-items | center | baseline |
| gap | 24(モバイルで 16) | 16 |
| flex-wrap | モバイルのみ wrap | wrap |
| 右肩の mono 化 | markup 側で `.tombo-mono` 併用 | CSS 側で font-family |
| 右肩の letter-spacing | なし | .12em |

さらに、タブ(`.tombo-tabs`)をトップバーに組み込むときの `border-bottom: 0; flex: 1` の打ち消しが消費側の暗黙知になっている。

**目的:** アプリ音量ページの先頭 20 行がどのプロダクトでも同一マークアップになるよう `.tombo-topbar` を components に追加し、ロゴ段・余白・罫線のブレを止める。

## スコープ

### 今回やる(純追加・非破壊 = v0.14.0)

- **`.tombo-topbar`** — 下罫(hairline)+ padding-block 16。直下の `.tombo-shell` を flex 化(baseline 揃え・gap 16・wrap)。
- **`.tombo-topbar .brand`** — display 声のロゴ段(Instrument Sans 700・text-body 段・-.015em)。中の `<a>` は ink 継承・下線なし。
- **`.tombo-topbar .meta`** — mono ink-faint の右肩ラベル(text-label 段・.12em・`margin-inline-start: auto`)。
- **`.tombo-topbar .tombo-tabs`** — 組み込み時の打ち消し(`border-block-end: 0; flex: auto`)を部品側で吸収。
- **example**: examples/app.html のトップバーを新部品で置き換え(ページ CSS の `.top`/`.logo`/`.me` と 640px の wrap 上書きを削除)。
- **example**: components.html カタログに「20 — トップバー」節(実演 + コピペ用スニペット)+ toc 追加。
- **README**: 「Topbar (トップバー)」節(クラス一覧 + markup 契約)。Charts と Print の間に追加。

### 今回やらない

- **汎用バー部品(`.tombo-bar` 等)への抽象化** — フッターは `.tombo-footer` が既にあり、ツールバー需要はまだ無い(YAGNI)。トップバーという 1 レシピを固定する。
- **狭幅での `.meta` 非表示** — studio-internal は狭幅で `.path` を `display:none` にしているが、消すか折り返すかはページの判断。部品の既定は wrap(折り返し)。
- **studio-internal 側の置き換え** — 別リポジトリ。issue #16 のスコープは tombo 側(tombo.css + examples)のみ。
- **example 専用 CSS の全廃** — app.html の `.metrics` グリッド等、トップバー以外のページ組みは残る。

## 設計判断

> 本 spec は /goal による自律モードで確定した(前例: 2026-07-24 図版 spec)。open questions は下記の根拠で自己決定し、ユーザーレビューは spec/実装のレビューで受ける。

1. **命名は issue 案どおり `.tombo-topbar` + 配下短名 `.brand` / `.meta`。** グローバルな `.brand` は作らず、`.tombo-metric > .k`・`.tombo-logo > .h` と同じ「コンポーネント配下の内部短名」パターン。catalog サイドバーの `.brand`(ページ CSS)とも衝突しない。
2. **ロゴ段は `var(--tombo-text-body)`(15px)。** 14px(app)と 15px(studio)のブレは、type scale「ad-hoc サイズ禁止」に照らすと 15px 一択(14px はスケールに無い)。`letter-spacing: -.015em` は `.tombo-display` と同じ Instrument Sans の詰め。line-height は継承(2 = 30px)で両実装と同じ。
3. **`align-items: baseline`。** ロゴ(15px)と右肩(10.5px)の異サイズ並置はベースライン揃えが活字的に正しい(studio 版で実証済み)。タブを挟んでもフレックスのベースライン整列はテキストベースライン同士を揃える。app 版の center が今回のブレ。
4. **`gap: var(--tombo-space-16)` + `flex-wrap: wrap` を既定にする。** issue が「現状のレシピ」として引用しているのは studio 版(16/wrap)。app 版の 24 も 640px 以下では 16 + wrap に落ちており、統一しても失うものがない。メディアクエリ無しで全幅域が動く(コンテナ思想と同じ)。
5. **`.meta` は mono 声を部品側が持つ。** app 版は markup の `.tombo-mono` 併用、studio 版は CSS — 部品化するなら CSS 側。`letter-spacing: .12em` は `.tombo-footer`・`.path` と同値。`text-transform` は**かけない** — ユーザー名・REV など大小文字を運ぶ内容が載る(studio も未設定)。
6. **ロゴのリンクは部品が受ける。** `.tombo-topbar .brand a { color: inherit; text-decoration: none; }` — studio 版で必要になった実証済みレシピ。ロゴがリンクなのはトップバーの常態で、green 下線のままでは使えない。
7. **タブの打ち消しは部品側。** `.tombo-topbar .tombo-tabs`(0,2,0)は同層の `.tombo-tabs`(0,1,0)に specificity で勝つ。`flex: auto` でタブが残り幅を取る(basis 0 の `flex: 1` は狭幅で nav を min-content まで潰し、CJK タブが 1 文字幅の縦積みになるため不採用 — auto なら内容幅を保ったままブロックごと折り返す)。`.meta` の `margin-inline-start: auto` は(タブ無しでも)右肩を保証する。
8. **要素は `<header>` を契約に推す。** ページ先頭のバーは banner ランドマーク。クラス自体は要素非依存(app.html の現行は `<div>` — 置き換え時に `<header>` へ)。セレクタは直下結合(`.tombo-topbar > .tombo-shell`)— 両実装とも shell は直下で、深い入れ子の誤爆を避ける。

## 設計(CSS)

`@layer tombo.components` の新ブロックとして、図版ブロックの後・print 節の前に追加する(追記パターンの踏襲)。

```css
@layer tombo.components {
  /* トップバー — アプリ音量の先頭 (spec 2026-07-24, issue #16)。
     外枠が全幅の下罫、幅は内側の .tombo-shell(直下)が決める。
     ロゴ段は display 声の text-body 固定 — 14/15px のブレはここで止める。 */
  .tombo-topbar { border-block-end: 1px solid var(--tombo-hairline); padding-block: var(--tombo-space-16); }
  .tombo-topbar > .tombo-shell { display: flex; align-items: baseline; gap: var(--tombo-space-16); flex-wrap: wrap; }
  .tombo-topbar .brand { font-family: var(--tombo-font-display); font-weight: 700;
    font-size: var(--tombo-text-body); letter-spacing: -.015em; }
  .tombo-topbar .brand a { color: inherit; text-decoration: none; } /* ロゴリンクは ink・下線なし */
  .tombo-topbar .meta { margin-inline-start: auto; font-family: var(--tombo-font-mono);
    font-size: var(--tombo-text-label); line-height: var(--tombo-lh-label);
    letter-spacing: .12em; color: var(--tombo-ink-faint); } /* 大小文字を運ぶので uppercase はかけない */
  /* タブ組み込み — 消費側の暗黙知だった打ち消しを部品側で吸収。flex は auto —
     basis 0 だと狭幅で nav が min-content まで潰れ、CJK タブが 1 文字幅の縦積みになる */
  .tombo-topbar .tombo-tabs { border-block-end: 0; flex: auto; }
}
```

## markup 契約(README と catalog に明記。CSS では強制できない)

```html
<header class="tombo-topbar">
  <div class="tombo-shell">
    <span class="brand"><a href="/">SCREENBOOK</a></span>
    <nav class="tombo-tabs">
      <a href="/screens" aria-current="page">画面一覧</a>
      <a href="/deps">依存グラフ</a>
    </nav>
    <span class="meta">wadakatu@prod / REV 4.2.1</span>
  </div>
</header>
```

- 外枠は shell の**外** — 下罫は全幅に走り、中身は `.tombo-shell` が絞る。`.tombo-shell` は直下に置く。
- 要素は `<header>`(banner ランドマーク)。ロゴだけ・タブ無しの構成も可(`.meta` は auto margin で右肩に残る)。
- タブは `.tombo-tabs` をそのまま入れる — 打ち消しは部品が持つので消費側 CSS は不要。現在地は従来どおり `aria-current`。
- 狭幅では wrap で折り返す。`.meta` を消したいページは自分の CSS で(部品は消さない)。

## 色・コントラスト

新色・新トークンなし。使用ペア(`ink/paper`・`ink-faint/paper`・`hairline`)は全て既存ゲート対象。コントラストゲートは構造的に不変。

## example

- **app.html**: `.top`/`.logo`/`.me`/タブ打ち消しのページ CSS(5 宣言)と 640px メディアクエリ内の `.top` wrap 上書きを削除し、markup を契約形(`<header class="tombo-topbar">`)へ置き換え。`.me` の `.tombo-mono` 併用も不要になる。視覚差分はロゴ 14→15px・center→baseline・gap 24→16 で、これは意図した統一。
- **components.html**: toc に「20 — トップバー」を追加、`#c20` 節を図版(c19)の後に追加。実演はロゴ + タブ 3 本 + 右肩ラベルの 1 本。demo 枠(padding 24)の中に shell のガター(clamp 20–64px)が重なると余白が二重になるので、カタログのページ CSS で `#c20 .tombo-shell { padding-inline: 0 }` に落とす(実演は構造 — 全幅の下罫と flex — を見せる)。note に「先頭 20 行が同一マークアップになる」目的とタブ打ち消し吸収・`<header>` 契約を書く。

## README

「Topbar (トップバー)」節を Charts (図版) と Print の間に追加: クラス一覧表(`.tombo-topbar` / `.brand` / `.meta` / タブ吸収)+ markup 契約 + 「ロゴ段は text-body 固定・ブレ禁止」の規範。

## リリース

- **v0.14.0**(feat・純追加・非破壊)。banner(tombo.css/tombo.js)と README の vendoring pins を chore commit で bump(check_banner.py がタグ時に強制)。
- リリースフロー: feature ブランチ → ff-merge → lightweight tag `v0.14.0` → push(linear history 維持、PR は作らない)。
- サイズ予算: 追加 ~0.6KB raw ≈ +0.2KB gzip 見込み。ceiling 12KiB に対し余裕。

## 検証

- `npm run check`(stylelint Baseline / contrast / size / banner / node --check)が green。
- chrome-devtools で app.html と catalog #c20 を**昼夜 2 テーマ**スクリーンショット。ロゴとタブとメタのベースライン整列・タブの下罫消え・右肩の位置を目視 + computed style で確認(`.brand` font-size = 15px、`.tombo-tabs` border-bottom = 0、`.meta` の margin-inline-start が効いた右寄せ)。
- 狭幅(<640px 相当)で wrap が発動し、ページ本体が横に動かないこと。
- タブ無し構成(ロゴ + meta だけ)で `.meta` が右肩に残ること(catalog かデスクトップ確認で 1 ケース)。
