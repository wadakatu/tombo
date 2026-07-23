<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/tombo-mark-dark.svg">
    <img src="assets/logo/tombo-mark.svg" alt="TOMBO mark — a dragonfly drawn as a printer's registration mark" width="92">
  </picture>
</p>
<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/tombo-wordmark-dark.svg">
    <img src="assets/logo/tombo-wordmark.svg" alt="TOMBO" width="320">
  </picture>
</h1>

A single-file CSS design system for everything wadakatu ships — OSS docs sites, web apps, LPs, portfolios. Zero dependencies, one `<link>` — an optional `tombo.js` adds theme persistence and copy buttons, but no page needs it.

The goal is not a component library. It's recognition: the same handful of signature marks, repeated without exception across every product, at a "volume" tuned to context — quiet in docs, loud in an LP.

## Name

**トンボ (tombo)** is a printer's registration mark — the small cross drawn on a printing plate so every layer of ink aligns to the same point. It is the mark that measures.

It's also a homophone for **蜻蛉 (tombo)**, the dragonfly: an insect that only flies forward, never backward, which made it a symbol of victory (**勝ち虫**, *kachimushi*) to samurai. *Katu* (勝) — to win — hides inside *wadaKATU*.

The logo is a registration cross with two wing strokes and a tail tick in shu (朱, vermillion) — the same red the system uses everywhere else to mark "you are here."

The dark flavor is named **hotaru** (蛍, firefly): at night, the instruments glow.

## The three rules

1. **すべてを測る — measure everything.** Elements sit next to dimension lines, tick marks, and running numbers. The sense that something was measured before it was placed is what gives the page its air.
2. **銘は等幅 — inscriptions are monospace.** Numbers, labels, indices, and units are always set in mono. Body copy stays in a quiet sans; only the instrumentation gets to glow in mono.
3. **朱は現在地 — shu marks the current position.** Red is reserved for a 1–2px line that points at "here" — the current tab, the current TOC entry, the current ruler value. The moment it fills a shape, it stops being shu and becomes plain red.

## Quick start

This repository is private, so there is no CDN to link — jsDelivr's `gh` endpoint 404s on private repos, tag or no tag. Vendor the stylesheet from a tag instead:

```bash
git -C /path/to/tombo show v0.7.0:tombo.css > public/styles/tombo.css
git -C /path/to/tombo show v0.7.0:LICENSE   > public/styles/tombo.LICENSE
```

Then link your copy, alongside the three voices:

```html
<link rel="stylesheet" href="/styles/tombo.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@600;700&family=M+PLUS+2:wght@450;500;700&family=Martian+Mono:wdth,wght@75..112.5,400..600&display=swap" rel="stylesheet">
```

No build step, no framework — it's a single stylesheet, so any templating layer works (Astro, Laravel Blade, Vue, plain HTML). The font `<link>`s are optional: `tombo.css` declares font stacks with system fallbacks (`system-ui`, `ui-monospace`), so the page degrades gracefully without them.

A vendored copy drifts silently, so pin it: record the tag and the file's sha256 in the consuming repo and check it in CI. Then a hand-edit or a stale copy fails the build instead of turning into a mystery months later.

## Behavior (tombo.js)

`tombo.js` is optional. It's a single dependency-free file that layers three behaviors onto the CSS: theme persistence across visits, wiring for the `.tombo-themes` control, and copy buttons on code blocks. Nothing in `tombo.css` requires it — every page renders and works with the stylesheet alone.

### Loading

Vendor `tombo.js` the same way as `tombo.css`, from a tag, with the same sha256-pin discipline:

```bash
git -C /path/to/tombo show v0.7.0:tombo.js > public/scripts/tombo.js
```

Then wire two script tags around the page:

```html
<!-- in <head>, before paint: applies a stored theme with no flash -->
<script>try{var t=localStorage.getItem('tombo-theme');if(t==='tombo'||t==='hotaru')document.documentElement.dataset.theme=t}catch(e){}</script>
<!-- once, before </body> -->
<script src="/path/tombo.js" defer></script>
```

Both are optional, and independent of each other:

- **Neither** — the page still follows the OS theme (`color-scheme` handles that on its own); the `.tombo-themes` control stays hidden and code blocks get no copy button, since only `tombo.js` reveals and wires those.
- **The deferred `tombo.js`, no inline snippet** — a previously chosen `tombo`/`hotaru` theme still applies (`tombo.js` reads `localStorage` itself on load), and the theme control and copy buttons both work. But a reader who overrode their OS theme sees the OS-default theme paint first and then swap a moment later — a brief flash. A reader who never overrode it sees nothing, since the OS default and the stored choice already agree.
- **The inline snippet, no deferred script** — no flash, but nothing else: the `.tombo-themes` block never un-hides, no copy button appears, and `window.Tombo` doesn't exist.

### Theme control

You author the `.tombo-themes` markup; `tombo.js` reveals it and wires the clicks. Ship it `hidden`, since there's nothing to click when JS never runs:

```html
<div class="tombo-themes tombo-label" hidden>
  <button type="button" data-tombo-theme="system">system</button>
  <button type="button" data-tombo-theme="tombo">tombo</button>
  <button type="button" data-tombo-theme="hotaru">hotaru</button>
</div>
```

On load, `tombo.js` un-hides every `.tombo-themes[hidden]` block and sets `aria-pressed` on each button — `true` for whichever matches the current setting, `false` for the rest. Clicking any `[data-tombo-theme]` element calls `setTheme()` with its value: `tombo` and `hotaru` force that theme and persist it; `system` clears the stored choice and returns the page to following the OS.

### `window.Tombo`

```js
window.Tombo.setTheme('system' | 'tombo' | 'hotaru');
window.Tombo.getTheme(); // 'system' | 'tombo' | 'hotaru' — 'system' when nothing is stored
```

Use these instead of touching `localStorage['tombo-theme']` or `data-theme` by hand — `setTheme()` updates the stored value, `<html data-theme>`, and every `[data-tombo-theme]` button's `aria-pressed` state together in one call; changing only one of those leaves the others stale until the next click.

### Copy buttons

Every `.tombo-code` figure gets a copy button injected into its `figcaption` automatically (one is created if the block doesn't already have one) — no markup required beyond the block itself:

```html
<figure class="tombo-code">
  <figcaption><span>SHELL — INSTALL</span></figcaption>
  <pre tabindex="0">$ composer require wadakatu/laravel-spectrum</pre>
</figure>
```

Opt a block out with `data-tombo-copy="off"`:

```html
<figure class="tombo-code" data-tombo-copy="off">
  <pre tabindex="0">…</pre>
</figure>
```

The button copies the `<pre>`'s text via the Clipboard API, reads "COPIED ✓" for 1.5s, and falls back to an `aria-live` announcement ("Press Ctrl or Cmd + C to copy") if the clipboard call is unavailable or is rejected.

Give every code `<pre>` inside `.tombo-code` a `tabindex="0"`, whether or not `tombo.js` is loaded — it's a horizontally-scrolling region, and one that can't take focus is unreachable by keyboard.

### SSR (optional upgrade)

`localStorage` is the universal default, but a server-rendered consumer (Blade, Astro SSR) can go one step further: store the choice in a cookie instead of — or alongside — `localStorage`, read it on the server, and emit `data-theme` on `<html>` directly in the response HTML. That skips even the inline boot snippet, since there's nothing left to apply client-side before paint. `tombo.js` itself only ever reads `localStorage`; the cookie round-trip is something the consuming app implements on its own.

## Type

Three voices, selected zero-base with the reader first (see `docs/superpowers/specs/2026-07-21-tombo-typography-design.md`):

| Voice | Face | Role |
|---|---|---|
| DISPLAY | Instrument Sans 700 | Latin display headings only (tracking -.015em never touches Japanese) |
| BODY | M PLUS 2 at weight 450 | Japanese body, UI copy, Japanese headings |
| INSTRUMENT | Martian Mono | labels, numbers, indices, code (code condenses to width 87.5%) |

A 10-step type scale (`--tombo-text-*` / `--tombo-lh-*`, body 15px/30px) replaces all ad-hoc sizes — components may only reference scale tokens.

## Themes

TOMBO ships two flavors, structured like catppuccin's: one umbrella system name, two `data-theme` values.

| Theme | Role |
|---|---|
| `tombo` | Day drawing (light, default) |
| `hotaru` | Night drawing (dark) |

By default the page follows the OS via `color-scheme: light dark` and `light-dark()` token values — no flag needed. To force a theme, set `data-theme` on `<html>`:

```html
<html data-theme="hotaru">
```

```js
document.documentElement.dataset.theme = "hotaru"; // or "tombo"
```

## Tokens

Prefix: `--tombo-`. Only the values change between themes; the token names don't.

### tombo (day)

| Token | Value | Use |
|---|---|---|
| paper | `#F2F4EF` | page background (greenish drafting paper) |
| surface | `#FAFBF8` | cards / panels (+1 step) |
| ink | `#1A211D` | body text, primary rules |
| ink-sub | `#4C5650` | secondary text |
| ink-faint | `#667069` | annotations, numbers |
| hairline | `rgba(26,33,29,.16)` | rules |
| grid | `rgba(26,33,29,.07)` | graph paper |
| green | `#0E5A47` | brand / interactive (links, buttons, ticks) |
| shu | `#D8442B` | current-position line only |

Day has no `raised` (+2) step — pure white is forbidden, so there's no headroom above the paper's own lightness. The +2 step is faked with `surface` + a 1.5px `ink` rule instead.

### hotaru (night)

| Token | Value | Use |
|---|---|---|
| paper | `#131714` | page background (greenish ink-black) |
| surface | `#1A201C` | +1 step |
| raised | `#212824` | +2 step |
| ink | `#E5EBE6` | body text (moonlight) |
| ink-sub | `#9AA69F` | secondary text |
| ink-faint | `#808D86` | annotations, numbers |
| hairline | `rgba(229,235,230,.14)` | rules |
| grid | `rgba(229,235,230,.05)` | graph paper (~half of day) |
| green | `#4FC2A2` | instrument glow — the fireflies |
| shu | `#E5654C` | current-position line only |

### Status (app volume only)

| State | Day | Night | Note |
|---|---|---|---|
| success | `#2C7A4B` | `#57B98A` | distinct from brand green in saturation and role |
| warn | `#B07818` | `#D9A441` | |
| error | `#A6301C` (crimson) | `#D06A5A` | **fills are allowed** — distinguished from shu by weight and role: shu = position, crimson = failure |

Forbidden everywhere: pure `#000`/`#FFF`, filled shu, shu body text, and any shadow with an offset — a shadow that implies a light source. The one exception is the offset-zero glow of [`.tombo-glow`](#glow), which is opt-in and night-only.

## Containers

One class, `.tombo-shell`, and a four-step scale. The step is chosen by what the container holds, not by screen size.

| Token | Value | Holds |
|---|---|---|
| `--tombo-shell-reading` | `65ch` | body copy — caps the line at 621px at the body voice, 76 latin / 41 japanese characters |
| `--tombo-shell-default` | `1280px` | ordinary pages and documentation |
| `--tombo-shell-wide` | `1792px` | landing pages, card grids, dashboards |
| `--tombo-shell-gutter` | `clamp(20px, 3.25vw, 64px)` | the inline padding, fluid across the whole range |

`reading` is in `ch` because it *is* a measure — it has to track whatever type it wraps, so the same token is wider on a mono caption than on body copy. `default` and `wide` are structural, so they stay in `px` to match the px type scale: a `rem` container under a `px` type scale lengthens the line without enlarging the text.

```html
<div class="tombo-shell">                       <!-- the page's width (default) -->
<div class="tombo-shell tombo-shell--reading">  <!-- body copy -->
<div class="tombo-shell tombo-shell--wide">     <!-- LP, grids -->
<div class="tombo-shell tombo-shell--full">     <!-- backgrounds, decoration: no cap, no gutter -->
```

Markup is the whole API. `.tombo-shell` reads `--tombo-shell`; the modifiers rebind it for one element. `.tombo-gutters` reads the same variable and adds the shell's own gutter, so the margin grid meets the content edge rather than the shell's outer edge. There are no container breakpoints — `max-inline-size` plus the clamp()ed gutter cover every viewport continuously.

`reading` is the only step measured on the text rather than the box: the shell is `border-box`, so `.tombo-shell--reading` sizes itself to `65ch` **plus two gutters**, and the line inside lands on 65ch wherever the viewport affords it. Below that the shell fills the viewport and the line shrinks with it — every step is a ceiling, not a fixed width. `default` and `wide` are frame widths and mean exactly the number they state. Applying `--tombo-shell-reading` directly to a paragraph — which has no gutter — needs no compensation:

```css
.prose p { max-inline-size: var(--tombo-shell-reading); }
```

Two things to know:

- **Don't use the `padding` shorthand on a `.tombo-shell` element.** Your rule is unlayered and `.tombo-shell` lives in `@layer tombo.utilities`, so the shorthand wins and silently zeroes the gutter. Use `padding-block`.
- **Code blocks and tables are not prose.** Cap paragraphs at `--tombo-shell-reading`; let code and tables fill the column. A grid item holding a code block also needs `min-inline-size: 0`, or its longest line widens the track instead of scrolling.
- **Wrap any table that can outgrow its column** in `.tombo-table-wrap`. A data table is a reflow exception under [WCAG 2.2 SC 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), but the scroll belongs to the table, not the page. The three attributes are one set — a scroll container that cannot take focus is unreachable by keyboard, and `role="region"` needs a name:

  ```html
  <div class="tombo-table-wrap" role="region" aria-labelledby="cap" tabindex="0">
    <table class="tombo-table"> … </table>
  </div>
  <p class="tombo-dimlab" id="cap">動作要件</p>
  ```

### Overriding the page width

The page runs at `--tombo-shell-default`. When a whole page wants a different step — an LP, say — reassign `--tombo-shell` once in your own stylesheet:

```css
:root { --tombo-shell: var(--tombo-shell-wide); }
```

**`:root` and nowhere else.** Because `.tombo-gutters` sits on `<body>`, the margin grid will not follow an override made further down — set `--tombo-shell` on `<body>` and it looks like it works while the gutters silently stop meeting the content edge.

When only one container needs another step, use the modifier classes rather than reassigning anything.

The system's one sanctioned inline custom property is `--tombo-ruler-value`; `--tombo-shell` is not one. Keep it in a stylesheet.

### Migrating from `--tombo-shell-max` (removed in v0.7.0)

`--tombo-shell-max` resolved as an alias for `--tombo-shell` from 0.4 through 0.6 — but **its value changed** in 0.4, so a page that read it without migrating shifted:

| | 0.3 | 0.4 |
|---|---|---|
| below 1600px | 1100px | 1280px |
| 1600px and up | 1280px | 1280px |
| the 1600px step | yes | gone — the scale replaces it |

The alias is **removed as of v0.7.0**. A page still reading `var(--tombo-shell-max, 1100px)` now falls back to its own `1100px` default because the variable is undefined — it can look unchanged while silently diverging from the system, so migrate off it. To migrate, drop your hand-rolled container and pick the step by what it holds:

```css
/* 0.3 */
.site-shell { max-width: var(--tombo-shell-max, 1100px); margin: 0 auto; padding: 0 32px; }
```
```html
<!-- 0.4 — no CSS of your own -->
<div class="tombo-shell">                       <!-- was: the 1280px case -->
<div class="tombo-shell tombo-shell--reading">  <!-- was: the 1100px prose case -->
```

If a page was relying on 1100px specifically, that was a measure, and `--tombo-shell-reading` (65ch) is what it wanted — narrower, and it tracks the type instead of guessing at it.

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

## Signature classes (the 6 fingerprints)

Six marks repeated across every product, "played" at a different volume per context (docs quiet, app functional, LP loud). See `examples/{docs,app,lp}.html`.

| ID | Name | Classes | What it does |
|---|---|---|---|
| S-01 | Registration corners | `.tombo-corners` (+ `.tombo-corner-tr`, `.tombo-corner-bl` for all 4) | 12px corner brackets on cards, figures, hero frames |
| S-02 | Dimension line | `.tombo-dim`, `.tombo-dimlab` | hr replacement — end rules + center tick + mono caption |
| S-03 | Tick marks | `.tombo-ticks`, `.tombo-ruler` | list bullets as green ticks; ruler = 10%-grid track + green fill + shu current-value line |
| S-04 | Running numbers | `.tombo-sections`, `.tombo-sec`, `.tombo-fig` | auto-numbered headings (`02 —`) and mono figure/note captions |
| S-05 | Shu current position | `.tombo-current`, `.tombo-kicker`, `[aria-current]` | the shu marker on active tabs, TOC entries, kickers |
| S-06 | Graph paper | `.tombo-vol-lp`, `.tombo-gutters`, `.tombo-glow` | background grid — full-bleed hero on LP, margins only on docs, off on app; the glow lights the grid at night |

## Volume dial

The same six marks, turned up or down per product type:

| Signature | DOCS | APP | LP |
|---|---|---|---|
| Graph paper | margins only | none | hero full-bleed |
| Registration corners | figures only | instrument cards only | hero frame + figures |
| Dimension line | hr replacement | none | under headings + captions |
| Running numbers | headings, notes | REV label | FIG. numbers |
| Shu current position | TOC, tabs | nav, instruments | first stroke of the kicker |
| Glow (hotaru) | none | none | hero + instruments, opt-in |

## Glow

`hotaru` means firefly: at night the instruments are supposed to glow. Until 0.5 that was one hard-coded exception on the LP logo tail. It is now an opt-in class.

```html
<header class="hero tombo-vol-lp tombo-glow tombo-corners"> … </header>
<figure class="tombo-metric tombo-glow"> … </figure>
```

`.tombo-glow` lights a surface, rings it, and haloes the display type and metric values inside it. Every glow token is `light-dark(transparent, …)`, so **the class is inert by day and needs no theme selector** — it follows the OS and `data-theme` alike through `color-scheme`. Writing the rules as `[data-theme="hotaru"]` instead would miss every page that merely follows a dark OS without forcing a theme.

Two constraints are baked in, and both exist because the mockups got them wrong first:

- **The wash is a background layer, never a pseudo-element.** `.tombo-corners`, `.tombo-dim`, `.tombo-ticks`, `.tombo-ruler`, `.tombo-current` and `.tombo-kicker` all own `::before`/`::after`. A glow built on a pseudo silently eats one of their marks the first time the classes are combined — in our case the hero's bottom-right registration mark vanished and survived two rounds of review.
- **Annotation ink is lifted one step inside the glow.** A lit surface sits ~1.3 contrast points brighter, which drops `--tombo-ink-faint` to 3.93:1 on the wash and 3.68:1 on a lit panel — under the 4.5 floor that `.tombo-dimlab`, `.tombo-fig` and `.tombo-footer` all depend on. `.tombo-glow` rebinds `--tombo-ink-faint`, so every component inside follows without being touched.

The contrast gate flattens the wash onto the background before measuring, so raising `--tombo-glow-wash` past `.23` fails the build instead of the review.

## Contrast gate

28 token pairs (light + dark, on paper and on surface) are checked against WCAG 2.1 floors — 7:1 for primary body text, 4.5:1 for secondary text and interactive color, 3:1 for non-text (lines, status dots). Token values are parsed from `tombo.css` itself, so editing a token there is automatically re-checked.

```bash
python3 scripts/check_contrast.py       # runs the gate, exits 1 on any violation
python3 scripts/check_contrast.py --self-test   # verifies the luminance math itself
```

## Examples

Three volumes of the same language, side by side:

- `examples/docs.html` — documentation site
- `examples/app.html` — web application
- `examples/lp.html` — landing page
- `examples/components.html` — the component catalog: every component as a live demo + copy-paste markup, dogfooded at docs volume

Each toggles `tombo` / `hotaru` live and can be opened directly in a browser (no build step).

## Scope

Zero dependencies — one `tombo.css` file (`@layer tombo.reset, tombo.tokens, tombo.base, tombo.components, tombo.utilities`), plus an **optional** `tombo.js` for theme persistence and copy buttons (see [Behavior (tombo.js)](#behavior-tombojs)). It's progressive enhancement, not a requirement: every page renders and works with `tombo.css` alone and no JS at all, following the OS theme; `tombo.js` only makes a chosen theme remember itself across visits and adds the copy buttons. Distributed by vendoring from a tag; the repo is private, so there is no CDN and no npm package.

Deliberately out of scope for v1: Figma kit, JS components, framework wrappers (React/Vue), an icon set beyond the logo, and **npm publishing** — these are follow-ups once the CSS itself is stable.

## License

MIT — see [LICENSE](./LICENSE).
