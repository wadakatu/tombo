# TOMBO トップバー(.tombo-topbar) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** issue #16 — アプリ音量ページの先頭が同一マークアップになるトップバー部品(`.tombo-topbar` + 配下 `.brand`/`.meta` + `.tombo-tabs` 吸収)を tombo.css に追加し、app.html を置き換え、catalog/README に明文化して v0.14.0 として出す。

**Architecture:** `@layer tombo.components` の新ブロック 1 つ(図版ブロックの後・unlayered print 節の前)。内部クラスは `.tombo-topbar` 配下に scoped(グローバル `.brand` を作らない)。JS 変更なし・新トークンなし・print 追記なし。

**Tech Stack:** 手書き CSS(tombo.css 単一ファイル)、検証は `npm run check`(stylelint Baseline / contrast / size / banner / node --check)+ chrome-devtools MCP の computed style 実測とスクリーンショット(昼夜 2 テーマ)。

**Spec:** `docs/superpowers/specs/2026-07-24-tombo-topbar-design.md`(CSS 全文・markup 契約はここが正)

**Subagent policy:** implementer は Sonnet(最低)、レビューは Opus([[tombo-subagent-model-policy]])。

## Global Constraints

- 追加のみ・非破壊。既存セレクタは一切変更しない(print 節も今回は触らない — トップバーはそのまま刷れる)。
- 新トークン・新色を作らない(使用ペアは `ink/paper`・`ink-faint/paper`・`hairline` の既存ゲート対象のみ → contrast gate PASS 数不変)。
- font-size は type scale のみ(`.brand` = `var(--tombo-text-body)`。14px 等の ad-hoc 値を書かない)。
- Baseline widely 内の CSS のみ(stylelint gate が強制。PE ledger への追加はしない)。
- コミットは英語 Conventional Commits、`Co-Authored-By` 禁止。
- サイズ予算: `tombo.css` gzip ≤ 12KiB(追加 ~0.6KB raw 見込みで余裕)。

---

### Task 1: tombo.css — トップバーブロック

**Files:**
- Modify: `tombo.css` — 図版ブロック(`.tombo-numbers[open] > summary` を含む `@layer tombo.components` ブロック)の閉じ括弧の直後・`/* ── print ──` コメントの前
- Test: `npm run check` + scratch ページの computed style 実測

**Interfaces:**
- Produces: `.tombo-topbar`(外枠)/ `.tombo-topbar > .tombo-shell`(flex 行)/ `.tombo-topbar .brand`(+ 中の `a`)/ `.tombo-topbar .meta` / `.tombo-topbar .tombo-tabs`(打ち消し)。Task 2/3 の examples・README はこの名前をそのまま使う。

- [ ] **Step 1: 「failing test」= scratch ページを先に作る**

`/private/tmp/claude-501/-Users-wadakatu-www-oss-tombo/1752e70a-4970-4df3-a4b5-9b20dd9b52d4/scratchpad/topbar-test.html` に spec の markup 契約どおりのトップバー(brand リンク + tabs 3 本 + meta。比較用にタブ無し構成をもう 1 本)を `<link rel="stylesheet" href="file:///Users/wadakatu/www/oss/tombo/tombo.css">` で置く。CSS 追加前に chrome-devtools で開き、`.tombo-topbar` に border が**なく**、`.tombo-shell` が flex で**ない**こと(縦積み)を確認 — これが red 状態。

- [ ] **Step 2: tombo.css にトップバーブロックを追加**

図版ブロックの閉じ括弧(`}`)の直後・`/* ── print ──` コメントの前に、spec「設計(CSS)」節の CSS 全文を挿入する(spec が正 — コメント含めそのまま):

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
  /* タブ組み込み — 消費側の暗黙知だった打ち消しを部品側で吸収 */
  .tombo-topbar .tombo-tabs { border-block-end: 0; flex: 1; }
}
```

- [ ] **Step 3: gate + 実測で green を確認**

Run: `npm run check` → 5 ゲート全部 PASS(stylelint に Baseline 違反が出ないこと)。
chrome-devtools で scratch ページを再読み込みし computed style を実測(昼テーマ):
- `.tombo-topbar` — `border-bottom: 1px solid` hairline 実値、`padding-block: 16px`
- `> .tombo-shell` — `display: flex`、`align-items: baseline`、`gap: 16px`、`flex-wrap: wrap`
- `.brand` — `font-size: 15px`、`font-weight: 700`、font-family 先頭が Instrument Sans、`letter-spacing: -0.225px`(-.015em)
- `.brand a` — `color` = ink 実値(昼 `rgb(26, 33, 29)`、green でない)、`text-decoration-line: none`
- `.meta` — `font-size: 10.5px`、`line-height: 18px`、`letter-spacing: 1.26px`(.12em)、`color` = ink-faint 実値(昼 `rgb(102, 112, 105)`)、右端が shell のコンテンツ右端に接する(auto margin)
- `.tombo-topbar .tombo-tabs` — `border-bottom-width: 0px`、`flex-grow: 1`
- タブ無し構成でも `.meta` が右端に付くこと
- 420px 幅に絞って行が wrap し、`document.documentElement.scrollWidth == clientWidth`(ページは溢れない)

- [ ] **Step 4: Commit**

```bash
git add tombo.css
git commit -m "feat: add the app-volume topbar — .tombo-topbar with scoped .brand/.meta"
```

---

### Task 2: examples/app.html をトップバー部品で置き換え

**Files:**
- Modify: `examples/app.html` — `<style>` から 5 宣言 + メディアクエリ 1 行を削除、markup の `div.top` を `header.tombo-topbar` へ

**Interfaces:**
- Consumes: Task 1 の `.tombo-topbar` / `.brand` / `.meta`(そのまま)。
- Produces: なし(example のみ)。

- [ ] **Step 1: ページ CSS からトップバーのレシピを削除**

`<style>` 内の以下 5 宣言を削除:

```css
  .top { border-bottom: 1px solid var(--tombo-hairline); padding: var(--tombo-space-16) 0; }
  .top .tombo-shell { display: flex; align-items: center; gap: var(--tombo-space-24); }
  .logo { font-family: var(--tombo-font-display); font-weight: 700; font-size: 14px; }
  .top .tombo-tabs { border-bottom: 0; flex: 1; }
  .me { margin-left: auto; font-size: var(--tombo-text-label); color: var(--tombo-ink-faint); }
```

640px メディアクエリからも `.top` 行を削除(`.metrics` 行は残す):

```css
  @media (max-width: 640px) {
    .metrics { grid-template-columns: 1fr; }
  }
```

- [ ] **Step 2: markup を契約形へ置き換え**

```html
  <header class="tombo-topbar">
    <div class="tombo-shell">
      <span class="brand">SCREENBOOK</span>
      <nav class="tombo-tabs">
        <a href="#" aria-current="page">画面一覧</a>
        <a href="#">依存グラフ</a>
        <a href="#">変更影響</a>
      </nav>
      <span class="meta">wadakatu@prod / REV 4.2.1</span>
    </div>
  </header>
```

(旧: `div.top > div.tombo-shell > span.logo + nav.tombo-tabs + span.me.tombo-mono`。`.tombo-mono` 併用は不要になる — `.meta` が mono 声を持つ。)

- [ ] **Step 3: 検証(昼夜 2 テーマ)**

- `grep -n "\.top\b\|\.logo\b\|\.me\b" examples/app.html` → ヒット 0(取り残しなし)。
- chrome-devtools で `examples/app.html` を開き、昼(tombo)/夜(hotaru)両テーマでスクリーンショット。確認: 下罫全幅・ロゴ 15px・タブの下罫が消えて残り幅を取る・右肩 mono ink-faint・ベースライン整列。
- 420px 幅で wrap 発動・ページ非溢れ(`scrollWidth == clientWidth`)。
- `npm run check` green のまま。

- [ ] **Step 4: Commit**

```bash
git add examples/app.html
git commit -m "docs: rebuild the app example's topbar on .tombo-topbar"
```

---

### Task 3: catalog #c20 + README「Topbar (トップバー)」

**Files:**
- Modify: `examples/components.html` — toc(c19 の次)+ `#c20` 節(c19 節の後)+ catalog `<style>` にガター落とし 1 行
- Modify: `README.md` — `## Charts (図版)` と `## Print` の間に `## Topbar (トップバー)`

**Interfaces:**
- Consumes: Task 1 の全クラス名(そのまま)。
- Produces: なし(ドキュメントのみ)。

- [ ] **Step 1: toc にエントリ追加**

`<a href="#c19">19 — 図版</a>` の直後:

```html
        <a href="#c20">20 — トップバー</a>
```

- [ ] **Step 2: catalog `<style>` にガター落としを追加**

`.foot { … }` 行の前に(demo 枠の padding 24 と shell のガター clamp 20–64px が二重になるため):

```css
  #c20 .tombo-shell { padding-inline: 0; } /* demo枠内はガター不要(実演は下罫とflexの構造) */
```

- [ ] **Step 3: `#c20` 節を c19 の `</section>` の直後に追加**

```html
      <section id="c20">
        <h2 class="tombo-sec">トップバー</h2>
        <p class="note">アプリ音量の先頭。外枠が全幅のhairline下罫を引き、幅は直下の <code>.tombo-shell</code> が決める(下罫はビューポート全幅・中身はshellが絞る)。ロゴ段(<code>.brand</code>)はdisplay声のtext-body固定 — 実装ごとの14/15pxのブレはここで止まる。中の <code>&lt;a&gt;</code> はink継承・下線なし。右肩(<code>.meta</code>)は等幅ink-faintで <code>margin-inline-start: auto</code> — ユーザー名やREVなど大小文字を運ぶのでuppercaseはかけない。タブは <code>.tombo-tabs</code> をそのまま入れる — 組み込み時の打ち消し(<code>border-block-end: 0; flex: 1</code>)は部品側が吸収する。要素は <code>&lt;header&gt;</code>(bannerランドマーク)、現在地は従来どおり <code>aria-current</code>。行はbaseline揃え、狭幅ではwrapで折り返す(<code>.meta</code> を消したいページは自分のCSSで — 部品は消さない)。</p>
        <div class="demo">
          <header class="tombo-topbar">
            <div class="tombo-shell">
              <span class="brand"><a href="#c20">SCREENBOOK</a></span>
              <nav class="tombo-tabs">
                <a href="#c20" aria-current="page">画面一覧</a>
                <a href="#c20">依存グラフ</a>
                <a href="#c20">変更影響</a>
              </nav>
              <span class="meta">wadakatu@prod / REV 4.2.1</span>
            </div>
          </header>
        </div>
        <figure class="tombo-code">
          <figcaption><span>HTML</span><span>.TOMBO-TOPBAR</span></figcaption>
          <pre tabindex="0">&lt;header class="tombo-topbar"&gt;
  &lt;div class="tombo-shell"&gt;
    &lt;span class="brand"&gt;&lt;a href="/"&gt;SCREENBOOK&lt;/a&gt;&lt;/span&gt;
    &lt;nav class="tombo-tabs"&gt;
      &lt;a href="/screens" aria-current="page"&gt;画面一覧&lt;/a&gt;
      &lt;a href="/deps"&gt;依存グラフ&lt;/a&gt;
    &lt;/nav&gt;
    &lt;span class="meta"&gt;wadakatu@prod / REV 4.2.1&lt;/span&gt;
  &lt;/div&gt;
&lt;/header&gt;</pre>
        </figure>
        <p class="note">アプリ/ダッシュボード音量のページの先頭20行を、どのプロダクトでも同一マークアップにするための部品。ロゴだけ・タブ無しの構成も可 — <code>.meta</code> はauto marginで右肩に残る。実物は <a href="app.html">examples/app.html</a> の先頭。</p>
      </section>
```

- [ ] **Step 4: README に `## Topbar (トップバー)` 節を追加**

`## Print` 見出しの直前に:

```markdown
## Topbar (トップバー)

Every app-volume page opens the same way: a full-width hairline rule, the brand in the display voice, mono metadata on the right shoulder. `.tombo-topbar` fixes that recipe so the first 20 lines of every product are the same markup — the brand is locked to `--tombo-text-body` (no more 14px/15px drift), the row aligns on baselines and wraps on narrow screens, and dropping `.tombo-tabs` inside needs no undo CSS (the bar absorbs `border-block-end: 0; flex: 1`).

| Class | Role |
|---|---|
| `.tombo-topbar` | the bar — full-width hairline bottom rule, `--tombo-space-16` block padding; put a `.tombo-shell` directly inside |
| `.brand` | the logo line — display voice, 700, `--tombo-text-body`, `-.015em`; a nested `<a>` inherits ink with no underline |
| `.meta` | the right shoulder — mono, label-size, ink-faint, `margin-inline-start: auto`; carries case (no uppercase transform) |
| `.tombo-topbar .tombo-tabs` | tabs drop in as-is — the bar removes their bottom rule and gives them the remaining width |

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

The rule spans the viewport because the border sits on the bar, not the shell — keep `.tombo-shell` as the direct child. Brand-only bars work too: `.meta` stays on the right shoulder via its auto margin. On narrow screens the row wraps; if a page wants `.meta` gone instead, hide it from that page's stylesheet — the component never does.
```

- [ ] **Step 5: 検証(昼夜 2 テーマ)**

- chrome-devtools で `examples/components.html#c20` を開き、両テーマでスクリーンショット。確認: 下罫が demo 枠の全幅・ロゴリンクが ink 下線なし・タブ下罫消え・右肩 meta・`#c20 .tombo-shell` のガター 0。
- toc「20 — トップバー」からのアンカー遷移。
- `npm run check` green のまま。

- [ ] **Step 6: Commit**

```bash
git add examples/components.html README.md
git commit -m "docs: add the topbar section to the catalog and README"
```

---

### Task 4: v0.14.0 バージョン bump

**Files:**
- Modify: `tombo.css:1`(banner)/ `tombo.js:1`(banner)/ `README.md` vendoring pins(`v0.13.0` 参照)

**Interfaces:**
- Consumes: なし。Produces: タグ `v0.14.0` と整合する banner(check_banner.py がタグ push 時に強制)。

- [ ] **Step 1: 現在の v0.13.0 参照を列挙**

Run: `grep -n "v0\.13\.0" tombo.css tombo.js README.md`
Expected: tombo.css:1、tombo.js:1、README の pins(前回実績 3 箇所、計 5 行)。

- [ ] **Step 2: 全箇所を v0.14.0 に置換**

- [ ] **Step 3: banner ゲートで検証**

Run: `npm run check`
Expected: `check_banner.py` PASS(css == js banner == README pins)。他ゲートも green。

- [ ] **Step 4: Commit**

```bash
git add tombo.css tombo.js README.md
git commit -m "chore: bump banners and vendoring pins to v0.14.0"
```

---

### Task 5: Opus whole-branch review + 修正

- [ ] **Step 1:** Agent(model: opus)に `git diff main...feature/topbar` の全量レビューを依頼(観点: spec 準拠・既存パターンとの一貫性・a11y 契約(`<header>`/`aria-current`)・catalog HTML の実 geometry・README の正確さ・app.html の取り残し)。
- [ ] **Step 2:** Critical/Important は修正して追コミット(`fix:`/`docs:`)、Minor は判断の上対応 or 記録。
- [ ] **Step 3:** 修正後 `npm run check` + 両テーマ再スクリーンショット。

---

### Task 6: リリース(linear history)

- [ ] **Step 1:** `git checkout main && git merge --ff-only feature/topbar`
- [ ] **Step 2:** `git tag v0.14.0`(lightweight)
- [ ] **Step 3:** `git push origin main && git push origin v0.14.0`
- [ ] **Step 4:** CI(push run)green を確認(`gh run list`)
- [ ] **Step 5:** issue #16 をクローズ(実装内容・自己決定した設計判断 — brand 15px 固定・baseline・gap 16 — の理由をコメント)
- [ ] **Step 6:** ブランチ削除、メモリ更新(roadmap: v0.14.0)
