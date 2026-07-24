# Foundations

The three voices, the two themes, and the token table everything else is built from.

## Type

Three voices, selected zero-base with the reader first (see `superpowers/specs/2026-07-21-tombo-typography-design.md`):

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

Forbidden everywhere: pure `#000`/`#FFF`, filled shu, shu body text, and any shadow with an offset — a shadow that implies a light source. The one exception is the offset-zero glow of [`.tombo-glow`](signatures.md#glow), which is opt-in and night-only.

## Japanese typography

Mixed Japanese/Latin (和欧混植) spacing is CSS-native — you don't hand-type spaces between the scripts. `tombo.css` opts into [`text-autospace: normal`](https://www.w3.org/TR/css-text-4/#text-autospace-property) on `body`, so the browser inserts the proper 八分アキ (1/8 em) at every Japanese↔Latin/number boundary. Verbatim text (`code`, `kbd`, `samp`, `pre`) is exempt.

```html
<!-- write it tight; the browser does the spacing -->
<p>Laravel 11以降に対応し、OpenAPIドキュメントを生成する。</p>
```

It's progressive enhancement: supporting engines (Chromium today) render the 八分アキ; others render tight — fully legible — and pick it up automatically as they ship `text-autospace`, with no change to your markup. A hand-typed space, if you leave one in, is respected and suppresses autospace at that boundary.
