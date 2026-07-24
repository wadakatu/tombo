# Forms

Native-first: TOMBO styles real `input` / `select` / `textarea` / `checkbox` / `radio` — no JS, no custom widgets. The look only applies inside `.tombo-field` (and `.tombo-check` / `.tombo-fieldset`), so it never hijacks an input elsewhere on the page.

A field is a hairline box with a heavier bottom rule that carries its state — the instrument's reading line: it lights **green** on focus and **crimson** on invalid. Labels use the mono instrument voice; the required marker is an ink `*` (shu stays reserved for current-position lines). Checkbox and radio use the native `accent-color`.

| Class | Role |
|---|---|
| `.tombo-field` | one field: label → control → help/error, stacked |
| `.tombo-req` | the required marker (`*`) inside a label |
| `.tombo-select` | wrapper that gives a `<select>` a themeable caret |
| `.tombo-check` | one checkbox/radio row (the `<label>` is the whole target) |
| `.tombo-fieldset` | a native `<fieldset>` reset, with a mono `<legend>` — for radio/checkbox groups |

```html
<div class="tombo-field">
  <label for="cov">COVERAGE THRESHOLD<span class="tombo-req" aria-hidden="true">*</span></label>
  <input id="cov" type="number" required
         aria-describedby="cov-help cov-err" aria-invalid="true">
  <p class="help"  id="cov-help">0–100の整数。</p>
  <p class="error" id="cov-err">0から100の数値を入力してください。</p>
</div>

<div class="tombo-field">
  <label for="fw">FRAMEWORK</label>
  <div class="tombo-select"><select id="fw"><option>Laravel</option></select></div>
</div>

<fieldset class="tombo-fieldset">
  <legend>MODE</legend>
  <label class="tombo-check"><input type="radio" name="m" checked> Strict</label>
  <label class="tombo-check"><input type="radio" name="m"> Lenient</label>
</fieldset>
```

The CSS styles the states; you own the accessible markup:

- Wire `label[for]` to `control[id]`; point `aria-describedby` at **both** the help and error ids (space-separated).
- Set `aria-invalid="true"` only when a field is in error; mark required with the native `required` attribute; show a "**\* required**" note once per form.
- Put radio/checkbox groups in `<fieldset><legend>`.
- States are pure CSS: `:focus` (baseline green) + the base `:focus-visible` ring, `:user-invalid` **and** `[aria-invalid="true"]` (baseline crimson), `:disabled` (dimmed), `:read-only` (recessed). `:user-invalid` shows validation only after the reader interacts; the `[aria-invalid]` hook covers scripted or server-side validation.

Controls are `width:100%`, so keep the form's container to a comfortable measure (a login form around `380px`, a settings form no wider than the reading measure) rather than the full page width. Deep styling of `range` / `color` / `file` / date pickers is deliberately left native.
