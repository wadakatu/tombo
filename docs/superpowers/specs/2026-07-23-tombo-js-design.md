# TOMBO tombo.js 設計書 — 任意・ゼロ依存の状態レイヤー

日付: 2026-07-23
状態: ユーザー承認待ち(Q1–Q4 は会話で承認済み、本書は統合レビュー用)
対象: 新規ファイル `tombo.js`(任意読み込み) + `tombo.css` への小追加 + examples/README/spec 更新。次のマイナー(想定 v0.6.0)。破壊的変更なし(純追加)。

## 1. 背景と目的

TOMBO は「ゼロ JS」を憲章に掲げていたが、その結果 **JS が消えるのではなく利用者側へ押し付けられていた**:

- テーマ切替 JS が 4 つの example に ~14 行ずつ重複(`.tombo-themectl` の CSS も 4 重複)。
- コードブロックの `COPY` が `<button>` ですらない `<span>COPY ⧉</span>` — 押せるように見えて何も起きない**偽アフォーダンス(a11y 欠陥)**。

方針を **「ゼロ依存は死守 / ゼロ JS はプログレッシブエンハンスメント(PE)に緩める」** へ転換する(別紙 [[tombo-direction]] のワークスペース合意)。採用ゲートは **Baseline widely available**、判定は「W3C か」ではなく「相互運用(Baseline)か」。`tombo.js` は **プラットフォームが提供しない『状態』だけ**を担う — テーマ永続化とクリップボード。modal/popover/menu 等のプリミティブは再実装せず `<dialog>` / popover / `command` に委ねる。

### 不変条件(PE の砦)

**JS が無くてもページは完全に機能する。** 具体的には JS 不在時:
- テーマは `light-dark()` で **OS 追従**(既存挙動、無変更)。
- テーマ制御は `hidden` のまま出現しない。
- コピーボタンは**存在しない**(注入されない)ため、偽アフォーダンスが原理的に発生しない。

## 2. スコープ

**担う(YAGNI 準拠)**: (1) テーマ設定の永続化 + フラッシュ防止、(2) コードブロックのコピー。
**担わない**: modal/popover/tooltip/menu/tabs/nav(CSS + プラットフォームの仕事)、アニメーション表現(CSS 側。spec §8 のバウンス/パララックス禁止は不変)、ビルドステップ、依存。

## 3. テーマ永続化(Q1=3値 / Q2=localStorage + インライン起動)

### 3.1 3値モデル

設定は **`system` / `tombo` / `hotaru`** の3値(業界コンセンサス: bi-state は最頻出の誤り)。`system` は「OS 追従に戻れる第一級状態」。

- **保存形式**: `localStorage['tombo-theme']` に `"tombo"` か `"hotaru"` のみ格納。**`system` は「キー不在」で表現**(= `removeItem`)。これによりインライン起動片は tombo/hotaru のときだけ作用し、`system` は既定の OS 追従に自然に戻る。
- **適用**: 明示テーマは `<html data-theme="tombo|hotaru">`。既存の `:root[data-theme] { color-scheme }` と `light-dark()` がそのままカスケードするため、`data-theme` を差す/外すだけでよい。

### 3.2 フラッシュ防止 — 描画前インライン起動片

`light-dark()` は CSS で localStorage を読めないため、**保存値の適用は描画前 JS が必須**。`<head>` に極小のブロッキング片を置く(2026 標準: IIFE + try/catch + allowlist):

```html
<script>try{var t=localStorage.getItem('tombo-theme');if(t==='tombo'||t==='hotaru')document.documentElement.dataset.theme=t}catch(e){}</script>
```

- ~100 バイト。フラッシュ完全ゼロ。本体 `tombo.js` は描画後で良いので `defer`。
- **任意**: 省いても動く(上書きユーザーだけが一瞬のフラッシュを見る)。PE のダウングレードとして許容。

### 3.3 SSR/Cookie は任意の上乗せ(ドキュメントのみ)

Cookie 方式は SSR 環境でフラッシュゼロかつインライン片不要にできるが、**サーバ側レンダリングロジックが必須でプレーン静的 HTML では成立しない**。ゆえに TOMBO の出荷既定は localStorage + インライン片(全環境で動く唯一の方式)。Blade / Astro-SSR 利用者向けに「Cookie からサーバで `data-theme` を出力すればインライン片も省ける」上位互換を README に記載する。

## 4. API 形状(Q3=B: 宣言的 auto-init + 極小グローバル)

配布は **IIFE・非 ES module・`defer`**(全環境 drop-in の定石。module は読み込み順/CORS/`file://` の難あり)。主要 drop-in ライブラリ(Bootstrap/Alpine/htmx)に倣い **宣言的 auto-init を主役 + 単一名前空間グローバル**を露出。

### 4.1 宣言的マークアップ(利用者が書くのはこれだけ)

テーマ制御は配置が可変(footer/header 等)なので**利用者がマークアップを書き、tombo.js が `hidden` 解除 + 配線**:

```html
<div class="tombo-themes" hidden>
  <button type="button" data-tombo-theme="system">system</button>
  <button type="button" data-tombo-theme="tombo">tombo</button>
  <button type="button" data-tombo-theme="hotaru">hotaru</button>
</div>
```

- スタイルは class `.tombo-themes`、挙動フックは属性 `[data-tombo-theme]`(style と behavior の分離)。
- **現在地表示**: 設定(resolved ではなく setting)に一致するボタンへ `aria-pressed="true"` + 朱の下線(S-05 の自己ドッグフード)。`system` 選択時は system ボタンが押下表示(OS がダークでも「setting=system」を示す)。

### 4.2 グローバル

```js
window.Tombo = {
  setTheme(setting),  // 'system' | 'tombo' | 'hotaru'
  getTheme()          // 保存された setting を返す(不在時は 'system')
}
```

- `setTheme('tombo'|'hotaru')` → `setItem` + `data-theme` 付与。`setTheme('system')` → `removeItem` + `data-theme` 除去(OS 追従へ)。
- 利用者が localStorage / `data-theme` を素手で触らずに済む公認フック(壊れやすい部分の再実装を防ぐ)。

### 4.3 イベント委譲

テーマボタン・コピーボタンとも **`document` に 1 個の委譲リスナー**(要素ごとに貼らない)。動的追加された `.tombo-code` にも対応し、性能ベストプラクティスに合致。

## 5. コピー(Q4=自動注入 + a11y UX)

### 5.1 自動注入

`tombo.js` は各 `.tombo-code:not([data-tombo-copy="off"])` を走査し、その `<figcaption>` に実 `<button class="tombo-copy" type="button" aria-label="Copy code">COPY ⧉</button>` を注入する(figcaption 不在なら生成)。利用者のコピー用マークアップはゼロ。既存の偽 `<span>COPY ⧉</span>` は examples から削除。

- **なぜ注入か**: ボタンは JS が走った時だけ存在 = **偽アフォーダンスが原理的に生じない**(PE 最良)。配置がコード欄の caption に固定なので自動化が安全。
- **オプトアウト**: `.tombo-code[data-tombo-copy="off"]`。

### 5.2 動作と UX

クリック → 同 `figure` 内 `<pre>` の `textContent` を `navigator.clipboard.writeText` → ボタン表示を `COPIED ✓` に変更、共有の live 領域で通知、**~1.5 秒**で `COPY ⧉` に復帰。`writeText` 不可(非セキュア文脈等)の場合のみ最小フォールバック(選択 or「⌘C を押す」ヒント)。

### 5.3 アクセシビリティ

- 実 `<button>`(Space/Enter は自動)+ `aria-label`。
- **共有の視覚非表示 live 領域** `<div role="status" aria-live="polite" class="tombo-sr-only">` を tombo.js が 1 つ生成し、全コピーの成否を通知。
- **関連: コード欄のフォーカス**。`.tombo-code pre` は `overflow-x:auto` のスクロール領域だが既定でフォーカス不可。JS 不在でもキーボードでスクロールできるべきなので **マークアップで `tabindex="0"` を付与する**ことを README に記載(table-wrap と同じ「スクロール領域はフォーカス可能に」の掟。JS では付けない — PE のため)。

## 6. tombo.css への追加(本機能に付随)

`tombo.js` 単体では完結せず、以下を `tombo.css` に追加する(examples の重複を解消するため):

- `.tombo-themes` — テーマ制御コンテナ + `[data-tombo-theme]` ボタンの静止/`aria-pressed`(朱下線)スタイル。現状 example ローカルに 4 重複しているものをシステム側へ昇格。
- `.tombo-copy` — 注入されるコピーボタンの静止/hover/`COPIED` スタイル(現行の caption COPY の見た目に一致させる。mono・大文字・caption 色)。
- `.tombo-sr-only` — 視覚非表示ユーティリティ(live 領域用。TOMBO に未存在のため新設)。

いずれも純追加でコントラストゲートに影響しない(色トークン不変)。

## 7. 配布

`tombo.js` は `tombo.css` と同様に**タグから vendor**(private リポのため CDN 無し。消費側で sha256 をピン留めして CI 検証)。読み込みは `<script src="/path/tombo.js" defer></script>` + §3.2 のインライン起動片。ソフトなサイズ目安 ~1–2KB(未圧縮)。ライセンスバナーを `tombo.js:1` に付す。

## 8. 検証方針

- **PE 不変条件**: JS を無効化して examples を開き、(a) テーマが OS 追従、(b) テーマ制御が非表示、(c) コピーボタンが存在しない、(d) ページが完全に使えることを確認。
- **フラッシュ**: 保存値と OS を食い違わせ(例 OS=dark / 設定=tombo)、リロードでフラッシュが出ないこと(インライン片あり)/ 出ること(インライン片なし・許容)を確認。
- **3値遷移**: system↔tombo↔hotaru の往復、リロード後の永続、`system` で OS 追従復帰を確認。
- **コピー**: クリップボード内容一致、`COPIED ✓` 表示と復帰、`role=status` の読み上げ、キーボード(Space/Enter)動作。
- **回帰**: 既存コンポーネント無変更、`python3 scripts/check_contrast.py` PASS、昼夜両テーマのスクリーンショット(グローバル UI ルール)。
- TDD 補足: computed-style の自動 assert は未整備(CI 段の候補)。上記手順の実測 + スクショが証跡。

## 9. リリース

想定 **v0.6.0**(純追加のマイナー)。ロードマップ上の E(`--tombo-shell-max` 削除 = 破壊的)は独立の論理変更なので**別リリース(例 v0.7.0)に分離**することを推奨(atomic release)。最終的な版番号は実装計画時に確定。
