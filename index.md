---
layout: home
title: アーキテクチャ設計ガイドライン
hero:
  name: Future <wbr>Architecture Guidelines
  tagline: '<span style="white-space: nowrap">フューチャー株式会社の有志が作成する<wbr>良いアーキテクチャを実現するための設計ガイドライン</span>'
  actions:
    - theme: brand
      text: Webフロントエンド設計
      link: ./documents/forWebFrontend/
    - theme: brand
      text: WebAPI設計
      link: ./documents/forWebAPI/
    - theme: brand
      text: バッチ設計
      link: ./documents/forBatch/
    - theme: brand
      text: I/F設計
      link: ./documents/forIF/
    - theme: brand
      text: DB設計
      link: ./documents/forDB/
    - theme: brand
      text: AWS設計
      link: ./documents/forAWS/
    - theme: brand
      text: Terraform設計
      link: ./documents/forTerraform/
    - theme: brand
      text: データマネジメント設計
      link: ./documents/forDataManagement/
    - theme: alt
      text: Gitブランチフロー
      link: ./documents/forGitBranch/
    - theme: alt
      text: Markdown設計ドキュメント
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

本ガイドラインを用いると、開発チームは考慮すべき設計事項と推奨案を知ることで、意思決定や合意形成のためのベースラインを得ることができる。

また、ガイドラインには次の目的がある。

- **車輪の再発明を防ぐ**: システム間で差異が出にくい設計事項のベストプラクティスを提供し、設計者が悩むポイントを軽減し、真に必要な設計に集中できるようにする
- **設計品質の標準化**: プロジェクト間で設計品質のばらつきや属人性をなくし、品質を底上げする。また、ナレッジやツールの横展開を容易にする
- **リスクの低減**: 非機能（可用性、性能、セキュリティ、保守運用性、移行性）・法令遵守などに関する考慮漏れを防ぎ、安定したシステム稼働を実現する
- **知見の共有**: システム設計に関する体系的な知識を共有することでチーム内・組織内で知見の共有を促進し、成長サイクルを回す

<br>

[![GitHub last commit](https://img.shields.io/github/last-commit/future-architect/arch-guidelines.svg)](https://github.com/future-architect/arch-guidelines)
[![GitHub stars](https://img.shields.io/github/stars/future-architect/arch-guidelines.svg?style=social&label=Stars&logo=github)](https://github.com/future-architect/arch-guidelines/stargazers)

## License

[![CC-By-4.0](https://licensebuttons.net/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/deed.ja)

<FutureStar kind="1"/>
<FutureStar kind="2" />
