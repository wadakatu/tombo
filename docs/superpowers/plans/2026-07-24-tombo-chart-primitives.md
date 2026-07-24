# TOMBO 図版(チャート)プリミティブ Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** issue #15 — 消費側がページ CSS ゼロで tombo 流の棒グラフ + ツールチップ + 数表を組めるチャート語彙(`.tombo-plate` / `.tombo-tip` / `.tombo-numbers`)を tombo.css に追加し、規範を catalog/README に明文化して v0.13.0 として出す。

**Architecture:** `@layer tombo.components` の新ブロック 1 つ(checkbox/radio ブロックの後・unlayered print 節の前)+ print 硬化 2 行。チャート内部クラスは `.tombo-plate` 配下に scoped(グローバル `.bar` を作らない)。JS 変更なし(tombo.js は state-only)。新トークン・新色なし。

**Tech Stack:** 手書き CSS(tombo.css 単一ファイル)、検証は `npm run check`(stylelint Baseline gate / contrast / size / banner / node --check)+ chrome-devtools MCP の computed style 実測とスクリーンショット(昼夜 2 テーマ)。

**Spec:** `docs/superpowers/specs/2026-07-24-tombo-chart-primitives-design.md`(CSS 全文・markup 契約・規範 5 項はここが正)

## Global Constraints

- 追加のみ・非破壊。既存セレクタの変更は print 節の 2 リスト(分割禁止・非印刷)への追記だけ。
- 新トークン・新色を作らない(色は既存ペアのみ → contrast gate 37 PASS 不変)。
- Baseline widely 内の CSS のみ(stylelint gate が強制。PE ledger への追加はしない)。
- インライン custom property の許可は `--tombo-ruler-value` のみ(規範)— `--tombo-plate-min` の上書きはスタイルシートで。
- コミットは英語 Conventional Commits、`Co-Authored-By` 禁止。
- 朱は線専用(`.now` は stroke のみ、面塗りの朱を作らない)。
- サイズ予算: `tombo.css` gzip ≤ 12KiB(現在 ~10.2KB、追加 ~1.4KB raw 見込みで余裕)。

---

### Task 1: tombo.css — 図版ブロック + print 硬化

**Files:**
- Modify: `tombo.css` — `@layer tombo.components`(checkbox/radio ブロック、`.tombo-fieldset > legend` の閉じ以降)と print 節の 2 行
- Test: `npm run check` + scratch ページの computed style 実測

**Interfaces:**
- Produces: `.tombo-plate`(枠)/ `.tombo-plate svg`(`min-inline-size: var(--tombo-plate-min, 560px)`)/ `.tombo-plate .axis|.base|.bar|.is-zero|.val|.now|text` / `.tombo-tip`(+ `> b`)/ `.tombo-numbers`(`<details>` 用、`> summary`)。Task 2 の catalog/README はこの名前をそのまま使う。

- [ ] **Step 1: 「failing test」= scratch ページを先に作る**

`/private/tmp/claude-501/-Users-wadakatu-www-oss-tombo/1c4aef00-50d5-40af-b6bf-2bb261c678d5/scratchpad/plate-test.html` に、spec の markup 契約どおりの図版(枠 + SVG + tip + numbers)を tombo.css 参照で置く。CSS 追加前に chrome-devtools で開き、`.bar` の fill が green で**ない**こと(SVG 既定の black)、`.tombo-plate` に border が**ない**ことを確認 — これが red 状態。

- [ ] **Step 2: tombo.css に図版ブロックを追加**

`.tombo-fieldset > legend` を含む `@layer tombo.components` ブロックの閉じ括弧(`}`)の直後・`/* ── print ──` コメントの前に、spec「設計(CSS)」節の CSS 全文を挿入する(spec が正 — コメント含めそのまま)。

- [ ] **Step 3: print 節の 2 リストに追記**

```css
/* before */
.tombo-themes, .tombo-copy { display: none; }
/* after */
.tombo-themes, .tombo-copy, .tombo-tip { display: none; }

/* before */
.tombo-metric, .tombo-callout, .tombo-code, figure, tr, .tombo-check { break-inside: avoid; }
/* after */
.tombo-metric, .tombo-callout, .tombo-code, figure, tr, .tombo-check, .tombo-plate { break-inside: avoid; }
```

- [ ] **Step 4: gate + 実測で green を確認**

Run: `npm run check` → 5 ゲート全部 PASS(stylelint に Baseline 違反が出ないこと = 新規則が widely 内である証明)。
chrome-devtools で scratch ページを再読み込みし computed style を実測:
- `.tombo-plate` — `border: 1px solid` hairline 実値、`padding: 24px`、`position: relative`、`overflow-x: auto`
- `svg` — `min-inline-size: 560px`
- `.bar` fill = green 実値(昼 `rgb(14, 90, 71)`)、`.is-zero` fill = hairline 実値
- `.base` stroke = ink・`stroke-width: 1.5`、`.axis` stroke = hairline・1、`.now` stroke = shu 実値(昼 `rgb(216, 68, 43)`)・2
- `text` — `font-family` に Martian Mono、`font-size: 10.5px`、fill = ink-faint 実値、`.val` fill = ink・`font-weight: 600`
- `.tombo-tip` — `display: none`(既定)。デモ的に `display:block` を当てれば surface 背景 + ink 1px 罫 + `padding: 8px 12px`
- `.tombo-numbers > summary` — mono・10.5px・`cursor: pointer`、`[open] > summary` の `margin-block-end: 12px`
- 480px 幅に絞って `.tombo-plate` が枠内スクロール(`scrollWidth > clientWidth`)し、`document.documentElement.scrollWidth == clientWidth`(ページは溢れない)

- [ ] **Step 5: Commit**

```bash
git add tombo.css
git commit -m "feat: add the 図版 chart vocabulary — .tombo-plate, .tombo-tip, .tombo-numbers"
```

---

### Task 2: catalog #c19 + README「Charts (図版)」

**Files:**
- Modify: `examples/components.html` — toc(c18 の次)+ `#c19` 節(c18 節の後)+ catalog `<style>` にデモ用 tip 静置 1 行
- Modify: `README.md` — `## Forms` と `## Print` の間に `## Charts (図版)`

**Interfaces:**
- Consumes: Task 1 の全クラス名(そのまま)。
- Produces: なし(ドキュメントのみ)。

- [ ] **Step 1: toc にエントリ追加**

`<a href="#c18">18 — 印刷</a>` の直後:

```html
        <a href="#c19">19 — 図版</a>
```

- [ ] **Step 2: catalog `<style>` にデモ用の tip 静置を追加**

`.foot { … }` 行の前に(カタログのデモはページ JS ゼロ — tip を見せるための display/position 上書き):

```css
  #c19 .tombo-tip { display: inline-block; position: static; margin-top: var(--tombo-space-16); }
```

- [ ] **Step 3: `#c19` 節を c18 の `</section>` の直後に追加**

データは 2026-W30(MON 07/20〜SUN 07/26、今日 = FRI 07/24)。値 4/9/0/21/6/12/3、軸最大 24、ピーク THU 23(`.val`)、`.now` は FRI の下。`.tombo-tip` の中身は `white-space: pre` なので**各行を行頭から書く**(インデント禁止):

```html
      <section id="c19">
        <h2 class="tombo-sec">図版</h2>
        <p class="note">S-03「グラフ軸」の部品化。<code>.tombo-plate</code>(=版)が図版枠 — hairline罫 + padding、溢れたら枠内だけが横スクロールする(SVGの最小幅は <code>--tombo-plate-min</code>、既定560px。上書きはスタイルシートで — インラインcustom propertyは <code>--tombo-ruler-value</code> だけ)。銘は既存の <code>.tombo-fig</code> を <code>&lt;figcaption&gt;</code> に載せて枠の上に置く。チャート内部は枠配下でだけ効く — <code>.axis</code>(hairline目盛線)/ <code>.base</code>(ink基線)/ <code>.bar</code>(green面、<code>.is-zero</code> はhairline)/ <code>.val</code>(値ラベル)/ <code>.now</code>(朱の現在地)。SVGの <code>text</code> は自動で等幅・label段・ink-faintになる(銘は等幅)。</p>
        <p class="note">規範: <b>軸は1本</b>(ink基線のみ、第2軸は作らない)・<b>目盛線はhairline</b>・<b>単系列はgreen一色</b>(多系列の色分けはしない — 系列が増えたら図を分ける)・<b>値ラベルは選択的</b>(ピークだけ。全記入は数表の仕事)・<b>朱は現在地のみ</b>(選択中の週・今日を指す線。データには使わない)。</p>
        <div class="demo">
          <figure>
            <figcaption class="tombo-fig">FIG. 19 — DAILY CONTRIBUTIONS · W30</figcaption>
            <div class="tombo-plate" style="margin-top:12px">
              <svg viewBox="0 0 720 200" role="img" aria-label="日別コントリビューション数の棒グラフ(デモ)">
                <line class="axis" x1="34" y1="24" x2="710" y2="24"/>
                <line class="axis" x1="34" y1="98" x2="710" y2="98"/>
                <text x="28" y="27" text-anchor="end">24</text>
                <text x="28" y="101" text-anchor="end">12</text>
                <text x="28" y="175" text-anchor="end">0</text>
                <rect class="bar" x="58" y="147" width="48" height="25"/>
                <rect class="bar" x="155" y="116" width="48" height="56"/>
                <rect class="bar is-zero" x="251" y="170" width="48" height="2"/>
                <rect class="bar" x="348" y="42" width="48" height="130"/>
                <rect class="bar" x="445" y="135" width="48" height="37"/>
                <rect class="bar" x="541" y="98" width="48" height="74"/>
                <rect class="bar" x="638" y="154" width="48" height="18"/>
                <text class="val" x="372" y="35" text-anchor="middle">21</text>
                <line class="now" x1="441" y1="177" x2="497" y2="177"/>
                <line class="base" x1="34" y1="172" x2="710" y2="172"/>
                <text x="82" y="192" text-anchor="middle">MON 20</text>
                <text x="179" y="192" text-anchor="middle">TUE 21</text>
                <text x="275" y="192" text-anchor="middle">WED 22</text>
                <text x="372" y="192" text-anchor="middle">THU 23</text>
                <text x="469" y="192" text-anchor="middle">FRI 24</text>
                <text x="565" y="192" text-anchor="middle">SAT 25</text>
                <text x="662" y="192" text-anchor="middle">SUN 26</text>
              </svg>
<div class="tombo-tip" role="presentation"><b>07/23 THU — 21</b>COMMITS      14
PR MERGED     4
REVIEWS       3</div>
            </div>
            <details class="tombo-numbers" open>
              <summary>NUMBERS — 数表を開く</summary>
              <div class="tombo-table-wrap" role="region" aria-label="日次の数表(デモ)" tabindex="0">
                <table class="tombo-table">
                  <thead><tr><th>DATE</th><th>COMMITS</th><th>TOTAL</th></tr></thead>
                  <tbody>
                    <tr><td class="tombo-mono">07/22 WED</td><td class="tombo-mono">0</td><td class="tombo-mono">0</td></tr>
                    <tr><td class="tombo-mono">07/23 THU</td><td class="tombo-mono">14</td><td class="tombo-mono">21</td></tr>
                  </tbody>
                </table>
              </div>
            </details>
          </figure>
        </div>
        <figure class="tombo-code">
          <figcaption><span>HTML</span><span>.TOMBO-PLATE / .TOMBO-TIP / .TOMBO-NUMBERS</span></figcaption>
          <pre tabindex="0">&lt;figure&gt;
  &lt;figcaption class="tombo-fig"&gt;FIG. 01 — DAILY CONTRIBUTIONS&lt;/figcaption&gt;
  &lt;div class="tombo-plate"&gt;
    &lt;svg viewBox="0 0 720 200" role="img" aria-label="日別コントリビューション数の棒グラフ"&gt;
      &lt;line class="axis" …/&gt;&lt;text …&gt;12&lt;/text&gt;   &lt;!-- hairlineの目盛線 + 等幅の銘 --&gt;
      &lt;rect class="bar" … tabindex="0" aria-label="07/23 THU: 21"/&gt;
      &lt;rect class="bar is-zero" …/&gt;              &lt;!-- ゼロ値は2pxスタブ --&gt;
      &lt;text class="val" …&gt;21&lt;/text&gt;              &lt;!-- 値ラベルはピークだけ --&gt;
      &lt;line class="now" …/&gt;                      &lt;!-- 朱は現在地のみ --&gt;
      &lt;line class="base" …/&gt;                     &lt;!-- 軸はこの1本 --&gt;
    &lt;/svg&gt;
    &lt;div class="tombo-tip" role="presentation"&gt;&lt;b&gt;07/23 THU — 21&lt;/b&gt;COMMITS 14&lt;/div&gt;
  &lt;/div&gt;
  &lt;details class="tombo-numbers"&gt;
    &lt;summary&gt;NUMBERS — 数表を開く&lt;/summary&gt;
    &lt;div class="tombo-table-wrap" role="region" aria-label="日次の数表" tabindex="0"&gt;
      &lt;table class="tombo-table"&gt;…&lt;/table&gt;
    &lt;/div&gt;
  &lt;/details&gt;
&lt;/figure&gt;</pre>
        </figure>
        <p class="note">ツールチップはこのデモでは見せるために静置している(カタログはページJSゼロ)。実装では既定 <code>display:none</code> — 消費側JSが <code>display</code> を立て、<code>transform: translate(x, y)</code> で置く。アクセシブルなデータ経路は数表が担い、ツールチップは視覚の補助(<code>role="presentation"</code>・<code>pointer-events:none</code>)。インタラクティブなバーには <code>tabindex="0"</code> と <code>aria-label</code> を振る。枠がスクロールし得るのに中にフォーカス可能要素が無い図では、テーブルと同じ作法(<code>role="region"</code> + アクセシブル名 + <code>tabindex="0"</code>)を枠に付ける。</p>
      </section>
```

- [ ] **Step 4: README に `## Charts (図版)` 節を追加**

`## Print` 見出しの直前に:

```markdown
## Charts (図版)

Charts are instruments too. `.tombo-plate` frames a figure — hairline border, `--tombo-space-24` padding, and overflow that scrolls **inside** the frame, never the page. Everything a bar chart needs is a class scoped under the plate, so the norms live in the vocabulary instead of each consuming page. The caption stays `.tombo-fig` (the existing S-04 mono 銘) on a `<figcaption>` above the frame.

| Class | Role |
|---|---|
| `.tombo-plate` | the figure frame; the SVG inside is fluid with `min-inline-size: var(--tombo-plate-min, 560px)` |
| `.axis` / `.base` | hairline gridlines / the single ink baseline — the only axis |
| `.bar` / `.bar.is-zero` | green single-series bars / hairline zero stubs (2px) |
| `.val` | the selective value label (ink, 600) — peaks only |
| `.now` | the shu current-position line — never a data series |
| `.tombo-tip` | the tooltip panel (surface, ink border, mono note voice) — your JS shows and positions it |
| `.tombo-numbers` | the `<details>` disclosure for the figure's data table |

```html
<figure>
  <figcaption class="tombo-fig">FIG. 01 — DAILY CONTRIBUTIONS</figcaption>
  <div class="tombo-plate">
    <svg viewBox="0 0 720 200" role="img" aria-label="日別コントリビューション数の棒グラフ">
      <line class="axis" … /><text …>12</text>
      <rect class="bar" … tabindex="0" aria-label="07/23 THU: 21" />
      <rect class="bar is-zero" … />
      <text class="val" …>21</text>
      <line class="now" … />
      <line class="base" … />
    </svg>
    <div class="tombo-tip" role="presentation"><b>07/23 THU — 21</b>COMMITS 14</div>
  </div>
  <details class="tombo-numbers">
    <summary>NUMBERS — 数表を開く</summary>
    <div class="tombo-table-wrap" role="region" aria-label="日次の数表" tabindex="0">
      <table class="tombo-table">…</table>
    </div>
  </details>
</figure>
```

The norms are part of the system: **one axis** (the ink baseline), hairline gridlines, **one green** for a single series (need a second series? split the figure — there is no categorical palette), **selective value labels** (peaks only; the full record belongs to the table), and **shu strictly for "you are here"** (the selected week, today — never a data color).

`text` inside a plate is automatically mono, label-size, ink-faint (銘は等幅). The `<details class="tombo-numbers">` table is the accessible data channel; the tooltip is a visual aid (`role="presentation"`, `pointer-events: none`) that your JS toggles (`display`) and places (`transform: translate(x, y)`) — no JS, no tooltip, and the figure still reads. Interactive bars get `tabindex="0"` + `aria-label`. Override the minimum width in your stylesheet, not inline:

```css
.trend .tombo-plate { --tombo-plate-min: 900px; } /* one wide figure */
```
```

- [ ] **Step 5: 検証(昼夜 2 テーマ + a11y)**

- chrome-devtools で `examples/components.html#c19` を開き、tombo(昼)/hotaru(夜)両テーマでスクリーンショット。確認: バー green・ゼロ値 hairline・基線 ink・`.now` 朱・軸ラベル mono/faint・`.val` ink 600・tip パネル(surface + ink 罫)・数表 open。
- toc「19 — 図版」からのアンカー遷移、`details` の開閉(JS ゼロ)動作。
- 狭幅(~480px)で `.tombo-plate` の枠内スクロール発動・ページ非溢れを確認。
- `npm run check` green のまま。

- [ ] **Step 6: Commit**

```bash
git add examples/components.html README.md
git commit -m "docs: add the 図版 section to the catalog and README"
```

---

### Task 3: v0.13.0 バージョン bump

**Files:**
- Modify: `tombo.css:1`(banner)/ `tombo.js:1`(banner)/ `README.md` vendoring pins(`v0.12.0` 参照 3 箇所)

**Interfaces:**
- Consumes: なし。Produces: タグ `v0.13.0` と整合する banner(check_banner.py がタグ push 時に強制)。

- [ ] **Step 1: 現在の v0.12.0 参照を列挙**

Run: `grep -n "v0\.12\.0" tombo.css tombo.js README.md`
Expected: tombo.css:1、tombo.js:1、README の pins 3 箇所(合計 5 行)。

- [ ] **Step 2: 全箇所を v0.13.0 に置換**(banner 2 + README pins 3)

- [ ] **Step 3: banner ゲートで検証**

Run: `npm run check`
Expected: `check_banner.py` PASS(css == js banner == README pins)。他ゲートも green。

- [ ] **Step 4: Commit**

```bash
git add tombo.css tombo.js README.md
git commit -m "chore: bump banners and vendoring pins to v0.13.0"
```

---

### Task 4: Opus whole-branch review + 修正

- [ ] **Step 1:** Agent(model: opus)に `git diff main...feature/chart-primitives` の全量レビューを依頼(観点: spec 準拠・規範の一貫性・a11y 契約・カタログ HTML の実 geometry・print 追記の妥当性・README の正確さ)。
- [ ] **Step 2:** Critical/Important は修正して追コミット(`fix:`/`docs:`)、Minor は判断の上対応 or 記録。
- [ ] **Step 3:** 修正後 `npm run check` + 両テーマ再スクリーンショット。

---

### Task 5: リリース(linear history)

- [ ] **Step 1:** `git checkout main && git merge --ff-only feature/chart-primitives`
- [ ] **Step 2:** `git tag v0.13.0`(lightweight)
- [ ] **Step 3:** `git push origin main && git push origin v0.13.0`
- [ ] **Step 4:** CI(push run)green を確認(`gh run watch` / `gh run list`)
- [ ] **Step 5:** issue #15 をクローズ(実装内容・命名変更 `.tombo-fig`→`.tombo-plate` の理由をコメント)
- [ ] **Step 6:** ブランチ削除、メモリ更新
