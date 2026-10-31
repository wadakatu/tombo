# Signatures (the 6 fingerprints)

Six marks repeated across every product, "played" at a different volume per context (docs quiet, app functional, LP loud). See `../examples/{docs,app,lp}.html`.

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

## Current navigation items

For `.tombo-tabs` and `.tombo-toc`, use `aria-current="page"` on the current
link. Omit the attribute or set `aria-current="false"` on other links; an
empty value is also inactive. Non-empty values other than `false` keep the
current-position mark, following [WAI-ARIA](https://www.w3.org/TR/wai-aria/#aria-current).
Mark only one item in each navigation set as current. These are navigation
links, not a JavaScript tab widget (`role="tab"` uses `aria-selected` instead).
