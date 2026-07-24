# Topbar (トップバー)

Every app-volume page opens the same way: a full-width hairline rule, the brand in the display voice, mono metadata on the right shoulder. `.tombo-topbar` fixes that recipe so the first 20 lines of every product are the same markup — the brand is locked to `--tombo-text-body` (no more 14px/15px drift), the row aligns on baselines and wraps on narrow screens, and dropping `.tombo-tabs` inside needs no undo CSS (the bar absorbs `border-block-end: 0; flex: auto`).

| Class | Role |
|---|---|
| `.tombo-topbar` | the bar — full-width hairline bottom rule, `--tombo-space-16` block padding; put a `.tombo-shell` directly inside |
| `.brand` | the logo line — display voice, 700, `--tombo-text-body`, `-.015em`; a nested `<a>` inherits ink with no underline |
| `.meta` | the right shoulder — mono, label-size, ink-faint, `margin-inline-start: auto`; carries case (no uppercase transform) |
| `.tombo-topbar .tombo-tabs` | tabs drop in as-is — the bar removes their bottom rule and gives them the remaining width |

```html
<header class="tombo-topbar">
  <div class="tombo-shell">
    <span class="brand"><a href="/">SCREENBOOK</a></span>
    <nav class="tombo-tabs">
      <a href="/screens" aria-current="page">画面一覧</a>
      <a href="/deps">依存グラフ</a>
    </nav>
    <span class="meta">wadakatu@prod / REV 4.2.1</span>
  </div>
</header>
```

The rule spans the viewport because the border sits on the bar, not the shell — keep `.tombo-shell` as the direct child. Brand-only bars work too: `.meta` stays on the right shoulder via its auto margin. On narrow screens the row wraps; if a page wants `.meta` gone instead, hide it from that page's stylesheet — the component never does.
