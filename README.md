# TOMBO

A single-file CSS design system for everything wadakatu ships — OSS docs sites, web apps, LPs, portfolios. Zero JS, zero dependencies, one `<link>`.

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

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/wadakatu/tombo@main/tombo.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;900&family=IBM+Plex+Sans+JP:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

That's it — no build step, no framework. Works with any templating layer (Astro, Laravel Blade, Vue, plain HTML) since it's a single stylesheet.

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
| ink-faint | `#8B968F` | annotations, numbers |
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
| ink-faint | `#66716A` | annotations, numbers |
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

Forbidden everywhere: pure `#000`/`#FFF`, filled shu, shu body text, drop shadows, blur.

## Signature classes (the 6 fingerprints)

Six marks repeated across every product, "played" at a different volume per context (docs quiet, app functional, LP loud). See `examples/{docs,app,lp}.html`.

| ID | Name | Classes | What it does |
|---|---|---|---|
| S-01 | Registration corners | `.tombo-corners` (+ `.tombo-corner-tr`, `.tombo-corner-bl` for all 4) | 12px corner brackets on cards, figures, hero frames |
| S-02 | Dimension line | `.tombo-dim`, `.tombo-dimlab` | hr replacement — end rules + center tick + mono caption |
| S-03 | Tick marks | `.tombo-ticks`, `.tombo-ruler` | list bullets as green ticks; ruler = 10%-grid track + green fill + shu current-value line |
| S-04 | Running numbers | `.tombo-sections`, `.tombo-sec`, `.tombo-fig` | auto-numbered headings (`02 —`) and mono figure/note captions |
| S-05 | Shu current position | `.tombo-current`, `.tombo-kicker`, `[aria-current]` | the shu marker on active tabs, TOC entries, kickers |
| S-06 | Graph paper | `.tombo-vol-lp`, `.tombo-gutters` | background grid — full-bleed on LP, margins only on docs, off on app |

## Volume dial

The same six marks, turned up or down per product type:

| Signature | DOCS | APP | LP |
|---|---|---|---|
| Graph paper | margins only | none | full bleed |
| Registration corners | figures only | instrument cards only | hero frame + figures |
| Dimension line | hr replacement | none | under headings + captions |
| Running numbers | headings, notes | REV label | FIG. numbers |
| Shu current position | TOC, tabs | nav, instruments | first stroke of the kicker |
| Logo tail glow (hotaru) | none | none | hero only |

## Contrast gate

All 16 token pairs (light + dark) are checked against WCAG 2.1 floors — 7:1 for primary body text, 4.5:1 for secondary text and interactive color, 3:1 for non-text (lines, status dots).

```bash
python3 scripts/check_contrast.py       # runs the gate, exits 1 on any violation
python3 scripts/check_contrast.py --self-test   # verifies the luminance math itself
```

## Examples

Three volumes of the same language, side by side:

- `examples/docs.html` — documentation site
- `examples/app.html` — web application
- `examples/lp.html` — landing page

Each toggles `tombo` / `hotaru` live and can be opened directly in a browser (no build step).

## Scope

Pure CSS, zero JS, zero dependencies — one `tombo.css` file (`@layer tombo.reset, tombo.tokens, tombo.base, tombo.components, tombo.utilities`). Distributed via GitHub + jsDelivr CDN.

Deliberately out of scope for v1: Figma kit, JS components, framework wrappers (React/Vue), an icon set beyond the logo, and **npm publishing** — these are follow-ups once the CSS itself is stable.

## License

MIT — see [LICENSE](./LICENSE).
