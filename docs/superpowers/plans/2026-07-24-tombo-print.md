# TOMBO print vocabulary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. **NOTE:** Task 2 (paper トンボ) is an *empirically pinned* task — its exact geometry is tuned in a browser print preview, which only the controller drives. See "Execution" — inline execution is recommended for this feature.

**Goal:** Add a `@media print` vocabulary to tombo.css: unconditional print-hardening for every TOMBO page, plus an opt-in `.tombo-trim` that prints real printer's トンボ (single 角トンボ + センタートンボ) on the page.

**Architecture:** One new *unlayered* print section at EOF of `tombo.css` — a bare `@page { margin: 16mm }` plus a `@media print { … }` block. Unlayered so its overrides beat every `@layer` rule without `!important`. Part A (hardening) is deterministic CSS. Part B (trim marks) reuses the existing wide-screen registration-mark technique (ink drawn as `linear`/`radial-gradient` background layers) on `html:has(> body.tombo-trim)::before` (corners) / `::after` (centers), `position: fixed` so they repeat on every printed page, `print-color-adjust: exact` scoped to the overlay so the background-drawn marks actually print.

**Tech Stack:** Single-file CSS (`tombo.css`), `@layer` cascade, `light-dark()`/`color-scheme` tokens, CSS Paged Media (`@page`), CSS Fragmentation (`break-*`). No JS. No build. Verification = `node --check`, `scripts/check_contrast.py`, chrome-devtools print preview.

## Global Constraints

- **Version = v0.11.0**, additive / non-breaking. Bump both banners (`tombo.css:1`, `tombo.js:1`) and the three README vendoring pins (`v0.10.0:` → `v0.11.0:`).
- **No new color.** Every mark and override reuses an existing token (`--tombo-ink`, `--tombo-ink-sub`, `--tombo-hairline`). The contrast gate (`scripts/check_contrast.py`) parses token *values* from `tombo.css`; adding no token keeps it structurally unaffected — it must still print all PASS.
- **No shu in print.** Marks are `--tombo-ink` (registration black = all-plate black, not a current-position line). Existing shu hairlines (`.tombo-current`/`.tombo-kicker`/`.tombo-ruler`) are left untouched.
- **Paper トンボ is opt-in** via `.tombo-trim` on `<body>`. Hardening (Part A) is unconditional.
- **Reset / tokens / base / component layers are unchanged.** The print section is appended unlayered after the final `@layer` block. `@page` is a bare at-rule (it cannot live inside `@layer`).
- **Commit trailer:** every commit message ends with `Claude-Session: https://claude.ai/code/session_01CYKP1wE7CusnhuQm9CxTue`. **Never** add `Co-Authored-By`. English Conventional Commits.
- **Branch:** `feature/print` (already created; spec committed at `f10fe85`).
- **UI verification is mandatory in both themes** (`tombo` day / `hotaru` night) via chrome-devtools before any task is marked done.

---

## File Structure

- `tombo.css` — **all CSS changes.** Append one unlayered print section at EOF (after line 491, the close of the last `@layer tombo.components` block). Banner bump at line 1.
- `tombo.js` — banner bump only (line 1). No logic change.
- `examples/docs.html` — add `tombo-trim` to the `<body>` class (line 34) so ⌘P shows the marks.
- `examples/components.html` — add TOC link (after line 64) + a `#c18` print section (before `</main>`, line 447).
- `README.md` — add `## Print` section (between the Forms section end, line 405, and `## Contrast gate`, line 406) + bump three vendoring pins (lines 39, 40, 65).

---

## Task 1: Print hardening (Part A)

**Files:**
- Modify: `tombo.css` — append the print section skeleton + Part A rules at EOF (after line 491).

**Interfaces:**
- Produces: the unlayered `@page { margin: 16mm }` and `@media print { … }` block that Task 2 extends with the `.tombo-trim` overlay rules (Task 2 adds rules *inside* the same `@media print` block).

- [ ] **Step 1: Append the print section (skeleton + Part A) at EOF of `tombo.css`**

Append exactly this after the final line (the closing `}` of the last `@layer tombo.components` block):

```css

/* ── print ─────────────────────────────────────────────────────────────
   Unlayered on purpose: these overrides must beat every @layer rule, and
   being outside all layers wins the cascade without !important. Two halves:
   (A) hardening — every TOMBO page prints cleanly; (B) opt-in .tombo-trim —
   real printer's トンボ on the sheet (the system finally does what it is named
   after). @page is a bare at-rule; it cannot live inside @layer. */
@page { margin: 16mm; }

@media print {
  /* (A) hardening — unconditional */

  /* night pages print on white paper: flipping color-scheme re-resolves every
     light-dark() token to its light value (surfaces near-white, ink near-black),
     so a hotaru page never prints as a black rectangle. */
  :root,
  :root[data-theme="tombo"],
  :root[data-theme="hotaru"] { color-scheme: light; }

  /* screen-only chrome never prints */
  .tombo-themes, .tombo-copy { display: none; }

  /* glow + motion off (mirrors the forced-colors guard) */
  .tombo-glow { background-image: none; box-shadow: none; }
  .tombo-glow .tombo-display,
  .tombo-glow.tombo-metric > .v { text-shadow: none; }
  *, *::before, *::after { transition: none; animation: none; }

  /* the code panel is dark in both themes (a background — not printed by
     default, which would drop its light text onto white and vanish). Repaint
     to ink-on-white with a hairline so code stays readable on paper. */
  .tombo-code, .tombo-code pre {
    background: #fff; color: var(--tombo-ink);
    border: 1px solid var(--tombo-hairline);
  }
  .tombo-code > figcaption { color: var(--tombo-ink-sub); }

  /* fragmentation: keep instrument blocks whole; don't strand headings */
  .tombo-metric, .tombo-callout, .tombo-code, figure, tr, .tombo-check { break-inside: avoid; }
  h1, h2, h3, h4 { break-after: avoid; }
  p, li { orphans: 2; widows: 2; }
}
```

- [ ] **Step 2: Syntax + balance check**

Run:
```bash
node -e "require('fs').readFileSync('tombo.css','utf8')" && \
  awk '{o+=gsub(/{/,"{"); c+=gsub(/}/,"}")} END{print "braces:",o,c}' tombo.css
```
Expected: no error; `braces:` two equal numbers.

- [ ] **Step 3: Verify hardening in chrome-devtools print preview (controller, both themes)**

Load `examples/docs.html`, emulate print media (chrome-devtools `emulate` CSS media `print`, or open the print preview). Confirm:
- **hotaru**: force `data-theme="hotaru"`, print-emulate → page renders on **white** (not the dark paper), ink is dark. (Verify computed `color-scheme` on `:root` = `light` under print emulation, or visually via screenshot.)
- Load `examples/components.html` (has a `.tombo-code` block): under print emulation the code figure is **white background, dark (`--tombo-ink`) text, hairline border**, and the COPY button (`.tombo-copy`, injected by tombo.js) is **absent**.
- The theme toggle (`.tombo-themes`) is **absent** under print.
- No console errors.

Capture a print-emulation screenshot of `docs.html` (both themes) for the record.

- [ ] **Step 4: Contrast gate + commit**

Run: `python3 scripts/check_contrast.py`
Expected: all PASS (no token added).

```bash
git add tombo.css
git commit -m "$(cat <<'EOF'
feat: harden every TOMBO page for print (@media print, @page margin)

Force light theme on paper, repaint the dark code panel to ink-on-white,
hide screen-only chrome (theme toggle, copy buttons), kill glow/motion,
add fragmentation control, and set a 16mm @page margin.

Claude-Session: https://claude.ai/code/session_01CYKP1wE7CusnhuQm9CxTue
EOF
)"
```

---

## Task 2: Paper トンボ — opt-in `.tombo-trim` (Part B, empirically pinned)

**Files:**
- Modify: `tombo.css` — add the `.tombo-trim` overlay rules **inside** the `@media print` block created in Task 1 (append them just before the block's closing `}`).

**Interfaces:**
- Consumes: the `@media print { … }` block from Task 1.
- Produces: `html:has(> body.tombo-trim)::before` (角トンボ) + `::after` (センタートンボ). Task 3 opts `docs.html` in by adding `tombo-trim` to its `<body>`.

**Why this task is controller-run:** browser print engines position `fixed` boxes and paint background layers in paged media in engine-specific ways. The exact `inset`, arm length, gap, and ring geometry must be tuned against a real print preview. The CSS below is the complete, working *starting point* (the robust "hug the printable-area corner" form, guaranteed to render); the steps then pin the geometry and, if stable, push the marks into the 16mm margin band (the approved look). The fallback is the starting form itself.

- [ ] **Step 1: Add the `.tombo-trim` overlay CSS inside the `@media print` block**

Insert these rules immediately before the closing `}` of the `@media print` block:

```css

  /* (B) paper トンボ — opt-in via <body class="tombo-trim">.
     Marks are ink (registration black), drawn as background layers, so the
     overlay needs print-color-adjust:exact or nothing prints. position:fixed
     repeats the marks on every page. ::before = 角トンボ (corner crop marks),
     ::after = センタートンボ (edge-center registration rings). Geometry lives in
     custom properties so it can be tuned against the print preview. */
  html:has(> body.tombo-trim)::before,
  html:has(> body.tombo-trim)::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
    background-repeat: no-repeat;
  }

  /* 角トンボ: a single L hugging each corner of the printable area, arms along
     the trim edges with a small gap at the vertex (crop-mark convention). */
  html:has(> body.tombo-trim)::before {
    --tl: 24px;  /* arm length */
    --tk: 1px;   /* stroke     */
    --gp: 7px;   /* gap from the exact corner */
    background-image:
      linear-gradient(var(--tombo-ink), var(--tombo-ink)),
      linear-gradient(var(--tombo-ink), var(--tombo-ink)),
      linear-gradient(var(--tombo-ink), var(--tombo-ink)),
      linear-gradient(var(--tombo-ink), var(--tombo-ink)),
      linear-gradient(var(--tombo-ink), var(--tombo-ink)),
      linear-gradient(var(--tombo-ink), var(--tombo-ink)),
      linear-gradient(var(--tombo-ink), var(--tombo-ink)),
      linear-gradient(var(--tombo-ink), var(--tombo-ink));
    background-size:
      var(--tl) var(--tk), var(--tk) var(--tl),   /* TL: horizontal, vertical */
      var(--tl) var(--tk), var(--tk) var(--tl),   /* TR */
      var(--tl) var(--tk), var(--tk) var(--tl),   /* BL */
      var(--tl) var(--tk), var(--tk) var(--tl);   /* BR */
    background-position:
      left var(--gp) top 0,     left 0 top var(--gp),
      right var(--gp) top 0,    right 0 top var(--gp),
      left var(--gp) bottom 0,  left 0 bottom var(--gp),
      right var(--gp) bottom 0, right 0 bottom var(--gp);
  }

  /* センタートンボ: a 1px ink ring + crosshair at each edge midpoint. Offset in
     from the edge by the ring radius so it isn't clipped by the overlay box. */
  html:has(> body.tombo-trim)::after {
    --rs: 13px;  /* ring size (outer) */
    --cl: 26px;  /* crosshair length  */
    --tk: 1px;
    --rr: calc(var(--rs) / 2);            /* ring radius */
    --ring: radial-gradient(circle,
      transparent calc(var(--rr) - 1px),
      var(--tombo-ink) calc(var(--rr) - 1px) var(--rr),
      transparent var(--rr));
    --hbar: linear-gradient(var(--tombo-ink), var(--tombo-ink));
    --vbar: linear-gradient(var(--tombo-ink), var(--tombo-ink));
    background-image:
      var(--ring), var(--ring), var(--ring), var(--ring),   /* top, bottom, left, right rings */
      var(--hbar), var(--hbar), var(--hbar), var(--hbar),   /* horizontal cross bars */
      var(--vbar), var(--vbar), var(--vbar), var(--vbar);   /* vertical cross bars */
    background-size:
      var(--rs) var(--rs), var(--rs) var(--rs), var(--rs) var(--rs), var(--rs) var(--rs),
      var(--cl) var(--tk), var(--cl) var(--tk), var(--cl) var(--tk), var(--cl) var(--tk),
      var(--tk) var(--cl), var(--tk) var(--cl), var(--tk) var(--cl), var(--tk) var(--cl);
    background-position:
      top var(--rr) left 50%,  bottom var(--rr) left 50%,  left var(--rr) top 50%,  right var(--rr) top 50%,
      top var(--rr) left 50%,  bottom var(--rr) left 50%,  left var(--rr) top 50%,  right var(--rr) top 50%,
      top var(--rr) left 50%,  bottom var(--rr) left 50%,  left var(--rr) top 50%,  right var(--rr) top 50%;
  }
```

- [ ] **Step 2: Syntax + balance check**

Run:
```bash
node -e "require('fs').readFileSync('tombo.css','utf8')" && \
  awk '{o+=gsub(/{/,"{"); c+=gsub(/}/,"}")} END{print "braces:",o,c}' tombo.css && \
  grep -c 'print-color-adjust: exact' tombo.css
```
Expected: no error; balanced braces; `print-color-adjust: exact` appears exactly **1** time (only in the overlay rule — it must NOT leak onto body content).

- [ ] **Step 3: Pin geometry in chrome-devtools print preview (controller)**

Temporarily add `tombo-trim` to `examples/docs.html`'s `<body>` (Task 3 makes it permanent) OR test on a scratch page. Under print emulation, verify and tune the custom properties (`--tl`, `--gp`, `--rs`, `--cl`) live:
1. **Marks render in ink** at all four corners (角トンボ) and all four edge midpoints (センタートンボ). If nothing shows, the `print-color-adjust: exact` isn't taking — do not proceed until marks paint.
2. **Every page repeats** the marks: make the doc span ≥2 printed pages (print preview page count > 1) and confirm the corner + center marks appear on **each** page.
3. **No collision with body content** (marks sit at/near the printable-area edge; the 16mm `@page` margin keeps text clear).
4. **Rings are round and crosshairs centered** on each ring; adjust `--rr`/positions until the ⊕ reads cleanly.

- [ ] **Step 4: Attempt the margin-band placement (approved look); else keep the fallback**

The starting CSS hugs the printable-area corners. Attempt the approved outward look (marks sitting in the 16mm margin band, arms extending off the trim edges — matching the design mock) by extending the overlay to the paper edge, e.g. change the overlay `inset: 0` to a paper-spanning box (`inset: -16mm`, matching the `@page` margin) and re-pinning the mark positions so each L vertex lands on the trim corner with arms running into the margin. Re-verify Steps 3.1–3.3 in the print preview.
- **Decision gate:** if margin-band placement is stable in the print preview (marks on paper, every page, no clipping), keep it. If it is not reproducible (fixed box positions off-page, marks clipped, or inconsistent), **revert to the Step-1 corner-hugging form** — it is the documented, honest fallback (marks still point at the true printable-area corners/edges). Either way, capture a print-preview screenshot to show the user.

- [ ] **Step 5: Confirm non-opt-in pages show nothing**

Under print emulation, load `examples/app.html` (no `tombo-trim`). Confirm **no corner/center marks** print (the `html:has(> body.tombo-trim)` guard keeps them off). Confirm Task 1 hardening still holds there.

- [ ] **Step 6: Contrast gate + commit**

Run: `python3 scripts/check_contrast.py`
Expected: all PASS.

```bash
git add tombo.css
git commit -m "$(cat <<'EOF'
feat: add .tombo-trim — opt-in printer's トンボ on the printed page

Single 角トンボ at the four corners + センタートンボ at the four edge centers,
drawn in ink as gradient layers on a position:fixed overlay so they repeat on
every sheet; print-color-adjust:exact scoped to the overlay. The design system
finally prints the marks it is named after.

Claude-Session: https://claude.ai/code/session_01CYKP1wE7CusnhuQm9CxTue
EOF
)"
```

---

## Task 3: Dogfood + docs + version bump

**Files:**
- Modify: `examples/docs.html:34` — add `tombo-trim` to the body class.
- Modify: `examples/components.html` — TOC link after line 64 + `#c18` section before line 447.
- Modify: `README.md` — `## Print` section before line 406 + pins on lines 39, 40, 65.
- Modify: `tombo.css:1`, `tombo.js:1` — banner version.

**Interfaces:**
- Consumes: `.tombo-trim` from Task 2.

- [ ] **Step 1: Opt `docs.html` in**

In `examples/docs.html`, line 34, change:
```html
<body class="tombo-gutters">
```
to:
```html
<body class="tombo-gutters tombo-trim">
```

- [ ] **Step 2: Add the catalog print section to `components.html`**

After line 64 (`<a href="#c17">17 — フォーム</a>`), add the TOC link:
```html
        <a href="#c18">18 — 印刷</a>
```

Before `</main>` (line 447), after the `#c17` section's closing `</section>`, add:
```html
      <section id="c18">
        <h2 class="tombo-sec">印刷</h2>
        <p class="note">TOMBO は名前どおり印刷の見当マーク。どのページも <code>@media print</code> で素直に刷れる（夜テーマも紙は白、コードは白地インク、トグルやコピーボタンは消える、計器ブロックは改ページで割れない）。さらに <code>&lt;body class="tombo-trim"&gt;</code> を付けると、紙面の余白に本物のトンボ——四隅の<strong>角トンボ</strong>と各辺中央の<strong>センタートンボ</strong>——がインク1色で毎ページ刷られる。ブラウザ印刷に裁ち落とし領域は無いので、単一の角トンボ（＝紙の端が真の仕上がり）を採る視覚的オマージュ。</p>
        <p class="note">このカタログ（<code>components.html</code>）自体は opt-in していないので、<kbd>⌘P</kbd> してもトンボは出ない。<code>docs.html</code> を <kbd>⌘P</kbd> するとトンボが出る。</p>
        <figure class="tombo-code">
          <figcaption><span>HTML</span><span>.TOMBO-TRIM</span></figcaption>
          <pre tabindex="0">&lt;body class="tombo-trim"&gt;
  &lt;!-- 中身は普段どおり。印刷すると余白にトンボが出る --&gt;
&lt;/body&gt;</pre>
        </figure>
      </section>
```

- [ ] **Step 3: Add the README `## Print` section**

In `README.md`, insert before line 406 (`## Contrast gate`), after the Forms section's last line (405):

```markdown
## Print

TOMBO is named after the printer's registration mark, so it prints like one.

**Hardening is unconditional.** Any TOMBO page prints cleanly: a `hotaru` page prints on white paper (not a black rectangle), the dark code panel repaints to ink-on-white so it stays readable, the theme toggle and copy buttons disappear, glow and motion are dropped, and instrument blocks (`.tombo-metric`, `.tombo-callout`, `.tombo-code`, figures, table rows) don't split across a page break. The page margin is a consistent `16mm`.

**Real トンボ are opt-in.** Add `tombo-trim` to `<body>` and every printed sheet gets actual printer's marks in ink: a single 角トンボ (corner crop mark) at each of the four corners, and a センタートンボ (registration ring + crosshair) at each edge center.

```html
<body class="tombo-trim">
  <!-- your page — print it (⌘P) to see the トンボ -->
</body>
```

The marks are `--tombo-ink` — registration black, the all-plate alignment color — never shu (shu stays reserved for current-position lines). Browser print has no bleed area, so the corner mark is a single line at the true trim (the sheet edge), an honest homage rather than an imposition-accurate double mark with a fake bleed line.
```

- [ ] **Step 4: Bump vendoring pins + banners**

In `README.md`, change `v0.10.0:` → `v0.11.0:` on lines 39, 40, 65:
```bash
git grep -n 'v0.10.0:' README.md   # expect 3 hits (lines 39, 40, 65)
```
(Edit each `git -C /path/to/tombo show v0.10.0:…` to `v0.11.0:`.)

In `tombo.css:1`:
```css
/*! TOMBO v0.11.0 — wadakatu design system. MIT. https://github.com/wadakatu/tombo */
```
In `tombo.js:1`:
```css
/*! TOMBO tombo.js v0.11.0 — wadakatu design system. Optional, zero-dependency. MIT. https://github.com/wadakatu/tombo */
```

- [ ] **Step 5: Verify docs + dogfood in chrome-devtools (both themes)**

- Reload `examples/docs.html` under print emulation: the トンボ appear (Task 2 result), both `tombo` and `hotaru`.
- Reload `examples/components.html` on screen: section `#c18` renders, TOC link `18 — 印刷` present and anchors to it; no layout break; both themes.
- `grep -n 'v0.11.0' tombo.css tombo.js` → banners bumped; `git grep -n 'v0.10.0' README.md` → **no hits**.

- [ ] **Step 6: Full gate + commit**

Run:
```bash
node --check tombo.js && python3 scripts/check_contrast.py
```
Expected: `node --check` clean; contrast all PASS.

```bash
git add tombo.css tombo.js README.md examples/docs.html examples/components.html
git commit -m "$(cat <<'EOF'
docs: dogfood .tombo-trim in docs.html, document print, bump to v0.11.0

docs.html opts into tombo-trim; components.html gains a print catalog entry;
README gains a Print section; banners and vendoring pins move to v0.11.0.

Claude-Session: https://claude.ai/code/session_01CYKP1wE7CusnhuQm9CxTue
EOF
)"
```

---

## Verification (whole feature)

1. `node --check tombo.js` — clean (banner-only change).
2. `python3 scripts/check_contrast.py` — all PASS (no new color).
3. chrome-devtools **print preview / emulation, both themes**:
   - Hardening: hotaru → white paper; code block ink-on-white readable; `.tombo-themes`/`.tombo-copy` gone; glow gone; `.tombo-metric` etc. not split.
   - Trim (`docs.html`): 角トンボ (4 corners) + センタートンボ (4 edge centers) print in ink, on **every** page; no body collision.
   - Non-opt-in (`app.html`): no marks.
4. `grep`: `@page`/`@media print` present; `print-color-adjust: exact` appears once (overlay only); banners + pins at v0.11.0; no `v0.10.0` left in README.

## Execution

**Recommended: inline execution.** The diff is one CSS file plus three doc touches, and Task 2's core (trim-mark geometry) is pinned against a real print preview that only the controller drives — a blind implementer subagent can't tune it. This mirrors the v0.9.0 cycle (controller authors the one-file change inline, then dispatches **one Opus whole-diff review** as the independent safety net). Per [[tombo-subagent-model-policy]] any subagent (the final review) runs on Opus.

If subagent-driven is chosen instead: Task 1 and Task 3 are subagent-suitable (deterministic); Task 2 must still be controller-pinned in the browser after the subagent lays down the starting CSS.

## Release (USER-GATED)

Local ff-merge of `feature/print` into `main`, lightweight tag `v0.11.0`, push (linear history, no force-push — same procedure as v0.7.0–v0.10.0). Then update `tombo-roadmap` memory: print done → v0.11.0; remaining = `text-autospace`/`palt`, CI.

## Out of scope (follow-up)
Bleed-accurate double 角トンボ, link-URL print expansion, `@page :left/:right` binding margins, margin-box running heads/folios (browsers don't implement margin-box `content`). `text-autospace`/`palt`, CI — separate roadmap items.
