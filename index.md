---
layout: home
title: アーキテクチャ設計ガイドライン
hero:
  name: Future <wbr>Architecture Guidelines
  tagline: '<span style="white-space: nowrap">フューチャー株式会社の有志が作成する<wbr>良いアーキテクチャを実現するための設計ガイドライン</span>'
  actions:
    - theme: brand
      text: Webフロントエンド
      link: ./documents/forWebFrontend/
    - theme: brand
      text: WebAPI
      link: ./documents/forWebAPI/
    - theme: brand
      text: バッチ
      link: ./documents/forBatch/
    - theme: brand
      text: I/F
      link: ./documents/forIF/
    - theme: brand
      text: メール
      link: ./documents/forMail/
    - theme: brand
      text: DB
      link: ./documents/forDB/
    - theme: brand
      text: AWS
      link: ./documents/forAWS/
    - theme: brand
      text: Terraform
      link: ./documents/forTerraform/
    - theme: brand
      text: データマネジメント
      link: ./documents/forDataManagement/
    - theme: alt
      text: Gitブランチフロー
      link: ./documents/forGitBranch/
    - theme: alt
      text: Markdown設計書
      link: ./documents/forMarkdown/
    - theme: alt
      text: コードレビュー
      link: ./documents/forCodeReview/
    - theme: alt
      text: Slack利用
      link: ./documents/forSlack/
features:
  - title: Design
    details: 多くの開発者が関わるシステム開発において、一貫性のある設計を行うことは何より重要です。しかし、従来はどのような設計項目が存在するかすらも各人の経験則に近い形でしか蓄積されていませんでした。そこで有志メンバーがボトムアップ的に主要な設計項目を集め、設計パターンや推奨方式をまとめました。
  - title: Agility
    details: 世の中のIT技術の進歩は著しく、過去のベストプラクティスが今のアンチパターンとされることも珍しくありません。本規約ではこうした変化に対応できるよう、設計標準を公開することでフィードバックを集め、民主主義的に内容を改善し続けること目指します。
  - title: Enterprise
    details: 趣味で開発されたホビープロダクトと比べ、エンタープライズ領域では高度なセキュリティや保守運用性などの非機能要件が重視されます。技術の流行や開発のしやすさといった以外の視点に気がつくきっかけにもなるでしょう。
pageClass: standards-home
---

<br>

本ガイドラインに記載された設計上の論点や推奨案を知ることで、開発チームは意思決定や合意形成のためのベースラインを得ることができます。

また、本書には次のような目的があります。

- **車輪の再発明を防ぐ**: システム間で差異が出にくい設計事項のベストプラクティスを提供します。これにより、設計者が悩むポイントを軽減し、本当に必要な設計に集中できるようになります
- **設計品質の標準化**: プロジェクト間での設計品質のばらつきや属人性をなくし、品質を底上げします。また、ナレッジやツールの横展開を容易にします
- **リスクの低減**: 非機能要件（可用性、性能、セキュリティ、保守運用性、移行性）や法令遵守などに関する考慮漏れを防ぎ、安定したシステム稼働を実現します
- **知見の共有**: システム設計に関する体系的な知識を共有することで、チーム内・組織内での知見の共有を促進し、成長サイクルを回していきます

<br>

::: tip 答えを提供するのではなく、考えるための土台を提供する

本ガイドラインは、設計上の "答え" を提供するためではなく、考えるための土台を提供する目的で作成されています。記載内容に必ず従うことは求めておらず、プロダクト固有の背景や要件に対して相容れない部分があれば、上書きして利用することを想定しています。そのために、設計案を複数の観点で評価するとともに、推奨案の選定理由をなるべく明記するようにしています。
:::

## 関連コンテンツ

- [コーディング規約](https://future-architect.github.io/coding-standards/)
- [仕事ですぐに使えるTypeScript](https://future-architect.github.io/typescript-guide/)

<br>

[![GitHub last commit](https://img.shields.io/github/last-commit/future-architect/arch-guidelines.svg)](https://github.com/future-architect/arch-guidelines)
[![GitHub stars](https://img.shields.io/github/stars/future-architect/arch-guidelines.svg?style=social&label=Stars&logo=github)](https://github.com/future-architect/arch-guidelines/stargazers)

## License

[![CC-By-4.0](https://licensebuttons.net/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/deed.ja)

<FutureStar kind="1"/>
<FutureStar kind="2" />
