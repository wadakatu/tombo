# TOMBO CI — 設計 (2026-07-24)

## 背景・目的

TOMBO はロードマップの機能語彙（tokens / space scale / forms / print / text-autospace …）を一通り出し切った。残る最後の項目が **CI** で、これを整えると TOMBO は「完成」する。現状 `.github/` は無く、品質ゲート（`scripts/check_contrast.py`・両テーマ目視・`node --check`・banner/pin 整合）はすべて**手作業**で回している。人手ゆえ回し忘れ・見落としが起こりうる。

**目的:** それらのゲートを GitHub Actions で自動化し、かつ **ローカルと CI が同一コマンド**で回る形にする。特に [[tombo-direction]] が掲げる進歩的強化（PE）の規律——「Baseline widely を既定の採用ゲートとし、それ未満は正当化の上で使う」——を**機械で強制**する `use-baseline` ゲートを中核に据える。これにより「うっかり非 Baseline 機能を足す」が CI で落ち、意図的な PE 機能は**正当化つき台帳**として明文化される。

### ベストプラクティス根拠

- **`use-baseline`（stylelint-plugin-use-baseline, ryo-manba）** — <https://github.com/ryo-manba/stylelint-plugin-use-baseline>。`plugin/use-baseline` は CSS の各機能（プロパティ・at-rule・メディア条件・値・関数・単位・擬似要素/擬似クラス）を Baseline データセットに照合する。`available: "widely"`(既定・30ヶ月)／`"newly"`／`YYYY`。許容は `@supports` で包む、または設定の `ignoreProperties`/`ignoreFunctions`/`ignoreSelectors`/`ignoreAtRules`/`ignoreUnits` で行う（**設定側で完結＝tombo.css を触らない**）。`@supports` が不要（＝既に available）なら「unnecessary @supports」を警告する（陳腐化した guard を検出）。
- **web.dev — Baseline を CI に組み込む** — <https://web.dev/blog/eslint-baseline-integration>。ESLint/stylelint の baseline ルールで採用窓をコードベースに強制するのが 2025 の推奨。TOMBO の PE 方針と直結。
- **CSS ライブラリ CI の標準形** — stylelint（lint）・構文妥当性・サイズ予算（gzip 上限、Open Props はバンドル別にサイズ追跡）・a11y/コントラスト・ビジュアル回帰・タグ時公開自動化。TOMBO はこのうち合わないものを落として採る（下記スコープ）。

## スコープ

### 今回やる（CI 基盤の純追加・version bump なし）

`.github/workflows/ci.yml` の単一ジョブが、ローカルと同一の **`npm run check`（= `scripts/check.sh`）** を実行する。5つのゲート:

1. **stylelint** — `plugin/use-baseline`（`widely`）＋最小エラー規則。allow-list 台帳は設定にコメント付きで。
2. **コントラスト** — 既存 `scripts/check_contrast.py`（exit 0/1、37 PASS）。
3. **サイズ予算** — 新規 `scripts/check_size.py`（依存ゼロ）。`tombo.css`/`tombo.js` を gzip して上限と比較。
4. **banner/tag 整合** — 新規 `scripts/check_banner.py`。banner×2 と README ピン×3 の一致、タグ push 時はタグとも一致。
5. **`node --check tombo.js`**。

新規/変更: `.github/workflows/ci.yml`・`package.json`＋`package-lock.json`・`stylelint.config.mjs`・`scripts/check.sh`・`scripts/check_size.py`・`scripts/check_banner.py`／README に短い `## CI` 節。**tombo.css・tombo.js は不変（banner は v0.12.0 のまま）**。

### 今回やらない（対象外・follow-up）

- **stylelint-config-standard + Prettier**。チームの整形強制用で、TOMBO の意図的な整形（複数宣言の1行化・トークン桁揃え・独自コメント声）を大量に誤検出する。手書き1ファイルには**最小エラー規則**が最適。
- **ビジュアル回帰（Percy/Chromatic/Playwright）**。重い基盤（ホスト型 or スクショ基準のリポジトリ同梱）。両テーマ目視（chrome-devtools）で代替済み。将来必要になれば別項目。
- **npm publish / リリース自動化**。TOMBO は private・vendored 配布で npm パッケージではない。タグ push は既存のローカル ff-merge 運用のまま。
- **version bump / タグ**。CI は配布物（tombo.css/js）の API を変えないので semver 対象外。commit は `ci:`。
- **HTML バリデーション・リンクチェック・actionlint**。価値はあるが今回のスコープ外（YAGNI）。

## 設計判断（ブレインストーミングでユーザー承認済み）

1. **Baseline しきい値 = `widely` ＋ 正当化つき allow-list 台帳**（ユーザー承認済み）。[[tombo-direction]] の文言（「gate = Baseline widely、newly は `@supports` の後ろでのみ」）に忠実。`widely` は TOMBO の土台である `light-dark()`（newly 2024）・`:has()`・`:user-invalid` を弾くので、設定が「widely でない使用機能とその正当化」の**明示台帳**になる——これが価値。新しい非 widely 機能を足すと CI が落ち、台帳に正当化を書くまで通らない。`newly` は「Limited だけ吠える」案として検討し、より厳格な `widely` を採用。
2. **allow-list 台帳は stylelint 設定側（`ignore*` オプション）に置く**。プラグインが設定での除外を支持するので、**tombo.css を一切触らずに**台帳を持てる。`@supports` で包む案もあるが、text-autospace 等は「宣言するだけで graceful に degrade」する設計なので guard は不要（包むと unnecessary @supports 警告にもなる）。台帳の見込みは `text-autospace`（Limited）・`light-dark`・`:has`・`:user-invalid`、実測で `print-color-adjust`・改ページ系を追記しうる。**最終台帳は実装時に stylelint を1回走らせて実測で確定**（弾かれた各機能を「なぜ許容か」付きで登録）。
3. **stylelint = 最小エラー規則のみ**。`use-baseline` をホストするために stylelint は必須だが、規則は本物のバグだけ（不正hex・重複プロパティ・空ブロック・未知プロパティ/単位・`@layer`/`@page` 位置 等）。**実測でゼロ違反の規則だけ採用**し、意図した造形と競合するものは入れない。
4. **サイズ予算・banner 整合は依存ゼロの自作計器**（`check_contrast.py` の系譜）。`size-limit` 等の npm ツールを増やさず、Python 標準ライブラリで gzip サイズと banner/pin/tag の一致を測る。憲法 §1「すべてを測る」に忠実。
5. **ローカルと CI は同一コマンド**（`npm run check` → `scripts/check.sh`）。ローカル ff-merge 運用では CI は main push 後の**事後レポート**になるため、手元の `npm run check` が ff-merge 前の実質ゲートになる。両者が同一スクリプトを呼ぶことで乖離しない。
6. **package.json は dev 依存のみ**。利用者は tombo.css を vendor するだけで `npm install` しない＝**単一ファイル配布の原則は不変**。npm 導入は dev/CI 専用の関心事。

## 設計

### `package.json`（dev 依存のみ）

```jsonc
{
  "name": "tombo", "private": true, "type": "module",
  "scripts": {
    "check": "bash scripts/check.sh",
    "lint:css": "stylelint 'tombo.css'"
  },
  "devDependencies": {
    "stylelint": "^16",
    "stylelint-plugin-use-baseline": "^1"
  }
}
```
（正確な最新版は実装時に確定し `package-lock.json` を同梱。`npm ci` で再現可能に。）

### `stylelint.config.mjs`

```js
export default {
  plugins: ["stylelint-plugin-use-baseline"],
  rules: {
    "plugin/use-baseline": [true, {
      available: "widely",
      ignoreProperties: ["text-autospace"],       // Limited — PE で degrade（未対応はベタ組み）
      ignoreFunctions:  ["light-dark"],            // Baseline newly 2024 — 全トークンの土台
      ignoreSelectors:  [":has", ":user-invalid"], // newly/境界 — PE で無害に degrade
      // print-color-adjust・break-inside 等は実測で必要なら「なぜ許容か」付きで追記
    }],
    // 最小エラー規則（実測でゼロ違反のものだけ最終採用）
    "color-no-invalid-hex": true,
    "declaration-block-no-duplicate-properties": true,
    "block-no-empty": true,
    "no-duplicate-selectors": true,
    "property-no-unknown": true,
    "unit-no-unknown": true,
  },
};
```

### `scripts/check_size.py`（新規・依存ゼロ）

`tombo.css`/`tombo.js` を読み、`gzip` 圧縮後バイト数を上限と比較。実測値と上限を表示、超過で exit 1。上限（見込み・実装時に実測で確定）: `tombo.css` gzip ≤ **12 KiB (12288 B)**（現 10,243 B）、`tombo.js` gzip ≤ **2 KiB (2048 B)**（現 1,273 B）。

### `scripts/check_banner.py`（新規・依存ゼロ）

- `tombo.css`:1 と `tombo.js`:1 の banner から version を抽出（`/*! TOMBO … vX.Y.Z …`）。
- README の vendoring ピン3本（`git … show vX.Y.Z:…`）から version を抽出。
- 4者（css・js・pin×3）が全一致でなければ exit 1。
- 環境変数 `GITHUB_REF` が `refs/tags/vX.Y.Z` のとき、その version と一致しなければ exit 1（タグ push 時の追加検査）。

### `scripts/check.sh`（新規・オーケストレータ）

5ゲートを順に実行し、いずれか失敗で非ゼロ終了（`set -e` 相当）。各ゲートの見出しと結果を出力。CI もローカルもこれを呼ぶ。

```sh
#!/usr/bin/env bash
set -euo pipefail
npx stylelint 'tombo.css'
python3 scripts/check_contrast.py
python3 scripts/check_size.py
python3 scripts/check_banner.py
node --check tombo.js
```

### `.github/workflows/ci.yml`

```yaml
name: CI
on:
  push: { branches: [main], tags: ['v*'] }
  pull_request: { branches: [main] }
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm run check
```
（`python3` は ubuntu-latest に標準搭載。banner のタグ検査は `GITHUB_REF` で効く。）

### README `## CI` 節

ゲートの一覧（use-baseline=widely＋台帳・contrast・size・banner/tag・node）と、ローカルで `npm run check` を回せること、CI が事後レポートである旨を短く記す。

## 検証（初回 CI 緑を実装時に担保）

1. `npm run check` がローカルで**全緑**: stylelint ゼロ違反（台帳確定後）・contrast 37 PASS・size 上限内・banner 一致（全て v0.12.0）・`node --check` OK。
2. `stylelint.config.mjs` の台帳が過不足ないこと（`available:"widely"` で走らせ、弾かれた機能＝台帳エントリが1:1）。意図的 PE 機能のみが台帳にあり、それ以外は素で通る。
3. `check_banner.py` の自己検証: わざと banner を不一致にすると exit 1、`GITHUB_REF=refs/tags/v0.12.0` で一致 exit 0・`v9.9.9` で exit 1。
4. `check_size.py`: 現サイズで exit 0、上限を現値未満に一時変更すると exit 1。
5. ワークフロー YAML の妥当性（構文）。push 後に Actions が緑。

## References

- stylelint-plugin-use-baseline: <https://github.com/ryo-manba/stylelint-plugin-use-baseline>
- web.dev — ESLint/Baseline in CI: <https://web.dev/blog/eslint-baseline-integration>
- stylelint: <https://github.com/stylelint/stylelint>
- Open Props（サイズ追跡・release ワークフローの参考）: <https://github.com/argyleink/open-props>

関連: [[tombo-overview]], [[tombo-direction]], [[tombo-roadmap]], [[tombo-repo-conventions]]。
