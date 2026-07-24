# TOMBO — GitHub Pages 紹介サイト 設計仕様

- Status: Approved(ブレインストーミングでユーザー承認済み)
- Date: 2026-07-24
- Author: wadakatu + Claude(ブレインストーミングによる共同設計)
- Issue: #18(依存: #17 → v0.14.1 で解消済み)

## 1. 目的とスコープ

リポジトリの public 化に伴い、TOMBO のデザインシステム紹介ページを GitHub Pages で公開する。目標は 2 つ:

1. **「wadakatu 製だとわかる」** — tombo.css 自身を LP ボリュームでドッグフーディングし、ページそのものが 6 署名要素の実演になる
2. **入口の一本化** — Quick start・リファレンス(docs/)・ライブデモ(examples/)への導線を 1 ページに束ねる

サイトは tombo.css の「最初の公式コンシューマー」として振る舞う: レイアウトはコンシューマー側 CSS(`assets/site.css`)に書き、tombo のトークン・クラスだけを使う。

### スコープ外

- og:image / social preview 画像の生成(follow-up)
- カスタムドメイン
- examples/ 自体の改修

## 2. 配信構成

- **GitHub Pages: main ブランチ / ルートから配信**(Actions ワークフロー追加なし)
- `.nojekyll` をルートに置き Jekyll 処理を無効化(`ja/` ディレクトリや `_` なしでも安全側に倒す)
- 副産物として `examples/*.html` がそのままライブデモ URL になる
- リポジトリの `homepage` フィールドを `https://wadakatu.github.io/tombo/` に設定

## 3. ファイル構成

| ファイル | 役割 |
|---|---|
| `index.html` | 英語主体 + 日本語の銘(README と同じ声) |
| `ja/index.html` | 日本語主体(銘・ラベルは共通) |
| `assets/site.css` | 両ページ共有のレイアウト CSS。tombo トークンのみ参照、`@layer` 外(コンシューマーの流儀) |
| `.nojekyll` | Jekyll 無効化(空ファイル) |

スタイルシートは各ページから相対で読む: `index.html` は `tombo.css`、`ja/index.html` は `../tombo.css`(site.css も同様)。tombo.js・フォント `<link>`・inline テーマスニペットは examples と同じ構成。

## 4. ページ構成(両言語共通、LP ボリューム)

1. **トップバー** `.tombo-topbar` — brand「TOMBO」、右肩 `.meta` に `REV v0.14.1`・言語リンク(日本語 ⇄ English)・`.tombo-themes` トグル(hidden で出荷、tombo.js が点灯)
2. **ヒーロー** `tombo-vol-lp tombo-glow tombo-corners`(方眼フルブリード、夜は glow)— `.tombo-logo`(mark)+ ワードマーク、`.tombo-kicker`(朱の第一画)、`.tombo-display` タグライン(EN: "The mark that measures." / JA: 「測ってから、置く。」)、`.tombo-dim` + `.tombo-dimlab`、CTA は `<a class="tombo-btn">`(primary: Quick start へ / secondary: GitHub へ)。脇に `.tombo-metric` で **実測 gzip サイズを `.tombo-ruler` 表示**(値はサイズ予算ゲートと同じ実測値を手で転記し、コメントで出典を示す)
3. **三原則** — `.tombo-sections` の通し番号 3 カード(`.tombo-corners`)。見出しは日本語の銘(すべてを測る / 銘は等幅 / 朱は現在地)、本文は EN / JA
4. **6 つの署名要素** — S-01〜S-06 を「説明ではなく実物」で: 寸法線を実際に引き、`.tombo-ticks` リストを刻み、`.tombo-ruler` に朱の現在値を置き、`[aria-current]` タブに朱を灯し、`.tombo-corners` カードと方眼スウォッチを見せる
5. **テーマとトークン** — tombo / hotaru の説明 + 主要トークンのスウォッチ(`var(--tombo-*)` を直接描画するので理論値と実物が乖離しない)。「トップバーのトグルで切り替え、選択は再訪時も残る(tombo.js)」の一文
6. **Quick start** — `.tombo-code` + コピーボタンで vendoring 3 コマンド(`show v0.14.1:` ピン付き)+ フォント `<link>`。README の該当節と同内容
7. **Volume dial** — 同じ言語を 3 つの音量で: docs / app / lp のライブ examples へのリンクカード + components カタログ
8. **フッター** `.tombo-footer` — MIT / GitHub / vendoring 方針の一文 / wadakatu

## 5. i18n

- `/index.html` は `<html lang="en">`、日本語の銘には `lang="ja"` を付与
- `/ja/index.html` は `<html lang="ja">`(等幅ラベルの Latin はそのまま)
- 相互に `<link rel="alternate" hreflang="…">` を張る(en ⇄ ja + `x-default` = en)
- 切り替えはトップバー `.meta` 内の素の `<a>`(JS 不要)

## 6. ゲート拡張(check_banner.py)

サイトの Quick start にもバージョンピンが入るため、リリース時の bump 漏れを CI で検出する:

- README.md は従来どおり **ちょうど 3 ピン** を要求
- `index.html` / `ja/index.html` からも `show vX.Y.Z:` を収集し(各ちょうど 3 ピン)、**全ピン + 両バナーが同一バージョン** であることを assert
- 出力の versions 表に site の行を追加

## 7. 検証

1. `npm run check` 全ゲート green(拡張後の banner ゲート含む)
2. chrome-devtools で **両テーマ × 両言語**(4 通り)のスクリーンショット確認 + 狭幅(375px)での折り返し確認
3. リンク検査: 言語リンク・docs/examples への相対リンク・hreflang の解決
4. tombo.js なしでも全文が読めること(`.tombo-themes` が hidden のまま、コピーボタン無し、それ以外は完全)
5. マージ後: Pages 反映を待って https://wadakatu.github.io/tombo/ と /ja/ をライブで再確認、`homepage` フィールド設定

## 8. リリース

- ブランチ `feature/pages-site` → PR(この spec を含む)→ CI green → rebase-merge
- サイトは main を直接配信するためタグ付けは不要(Quick start のピンは最新タグ v0.14.1 を指す)
