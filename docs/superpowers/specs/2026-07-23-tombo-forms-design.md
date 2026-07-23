# TOMBO forms 語彙 — 設計 (2026-07-23)

## 背景・目的

TOMBO はロードマップ上**最大の空白がフォーム**である。tombo.css は `input/select/textarea/checkbox/radio/label/fieldset/legend` を一切スタイルしておらず（reset 層の `button, input, select, textarea { font: inherit; color: inherit; }` だけ）、app example が掲げる `/login` 画面を TOMBO 自身では組めない。

**目的:** ネイティブ要素を土台にした、アクセシブルなフォーム語彙を単一ファイル CSS に追加する。計器の美意識（憲法 §3・署名要素）と整合させつつ、W3C/WCAG 2.2/WAI-ARIA APG のベストプラクティスに準拠する。**JS は不要**（`tombo.js` はテーマとコピーの state 層のみ。フォームはゼロ JS で成立し、検証エラーの表示はサーバ往復でも成立する）。

### ベストプラクティス根拠

- **W3C WAI Forms Tutorial** — Labels / Grouping（`fieldset`+`legend`）/ Instructions / Validating Input / User Notifications（<https://www.w3.org/WAI/tutorials/forms/>）。ネイティブ優先・明示ラベル・グループ化・エラー通知の指針。
- **WCAG 2.2 達成基準** — 1.3.1 情報と関係性 / 1.4.1 色の使用 / 1.4.11 非テキストコントラスト（≥3:1）/ 2.4.7 フォーカスの可視化 / 2.4.11 フォーカスの外観 / 2.5.8 ターゲットサイズ（最小・24×24, AA）/ 3.3.1 エラーの特定 / 3.3.2 ラベルまたは説明 / 3.3.3 エラー修正の提案。
- **ARIA APG** — カスタム widget は作らない（ネイティブで足りる）。`aria-describedby`（help/error の結線）・`aria-invalid`・native `required` のパターンのみ採用。
- **MDN** — `:user-invalid`（操作後のみ発火する検証擬似クラス、Baseline）・`accent-color`（Baseline）・`appearance`。

## スコープ

### 今回やる（純追加・非破壊 = v0.10.0）

- **対象コントロール**: text / email / password / number / search / tel / url の各 `input`、`textarea`、`select`、`checkbox`、`radio`、`label`、`fieldset` / `legend`、help / error テキスト。
- **状態**: resting / focus / invalid / disabled / readonly / required。
- **クラス語彙**: `.tombo-field`・`.tombo-req`・`.tombo-select`・`.tombo-check`・`.tombo-fieldset` と、`.tombo-field` 内に scoped した造形・状態ルール。
- **example**: app.html に実物の `/login` フォームを組む（ロードマップの payoff）。components.html カタログに全コントロール・全状態の「Forms」節を追加。
- **README**: 「Forms」節（クラス一覧 + アクセシブル markup 契約）。

### 今回やらない（対象外・follow-up）

- range / color / file / date-picker の**深い**スタイリング（ネイティブのまま。`.tombo-field` 内でもボックスは当てない）。
- JS によるクライアント検証・エラーの動的トグル（表示制御は author/サーバの責務。語彙は見た目だけを提供）。
- `.tombo-form` ラッパ（accent-color scope と measure 制約を一括する便利クラス）。YAGNI。必要が生じたら follow-up。
- カスタム計器風 checkbox（ネイティブ `accent-color` で足りる。AT 破壊リスクを避ける）。

## 設計判断（ブレインストーミングでユーザー承認済み）

1. **スコープ = コンポーネント scoped**。グローバル `input {}` で classless に効かせず、造形は `.tombo-field` の中でだけ効かせる opt-in。フォームは衝突面が広く（サードパーティ widget を乗っ取る）、`.tombo-btn`/`.tombo-metric` と同じ扱いが安全。reset 層の `font/color: inherit` は据え置き、base 層にグローバル input styling を足さない。
2. **造形 = ハイブリッド C**。hairline ボックス（`.tombo-metric` 系と整合・アフォーダンス高・select/textarea も破綻しない）＋**状態を運ぶ重い下ルール**。下ルールは寸法線・目盛・朱の現在地が宿る「端のルール」＝ TOMBO の署名で、憲法 §1「すべてを測る」をフィールド自身に埋め込む（ベースライン＝計器の読み取り線）。
3. **ラベル声 = mono 大文字**（憲法②）。`.tombo-label`・table th・metric `.k`・kicker と全ラベル共通の声。フォームのラベルは短い名詞句が大半で mono 大文字が得意な register。TOMBO のフォームを TOMBO に見せる最大の一手。
4. **required マーカー = `--tombo-ink` の mono `*`**（**朱ではない**）。憲法 §3 は朱を「現在地を指す 1–2px の線」に限り、テキスト字形の朱は禁止（かつ `shu/paper` 昼 3.97:1 でラベルサイズのテキスト 4.5:1 に届かない）。required は「現在地」でも「エラー」でもない → ink `*`（`ink/paper` 昼 14.82 / 夜 14.96, AAA）。字形（*）＋ native `required` ＋「* required」凡例で意味を多重化し、色に依存しない（1.4.1）。**結果、フォーム語彙に朱は登場しない**（現在地概念が無いので正しく不在）。error は臙脂（`--tombo-error`）が担い役割衝突なし。
5. **checkbox/radio = ネイティブ `accent-color: var(--tombo-green)`**。緑チェック/ドット、a11y・ゼロ JS・OS 準拠。選択であって error/現在地ではないので緑が正。

## 設計（CSS）

すべて `@layer tombo.components` に追加する（reset 層は不変）。以下の control グループは可読性のため `:is()` で示す（実装で列挙に展開可）。

### 1. `.tombo-field`（テキスト系フィールドの単位）

label → control → help/error の縦スタック。内部間隔は space-8。フィールド間の 24px リズムは**既存 `.tombo-flow`** に任せる（新設しない）。

```css
.tombo-field > label {
  display: block;
  margin-block-end: var(--tombo-space-8);
  font-family: var(--tombo-font-mono);
  font-size: var(--tombo-text-label); line-height: var(--tombo-lh-label);
  font-weight: 500; letter-spacing: .14em; text-transform: uppercase;
  color: var(--tombo-ink-sub);
}
.tombo-req { color: var(--tombo-ink); margin-inline-start: .3em; } /* required の * */
.tombo-field .help {
  margin-block-start: var(--tombo-space-8);
  font-size: var(--tombo-text-note); line-height: var(--tombo-lh-note);
  color: var(--tombo-ink-faint);
}
.tombo-field .error {
  margin-block-start: var(--tombo-space-8);
  font-size: var(--tombo-text-note); line-height: var(--tombo-lh-note);
  color: var(--tombo-error);
}
.tombo-field .error::before { content: "!\00a0"; font-weight: 700; } /* 非色の cue（1.4.1） */
```

- **help / error は body 書体・センテンスケース**（mono 大文字は running text の可読性を損なう）。声の計器性はラベルとフィールドが担い、メッセージは prose として読ませる。
- **error の `::before "!"`** が色以外の手掛かりを常に付与（author はメッセージ本文に記号を書かない）。AT への非色 cue は `aria-invalid` が担う。

### 2. control 造形（ハイブリッド C）

```css
.tombo-field :is(
  input:not([type]), input[type="text"], input[type="email"], input[type="password"],
  input[type="number"], input[type="search"], input[type="tel"], input[type="url"],
  select, textarea
) {
  inline-size: 100%;
  background: var(--tombo-surface);
  border: 1px solid var(--tombo-hairline);
  border-block-end: 1.5px solid var(--tombo-ink-sub); /* 計器のベースライン */
  padding: var(--tombo-space-8) var(--tombo-space-12);
  font-family: var(--tombo-font-body);
  font-size: var(--tombo-text-ui); line-height: var(--tombo-lh-ui);
  color: var(--tombo-ink);
  transition: border-color var(--tombo-dur) var(--tombo-ease);
}
```

- **角丸なし**（憲法：図面に丸はない。原則 0）。
- `transition` は border-color のみ（§8 の許可＝計器の明度/線遷移）。

### 3. 状態

```css
/* focus — ベースラインが点灯（クリック/キーボードとも）。2px 緑リングは base の :focus-visible が担う */
.tombo-field :is(<controls>):focus { border-block-end-color: var(--tombo-green); }

/* invalid — :user-invalid（操作後のみ）＋ [aria-invalid]（スクリプト/サーバ検証の普遍フォールバック） */
.tombo-field :is(<controls>):user-invalid,
.tombo-field :is(<controls>)[aria-invalid="true"] { border-block-end-color: var(--tombo-error); }

/* disabled — .tombo-btn:disabled と統一 */
.tombo-field :is(<controls>):disabled { opacity: .5; cursor: not-allowed; }

/* readonly — 背景を paper に沈め、ベースラインを hairline に落として「編集不可」を示す */
.tombo-field :is(<controls>):read-only:not(:disabled) {
  background: var(--tombo-paper);
  border-block-end-color: var(--tombo-hairline);
}
```

- **focus は `:focus`**（ベースライン点灯＝フィールド固有のアフォーダンス、マウスでも反応）。**2px 緑アウトラインは base 層の `:focus-visible`**（キーボード時のみ・AT フォーカスの可視化 2.4.7 / 2.4.11）。両者は冗長でなく**層**（アウトライン＝「キーボードフォーカスここ」、ベースライン＝「このフィールドの状態」）。
- **invalid は `:user-invalid`** を採用（`:invalid` はロード時に未入力必須を即赤化してしまう。`:user-invalid` は操作後のみ）。`:user-invalid` は Baseline（Firefox 88 / Safari 16.5 / Chrome 119）。未対応環境でも `[aria-invalid="true"]` 経路で退化して機能する。
- disabled の opacity 低下によるコントラスト割れは WCAG が非活性 UI を除外するため許容（`.tombo-btn:disabled` 前例と同一）。

### 4. `.tombo-select`（select のカレット）

ネイティブの OS 矢印は計器の見た目を壊すため `appearance: none` ＋ CSS カレット。カレットは**テーマ追従が必要**なので data-URI 画像ではなく**ラッパの `::after`**（`border-color` トークンで描く）で実装する。

```css
.tombo-select { position: relative; }
.tombo-select select { appearance: none; padding-inline-end: var(--tombo-space-32); }
.tombo-select::after {
  content: ""; position: absolute; inset-inline-end: var(--tombo-space-12); inset-block-start: 50%;
  inline-size: 7px; block-size: 7px;
  border-inline-end: 1.5px solid var(--tombo-ink-sub);
  border-block-end: 1.5px solid var(--tombo-ink-sub);
  transform: translateY(-70%) rotate(45deg); pointer-events: none;
}
@media (forced-colors: active) {
  .tombo-select select { appearance: auto; padding-inline-end: var(--tombo-space-12); }
  .tombo-select::after { display: none; } /* ネイティブ矢印を復帰し消失を防ぐ */
}
```

markup: `<div class="tombo-select"><select>…</select></div>`（styled select にはラッパ必須）。

### 5. checkbox / radio と fieldset

```css
:where(.tombo-field, .tombo-check, .tombo-fieldset) { accent-color: var(--tombo-green); }

.tombo-check { /* <label> 自身が行。行全体がクリックターゲット */
  display: flex; align-items: center; gap: var(--tombo-space-8);
  min-block-size: 24px; /* 2.5.8 ターゲットサイズ最小 */
  font-size: var(--tombo-text-ui); line-height: var(--tombo-lh-ui);
}
.tombo-check input { inline-size: 18px; block-size: 18px; }

.tombo-fieldset { border: 0; padding: 0; min-inline-size: 0; } /* min-inline-size:0 = fieldset の flex/grid 収縮バグ回避 */
.tombo-fieldset > legend {
  padding: 0; margin-block-end: var(--tombo-space-8);
  font-family: var(--tombo-font-mono);
  font-size: var(--tombo-text-label); line-height: var(--tombo-lh-label);
  font-weight: 500; letter-spacing: .14em; text-transform: uppercase;
  color: var(--tombo-ink-sub);
}
```

- checkbox/radio は 18px、行 min-height 24px ＋ `<label>` 全体がターゲット → 2.5.8 を満たす。
- **radio / checkbox 群は `<fieldset>`+`<legend>` 必須**（グループ名を AT に伝える。WAI Grouping）。

## アクセシブル markup 契約（README と spec に明記。CSS では強制できない）

```html
<div class="tombo-field">
  <label for="cov">COVERAGE THRESHOLD<span class="tombo-req" aria-hidden="true">*</span></label>
  <input id="cov" type="number" required
         aria-describedby="cov-help cov-err" aria-invalid="true">
  <p class="help"  id="cov-help">0–100 の整数。</p>
  <p class="error" id="cov-err">0 から 100 の数値を入力してください。</p>
</div>
```

- `label[for]` ↔ `control[id]` を必ず結線（暗黙ネストより明示 for/id）。
- help と error の**両方**を `aria-describedby="help-id err-id"`（空白区切り）で結ぶ。error 要素はエラー時のみ存在（サーバ描画 or JS トグル）。
- エラー時のみ `aria-invalid="true"`。必須は native `required`（AT に必須が伝わる。`aria-required` は冗長なので任意）。
- フォーム頭に「**\* required**」を一度明示（3.3.2）。`*` は `aria-hidden`（意味は `required` と凡例が担う）。
- radio/checkbox 群 → `<fieldset><legend>`。
- 入力幅は `inline-size:100%` なので、フォーム容器を wide-shell 全幅に広げない（長すぎる text field は UX 悪化）。measure 目安を README に記す。

## 色・コントラスト

**forms は新しい色を一切増やさない。** border/text すべて既存トークン（ink / ink-sub / ink-faint / green / error / hairline / surface / paper）で構成する。したがって **contrast gate（check_contrast.py の 28 ペア）は無影響**（space-scale リリースと同じ性質）。使用ペアはすべて既存テーブルに存在し基準を満たす:

- error テキスト（メッセージ）: `error/paper` 昼 6.19 / 夜 5.08（AA）。
- error ベースライン（非テキスト ≥3:1）: 同上、余裕で PASS。
- green focus ベースライン/リング（非テキスト）: `green/paper` 昼 7.37 / 夜 8.25。
- ink `*`（required）: `ink/paper` 昼 14.82 / 夜 14.96（AAA）。
- help（ink-faint）: `ink-faint/paper` 昼 4.64 / 夜 5.23（AA）。
- control テキスト（ink on surface）: `ink/surface` 昼 15.81 / 夜 13.70（AAA）。

## example

- **app.html**: `/login` を実物のフォームで組む（email + password + 「Remember me」checkbox + submit、および 1 つのサーバエラー例）。ロードマップの「app の /login が組めない」を解消する payoff。
- **components.html**: カタログに「Forms」節を追加し、全コントロール（text/select/textarea/checkbox/radio）× 全状態（resting/focus/invalid/disabled/readonly）と fieldset/legend、help/error を一望できるようにする（検証と回帰の基準面）。

## README

新設「Forms」節: クラス一覧（`.tombo-field`・`.tombo-req`・`.tombo-select`・`.tombo-check`・`.tombo-fieldset`）、上記アクセシブル markup 契約、状態の擬似クラス（`:focus`/`:user-invalid`/`[aria-invalid]`/`:disabled`/`:read-only`）、measure 目安。既存の container / type / space scale 節と並ぶ公開 API として文書化。

## リリース

- **v0.10.0**（新クラス群の純追加 = 非破壊のマイナー）。banner を tombo.css・tombo.js とも v0.10.0 に、README vendoring pin も v0.10.0 に。
- **ローカル ff-merge + lightweight tag v0.10.0 + push**（v0.7.0〜v0.9.0 と同一手順。リニア履歴維持・force-push なし）。すべてユーザーゲート。

## 検証

- **contrast gate**（check_contrast.py）: 新色なし → PASS（hygiene で実行）。
- **`node --check tombo.js`**: banner のみ変更 → clean。
- **ブラウザ（chrome-devtools・両テーマ）**: components.html「Forms」節と app.html `/login` を tombo/hotaru で確認。特に (a) ハイブリッド造形が両テーマで破綻しないこと、(b) focus でベースライン緑点灯＋キーボード時の 2px リング、(c) invalid で error ベースライン＋メッセージ、(d) disabled/readonly の識別、(e) select カレットのテーマ追従。
- **キーボード/AT**: Tab で全コントロールを辿り `:focus-visible` リングが可視・`.tombo-check` の行全体がターゲット・fieldset/legend のグループ名。`:user-invalid` は「不正入力 → blur」で発火することを確認。
- **forced-colors**: `@media (forced-colors: active)` で select がネイティブ矢印に復帰し、カレット消失が起きないこと。
- **grep**: 追加ルールが `@layer tombo.components` 内にあり、生の px（トークン外）を新設していないこと（space token / 型トークンのみ参照）。

## 非対象（follow-up として記録）

- `.tombo-form` ラッパ（accent-color scope + measure 制約の便利クラス）。
- range / color / file / date-picker の深いスタイリング、JS クライアント検証。
- `@media print`、`text-autospace`/`palt`、CI（別ロードマップ項目）。
