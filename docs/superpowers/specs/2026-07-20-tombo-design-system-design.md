# TOMBO — wadakatu Design System 設計仕様

- Status: Draft(ユーザーレビュー待ち)
- Date: 2026-07-20
- Author: wadakatu + Claude(ブレインストーミングによる共同設計)

## 1. 目的とスコープ

wadakatu が作るすべての Web プロダクト — OSS ドキュメントサイト、Web アプリケーション、LP、ポートフォリオ — に適用する個人デザインシステム。目標は「**デザインだけを見て wadakatu 製だと認知される**」こと。

- 個人的趣味のモチーフ(写真・HHKB 等)は使わない。認知は純粋にデザイン言語の反復で獲得する
- 少数の署名要素を全プロダクトで執拗に反復する(認知獲得の定石)
- 同じ言語を「音量」を変えて鳴らす: ドキュメントでは静かに、LP では最大音量で

### スコープ外(v1)

Figma キット / JS コンポーネント / React・Vue ラッパー / アイコンセット(ロゴ以外)/ npm 公開。これらは v1 の CSS が安定してからの follow-up。

## 2. 命名

| 名前 | 役割 | 由来 |
|---|---|---|
| **TOMBO** | システムの傘(リポジトリ・呼称・CSS プレフィックス) | ① 印刷の「トンボ」= 版の見当合わせマーク。「すべてを測る」の憲法を名乗る ② 蜻蛉 = 前にしか飛ばない「勝ち虫」。wadakatu の *katu(勝)* が名前に埋まる ③ 十字+翅二対で幾何学ロゴが描ける |
| **tombo** | ライトテーマ名(昼の図面、デフォルト) | 同上 |
| **hotaru** | ダークテーマ名(夜の図面) | 蛍。「夜、計器は蛍になる」— green の増光は文字通りの蛍光(ユーザー発案) |

構造は catppuccin の flavors と同型: 傘は TOMBO ひとつで認知を分散させず、テーマは `data-theme="tombo" | "hotaru"` で切り替える。

## 3. 憲法(3 ヶ条)

1. **すべてを測る** — 要素は寸法線・目盛・通し番号とともに置かれる。「測られた上でそこにある」精度の気配が紙面の空気を作る
2. **銘は等幅** — 数字・ラベル・索引・単位はすべてモノスペース。本文は静かなサンセリフで組み、計器の部分だけが等幅で光る
3. **朱は現在地** — 赤は「いまここ」を指す 1px〜2px の線にだけ許される。面に塗った瞬間、それは朱ではなくただの赤になる

## 4. 署名要素(6 つの指紋)

全プロダクトで反復する。これが「wadakatu 製」の認知を作る本体。

| ID | 名前 | 適用箇所 | 実装 |
|---|---|---|---|
| S-01 | トンボ(四隅マーク) | カード・図版・画像・LP ヒーローの枠 | 角 12-14px、1.5px 罫、ink 色 opacity .75-.85。`::before/::after` または専用 span |
| S-02 | 寸法線 | 区切り(hr 代替)・見出し下・図版注記 | 両端 1px 縦罫 + 中央横罫 + mono ラベル(`section — 02 / margin: 96px` 等) |
| S-03 | 目盛 | 箇条書きの点・進捗・グラフ軸 | リスト: 12px/1.5px の green 横線。ルーラー: 10% 刻み目盛背景 + ink 基線 + green 帯 + 朱の現在値線 |
| S-04 | 通し番号 | 見出し(`02 —`)・図版(`FIG. 04-1`)・注記(`NOTE 001`)・リリース(`REV 2026.07.20`) | mono、green または faint。CSS カウンタで自動採番可 |
| S-05 | 朱の現在地 | アクティブタブ・ナビ現在地・TOC 現在節・ルーラー現在値・callout 左罫 | 1.5-2px の shu 線。面塗り・本文文字は禁止(夜の小ラベルのみ AA を満たすため許可) |
| S-06 | 方眼 | 背景。音量で濃度が変わる | LP: ヒーロー全面 / docs: 余白のみ / app: なし。夜は濃度半減 |

## 5. 色

トークンプレフィックスは `--tombo-`。テーマで値だけが入れ替わる。

### tombo(昼の図面)

| トークン | 値 | 用途 |
|---|---|---|
| paper | `#F2F4EF` | ページ背景(緑がかった図面紙) |
| surface | `#FAFBF8` | カード・パネル(+1 段) |
| ink | `#1A211D` | 本文・主要罫線 |
| ink-sub | `#4C5650` | 補助テキスト |
| ink-faint | `#667069` | 注記・番号 |
| hairline | `rgba(26,33,29,.16)` | 罫線 |
| grid | `rgba(26,33,29,.07)` | 方眼 |
| green | `#0E5A47` | ブランド・インタラクティブ(リンク・ボタン・目盛) |
| shu | `#D8442B` | 現在地の線のみ |

昼に raised(+2 段)はない(純白が禁止のため紙の明度に余地がない)。昼の +2 段は surface + 1.5px ink 罫で表現する。

### hotaru(夜の図面)

| トークン | 値 | 用途 |
|---|---|---|
| paper | `#131714` | ページ背景(緑がかった墨) |
| surface | `#1A201C` | +1 段 |
| raised | `#212824` | +2 段 |
| ink | `#E5EBE6` | 本文(月光色) |
| ink-sub | `#9AA69F` | 補助テキスト |
| ink-faint | `#808D86` | 注記・番号 |
| hairline | `rgba(229,235,230,.14)` | 罫線 |
| grid | `rgba(229,235,230,.05)` | 方眼(昼の約半分) |
| green | `#4FC2A2` | 計器の増光 = 蛍光 |
| shu | `#E5654C` | 現在地の線のみ |

### 状態色(アプリ音量でのみ解禁)

| 状態 | 昼 | 夜 | 備考 |
|---|---|---|---|
| success | `#2C7A4B` | `#57B98A` | brand green とは彩度・用途で区別 |
| warn | `#B07818` | `#D9A441` | |
| error | `#A6301C`(臙脂) | `#D06A5A` | **面塗り可**。朱(線)とは太さと役割で区別 — 朱=現在地、臙脂=失敗 |

### コントラスト実測値(WCAG 2.1、scripts/check_contrast.py の全 28 ペアと同期)

| ペア | 比 | 判定 |
|---|---|---|
| ink / paper(昼) | 14.82 | AAA |
| ink-sub / paper(昼) | 6.88 | AA |
| ink-faint / paper(昼) | 4.64 | AA |
| green / paper(昼) | 7.37 | AAA |
| shu / paper(昼) | 3.97 | 非テキスト 3:1 PASS(線専用のため設計通り) |
| on-green / green(昼) | 7.37 | AAA |
| error / paper(昼) | 6.19 | AA |
| success dot / paper(昼) | 4.75 | 非テキスト 3:1 PASS |
| warn dot / paper(昼) | 3.42 | 非テキスト 3:1 PASS |
| callout-label / paper(昼) | 6.19 | AA |
| ink / surface(昼) | 15.81 | AAA |
| ink-sub / surface(昼) | 7.34 | AAA |
| ink-faint / surface(昼) | 4.95 | AA |
| code-faint / code-bg(昼) | 4.84 | AA |
| ink / paper(夜) | 14.96 | AAA |
| ink-sub / paper(夜) | 7.18 | AAA |
| ink-faint / paper(夜) | 5.23 | AA |
| green / paper(夜) | 8.25 | AAA |
| shu / paper(夜) | 5.43 | AA(夜のみ小ラベル可) |
| on-green / green(夜) | 7.70 | AAA |
| error / paper(夜) | 5.08 | AA |
| success dot / paper(夜) | 7.51 | 非テキスト 3:1 PASS |
| warn dot / paper(夜) | 8.05 | 非テキスト 3:1 PASS |
| callout-label / paper(夜) | 5.43 | AA |
| ink / surface(夜) | 13.70 | AAA |
| ink-sub / surface(夜) | 6.57 | AA |
| ink-faint / surface(夜) | 4.79 | AA |
| code-faint / code-bg(夜) | 4.60 | AA |

「朱は面に塗らない・文字にしない」の掟が、そのまま WCAG 非テキスト基準の保証になる。

### 禁止事項

- `#000` / `#FFF` の使用(図面はあくまで紙)
- 朱の面塗り・朱の本文文字
- ドロップシャドウ・ぼかし(昼夜とも。階層は面の明度 1 段 + 罫線で作る)

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
- 配信: Google Fonts(M PLUS 2 は unicode-range 分割)。フォールバック: `'Instrument Sans', 'M PLUS 2', system-ui, sans-serif` / `'M PLUS 2', system-ui, sans-serif` / `'Martian Mono', ui-monospace, SFMono-Regular, monospace`

## 7. レイアウト・形状

- 基本単位 4px。space token `--tombo-space-{4,8,12,16,24,32,48,72,96}`（24 以上は 24px 方眼セルの倍数）。方眼セルは 24px 固定、セクション律動は docs 72px（3 セル）/ LP 96px（4 セル）。縦リズムは `.tombo-flow`（owl セレクタ + `--tombo-flow-space`、既定 1 セル）で管理する
- **〜v0.3(廃止、下の v0.4 契約に置換済み)**: 本文最大幅 62ch(docs)。shell(コンテンツ列)は `--tombo-shell-max` = 1100px で、**1600px 以上で 1280px** に段階拡大(消費側は `max-width: var(--tombo-shell-max, 1100px)` で追随)
- **v0.4 以降 — 用途別コンテナスケール(2026-07-22)**: `.tombo-shell` 1 クラス + `--tombo-shell-{reading,default,wide}` = 65ch / 1280px / 1792px、ガターは `clamp(20px, 3.25vw, 64px)`。ページ幅は `--tombo-shell` に **`:root` で一度だけ**代入する(`<body>` 以下だと `<body>` に載る `.tombo-gutters` の方眼が追従しない)。`reading` だけ `ch`(measure は組む書体を追う必要がある)、`default`/`wide` は px 型スケールに合わせて px。shell は border-box なので `--reading` の外寸はガター 2 本分を足す(足さないと実測 51.9ch になる)。`.tombo-gutters` の幅も shell 外側の余白 + ガターで本文の端に一致させる。コンテナのブレークポイントは廃止 — `max-inline-size` と clamp() で連続。旧 62ch は `--tombo-shell-reading` に統合。`--tombo-shell-max` は 0.4〜0.6 の間 alias として存続したが **値が 1100px → 1280px に変化**し、**v0.7.0 で削除**
- 広幅(1600px 以上)では余白を計器化する: `.tombo-gutters` の方眼が `--tombo-grid-bold`(昼 .13 / 夜 .09)に濃くなり、ビューポート四隅に見当マーク(ink、opacity .45)が出る。印刷でトンボが住むのは版面外 — 画面ではビューポートの縁がそれにあたる(2026-07-22 追加)
- 角丸: 原則 0(図面に丸はない)。例外: コードブロック等の大型パネル 6px、チップ 99px
- 罫線: 通常 1px hairline / 強調 1.5px ink / 現在地 2px shu

## 8. モーション(計器の動き)

- 120-180ms、ease-out(`cubic-bezier(0.2, 0, 0, 1)`)。計器の針のように速く正確に
- 許可: ルーラー・針の伸縮、明度遷移、朱の現在地線の移動
- 禁止: バウンス・パララックス・長い演出
- `prefers-reduced-motion` で全遷移を無効化

## 9. 音量ダイヤル

| 署名要素 | DOCS | APP | LP |
|---|---|---|---|
| 方眼 | 余白のみ | なし | ヒーロー全面 |
| トンボ | 図版のみ | 計器カードのみ | ヒーロー枠 + 図版 |
| 寸法線 | hr 代替 | なし | 見出し下 + 注記 |
| 通し番号 | 見出し・注記 | REV 表記 | FIG. 番号 |
| 朱の現在地 | TOC・タブ | ナビ・計器 | キッカー先頭の一画 |
| ロゴ尾部の発光(hotaru) | なし | なし | ヒーローのみ許可 |

## 10. ダークモード(hotaru の掟 6 ヶ条)

1. 影を使わない — 階層は面の明度 1 段(paper → surface → raised)と罫線
2. 方眼は半減 — 発光する画面では同じ「気配」に物理量を下げる
3. 計器は増光 — green #0E5A47 → #4FC2A2。夜のコックピットの計器
4. 朱は変わらず線 — 役割は昼と完全に同一
5. コードは沈めない — 昼はコードブロックだけ夜になるが、夜は罫線の枠のみ。「黒の上の黒」を作らない
6. 純黒・純白の禁止

切替: `prefers-color-scheme` をデフォルトに、`[data-theme]` で明示上書き。

## 11. コンポーネント(v1 インベントリ)

button(primary / secondary / ghost)、link(green 下線)、tabs(朱の現在地)、sidebar-nav / TOC(朱の現在節)、code block(行番号・言語バー・COPY)、callout(NOTE / WARN、朱の左罫 + 通し番号)、table(mono ヘッダ・hairline 罫)、chip / status(● + mono)、metric card(mono 大数字 + ルーラー)、寸法線 hr、目盛リスト、footer(REV 表記 + ロゴ刻印)

各コンポーネントは docs / app / LP の三音量で崩れないことをサンプルページで確認する。

## 12. 実装アーキテクチャ

- **純 CSS・ゼロ JS・ゼロ依存**。`tombo.css` 一枚(内部は `@layer tombo.tokens, tombo.base, tombo.components, tombo.utilities`)
- トークンは CSS カスタムプロパティ `--tombo-*`。テーマは `:root` と `[data-theme="hotaru"]` で値を入れ替え
- リポジトリ構成(v1):

```
tombo/
├── tombo.css              # 本体(tokens + base + components)
├── examples/              # docs / app / LP の三音量サンプル
├── scripts/check-contrast.py   # コントラスト検証(CI 可)
├── docs/superpowers/specs/     # 本仕様書
└── README.md              # TOMBO 自身も TOMBO で書かれた見た目にする(将来)
```

- 配布: GitHub リポジトリ + jsDelivr CDN 参照。npm 公開は follow-up
  - **2026-07-22 訂正**: リポジトリを private 化した時点で jsDelivr の `gh` エンドポイントは 404 になっており、CDN 配布は最初から成立していなかった(既存タグ v0.3.2 でも 404 を実測)。実際の配布はタグからの vendor(消費側で sha256 をピン留めして CI 検証)。公開予定が立つまでこれが唯一の経路
- 適用先の実装形態(Astro / Laravel Blade / Vue)を問わず `<link rel="stylesheet">` 一枚で導入できること

## 13. 検証方針

- 全ビジュアル変更は chrome-devtools のスクリーンショットで確認(ユーザーのグローバルルール)
- `scripts/check-contrast.py` が全色ペアの WCAG 基準を検証し、しきい値未満で exit 1(CI に組み込み可能)
- examples/ の三音量サンプルを昼夜 × 3 画面 = 6 状態で目視確認

## 14. 決定記録

- 3 方向案(朱筆 / 計測 / 一色)からユーザーが **B: 計測** を選択
- 没案 A の魂(朱)を「朱は現在地」の掟として B に移植 — 深緑の計器 UI + 朱の 1px は既存システムに存在しない組み合わせで、これが最強の指紋
- ターミナル風(既存サイトの路線)は飽和のため単独継承せず、mono ラベルの「計器」文法として昇華
- システム名 TOMBO はユーザー発案。ダークテーマ名 HOTARU もユーザー発案、傘 + flavors 構造は Claude 提案でユーザー承認待ち
