---
sidebarDepth: 4
author: フューチャー株式会社
layout: home
hero:
  name: "Web API<wbr>設計ガイドライン"
  tagline: Web API Design Guidelines
  actions:
    - theme: brand
      text: WebAPI設計ガイドライン
      link: ./web_api_guidelines.md
---

## はじめに

本ガイドラインはWeb APIを利用する開発者向けに、RESTライクなWeb APIの主な設計手法をまとめ、システム開発プロジェクトにおける設計のベースラインを提供するために作成された。本ガイドラインを用いることで、開発チームは何を設計すべきか、どのような判断を下すべきかについて共通認識を得ることができる。また、設計の属人性を軽減させ、ナレッジやツールの横展開を容易にすることを狙いにしている。

::: warning 免責事項

- 有志で作成したドキュメントである。フューチャーには多様なプロジェクトが存在し、それぞれの状況に合わせて工夫された開発プロセスや高度な開発支援環境が存在する。本ガイドラインはフューチャーの全ての部署 / プロジェクトで適用されているわけではなく、有志が観点を持ち寄って新たに整理したものである
- 相容れない部分があればその領域を書き換えて利用することを想定している。プロジェクト固有の背景や要件への配慮は、ガイドライン利用者が最終的に判断すること。本ガイドラインに必ず従うことは求めておらず、設計案の提示と、それらの評価観点を利用者に提供することを主目的としている
- 掲載内容および利用に際して発生した問題、それに伴う損害については、フューチャー株式会社は一切の責務を負わないものとする。掲載している情報は予告なく変更する場合がある

:::

## 前提条件

本ガイドラインの前提は以下の通り。

- gRPC、JSON-RPC、SOAP、GraphQLなど、RPCやグラフ志向ではなく、REST志向のWeb API構築が対象である
- 業務システム向け Web API 提供である（サードパーティ向けに広く開発する Web API ではなく、限られたクライアントやシステムと連携すること。いわゆる、LSUDs（Large Set of Unknown Developers）ではなく、SSKDs（Small Set of Known Developers）が対象である
- AWSなどのクラウド環境で構築される

また、利用者は以下の技術を理解しているとし、本ガイドラインではこれらについて解説はしない。

- 基礎的なHTTPの知識
- 基礎的なRESTの知識

また、本ガイドラインの適用範囲は、Web APIのサーバーサイドの設計についてまとめる。クライアントサイドについては対象外とする。

## 参考資料

- [Web API 設計のベスト プラクティス \- Azure Architecture Center](https://learn.microsoft.com/ja-jp/azure/architecture/best-practices/api-design)
- [Web API 実装 \- Best practices for cloud applications](https://learn.microsoft.com/ja-jp/azure/architecture/best-practices/api-implementation)

## 謝辞

このアーキテクチャガイドラインの作成には多くの方々にご協力いただいた。心より感謝申し上げる。

- **作成者**: 真野隼記、佐々木伸悟、武田大輝、宮崎将太、澁川喜規、佐藤尭彰
- **レビュアー**: 辻大志郎、合田飛

## Articles

- 2025.05.13 [Web API設計ガイドラインを公開しました](https://future-architect.github.io/articles/20250513b/)

<div class="next-page-nav">

次のページ: [Web API設計ガイドライン](./web_api_guidelines.md)

</div>
