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

TOMBO is distributed by vendoring — no npm package, no CDN link to go down or drift. Copy the files out of a release tag:

```bash
git -C /path/to/tombo show v0.14.1:tombo.css > public/styles/tombo.css
git -C /path/to/tombo show v0.14.1:LICENSE   > public/styles/tombo.LICENSE
git -C /path/to/tombo show v0.14.1:tombo.js  > public/scripts/tombo.js   # optional — see docs/tombo-js.md
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

`tombo.js` is optional and independent: theme persistence, the `.tombo-themes` control, and copy buttons — see [docs/tombo-js.md](docs/tombo-js.md) for the two script tags and what each one does.

For existing copies, follow the [upgrade guide](docs/upgrading.md) for behavior
changes, verification and rollback. Main may contain changes not yet in a release.

## AI-assisted integration

Start with [the agent guide](docs/ai.md) for task-specific references and integration
constraints. [llms.txt](llms.txt) is the concise index; [llms-full.txt](llms-full.txt)
is the generated full reference. Match the documentation to your vendored release.

## Documentation

The reference lives in `docs/`, one page per concern:

| Page | Covers |
|---|---|
| [Foundations](docs/foundations.md) | the three type voices, `tombo`/`hotaru` themes, the token table, Japanese typography (`text-autospace`) |
| [Layout](docs/layout.md) | `.tombo-shell` containers, the space scale, `.tombo-flow`, migrating off `--tombo-shell-max` |
| [Signatures](docs/signatures.md) | the 6 fingerprint marks, the volume dial, `.tombo-glow` |
| [Forms](docs/forms.md) | native-first fields: `.tombo-field`, `.tombo-check`, `.tombo-fieldset` |
| [Charts](docs/charts.md) | `.tombo-plate` figures and the chart norms |
| [Topbar](docs/topbar.md) | `.tombo-topbar` — how every app-volume page opens |
| [Behavior (tombo.js)](docs/tombo-js.md) | theme persistence, `window.Tombo`, copy buttons, SSR |
| [Print](docs/print.md) | unconditional print hardening and the opt-in trim marks |

The design history — every spec and plan that shaped a release — is under [docs/superpowers/](docs/superpowers/).

## Examples

Three volumes of the same language, side by side:

- `examples/docs.html` — documentation site
- `examples/app.html` — web application
- `examples/lp.html` — landing page
- `examples/components.html` — the component catalog: every component as a live demo + copy-paste markup, dogfooded at docs volume

Each toggles `tombo` / `hotaru` live and can be opened directly in a browser (no build step).

## Contrast gate

Supported token pairs (light + dark, on paper, surface, and supported raised combinations) are checked against WCAG 2.1 floors — 7:1 for primary body text, 4.5:1 for secondary text and interactive color, 3:1 for non-text (lines, status dots). Token values are parsed from `tombo.css` itself, so editing a token there is automatically re-checked.

The [contrast checker](scripts/check_contrast.py) defines the tested pairs,
including code focus and composited glow surfaces. This gate covers those
combinations; consuming pages still need checks for their own backgrounds,
overrides and content. It is not a full-page WCAG conformance test.

```bash
python3 scripts/check_contrast.py       # runs the gate, exits 1 on any violation
python3 scripts/check_contrast.py --self-test   # verifies the luminance math itself
```

## CI

Every push to `main`, every `v*` tag, and every pull request runs one gate —
the same `npm run check` you can run locally before merging:

1. **stylelint + [`use-baseline`](https://github.com/ryo-manba/stylelint-plugin-use-baseline)** (`available: "widely"`) — keeps `tombo.css` inside Baseline. Deliberately non-widely features (progressive enhancement) are listed, with justification, in `stylelint.config.mjs` — that list is the project's PE ledger.
2. **Contrast** — `scripts/check_contrast.py` (above).
3. **Size budget** — `scripts/check_size.py` (gzipped-byte ceilings and current measurements in both introduction pages).
4. **Banner / tag integrity** — `scripts/check_banner.py` asserts the version agrees across both banners and the three vendoring pins, and matches the tag on a release.
5. **JS syntax** — `node --check tombo.js`.

There's no build step and nothing is published; CI only verifies. Run the whole
gate yourself with `npm run check` (Node + Python 3 required for dev only).

After changing `tombo.css` or `tombo.js`, run
`python3 scripts/check_size.py --write` to refresh both introduction pages' byte
counts, decimal KB labels and budget ruler from the same gzip measurement.
Commit those updates with the asset change. The ordinary check is read-only and
fails on stale values or missing measurement markers; `--write` still fails if
an asset exceeds its budget. These measurements describe this checkout, while
Quick start pins continue to point to the published release.

### Visual regression

Run `npm run test:visual` (Docker required). A separate CI job uses the same
Playwright image and Linux/amd64 architecture to compare full-page screenshots
of every `examples/*.html` page in both themes at desktop 1280×900 and mobile
390×844 (touch enabled): 16 comparisons in total. Both projects also reject
horizontal page overflow; wide tables and code must scroll within their own
wrappers. The same job tests theme persistence, keyboard activation and clipboard
success/fallback behavior on the component catalog at both widths. Clipboard API
outcomes are simulated; OS clipboard permissions and screen-reader output still
need manual verification. The regular
`npm run check` remains browser-free. On failure, CI uploads the HTML report,
expected/actual/diff images and traces as the `visual-diff` artifact.

For an intentional visual change, run `npm run test:visual:update`, review the
changed images in `tests/visual/snapshots/`, then commit them with the change.
Never update baselines just to make an unexplained failure pass. A missing
baseline fails the comparison; CI does not create or accept new baselines.

The test replaces Google Fonts responses with the same font families from
locked Fontsource development dependencies (including Martian Mono's width
axis), waits for fonts, and disables animations during capture. Other external
requests fail. This stabilizes comparisons without changing the shipped pages.
Playwright and font upgrades require a reviewed baseline update. The container
version follows the exact `@playwright/test` version in package.json.

These are two fixed Chromium viewports, not a substitute for intermediate
widths, real-device interaction, accessibility or other-browser checks. Rendering is environment
dependent; use the wrapper commands above rather than native screenshot runs.
See [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)
and [the official Docker environment](https://playwright.dev/docs/docker).

## Scope

Zero dependencies — one `tombo.css` file (`@layer tombo.reset, tombo.tokens, tombo.base, tombo.components, tombo.utilities`), plus an **optional** `tombo.js` for theme persistence and copy buttons (see [docs/tombo-js.md](docs/tombo-js.md)). It's progressive enhancement, not a requirement: every page renders and works with `tombo.css` alone and no JS at all, following the OS theme; `tombo.js` only makes a chosen theme remember itself across visits and adds the copy buttons. Distributed by vendoring from a tag — there is no CDN and no npm package, deliberately.

Deliberately out of scope for v1: Figma kit, JS components, framework wrappers (React/Vue), an icon set beyond the logo, and **npm publishing** — these are follow-ups once the CSS itself is stable.

## License

MIT — see [LICENSE](./LICENSE).
