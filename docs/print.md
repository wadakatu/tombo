# Print

TOMBO is named after the printer's registration mark, so it prints like one.

**Print styles apply unconditionally.** A `hotaru` page prints on white paper (not a black rectangle), the dark code panel repaints to ink-on-white so it stays readable, the theme toggle and copy buttons disappear, glow and motion are dropped, and instrument blocks (`.tombo-metric`, `.tombo-callout`, `.tombo-code`, figures, table rows) request that the browser avoid page breaks inside them. The page margin is a consistent `16mm`.

**Real トンボ are opt-in.** Add `tombo-trim` to `<body>` and every printed sheet gets actual printer's marks in ink: a single 角トンボ (corner crop mark) at each of the four corners, and a センタートンボ (registration ring + crosshair) at each edge center.

```html
<body class="tombo-trim">
  <!-- your page — print it (⌘P) to see the トンボ -->
</body>
```

The marks are `--tombo-ink` — registration black, the all-plate alignment color — never shu (shu stays reserved for current-position lines). Browser print has no bleed area, so each corner gets a single crop mark at the printable-area corner — an honest homage rather than an imposition-accurate double mark with a fake bleed line.

## Verification

`npm run test:visual` includes print-media checks on the component catalog in
both themes: code switches to dark ink on white, screen-only controls disappear,
glow and transitions stop, and trim marks appear only when opted in. Switching
back to screen media restores the selected theme and controls.

[Media emulation](https://playwright.dev/docs/api/class-page#page-emulate-media)
checks computed styles, not actual printed sheets. Before shipping
print output, inspect the browser's print preview or exported PDF with real content:
long code lines and wide tables, blocks taller than a page, page breaks, and trim
marks on every sheet. `break-inside: avoid` cannot keep an oversized block on a
single page (see [CSS fragmentation rules](https://www.w3.org/TR/css-break-3/#unforced-breaks)).
Browser and printer settings (paper size, margins and backgrounds)
can change the result.
