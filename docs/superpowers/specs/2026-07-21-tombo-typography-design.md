# TOMBO タイポグラフィ v0.2 設計書

日付: 2026-07-21
状態: ユーザー承認済み(書体・システム設計とも実文比較の上で選定)
対象: tombo.css v0.2.0(視覚的破壊的変更)。色トークンは無変更。

## 1. 背景と決定経緯

v0.1 のタイポグラフィは「書体の選定」で止まっており、組版システムとして未設計だった(サイズ 13 種がその場決め、和欧混植規則なし、垂直リズムなし)。wadakatu.dev リデザイン着手を機に、**全書体ゼロベース・読者ファースト**で再設計した。

要件(承認済み):

- R1 和文長文の可読性が最優先
- R2 技術文字の判別性(Il1 / 0O / 日時)
- R3 小サイズ耐性 — かつ最小サイズ自体を引き上げる
- R4 配信性能は体験の一部(LCP < 2.5s と両立)
- R5 オープンライセンス限定(TOMBO は OSS サイトにも適用するため)
- R6 昼夜両テーマでの描画耐性(夜の痩せ)
- R7 TOMBO の声(計測・静かな計器)は R1–R6 充足後の決め手

選定方法: 実文サンプル(実ブログ本文・計器ラベル・コード・判別行)を companion で比較。
1 次比較: 和文 5(BIZ UDPGothic / Noto Sans JP / LINE Seed JP / M PLUS 2 / IBM Plex Sans JP)× mono 4(Plex Mono / Martian Mono / JetBrains Mono / Space Mono)× display 4(Archivo / Space Grotesk / Instrument Sans / Inter)+ 家族構成 3。
決勝: D2「IBM Plex 一家統一」 vs D4「計器トリオ(ユーザーの 3 選)」の実ページ丸ごと比較 → **D4 を採用**。

## 2. 三声の書体(確定)

| 声 | 書体 | ウェイト/軸 | 役割 |
|---|---|---|---|
| DISPLAY | **Instrument Sans**(OFL, variable) | 700(サブ 600)。**最大 700 — 900 は存在しない** | 欧文題字・大見出し。字間 -.015em は**この声の欧文専用** |
| BODY | **M PLUS 2**(OFL, variable 100–900) | **本文 450**(強調 500 / 太字・和文見出し 700) | 和文本文・UI 文言・和文見出し。450 は夜の痩せ対策(400 は hotaru で細い) |
| INSTRUMENT | **Martian Mono**(OFL, variable wght 100–800 / wdth 75–112.5) | 銘 400–500(600 は大数字補助)。**コードは wdth 87.5%** | 計器ラベル・数値・索引・コード。大文字 + 字間 .12–.16em は v0.1 を継承 |

フォールバックスタック:

```css
--tombo-font-display: "Instrument Sans", "M PLUS 2", system-ui, sans-serif;
--tombo-font-body: "M PLUS 2", system-ui, sans-serif;
--tombo-font-mono: "Martian Mono", ui-monospace, SFMono-Regular, monospace;
--tombo-w-body: 450;
```

不採用の記録: BIZ UDPGothic(UD 思想は最良だが 2 ウェイト制約と事務的な字面)、Noto Sans JP(可読だが声が無個性)、LINE Seed JP(丸み = 温かみ寄りで計器と不整合)、Plex 一家(静かで上質だが計器の声で D4 に劣後 — ユーザー実見で決定)、JetBrains Mono(判別性は最高クラスだが旧 Matrix サイトの声の継承を避けた)。

## 3. タイプスケール(v0.2 で全コンポーネントが参照)

基数 15px・比おおむね 1.25 を、方眼(24px)の半単位 12px に丸めた実用スケール。**その場サイズの新設は禁止** — 足りなければスケールに段を足す(spec 改訂を伴う)。

| トークン | size / line-height | 書体・ウェイト | 字間 | 用途(移行元) |
|---|---|---|---|---|
| --tombo-text-label | 10.5 / 18 | mono 500 caps | .14em | 計器銘・チップ・フッター(10, 10.5, 11) |
| --tombo-text-note | 12 / 18 | mono 400 | .08em | 寸法ラベル・fig・注記(10.5, 11.5) |
| --tombo-text-code | 12 / 22 | mono 400 wdth 87.5% | 0 | コードブロック(12) |
| --tombo-text-ui | 13 / 24 | body 450–500 | 0 | 表・コールアウト・タブ・ボタン(12, 12.5, 13, 13.5) |
| --tombo-text-body | **15 / 30** | body 450 | 0 | 本文(13.5, 14 — **R3 のサイズ床引き上げ**) |
| --tombo-text-h3 | 19 / 30 | body 700 | 0 | 小見出し(15) |
| --tombo-text-h2 | 23 / 36 | body 700 | 0 | 見出し(20) |
| --tombo-text-h1 | 29 / 42 | body 700 | 0 | ページ題・和文大見出し(28) |
| --tombo-text-metric | 29 / 36 | mono 600 | 0 | 計器の大数字(30, 34) |
| --tombo-text-display | clamp(44px, 6vw, 64px) / 1.1 | display 700 | -.015em | 欧文題字(44–64) |

実装形: 各段は `--tombo-text-<name>`(font-size)と `--tombo-lh-<name>`(line-height)の対トークン(例 `--tombo-text-body: 15px; --tombo-lh-body: 30px;`)。display のみ lh は無単位 1.1。行送りは 6px の倍数に統一し、余白は従来通り 4/8/12/24 の系で方眼と噛み合わせる。

## 4. 和欧混植の規則

1. **和文に負の字間を当てない**。-.015em は Instrument Sans の欧文題字専用。和文見出し(M PLUS 2 700)は字間 0
2. `.tombo-display` は**欧文専用クラス**と明文化(和文が混ざる見出しは h1/h2 の標準スタイルを使う)
3. 本文中の英字・数字・inline code 周辺の欧文は **M PLUS 2 自身のラテン**で組む(別書体を混ぜず、混植の釣り合いを書体内で完結させる)
4. 数値が並ぶ場所(表の数値列・計器・日時)は掟 2「銘は等幅」に従い Martian Mono(等幅ゆえ桁が揃う — tnum 相当を書体構造で担保)

## 5. 配信

Google Fonts(css2)。M PLUS 2 は unicode-range 分割配信のため和文でも初期転送は小さい。読み込みは consumer 側 `<link>`(v0.1 と同じ思想、@import 禁止):

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@600;700&family=M+PLUS+2:wght@450;500;700&family=Martian+Mono:wdth,wght@75..112.5,400..600&display=swap" rel="stylesheet">
```

- ウェイトは上記の必要分のみ(R4)。`display=swap` 維持
- フォールバックは system-ui / ui-monospace(フォント未達でも読める)
- セルフホスト(woff2 同梱)は follow-up issue に切る(本設計の範囲外)

## 6. ワードマーク再制作(決定: b 案)

- C-03 ワードマーク(現 Archivo 900 パス化)を **Instrument Sans 700 で再アウトライン**する(パイプラインは v0.1 で実証済み: fonttools instancer → SVGPathPen)。寸法線・朱の目盛(62%)・viewBox 構成は踏襲
- 昼夜 4 ファイル(assets/logo/tombo-wordmark*.svg)を差し替え。README の `<picture>` はパス不変のため変更不要
- C-01 見当マーク(文字なし)と CSS 刻印 .tombo-logo は無変更

## 7. 移行対象(v0.2.0)

| 対象 | 変更 |
|---|---|
| tombo.css | 書体・ウェイト・スケールのトークン追加、base/components の全サイズ参照書き換え。バナーを v0.2.0 に |
| 本 spec(§6 タイポグラフィ) | メイン spec の §6 を本設計書の内容で全面改稿 |
| examples 4 枚 + components.html | フォント `<link>` 差し替え、ローカル style のサイズをトークン参照へ |
| README | Quick start のフォント `<link>` 差し替え、タイポグラフィ節更新 |
| assets/logo | ワードマーク 2 ファイル再生成(§6) |
| タグ | v0.2.0(色は無変更なのでコントラストゲートは 28/28 のまま) |

## 8. 検証

1. コントラストゲート 28/28 PASS 維持(色無変更の確認)
2. カタログ + 3 examples を昼夜スクリーンショットで全数確認(CLAUDE.md の UI 検証ルール)。特に hotaru での本文 450 の痩せ、Martian Mono 銘の折り返し(横幅増への対処: 幅軸か文言短縮)
3. 15px/30px の和文長文(実ブログ本文相当)を通し読みして R1 を最終確認
4. ワードマーク再生成後、ブラウザ描画でレターフォーム確認(v0.1 と同手順)

## 9. 決定記録

- 全書体ゼロベース・読者ファーストはユーザー指示(2026-07-21)。「TOMBO を見るユーザーのことを考えて選定」
- 1 次比較の A4 / B2 / C3 + 家族 D2 という一見矛盾する 4 選から「幾何学的計器の声 × 家族の統一感」という要求を抽出し、決勝 D2 vs D4 で D4 確定(ユーザー実見)
- 本文 450 と幅軸 87.5% は比較ページ上で実証した運用値
- ワードマーク b 案(再制作)は Claude 推奨をユーザーが承認
- Instrument Sans に 900 が無い制約は承知の上で採用(題字の黒みは 700 + サイズで作る)
