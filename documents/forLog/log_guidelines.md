---
sidebarDepth: 4
title: ログ設計ガイドライン
author: フューチャー株式会社
head:
  - - meta
    - name: keywords
      content: ログ,log
---

<page-title/>

本ガイドラインは、世の中のシステム開発プロジェクトのために無償で提供する。ただし、掲載内容および利用に際して発生した問題、それに伴う損害については、フューチャー株式会社は一切の責務を負わないものとする。また、掲載している情報は予告なく変更する場合があるため、あらかじめご了承ください。

::: warning 免責事項: 有志で作成したドキュメントである

- フューチャーには多様なプロジェクトが存在し、それぞれの状況に合わせて工夫された開発プロセスや高度な開発支援環境が存在する。本ガイドラインはフューチャーの全ての部署／プロジェクトで適用されているわけではなく、有志が観点を持ち寄って新たに整理したものである
- 相容れない部分があればその領域を書き換えて利用することを想定している
  - プロジェクト固有の背景や要件への配慮は、ガイドライン利用者が最終的に判断すること
- 本ガイドラインに必ず従うことは求めておらず、設計案の提示と、それらの評価観点を利用者に提供することを主目的としている

:::

- **対象スコープ**
  - アプリケーションが出力するログ（アプリログ）が対象
  - AWS CloudTrailやVPCフローログといった、クラウドサービスやインフラストラクチャ側で出力されるログは対象外
  - 主にバックエンド領域のログを扱う。フロントエンドのログについても一部言及するが、本ガイドラインの主眼にしない
- **前提条件**
  - **実行環境**: クラウド利用を前提とする。オンプレミス環境で必要となるファイルベースのログローテーションは考慮しない
  - **出力方式**: ログはファイルではなく、標準出力を基本とする

# ログキー命名規則

## 標準的な規約

Elastic Common Schema (ECS) 、OpenTelemetry Semantic Conventionsの2つが有名である。2023年にOpenTelemetry（OTel）にECSが統合された。そのため、OTelが実質的に標準と言える。

- [Announcing the Elastic Common Schema (ECS) and OpenTelemetry Semantic Convention Convergence](https://opentelemetry.io/blog/2023/ecs-otel-semconv-convergence/)

▼OTel Semantic Conventions とECS 比較

| \#             | OpenTelemetry Semantic Conventions                                                                           | Elastic Common Schema (ECS)                                                                        |
| :------------- | :----------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| 説明           | 開発者向けのオブザーバビリティ（トレース、メトリクス、ログの相関）に重点を置く。分散システムの挙動追跡に利用 | セキュリティ分析 (SIEM) と運用分析に重点を置く。豊富なイベント分類語彙、特にセキュリティ分野に強い |
| 構造           | フラットなAttributesとResource                                                                               | ネストされたJSONオブジェクト（論理的にグルーピング）                                               |
| 命名規則       | dot.case (例: service.name)                                                                                  | dot.case (例: service.name)                                                                        |
| タイムスタンプ | timestamp (トップレベル)                                                                                     | @timestamp (トップレベル)                                                                          |
| メッセージ     | body (トップレベル)                                                                                          | message (トップレベル)                                                                             |
| サービス名     | service.name (リソース属性)                                                                                  | service.name (フィールドセット)                                                                    |
| トレースID     | traceId (トップレベル)                                                                                       | trace.id (フィールドセット)                                                                        |

::: tip OTel ログデータ例

```json
{
  "logRecords": [
    {
      "timeUnixNano": "1724737589123456789",
      "observedTimeUnixNano": "1724737589124567890",
      "severityNumber": 17,
      "severityText": "ERROR",
      "body": {
        "stringValue": "Payment processing failed due to insufficient funds"
      },
      "attributes": [
        {
          "key": "http.request.method",
          "value": { "stringValue": "POST" }
        },
        {
          "key": "http.route",
          "value": { "stringValue": "/api/v1/payment" }
        },
        {
          "key": "customer.id",
          "value": { "stringValue": "customer-00123" }
        },
        {
          "key": "payment.processor.error_code",
          "value": { "intValue": 2001 }
        }
      ],
      "traceId": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
      "spanId": "1a2b3c4d5e6f7a8b"
    }
  ]
}
```

:::

::: tip ECSデータセット例

```json
{
  "@timestamp": "2025-08-27T13:46:29.123Z",
  "ecs": {
    "version": "8.11.0"
  },
  "log": {
    "level": "error"
  },
  "message": "Payment processing failed due to insufficient funds",
  "service": {
    "name": "checkout-service",
    "version": "1.2.5",
    "instance": {
      "id": "checkout-7b5b76d9c-x4z2l"
    },
    "environment": "production"
  },
  "http": {
    "request": {
      "method": "POST"
    },
    "route": "/api/v1/payment"
  },
  "trace": {
    "id": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
  },
  "span": {
    "id": "1a2b3c4d5e6f7a8b"
  },
  "labels": {
    "customer_id": "customer-00123"
  },
  "payment": {
    "processor": {
      "error_code": 2001
    }
  }
}
```

:::

## 各言語のロガーが利用するキー名

各言語の構造化ロギングライブラリが利用するキー名称をまとめる。

| \#               | Java (Logback \+ logstash-encoder) | Go (標準ライブラリ `slog`) | Python (標準 `logging` \+ python-json-logger) |
| :--------------- | :--------------------------------- | :------------------------- | :-------------------------------------------- |
| タイムスタンプ   | `@timestamp`                       | `time`                     | `timestamp`                                   |
| メッセージ       | `message`                          | `msg`                      | `message`                                     |
| ログレベル       | `level`                            | `level`                    | `levelname`                                   |
| ファイル名       | `caller_file_name`                 | `source`                   | `filename`                                    |
| 行番号           | `caller_line_number`               | `source`                   | `lineno`                                      |
| クラス名         | `caller_class_name`                | 該当なし                   | 該当なし                                      |
| スレッド名       | `thread_name`                      | 該当なし                   | `threadName`                                  |
| ロガー名         | `logger_name`                      | （カスタム属性)            | `name`                                        |
| スタックトレース | `stack_trace ※2`                   | （カスタム属性)※3          | `exc_info` / `exc_text`                       |

※1: slogにはロガー名という概念が無い。slog.With("component", "my-service") のように、任意で紐づけるのみである  
※2: `logger.error("エラー", e);` のように**例外オブジェクト**を渡した際に追加した場合のキー名  
※3: stackもしくはstacktrace が多そうである

## Apache / Nginx

ApacheとNginxのアクセスログでよく利用される、標準的なキー名をまとめる。

| 分類                | 項目                   | Apache           | Nginx                |
| :------------------ | :--------------------- | :--------------- | :------------------- |
| Combined Log Format | クライアントIPアドレス | remote_host      | remote_addr          |
|                     | 認証ユーザー           | remote_user      | remote_user          |
|                     | タイムスタンプ         | time             | time_local           |
|                     | リクエストライン ※1    | request          | request              |
|                     | HTTPステータスコード   | status           | status               |
|                     | レスポンスサイズ       | bytes_sent       | body_bytes_sent      |
|                     | リファラ               | referer          | http_referer         |
|                     | ユーザーエージェント   | user_agent       | http_user_agent      |
|                     | リクエスト処理時間     | (追加設定が必要) | request_time         |
|                     | プロキシ先IP (XFF)     | x_forwarded_for  | http_x_forwarded_for |
| カスタム項目        | HTTPメソッド           | method           | request_method       |
|                     | リクエストURI          | request_uri      | request_uri          |

※1 requestは "GET /index.html HTTP/1.1" といった形式で、HTTPメソッドやURIが含まれる。分析を容易にするためカスタム属性で分解することもある。

## プラットフォーム

AWSとGoogle Cloudのログサービスにおける、特別なキー名をまとめる。

| \#             | AWS CloudWatch Logs (Insights)                                                 | Google Cloud Logging (LogEntry)                                                                            |
| :------------- | :----------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| タイムスタンプ | @timestamp                                                                     | timestamp                                                                                                  |
| ログメッセージ | @message                                                                       | jsonPayload                                                                                                |
| ログレベル     | (カスタム属性)                                                                 | severity（INFO, ERROR等の値に応じてUIのアイコンや色が変わり、フィルタリングも容易）                        |
| トレース連携   | ※専用フィールドなし（X-RayのトレースIDをカスタムキーとして含めることが一般的） | trace、spanId（Cloud Traceと自動で連携するためのID。ログエクスプローラ上でトレースへのリンクが生成される） |
| HTTPリクエスト | (カスタム属性)                                                                 | httpRequest。HTTPリクエスト情報（requestMethod, status, latency等）を入れることで、特別に表示される        |
| カスタム属性   | (カスタム属性)                                                                 | labels。インデックス化され、高速な検索・フィルタリングに使いたいキーを指定する                             |

- 見解
  - ソフトなベンダーロックインになるため、移植性を考慮するとOTelの規則を使う方がベター
  - OTelのエクスポーターなど、FWレイヤーなどでマッピングするイメージ
    - 例: `trace_id` を `logging.googleapis.com/trace` にマッピング
- 思想について
  - AWS CloudWatch Logs
    - `@`で始まるいくつかのメタデータフィールドを除き、ログメッセージ(`@message`)の中身は自由である。クエリ実行時(スキーマオンリード)に必要な情報をパースする考え方が基本
  - Google Cloud Logging
    - `LogEntry`という厳格なオブジェクト構造を持ち、`severity`や`httpRequest`といった定義済みのフィールドに沿って出力する(スキーマオンライト)ことで、特別なUI表示やCloud Traceとシームレスに連携させるという思想である

::: tip AWS CloudWatch Logs の Embedded Metric Format (EMF)  
AWS CloudWatch Logsには、EMFというログイベント内にメトリクスデータを埋め込むためのJSON仕様がある。これを利用することで、PutMetricDataのような同期的APIを呼び出さず、特定のフォーマットで構造化されたログを標準出力に書き出すだけでメトリクス連携ができる。

- [仕様: 埋め込みメトリクスフォーマット \- Amazon CloudWatch](https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html)

:::

## SaaSオブザーバビリティプラットフォーム

NewRelic、DataDogなども独自のキーがあるが、OTelのエクスポーターなどの対応が積極的であるため、その層で吸収する方針が妥当だと考えられる。

| \#                                   | DataDog キー | New Relic キー | OpenTelemetry 相当規約 |
| :----------------------------------- | :----------- | :------------- | :--------------------- |
| トレースID                           | dd.trace_id  | trace.id       | trace_id               |
| スパンID                             | dd.span_id   | span.id        | span_id                |
| サービス名                           | service      | entity.name    | service.name           |
| 環境                                 | env          | (カスタム属性) | deployment.environment |
| バージョン                           | version      | (カスタム属性) | service.version        |
| ホスト                               | host         | hostname       | host.name              |
| ログ重要度レベル                     | status       | TODO           | TODO                   |
| ログ生成元 （nginx、postgresqlなど） | source       | TODO           | TODO                   |

## 推奨するキー名称

方針は以下の通り。

1. OTel準拠とECSの語彙を取り入れる
   - 可能な限りOpenTelemetryのセマンティック規約の命名規則に従う
   - 不足していれば、ECSの語彙を取り入れる
   - ログレベルが `severity.text` になるなど、取り入れることが厳しい場合は、 `level` などに一部だけ書き換えることを想定する。ただし、技術標準がある以上、長期的に準拠していく
2. プラットフォーム非依存
   - アプリケーションコード内で出力するキーは、特定のクラウドプロバイダーやSaaSベンダーに固有のキーを含まない
   - プラットフォーム固有のキーへのマッピングは、フレームワークレイヤー（ログコレクター）の責務に（できる限り）する
3. 全てのログに必須の「共通スキーマ」と、特定のコンテキスト（例: HTTPリクエスト、データベースクエリ）に応じて追加されるオプションの「拡張スキーマ」を持つ、階層的な構造とする

| 大分類       | 小分類           | キー名                                                                 | 説明                                         | 例                                    | 理由                                                                                                                                                                    |
| :----------- | :--------------- | :--------------------------------------------------------------------- | :------------------------------------------- | :------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 共通スキーマ | コアフィールド   | timestamp                                                              | タイムスタンプ。可読性の高いISO 8601形式     | "2025-08-26T10:30:00.123456789Z"      | OTel, ECSの両方で必須                                                                                                                                                   |
|              |                  | severity.text （※使用しているライブラリによってはlevelのままでも許容） | 人間が読むための主要な重大度レベル           | "ERROR"                               | OTel規約に準拠。ecsでは [log.level](https://www.elastic.co/docs/reference/ecs/ecs-log#field-log-level)                                                                  |
|              |                  | message                                                                | ログの主要なペイロード                       | "User login failed"                   | OTelのBodyに相当。ECSでは[message](https://www.elastic.co/docs/reference/ecs/ecs-base#field-message)                                                                    |
|              | ロガーで自動付与 | service.name                                                           | システム内でサービスを識別する最も重要な属性 | "authentication-service"              | OTel, ECS, DataDog, New Relic全てで中核                                                                                                                                 |
|              |                  | service.version                                                        | リリースの追跡とリグレッション分析に不可欠   | "1.2.3"                               | OTel, ECS, DataDogで標準                                                                                                                                                |
|              |                  | deployment.environment                                                 | 本番/ステージング環境のフィルタリングに必須  | "production"                          | OTel, DataDogで標準                                                                                                                                                     |
|              | 計装で自動付与   | trace_id                                                               | 分散トレースへの基本的なリンク               | "a1b2c3d4e5f6..."                     | OTel, ECS, New Relicに準拠（DataDogはdd.trace_idにマッピング要）                                                                                                        |
|              |                  | span_id                                                                | トレース内の特定の操作へのリンク             | "f1e2d3c4b5a6..."                     | OTel, ECS, New Relicに準拠（DataDogはdd.span_idにマッピング要）                                                                                                         |
| 拡張スキーマ | HTTP要求/応答    | http.request.method                                                    | HTTPメソッド                                 | "GET"                                 | `OTelとECSのHTTP規約から規定`                                                                                                                                           |
|              |                  | http.response.status_code                                              | HTTPステータスコード                         | 200                                   |                                                                                                                                                                         |
|              |                  | url.path                                                               | リクエストURL                                | "/users/123?query=abc"                | OTelでは[url.path](https://opentelemetry.io/docs/specs/semconv/registry/attributes/url/#url-path)                                                                       |
|              |                  | user_agent.original                                                    | ユーザーエージェント                         | "Mozilla/5.0..."                      |                                                                                                                                                                         |
|              |                  | client.address                                                         | クライアントIPアドレス                       | "192.0.2.1"                           | OTelでは[client.address](https://opentelemetry.io/docs/specs/semconv/registry/attributes/client/#client-address)                                                        |
|              |                  | http.request.body.size                                                 | リクエストボディのバイト数                   | 1024                                  | OTelでは[http.request.body.size](https://opentelemetry.io/docs/specs/semconv/registry/attributes/http/#http-request-body-size)                                          |
|              |                  | http.server.request.duration                                           | 処理時間（ナノ秒）                           | 125000000                             | OTelでは[http.server.request.duration](https://github.com/open-telemetry/semantic-conventions/blob/v1.37.0/docs/http/http-metrics.md)                                   |
|              | DB               | db.system                                                              | データベースの種類                           | "postgresql"                          | OTelのデータベース規約に基づく`                                                                                                                                         |
|              |                  | db.statement                                                           | 実行SQL文                                    | "SELECT \* FROM users WHERE id \=?"   |                                                                                                                                                                         |
|              |                  | db.operation                                                           | 実行操作                                     | "SELECT"                              |                                                                                                                                                                         |
|              |                  | db.duration                                                            | クエリ実行時間（ナノ秒）                     | 15000000                              |                                                                                                                                                                         |
|              | 例外             | exception.type                                                         | 例外クラス名                                 | "java.lang.NullPointerException"      | OTelでは[exception](https://opentelemetry.io/docs/specs/semconv/exceptions/exceptions-logs)を利用。ecsでは [error](https://www.elastic.co/docs/reference/ecs/ecs-error) |
|              |                  | exception.message                                                      | エラーメッセージ                             | "Cannot invoke method on null object" |                                                                                                                                                                         |
|              |                  | exception.stack_trace                                                  | スタックトレース                             | "at com.example.MyClass..."           |                                                                                                                                                                         |
|              |                  | event.kind                                                             | イベントの種類                               | "event"                               | ecsでは [event](https://www.elastic.co/docs/reference/ecs/ecs-event)                                                                                                    |
|              |                  | event.category                                                         | イベントのカテゴリ                           | "error"                               |                                                                                                                                                                         |
|              |                  | event.outcome                                                          | イベントの結果                               | "failure"                             |                                                                                                                                                                         |

# レイアウト

ログのフォーマットには構造化ログである、JSONLinesを利用する。

- RFC8259で仕様が標準化されており、数値型や真偽値などのデータ型が利用できるため。幅広く利用されているため、CloudWatch LogsやBigQuery等の多くのサービスやツールでサポートされているため。
- Apache Combined FormatやLTSV（Labeled Tab-Separated Values）は信頼できる仕様が存在しない。

## ローカル環境の場合

ローカル環境に限っては、JSON Linesではなく非構造なログ形式も許容する（構造化ロギングのままでも良い）。

::: tip 絵文字でカラフルに  
特にローカル環境のターミナルでしか利用しない場合は、ログメッセージに絵文字を入れると視認性が向上しやすいというテクニックがある。

```console
DEBUG: Order #ORD-123 の処理を開始します。現在のステータス: PENDING ⏳
DEBUG: 在庫を確認中... 商品ID: P-123 の在庫は 10個です ✅
DEBUG: 注文ステータスを PROCESSING ⚙️ に更新しました。
DEBUG: 最終的な合計金額を計算しました: 💰 10000円
DEBUG: ユーザー customer@example.com 宛に確認メールを送信します 📧
DEBUG: 注文ステータスを COMPLETED ✨ に更新しました。
DEBUG: Order #ORD-123 の処理が正常に完了しました 🎉
```

適切な絵文字を使うことで、ログメッセージの見逃しを防ぐことができる。デバッグ中の心理的な負担を抑制できるという声もある。ただし、あくまで開発環境限定とし、デプロイメント環境ではこういった絵文字は出さない（ノイズとなるため）ようにすること。

:::

::: tip ANSIエスケープシーケンスでターミナルを彩る  
モダンなロギングライブラリが普及する前は、ANSIエスケープシーケンスと呼ばれる特殊な文字列をログに埋め込むことで、ターミナルのログ出力に色を付けて視認性を高めるテクニックが使われることもあった。

- \\u001B\[31m: 赤色
- \\u001B\[33m: 黄色
- \\u001B\[32m: 緑色
- \\u001B\[0m: 装飾をリセット

```java
// Javaでの出力例
System.out.println("\u001B[31m" + "ERROR" + "\u001B[0m" + ": Critical failure detected.");
System.out.println("\u001B[33m" + "WARN" + "\u001B[0m" + ": API response is slow.");
```

####

ANSIエスケープのよくある課題は、ANSIエスケープシーケンスを解釈できない環境では、ただのノイズの多い文字列として表示されてしまうことである。例えば、ログをファイルにリダイレクト（\>）して、後からテキストエディタで開いたり、CI/CDツールのログビューアで表示したりすると、以下のようにシーケンスがそのまま表示され、視認性が低下する。

```shell
# 制御シーケンスが表示されたログの例
^[[31mERROR^[[0m: Critical failure detected.
^[[33mWARN^[[0m: API response is slow.
```

####

そのため、高性能なロギングライブラリ（Logback, Log4j2など）では、出力先が色表示に対応したターミナル（TTY）であるかを自動的に判別し、対応している場合のみ安全に色を付けるといった機能を持つものがある。

便利な場面もあるが、クラウド環境ではパースの負荷がかかるだけであり、エスケープミスなどの事故も多いため、原則、ANSIエスケープは利用しない。

:::

# 出力項目

## ログレベル

主要なログレベルは下表の通り。 [RFC 5424 - The Syslog Protocol](https://tex2e.github.io/rfc-translater/html/rfc5424.html)のSeverity定義、およびAndroidの[ロギング定義](https://source.android.com/docs/core/tests/debug/understanding-logging?hl=ja)と整合性を持たせ、システムの運用監視と開発効率の両立を目指す。

【凡例】 ✅️:ログ出力を行う

| レベル | 説明     | 目的                                                                                                                  | ローカル | 開発 | 検証 | 本番 |
| :----- | :------- | :-------------------------------------------------------------------------------------------------------------------- | :------- | :--- | :--- | :--- |
| FATAL  | 致命的   | 【サービス停止】 アプリケーションの継続が不可能なエラー。サービスを停止させる。必須の環境変数が未設定など。           | ✅️      | ✅️  | ✅️  | ✅️  |
| ERROR  | エラー   | 【要対応】 特定のリクエスト処理は失敗したが、アプリケーション自体は動作を継続できるエラー。処理中の予期せぬ例外など   | ✅️      | ✅️  | ✅️  | ✅️  |
| WARN   | 警告     | 【潜在的な問題】 直ちにエラーではないが、将来（N営業日以内）に対応が必要な状態。証明書の期限切れまで1ヶ月を切ったなど | ✅️      | ✅️  | ✅️  | ✅️  |
| INFO   | 情報     | 【動作記録】 運用者がシステムの正常性を判断するための、ビジネスプロセス上の重要なイベント。バッチ処理の開始/終了 など | ✅️      | ✅️  | ✅️  | ✅️  |
| DEBUG  | デバッグ | 【開発者向けデバッグ情報】 開発者がバグを修正する際に使用する詳細情報。実行されたSQLクエリなど                        | ✅️      | ✅️  |      |      |
| TRACE  | トレース | 【開発者向け詳細追跡情報】 `DEBUG`より更に詳細なコードの実行情報。メソッドの開始/終了など                             | ✅️      |      |      |      |

推奨は以下の通り。

- アプリからの個別ロジックでは、`DEBUG` ～ `ERROR` を利用する
  - 各アプリからは、`TRACE` `FATAL` （`CRITICAL`）は利用しない（フレームワークや共通ライブラリ側は利用する可能性あり）
- デプロイメント環境（dev, stg, prod）での推奨出力レベルは上表の通りとする
  - デプロイメント環境のうち、開発環境は、SQLログなどを確認することも多いため `DEBUG` にする
  - ただし、本番データを移行するなど、データ起因で大量にログ出力がありえる場合は、 `INFO` レベルに事前に切り上げる
- 環境変数（ `LOG_LEVEL` ）で切り替え可能にする
- `/loggers` エンドポイントや、JMX (Java Management Extensions) を利用して、外部からログレベルを動的に変更可能にすることは非推奨とする
  - CI/CDが発達した昨今であれば、直接Terraformなどのコード変更でシームレスにデプロイ可能であるため
  - セキュリティ上、公開機能は最小限にしたいため
  - コンテナでホスティングされているとLB経由で操作することになり、ログレベルの書き換えを適切に反映させることが困難であるため

## 通知フラグ

エラーなどが発生した時に、システム管理者にメールやSlackで通知する必要がある。大量の不要なアラート通知に晒されると、重要な通知を見逃すことに繋がるため、「本当に人間が確認すべきこと」を通知する設計が必要である。ログの通知判定方法としては、ログレベルで行うパターンと通知フラグという項目で制御する方法がある。

推奨は以下の通り。

- 基本的に、ログレベル（WARN、ERROR）で通知の制御を完結させることができないか検討する（通知フラグの導入無しで運用できないか考える）
  - WARN、ERROR以上は一律、通知するというシンプルな設計を実現できる
- 通知フラグを導入する場合は、以下の条件のいずれかが必要になった場合のみとする
  - INFOレベルでも通知したいケース（例. 重要なバッチの完了通知）。特に、アプリ上に通知処理のコードを書くのではなく、ログ通知の仕組みに乗っかりたい場合
  - コード修正なしに、「メッセージ定義書」だけで、通知のON/OFFを切り替える必要がある場合
    - この場合、ログレベルと通知の有無は、直接的には無関係になる。実装上は、特定のログレベル以上ではデフォルトで通知フラグを立てておくと、実装時に通知フラグを付与するかどうかの判断や手間を減らすことができる
    - あるメッセージIDの通知有無を変えたい場合に、複数箇所があり修正漏れの可能性を許容できない、静的解析などで担保できない場合など

::: tip ERRORレベルでも通知させたくない場合がある？  
例えば、外部APIの一時的な接続エラーが発生したが、リトライで成功する可能性が高いため、そのERRORレベルのログは通知させたくないという場合がある。しかし、これは通知フラグで制御するのではなく、通知が不要であればINFOレベルにすべきである。  
:::

## メッセージコード

- エラーログを運用者が参照する「運用手順書（障害対応マニュアル）」と紐づけるために、開発者はログを一意に識別できるメッセージコードを付与する
  - 自然言語のエラーメッセージは、開発者によって表現が揺らいだり、同じ文面でも発生箇所によって意味が異なったりすることがあるため
- 運用者の対応が必要なログレベル（例. WARN以上）にはメッセージコード設定する

::: tip INFOレベルにはメッセージコードの設定は不要
あくまで、メッセージコードの管理は、運用手順と紐づかせるために設定する。INFOレベルのログは通知フラグなどの制御を導入しない限り、システム管理者に通知されないため、あくまで開発者の動作確認など目的で出力して良く、メッセージコードも不要である。  
:::

## トレースID

[トレースIDをどこで払い出すべきか | オブザーバビリティ | Web API設計ガイドライン](https://future-architect.github.io/arch-guidelines/documents/forWebAPI/web_api_guidelines.html#%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B9id%E3%82%92%E3%81%A8%E3%82%99%E3%81%93%E3%81%A6%E3%82%99%E6%89%95%E3%81%84%E5%87%BA%E3%81%99%E3%81%B8%E3%82%99%E3%81%8D%E3%81%8B) に記載したとおり、なるべく上流でトレースIDは払い出して出力する。

- クライアント側のアプリケーションの統制を行えるのであれば、①クライアント側でトレースIDを生成する
- 統制が無理な場合は、サーバーのミドルウェア（ServletFilterやインターセプターの層）でトレースIDを発番する

## ユーザーメッセージとログ

開発者/運用者向けの「ログメッセージ」と類似の概念として、エンドユーザー向けにユーザーに状況を伝え、次に行うべきアクションを促すことを目的とした「ユーザーメッセージ」が存在する。

推奨は以下の通り。

- ログのメッセージと、ユーザーに表示するエラーメッセージは、目的と対象者が異なるため、必ず分離して管理する
  - セキュリティリスクを避けるため（ SQLException: Connection refused for user 'root'@'db-host-internal' を出すと攻撃のヒントになってしまう）
  - 保守性を上げるため（デバッグのためにログ情報を追加・変更したい場合でも、ユーザーメッセージの文言を気にしなくても済む。またその逆もある）
- ログ出力をしつつ、ユーザー向けにエラーを表示することがある。それらを紐づけるために、トレースIDをユーザーメッセージにも出力し、紐づけを可能とする
  - これにより、ユーザーからの「このIDが表示されたエラーが出ました」と問い合わせがあった際に、そのIDをキーに調査が可能となる（どのような操作をしたか？何時頃ですか？といったやり取りを減らすことができる）

✅️出力例（開発者向けのログ）

```json
{
  "timestamp": "2025-09-12T14:46:16.234+09:00",
  "severity.text": "ERROR",
  "message": "Error processing payment.",
  "service.name": "payment-service",
  "thread.name": "http-nio-8080-exec-5",
  "logger.name": "com.example.MyPaymentService",
  "error.id": "E-1a2b3c4d",
  "error.code": "PAYMENT-003",
  "exception.type": "com.example.PaymentApiException",
  "exception.message": "Credit card company timeout",
  "exception.stack_trace": "com.example.PaymentApiException: Credit card company timeout\n\tat com.example.MyPaymentService.processPayment(MyPaymentService.java:42)\n\t... (スタックトレースが続く)"
}
```

✅️出力例（ユーザー向けのメッセージ）

```console
決済処理中にエラーが発生しました。お手数ですが、時間をおいて再度お試しください。
解決しない場合は、サポートまでお問い合わせください。(エラーコード:E10222  トレースID: E-00112233)
```

## メッセージの書き方

ログメッセージ単体でも、「何が・なぜ起きたのか」を理解できるように書くと、初動を上げることができ、運用視点でも優れている。

推奨は以下の通り。

- 具体的かつ、一意に解釈できるように書く
  - ❌️: 「DBエラーです」 (接続？クエリ？タイムアウト？)
  - ✅️: 「商品テーブルへのINSERTに失敗しました。原因: 主キーが重複しています。 productId: 12345」
- 調査で切り分けに使える（トレースできる情報）識別子を含めること
  - JavaではMDC、Goではcontextに入れて、フレームワーク側で自動的にログに付与する設計にする
  - 識別子の例
    - リクエストID / トレースID: リクエストの入口から出口までを繋ぐ最も重要なID
    - ユーザーID / テナントID: 誰のリクエストで問題が起きたのかを特定
    - セッションID: 特定のセッションでの一連の操作を追跡
    - 注文ID / 商品IDなど: ビジネス上重要なID
- 事実とデータを分離する
  - ログメッセージの「テンプレート（事実）」と「可変値（データ）」を分離する
  - 可変値は構造化ログとして個別のキーとして切り出す
  - Goのslogを使った例
    - ❌️: logger.Info("ユーザー " \+ userId \+ " のカート追加時の在庫引当に失敗しました。SKU: " \+ skuId)
    - ❌️: logger.Info(“カート追加時の在庫引当が失敗しました。（ユーザー " \+ userId \+ "SKU: " \+ skuId+ “）”)
    - ✅️: logger.Info("カート追加時の在庫引当が失敗しました。", "user.id", userId,"sku.cd", skuId)
  - 可変値は、トップレベルでフラットにもたせる
    - ログ分析性を上げるため（detailsにすると視認性が上がるが、ログ基盤上のクエリが書きにくく性能劣化の可能性もあるため）

✅️: 可変値をフラットにし、テンプレートと分離した例

```json
{
  "timestamp": "2025-08-26T10:36:17.123+09:00",
  "severity.text": "INFO",
  "message": "カート追加時の在庫引当が失敗しました。",
  "user.id": "user-456",
  "sku.cd": "ABC-123-XYZ-RED-L"
}
```

❌️: メッセージ本文に可変値を埋め込んだ例

```json
{
  "timestamp": "2025-08-26T10:36:17.123+09:00",
  "severity.text": "INFO",
  "message": "カート追加時の在庫引当が失敗しました。（ユーザーID:user-456 SKU:ABC-123-XYZ-RED-L）"
}
```

❌️: details配下にまとめる例

```json
{
  "timestamp": "2025-08-26T10:36:17.123+09:00",
  "severity.text": "INFO",
  "message": "カート追加時の在庫引当が失敗しました。",
  "details": {
    "user.id": "user-456",
    "sku.cd": "ABC-123-XYZ-RED-L"
  }
}
```

# 出力ルール

## フロントエンドのログ出力

フロントエンドでは、基本的にログ出力を行わない。

- 開発者向けのデバッグ情報が、一般のユーザーにも見えてしまう可能性があり、情報漏洩のリスクがあるため
- デバッグ用のconsoleが残っていると、コードが読みにくくなるため
- ESLintやBiomeのルールでconsoleの使用は警告されるため、そのルールに合わせる

もし、クライアントのエラー状況など収集したい場合は、Sentryなどのログ基盤を導入を検討すること

::: info 参考

- [noConsole | Biome](https://biomejs.dev/linter/rules/no-console/)
- [no-console \- ESLint \- Pluggable JavaScript Linter](https://eslint.org/docs/latest/rules/no-console)

:::

## 起動時のログ出力

アプリケーション起動時のログ出力は、アプリケーションの状態を把握し、問題を素早く特定するために非常に重要である。「何が、どのような設定で、正常に起動したか」を一目で把握でき、問題発生時の迅速な原因特定が可能なようログ出力を行う。

推奨は以下の通り。

- ログレベル: INFO にする
- 以下の項目を出力する

| 項目           | 概要                                                                                                               | 例                            |
| :------------- | :----------------------------------------------------------------------------------------------------------------- | :---------------------------- |
| サービス名     | どのサービスのログかを明確にするため（特にマイクロサービス環境で重要）                                             | user-api                      |
| バージョン情報 | アプリケーションバージョンを示す。ビルド時のgit tag情報等を出力する                                                | v1.2.3                        |
| Gitハッシュ    | ビルド時のgit hash値を出力する                                                                                     | da94541                       |
| タイムスタンプ | “ビルド時” のタイムスタンプをJSTで出力する。起動時では無いことに注意                                               | 2025-09-12T14:46:16.234+09:00 |
| 実行環境       | development, staging, production のどれで動いているかを区別するため                                                | production                    |
| 主要な設定値   | 接続先のDBホストなど、動作に影響する重要な設定値。 ⚠️注意：パスワードやAPIキーなどの機密情報は絶対に出力しないこと | DB_HOST: prod-db.example.com  |

- 起動シーケンスのマイルストーンを記録する
  - 起動が完了するまでの主要なステップ（マイルストーン）をログに出力することで、もし途中で失敗した場合にどの段階で問題が起きたのかを特定することができる。

::: tip 起動ログのフォーマット  
起動ログは必ずしもその他のログフォーマットと一致していなくとも良い。通常のログは機械的な解析に備えて構造化させておいた方が有利だが、起動ログはデプロイ時や障害発生時の切り分け等、開発者による確認用途が主となるので、ここでは視認性を優先している。

ただし、ユニットテスト時など大量に起動ログが出力されるケースではノイズとなる可能性があるので、そういった場合は実行環境によって出力有無を切り変えることを検討する。  
:::

::: tip バージョン情報のバインド  
バナー内にバージョン番号などをハードコーディングすると、更新を忘れがちになり、実際のバージョンと乖離する可能性がある。ビルドプロセスで静的ファイルに書き込むなどで可能な限り自動化することを検討する。  
:::

```console
  _   _   _   _   _   _
 / \ / \ / \ / \ / \ / \
( U | S | E | R | A | P | I )
 \_/ \_/ \_/ \_/ \_/ \_/
 ==================================================
 Service: UserAPI
 Ver: v1.5.2
 GitHash: da94541
 Timestamp: "2025-09-12T14:36:16.234+09:00"
 ENV: production
 ==================================================

{
  "timestamp": "2025-09-12T14:46:16.234+09:00",
  "severity.text": "INFO",
  "message": "Application startup sequence initiated.",
}
{
  "timestamp": "2025-09-12T14:46:16.235+09:00",
  "severity.text": "INFO",
  "message": "Configuration loaded successfully.",
}
{
  "timestamp": "2025-09-12T14:46:16.236+09:00",
  "severity.text": "INFO",
  "message": "Config: {"key": "value"...}",
}
{
  "timestamp": "2025-09-12T14:46:16.237+09:00",
  "severity.text": "INFO",
  "message": "Database connection established.",
}
{
  "timestamp": "2025-09-12T14:46:16.238+09:00",
  "severity.text": "INFO",
  "message": "Server listening on http://0.0.0.0:8080",
}
```

## 稼働中のログ出力

- バッチの進行中
  - IF等での一括処理時は処理状況を一定タイミングでロギング（xx行目\~xx行目処理中 など）
    - ハングしていないことの確認
- SQL実行ログについて
  - twoway-sql の場合は、生成後のSQLにたいして　フォーマットして出力することが望ましい
- ヘルスチェックのログは、アクセスログに出さないように制御する
  - ログ検索で除外できるとはいえ、ノイズである。また、ヘルスチェックのログを見る用途は稼働してしまえば存在しないため、不要な費用発生である

## 非正規化

利用規約などに明記し、ユーザーと合意を取った上で、アクセスログを分析する場合、分析に必要なユーザー属性を振り下ろすという非正規化を行うことはよくある。例えば、会員ランク（通常会員、プレミアム会員）などの属性はマスタから引き当てることができるが、分析時のコストが上がるため、振り下ろすことが望ましいのであれば、予めログ項目として出力することが望ましい。

## 暗黙的なログ項目・明示的なログ項目

多くのログ出力ライブラリでは、ロガー生成時に項目を設定したり、親のロガーに対して情報を付与した子ロガーを作成できることが多い。また日付などのようにインプットを与えなくても機械的に決定できる項目もあったりデータごとのライフサイクルは様々である。

推奨は以下の通り。

- 下表のような、ログ項目一覧を作成する
  - このライフサイクルを明記する
  - 共通処理のレイヤーや、利用するフレームワーク等で暗黙的に出力するものと、アプリケーション開発者が明示的に出力しなければならないものを明確にする

| 出力場所         | トリガー             | 項目種別             | 項目例                                                                                                         | 補足説明                                                                                                           |
| :--------------- | :------------------- | :------------------- | :------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| フレームワーク   | リクエスト単位で出力 | HTTPリクエスト       | HTTPステータス、パス、処理時間、リクエスト元IP                                                                 | Webフレームワークなどがリクエスト処理のライフサイクルを通じて自動的に記録する情報                                  |
|                  |                      | DBアクセス           | SQLクエリなど                                                                                                  |                                                                                                                    |
|                  | 例外発生時           | 例外                 | 例外メッセージ、ログレベル                                                                                     | try/catchで拾った例外はフレームワークでログレベルを決定                                                            |
| アプリケーション | アプリ呼び出し       | ロガー出力項目       | ファイル名、行番号など                                                                                         | ログ出力ライブラリがスタックトレースなどから自動的に取得する情報                                                   |
|                  |                      | コンテキスト設定項目 | ・起動時のオプション、環境変数など<br> ・ログインユーザーID、セッションID<br> ・トレースID、トランザクションID | 処理の開始点（AP起動時、リクエスト受付時など）で設定され、MDCやContextオブジェクト等で後続の処理に引き継がれる情報 |
|                  |                      | 暗黙的設定項目       | クラス名（ロガー名）など                                                                                       | ロガー初期化時に指定                                                                                               |
|                  |                      | 明示的出力項目       | ・エラーメッセージ、エラーコード<br> ・処理の状況、特定の変数やパラメータなど                                  | 開発者が個別にログ内容を実装                                                                                       |
|                  |                      |                      | ログレベル                                                                                                     | log.error() というように、明示的に指定する場合                                                                     |

# 国際化対応/英語の対応是非

開発、保守運用、SRE、サポートなどの一部がグローバルで体制が組まれる場合は、英語でのログメッセージ化が必要になる。

- 推奨
  - もし、国際化対応が必要な場合、原則、英語の対応とする（日本語でのメッセージ出力は行わない）
    - 日本語やその他各国の言語でのログ出力は行わない
    - ログメッセージ管理のSSoT（Single Source of Truth: 信頼できる唯一の情報源）管理のため
  - ログごとに、運用が一意となるメッセージコードを付与する
    - それに紐づく運用マニュアルは、各国拠点ごとに作成させるなどは、状況に応じて実施する

✅️出力例（英語での出力）

```json
{
  "timestamp": "2025-08-26T11:45:10.880+09:00",
  "severity.text": "WARN",
  "message.code": "BIZ-W-1001",
  "message": "Inventory update failed due to a data conflict (optimistic lock). Please retry the operation.",
  "process.name": "inventory_allocation",
  "order.id": "order-67890",
  "product.id": "product-ABC-001",
  "requested.quantity": 5,
  "current.version": 12,
  "attempted.version": 11
}
```

❌️出力例（message、message_jpを設けることで、英語・日本語の2種別で出力。冗長でログサイズの肥大化を招き、メッセージ管理の保守性も低下）

```json
{
  "timestamp": "2025-08-26T11:45:10.880+09:00",
  "severity.text": "WARN",
  "message.code": "BIZ-W-1001",
  "message": "Inventory update failed due to a data conflict (optimistic lock). Please retry the operation.",
  "process.name": "inventory_allocation",
  "order.id": "order-67890",
  "product.id": "product-ABC-001",
  "requested.quantity": 5,
  "current.version": 12,
  "attempted.version": 11
}
```

# ドキュメント管理

特にWARNレベル以上のログは、業務・システム対応が必要と考えられるため、ドキュメントで一元的に管理する必要がある。それぞれのメッセージコードに紐づく、一意な運用フローが定義できるようにする。

下記に例を示す。運用定義は「運用一覧」・「運用手順書」として別ドキュメントに記載することも多い。

| 分類     | 項目                         | 必須 | 内容                                                 | 例                                                                                                    |
| :------- | :--------------------------- | :--- | :--------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| 出力項目 | メッセージコード             | ✅️  | 一意なID。命名規則を設けるべき                       | AUTH-LOGIN-001                                                                                        |
|          | メッセージ                   | ✅️  | 何が起きたかを一行で簡潔に説明                       | ユーザー認証の失敗                                                                                    |
|          | 可変値                       |      | 可変値                                               | userID, itemID, ColorCD, SizeCD                                                                       |
|          | エンドユーザー向けメッセージ |      | (もしあれば) 設定する                                | 「ユーザーIDまたはパスワードを確認してください」                                                      |
|          | ログレベル                   | ✅️  | ERROR, WARN, INFO のいずれか                         | WARN                                                                                                  |
|          | 通知フラグ                   |      | ログレベルとは別に通知有無を制御したい場合に設定する | true / false                                                                                          |
| 運用定義 | 発生原因                     | ✅️  | この事象が発生する主な原因や発生条件を列挙           | 1\. パスワードの入力ミス<br> 2\. 存在しないユーザーIDの指定                                           |
|          | アクション                   | ✅️  | 運用者が取るべき対応や調査を記載                     | ・関連ログからリクエスト元のIPアドレスを確認<br> ・短時間での多発はブルートフォース攻撃の可能性を疑う |

# セキュリティ

推奨は以下の通り。

- 機密情報をログ出力しない
  - パスワード、APIキー、クレジットカード番号、個人情報（PII）などのログ出力は禁止する
  - 誤って出力されないように、ログ出力のフレームワーク側でもマスキングやオミットするような作り込みを行っておく
    - 機密フィールドを除外した、JavaでいうtoString()メソッドやDTO（構造体など）を作っておく
- アクセス制御
  - ログの不正な改ざんを防ぐため、一度書き込まれたら変更、削除できないようなIAMロール設定を行う
  - 閲覧制御も、必要なメンバーのみに絞るようにする

# 性能

推奨は以下の通り。

- 非同期ロギング
  - Javaでは、 **SLF4J \+ Logback** の組み合わせかつ、AsyncAppender を活用する
  - Goのロギングは非常にシンプルで性能が良いため、非同期ロギングは利用しなくても良い
  - AsyncAppender は、ログイベントを一旦メモリ上のキューに格納し、別のワーカースレッドがキューからイベントを取り出しログ出力する
  - プロセス障害時のログ欠損に備え、JVMのシャットダウンフックでキュー内のログをフラッシュさせる設定をいれる
  - キューが溢れた時の対応は、アプリケーションをブロッキングさせる。ログを破棄させる設定にはしない
- 遅延評価の活用
  - SLF4J利用かつ、付加項目をメッセージに埋め込む場合、プレースホルダ ({}) を使用し、そのログレベルが出力対象でない場合、引数の文字列化などの処理自体をなくす
    - ✅️良い例: `log.debug("Processing user data: {}", userObject);`
    - ❌️悪い例: `log.debug("Processing user data: " + userObject.toString());`
  - Pythonのloggingモジュールを利用する場合、f文字列ではなく、%形式のプレースホルダを使用することで、そのログレベルが出力対象でない場合の引数のレンダリング処理を防ぐ
    - ✅️ 良い例: `logging.debug("Processing user data: %s", user_object)`
    - ❌️ 悪い例: `logging.debug(f"Processing user data: {user_object}")`
  - 構造化ログの場合、アプリケーション側で toString() などを呼び出さず、ロガー側に任せる
    - 本当にログ出力される場合に限り、シリアライズを限定できる
- ログ出力の分岐を書く
  - slf4jなどの場合、 `if (logger.isDebugEnabled()) {...}` などとログレベルに応じた分岐を行う。特にログ出力用に文字列加工を行う場合は必須とする
  - Goのロギングは上記のような慣習が無いため行わなくても良い（構造化ロギングの場合、文字列生成を行わないため許容されていると思われる）

注意点は以下の通り。

- forループでのマシンガンログはNG
  - 1000件に1度など、サンプリングしたログ出力を行う
- ファイル名・行番号はログ出力項目にしない
  - ログ項目として「ファイル名」や「行番号」を取得する処理はスタックトレースから取得する場合は負荷が高く、性能劣化の原因になりえる
  - ローカル環境のみ許容し、デプロイメント環境には出力させない。Javaであればロガー名からファイル名の特定は容易であるため
- アプリケーション側での性能問題の疑いがある場合、ログ出力を疑ってみる
  - 特にSQLログなどを大量に出力している場合、そこが遅い場合もある

::: tip logback.xml の設定例  
AsyncAppenderの設定例を示す。

```xml
<configuration>
  <appender name="JSON_STDOUT" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder" />
  </appender>
  <appender name="ASYNC_JSON_STDOUT" class="ch.qos.logback.classic.AsyncAppender">
    <discardingThreshold>0</discardingThreshold>
    <queueSize>256</queueSize>
    <appender-ref ref="JSON_STDOUT" />
  </appender>
  <root level="INFO">
    <appender-ref ref="ASYNC_JSON_STDOUT" />
  </root>
</configuration>
```

:::

::: tip エラー時のバッファリングに注意  
アプリケーションプロセスがクラッシュするような致命的なエラー（FATALレベルなど）が発生した場合、最後に記録しようとしたログメッセージが失われることがある。これは性能向上のためにログ出力内容をメモリ上にバッファすることで生じる。これは原因特定の手がかりが欠損するため、よく問題になる。

この問題を回避するため、「エラーログは即座に書き出す（フラッシュする）べき」という考え方が昔から語られてきた。具体的には、標準エラー出力（stderr）は、標準出力（stdout）と異なり、多くの環境で行バッファリング（改行ごとに書き出し）やバッファリングなしで動作するため、エラーログの出力先として推奨されてきた経緯がある。Goのslogでは明示的にbufio.Writerなどを利用しない限りはバッファリングしないが、そうではない言語では注意が必要である。

Javaのロギングライブラリ（Logback, Log4j2など）では、特定のログレベル（例: WARN以上）のログが記録された際に、自動的にバッファをフラッシュする設定が可能であるため、設定を確認すると良い。

設定例 (Logback)

```xml
<appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
        <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
    </encoder>
    <immediateFlush>true</immediateFlush>
</appender>
```

※注: ConsoleAppenderのimmediateFlushはデフォルトでtrueである。ここでは説明のためにあえて明示的に記載している  
:::

# 費用

CloudWatch Logsやその他のマネージドログサービス（Datadogなど）は、ログデータ量（GB）に応じた課金であり、保持期間に応じたストレージ費用も必要となる。ログ検索時は、クエリのスキャンに応じて課金するサービスが多い。

- 推奨
  - 発生源でログができる限り絞る
    - ログレベルは適切に設定し、用途が不明なログは出力しない
    - 巨大なペイロードはログ出力しない（例えば、Base64化したバイナリデータなど）
    - ログを削ることが目的ではなく、無駄なログを削る。障害発生時に調査に必要なログが欠落してしまえば本末転倒であるため
  - 最初から構造化ロギングにする
    - ログ基盤側でのパース処理は高コストであるため、アプリケーション上からJSONLinesで出力する
  - 保持期間ポリシーを明確にする
    - ビジネス要件やコンプライアンス要件に基づき、保持期間を定める（例: アプリケーションログは30日など）
    - 環境別に定義する。例えば、開発環境は1週間など、短くすることも有効
  - ストレージ階層化
    - データのライフサイクル管理機能は原則不要とする
    - 例: AWSでは一定期間（例: 14日）を過ぎたログは、安価なアーカイブストレージ（Amazon S3 Glacierなど）へ自動的に移動させるなども可能だが、コストメリットがそこまで大きくない

::: info 参考

- [CloudWatch Logs と S3 にかかる料金比較 | DevelopersIO](https://dev.classmethod.jp/articles/comparison-of-fees-for-cloudwatch-logs-and-s3/)
  - CloudWatch Logs \-\> S3 に移動させても、そこまで大きなコスト圧縮にはならないと考えられる
- [Amazon CloudWatch Logs の Amazon S3 へのエクスポート方式の検討 – TechHarmony](https://blog.usize-tech.com/export-cloudwatch-logs-to-s3/)
  - S3へのエクスポート設定もいくつかの設計が必要である

:::

# 謝辞

このアーキテクチャガイドラインの作成にご協力いただいた皆様に、心より感謝申し上げる。

- **作成者**: 真野隼記、八木雅斗、宮崎将太、武田大輝、澁川喜規
- **レビュアー**: 募集中

皆様のご尽力なしには、本ガイドラインは完成しなかった。深く感謝する。
