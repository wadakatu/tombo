# Behavior (tombo.js)

`tombo.js` is optional. It's a single dependency-free file that layers three behaviors onto the CSS: theme persistence across visits, wiring for the `.tombo-themes` control, and copy buttons on code blocks. Nothing in `tombo.css` requires it — every page renders and works with the stylesheet alone.

## Loading

Vendor `tombo.js` from a tag alongside `tombo.css`, with the same sha256-pin discipline — the pinned commands live in the README's [Quick start](../README.md#quick-start).

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

## Theme control

You author the `.tombo-themes` markup; `tombo.js` reveals it and wires the clicks. Ship it `hidden`, since there's nothing to click when JS never runs:

```html
<div class="tombo-themes tombo-label" hidden>
  <button type="button" data-tombo-theme="system">system</button>
  <button type="button" data-tombo-theme="tombo">tombo</button>
  <button type="button" data-tombo-theme="hotaru">hotaru</button>
</div>
```

On load, `tombo.js` un-hides every `.tombo-themes[hidden]` block and sets `aria-pressed` on each button — `true` for whichever matches the current setting, `false` for the rest. Clicking any `[data-tombo-theme]` element calls `setTheme()` with its value: `tombo` and `hotaru` force that theme and persist it; `system` clears the stored choice and returns the page to following the OS.

Theme and copy buttons have a minimum 24 × 24 CSS pixel target without enlarging
their caption typography. Preserve this minimum when customizing their labels or
styles. Touch-heavy applications may choose larger targets in consumer styles;
24px is a floor, not a recommendation to shrink other controls. See
[WCAG target size guidance](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
for the criterion and its spacing exceptions.

## `window.Tombo`

```js
window.Tombo.setTheme('system' | 'tombo' | 'hotaru');
window.Tombo.getTheme(); // 'system' | 'tombo' | 'hotaru' — the current page setting
```

Use these instead of touching `localStorage['tombo-theme']` or `data-theme` by hand — `setTheme()` updates the stored value, `<html data-theme>`, and every `[data-tombo-theme]` button's `aria-pressed` state together in one call; changing only one of those leaves the others stale until the next click.

If storage is unavailable or a write is rejected, the selected theme still applies
to this page: `getTheme()` and the pressed buttons reflect that selection.
Persistence across reloads is best-effort; a reload reads the saved setting again.
Invalid values passed to `setTheme()` are ignored.

## Copy buttons

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

The button copies the `<pre>`'s text via the Clipboard API, reads "COPIED ✓" for 1.5s, and selects the code for manual copying, focuses the code block, and falls back to an `aria-live` announcement ("Press Ctrl or Cmd + C to copy") if the clipboard call is unavailable or is rejected.

Give every code `<pre>` inside `.tombo-code` a `tabindex="0"`, whether or not `tombo.js` is loaded — it's a horizontally-scrolling region, and one that can't take focus is unreachable by keyboard.

The code panel stays dark in both themes. Its focus indicators use
`--tombo-code-green`; the `pre` indicator is inset so the panel's clipped overflow
does not hide it. Keep the native outline enabled, including when adding syntax
highlighting or custom copy controls. These focus styles also work without JS.

## SSR (optional upgrade)

`localStorage` is the universal default, but a server-rendered consumer (Blade, Astro SSR) can go one step further: store the choice in a cookie instead of — or alongside — `localStorage`, read it on the server, and emit `data-theme` on `<html>` directly in the response HTML. That skips even the inline boot snippet, since there's nothing left to apply client-side before paint. `tombo.js` itself only ever reads `localStorage`; the cookie round-trip is something the consuming app implements on its own.
