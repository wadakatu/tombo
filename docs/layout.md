# Layout

Containers, the space scale, and vertical rhythm.

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

## Overriding the page width

The page runs at `--tombo-shell-default`. When a whole page wants a different step — an LP, say — reassign `--tombo-shell` once in your own stylesheet:

```css
:root { --tombo-shell: var(--tombo-shell-wide); }
```

**`:root` and nowhere else.** Because `.tombo-gutters` sits on `<body>`, the margin grid will not follow an override made further down — set `--tombo-shell` on `<body>` and it looks like it works while the gutters silently stop meeting the content edge.

When only one container needs another step, use the modifier classes rather than reassigning anything.

The system's one sanctioned inline custom property is `--tombo-ruler-value`; `--tombo-shell` is not one. Keep it in a stylesheet.

## Migrating from `--tombo-shell-max` (removed in v0.7.0)

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

## Space scale

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

### Vertical rhythm — `.tombo-flow`

Add `.tombo-flow` to a container to space its direct children apart with a single grid cell. Override `--tombo-flow-space` on the container to change the default, or on any child to change the space that precedes it:

```css
.article { } /* markup: <div class="article tombo-flow"> */
.article { --tombo-flow-space: var(--tombo-space-16); }   /* body rhythm */
.article > h2 { --tombo-flow-space: var(--tombo-space-48); } /* more air before headings */
```

`.tombo-flow` uses `margin-block-start` on `* + *`, so the first child has no leading margin. Use it for stacked prose/content; keep `gap` for grid and flex layouts.

## Table row headers

Use `th[scope="col"]` for column headers and `th[scope="row"]` for row headers
in simple two-direction tables, following [WAI guidance](https://www.w3.org/WAI/tutorials/tables/two-headers/).
TOMBO keeps column headings in the uppercase instrument voice with the heavier
baseline. Explicit row headings inherit the table's text size, font and color,
preserve letter case, and share data-cell padding and hairline borders. Wrap
technical identifiers in `code` when they need monospace. Markup supplies the
header relationships; CSS alone cannot make ordinary cells into headers.
