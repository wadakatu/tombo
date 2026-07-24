# TOMBO text-autospace 語彙 — 設計 (2026-07-24)

## 背景・目的

TOMBO の examples は和文と欧文の境目に**手打ちの半角スペース**を入れて和欧混植の間隔を作っている（`Composer で導入`・`Laravel 11 以降`・`8 文字以上`・`OpenAPI ドキュメント`）。これは本来コンテンツに紛れ込んだレンダリングのハックで、実害がある——ページ内検索が途切れる（`OpenAPI` の一致がずれる）、コピーに余分な空白が乗る、一部スクリーンリーダーが空白をポーズとして読み上げる、人手ゆえ付け忘れのムラが出る。

CSS Text Module Level 4 の `text-autospace` は、この間隔を**ブラウザが自動で挿入する**正規手段である。和欧境界に正しい**八分アキ（1/8 em）**を入れ、手打ちスペースを不要にする。

**目的:** 手打ち半角を `text-autospace` に置き換える。tombo.css で和欧オートスペースを opt-in し、examples の手打ちスペースを剥がして、CSS ネイティブな和欧混植を実演・提供する。憲法 §1「すべてを測る」に忠実——**ブラウザが厳密な八分アキを測る**のであって、人が広すぎる全角スペースを目分量で置くのではない。

### ベストプラクティス根拠（W3C / 実装者一次情報）

- **CSS Text Module Level 4 — `text-autospace`**（<https://www.w3.org/TR/css-text-4/#text-autospace-property>, <https://developer.mozilla.org/en-US/docs/Web/CSS/text-autospace>）。CJK 表意文字/かなと隣接するラテン文字・数字の間に inter-script spacing を挿入する正規プロパティ。値 `normal` = `ideograph-alpha ideograph-numeric`（和文↔ラテン and 和文↔数字の両方に八分アキ）。
- **CSS Text Module Level 4 — `text-spacing-trim`**（<https://developer.mozilla.org/en-US/docs/Web/CSS/text-spacing-trim>）。全角約物の内側アキを詰める正規プロパティ。**初期値 `normal`（詰めあり）が標準の推奨挙動**であり、対応ブラウザでは宣言なしで既に効く。
- **Chrome for Developers — new i18n CSS features**（<https://developer.chrome.com/blog/css-i18n-features>）。実装者の言明: "Chrome is **planning to start inserting inter-script spacing by default**"（将来オートスペースを既定化する方向）／ "Chrome doesn't insert the spacing if there are explicit space characters around different scripts, so **you don't have to worry about fixing existing content**"（既存の手打ちスペースは尊重され、二重にならない）。

### 実測（Chrome、`text-autospace`/`text-spacing-trim` 対応、2026-07-24 に本設計のため計測）

font-size 20px / M PLUS 2 で計測:

| 検証 | 結果 |
|---|---|
| 和欧境界 + `text-autospace: normal` | 境界1つあたり **+2.5px = 厳密に 1/8 em（八分アキ）** |
| 手打ち半角スペース | **+6.67px ≈ 1/3 em**（八分アキの約3倍で広すぎる） |
| 手打ちスペース + `text-autospace: normal` | +0（**手打ちスペースが autospace を打ち消す**） |
| `text-autospace` の素の computed 値 | **`no-autospace`**（＝既定オフ。仕様初期値は `normal` だが web 互換のため UA 上は当たらない → **明示宣言が必須**） |
| `text-spacing-trim` の素の computed 値 | **`normal`**（＝標準の約物詰めが既定で効く → **触らない**） |
| `text-spacing` shorthand の対応 | **未実装**（`CSS.supports('text-spacing','normal')` = false → longhand を使う） |

この実測から2つの非対称が確定する: (1) `text-autospace` は既定オフなので `normal` を明示して opt-in する必要がある。(2) `text-spacing-trim` は既定が標準推奨の `normal` なので宣言不要。

## スコープ

### 今回やる（純追加・非破壊 = v0.12.0）

- **tombo.css**: `@layer tombo.base` に和欧オートスペースを opt-in（`body { text-autospace: normal }`）＋逐語テキストの除外（`code, kbd, samp, pre { text-autospace: no-autospace }`）。**2 宣言のみ**。
- **examples**: 4 ファイル（docs / app / components / lp）と README のマークアップ・スニペットから、**和欧境界の手打ち半角スペースを剥がす**。
- **components.html**: 和欧混植の短い note（既存の並びに追加）。
- **README**: `## Japanese typography`（和欧混植）節。
- バナー（tombo.css / tombo.js）と README vendoring pins を **v0.12.0** へ。

### 今回やらない（対象外・follow-up）

- **`text-spacing-trim` の明示宣言**。対応ブラウザの既定が標準推奨の `normal` 詰めなので、`normal` を書いても no-op。既定と違う値（`space-all` で詰めを切る等）を選ぶ要求は TOMBO に無い → **標準の既定に委ねる**（W3C の作法）。
- **`font-feature-settings: "palt"`**。フォント依存で全角すべての字幅を詰める重い手法。通常 letter-spacing での再調整が要り、ブラウザ自前の約物詰め（`text-spacing-trim: normal`）とも競合。非標準の代替路であり不採用。
- **`text-spacing` shorthand**。未実装（宣言ごと落ちる）。longhand `text-autospace` を使う。
- **`@supports` ゲート**。未対応エンジンは未知プロパティを無視 → ベタ組みへ degrade（破綻しない）ので不要。
- **`.tombo-mono` / ラベル系の個別除外**。これらは概ね純ラテンで autospace が発火しないか、発火しても望ましい八分アキになる。実害が出たら follow-up。

## 設計判断（ブレインストーミングでユーザー承認済み）

1. **手打ちスペースを剥がして `text-autospace` に置き換える**（ユーザー承認済み）。手打ちスペースは尊重される＝剥がさないと autospace は一切効かず、examples が機能の実演にならない。剥がすと対応ブラウザは八分アキ（手打ちの 1/3 em より締まって精緻）、非対応は当面ベタ組み（判読可・日本語組版では普通）、両エンジンが実装した時点で**内容を触らず自動で八分アキに揃う**。これが進歩的強化の筋（[[tombo-direction]] は `text-autospace` を「PE と組むべき partial impl」として名指ししている）。代償は今日の Safari/Firefox で和欧がベタ組みになること——破綻ではなく judicious な後退。
2. **約物側は標準の既定に委ねる（`palt` も明示 trim もやらない）**。W3C の作法に照らすと、`text-spacing-trim` の標準既定 `normal`（推奨詰め）が既に効いており、明示は no-op、`palt` はやり過ぎ。和欧混植の核は `text-autospace` の一点なので、v0.12.0 はそこに絞る。
3. **`text-autospace` は継承プロパティ**。`body` で有効化すると子孫すべて（コードブロック含む）に継承する。ソース（逐語）を再スペースしてはいけないので、既存の `code, kbd, samp, pre` セレクタ（tombo.css:122）に合わせて明示的に `no-autospace` へ戻す。
4. **新色ゼロ・トークン/クラスの増減ゼロ**。挙動の追加のみ。**contrast gate は構造的に無関係**（37 PASS 維持）。consumer にとっても安全——手打ちスペースは尊重され二重にならず、ベタ和欧だけが対応ブラウザで精緻化する。

## 設計（CSS）

`@layer tombo.base` の既存宣言に追記する。層順・トークン・その他の base 規則は不変。

```css
@layer tombo.base {
  /* …既存の body 宣言に text-autospace を追加… */
  body {
    /* …既存プロパティ… */
    text-autospace: normal;   /* 和欧の境界に八分アキ(1/8 em)を opt-in。CSS Text L4。
                                 非対応エンジンは無視 → ベタ組みへ degrade(破綻せず) */
  }

  /* …既存の `code, kbd, samp, pre { font-family… }`(line 122)に text-autospace を追加… */
  code, kbd, samp, pre {
    /* …既存プロパティ… */
    text-autospace: no-autospace;  /* 逐語/ソースは再スペースしない(継承の明示リセット) */
  }
}
```

- `text-spacing-trim` は宣言しない（標準既定 `normal` の約物詰めがそのまま効く）。
- vendor prefix 不要（Chrome 133+ は unprefixed）。`@supports` 不要（graceful degrade）。

## examples 移行

和欧境界の手打ち半角スペースだけを剥がす。**剥がさないもの**を明確化する:

- **剥がす**: 和文↔ラテン/数字の境界（`12px のブラケット`→`12px のブラケット`、`OpenAPI 定義`→`OpenAPI定義`、`8 文字以上`→`8文字以上` 等）。
- **剥がさない**: ラテン語内のスペース（`NOTE — 001`、`M PLUS 2`、英文）、約物・ダッシュ周りのスペース（`—` の前後）、コード/コマンド内の意味あるスペース（`composer require …`）、`.tombo-mono` の数式（`≥ 8.2` 等、演算子まわりの空白）。
- 対象ファイル: `examples/docs.html`, `examples/app.html`, `examples/components.html`, `examples/lp.html`, および `README.md` のマークアップ・スニペット中の該当箇所。

移行は目視 + 実ブラウザで、対応ブラウザに八分アキが乗り、剥がし過ぎ（本来必要なラテン内スペースの除去）が無いことを確認する。

## docs / version

- **README**: `## Japanese typography` 節を追加。和欧オートスペース（`text-autospace: normal` を base で opt-in、逐語は除外）、進歩的強化（対応ブラウザは八分アキ／非対応はベタ組み／将来自動で揃う）、手打ちスペースを入れない作法を説明。
- **components.html**: 和欧混植の短い note。
- **バナー / pins**: tombo.css:1・tombo.js:1 を `v0.11.0 → v0.12.0`、README の3つの vendoring pin を `v0.12.0` へ。

## 検証（JS テストランナー無し — computed-style + 実測 + screenshots）

1. **computed-style（chrome-devtools）**: `body` の `text-autospace` = `normal`、`code/kbd/samp/pre` = `no-autospace`。
2. **実測（chrome-devtools）**: examples の和欧境界で、剥がした後に八分アキ（境界あたり 1/8 em ≒ font-size×0.125）が乗ることを幅計測で確認。コードブロックは八分アキが乗らない（`no-autospace`）ことを確認。
3. **screenshots — 両テーマ**: 4 examples を `tombo`（昼）/ `hotaru`（夜）で。剥がし過ぎ（ラテン内スペースの喪失）・詰まり過ぎが無いこと、コード/ラベルが従来どおりであることを確認。
4. `python3 scripts/check_contrast.py` → 全 PASS（色不変）。`node --check tombo.js` clean（tombo.js はバナーのみ）。
5. **非対応の degrade 確認**: `text-autospace` を無効化した状態（≒非対応エンジン）でベタ組みになり破綻しないことを確認（media/プロパティ切替 or DevTools）。

## References

- CSS Text Module Level 4 — `text-autospace`: <https://www.w3.org/TR/css-text-4/#text-autospace-property>
- MDN — `text-autospace`: <https://developer.mozilla.org/en-US/docs/Web/CSS/text-autospace>
- MDN — `text-spacing-trim`: <https://developer.mozilla.org/en-US/docs/Web/CSS/text-spacing-trim>
- Chrome for Developers — new i18n CSS features: <https://developer.chrome.com/blog/css-i18n-features>

関連: [[tombo-overview]], [[tombo-direction]], [[tombo-roadmap]]。
