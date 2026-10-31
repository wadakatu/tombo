# Integration recipes

Copy a complete composition, then adapt its content and application behavior.
These recipes use existing TOMBO classes; they do not require a framework or
`tombo.js`. Load your pinned `tombo.css` before the consumer stylesheet. References:
[forms](forms.md), [layout](layout.md), and [agent workflow](ai.md).

## Settings form

This is the initial, valid state. `/settings` is an example application endpoint:
replace it with your real handler and add your framework's CSRF protection before
using the form. TOMBO does not provide a backend or save settings.

```html
<main class="tombo-shell tombo-shell--reading tombo-flow">
  <h1>検証設定</h1>
  <p>プロジェクトの検証条件を設定します。* は必須項目です。</p>
  <form class="tombo-flow" method="post" action="/settings">
    <div class="tombo-field">
      <label for="settings-project">プロジェクト名<span class="tombo-req" aria-hidden="true">*</span></label>
      <input id="settings-project" name="project" type="text" required
             value="gesso" aria-describedby="settings-project-help">
      <p class="help" id="settings-project-help">一覧で識別しやすい名前を入力してください。</p>
    </div>
    <div class="tombo-field">
      <label for="settings-coverage">カバレッジ下限 (%)<span class="tombo-req" aria-hidden="true">*</span></label>
      <input id="settings-coverage" name="coverage" type="number"
             min="0" max="100" step="1" required value="90"
             aria-describedby="settings-coverage-help">
      <p class="help" id="settings-coverage-help">0から100の整数を入力してください。</p>
    </div>
    <fieldset class="tombo-fieldset">
      <legend>検証モード</legend>
      <label class="tombo-check"><input type="radio" name="mode" value="strict" checked>厳密</label>
      <label class="tombo-check"><input type="radio" name="mode" value="lenient">許容</label>
    </fieldset>
    <button class="tombo-btn tombo-btn--primary" type="submit">設定を保存</button>
  </form>
</main>
```

On server validation failure, preserve entered values and replace the affected
field with an error state. Keep help and error IDs distinct and point to both.
Use unique IDs if this composition appears more than once on a page.

```html
<div class="tombo-field">
  <label for="settings-coverage">カバレッジ下限 (%)<span class="tombo-req" aria-hidden="true">*</span></label>
  <input id="settings-coverage" name="coverage" type="number"
         min="0" max="100" step="1" required value="101" aria-invalid="true"
         aria-describedby="settings-coverage-help settings-coverage-error">
  <p class="help" id="settings-coverage-help">0から100の整数を入力してください。</p>
  <p class="error" id="settings-coverage-error">101は上限を超えています。100以下に変更してください。</p>
</div>
```

Replace the field; do not append a second copy with the same IDs. Once the error
is resolved, remove `aria-invalid`, the error paragraph and its ID from
`aria-describedby`. For dynamic validation, manage focus/announcements in the
application. TOMBO only styles the state and does not decide when it is resolved.

Check: labels focus their input; Tab reaches each control; arrow keys change the
radio option; native validation rejects missing names and out-of-range numbers.
Application tests must separately verify saving and server-side validation.

## Data table with local scrolling

Use a named, focusable wrapper so overflow belongs to the table, not the page.
Retain native table semantics and explicit column/row headers. The minimum table
width below is a consumer decision for these columns, not a new TOMBO token.
Place this CSS in the consuming application's stylesheet. Preserve endpoint
letter case in row headings; the default table header voice uses uppercase.

```css
.endpoint-table { min-inline-size: 40rem; }
.endpoint-table th[scope="row"] { text-transform: none; }
```

```html
<section class="tombo-shell tombo-flow" aria-labelledby="endpoints-title">
  <h2 id="endpoints-title">エンドポイントの検証状況</h2>
  <p id="endpoints-help">幅が足りない場合は表の枠内を横にスクロールできます。</p>
  <div class="tombo-table-wrap" role="region" tabindex="0"
       aria-labelledby="endpoints-title" aria-describedby="endpoints-help">
    <table class="tombo-table endpoint-table">
      <thead><tr>
        <th scope="col">エンドポイント</th>
        <th scope="col">ステータス</th>
        <th scope="col">検証結果</th>
      </tr></thead>
      <tbody>
        <tr><th scope="row"><code>GET /users/{id}</code></th>
          <td>200</td><td><span class="tombo-chip" data-status="ok">検証済み</span></td></tr>
        <tr><th scope="row"><code>POST /orders</code></th>
          <td>201</td><td><span class="tombo-chip" data-status="warn">未検証</span></td></tr>
      </tbody>
    </table>
  </div>
</section>
```

Check at 390px and desktop widths: only the wrapper scrolls horizontally; keyboard
users can focus it and scroll with arrow keys. Status remains understandable
without color because each chip has text. For zero rows, render an application
message explaining how to add data instead of leaving a blank table body.

For both recipes, verify light and dark themes and preserve the visible focus
indicator. Do not interpret a passing token contrast check as a complete
accessibility audit of the consuming application.
