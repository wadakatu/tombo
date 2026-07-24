# TOMBO text-autospace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the examples' hand-typed 和欧 spaces with CSS-native `text-autospace`, opted in from `tombo.css`.

**Architecture:** Two declarations in `@layer tombo.base` — `body { text-autospace: normal }` opts into 八分アキ (1/8 em) at every Japanese↔Latin/number boundary, and `code, kbd, samp, pre { text-autospace: no-autospace }` keeps verbatim text unspaced (the property inherits). The examples then drop the hand-typed boundary spaces so the browser does the spacing. Non-supporting engines ignore the property and render tight (graceful degrade — no `@supports` needed).

**Tech Stack:** Single-file CSS (`tombo.css`), plain HTML examples, `python3 scripts/check_contrast.py`, `node --check`, chrome-devtools for computed-style + width measurement.

## Global Constraints

- **Version:** `v0.12.0` — additive/non-breaking. Banners `tombo.css:1` + `tombo.js:1` and the three README vendoring pins (`README.md:39,40,65`) go `v0.11.0 → v0.12.0`.
- **No new color / token / class / `@layer` change** → contrast gate is structurally unaffected (37 PASS). Behaviour-only addition.
- **`text-spacing-trim` / `palt` / `text-spacing` shorthand: do NOT add** — the standard `text-spacing-trim` default is already `normal`; the shorthand is unshipped; `palt` is the non-standard heavy path.
- **No `@supports` gate** — unknown property degrades to tight 和欧, which is the PE baseline.
- **Empirically established (Chrome, 2026-07-24):** autospace inserts exactly 1/8 em; a manual space suppresses it; the UA default is `no-autospace` (must opt in); autospace **crosses normal inline boundaries** (`<a>`/`<b>`) but **NOT** a `<code>`/`<kbd>`/`<samp>` (`no-autospace`) boundary.
- Commit trailer on every commit: `Claude-Session: https://claude.ai/code/session_01CYKP1wE7CusnhuQm9CxTue`. No `Co-Authored-By`. English Conventional Commits. Branch `feature/text-autospace`.
- Spec: `docs/superpowers/specs/2026-07-24-tombo-text-autospace-design.md`.

---

### Task 1: opt into 和欧 auto-spacing in tombo.css

**Files:**
- Modify: `tombo.css:103-110` (the `body {…}` block in `@layer tombo.base`)
- Modify: `tombo.css:122` (the `code, kbd, samp, pre {…}` rule in `@layer tombo.base`)

**Interfaces:**
- Produces: `body` computes `text-autospace: normal`; `code, kbd, samp, pre` compute `text-autospace: no-autospace`. Task 2 relies on this being live so the stripped boundaries render with 八分アキ.

- [ ] **Step 1: Add `text-autospace: normal` to `body`.** The current block is:

```css
  body {
    background: var(--tombo-paper);
    color: var(--tombo-ink);
    font-size: var(--tombo-text-body);
    font-weight: var(--tombo-w-body);
    line-height: 2; /* = 30px at body size; unitless so larger text inherits safely */
    transition: background var(--tombo-dur) var(--tombo-ease), color var(--tombo-dur) var(--tombo-ease);
  }
```

Insert one line after the `line-height` line:

```css
    line-height: 2; /* = 30px at body size; unitless so larger text inherits safely */
    text-autospace: normal; /* 八分アキ(1/8 em) at 和欧 boundaries — CSS Text L4. Unsupported → tight (PE) */
    transition: background var(--tombo-dur) var(--tombo-ease), color var(--tombo-dur) var(--tombo-ease);
```

- [ ] **Step 2: Exempt verbatim text.** The current rule (tombo.css:122) is:

```css
  code, kbd, samp, pre { font-family: var(--tombo-font-mono); font-weight: 400; }
```

Replace with:

```css
  code, kbd, samp, pre { font-family: var(--tombo-font-mono); font-weight: 400; text-autospace: no-autospace; } /* verbatim: no re-spacing (text-autospace inherits) */
```

- [ ] **Step 3: Verify computed values + mechanism (chrome-devtools).** Open `examples/components.html`, then evaluate:

```js
() => {
  const bodyAS = getComputedStyle(document.body).textAutospace;
  const code = document.querySelector('code, pre');
  const codeAS = code ? getComputedStyle(code).textAutospace : 'n/a';
  // synthetic probe: tight 和欧 boundary in a normal context vs inside code
  const mk = (tag) => { const e=document.createElement(tag); e.style.cssText='position:absolute;white-space:nowrap;font-size:20px';
    e.textContent='Composerで'; document.body.appendChild(e);
    const r=document.createRange(); r.selectNodeContents(e); const w=r.getBoundingClientRect().width; e.remove(); return w; };
  return { bodyAS, codeAS, span_w: mk('span').toFixed(2), code_w: mk('code').toFixed(2) };
}
```

Expected: `bodyAS === "normal"`, `codeAS === "no-autospace"`, and `span_w` ≈ 2.5px wider than `code_w` (autospace fires in the span, not in code).

- [ ] **Step 4: Contrast + syntax hygiene.**

```bash
python3 scripts/check_contrast.py && node --check tombo.js
```

Expected: all contrast PASS; `node --check` silent (tombo.js untouched here).

- [ ] **Step 5: Commit.**

```bash
git add tombo.css
git commit -m "feat: space 和欧 automatically with text-autospace

Claude-Session: https://claude.ai/code/session_01CYKP1wE7CusnhuQm9CxTue"
```

---

### Task 2: strip hand-typed 和欧 spaces from examples + README snippets

**Files:**
- Modify: `examples/docs.html` (lines 50, 58)
- Modify: `examples/app.html` (line 98)
- Modify: `examples/components.html` (many `.note`/snippet lines — enumerated below)
- Modify: `README.md` (lines 381, 382 — snippet prose)
- `examples/lp.html` has **no** 和欧 boundary spaces (verified) — nothing to strip; screenshot-verify only.

**Interfaces:**
- Consumes: Task 1's `body { text-autospace: normal }` (so the stripped boundaries render with 八分アキ in Chrome).

**The rule (apply to every boundary below):** delete the single ASCII space at the Japanese↔Latin/number boundary. **KEEP** a space when the char on either side belongs to an inline `<code>`/`<kbd>`/`<samp>` element (autospace can't cross that boundary — verified), when it is Latin-internal (`M PLUS 2`), around `—`/`/`, or is code/command syntax. The enumerated list below is alnum-adjacent prose (already excludes tag-adjacent boundaries); still confirm each in context before deleting.

**Enumerated boundaries to strip** (from `grep -noP '[ぁ-ヿ一-鿿々ー] [A-Za-z0-9]|[A-Za-z0-9] [ぁ-ヿ一-鿿々ー]'`):

- `docs.html:50` — `Composer で導入`→`Composerで導入`, `Laravel 11 以降`→`Laravel11以降`, `自動で OpenAPI ドキュメント`→`自動でOpenAPIドキュメント`
- `docs.html:58` — `Lumen で使う`→`Lumenで使う`
- `app.html:98` — `8 文字以上`→`8文字以上`
- `components.html:71` — `docs の全…`/`各項は…が docs 音量`/`docs 音量の実演`/`寸法線、hr 代替` → strip each (`docs`↔kana, `hr`↔kana etc.)
- `components.html:75` — `S-01。`… `四隅に置く 12px の`→`12pxの`, `::before / ::after が…`, `&lt;b&gt; を 2 つ` → strip the num/latin↔kana spaces
- `components.html:92` — `docs 音量`→`docs音量`
- `components.html:106` — `black の目盛線に置き換える…green の…` → `green`↔kana
- `components.html:109-111,117` — `を OpenAPI 定義で` → `をOpenAPI定義で` (live list AND the `<pre>` markup snippet — keep them identical, tight in the `<pre>` is correct source)
- `components.html:124` — `10% 刻み`/`green の充填`/`インライン custom property`/`content-type で` → strip
- `components.html:136,151,181,199,218,220,232,261,302,320,338,341,347,356,365,373,381,386,398,433,434,450,451` — same rule: strip alnum↔kana prose spaces; **keep** any that sit against an inline `<code>`/`<kbd>` tag (e.g. `<code>@media print</code> で`, `<kbd>⌘P</kbd> して`)
- `README.md:381,382` — the forms snippet prose: `0–100 の整数`→`0–100の整数`, `0 から 100 の数値`→`0から100の数値`

- [ ] **Step 1: Strip docs.html + app.html (body prose — highest value).** Edit `docs.html:50,58` and `app.html:98` per the list.

- [ ] **Step 2: Verify docs.html + app.html in Chrome (both themes).** Open each; for a stripped boundary measure it renders with autospace, e.g. on docs.html:

```js
() => { const p=[...document.querySelectorAll('p')].find(e=>e.textContent.includes('Composerで導入'));
  const r=document.createRange(); r.selectNodeContents(p); return {found:!!p}; }
```

Take a screenshot in `tombo` and `hotaru` (toggle via the footer control or `document.documentElement.dataset.theme`). Confirm boundaries read as a hair-space, nothing lost mid-word.

- [ ] **Step 3: Strip components.html** per the enumerated lines. Work top-down; for each line delete the boundary space, keeping `<code>`/`<kbd>`-adjacent ones.

- [ ] **Step 4: Strip README.md:381,382** snippet prose.

- [ ] **Step 5: Verify components.html + README both themes.** Screenshot components.html in `tombo` and `hotaru`. Spot-check: `.note` prose boundaries show 八分アキ; inline `<code>`↔kana spacing preserved; code blocks (`<pre>`) unchanged (no-autospace); no over-strip (no Latin words fused, `M PLUS 2` intact).

- [ ] **Step 6: Confirm nothing over-stripped (grep guard).** Re-run the enumeration grep; the remaining hits must be only the intentionally-kept `<code>`/`<kbd>`-adjacent ones:

```bash
for f in examples/docs.html examples/app.html examples/components.html examples/lp.html README.md; do echo "== $f =="; grep -noP '[ぁ-ヿ一-鿿々ー] [A-Za-z0-9]|[A-Za-z0-9] [ぁ-ヿ一-鿿々ー]' "$f"; done
```

Expected: only code/kbd-adjacent survivors (or none). No plain-prose boundary remains.

- [ ] **Step 7: Commit.**

```bash
git add examples/docs.html examples/app.html examples/components.html README.md
git commit -m "refactor: drop hand-typed 和欧 spaces; text-autospace handles them

Claude-Session: https://claude.ai/code/session_01CYKP1wE7CusnhuQm9CxTue"
```

---

### Task 3: document 和欧 autospace + bump to v0.12.0

**Files:**
- Modify: `README.md` (new `## Japanese typography` section; pins at 39, 40, 65)
- Modify: `examples/components.html` (one `.note` in the typography section, near line 320)
- Modify: `tombo.css:1`, `tombo.js:1` (banners)

**Interfaces:**
- Consumes: Tasks 1–2 (documents the shipped behaviour).

- [ ] **Step 1: Add the README section.** Insert between the `## Print` section and `## Contrast gate` (find the boundary with `grep -n '^## ' README.md`):

```markdown
## Japanese typography

Mixed Japanese/Latin (和欧混植) spacing is CSS-native. `tombo.css` opts into
[`text-autospace: normal`](https://www.w3.org/TR/css-text-4/#text-autospace-property)
on `body`, so the browser inserts the proper 八分アキ (1/8 em) at every
Japanese↔Latin/number boundary — you don't hand-type spaces between them.
Verbatim text (`code`, `kbd`, `samp`, `pre`) is exempt.

```html
<!-- write it tight; the browser spaces it -->
<p>Laravel11以降に対応し、OpenAPIドキュメントを生成する。</p>
```

Progressive enhancement: supporting engines (Chromium today) render the 八分アキ;
others render tight — fully legible — and pick up the spacing automatically as
they ship `text-autospace`, with no change to your markup. A hand-typed space,
if you leave one in, is respected and suppresses autospace at that boundary.
```

- [ ] **Step 2: Add the components.html note.** In the typography section (the one whose note starts `.tombo-display は Instrument Sans…`, components.html:320), append a sibling `.note`:

```html
        <p class="note">和欧混植の間隔は CSS に任せる。<code>tombo.css</code> が <code>text-autospace: normal</code> を <code>body</code> に効かせるので、和文と欧文の境目にブラウザが八分アキ(1/8 em)を入れる — 手打ちの半角スペースは要らない。<code>code</code>/<code>pre</code> は逐語なので除外。未対応ブラウザはベタ組みに degrade し、実装が揃えば自動で八分アキになる。</p>
```

- [ ] **Step 3: Bump banners + pins.**

```bash
# tombo.css:1 and tombo.js:1 banners (line 1 only), README pins at 39,40,65
sed -i '' '1s/v0\.11\.0/v0.12.0/' tombo.css
sed -i '' '1s/v0\.11\.0/v0.12.0/' tombo.js
sed -i '' '39s/v0\.11\.0/v0.12.0/;40s/v0\.11\.0/v0.12.0/;65s/v0\.11\.0/v0.12.0/' README.md
```

Verify: `grep -n 'v0.12.0' tombo.css tombo.js; grep -n 'v0.11.0\|v0.12.0' README.md` — banners show v0.12.0, the three pins show v0.12.0, no stray v0.11.0 in pins (migration-history mentions of older versions stay).

- [ ] **Step 4: Verify the note renders (chrome-devtools, both themes).** Reload components.html; screenshot the typography section in `tombo` and `hotaru`; confirm the new `.note` reads correctly and its own 和欧 boundaries are spaced.

- [ ] **Step 5: Final hygiene.**

```bash
python3 scripts/check_contrast.py && node --check tombo.js
```

Expected: all PASS; `node --check` silent.

- [ ] **Step 6: Commit.**

```bash
git add README.md examples/components.html tombo.css tombo.js
git commit -m "docs: document 和欧 autospace and bump to v0.12.0

Claude-Session: https://claude.ai/code/session_01CYKP1wE7CusnhuQm9CxTue"
```

---

## Verification (whole branch)

- `body` computes `text-autospace: normal`; `code, kbd, samp, pre` compute `no-autospace`.
- Stripped 和欧 boundaries render with 八分アキ in Chromium (measured), tight elsewhere (degrade).
- No over-strip: enumeration grep leaves only `<code>`/`<kbd>`-adjacent survivors; `M PLUS 2`, dashes, code syntax intact.
- Both themes screenshot-clean on docs/app/components/lp.
- `check_contrast.py` all PASS; `node --check tombo.js` clean.
- Banners + 3 pins at v0.12.0.

## Execution & release

- **Execution:** one small CSS change + prose stripping I authored, all verifiable in-browser — execute **inline** (executing-plans), then one **Opus whole-diff review** as the safety net (per [[tombo-subagent-model-policy]]). The review must specifically check the strip list for over-stripping and confirm code-adjacent spaces were kept.
- **Release (USER-GATED):** local ff-merge of `feature/text-autospace` into `main`, lightweight tag `v0.12.0`, push (linear history, no force-push — same as v0.7.0–v0.11.0). Then update `tombo-roadmap` memory: text-autospace done → v0.12.0; remaining = CI.

## Out of scope (follow-up)
`text-spacing-trim`/`palt` explicit declaration, `text-spacing` shorthand, link-URL print expansion, CI — separate items.
