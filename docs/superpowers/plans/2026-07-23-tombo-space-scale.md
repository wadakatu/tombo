# TOMBO Space Scale Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a 4px-based `--tombo-space-*` token scale and a `.tombo-flow` vertical-rhythm utility, then migrate the four examples off ~19 hand-rolled spacing values onto them.

**Architecture:** Additive/non-breaking. New tokens live in `@layer tombo.tokens`, the `.tombo-flow` utility in `@layer tombo.utilities` (owl selector `> * + *` + `margin-block-start: var(--tombo-flow-space)`, default `--tombo-space-24`). Examples adopt `.tombo-flow` on their vertical content columns (with per-child `--tombo-flow-space` overrides) and reference tokens for grid/flex `gap` and `padding`. tombo.css component-internal padding is NOT touched (roadmap item B, a later breaking release).

**Tech Stack:** Plain CSS (`@layer`, custom properties, logical properties). No build, no JS test runner. Verification = grep + chrome-devtools computed-style/screenshots + `check_contrast.py` + `node --check`.

## Global Constraints

- **Exact scale (px, `@layer tombo.tokens`):** `--tombo-space-4:4px; -8:8px; -12:12px; -16:16px; -24:24px; -32:32px; -48:48px; -72:72px; -96:96px;` — 9 tokens, pixel-encoded names (name = value). 24 and up are multiples of 24 (grid-aligned).
- **`.tombo-flow` contract:** `.tombo-flow { --tombo-flow-space: var(--tombo-space-24); }` and `.tombo-flow > * + * { margin-block-start: var(--tombo-flow-space); }`. Per-context override by setting `--tombo-flow-space` on a child element.
- **Non-breaking:** no token renames/removals, no color changes, no tombo.css component-padding changes. `@layer` order unchanged (`reset, tokens, base, components, utilities`).
- **Role→token rounding (applied verbatim in migration tasks):** body reading rhythm 14→`-16`; block rhythm 24→`-24`; section rhythm 52/56/64→`-48`/`-72` per task; tight secondary 7/10→`-8`; 12→`-12`; 16→`-16`; 18→`-16`; 20→`-24`; 22/26/28→`-24`; 32→`-32`; 40→`-48`; 48→`-48`; 76→`-72`.
- **lp empirically-tuned values are literals, not rounded:** `.hero .cols` `gap:56px` and the `min-width:841–1099px` mid-band overrides are tied by comment to the 840px stacking breakpoint. Tokenize only where the literal already equals a token (32→`-32`, 16→`-16`); keep 56px and 20px as literals with their comments.
- **Version:** v0.8.0 (additive minor). Bump `tombo.css:1` and `tombo.js:1` banners and README vendoring pins (lines with `v0.7.0:`) to v0.8.0.
- **Verify every visual change in both `tombo` (day) and `hotaru` (night); example drift is intentional — verify "looks intentional," not "identical."**

---

### Task 1: Add the `--tombo-space-*` token scale

**Files:**
- Modify: `tombo.css` `@layer tombo.tokens` (insert after the `--tombo-shell-gutter`/`--tombo-shell` block, before the `/* instruments */` comment near line 30)

**Interfaces:**
- Produces: custom properties `--tombo-space-4|8|12|16|24|32|48|72|96` on `:root`, resolving to `4px…96px`.

- [ ] **Step 1: Add the token block.** Insert into `@layer tombo.tokens` `:root`, immediately before `/* instruments */`:

```css
    /* space scale — 4px base; 24 and up are multiples of the 24px grid cell.
       Names are pixel-encoded (the name is the measurement). See spec §7. */
    --tombo-space-4:   4px;
    --tombo-space-8:   8px;
    --tombo-space-12:  12px;
    --tombo-space-16:  16px;
    --tombo-space-24:  24px;   /* one grid cell — default block rhythm */
    --tombo-space-32:  32px;
    --tombo-space-48:  48px;   /* 2 cells */
    --tombo-space-72:  72px;   /* 3 cells — docs section rhythm */
    --tombo-space-96:  96px;   /* 4 cells — LP section rhythm */
```

- [ ] **Step 2: Verify tokens resolve (chrome-devtools, controller-run).** Load any example; run:

```js
() => { const cs = getComputedStyle(document.documentElement);
  return ['4','8','12','16','24','32','48','72','96'].map(n => n + '=' + cs.getPropertyValue('--tombo-space-'+n).trim()); }
```
Expected: `["4=4px","8=8px","12=12px","16=16px","24=24px","32=32px","48=48px","72=72px","96=96px"]`.

- [ ] **Step 3: Contrast gate (hygiene) + commit.**

```bash
python3 scripts/check_contrast.py   # expect all PASS (no color changed)
git add tombo.css
git commit -m "feat: add the --tombo-space-* 4px token scale"
```

---

### Task 2: Add the `.tombo-flow` utility

**Files:**
- Modify: `tombo.css` `@layer tombo.utilities` (append near the end of that layer, after `.tombo-sr-only`/existing utilities)

**Interfaces:**
- Consumes: `--tombo-space-24` (Task 1).
- Produces: `.tombo-flow` class + settable `--tombo-flow-space` custom property.

- [ ] **Step 1: Add the utility.** Append to `@layer tombo.utilities`:

```css
  /* flow — vertical rhythm between stacked children (Every Layout "Stack" /
     Andy Bell "flow"). Override --tombo-flow-space on the container or on any
     child to change the space that precedes it. Default is one grid cell. */
  .tombo-flow { --tombo-flow-space: var(--tombo-space-24); }
  .tombo-flow > * + * { margin-block-start: var(--tombo-flow-space); }
```

- [ ] **Step 2: Verify behavior (chrome-devtools, controller-run).** In the console of a loaded example:

```js
() => { const d=document.createElement('div'); d.className='tombo-flow';
  d.innerHTML='<p>a</p><p id=x>b</p>'; document.body.appendChild(d);
  const first=getComputedStyle(d.firstElementChild).marginBlockStart;
  const second=getComputedStyle(d.querySelector('#x')).marginBlockStart;
  d.querySelector('#x').style.setProperty('--tombo-flow-space','var(--tombo-space-48)');
  const overridden=getComputedStyle(d.querySelector('#x')).marginBlockStart;
  d.remove(); return {first, second, overridden}; }
```
Expected: `{first:"0px", second:"24px", overridden:"48px"}` (first child no margin; default 24; override 48).

- [ ] **Step 3: `node --check` (unchanged file, sanity) + commit.**

```bash
node --check tombo.js   # untouched; sanity only
git add tombo.css
git commit -m "feat: add the .tombo-flow vertical-rhythm utility"
```

---

### Task 3: Migrate docs.html

**Files:**
- Modify: `examples/docs.html` (`<style>` lines 13–29; `<main>` tag line 45)

**Interfaces:**
- Consumes: tokens (Task 1), `.tombo-flow` (Task 2).

- [ ] **Step 1: Add `.tombo-flow` to the content column.** Change `<main class="tombo-sections">` (line 45) to `<main class="tombo-sections tombo-flow">`.

- [ ] **Step 2: Rewrite the `<style>` block.** Replace lines 13–29 with (tokenized gaps/padding; margin-top rules replaced by flow overrides; `max-inline-size` kept):

```css
  .layout { display: grid; grid-template-columns: 200px 1fr; gap: var(--tombo-space-48); padding-block: var(--tombo-space-48) var(--tombo-space-72); align-items: start; }
  .side { position: sticky; top: var(--tombo-space-48); }
  .brand { font-family: var(--tombo-font-display); font-weight: 700; font-size: 16px; }
  .brand small { display: block; font-family: var(--tombo-font-mono); font-weight: 400; font-size: var(--tombo-text-label); color: var(--tombo-ink-faint); letter-spacing: .12em; margin-top: var(--tombo-space-4); }
  .side .tombo-toc { margin-top: var(--tombo-space-24); }
  /* min-inline-size: 0 lets the code block scroll instead of widening the grid track */
  main.tombo-sections { counter-reset: tombo-section 1; min-inline-size: 0; --tombo-flow-space: var(--tombo-space-16); }
  main.tombo-sections > .tombo-sec { --tombo-flow-space: var(--tombo-space-4); }        /* eyebrow → title, tight */
  main.tombo-sections > :is(h3, .tombo-callout, .tombo-code, .tombo-table-wrap) { --tombo-flow-space: var(--tombo-space-24); }
  main.tombo-sections > .tombo-dim { --tombo-flow-space: var(--tombo-space-32); }
  main.tombo-sections > .tombo-dimlab { --tombo-flow-space: var(--tombo-space-8); }     /* dim line → caption, tight */
  main p { font-size: var(--tombo-text-body); line-height: var(--tombo-lh-body); color: var(--tombo-ink-sub); max-inline-size: var(--tombo-shell-reading); }
  main h3, main .tombo-callout { max-inline-size: var(--tombo-shell-reading); }
  main .tombo-dim { max-inline-size: var(--tombo-shell-reading); }
  @media (max-width: 680px) {
    .layout { grid-template-columns: 1fr; gap: var(--tombo-space-24); }
    .side { position: static; }
  }
  .foot { display: flex; align-items: center; gap: var(--tombo-space-16); }
```

- [ ] **Step 3: Verify (chrome-devtools, controller-run) — both themes.** Load `examples/docs.html`; screenshot in `tombo` and `hotaru`. Confirm: (a) eyebrow "DOCS / GETTING-STARTED / 02" sits tight above the "インストール" title; (b) body paragraph rhythm reads slightly looser than before but even; (c) code/callout/table blocks separated by one grid cell; (d) no leftover top margin on the first element. Grep: `awk '/<style>/,/<\/style>/' examples/docs.html | grep -nE '[0-9]+px'` shows only `200px`, `16px` (brand font-size), and breakpoint `680px` — no spacing px literals remain.

- [ ] **Step 4: Commit.**

```bash
git add examples/docs.html
git commit -m "refactor: migrate docs.html spacing to the space scale and .tombo-flow"
```

---

### Task 4: Migrate components.html

**Files:**
- Modify: `examples/components.html` (`<style>` lines 13–38; `<main>` tag on the `main.tombo-sections` element)

**Interfaces:**
- Consumes: tokens (Task 1), `.tombo-flow` (Task 2).

- [ ] **Step 1: Add `.tombo-flow` to the content column.** Change `<main class="tombo-sections">` to `<main class="tombo-sections tombo-flow">` (default flow-space = section rhythm; the lead paragraph and each `<section>` are the direct children).

- [ ] **Step 2: Rewrite the `<style>` block.** Replace lines 13–38 with:

```css
  .layout { display: grid; grid-template-columns: 220px 1fr; gap: var(--tombo-space-48); padding-block: var(--tombo-space-48) var(--tombo-space-72); align-items: start; }
  main.tombo-sections { min-width: 0; --tombo-flow-space: var(--tombo-space-48); }   /* section rhythm */
  main.tombo-sections > p.lead { --tombo-flow-space: var(--tombo-space-16); }        /* lead under H1 (first child gets 0 anyway) */
  .side { position: sticky; top: var(--tombo-space-48); }
  .brand { font-family: var(--tombo-font-display); font-weight: 700; font-size: 16px; }
  .brand small { display: block; font-family: var(--tombo-font-mono); font-weight: 400; font-size: var(--tombo-text-label); color: var(--tombo-ink-faint); letter-spacing: .12em; margin-top: var(--tombo-space-4); }
  .side .tombo-toc { margin-top: var(--tombo-space-24); }
  main > p.lead { font-size: var(--tombo-text-body); line-height: var(--tombo-lh-body); color: var(--tombo-ink-sub); max-inline-size: var(--tombo-shell-reading); }
  section { max-width: 720px; }
  @media (min-width: 1600px) { section { max-width: 880px; } }
  section .note { font-size: var(--tombo-text-ui); line-height: var(--tombo-lh-ui); color: var(--tombo-ink-sub); margin-top: var(--tombo-space-8); max-inline-size: var(--tombo-shell-reading); }
  .demo { border: 1px solid var(--tombo-hairline); padding: var(--tombo-space-24); margin-top: var(--tombo-space-16); }
  .demo + .tombo-code { margin-top: var(--tombo-space-12); }
  .row { display: flex; gap: var(--tombo-space-16); align-items: center; flex-wrap: wrap; }
  .cornerbox { height: 90px; }
  .demo .tombo-dim { max-width: 320px; }
  .demo .tombo-ruler { max-width: 320px; }
  .metric-demo { max-width: 280px; }
  .tombo-metric .tombo-ruler { margin-top: var(--tombo-space-12); height: 14px; }
  .griddemo { height: 96px; border: 1px solid var(--tombo-hairline); }
  .scale-demo .tombo-dimlab { margin-bottom: var(--tombo-space-24); }
  .scale-demo .tombo-dimlab:last-child { margin-bottom: 0; }
  @media (max-width: 680px) {
    .layout { grid-template-columns: 1fr; gap: var(--tombo-space-24); }
    .side { position: static; }
  }
  .foot { display: flex; align-items: center; gap: var(--tombo-space-16); }
```

Note: `section { margin-top: 52px }` is removed — section rhythm now comes from the flow default (48px) on `main.tombo-sections`. `.cornerbox`/`.griddemo` heights (90/96) and `max-width` values are sizes, not spacing — left as literals. `height: 14px` on the ruler is a size — left as literal.

- [ ] **Step 3: Verify (chrome-devtools, controller-run) — both themes.** Load `examples/components.html`; screenshot in `tombo` and `hotaru`. Confirm sections are evenly spaced (one 2-cell gap), lead paragraph sits under the title, demos/notes unchanged in feel, catalog renders top-to-bottom without collapse. Grep spacing px as in Task 3 (only `220px`, `320px`, `280px`, `90px`, `96px`, `14px`, `16px` font, breakpoints remain).

- [ ] **Step 4: Commit.**

```bash
git add examples/components.html
git commit -m "refactor: migrate components.html spacing to the space scale and .tombo-flow"
```

---

### Task 5: Migrate app.html

**Files:**
- Modify: `examples/app.html` (`<style>` lines 12–26)

**Interfaces:**
- Consumes: tokens (Task 1). No `.tombo-flow` — app is a dashboard; its spacing is grid/flex `gap` + section `padding`/`margin`, correctly gap-based.

- [ ] **Step 1: Rewrite the `<style>` block.** Replace lines 13–26 with:

```css
  .top { border-bottom: 1px solid var(--tombo-hairline); padding: var(--tombo-space-16) 0; }
  .top .tombo-shell { display: flex; align-items: center; gap: var(--tombo-space-24); }
  .logo { font-family: var(--tombo-font-display); font-weight: 700; font-size: 14px; }
  .top .tombo-tabs { border-bottom: 0; flex: 1; }
  .me { margin-left: auto; font-size: var(--tombo-text-label); color: var(--tombo-ink-faint); }
  .metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--tombo-space-24); margin: var(--tombo-space-32) 0 var(--tombo-space-24); }
  .tombo-metric .v small { font-size: var(--tombo-text-note); color: var(--tombo-ink-faint); font-weight: 400; }
  .tombo-metric .tombo-ruler { margin-top: var(--tombo-space-12); height: 14px; }
  main { padding-bottom: var(--tombo-space-48); }
  @media (max-width: 640px) {
    .metrics { grid-template-columns: 1fr; }
    .top .tombo-shell { flex-wrap: wrap; gap: var(--tombo-space-16); }
  }
  .foot { display: flex; align-items: center; gap: var(--tombo-space-16); }
```

- [ ] **Step 2: Verify (chrome-devtools, controller-run) — both themes.** Load `examples/app.html`; screenshot in `tombo` and `hotaru`. Confirm the 3-up metrics grid, header nav, and table render without collapse; metric ruler gap unchanged. Grep spacing px (only `14px` font/size, breakpoint `640px` remain).

- [ ] **Step 3: Commit.**

```bash
git add examples/app.html
git commit -m "refactor: migrate app.html spacing to the space scale"
```

---

### Task 6: Migrate lp.html

**Files:**
- Modify: `examples/lp.html` (`<style>` lines 12–53; add `.tombo-flow` to the hero-left column div and each `.fcard`)

**Interfaces:**
- Consumes: tokens (Task 1), `.tombo-flow` (Task 2).

**Constraint reminder:** `.hero .cols { gap: 56px }` and the `841–1099px` mid-band block are empirically tuned to the 840px stacking breakpoint (see the existing comment). Do NOT round `56px`→48 or `20px`→24. Tokenize only exact-match values (`32px`→`-32`, `16px`→`-16`).

- [ ] **Step 1: Add `.tombo-flow` to the two vertical stacks.**
  - The hero-left column: the `<div>` at line 64 (inside `.cols`, containing h1/dim/dimlab/tagline/cta) → add class `tombo-flow`: `<div class="tombo-flow">`.
  - Each `.fcard` (lines 98, 104, 110) → add `tombo-flow`: `<div class="fcard tombo-flow tombo-metric tombo-corners">`.

- [ ] **Step 2: Rewrite the `<style>` block.** Replace lines 12–53 with (tuned literals kept; flow overrides replace hero-left and fcard margin-tops):

```css
  :root { --tombo-shell: var(--tombo-shell-wide); }  /* LP volume runs wide */
  .hero { padding: var(--tombo-space-72) 0; }
  /* full-bleed frame: the corners' 1px outdent would poke past the viewport and grow scrollWidth */
  .hero.tombo-corners::after, .hero .tombo-corner-tr { right: 0; }
  .hero .cols { display: grid; grid-template-columns: 1.25fr .75fr; gap: 56px; align-items: center; margin-top: var(--tombo-space-24); }
  /* hero-left column rhythm (.tombo-flow) */
  .hero .cols > .tombo-flow { --tombo-flow-space: var(--tombo-space-16); }
  .hero .cols > .tombo-flow > .tombo-dim { --tombo-flow-space: var(--tombo-space-24); }
  .hero .cols > .tombo-flow > .cta { --tombo-flow-space: var(--tombo-space-24); }
  .hero h1 small { display: block; font-family: var(--tombo-font-body); font-weight: 700;
    font-size: clamp(18px, 2vw, 22px); color: var(--tombo-green); margin-top: var(--tombo-space-16); letter-spacing: -.005em; }
  /* max-, not a fixed width: at 320px a fixed 320 stretches the whole grid track */
  .hero .tombo-dim { max-inline-size: 320px; }
  .tagline { font-size: var(--tombo-text-body); line-height: var(--tombo-lh-body); color: var(--tombo-ink-sub); max-width: 50ch; }
  .cta { display: flex; gap: var(--tombo-space-16); align-items: center; flex-wrap: wrap; }
  .inst .tombo-fig { position: absolute; top: -20px; left: 0; }
  .inst .v small { font-size: var(--tombo-text-ui); color: var(--tombo-ink-faint); font-weight: 400; }
  .inst .rows { margin-top: var(--tombo-space-16); border-top: 1px solid var(--tombo-hairline); }
  .inst .row { display: flex; justify-content: space-between; gap: var(--tombo-space-16); font-family: var(--tombo-font-mono);
    font-size: var(--tombo-text-label); padding: var(--tombo-space-8) 0; border-bottom: 1px solid var(--tombo-hairline); color: var(--tombo-ink-sub); }
  .inst .row b { color: var(--tombo-ink); font-weight: 500; }
  .inst .row .miss { color: var(--tombo-error); }
  .inst .cfoot { margin-top: var(--tombo-space-16); }
  .feat-sec { padding-block: var(--tombo-space-48) var(--tombo-space-8); }
  .feat { margin-top: var(--tombo-space-24); display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--tombo-space-16); }
  .fcard { display: flex; flex-direction: column; --tombo-flow-space: var(--tombo-space-8); }
  .fcard > .meta { margin-top: auto; --tombo-flow-space: 0; padding-top: var(--tombo-space-16); }
  .fcard .meta div { border-top: 1px solid var(--tombo-hairline); padding-top: var(--tombo-space-8); min-height: 55px; }
  @media (max-width: 840px) {
    .hero .cols, .feat { grid-template-columns: 1fr; }
  }
  @media (min-width: 841px) and (max-width: 1099px) {
    /* Martian Mono's wider letterforms need more room for .inst .row than
       the default 1.25fr/.75fr split + 56px gap can give in this band.
       Empirically, .inst .row wraps up to 824px viewport with this ratio/gap;
       840px is the stacking breakpoint (16px buffer above the measured
       threshold), so the whole broken sub-range is absorbed by the
       single-column layout instead. */
    .hero .cols { grid-template-columns: 1.27fr .95fr; gap: 32px; }
    .inst.tombo-metric { padding: 20px 16px; }
  }
  .foot { display: flex; align-items: center; gap: var(--tombo-space-16); }
  .hero .tombo-logo { display: block; margin-bottom: var(--tombo-space-16); }
```

Notes on the flow migration: the hero-left column's children (h1 → dim → dimlab → tagline → cta) were `margin-top` 22/18/26; under `.tombo-flow` the default is `-16` (tagline/dimlab), with `.tombo-dim` and `.cta` bumped to `-24`. The old `.hero .tombo-dim margin-top:22`, `.tagline margin-top:18`, `.cta margin-top:26` declarations are removed (flow supplies them). `.fcard` internal rhythm (fig→h3→p was 8/10) becomes flow default `-8`; `.meta` keeps `margin-top:auto` (push to bottom) with `--tombo-flow-space:0` so the owl adds nothing on top of `auto`. Kept literals: `.cols gap:56px`, mid-band `gap:32px`/`padding:20px 16px`, `top:-20px`, `max-inline-size:320px`, `min-height:55px`, `1.25fr/.75fr`.

- [ ] **Step 3: Verify (chrome-devtools, controller-run) — both themes AND breakpoints.** Load `examples/lp.html`; screenshot in `tombo` and `hotaru` at desktop width. Then resize to **900px** (mid-band) and confirm `.inst .row` does not wrap (the tuned 56px/32px gaps are intact) and to **800px** to confirm single-column stacking. Confirm hero-left rhythm (headline → dim → tagline → CTA) reads evenly and the feature cards' fig/title/body/meta spacing looks intentional with meta pinned to the bottom.

- [ ] **Step 4: Commit.**

```bash
git add examples/lp.html
git commit -m "refactor: migrate lp.html spacing to the space scale and .tombo-flow"
```

---

### Task 7: Update spec §7 and add the README "Space scale" section

**Files:**
- Modify: `docs/superpowers/specs/2026-07-20-tombo-design-system-design.md:158` (the "基本単位 4px…" bullet in §7)
- Modify: `README.md` (add a "Space scale" section after the "Overriding the page width" / container documentation)

- [ ] **Step 1: Update spec §7.** Replace the bullet at line 158 (`- 基本単位 4px。方眼セルは 24px 固定、セクション律動は docs 64px / LP 96px`) with:

```
- 基本単位 4px。space token `--tombo-space-{4,8,12,16,24,32,48,72,96}`（24 以上は 24px 方眼セルの倍数）。方眼セルは 24px 固定、セクション律動は docs 72px（3 セル）/ LP 96px（4 セル）。縦リズムは `.tombo-flow`（owl セレクタ + `--tombo-flow-space`、既定 1 セル）で管理する
```

- [ ] **Step 2: Add the README section.** Insert after the container "Overriding the page width" subsection (before "Signature classes"):

```markdown
### Space scale

Spacing is tokenised on a 4px base. Steps 24 and up are multiples of the 24px grid cell, so block and section rhythm sit on the same grid the margin marks draw.

| token | px | typical use |
|---|---|---|
| `--tombo-space-4` | 4 | hairline gap, eyebrow → title |
| `--tombo-space-8` | 8 | chip / row padding, tight caption |
| `--tombo-space-12` | 12 | button padding-y, tight rhythm |
| `--tombo-space-16` | 16 | callout / code inset, body rhythm, card gap |
| `--tombo-space-24` | 24 | one grid cell — default block rhythm |
| `--tombo-space-32` | 32 | medium gap between components |
| `--tombo-space-48` | 48 | 2 cells — sidebar gap, small section |
| `--tombo-space-72` | 72 | 3 cells — docs section rhythm |
| `--tombo-space-96` | 96 | 4 cells — LP section rhythm |

Use tokens for `gap` and `padding` in your own layout CSS: `gap: var(--tombo-space-48)`.

#### Vertical rhythm — `.tombo-flow`

Add `.tombo-flow` to a container to space its direct children apart with a single grid cell. Override `--tombo-flow-space` on the container to change the default, or on any child to change the space that precedes it:

```css
.article { } /* markup: <div class="article tombo-flow"> */
.article { --tombo-flow-space: var(--tombo-space-16); }   /* body rhythm */
.article > h2 { --tombo-flow-space: var(--tombo-space-48); } /* more air before headings */
```

`.tombo-flow` uses `margin-block-start` on `* + *`, so the first child has no leading margin. Use it for stacked prose/content; keep `gap` for grid and flex layouts.
```

- [ ] **Step 3: Verify + commit.** `grep -n 'tombo-space' README.md` shows the table; `grep -n 'space token' docs/superpowers/specs/2026-07-20-tombo-design-system-design.md` shows the updated §7.

```bash
git add README.md docs/superpowers/specs/2026-07-20-tombo-design-system-design.md
git commit -m "docs: document the space scale and .tombo-flow (README + spec §7)"
```

---

### Task 8: Bump banners and vendoring pins to v0.8.0

**Files:**
- Modify: `tombo.css:1`, `tombo.js:1` (banners), `README.md` (three `v0.7.0:` vendoring-pin lines)

- [ ] **Step 1: Bump the banners.**
  - `tombo.css:1` → `/*! TOMBO v0.8.0 — wadakatu design system. MIT. https://github.com/wadakatu/tombo */`
  - `tombo.js:1` → `/*! TOMBO tombo.js v0.8.0 — wadakatu design system. Optional, zero-dependency. MIT. https://github.com/wadakatu/tombo */`

- [ ] **Step 2: Bump the vendoring pins.** In `README.md`, replace every `v0.7.0:` with `v0.8.0:` (the three `git … show` vendoring lines).

- [ ] **Step 3: Verify + commit.**

```bash
head -1 tombo.css; head -1 tombo.js; grep -n 'show v0\.' README.md   # all v0.8.0
node --check tombo.js
python3 scripts/check_contrast.py   # expect all PASS
git add tombo.css tombo.js README.md
git commit -m "chore: bump the banner and vendoring pins to v0.8.0"
```

---

## Verification (end-to-end, after all tasks)

1. **Grep:** `grep -rn 'tombo-space' tombo.css examples/*.html | wc -l` > 0; no raw spacing px literals remain in the examples' `<style>` blocks except documented exceptions (docs `200px`, `680px`; components `220px`, sizes, breakpoints; app `14px`, `640px`; lp `56px`, mid-band `32px`/`20px 16px`, `-20px`, `320px`, `55px`, fr ratios).
2. **Computed-style:** the 9 tokens resolve (Task 1 check); `.tombo-flow` first-child 0 / default 24 / override works (Task 2 check).
3. **Screenshots:** all four examples in `tombo` AND `hotaru`; lp additionally at 900px and 800px. Drift is expected and intentional — confirm each looks deliberate (even rhythm, blocks on the grid), no collapsed or doubled spacing, no horizontal scroll.
4. `python3 scripts/check_contrast.py` → all PASS (no color touched).
5. `node --check tombo.js` clean.

## Release (USER-GATED — do NOT run without explicit go)

v0.8.0 (additive minor). Local ff-merge of `feature/space-scale` into `main`, lightweight tag `v0.8.0` on the tip, push branch-fast-forward + tag (same procedure as v0.7.0 — avoids the v0.6.0 merge-commit incident). Then update `tombo-roadmap` memory: 第2段 done → v0.8.0; remaining open items = component-padding normalization (B), forms, print, text-autospace, CI.

## Out of scope (follow-up)

- **B — tombo.css component-internal padding normalization** onto the scale (breaking; next release).
- forms, `@media print`, `text-autospace`/`palt`, CI (separate roadmap items).
