# Charts (図版)

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

`text` inside a plate is automatically mono, label-size, ink-faint (銘は等幅). The `<details class="tombo-numbers">` table is the accessible data channel; the tooltip is a visual aid (`role="presentation"`, `pointer-events: none`) that your JS toggles (`display`) and places (`transform: translate(x, y)`) — no JS, no tooltip, and the figure still reads. Interactive bars get `tabindex="0"` + `aria-label`. When the frame can scroll but holds no focusable element, treat the plate like a wide table: `role="region"` + an accessible name + `tabindex="0"`, or a keyboard user cannot scroll it. Override the minimum width in your stylesheet, not inline:

```css
.trend .tombo-plate { --tombo-plate-min: 900px; } /* one wide figure */
```
