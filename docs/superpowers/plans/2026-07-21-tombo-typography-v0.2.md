# TOMBO タイポグラフィ v0.2 実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 仕様書 `docs/superpowers/specs/2026-07-21-tombo-typography-design.md` の三声(Instrument Sans / M PLUS 2 / Martian Mono)とタイプスケール 10 段を tombo.css v0.2.0 として実装し、examples・カタログ・ワードマーク・README を追随させる。

**Architecture:** tombo.css の tokens 層に書体・スケールの対トークンを追加し、base / components / utilities 層の生 font-size を全てトークン参照に書き換える(「その場サイズの新設は禁止」を機械検査可能にする)。色トークンは無変更なのでコントラストゲートは 28/28 のまま。ワードマークは fonttools パイプラインで Instrument Sans 700 に再アウトライン。

**Tech Stack:** Pure CSS(cascade layers / light-dark / variable fonts)、Python(fonttools、コントラストゲート)、chrome-devtools MCP(視覚検証)。

## Global Constraints

- 色トークンは一切変更しない。各タスク完了時に `python3 scripts/check_contrast.py` が exit 0(28/28 PASS)であること
- tombo.css 内の `font-size:` は必ず `var(--tombo-text-*)` を参照(生 px 禁止)。例外(2026-07-21 実装中修正): 装飾 pseudo-element の**比例サイズ(em)は許容** — `.tombo-sec::before` の `.72em` の 1 箇所のみ(`.tombo-chip::before` は当初 `.76em` 化したが、● グリフのベースラインずれ(ユーザー指摘)により font-size を持たない幾何学的な円に置換済み)。検査: `grep -n "font-size:" tombo.css | grep -vE "var\(--tombo-text-|font-size: ?\.[0-9]+em"` が空
- `font-weight: 900` は全廃(Instrument Sans に 900 は存在しない)。検査: `grep -rn "font-weight: 900\|font-weight:900" tombo.css examples/` が空
- 和文に負の字間を当てない。`letter-spacing: -.015em` は `.tombo-display`(欧文専用)のみ
- 本文ウェイトは `var(--tombo-w-body)`(= 450)
- コードは Martian Mono 幅軸 87.5%(`font-stretch: 87.5%`)
- フォント読み込みは consumer の `<link>` のみ(css 内 @import 禁止)
- 最小 font-size は 10.5px(9.5px 等の既存ローカルサイズは 10.5px 以上へ昇格)
- ブラウザ検証は昼夜両テーマ必須。`data-theme` 切替後 300ms 以上待ってから計測・撮影(transition 150ms のため)
- コミットは英語 Conventional Commits。`Co-Authored-By` 行は付けない

新旧フォント `<link>`(examples 4 枚 + components.html + README で同一置換):

```html
<!-- OLD -->
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;900&family=IBM+Plex+Sans+JP:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<!-- NEW(HTTP 200 検証済み) -->
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@600;700&family=M+PLUS+2:wght@450;500;700&family=Martian+Mono:wdth,wght@75..112.5,400..600&display=swap" rel="stylesheet">
```

---

### Task 1: tombo.css — 書体・スケールトークンと base 層

**Files:**
- Modify: `tombo.css`(バナー、tokens 層 type 節、base 層)

**Interfaces:**
- Produces: `--tombo-font-{display,body,mono}` `--tombo-w-body` `--tombo-text-{label,note,code,ui,body,h3,h2,h1,metric,display}` `--tombo-lh-{label,note,code,ui,body,h3,h2,h1,metric}` — Task 2 以降の全参照元

- [ ] **Step 1: バナーを v0.2.0 に**

OLD → NEW(1 行目):

```css
/*! TOMBO v0.1.0 — wadakatu design system. MIT. https://github.com/wadakatu/tombo */
```

```css
/*! TOMBO v0.2.0 — wadakatu design system. MIT. https://github.com/wadakatu/tombo */
```

- [ ] **Step 2: tokens 層の type 節を差し替え**

OLD:

```css
    /* type */
    --tombo-font-display: "Archivo", "IBM Plex Sans JP", system-ui, sans-serif;
    --tombo-font-body: "IBM Plex Sans JP", system-ui, sans-serif;
    --tombo-font-mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, monospace;
```

NEW:

```css
    /* type — three voices (spec 2026-07-21) */
    --tombo-font-display: "Instrument Sans", "M PLUS 2", system-ui, sans-serif; /* Latin display only */
    --tombo-font-body: "M PLUS 2", system-ui, sans-serif;
    --tombo-font-mono: "Martian Mono", ui-monospace, SFMono-Regular, monospace;
    --tombo-w-body: 450; /* variable weight — 400 thins out on hotaru */
    /* type scale — no ad-hoc sizes: every font-size below references these */
    --tombo-text-label: 10.5px;  --tombo-lh-label: 18px;
    --tombo-text-note: 12px;     --tombo-lh-note: 18px;
    --tombo-text-code: 12px;     --tombo-lh-code: 22px;
    --tombo-text-ui: 13px;       --tombo-lh-ui: 24px;
    --tombo-text-body: 15px;     --tombo-lh-body: 30px;
    --tombo-text-h3: 19px;       --tombo-lh-h3: 30px;
    --tombo-text-h2: 23px;       --tombo-lh-h2: 36px;
    --tombo-text-h1: 29px;       --tombo-lh-h1: 42px;
    --tombo-text-metric: 29px;   --tombo-lh-metric: 36px;
    --tombo-text-display: clamp(44px, 6vw, 64px);
```

- [ ] **Step 3: base 層の body / 見出し / display を書き換え**

OLD:

```css
  body {
    background: var(--tombo-paper);
    color: var(--tombo-ink);
    font-size: 14px;
    line-height: 2;
    transition: background var(--tombo-dur) var(--tombo-ease), color var(--tombo-dur) var(--tombo-ease);
  }
  h1, h2, h3, h4 { line-height: 1.3; font-weight: 700; }
  h1 { font-size: 28px; } h2 { font-size: 20px; } h3 { font-size: 15px; }
  .tombo-display { font-family: var(--tombo-font-display); font-weight: 900;
    font-size: clamp(44px, 6vw, 64px); line-height: 1.1; letter-spacing: -.015em; }
```

NEW:

```css
  body {
    background: var(--tombo-paper);
    color: var(--tombo-ink);
    font-size: var(--tombo-text-body);
    font-weight: var(--tombo-w-body);
    line-height: 2; /* = 30px at body size; unitless so larger text inherits safely */
    transition: background var(--tombo-dur) var(--tombo-ease), color var(--tombo-dur) var(--tombo-ease);
  }
  h1, h2, h3, h4 { font-weight: 700; }
  h1 { font-size: var(--tombo-text-h1); line-height: var(--tombo-lh-h1); }
  h2 { font-size: var(--tombo-text-h2); line-height: var(--tombo-lh-h2); }
  h3 { font-size: var(--tombo-text-h3); line-height: var(--tombo-lh-h3); }
  h4 { line-height: 1.3; }
  .tombo-display { font-family: var(--tombo-font-display); font-weight: 700; /* Instrument Sans has no 900 */
    font-size: var(--tombo-text-display); line-height: 1.1; letter-spacing: -.015em; }
```

- [ ] **Step 4: ゲートと部分検査**

Run: `python3 scripts/check_contrast.py > /dev/null; echo exit=$?`
Expected: `exit=0`

Run: `grep -c "Archivo\|IBM Plex" tombo.css`
Expected: `0`

- [ ] **Step 5: Commit**

```bash
git add tombo.css
git commit -m "feat: add three-voice font tokens and 10-step type scale (v0.2.0 base)"
```

### Task 2: tombo.css — components / utilities 層をスケール参照へ

**Files:**
- Modify: `tombo.css`(utilities 層 .tombo-label、components 層の全サイズ)

**Interfaces:**
- Consumes: Task 1 の全トークン

以下、各 OLD → NEW を正確に適用する(すべて現 v0.2.0 ファイル内で一意)。

- [ ] **Step 1: utilities 層 .tombo-label**

OLD:

```css
  .tombo-label {
    font-family: var(--tombo-font-mono); font-size: 11px;
    letter-spacing: .14em; text-transform: uppercase; color: var(--tombo-ink-sub);
  }
```

NEW:

```css
  .tombo-label {
    font-family: var(--tombo-font-mono); font-size: var(--tombo-text-label);
    line-height: var(--tombo-lh-label); font-weight: 500;
    letter-spacing: .14em; text-transform: uppercase; color: var(--tombo-ink-sub);
  }
```

- [ ] **Step 2: 寸法線ラベルと fig(note 段へ)**

OLD:

```css
  .tombo-dimlab { font-family: var(--tombo-font-mono); font-size: 10.5px; letter-spacing: .08em; color: var(--tombo-ink-faint); margin-top: 7px; }
```

NEW:

```css
  .tombo-dimlab { font-family: var(--tombo-font-mono); font-size: var(--tombo-text-note); line-height: var(--tombo-lh-note); letter-spacing: .08em; color: var(--tombo-ink-faint); margin-top: 7px; }
```

OLD:

```css
  .tombo-fig { font-family: var(--tombo-font-mono); font-size: 10px; letter-spacing: .1em; color: var(--tombo-ink-faint); text-transform: uppercase; }
```

NEW:

```css
  .tombo-fig { font-family: var(--tombo-font-mono); font-size: var(--tombo-text-note); line-height: var(--tombo-lh-note); letter-spacing: .08em; color: var(--tombo-ink-faint); text-transform: uppercase; }
```

- [ ] **Step 3: kicker(label 段・.16em 維持)**

OLD:

```css
  .tombo-kicker { font-family: var(--tombo-font-mono); font-size: 11px; letter-spacing: .16em; color: var(--tombo-green); text-transform: uppercase; }
```

NEW:

```css
  .tombo-kicker { font-family: var(--tombo-font-mono); font-size: var(--tombo-text-label); line-height: var(--tombo-lh-label); font-weight: 500; letter-spacing: .16em; color: var(--tombo-green); text-transform: uppercase; }
```

- [ ] **Step 4: ボタン・タブ・目次(ui 段)**

OLD → NEW(それぞれ該当部分のみ):

```css
  .tombo-btn { display: inline-block; padding: 12px 26px; font-size: 13.5px; font-family: var(--tombo-font-body);
```

```css
  .tombo-btn { display: inline-block; padding: 12px 26px; font-size: var(--tombo-text-ui); font-family: var(--tombo-font-body);
```

```css
  .tombo-tabs > * { padding: 6px 2px 9px; color: var(--tombo-ink-sub); text-decoration: none; position: relative; font-size: 13px; }
```

```css
  .tombo-tabs > * { padding: 6px 2px 9px; color: var(--tombo-ink-sub); text-decoration: none; position: relative; font-size: var(--tombo-text-ui); }
```

```css
  .tombo-toc { font-size: 12.5px; }
```

```css
  .tombo-toc { font-size: var(--tombo-text-ui); }
```

- [ ] **Step 5: コード(caption = label 段 / pre = code 段 + 幅軸 87.5%)**

OLD:

```css
  .tombo-code > figcaption { display: flex; justify-content: space-between; font-family: var(--tombo-font-mono);
    font-size: 10px; letter-spacing: .1em; text-transform: uppercase; color: var(--tombo-code-faint);
    padding: 8px 14px; border-bottom: 1px solid var(--tombo-code-hairline); }
  .tombo-code pre { font-size: 12px; line-height: 1.9; padding: 14px 18px; overflow-x: auto; }
```

NEW:

```css
  .tombo-code > figcaption { display: flex; justify-content: space-between; font-family: var(--tombo-font-mono);
    font-size: var(--tombo-text-label); font-weight: 500; letter-spacing: .1em; text-transform: uppercase; color: var(--tombo-code-faint);
    padding: 8px 14px; border-bottom: 1px solid var(--tombo-code-hairline); }
  .tombo-code pre { font-size: var(--tombo-text-code); line-height: var(--tombo-lh-code); font-stretch: 87.5%; padding: 14px 18px; overflow-x: auto; }
```

- [ ] **Step 6: コールアウト・テーブル・チップ(ui / label 段)**

OLD → NEW:

```css
  .tombo-callout { border: 1px solid var(--tombo-hairline); border-left: 2px solid var(--tombo-shu);
    padding: 12px 16px; font-size: 12.5px; color: var(--tombo-ink-sub); }
```

```css
  .tombo-callout { border: 1px solid var(--tombo-hairline); border-left: 2px solid var(--tombo-shu);
    padding: 12px 16px; font-size: var(--tombo-text-ui); line-height: var(--tombo-lh-ui); color: var(--tombo-ink-sub); }
```

```css
  .tombo-callout > b:first-child { font-family: var(--tombo-font-mono); font-weight: 500; font-size: 10px;
```

```css
  .tombo-callout > b:first-child { font-family: var(--tombo-font-mono); font-weight: 500; font-size: var(--tombo-text-label);
```

```css
  .tombo-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
```

```css
  .tombo-table { width: 100%; border-collapse: collapse; font-size: var(--tombo-text-ui); }
```

```css
  .tombo-table th { font-family: var(--tombo-font-mono); font-size: 10px; letter-spacing: .12em;
```

```css
  .tombo-table th { font-family: var(--tombo-font-mono); font-size: var(--tombo-text-label); letter-spacing: .12em;
```

```css
  .tombo-chip { font-family: var(--tombo-font-mono); font-size: 10px; letter-spacing: .08em;
```

```css
  .tombo-chip { font-family: var(--tombo-font-mono); font-size: var(--tombo-text-label); font-weight: 500; letter-spacing: .08em;
```

- [ ] **Step 7: メトリクス・フッター**

OLD → NEW:

```css
  .tombo-metric > .k { font-family: var(--tombo-font-mono); font-size: 10px; letter-spacing: .14em;
```

```css
  .tombo-metric > .k { font-family: var(--tombo-font-mono); font-size: var(--tombo-text-label); font-weight: 500; letter-spacing: .14em;
```

```css
  .tombo-metric > .v { font-family: var(--tombo-font-mono); font-size: 30px; font-weight: 600; margin: 8px 0 12px; }
```

```css
  .tombo-metric > .v { font-family: var(--tombo-font-mono); font-size: var(--tombo-text-metric); line-height: var(--tombo-lh-metric); font-weight: 600; margin: 8px 0 12px; }
```

OLD(フッターは刻印なので weight 400 のまま — 意図的な例外):

```css
  .tombo-footer { border-top: 1px solid var(--tombo-hairline); padding: 22px 0 46px;
    font-family: var(--tombo-font-mono); font-size: 10px; letter-spacing: .12em; color: var(--tombo-ink-faint); line-height: 1.9; }
```

NEW:

```css
  .tombo-footer { border-top: 1px solid var(--tombo-hairline); padding: 22px 0 46px;
    font-family: var(--tombo-font-mono); font-size: var(--tombo-text-label); letter-spacing: .12em; color: var(--tombo-ink-faint); line-height: 1.9; }
```

- [ ] **Step 7b(実装中修正 2026-07-21): 装飾 pseudo-element の生 px を em 化**

計画の OLD→NEW に含まれない font-size が 2 箇所ある(実装者検出)。制約本文「生 px 禁止」の意図に合わせ:

- `.tombo-chip::before` の `font-size: 8px` → `font-size: .76em`(チップ本体 10.5px 比 ≈ 8px、視覚同寸)
- `.tombo-sec::before` の `font-size: .72em` は見出しに対する比例装飾(カウンター)なのでそのまま維持

- [ ] **Step 8: 機械検査 + ゲート**

Run: `grep -n "font-size:" tombo.css | grep -vE "var\(--tombo-text-|font-size: ?\.[0-9]+em"`
Expected: 出力なし(全 font-size がトークン参照。em 比例装飾 2 箇所のみ許容)

Run: `grep -n "font-weight: 900\|font-weight:900" tombo.css`
Expected: 出力なし

Run: `python3 scripts/check_contrast.py > /dev/null; echo exit=$?`
Expected: `exit=0`

- [ ] **Step 9: Commit**

```bash
git add tombo.css
git commit -m "feat: reference type scale tokens across all components"
```

### Task 3: examples 3 枚(docs / app / lp)の追随

**Files:**
- Modify: `examples/docs.html` `examples/app.html` `examples/lp.html`

**Interfaces:**
- Consumes: Task 1–2 のトークン、Global Constraints の新旧 `<link>`

- [ ] **Step 1: 3 ファイルのフォント `<link>` を差し替え**(Global Constraints の OLD → NEW、各ファイル 1 箇所)

- [ ] **Step 2: docs.html ローカルスタイル**

OLD → NEW:

```css
  .brand { font-family: var(--tombo-font-display); font-weight: 900; font-size: 16px; }
```

```css
  .brand { font-family: var(--tombo-font-display); font-weight: 700; font-size: 16px; }
```

```css
  .brand small { display: block; font-family: var(--tombo-font-mono); font-weight: 400; font-size: 9.5px; color: var(--tombo-ink-faint); letter-spacing: .12em; margin-top: 4px; }
```

```css
  .brand small { display: block; font-family: var(--tombo-font-mono); font-weight: 400; font-size: var(--tombo-text-label); color: var(--tombo-ink-faint); letter-spacing: .12em; margin-top: 4px; }
```

```css
  main p { font-size: 13.5px; line-height: 2.15; color: var(--tombo-ink-sub); margin-top: 14px; max-width: 62ch; }
```

```css
  main p { font-size: var(--tombo-text-body); line-height: var(--tombo-lh-body); color: var(--tombo-ink-sub); margin-top: 14px; max-width: 62ch; }
```

- [ ] **Step 3: app.html ローカルスタイル**

OLD → NEW:

```css
  .logo { font-family: var(--tombo-font-display); font-weight: 900; font-size: 14px; }
```

```css
  .logo { font-family: var(--tombo-font-display); font-weight: 700; font-size: 14px; }
```

```css
  .me { margin-left: auto; font-size: 10.5px; color: var(--tombo-ink-faint); }
```

```css
  .me { margin-left: auto; font-size: var(--tombo-text-label); color: var(--tombo-ink-faint); }
```

```css
  .tombo-metric .v small { font-size: 12px; color: var(--tombo-ink-faint); font-weight: 400; }
```

```css
  .tombo-metric .v small { font-size: var(--tombo-text-note); color: var(--tombo-ink-faint); font-weight: 400; }
```

- [ ] **Step 4: lp.html ローカルスタイル**

OLD → NEW:

```css
  .tagline { margin-top: 18px; font-size: 14.5px; line-height: 2.05; color: var(--tombo-ink-sub); max-width: 50ch; }
```

```css
  .tagline { margin-top: 18px; font-size: var(--tombo-text-body); line-height: var(--tombo-lh-body); color: var(--tombo-ink-sub); max-width: 50ch; }
```

```css
    font-size: 10.5px; padding: 8px 0; border-bottom: 1px solid var(--tombo-hairline); color: var(--tombo-ink-sub); }
```

```css
    font-size: var(--tombo-text-label); padding: 8px 0; border-bottom: 1px solid var(--tombo-hairline); color: var(--tombo-ink-sub); }
```

```css
  .inst .v small { font-size: 14px; color: var(--tombo-ink-faint); font-weight: 400; }
```

```css
  .inst .v small { font-size: var(--tombo-text-ui); color: var(--tombo-ink-faint); font-weight: 400; }
```

```css
  .fcard p { margin-top: 10px; font-size: 12.5px; line-height: 1.95; color: var(--tombo-ink-sub); }
```

```css
  .fcard p { margin-top: 10px; font-size: var(--tombo-text-ui); line-height: var(--tombo-lh-ui); color: var(--tombo-ink-sub); }
```

注: `.hero h1 small` の `clamp(18px, 2vw, 22px)` は display の従属要素なのでローカル値のまま維持(変更しない)。

- [ ] **Step 5: 機械検査**

Run: `grep -rn "font-weight: 900\|font-weight:900" examples/docs.html examples/app.html examples/lp.html`
Expected: 出力なし

Run: `grep -rln "Archivo\|IBM+Plex" examples/docs.html examples/app.html examples/lp.html`
Expected: 出力なし

- [ ] **Step 6: ブラウザ検証(昼夜)**

chrome-devtools で `file:///Users/wadakatu/tombo/examples/docs.html` `app.html` `lp.html` を順に開き、各ページで:

```js
async () => {
  const r = {};
  for (const t of ['tombo', 'hotaru']) {
    document.documentElement.dataset.theme = t;
    await new Promise(res => setTimeout(res, 350));
    const p = document.querySelector('main p, .tagline, .tombo-table td');
    r[t] = { body: getComputedStyle(document.body).fontFamily.split(',')[0],
             weight: getComputedStyle(document.body).fontWeight,
             sample: p ? getComputedStyle(p).fontSize : null };
  }
  document.documentElement.removeAttribute('data-theme');
  return r;
}
```

Expected: body の第一書体が `"M PLUS 2"`、fontWeight `450`。両テーマでスクリーンショットを撮り、レイアウト破綻(折返し・はみ出し・重なり)がないこと。Martian Mono 化で銘が横に伸びるため、特に lp.html の `.inst .row` と app.html のテーブルの折返しを目視確認。破綻があれば文言を短縮せず、該当ローカルスタイルの `gap`/`min-width` 調整で対処し、対処内容を報告に記す。

- [ ] **Step 7: Commit**

```bash
git add examples/docs.html examples/app.html examples/lp.html
git commit -m "feat: apply v0.2 typography to volume examples"
```

### Task 4: components.html カタログの追随

**Files:**
- Modify: `examples/components.html`

**Interfaces:**
- Consumes: Task 1–2 のトークン、Global Constraints の新旧 `<link>`

- [ ] **Step 1: フォント `<link>` 差し替え**(Global Constraints の OLD → NEW)

- [ ] **Step 2: ローカルスタイル**

OLD → NEW:

```css
  .brand { font-family: var(--tombo-font-display); font-weight: 900; font-size: 16px; }
```

```css
  .brand { font-family: var(--tombo-font-display); font-weight: 700; font-size: 16px; }
```

```css
  .brand small { display: block; font-family: var(--tombo-font-mono); font-weight: 400; font-size: 9.5px; color: var(--tombo-ink-faint); letter-spacing: .12em; margin-top: 4px; }
```

```css
  .brand small { display: block; font-family: var(--tombo-font-mono); font-weight: 400; font-size: var(--tombo-text-label); color: var(--tombo-ink-faint); letter-spacing: .12em; margin-top: 4px; }
```

```css
  main > p.lead { font-size: 13.5px; line-height: 2.15; color: var(--tombo-ink-sub); margin-top: 14px; max-width: 62ch; }
```

```css
  main > p.lead { font-size: var(--tombo-text-body); line-height: var(--tombo-lh-body); color: var(--tombo-ink-sub); margin-top: 14px; max-width: 62ch; }
```

```css
  section .note { font-size: 13px; line-height: 2.1; color: var(--tombo-ink-sub); margin-top: 10px; max-width: 62ch; }
```

```css
  section .note { font-size: var(--tombo-text-ui); line-height: var(--tombo-lh-ui); color: var(--tombo-ink-sub); margin-top: 10px; max-width: 62ch; }
```

- [ ] **Step 3: §14 ユーティリティ節の文言を新書体に更新**

OLD:

```html
        <p class="note">.tombo-display は Archivo 900 の見出し、.tombo-label は等幅の大文字銘、.tombo-mono は等幅化。方眼は音量クラスで敷く — .tombo-vol-lp が全面、.tombo-gutters が余白のみ(このページが実演)、app は敷かない。</p>
```

NEW:

```html
        <p class="note">.tombo-display は Instrument Sans 700 の欧文題字(和文が混ざる見出しは h1/h2 を使う)、.tombo-label は等幅の大文字銘、.tombo-mono は等幅化。方眼は音量クラスで敷く — .tombo-vol-lp がヒーロー全面、.tombo-gutters が余白のみ(このページが実演)、app は敷かない。</p>
```

OLD:

```html
          <p class="tombo-label" style="margin-top:10px">MEASURED / SET IN PLEX MONO</p>
```

NEW:

```html
          <p class="tombo-label" style="margin-top:10px">MEASURED / SET IN MARTIAN MONO</p>
```

- [ ] **Step 4: 機械検査**

Run: `grep -n "font-weight: 900\|Archivo\|PLEX MONO\|IBM+Plex" examples/components.html`
Expected: 出力なし

- [ ] **Step 5: ブラウザ検証(昼夜・全 14 セクション)**

chrome-devtools で `file:///Users/wadakatu/tombo/examples/components.html` を開き、Task 3 Step 6 と同じ手順で両テーマの fullPage スクリーンショットを取得。確認観点: ①全セクションでフォント適用(見出し 700 / 本文 450 / 銘 Martian)②コードブロックの幅軸 87.5% 適用(`getComputedStyle(document.querySelector('.tombo-code pre')).fontStretch` = `87.5%`)③hotaru で本文が痩せていないこと(目視)④銘の折返し破綻なし。

- [ ] **Step 6: Commit**

```bash
git add examples/components.html
git commit -m "feat: apply v0.2 typography to component catalog"
```

### Task 5: ワードマーク再アウトライン(Instrument Sans 700)

**Files:**
- Create(スクラッチパッド): `/private/tmp/claude-501/-Users-wadakatu/d33749c8-ad5b-444e-8f40-d965c5fee1a9/scratchpad/outline_wordmark_v2.py`
- Modify: `assets/logo/tombo-wordmark.svg` `assets/logo/tombo-wordmark-dark.svg`

**Interfaces:**
- Consumes: なし(独立タスク)。既存 venv `/private/tmp/claude-501/-Users-wadakatu/d33749c8-ad5b-444e-8f40-d965c5fee1a9/scratchpad/venv`(fonttools 導入済み。無ければ `python3 -m venv venv && venv/bin/pip install fonttools`)

- [ ] **Step 1: Instrument Sans variable TTF を取得**

```bash
cd /private/tmp/claude-501/-Users-wadakatu/d33749c8-ad5b-444e-8f40-d965c5fee1a9/scratchpad
curl -sL -o instrument-sans.ttf "https://github.com/google/fonts/raw/main/ofl/instrumentsans/InstrumentSans%5Bwdth%2Cwght%5D.ttf"
file instrument-sans.ttf
```

Expected: `TrueType Font data`(HTML が返った場合は URL を `gh api repos/google/fonts/contents/ofl/instrumentsans` で実ファイル名を確認して再取得)

- [ ] **Step 2: 生成スクリプトを作成**

```python
#!/usr/bin/env python3
"""Outline 'TOMBO' in Instrument Sans 700 and rebuild the wordmark (v0.2)."""
from fontTools import ttLib
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

SRC = "/private/tmp/claude-501/-Users-wadakatu/d33749c8-ad5b-444e-8f40-d965c5fee1a9/scratchpad/instrument-sans.ttf"
WORD = "TOMBO"
TRACKING_EM = -0.015  # spec: display tracking, Latin only

font = ttLib.TTFont(SRC)
instantiateVariableFont(font, {"wght": 700, "wdth": 100}, inplace=True)
upem = font["head"].unitsPerEm
cmap = font.getBestCmap()
glyph_set = font.getGlyphSet()
hmtx = font["hmtx"]

x = 0.0
paths = []
for ch in WORD:
    gname = cmap[ord(ch)]
    pen = SVGPathPen(glyph_set)
    tpen = TransformPen(pen, Transform().translate(x, 0))
    glyph_set[gname].draw(tpen)
    paths.append(pen.getCommands())
    x += hmtx[gname][0] + TRACKING_EM * upem
total_advance = x - TRACKING_EM * upem

try:
    cap = font["OS/2"].sCapHeight or 700
except Exception:
    cap = 700

CAP_TARGET = 26.0
scale = CAP_TARGET / cap
word_w = total_advance * scale
vx = 4.0
baseline_y = 30
vb_w = word_w + 8
vb_h = 56

d = " ".join(paths)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w:.1f} {vb_h}" style="color:#1A211D">
  <title>TOMBO — wordmark (Instrument Sans 700, outlined). The name, measured.</title>
  <g transform="translate({vx:.2f} {baseline_y}) scale({scale:.6f} {-scale:.6f})">
    <path d="{d}" fill="currentColor"/>
  </g>
  <line x1="{vx:.1f}" y1="40" x2="{vx:.1f}" y2="48" stroke="currentColor" stroke-width="2"/>
  <line x1="{vx + word_w:.1f}" y1="40" x2="{vx + word_w:.1f}" y2="48" stroke="currentColor" stroke-width="2"/>
  <line x1="{vx:.1f}" y1="44" x2="{vx + word_w:.1f}" y2="44" stroke="currentColor" stroke-width="2"/>
  <line x1="{vx + word_w * 0.62:.1f}" y1="38" x2="{vx + word_w * 0.62:.1f}" y2="50" stroke="#D8442B" stroke-width="2.4"/>
</svg>
'''
out = "/Users/wadakatu/tombo/assets/logo/tombo-wordmark.svg"
with open(out, "w") as f:
    f.write(svg)
print(f"wrote {out}  word_w={word_w:.1f} cap={cap} upem={upem}")
```

- [ ] **Step 3: 生成 + 夜変種**

```bash
cd /private/tmp/claude-501/-Users-wadakatu/d33749c8-ad5b-444e-8f40-d965c5fee1a9/scratchpad
venv/bin/python outline_wordmark_v2.py
cd /Users/wadakatu/tombo
sed -e 's/#1A211D/#E5EBE6/g' -e 's/#D8442B/#E5654C/g' assets/logo/tombo-wordmark.svg > assets/logo/tombo-wordmark-dark.svg
grep -o "#[0-9A-F]\{6\}" assets/logo/tombo-wordmark.svg | sort -u
grep -o "#[0-9A-F]\{6\}" assets/logo/tombo-wordmark-dark.svg | sort -u
```

Expected: 昼 = `#1A211D` `#D8442B` のみ / 夜 = `#E5654C` `#E5EBE6` のみ

- [ ] **Step 4: ブラウザでレターフォーム検証**

chrome-devtools で `file:///Users/wadakatu/tombo/assets/logo/tombo-wordmark.svg` を開きスクリーンショット。確認: TOMBO の 5 文字が Instrument Sans 700 の字形で欠けなく描画され、下部に寸法線 + 62% 位置の朱目盛があること。

- [ ] **Step 5: Commit**

```bash
git add assets/logo/tombo-wordmark.svg assets/logo/tombo-wordmark-dark.svg
git commit -m "feat: re-outline wordmark in Instrument Sans 700"
```

### Task 6: README・メイン spec §6・タグ v0.2.0

**Files:**
- Modify: `README.md` `docs/superpowers/specs/2026-07-20-tombo-design-system-design.md`

**Interfaces:**
- Consumes: Global Constraints の新 `<link>`

- [ ] **Step 1: README Quick start のフォント `<link>` 差し替え**(Global Constraints の OLD → NEW、1 箇所)

- [ ] **Step 2: README に Type 節を追加**(`## Themes` の直前に挿入)

```markdown
## Type

Three voices, selected zero-base with the reader first (see `docs/superpowers/specs/2026-07-21-tombo-typography-design.md`):

| Voice | Face | Role |
|---|---|---|
| DISPLAY | Instrument Sans 700 | Latin display headings only (tracking -.015em never touches Japanese) |
| BODY | M PLUS 2 at weight 450 | Japanese body, UI copy, Japanese headings |
| INSTRUMENT | Martian Mono | labels, numbers, indices, code (code condenses to width 87.5%) |

A 10-step type scale (`--tombo-text-*` / `--tombo-lh-*`, body 15px/30px) replaces all ad-hoc sizes — components may only reference scale tokens.

```

- [ ] **Step 3: メイン spec §6 を全面改稿**

OLD(§6 全体):

```markdown
## 6. タイポグラフィ

| 役割 | 書体 | 用途 |
|---|---|---|
| DISPLAY | Archivo 700/900 | 見出し(欧文)・ロゴ・大数字。字間 -.015em |
| BODY | IBM Plex Sans JP 400/500/700 | 本文・UI・和文見出し。字間はいじらない |
| INSTRUMENT | IBM Plex Mono 400/500/600 | 数値・ラベル・コード・索引。ラベルは大文字 + 字間 .12-.16em |

- スケール: display 44-64 / h1 28 / h2 20 / h3 15 / body 14 / small 12.5 / label 10-11(mono)
- 本文の行間 1.9-2.1。読み手の速度を邪魔しないことが本文の唯一の仕事で、個性は計器(mono とトンボ)が担当する
- 配信: Google Fonts。フォールバック: `Archivo, 'IBM Plex Sans JP', system-ui, sans-serif` / `'IBM Plex Mono', ui-monospace, monospace`
```

NEW:

```markdown
## 6. タイポグラフィ(v0.2 — 全書体ゼロベース改稿。詳細: specs/2026-07-21-tombo-typography-design.md)

| 役割 | 書体 | 用途 |
|---|---|---|
| DISPLAY | Instrument Sans 700(サブ 600。900 は存在しない) | 欧文題字専用。字間 -.015em はこの声だけ |
| BODY | M PLUS 2 — 本文 450 / 強調 500 / 太字・和文見出し 700 | 和文本文・UI・和文見出し。和文に負の字間を当てない |
| INSTRUMENT | Martian Mono 400–600(コードは幅軸 87.5%) | 数値・ラベル・コード・索引。ラベルは大文字 + 字間 .12-.16em |

タイプスケール(対トークン `--tombo-text-*` / `--tombo-lh-*`。その場サイズの新設は禁止):

| 段 | size / lh | 書体 | 用途 |
|---|---|---|---|
| label | 10.5 / 18 | mono 500 caps | 計器銘・チップ・フッター(フッターのみ 400 の刻印例外) |
| note | 12 / 18 | mono 400 | 寸法ラベル・fig・注記 |
| code | 12 / 22 | mono 400 幅 87.5% | コードブロック |
| ui | 13 / 24 | body | 表・コールアウト・タブ・ボタン |
| body | 15 / 30 | body 450 | 本文 |
| h3 / h2 / h1 | 19/30 · 23/36 · 29/42 | body 700 | 見出し |
| metric | 29 / 36 | mono 600 | 計器の大数字 |
| display | clamp(44–64) / 1.1 | display 700 | 欧文題字 |

- 和欧混植: 本文中の欧文・数字は M PLUS 2 自身のラテンで組む。数値の並ぶ場所は掟 2 により Martian Mono
- 配信: Google Fonts(M PLUS 2 は unicode-range 分割)。フォールバック: `'Instrument Sans', 'M PLUS 2', system-ui, sans-serif` / `'M PLUS 2', system-ui, sans-serif` / `'Martian Mono', ui-monospace, monospace`
```

- [ ] **Step 4: 整合検査**

Run: `grep -rn "Archivo" README.md docs/superpowers/specs/2026-07-20-tombo-design-system-design.md | grep -v "決定記録\|ワードマーク\|logo-proposals"`
Expected: 出力なし(歴史的記述・ロゴ経緯以外に Archivo が残らない)

Run: `python3 scripts/check_contrast.py > /dev/null; echo exit=$?`
Expected: `exit=0`

- [ ] **Step 5: Commit + タグ + push**

```bash
git add README.md docs/superpowers/specs/2026-07-20-tombo-design-system-design.md
git commit -m "docs: document v0.2 typography in README and spec §6"
git tag v0.2.0
git push origin main v0.2.0
```

注: README Quick start の jsDelivr URL は `@v0.1.1` のまま(タイポグラフィ変更を含む CSS を配るには v0.2.0 へのピン更新が必要だが、これは全タスク完了・最終レビュー通過後に行うため本タスクでは触らない。最終レビュー後、コントローラーが `@v0.1.1` → `@v0.2.0` の 1 行更新を別コミットで行う)。

---

## 完了後(コントローラーの仕事)

1. 最終ホールブランチレビュー(subagent-driven-development の手順通り)
2. README の jsDelivr ピンを `@v0.2.0` に更新して commit・push
3. **ユーザーに R1 最終確認を依頼**(spec §8-3: docs.html か catalog の 15px/30px 和文本文を実際に通し読みしてもらい、読み疲れがないか — NG なら M PLUS 2 のウェイト 430–470 で再調整)
4. メモリ(tombo-design-system.md)に v0.2 出荷を記録
5. サイトリデザイン(保留中)の再開 — v0.2 を消費する
