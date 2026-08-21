# arch-guidelines

VitePress で公開する設計ガイドライン集。コンテンツは日本語の Markdown で、文体は「である」調。

## 構成

- `documents/forXxx/` — ガイドライン1本につき1ディレクトリ。扉ページ `index.md`（`layout: home`）と本体 `xxx_guidelines.md` からなる。分量が多いものは章単位で分割する（例: `forNFR/` は overview / knowledge / appendix）
- `index.md` — サイトのトップページ
- `.vitepress/config.mjs` — nav（ヘッダーメニュー）と `links`（サイドバー）の定義
- `docs/` — ビルド成果物。gitignore 済みなのでコミットしない

## 導線は3箇所に登録する

ページを追加したら、次の3箇所を漏れなく更新する。既存の兄弟ドキュメントのディレクトリ名（例: `forPerformanceTest`）で横断 grep すると、登録箇所の全体が確認できる。

1. `index.md` の `hero.actions` — トップページのボタン。設計ドメイン別のガイドライン（Webフロントエンド〜ログ）は `theme: brand`、プロセス・スキル系は `theme: alt`
2. `.vitepress/config.mjs` の `themeConfig.nav` — ヘッダーメニュー。アプリケーション / DB / インフラ / 開発生産性 / はじめての〇〇シリーズ / その他 のいずれかに入れる
3. `.vitepress/config.mjs` の `links` — サイドバー。キーは `/documents/forXxx/`

リンク先は、本体が1ファイルなら本体（`xxx_guidelines.html`）、複数部構成なら扉ページ（`/documents/forXxx/`）を指す。扉ページを指すことで読者が第一部・第二部を選べる。並び順は読者がたどる時系列に合わせる（非機能要件 → 性能テスト）。

## 公開記事へのリンク

ガイドラインの公開記事は、そのガイドラインの `documents/forXxx/index.md` に `## Articles` を設け、謝辞と `<div class="next-page-nav">` の間に置く。

```markdown
## Articles

- 2026.08.19 [テクニカルライティングガイドラインを公開しました](https://future-architect.github.io/articles/20260819a/)
```

ルート `index.md` の `## Articles` は、公開スケジュールや年次振り返りなど横断的な記事のみを載せる。個別ガイドラインの公開記事はここに追加しない。

## 図

本サイトの図は mermaid で書く（` ```mermaid ` を vitepress-plugin-mermaid がレンダリングする）。`documents/forMarkdown/markdown_design_document.md` の PlantUML ブロックは、設計書の書き方として読者に示すサンプルなので mermaid に書き換えない。

## 確認とチェック

- `npm run watch` — 開発サーバー。URL は base 込みの `http://localhost:5173/arch-guidelines/`
- 開発サーバーは SSR なしのため、初期 HTML にリンクが現れない。リンク追加の確認はブラウザで見るか、`npm run build` 後の `docs/` を grep する
- `npm run lint`（prettier + eslint）と `npm run build` が CI の必須チェック（`.github/workflows/ci.yml`）
- `npx textlint <file>` — CI では実行されないが、Markdown を変更したら手元で流す。**`--fix` は使わない**（表記ルールに合った箇所まで機械的に書き換えるため）。表記ルールの正は `.textlintrc` と `prh-choon.yml`（カタカナ長音）

## コミットと PR

- コミットメッセージと PR 本文は日本語で書く
- PR 本文には `Fixes #<issue>`、変更内容、判断した点、確認したことを記載する
- squash merge のため PR ブランチに force-push しない。修正はコミットを積む
