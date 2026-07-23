# TOMBO Forms Vocabulary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a native-first, accessible forms vocabulary (`.tombo-field` / `.tombo-req` / `.tombo-select` / `.tombo-check` / `.tombo-fieldset` + control appearance and state rules) to `tombo.css`, then prove it with a real `/login` form in the app example and a catalog section in components.html.

**Architecture:** Additive/non-breaking (v0.10.0). All rules go in a new `@layer tombo.components` block appended to the end of `tombo.css`, scoped under `.tombo-field` / `.tombo-check` / `.tombo-fieldset` so nothing outside the system is restyled. Field look = "hybrid" (hairline box + a heavier bottom rule that carries state: green on focus, crimson on invalid). Labels use the mono instrument voice; the required marker is an ink `*` (shu stays line-only). Checkbox/radio use native `accent-color`. **No new color token** — every value reuses an existing token, so the contrast gate is unaffected.

**Tech Stack:** Plain CSS (`@layer`, `:is()`, logical properties, `accent-color`, `appearance`, `:user-invalid`, `@media (forced-colors)`). No build, no JS test runner. Verification = chrome-devtools computed-style/screenshots (both themes) + keyboard/AT spot-checks + forced-colors emulation + `check_contrast.py` + `node --check` + grep.

## Global Constraints

- **Version v0.10.0** (additive minor). Bump `tombo.css:1` and `tombo.js:1` banners `v0.9.0 → v0.10.0`, and every README `v0.9.0:` vendoring pin → `v0.10.0:`.
- **No new color, no token-value change, no `@layer` reorder, no markup/selector change to existing components.** Reuse only: `--tombo-ink`, `--tombo-ink-sub`, `--tombo-ink-faint`, `--tombo-green`, `--tombo-error`, `--tombo-hairline`, `--tombo-surface`, `--tombo-paper`, the `--tombo-space-*`, `--tombo-text-*`/`--tombo-lh-*`, `--tombo-font-*`, `--tombo-dur`, `--tombo-ease` tokens.
- **All new rules live in `@layer tombo.components`** (a new block appended to the end of `tombo.css`). The `tombo.reset` line `button, input, select, textarea { font: inherit; color: inherit; }` stays as-is; do NOT add global (unscoped) input styling.
- **Control allowlist (verbatim — boxes exactly these; date/range/color/file/checkbox/radio stay native by omission):**
  `input:not([type]), input[type="text"], input[type="email"], input[type="password"], input[type="number"], input[type="search"], input[type="tel"], input[type="url"], select, textarea`
- **Field look (hybrid C):** `background: var(--tombo-surface); border: 1px solid var(--tombo-hairline); border-block-end: 1.5px solid var(--tombo-ink-sub);` padding `var(--tombo-space-8) var(--tombo-space-12)`, no border-radius.
- **States:** focus (`:focus`) → `border-block-end-color: var(--tombo-green)` (the 2px green ring is the existing base `:focus-visible` outline — do not add another). invalid (`:user-invalid`, and `[aria-invalid="true"]`) → `border-block-end-color: var(--tombo-error)`. disabled (`:disabled`) → `opacity: .5; cursor: not-allowed`. readonly (`:read-only:not(:disabled)`) → `background: var(--tombo-paper); border-block-end-color: var(--tombo-hairline)`.
- **Label voice:** mono, uppercase, `letter-spacing:.14em`, weight 500, `--tombo-ink-sub`. **Required marker `.tombo-req`:** `color: var(--tombo-ink)` — never shu.
- **help/error:** body face, `--tombo-text-note`; help `--tombo-ink-faint`, error `--tombo-error` with a non-color `::before "!\00a0"`.
- **checkbox/radio:** native `accent-color: var(--tombo-green)`; `.tombo-check` row `min-block-size: 24px` (WCAG 2.5.8 target size); control box 18px.
- **select caret:** `.tombo-select` wrapper, `appearance: none` + a themeable `::after` chevron drawn with `--tombo-ink-sub` borders; `@media (forced-colors: active)` restores `appearance: auto` and hides the chevron.
- **fieldset:** `.tombo-fieldset { border:0; padding:0; min-inline-size:0; }`, `legend` in the mono label voice. Radio/checkbox groups go in `<fieldset><legend>`.
- **Verify every visual change in both `tombo` (day) and `hotaru` (night).** Forms are new (no "drift" baseline) — verify the states read deliberately and nothing collapses/clips.
- **Contrast gate must stay green** (no color touched — run as hygiene). `node --check tombo.js` clean (banner only).
- Spec: `docs/superpowers/specs/2026-07-23-tombo-forms-design.md`.

---

### Task 1: Text-field vocabulary (`.tombo-field` + control appearance + states)

**Files:**
- Modify: `tombo.css` — append a new `@layer tombo.components { … }` block at end of file (after the current final `}` on line ~370).

**Interfaces:**
- Produces: `.tombo-field` (block), `.tombo-field > label` (mono label), `.tombo-req` (ink `*`), `.tombo-field .help` / `.tombo-field .error` (messages), and the control appearance + `:focus`/`:user-invalid`/`[aria-invalid]`/`:disabled`/`:read-only` state rules for the allowlisted controls.
- Consumes: existing tokens only.

- [ ] **Step 1: Append the text-field block.** Add to the END of `tombo.css` (new top-level block, keeping the file's existing two-`@layer tombo.components` style):

```css
@layer tombo.components {
  /* forms — native-first field vocabulary (spec 2026-07-23). Everything is
     scoped to .tombo-field / .tombo-check / .tombo-fieldset so it never
     restyles inputs outside the system. Field look = hybrid: a hairline box
     with a heavier bottom rule that carries state (green focus / crimson
     invalid) — the instrument's reading line. Adds no new color. */
  .tombo-field > label {
    display: block; margin-block-end: var(--tombo-space-8);
    font-family: var(--tombo-font-mono);
    font-size: var(--tombo-text-label); line-height: var(--tombo-lh-label);
    font-weight: 500; letter-spacing: .14em; text-transform: uppercase;
    color: var(--tombo-ink-sub);
  }
  .tombo-req { color: var(--tombo-ink); margin-inline-start: .3em; } /* required *, never shu */
  .tombo-field .help,
  .tombo-field .error {
    margin-block-start: var(--tombo-space-8);
    font-size: var(--tombo-text-note); line-height: var(--tombo-lh-note);
  }
  .tombo-field .help  { color: var(--tombo-ink-faint); }
  .tombo-field .error { color: var(--tombo-error); }
  .tombo-field .error::before { content: "!\00a0"; font-weight: 700; } /* non-color cue (1.4.1) */

  /* control appearance — the allowlist boxes exactly text-like inputs, select,
     textarea; date/range/color/file/checkbox/radio stay native by omission */
  .tombo-field :is(
    input:not([type]), input[type="text"], input[type="email"], input[type="password"],
    input[type="number"], input[type="search"], input[type="tel"], input[type="url"],
    select, textarea
  ) {
    inline-size: 100%;
    background: var(--tombo-surface);
    border: 1px solid var(--tombo-hairline);
    border-block-end: 1.5px solid var(--tombo-ink-sub); /* the measured baseline */
    padding: var(--tombo-space-8) var(--tombo-space-12);
    font-family: var(--tombo-font-body);
    font-size: var(--tombo-text-ui); line-height: var(--tombo-lh-ui);
    color: var(--tombo-ink);
    transition: border-color var(--tombo-dur) var(--tombo-ease);
  }
  /* focus — the baseline lights (mouse or keyboard). The 2px green ring is the
     base-layer :focus-visible outline; the two are layers, not duplicates. */
  .tombo-field :is(
    input:not([type]), input[type="text"], input[type="email"], input[type="password"],
    input[type="number"], input[type="search"], input[type="tel"], input[type="url"],
    select, textarea
  ):focus { border-block-end-color: var(--tombo-green); }
  /* invalid — :user-invalid fires only after interaction (not on load); the
     [aria-invalid] hook is the universal fallback for scripted/server validation */
  .tombo-field :is(
    input:not([type]), input[type="text"], input[type="email"], input[type="password"],
    input[type="number"], input[type="search"], input[type="tel"], input[type="url"],
    select, textarea
  ):user-invalid,
  .tombo-field :is(
    input:not([type]), input[type="text"], input[type="email"], input[type="password"],
    input[type="number"], input[type="search"], input[type="tel"], input[type="url"],
    select, textarea
  )[aria-invalid="true"] { border-block-end-color: var(--tombo-error); }
  /* disabled — matches .tombo-btn:disabled */
  .tombo-field :is(
    input:not([type]), input[type="text"], input[type="email"], input[type="password"],
    input[type="number"], input[type="search"], input[type="tel"], input[type="url"],
    select, textarea
  ):disabled { opacity: .5; cursor: not-allowed; }
  /* readonly — recessed to paper, baseline de-emphasized to hairline (select is
     never readonly, so it is absent from this list) */
  .tombo-field :is(
    input:not([type]), input[type="text"], input[type="email"], input[type="password"],
    input[type="number"], input[type="search"], input[type="tel"], input[type="url"],
    textarea
  ):read-only:not(:disabled) {
    background: var(--tombo-paper);
    border-block-end-color: var(--tombo-hairline);
  }
}
```

- [ ] **Step 2: Verify computed styles per state (chrome-devtools, controller-run, day theme).** Load `examples/app.html`, run:

```js
() => {
  document.documentElement.dataset.theme='tombo';
  const b=document.createElement('div');
  b.innerHTML=`<div class="tombo-field"><label for="r">NAME<span class="tombo-req" id="rq">*</span></label>
    <input id="r" type="text"><p class="help">h</p><p class="error" id="er">e</p></div>
    <input class="x" id="f" type="text"><input class="x" id="iv" type="text" aria-invalid="true">
    <input class="x" id="d" type="text" disabled><input class="x" id="ro" type="text" readonly>`;
  // wrap the bare test inputs so they get the .tombo-field scope:
  ['f','iv','d','ro'].forEach(id=>{const w=document.createElement('div');w.className='tombo-field';
    const el=b.querySelector('#'+id);el.replaceWith(w);w.appendChild(el);});
  document.body.appendChild(b);
  const cs=id=>getComputedStyle(b.querySelector('#'+id));
  b.querySelector('#f').focus();
  return {
    rest_baseline: cs('r').borderBottomColor, rest_bg: cs('r').backgroundColor,
    focus_baseline: cs('f').borderBottomColor,
    invalid_baseline: cs('iv').borderBottomColor,
    disabled_opacity: cs('d').opacity,
    readonly_bg: cs('ro').backgroundColor, readonly_baseline: cs('ro').borderBottomColor,
    label_font: cs('r').fontFamily, req_color: getComputedStyle(b.querySelector('#rq')).color,
    error_before: getComputedStyle(b.querySelector('#er'),'::before').content
  };
}
```
Expected (day): `rest_baseline: "rgb(76, 86, 80)"` (ink-sub), `rest_bg: "rgb(250, 251, 248)"` (surface), `focus_baseline: "rgb(14, 90, 71)"` (green), `invalid_baseline: "rgb(166, 48, 28)"` (error), `disabled_opacity: "0.5"`, `readonly_bg: "rgb(242, 244, 239)"` (paper), `readonly_baseline: "rgba(26, 33, 29, 0.16)"` (hairline), `label_font` contains `"Martian Mono"`, `req_color: "rgb(26, 33, 29)"` (ink), `error_before` contains `"!"`.

- [ ] **Step 3: Contrast gate (hygiene) + commit.**

```bash
python3 scripts/check_contrast.py   # expect all PASS (no color changed)
git add tombo.css
git commit -m "feat: add the .tombo-field text-field vocabulary (hybrid look, states)"
```

---

### Task 2: Styled select caret (`.tombo-select`)

**Files:**
- Modify: `tombo.css` — append to the same forms `@layer tombo.components` block, after the Task 1 rules.

**Interfaces:**
- Consumes: `.tombo-field select` appearance from Task 1.
- Produces: `.tombo-select` wrapper that removes the native arrow and draws a themeable chevron; reverts to native under forced-colors.

- [ ] **Step 1: Append the select-caret rules.**

```css
@layer tombo.components {
  /* select caret — the OS arrow breaks the instrument look, so draw our own.
     A themeable chevron needs border-color tokens (a data-URI image can't
     follow the theme), so it lives on a .tombo-select wrapper's ::after. */
  .tombo-select { position: relative; display: block; }
  /* scoped under .tombo-field so it matches the base control rule's specificity
     (0,2,1) and wins on source order — an unscoped `.tombo-select select` (0,1,1)
     would lose padding-inline-end to the base `padding` shorthand */
  .tombo-field .tombo-select select { appearance: none; padding-inline-end: var(--tombo-space-32); }
  .tombo-select::after {
    content: ""; position: absolute; inset-inline-end: var(--tombo-space-12); inset-block-start: 50%;
    inline-size: 7px; block-size: 7px;
    border-inline-end: 1.5px solid var(--tombo-ink-sub);
    border-block-end: 1.5px solid var(--tombo-ink-sub);
    transform: translateY(-70%) rotate(45deg); pointer-events: none;
  }
  @media (forced-colors: active) {
    .tombo-field .tombo-select select { appearance: auto; padding-inline-end: var(--tombo-space-12); }
    .tombo-select::after { display: none; } /* restore the native arrow so it never vanishes */
  }
}
```

- [ ] **Step 2: Verify caret + forced-colors (chrome-devtools, controller-run).** Load `examples/app.html`, run:

```js
() => {
  const b=document.createElement('div'); b.className='tombo-field';
  b.innerHTML=`<div class="tombo-select"><select id="s"><option>A</option></select></div>`;
  document.body.appendChild(b);
  const s=b.querySelector('#s'); const after=getComputedStyle(b.querySelector('.tombo-select'),'::after');
  return { appearance: getComputedStyle(s).appearance, caret_border: after.borderRightColor,
    caret_content: after.content, pad_end: getComputedStyle(s).paddingInlineEnd };
}
```
Expected (normal mode): `appearance: "none"`, `caret_border: "rgb(76, 86, 80)"` (ink-sub, day), `caret_content: "\"\""`, `pad_end: "32px"`.
Then emulate forced-colors and re-check appearance:
```js
// controller: mcp__chrome-devtools__emulate to set forced-colors: active, then:
() => getComputedStyle(document.querySelector('.tombo-select select')).appearance
```
Expected under forced-colors: `"auto"`. (Reset the emulation afterward.)

- [ ] **Step 3: Commit.**

```bash
git add tombo.css
git commit -m "feat: add the .tombo-select themeable caret (native under forced-colors)"
```

---

### Task 3: Checkbox/radio + fieldset (`.tombo-check`, `.tombo-fieldset`, accent-color)

**Files:**
- Modify: `tombo.css` — append to the same forms `@layer tombo.components` block, after Task 2.

**Interfaces:**
- Produces: `accent-color` scope, `.tombo-check` (inline control row), `.tombo-fieldset` + `legend` (grouping).

- [ ] **Step 1: Append the checkbox/fieldset rules.**

```css
@layer tombo.components {
  /* checkbox / radio — native accent-color (a11y, zero-JS, OS-consistent);
     green because a selection is not an error or a current position */
  :where(.tombo-field, .tombo-check, .tombo-fieldset) { accent-color: var(--tombo-green); }
  .tombo-check { /* the <label> is the row and the whole click target */
    display: flex; align-items: center; gap: var(--tombo-space-8);
    min-block-size: 24px; /* WCAG 2.5.8 target size (minimum) */
    font-size: var(--tombo-text-ui); line-height: var(--tombo-lh-ui);
  }
  .tombo-check input { inline-size: 18px; block-size: 18px; }
  /* fieldset — reset native chrome; min-inline-size:0 defeats the fieldset
     min-content shrink bug inside flex/grid; radio groups need fieldset+legend */
  .tombo-fieldset { border: 0; padding: 0; min-inline-size: 0; }
  .tombo-fieldset > legend {
    padding: 0; margin-block-end: var(--tombo-space-8);
    font-family: var(--tombo-font-mono);
    font-size: var(--tombo-text-label); line-height: var(--tombo-lh-label);
    font-weight: 500; letter-spacing: .14em; text-transform: uppercase;
    color: var(--tombo-ink-sub);
  }
}
```

- [ ] **Step 2: Verify (chrome-devtools, controller-run, day theme).** Load `examples/app.html`, run:

```js
() => {
  document.documentElement.dataset.theme='tombo';
  const b=document.createElement('div');
  b.innerHTML=`<fieldset class="tombo-fieldset" id="fs"><legend id="lg">MODE</legend>
    <label class="tombo-check" id="ck"><input type="radio" name="m"> Strict</label></fieldset>`;
  document.body.appendChild(b);
  const cs=id=>getComputedStyle(b.querySelector('#'+id));
  return { accent: cs('ck').accentColor.replace(/\s/g,''),
    row_minh: cs('ck').minBlockSize, row_display: cs('ck').display,
    fs_border: cs('fs').borderTopWidth, fs_minw: cs('fs').minInlineSize,
    legend_font: cs('lg').fontFamily, legend_transform: cs('lg').textTransform };
}
```
Expected: `accent` is `"rgb(14,90,71)"` (green, day), `row_minh: "24px"`, `row_display: "flex"`, `fs_border: "0px"`, `fs_minw: "0px"`, `legend_font` contains `"Martian Mono"`, `legend_transform: "uppercase"`.

- [ ] **Step 3: Commit.**

```bash
git add tombo.css
git commit -m "feat: add .tombo-check and .tombo-fieldset (native accent-color, grouping)"
```

---

### Task 4: Build the `/login` form in the app example

**Files:**
- Modify: `examples/app.html` — add rules to its `<style>` (after line 26 `.foot {…}`) and a `<section class="login">` inside `<main>` after the `.tombo-table-wrap` block (after line 76).

**Interfaces:**
- Consumes: `.tombo-field`, `.tombo-req`, `.tombo-check`, `.tombo-btn` (existing), `.tombo-flow` (existing).

- [ ] **Step 1: Add login styles.** Append to `examples/app.html` `<style>` (before `</style>` on line 27):

```css
  .login { max-inline-size: 380px; margin-top: var(--tombo-space-48); }
  .login h2 { font-size: var(--tombo-text-h3); line-height: var(--tombo-lh-h3); }
  .login .cap { margin-top: var(--tombo-space-4); }
  .login form { margin-top: var(--tombo-space-24); }
  .login .reqnote { color: var(--tombo-ink-faint); }
```

- [ ] **Step 2: Add the login section.** Insert inside `<main class="tombo-shell">`, immediately after the closing `</div>` of `.tombo-table-wrap` (after line 76, before `</main>`):

```html
    <section class="login" aria-labelledby="login-h">
      <h2 id="login-h">サインイン</h2>
      <p class="tombo-fig cap">FIG. — /LOGIN · SCREEN PREVIEW</p>
      <form class="tombo-flow" action="#" method="post">
        <p class="tombo-label reqnote"><span class="tombo-req" aria-hidden="true">*</span> 必須</p>
        <div class="tombo-field">
          <label for="email">EMAIL<span class="tombo-req" aria-hidden="true">*</span></label>
          <input id="email" type="email" name="email" required autocomplete="email"
                 value="wadakatu@" aria-invalid="true" aria-describedby="email-err">
          <p class="error" id="email-err">メールアドレスの形式が正しくありません。</p>
        </div>
        <div class="tombo-field">
          <label for="pw">PASSWORD<span class="tombo-req" aria-hidden="true">*</span></label>
          <input id="pw" type="password" name="password" required autocomplete="current-password"
                 aria-describedby="pw-help">
          <p class="help" id="pw-help">8 文字以上。</p>
        </div>
        <label class="tombo-check"><input type="checkbox" name="remember"> ログイン状態を保持する</label>
        <button class="tombo-btn tombo-btn--primary" type="submit">サインイン</button>
      </form>
    </section>
```

- [ ] **Step 3: Screenshots, both themes (chrome-devtools, controller-run).** Load `examples/app.html`. Screenshot day (`data-theme=tombo`) and night (`data-theme=hotaru`). Confirm: the email field shows the crimson invalid baseline + "! …" error message; the password field shows the resting baseline + help; the "* 必須" legend and the ink `*` markers read clearly; the checkbox is a green tick; the submit button is unchanged; nothing collapses at 380px in either theme.

- [ ] **Step 4: Keyboard + `:user-invalid` + forced-colors spot-check (chrome-devtools, controller-run).**
  - Tab from the address bar into the form; confirm each control shows the 2px green `:focus-visible` ring, and the `.tombo-check` label toggles when its text is clicked.
  - In a fresh field: focus the password, type `abc`, then focus email and back — confirm `:user-invalid` does NOT fire on the untouched password (baseline stays ink-sub). Then clear the email's `aria-invalid` in devtools, type `abc` into email, blur → confirm `:user-invalid` turns the baseline crimson.
  - Emulate forced-colors: confirm the form stays legible and any `.tombo-select` (none here, checked in Task 2) would revert; reset emulation.

- [ ] **Step 5: Commit.**

```bash
git add examples/app.html
git commit -m "feat: build the /login form in the app example with the forms vocabulary"
```

---

### Task 5: Add a Forms section to the component catalog

**Files:**
- Modify: `examples/components.html` — add a TOC link after line 63 (`<a href="#c16">…`) and a `<section id="c17">` after the `#c16` section's closing `</section>` (line 380), before `</main>`.

**Interfaces:**
- Consumes: the full forms vocabulary (Tasks 1–3).

- [ ] **Step 1: Add the TOC entry.** After the `#c16` line in `<nav class="tombo-toc">` (line 63):

```html
        <a href="#c17">17 — フォーム</a>
```

- [ ] **Step 2: Add the catalog section.** Insert after the `</section>` that closes `#c16` (line 380), before `</main>`:

```html
      <section id="c17">
        <h2 class="tombo-sec">フォーム</h2>
        <p class="note">ネイティブ優先。造形は <code>.tombo-field</code> の中でだけ効く（外の input は素のまま）。ハイブリッド＝ hairline のボックス＋状態を運ぶ下ルール（focus=green・invalid=臙脂）。ラベルは等幅の計器声、required は ink の <code>*</code>（朱は線専用のまま）。checkbox/radio はネイティブ <code>accent-color</code>。エラーは <code>aria-describedby</code> と <code>aria-invalid</code> で結線する。</p>
        <div class="demo">
          <form class="tombo-flow" action="#" style="max-width:420px">
            <p class="tombo-label" style="color:var(--tombo-ink-faint)"><span class="tombo-req" aria-hidden="true">*</span> 必須</p>
            <div class="tombo-field">
              <label for="d-name">PROJECT NAME<span class="tombo-req" aria-hidden="true">*</span></label>
              <input id="d-name" type="text" required aria-describedby="d-name-help" value="gesso-openapi">
              <p class="help" id="d-name-help">小文字・ハイフン区切り。</p>
            </div>
            <div class="tombo-field">
              <label for="d-cov">COVERAGE THRESHOLD<span class="tombo-req" aria-hidden="true">*</span></label>
              <input id="d-cov" type="text" required aria-invalid="true" aria-describedby="d-cov-err" value="ninety">
              <p class="error" id="d-cov-err">0 から 100 の数値を入力してください。</p>
            </div>
            <div class="tombo-field">
              <label for="d-fw">FRAMEWORK ADAPTER</label>
              <div class="tombo-select">
                <select id="d-fw"><option>Laravel</option><option>Symfony</option><option>Pest</option></select>
              </div>
            </div>
            <div class="tombo-field">
              <label for="d-note">NOTES</label>
              <textarea id="d-note" rows="2">PATCH /users/{id} · 422 still untested.</textarea>
            </div>
            <div class="tombo-field">
              <label for="d-lock">LOCKED FIELD</label>
              <input id="d-lock" type="text" value="read-only" readonly>
            </div>
            <fieldset class="tombo-fieldset">
              <legend>MODE</legend>
              <label class="tombo-check"><input type="radio" name="d-m" checked> Strict mode</label>
              <label class="tombo-check"><input type="radio" name="d-m"> Lenient mode</label>
              <label class="tombo-check"><input type="checkbox" checked> Validate responses</label>
            </fieldset>
            <button class="tombo-btn tombo-btn--primary" type="submit">Save</button>
          </form>
        </div>
        <figure class="tombo-code">
          <figcaption><span>HTML</span><span>.TOMBO-FIELD</span></figcaption>
          <pre tabindex="0">&lt;div class="tombo-field"&gt;
  &lt;label for="cov"&gt;COVERAGE THRESHOLD&lt;span class="tombo-req" aria-hidden="true"&gt;*&lt;/span&gt;&lt;/label&gt;
  &lt;input id="cov" type="number" required
         aria-describedby="cov-help cov-err" aria-invalid="true"&gt;
  &lt;p class="help"  id="cov-help"&gt;0–100 の整数。&lt;/p&gt;
  &lt;p class="error" id="cov-err"&gt;0 から 100 の数値を入力してください。&lt;/p&gt;
&lt;/div&gt;

&lt;div class="tombo-select"&gt;&lt;select&gt;…&lt;/select&gt;&lt;/div&gt;

&lt;fieldset class="tombo-fieldset"&gt;
  &lt;legend&gt;MODE&lt;/legend&gt;
  &lt;label class="tombo-check"&gt;&lt;input type="radio" name="m"&gt; Strict&lt;/label&gt;
&lt;/fieldset&gt;</pre>
        </figure>
      </section>
```

- [ ] **Step 3: Screenshots, both themes (chrome-devtools, controller-run).** Load `examples/components.html`. Screenshot day and night. Confirm the `#c17` section renders every control and state (resting name w/ help, invalid coverage w/ error, styled select caret, textarea, readonly, radio+checkbox group in a fieldset, submit), the caret follows the theme, and nothing overflows the `.demo` box in either theme.

- [ ] **Step 4: Commit.**

```bash
git add examples/components.html
git commit -m "feat: add the forms section to the component catalog"
```

---

### Task 6: Document Forms in the README

**Files:**
- Modify: `README.md` — insert a `## Forms` section after the `## Glow` section (after line 360), before `## Contrast gate` (line 362).

**Interfaces:** none (docs).

- [ ] **Step 1: Insert the Forms section.** Add between `## Glow` and `## Contrast gate`:

````markdown
## Forms

Native-first: TOMBO styles real `input` / `select` / `textarea` / `checkbox` / `radio` — no JS, no custom widgets. The look only applies inside `.tombo-field` (and `.tombo-check` / `.tombo-fieldset`), so it never hijacks an input elsewhere on the page.

A field is a hairline box with a heavier bottom rule that carries its state — the instrument's reading line: it lights **green** on focus and **crimson** on invalid. Labels use the mono instrument voice; the required marker is an ink `*` (shu stays reserved for current-position lines). Checkbox and radio use the native `accent-color`.

| Class | Role |
|---|---|
| `.tombo-field` | one field: label → control → help/error, stacked |
| `.tombo-req` | the required marker (`*`) inside a label |
| `.tombo-select` | wrapper that gives a `<select>` a themeable caret |
| `.tombo-check` | one checkbox/radio row (the `<label>` is the whole target) |
| `.tombo-fieldset` | a native `<fieldset>` reset, with a mono `<legend>` — for radio/checkbox groups |

```html
<div class="tombo-field">
  <label for="cov">COVERAGE THRESHOLD<span class="tombo-req" aria-hidden="true">*</span></label>
  <input id="cov" type="number" required
         aria-describedby="cov-help cov-err" aria-invalid="true">
  <p class="help"  id="cov-help">0–100 の整数。</p>
  <p class="error" id="cov-err">0 から 100 の数値を入力してください。</p>
</div>

<div class="tombo-field">
  <label for="fw">FRAMEWORK</label>
  <div class="tombo-select"><select id="fw"><option>Laravel</option></select></div>
</div>

<fieldset class="tombo-fieldset">
  <legend>MODE</legend>
  <label class="tombo-check"><input type="radio" name="m" checked> Strict</label>
  <label class="tombo-check"><input type="radio" name="m"> Lenient</label>
</fieldset>
```

The CSS styles the states; you own the accessible markup:

- Wire `label[for]` to `control[id]`; point `aria-describedby` at **both** the help and error ids (space-separated).
- Set `aria-invalid="true"` only when a field is in error; mark required with the native `required` attribute; show a "**\* required**" note once per form.
- Put radio/checkbox groups in `<fieldset><legend>`.
- States are pure CSS: `:focus` (baseline green) + the base `:focus-visible` ring, `:user-invalid` **and** `[aria-invalid="true"]` (baseline crimson), `:disabled` (dimmed), `:read-only` (recessed). `:user-invalid` shows validation only after the reader interacts; the `[aria-invalid]` hook covers scripted or server-side validation.

Controls are `width:100%`, so keep the form's container to a comfortable measure (a login form around `380px`, a settings form no wider than the reading measure) rather than the full page width. Deep styling of `range` / `color` / `file` / date pickers is deliberately left native.
````

- [ ] **Step 2: Verify render (controller).** Read the section back (or open `README.md` in a Markdown preview) and confirm the table, both code fences, and the list render with no broken markup. Grep confirms placement:

```bash
grep -n "^## Forms" README.md            # exists, between Glow and Contrast gate
grep -n "^## Contrast gate" README.md     # still present, after Forms
```

- [ ] **Step 3: Commit.**

```bash
git add README.md
git commit -m "docs: document the forms vocabulary in the README"
```

---

### Task 7: Bump banners and vendoring pins to v0.10.0

**Files:**
- Modify: `tombo.css:1`, `tombo.js:1`, `README.md` (the `v0.9.0:` vendoring pins).

**Interfaces:** none.

- [ ] **Step 1: Bump the two banners.**
  - `tombo.css:1`: `/*! TOMBO v0.9.0 —` → `/*! TOMBO v0.10.0 —`
  - `tombo.js:1`: `TOMBO tombo.js v0.9.0 —` → `TOMBO tombo.js v0.10.0 —`

- [ ] **Step 2: Bump the README vendoring pins.** Replace every `v0.9.0:` with `v0.10.0:` (the three `git … show v0.9.0:…` lines in Quick start and Loading — currently README lines 39, 40, 65).

- [ ] **Step 3: Verify no stale version string remains + JS still parses.**

```bash
grep -rn "v0\.9\.0" tombo.css tombo.js README.md   # expect: no matches
node --check tombo.js                                # expect: clean (banner only)
```

- [ ] **Step 4: Commit.**

```bash
git add tombo.css tombo.js README.md
git commit -m "chore: bump the banners and vendoring pins to v0.10.0"
```

---

## Final verification (whole branch, before release)

- `python3 scripts/check_contrast.py` → all PASS (no color touched).
- `node --check tombo.js` → clean.
- `grep -n "border-radius\|border-block-end\|accent-color" tombo.css` → confirm the forms rules are present and use tokens; no raw off-scale px introduced (only the a11y constants 18px/24px/7px and border widths, which are geometry).
- chrome-devtools: `examples/app.html` (login) and `examples/components.html` (#c17) in **both** themes; keyboard focus ring; `.tombo-check` target; `:user-invalid`; `.tombo-select` caret theming; forced-colors revert.

## Release (USER-GATED — do not run without an explicit go)

Local ff-merge of `feature/forms` into `main`, lightweight tag `v0.10.0`, push both (same procedure as v0.7.0–v0.9.0 — linear history, no force-push). Then update `tombo-roadmap` memory: forms done → v0.10.0; remaining = `@media print`, `text-autospace`/`palt`, CI.

## Out of scope (follow-up)

`.tombo-form` wrapper (accent-color scope + measure cap), deep range/color/file/date-picker styling, JS client validation, `@media print`, `text-autospace`/`palt`, CI.
