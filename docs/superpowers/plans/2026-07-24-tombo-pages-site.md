# TOMBO GitHub Pages 紹介サイト Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** issue #18 — tombo.css を LP ボリュームでドッグフーディングする紹介ページ(EN `/` + JA `/ja/`)を GitHub Pages(main ルート配信)で公開し、`check_banner.py` をサイトのピンまで検査するよう拡張する。

**Architecture:** 静的 2 ページ + 共有 `assets/site.css`(コンシューマー流儀: tombo のトークン・クラスのみ参照、`@layer` 外)。言語切替はトップバーの素のリンク。tombo.css / tombo.js への変更なし。

**Tech Stack:** 手書き HTML/CSS。検証は `npm run check` + chrome-devtools MCP(昼夜 2 テーマ × 2 言語 + 375px)。デプロイは Pages「Deploy from a branch: main / root」。

**Spec:** `docs/superpowers/specs/2026-07-24-tombo-pages-site-design.md`(構成・i18n・ゲート仕様はここが正)

**Subagent policy:** implementer は Sonnet(最低)、レビューは Opus([[tombo-subagent-model-policy]])。

## Global Constraints

- ブランチ: `feature/pages-site`(spec コミット済みの現行ブランチ)。main は保護済み — 変更は必ず PR 経由、CI `check` green + up to date が条件
- バージョン参照はすべて **v0.14.1**(現行タグ・バナーと一致させる。README は触らない)
- サイトの vendoring ピンは **各ページちょうど 3 つ**(`show v0.14.1:` × tombo.css / LICENSE / tombo.js)
- DISPLAY voice(`.tombo-display`, tracking -.015em)は Latin にのみ使用。日本語見出しは BODY voice(素の h2/h3)
- 朱(`--tombo-shu`)は現在地の線のみ。面塗り・本文使用は禁止
- 純白 `#FFF` / 純黒 `#000` / オフセット付き影は禁止(tombo の掟)
- インラインの custom property は `--tombo-ruler-value` のみ許可
- コミットは英語 Conventional Commits、`Co-Authored-By` 禁止

---

### Task 1: EN ページ(index.html)+ assets/site.css + .nojekyll

**Files:**
- Create: `index.html`
- Create: `assets/site.css`
- Create: `.nojekyll`(空ファイル)

**Interfaces:**
- Consumes: tombo.css v0.14.1 の全クラス(特に `a.tombo-btn` — #17 で `<a>` 対応済み)
- Produces: `assets/site.css` のクラス群(`.hero .cols` `.cta` `.tagline` `.inst` `.sec` `.lede` `.cards3` `.fcard` `.sigs` `.sig` `.sig--grid` `.s-note` `.swatches` `.sw` `.vol` `.foot`)— Task 2 の ja/index.html が同じものを使う

- [ ] **Step 1: .nojekyll(空)を作成**

```bash
touch .nojekyll
```

- [ ] **Step 2: assets/site.css を作成**

```css
/* TOMBO intro site — consumer-side layout. tombo.css のトークン/クラスだけを参照する。 */
:root { --tombo-shell: var(--tombo-shell-wide); } /* LP: ページ全体を wide 段に(README の掟どおり :root で) */

/* topbar */
.tombo-topbar .tombo-themes { margin-inline-start: var(--tombo-space-16); }

/* hero — examples/lp.html のレシピを踏襲 */
.hero { padding-block: var(--tombo-space-72) var(--tombo-space-48); }
.hero .tombo-logo { display: block; margin-bottom: var(--tombo-space-16); }
.hero .cols { display: grid; grid-template-columns: 1.25fr .75fr; gap: 56px; margin-top: var(--tombo-space-24); align-items: start; }
.hero .cols > .tombo-flow > .tombo-dim { --tombo-flow-space: var(--tombo-space-24); }
.hero .cols > .tombo-flow > .cta { --tombo-flow-space: var(--tombo-space-24); }
.hero h1 small { display: block; font-family: var(--tombo-font-body); font-weight: 700;
  font-size: clamp(18px, 2vw, 22px); color: var(--tombo-green); margin-top: var(--tombo-space-16); letter-spacing: 0; }
.hero .tombo-dim { max-inline-size: 320px; }
.tagline { font-size: var(--tombo-text-body); line-height: var(--tombo-lh-body); color: var(--tombo-ink-sub); max-width: 50ch; }
.cta { display: flex; gap: var(--tombo-space-16); align-items: center; flex-wrap: wrap; }

/* hero instrument */
.inst .tombo-fig { position: absolute; top: -20px; left: 0; }
.inst .v small { font-size: var(--tombo-text-ui); color: var(--tombo-ink-faint); font-weight: 400; }
.inst .rows { margin-top: var(--tombo-space-16); border-top: 1px solid var(--tombo-hairline); }
.inst .row { display: flex; justify-content: space-between; gap: var(--tombo-space-16); font-family: var(--tombo-font-mono);
  font-size: var(--tombo-text-label); padding: var(--tombo-space-8) 0; border-bottom: 1px solid var(--tombo-hairline); color: var(--tombo-ink-sub); }
.inst .row b { color: var(--tombo-ink); font-weight: 500; }
.inst .cfoot { margin-top: var(--tombo-space-16); }

/* sections */
.sec { padding-block: var(--tombo-space-72) 0; }
.sec:last-of-type { padding-block-end: var(--tombo-space-96); }
.lede { max-width: var(--tombo-shell-reading); color: var(--tombo-ink-sub); margin-top: var(--tombo-space-16); }
.s-note { font-size: var(--tombo-text-ui); line-height: var(--tombo-lh-ui); color: var(--tombo-ink-sub); margin-top: var(--tombo-space-16); }

/* 3 枚カード(三原則・volume dial 共用) */
.cards3 { margin-top: var(--tombo-space-24); display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--tombo-space-16); }
.fcard { display: flex; flex-direction: column; --tombo-flow-space: var(--tombo-space-8); }
.fcard p { font-size: var(--tombo-text-ui); line-height: var(--tombo-lh-ui); color: var(--tombo-ink-sub); }
.fcard > .meta { margin-top: auto; --tombo-flow-space: 0; padding-top: var(--tombo-space-16); }
.fcard .meta div { border-top: 1px solid var(--tombo-hairline); padding-top: var(--tombo-space-8); }
a.vol { color: inherit; text-decoration: none; } /* カード全体リンク: base の下線/green を外す */
a.vol h3 { color: var(--tombo-green); }

/* 署名タイル */
.sigs { margin-top: var(--tombo-space-24); display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--tombo-space-16); }
.sig { position: relative; border: 1px solid var(--tombo-hairline); background: var(--tombo-surface); padding: var(--tombo-space-24) var(--tombo-space-16) var(--tombo-space-16); }
.sig .tombo-fig { margin-bottom: var(--tombo-space-16); }
.sig .tombo-ruler { margin-top: var(--tombo-space-16); }
.sig--grid { background-image: linear-gradient(var(--tombo-grid) 1px, transparent 1px), linear-gradient(90deg, var(--tombo-grid) 1px, transparent 1px); background-size: 24px 24px; }

/* トークンスウォッチ(色はクラスで — インライン style を使わない) */
.swatches { margin-top: var(--tombo-space-24); display: flex; gap: var(--tombo-space-16); flex-wrap: wrap; }
.sw { display: flex; flex-direction: column; gap: var(--tombo-space-8); }
.sw i { display: block; inline-size: 96px; block-size: 48px; border: 1px solid var(--tombo-hairline); }
.sw--paper i { background: var(--tombo-paper); }
.sw--surface i { background: var(--tombo-surface); }
.sw--ink i { background: var(--tombo-ink); }
.sw--ink-sub i { background: var(--tombo-ink-sub); }
.sw--green i { background: var(--tombo-green); }
.sw--shu i { background: var(--tombo-shu); }

/* footer */
.foot { display: flex; align-items: center; gap: var(--tombo-space-16); }

@media (max-width: 840px) {
  .hero .cols, .cards3, .sigs { grid-template-columns: 1fr; }
}
```

- [ ] **Step 3: index.html を作成**

head(hreflang は絶対 URL、ピンは 3 つ):

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TOMBO — the mark that measures. wadakatu's single-file CSS design system</title>
<meta name="description" content="TOMBO is wadakatu's single-file, zero-dependency CSS design system — six signature marks, two themes, and one vermillion line for “you are here.”">
<link rel="alternate" hreflang="en" href="https://wadakatu.github.io/tombo/">
<link rel="alternate" hreflang="ja" href="https://wadakatu.github.io/tombo/ja/">
<link rel="alternate" hreflang="x-default" href="https://wadakatu.github.io/tombo/">
<link rel="icon" href="assets/logo/tombo-mark.svg" type="image/svg+xml">
<link rel="stylesheet" href="tombo.css">
<link rel="stylesheet" href="assets/site.css">
<script>try{var t=localStorage.getItem('tombo-theme');if(t==='tombo'||t==='hotaru')document.documentElement.dataset.theme=t}catch(e){}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@600;700&family=M+PLUS+2:wght@450;500;700&family=Martian+Mono:wdth,wght@75..112.5,400..600&display=swap" rel="stylesheet">
</head>
<body class="tombo-gutters">
```

topbar(言語リンク + テーマトグル):

```html
<header class="tombo-topbar">
  <div class="tombo-shell">
    <span class="brand"><a href="./">TOMBO</a></span>
    <span class="meta">REV v0.14.1</span>
    <div class="tombo-themes tombo-label" hidden>
      <button type="button" data-tombo-theme="system">system</button>
      <button type="button" data-tombo-theme="tombo">tombo</button>
      <button type="button" data-tombo-theme="hotaru">hotaru</button>
    </div>
    <span class="tombo-label"><a href="ja/" lang="ja" hreflang="ja">日本語</a></span>
  </div>
</header>
```

hero(サイズ計は実測値。`96.1%` は 11,808 / 12,288 B):

```html
<main class="tombo-sections">
<section class="hero tombo-vol-lp tombo-glow tombo-corners">
  <b class="tombo-corner-tr"></b><b class="tombo-corner-bl"></b>
  <div class="tombo-shell">
    <span class="tombo-logo tombo-logo--glow" aria-hidden="true"><i class="h"></i><i class="b"></i><i class="w1"></i><i class="w2"></i><i class="t"></i></span>
    <p class="tombo-kicker">TOMBO — WADAKATU DESIGN SYSTEM / FIG. 00</p>
    <div class="cols">
      <div class="tombo-flow">
        <h1 class="tombo-display">The mark that<br>measures.<small lang="ja">測ってから、置く。</small></h1>
        <div class="tombo-dim"></div>
        <div class="tombo-dimlab">single file · zero dependencies · vendored from a tag</div>
        <p class="tagline">One stylesheet for everything wadakatu ships — docs sites, web apps, LPs, portfolios. Six signature marks, repeated without exception, at a volume tuned to context: quiet in docs, loud on an LP.</p>
        <div class="cta">
          <a class="tombo-btn tombo-btn--primary" href="#quickstart">Get the stylesheet</a>
          <a class="tombo-btn tombo-btn--secondary" href="https://github.com/wadakatu/tombo">View on GitHub</a>
          <span class="tombo-label">MIT · CSS 11.8 KB GZIP</span>
        </div>
      </div>
      <div class="inst tombo-metric tombo-glow tombo-corners">
        <b class="tombo-corner-tr"></b><b class="tombo-corner-bl"></b>
        <p class="tombo-fig">FIG. 01 — SIZE BUDGET</p>
        <div class="k">TOMBO.CSS GZIPPED</div>
        <div class="v">11.8<small>KB</small></div>
        <!-- 11,808 / 12,288 B = 96.1% — 出典: scripts/check_size.py(npm run check) -->
        <div class="tombo-ruler" style="--tombo-ruler-value:96.1%"></div>
        <div class="rows">
          <div class="row"><span>tombo.css · gzip</span><b>11,808 B</b></div>
          <div class="row"><span>ceiling</span><b>12,288 B</b></div>
          <div class="row"><span>tombo.js · gzip · optional</span><b>1,264 B</b></div>
          <div class="row"><span>ceiling</span><b>2,048 B</b></div>
        </div>
        <div class="cfoot tombo-label">MEASURED BY SCRIPTS/CHECK_SIZE.PY — CI GATE</div>
      </div>
    </div>
  </div>
</section>
```

三原則(3 カード。銘は `lang="ja"`):

```html
<section class="sec tombo-shell">
  <div class="tombo-dim"></div>
  <div class="tombo-dimlab">constitution — three rules / no exceptions</div>
  <h2 class="tombo-sec">The three rules</h2>
  <div class="cards3">
    <div class="fcard tombo-flow tombo-metric tombo-corners">
      <p class="tombo-fig">R-01</p>
      <h3 lang="ja">すべてを測る</h3>
      <p>Measure everything. Elements sit beside dimension lines, tick marks, and running numbers — the sense that something was measured before it was placed is what gives the page its air.</p>
      <div class="meta"><div class="tombo-label">DIMENSION LINES · TICKS · RUNNING NUMBERS</div></div>
    </div>
    <div class="fcard tombo-flow tombo-metric tombo-corners">
      <p class="tombo-fig">R-02</p>
      <h3 lang="ja">銘は等幅</h3>
      <p>Inscriptions are monospace. Numbers, labels, indices, and units are always set in mono; body copy stays in a quiet sans. Only the instrumentation gets to glow.</p>
      <div class="meta"><div class="tombo-label">VOICE: MARTIAN MONO — LABELS · NUMBERS · CODE</div></div>
    </div>
    <div class="fcard tombo-flow tombo-metric tombo-corners">
      <p class="tombo-fig">R-03</p>
      <h3 lang="ja">朱は現在地</h3>
      <p>Shu marks the current position. Red is reserved for a 1–2px line that points at “here.” The moment it fills a shape, it stops being shu and becomes plain red.</p>
      <div class="meta"><div class="tombo-label">SHU: CURRENT TAB · TOC · RULER VALUE — NEVER A FILL</div></div>
    </div>
  </div>
</section>
```

6 署名(実物デモ。S-03 の 62% は任意のデモ値):

```html
<section class="sec tombo-shell">
  <h2 class="tombo-sec">Six signatures</h2>
  <p class="lede">Not a component library — a fingerprint. Each tile below is the real thing, not a picture of it.</p>
  <div class="sigs">
    <div class="sig tombo-corners"><b class="tombo-corner-tr"></b><b class="tombo-corner-bl"></b>
      <p class="tombo-fig">S-01 — REGISTRATION CORNERS</p>
      <p class="s-note">12px brackets that say “aligned.” You are looking at them — this tile wears all four.</p>
    </div>
    <div class="sig">
      <p class="tombo-fig">S-02 — DIMENSION LINE</p>
      <div class="tombo-dim"></div>
      <div class="tombo-dimlab">the hr that measures — end rules · center tick · mono caption</div>
    </div>
    <div class="sig">
      <p class="tombo-fig">S-03 — TICKS &amp; RULER</p>
      <ul class="tombo-ticks"><li>bullets become green ticks</li><li>the ruler reads its current value in shu</li></ul>
      <div class="tombo-ruler" style="--tombo-ruler-value:62%"></div>
    </div>
    <div class="sig">
      <p class="tombo-fig">S-04 — RUNNING NUMBERS</p>
      <p class="s-note">Headings on this page number themselves (<span class="tombo-mono">01 —</span>, <span class="tombo-mono">02 —</span>), and every figure carries a mono inscription like the one above.</p>
    </div>
    <div class="sig">
      <p class="tombo-fig">S-05 — SHU CURRENT POSITION</p>
      <nav class="tombo-tabs" aria-label="S-05 demo">
        <a href="#" aria-current="page">you are here</a>
        <a href="#">elsewhere</a>
      </nav>
    </div>
    <div class="sig sig--grid">
      <p class="tombo-fig">S-06 — GRAPH PAPER</p>
      <p class="s-note">The drafting grid behind the hero — full-bleed on an LP, margins only in docs, off in apps. At night, <span class="tombo-mono">.tombo-glow</span> lights it.</p>
    </div>
  </div>
</section>
```

テーマとトークン:

```html
<section class="sec tombo-shell">
  <h2 class="tombo-sec">Two themes</h2>
  <p class="lede">One umbrella name, two <span class="tombo-mono">data-theme</span> values: <b>tombo</b>, the day drawing, and <b>hotaru</b> (蛍, firefly), the night drawing where the instruments glow. Pages follow the OS by default; the toggle in the topbar forces one and remembers it — that part is <span class="tombo-mono">tombo.js</span>, optional by design. This page reads fine without it.</p>
  <div class="swatches">
    <div class="sw sw--paper"><i></i><span class="tombo-label">PAPER</span></div>
    <div class="sw sw--surface"><i></i><span class="tombo-label">SURFACE</span></div>
    <div class="sw sw--ink"><i></i><span class="tombo-label">INK</span></div>
    <div class="sw sw--ink-sub"><i></i><span class="tombo-label">INK-SUB</span></div>
    <div class="sw sw--green"><i></i><span class="tombo-label">GREEN</span></div>
    <div class="sw sw--shu"><i></i><span class="tombo-label">SHU</span></div>
  </div>
  <p class="s-note">Swatches are painted straight from <span class="tombo-mono">var(--tombo-*)</span> — flip the theme and they follow. 28 token pairs are gated against WCAG 2.1 floors in CI.</p>
</section>
```

Quick start(ピン 3 つ・v0.14.1):

```html
<section class="sec tombo-shell" id="quickstart">
  <h2 class="tombo-sec">Quick start</h2>
  <p class="lede">No npm, no CDN — vendor the files out of a release tag, then pin the tag and the sha256 in your own CI.</p>
  <figure class="tombo-code">
    <figcaption><span>SHELL — VENDOR FROM A TAG</span></figcaption>
    <pre tabindex="0">git -C /path/to/tombo show v0.14.1:tombo.css > public/styles/tombo.css
git -C /path/to/tombo show v0.14.1:LICENSE   > public/styles/tombo.LICENSE
git -C /path/to/tombo show v0.14.1:tombo.js  > public/scripts/tombo.js</pre>
  </figure>
  <figure class="tombo-code">
    <figcaption><span>HTML — LINK YOUR COPY + THE THREE VOICES</span></figcaption>
    <pre tabindex="0">&lt;link rel="stylesheet" href="/styles/tombo.css"&gt;
&lt;link rel="preconnect" href="https://fonts.googleapis.com"&gt;
&lt;link rel="preconnect" href="https://fonts.gstatic.com" crossorigin&gt;
&lt;link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@600;700&amp;family=M+PLUS+2:wght@450;500;700&amp;family=Martian+Mono:wdth,wght@75..112.5,400..600&amp;display=swap" rel="stylesheet"&gt;</pre>
  </figure>
  <p class="s-note">Full reference: <a href="https://github.com/wadakatu/tombo/tree/main/docs">docs/</a> · <a href="https://github.com/wadakatu/tombo#quick-start">README</a>.</p>
</section>
```

Volume dial(ライブ examples へ)+ footer + tombo.js:

```html
<section class="sec tombo-shell">
  <h2 class="tombo-sec">Three volumes</h2>
  <p class="lede">The same six marks, turned up or down per product. Every example below is a live page — flip the theme from inside it.</p>
  <div class="cards3">
    <a class="vol fcard tombo-flow tombo-metric tombo-corners" href="examples/docs.html">
      <p class="tombo-fig">VOL — DOCS</p>
      <h3>Quiet</h3>
      <p>Graph paper in the margins only. Dimension lines replace hr. Headings number themselves.</p>
      <div class="meta"><div class="tombo-label">EXAMPLES/DOCS.HTML</div></div>
    </a>
    <a class="vol fcard tombo-flow tombo-metric tombo-corners" href="examples/app.html">
      <p class="tombo-fig">VOL — APP</p>
      <h3>Functional</h3>
      <p>No grid. Instruments only — metrics, rulers, status. Shu points at the current nav.</p>
      <div class="meta"><div class="tombo-label">EXAMPLES/APP.HTML</div></div>
    </a>
    <a class="vol fcard tombo-flow tombo-metric tombo-corners" href="examples/lp.html">
      <p class="tombo-fig">VOL — LP</p>
      <h3>Loud</h3>
      <p>Full-bleed grid, hero frame, corners everywhere — and the glow, at night.</p>
      <div class="meta"><div class="tombo-label">EXAMPLES/LP.HTML</div></div>
    </a>
  </div>
  <p class="s-note"><a href="examples/components.html">Component catalog</a> — every component as a live demo with copy-paste markup.</p>
</section>
</main>

<footer class="tombo-footer">
  <div class="tombo-shell foot">
    <span class="tombo-logo" aria-hidden="true"><i class="h"></i><i class="b"></i><i class="w1"></i><i class="w2"></i><i class="t"></i></span>
    <div>TOMBO — WADAKATU DESIGN SYSTEM · MIT · VENDORED FROM A TAG<br>
      <a href="https://github.com/wadakatu/tombo">GITHUB.COM/WADAKATU/TOMBO</a>
    </div>
  </div>
</footer>

<script src="tombo.js" defer></script>
</body>
</html>
```

- [ ] **Step 4: 検証**

```bash
npm run check   # 全ゲート green(README 不変なので banner は従来どおり)
grep -c 'show v0.14.1:' index.html   # 期待: 3
```

chrome-devtools で `file:///…/tombo/index.html` を開き:
1. 昼(`data-theme="tombo"`)・夜(`hotaru`)のフルページスクリーンショット — 方眼・glow・朱・コーナーの発現を確認
2. `.tombo-sec` 見出しに `01 —` 〜 `05 —` の通し番号が出ていること
3. CTA `<a>` に下線がないこと(#17 の回帰確認)
4. 375px(resize)で cols / cards3 / sigs が 1 カラムに落ち、横スクロールが出ないこと

- [ ] **Step 5: Commit**

```bash
git add .nojekyll index.html assets/site.css
git commit -m "feat: intro site (EN) — dogfooded LP for GitHub Pages"
```

---

### Task 2: JA ページ(ja/index.html)

**Files:**
- Create: `ja/index.html`

**Interfaces:**
- Consumes: `assets/site.css`(Task 1 のクラス群をそのまま使用)
- Produces: `/ja/` の公開 URL(Task 1 の hreflang が指す先)

- [ ] **Step 1: index.html をコピーし、構造 diff を適用**

`cp index.html ja/index.html` してから、以下を機械的に置換:

| 対象 | index.html | ja/index.html |
|---|---|---|
| `<html lang>` | `en` | `ja` |
| 相対パス | `tombo.css` / `assets/site.css` / `tombo.js` / `examples/…` / `assets/logo/…` | すべて `../` 前置(`../tombo.css` 等) |
| 言語リンク | `<a href="ja/" lang="ja" hreflang="ja">日本語</a>` | `<a href="../" lang="en" hreflang="en">English</a>` |
| 銘の `lang="ja"` 属性 | あり(h3 / h1 small) | 削除(ページ全体が ja) |
| hreflang 3 行 | そのまま | そのまま(絶対 URL なので不変) |
| Quick start アンカー・ピン | `#quickstart` / `show v0.14.1:` × 3 | 同一(変更しない) |

- [ ] **Step 2: コピーを日本語化(置換表)**

| 箇所 | JA テキスト |
|---|---|
| `<title>` | `TOMBO — 測る印。wadakatu のシングルファイル CSS デザインシステム` |
| `<meta name="description">` | `TOMBO は wadakatu のシングルファイル・依存ゼロの CSS デザインシステム。6 つの署名要素、2 つのテーマ、「現在地」を指す一本の朱。` |
| h1 small | `測ってから、置く。`(そのまま。DISPLAY 見出し "The mark that measures." も Latin のまま維持 — DISPLAY voice は Latin 専用) |
| dimlab(hero) | `単一ファイル · 依存ゼロ · タグから vendoring` |
| tagline | `wadakatu が作るすべて — ドキュメント、アプリ、LP、ポートフォリオ — をひとつのスタイルシートで。6 つの署名要素を例外なく反復し、文脈に合わせて「音量」だけを変える: ドキュメントでは静かに、LP では最大音量で。` |
| CTA | `スタイルシートを入手` / `GitHub で見る` |
| 三原則 dimlab | `憲法 — 三原則 / 例外なし` |
| 三原則 h2 | `三原則` |
| R-01 本文 | `要素は寸法線・目盛・通し番号の隣に置かれる。「置く前に測った」という気配が、ページの空気を作る。` |
| R-02 本文 | `数字・ラベル・インデックス・単位は必ず等幅。本文は静かなサンセリフに保ち、計器だけが等幅で光る。` |
| R-03 本文 | `赤は「ここ」を指す 1–2px の線にだけ使う。現在のタブ、現在の目次、現在の値。面を塗った瞬間、それは朱ではなくただの赤になる。` |
| 署名 h2 / lede | `6 つの署名要素` / `コンポーネントライブラリではなく、指紋。以下のタイルはすべて絵ではなく実物。` |
| S-01 s-note | `「合っている」ことを示す 12px のブラケット。いままさに見えている — このタイルは四隅すべてを着けている。` |
| S-02 dimlab | `測る hr — 両端の罫 · 中央のティック · 等幅の銘` |
| S-03 li × 2 | `箇条書きは green のティックになる` / `ルーラーは現在値を朱で読む` |
| S-04 s-note | `このページの見出しは自ら番号を刻み(01 —、02 —)、すべての図版が上のような等幅の銘を持つ。` |
| S-06 s-note | `ヒーローの背後にある製図の方眼 — LP ではフルブリード、ドキュメントでは余白のみ、アプリではオフ。夜は .tombo-glow が灯す。` |
| (共通) | mono ラベル(`S-01 — REGISTRATION CORNERS` 等)は Latin のまま |
| テーマ h2 / lede / s-note | `2 つのテーマ` / lede: `傘はひとつ、data-theme は 2 つ: 昼の図面 tombo と、計器が発光する夜の図面 hotaru(蛍)。既定では OS に追従し、トップバーのトグルで固定・記憶できる — その部分が tombo.js(設計上オプション)。このページは JS なしでも完全に読める。` / s-note: `スウォッチは var(--tombo-*) を直接塗っている — テーマを切り替えれば追従する。28 のトークンペアを WCAG 2.1 の下限値で CI ゲートしている。` |
| Quick start h2 / lede / s-note | `クイックスタート` / `npm も CDN もなし — リリースタグからファイルを vendoring し、タグと sha256 を自分の CI でピン留めする。` / `詳細リファレンス: docs/ · README。` |
| Volume h2 / lede / s-note | `3 つの音量` / `同じ 6 つの署名を、プロダクトごとに上げ下げする。以下はすべてライブページ — 中からテーマを切り替えられる。` / `コンポーネントカタログ — 全部品をライブデモ + コピペ用マークアップで。` |
| vol h3 × 3 | `静かに` / `機能的に` / `最大音量` |
| vol 本文 × 3 | docs: `方眼は余白にだけ。hr の代わりに寸法線。見出しは自ら番号を刻む。` / app: `方眼なし。計器だけ — メトリクス、ルーラー、ステータス。朱が現在のナビを指す。` / lp: `方眼はフルブリード、ヒーローに枠、四隅に見当 — そして夜は、発光。` |
| S-05 タブ | `現在地` / `よそ` |
| footer | `TOMBO — WADAKATU DESIGN SYSTEM · MIT · VENDORED FROM A TAG`(Latin 銘のまま) |

- [ ] **Step 3: 検証**

```bash
grep -c 'show v0.14.1:' ja/index.html        # 期待: 3
grep -c 'href="\.\./' ja/index.html          # 相対パスの ../ 前置を目視でも確認
npm run check
```

chrome-devtools で `file:///…/tombo/ja/index.html` を開き、昼夜 2 テーマのスクリーンショット + 375px 確認 + 言語リンクで EN⇄JA が往復できること(file:// では `../` → ディレクトリ表示になるため、`python3 -m http.server` でルートから配信して確認する)。和欧混植(text-autospace)が JA 本文で効いていることを目視。

- [ ] **Step 4: Commit**

```bash
git add ja/index.html
git commit -m "feat: intro site (JA) — /ja/ mirror with link-based language switch"
```

---

### Task 3: check_banner.py — サイトのピンも検査

**Files:**
- Modify: `scripts/check_banner.py`

**Interfaces:**
- Consumes: `index.html` / `ja/index.html`(Task 1–2 で作成済み、各ちょうど 3 ピン)
- Produces: 拡張された CI ゲート(README 3 + site 3×2 + バナー 2 の全一致)

- [ ] **Step 1: pin 収集を複数ファイル化**

`readme_pin_versions` を `pin_versions` にリネームし、`main()` の pins ブロックを置き換える:

```python
def pin_versions(path: Path) -> list[str]:
    # lines like: git -C /path/to/tombo show v0.12.0:tombo.css > ...
    return [m.group(1) for m in re.finditer(r"show v(\d+\.\d+\.\d+):", path.read_text())]
```

```python
    # main() 内 — 旧: pins = readme_pin_versions(...) / if len(pins) != 3 ブロックを削除して:
    pin_sources = [("README.md", 3), ("index.html", 3), ("ja/index.html", 3)]
    ok = True
    for name, want in pin_sources:
        got = pin_versions(ROOT / name)
        if len(got) != want:
            print(f"FAIL  expected {want} vendoring pins in {name}, found {len(got)}")
            ok = False
        for i, p in enumerate(got, 1):
            versions[f"{name} pin {i}"] = p
    if not ok:
        return 1
```

(versions 表示・全一致 assert・タグ照合のロジックは不変。docstring の「three README vendoring pins」を「README + index.html + ja/index.html の各 3 ピン」に更新)

- [ ] **Step 2: red を確認(わざと壊す)**

```bash
sed -i '' '0,/show v0.14.1:tombo.css/s//show v0.9.9:tombo.css/' index.html
python3 scripts/check_banner.py   # 期待: FAIL version mismatch(exit 1)
git checkout index.html           # 復元
```

- [ ] **Step 3: green を確認**

```bash
python3 scripts/check_banner.py   # 期待: PASS all banners and pins agree: v0.14.1(pin 行が 9 本出る)
npm run check                     # 全ゲート green
```

- [ ] **Step 4: Commit**

```bash
git add scripts/check_banner.py
git commit -m "ci: gate the intro site's vendoring pins in check_banner"
```

---

### Task 4: Opus whole-branch review + 修正

- [ ] **Step 1:** Agent(model: opus)に `git diff main...feature/pages-site` の全量レビューを依頼。観点: spec 準拠(8 節すべて)/ 朱・純白純黒・影の掟 / DISPLAY voice が Latin のみか / a11y(lang 属性・aria-current・tabindex 付き pre・リンクテキスト)/ EN⇄JA の内容同期 / 相対パスと hreflang / site.css がトークンのみ参照しているか / check_banner 拡張のエッジ(pin 0 個ファイル等)
- [ ] **Step 2:** 指摘を修正し、`npm run check` + 昼夜スクリーンショット再確認 → `fix:` で commit

---

### Task 5: PR → merge → Pages 有効化 → ライブ検証

- [ ] **Step 1:** pre-pr-walkthrough(メインセッション: 変更概要 → ユーザー承認)→ /pr で PR 作成(`Fixes #18`、up to date 確認)
- [ ] **Step 2:** CI green → rebase-merge
- [ ] **Step 3:** Pages 有効化 + homepage 設定:

```bash
gh api -X POST repos/wadakatu/tombo/pages --input - <<'EOF'
{"source": {"branch": "main", "path": "/"}}
EOF
gh repo edit wadakatu/tombo --homepage "https://wadakatu.github.io/tombo/"
```

- [ ] **Step 4:** Pages のビルド完了(`gh api repos/wadakatu/tombo/pages --jq .status` が `built`)を待ち、https://wadakatu.github.io/tombo/ と /ja/ を chrome-devtools で開いて昼夜スクリーンショット・言語往復・テーマ永続・コピーボタンをライブ確認
- [ ] **Step 5:** メモリ(tombo-overview / tombo-repo-conventions)に Pages URL を追記
