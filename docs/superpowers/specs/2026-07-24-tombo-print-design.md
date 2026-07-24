# TOMBO print 語彙 — 設計 (2026-07-24)

## 背景・目的

**トンボ (tombo) は印刷の見当・裁ち落としマークそのもの**である。README 冒頭がそう定義する（"a printer's registration mark — the small cross drawn on a printing plate so every layer of ink aligns to the same point"）。にもかかわらず tombo.css には `@media print` も `@page` も一切無く、名前が指す本来の仕事——**紙にトンボを刷る**——を果たしていない。加えて、hotaru（夜）テーマのページを刷ると黒い矩形が、コードブロックは薄字が白地に落ちて読めない、など素の印刷が破綻する。

**目的:** ①どの TOMBO ページも素直に刷れる**印刷ハードニング**（無条件）と、②opt-in で紙面の余白に**本物のトンボ（単一角トンボ＋センタートンボ）を刷る**署名機能、の2つを単一ファイル CSS に追加する。計器の美意識（憲法 §1「すべてを測る」/ §3「朱は現在地」）と整合させる。**JS 不要**（`@media print` と `@page` のみ。tombo.js は無関係）。

### ベストプラクティス根拠

- **CSS Paged Media Module Level 3** — `@page` と `margin`（<https://www.w3.org/TR/css-page-3/>）。印刷の余白は `@page` が唯一の正規手段。margin box（`@top-center` 等）の `content` はブラウザ未実装なので**使わない**。
- **CSS 2.1 §11.1.1 / CSS Positioned Layout** — paged media では `position: fixed` の要素は**各ページに反復**して描かれる。トンボを毎ページ出す機構の根拠。
- **CSS Fragmentation Module Level 3** — `break-inside: avoid` / `break-after: avoid` / `orphans` / `widows`（<https://www.w3.org/TR/css-break-3/>）。改ページ制御の正規プロパティ。
- **CSS Color Adjustment Module Level 1 / MDN `print-color-adjust`** — 既定で背景色・背景画像は**印刷されない**（`economy`）。背景描画で作るトンボは `print-color-adjust: exact` を当てないと出ない（<https://developer.mozilla.org/en-US/docs/Web/CSS/print-color-adjust>）。逆に、当てるのは**トンボのオーバーレイに限定**し、本文の面塗りは節約に任せる。
- **MDN `color-scheme` / `light-dark()`** — 印刷時に `color-scheme` を light へ倒せば既存トークンの `light-dark()` が light 値へ解決し、夜ページも紙は白になる。

## スコープ

### 今回やる（純追加・非破壊 = v0.11.0）

- **A. 印刷ハードニング（無条件・全印刷）**: 夜→紙は白 / コードブロックを白地インク / 画面専用 chrome の非表示 / glow・motion 無効化 / 改ページ制御 / `@page { margin: 16mm }`。
- **B. 紙のトンボ（opt-in `.tombo-trim`）**: `<body class="tombo-trim">` のページだけ、毎ページの余白帯に**四隅の単一角トンボ＋各辺中央のセンタートンボ**をインク1色で刷る。
- **example**: `docs.html` に `class="tombo-trim"` を付け、⌘P で実際にトンボが出る生きた実例にする。app / lp / components はハードニングだけで綺麗に刷れることを確認。
- **components.html**: 印刷の短い節（`.tombo-trim` の使い方＋「⌘P で確認」）。
- **README**: `## Print` 節（ハードニングの説明＋`.tombo-trim` の opt-in）。
- バナー（tombo.css / tombo.js）と README vendoring pins を **v0.11.0** へ。

### 今回やらない（対象外・follow-up）

- **裁ち落とし（bleed）に忠実な二重角トンボ**。ブラウザ印刷に bleed 領域は無く、外側の線は存在しない裁ち落としを描く＝憲法「飾りは嘘をつかない」と緊張。単一角トンボ（Option 2）を採る。
- **リンク URL の印刷展開**（`a::after { content: " (" attr(href) ")" }`）。雑音になりやすく YAGNI。将来 opt-in の余地だけ残す。
- **`@page :first` / `@page :left/:right` の左右非対称余白**。製本用途は現状の TOMBO の射程外。
- **margin box（`@top-center` 等）による柱・ノンブル**。ブラウザ未実装。

## 設計判断（ブレインストーミングでユーザー承認済み）

1. **紙のトンボは opt-in（`.tombo-trim`）**。signature 群も glow も「音量」は常に opt-in で、強制した前例が無い。実用文書（請求書・記事）をただ刷った紙に裁ち切りマークが勝手に生えるのは印刷事故に見える。ハードニング（A）だけは無条件（純粋な衛生で誰も損しない）。
2. **図像 = 単一角トンボ＋センタートンボ（Option 2「実式」）**。四隅に単一 L（＝印刷可能域の角＝真の仕上がり）、各辺中央に⊕（見当十字）。ブラウザ印刷では紙の端が実際の仕上がり線なので**描いた全マークが実測を指す**——憲法 §1「すべてを測る」/「飾りは嘘をつかない」に忠実。実機比較で二重（本式）と見比べ、単一を採用。
3. **マークは `--tombo-ink` 1色（朱ではない）**。実物のトンボは全版を重ねる基準＝レジストレーションブラック（全版黒）で刷られる。§3 の朱は「現在地を指す 1–2px の線」に限られ、トンボは「現在地」でも「エラー」でもない見当合わせの基準 → ink が正。**結果、印刷語彙に朱は登場しない**（現在地概念が無いので正しく不在）。既存の朱の細線（`.tombo-current`/`.tombo-kicker`/`.tombo-ruler`）は印刷でも**そのまま**（1–2px の線で忠実に刷れ、B/W でもティックとして機能。面塗り朱は存在しない）。
4. **`@page { margin: 16mm }` を全印刷に効かせる**（ユーザー承認済み）。ハードニングの一部＝一貫した読みやすい余白。トンボはこの余白帯の中に収まる。opt-in でない唯一の全体変更だが、追加・非破壊で誰も損しない。
5. **新色ゼロ**。全マーク・全ハードニングは既存トークン（`--tombo-ink` 等）を再利用。**contrast gate は構造不変**。

## 設計（CSS）

すべて **新規の `@media print` ブロック** を tombo.css 末尾（`@layer tombo.components` 内、forms の後）に追加する。reset / tokens / base 層は不変。`@page` はレイヤー外（`@page` は `@layer` に入れられない仕様）でファイル末尾に置く。

### A. 印刷ハードニング（無条件）

```css
@page { margin: 16mm; }

@media print {
  /* 夜ページも紙は白: color-scheme を light へ倒し light-dark() を light 値に解決 */
  :root,
  :root[data-theme="tombo"],
  :root[data-theme="hotaru"] { color-scheme: light; }

  /* 画面専用 chrome は刷らない */
  .tombo-themes, .tombo-copy { display: none !important; }

  /* glow / motion を無効化（forced-colors ブロックと同じ扱い） */
  .tombo-glow { background-image: none; box-shadow: none; }
  .tombo-glow .tombo-display,
  .tombo-glow.tombo-metric > .v { text-shadow: none; }
  *, *::before, *::after { transition: none !important; animation: none !important; }

  /* コードブロック: 画面は黒パネル（背景=既定で刷られない→薄字が白に落ち読めない）。
     印刷は白地インク・ヘアライン枠へ明示上書き */
  .tombo-code, .tombo-code pre {
    background: #fff !important;
    color: var(--tombo-ink) !important;
    border: 1px solid var(--tombo-hairline);
  }
  .tombo-code > figcaption { color: var(--tombo-ink-sub) !important; }

  /* 改ページ制御 */
  .tombo-metric, .tombo-callout, .tombo-code, figure, tr, .tombo-check { break-inside: avoid; }
  h1, h2, h3, h4 { break-after: avoid; }
  p, li { orphans: 2; widows: 2; }
}
```

### B. 紙のトンボ（opt-in `.tombo-trim`）

機構は既存のワイド画面 registration mark（`html:has(> body.tombo-gutters)::before`、`@media (min-width:1600px)`）と同じ **gradient で描くマーク**を踏襲する。印刷では `html:has(body.tombo-trim)` の擬似要素を `position: fixed` にし、`print-color-adjust: exact` を**このオーバーレイに限定**して当て、全ページに反復させる。擬似は2つに分担する：

- `::before` = **四隅の単一角トンボ**（各コーナー L = 水平＋垂直の2線、計8本の linear-gradient レイヤ）。
- `::after` = **各辺中央のセンタートンボ**（丸＝radial-gradient のリング4つ ＋ 十字＝linear-gradient の水平/垂直8本）。

```css
@media print {
  html:has(body.tombo-trim)::before,
  html:has(body.tombo-trim)::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
    background-repeat: no-repeat;
  }
  /* ::before = 四隅の角トンボ / ::after = 各辺のセンタートンボ。
     具体のグラデーション各レイヤ（位置・寸法）は実装で確定する（下記「幾何」参照）。 */
}
```

**幾何（意図値。実装で印刷プレビュー実測により確定）**

- **角トンボ**: L の腕長 ≈ 24px、線幅 1px（ink）、コーナーから gap ≈ 6px。単一（内側1組のみ）。四隅。
- **センタートンボ**: リング径 ≈ 13px（線幅 1px）＋ 十字の腕長 ≈ 24px（線幅 1px）、各辺の中央。
- **配置基準**: 実機比較モックの構図（マークは仕上がり＝印刷可能域の角/辺を指し、`@page` の 16mm 余白帯の中に収まる）を目標にする。

**実装で必ず実測・確定する未確定点（印刷は engine 依存が強い）**

1. **`position: fixed` の基準ボックス**が「印刷可能域（`@page` margin の内側）」か「紙面」かは Chrome で実測する。マークを余白帯に落とすため、`inset` の符号・大きさ（必要なら負の inset や負 margin でオーバーレイを紙面まで広げる）を確定する。
2. **全ページ反復**が効くこと（複数ページの docs.html で確認）。
3. **本文と衝突しない**こと（マークは余白帯、本文は `@page` margin の内側）。
4. `print-color-adjust: exact` で**マークが実際に刷られる**こと（背景描画なので必須）。
5. **フォールバック**: 余白帯への配置がエンジン間で安定しない場合は、印刷可能域の四隅を**内向きに抱える単一 L**（＝`.tombo-corners` を紙面スケールにしたもの）＋各辺中央の⊕へ退避する。これも「マークが真の印刷可能域の角/辺を指す」点で憲法に忠実。どちらに落ちても**実機の印刷プレビューをユーザーに提示**して最終確認する。

## example / ドキュメント

- **docs.html**: `<body>` に `class="tombo-trim"` を追加（既存クラスと併記）。⌘P で四隅の角トンボ＋各辺のセンタートンボが出る。
- **components.html**: 印刷の短い節を追加（`.tombo-trim` の 1 行 markup ＋「このページを ⌘P するとトンボが出る」ヒント）。印刷はスクリーンに映る「コンポーネント」ではないので、カタログには**振る舞いの説明**として置く。
- **README**: `## Print` 節。ハードニング（無条件で素直に刷れる）＋ `.tombo-trim` の opt-in（紙にトンボ）を説明。

## 検証（JS テストランナ無し = computed-style / 印刷プレビュー / grep）

1. **`node --check tombo.js`** clean（tombo.js はバナーのみ変更）。
2. **`python3 scripts/check_contrast.py`** 全 PASS（新色ゼロ）。
3. **chrome-devtools 印刷プレビュー**（両テーマ）:
   - ハードニング: hotaru ページが**白地**に刷れる / コードブロックが**白地インクで可読** / `.tombo-themes`・`.tombo-copy` が**非表示** / glow 無し / 改ページで `.tombo-metric` 等が割れない。
   - トンボ（docs.html `.tombo-trim`）: 四隅の角トンボ＋各辺のセンタートンボが**インクで出る** / **全ページに反復** / 本文と衝突しない。幾何（腕長・gap・リング径）が意図どおり。
   - トンボ**非** opt-in（app.html 等）: マークが出ないこと。
4. **grep**: `@page` と `@media print` ブロックの追加、`print-color-adjust: exact` がオーバーレイに限定されていること、`.tombo-trim` 以外に印刷マークが漏れていないこと。

## リリース（USER-GATED）

`feature/print` で subagent-driven（Sonnet 実装 / Opus レビュー、Haiku 不使用）。最終 Opus whole-branch レビュー後、local ff-merge + lightweight tag `v0.11.0` + push（リニア履歴、force-push 無し）。その後 `tombo-roadmap` memory を更新（print done → v0.11.0、残 = text-autospace, CI）。
