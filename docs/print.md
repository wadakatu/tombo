# Print

TOMBO is named after the printer's registration mark, so it prints like one.

**Hardening is unconditional.** Any TOMBO page prints cleanly: a `hotaru` page prints on white paper (not a black rectangle), the dark code panel repaints to ink-on-white so it stays readable, the theme toggle and copy buttons disappear, glow and motion are dropped, and instrument blocks (`.tombo-metric`, `.tombo-callout`, `.tombo-code`, figures, table rows) don't split across a page break. The page margin is a consistent `16mm`.

**Real トンボ are opt-in.** Add `tombo-trim` to `<body>` and every printed sheet gets actual printer's marks in ink: a single 角トンボ (corner crop mark) at each of the four corners, and a センタートンボ (registration ring + crosshair) at each edge center.

```html
<body class="tombo-trim">
  <!-- your page — print it (⌘P) to see the トンボ -->
</body>
```

The marks are `--tombo-ink` — registration black, the all-plate alignment color — never shu (shu stays reserved for current-position lines). Browser print has no bleed area, so each corner gets a single crop mark at the printable-area corner — an honest homage rather than an imposition-accurate double mark with a fake bleed line.
