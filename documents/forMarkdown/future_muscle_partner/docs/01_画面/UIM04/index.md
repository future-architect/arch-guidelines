# [UIM04] 決済

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://embed.figma.com/design/kLgdi4xdGRpQudMEoZYwvq/%E3%80%90FMP%E3%80%91Future-Muscle-Partner_%E7%94%BB%E9%9D%A2%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3?node-id=249-925&embed-host=share" allowfullscreen></iframe>

## 概要

機能目的:

- トレーニング予約内容を表示し、決済によって確定する

機能概要:

- トレーニングのコース／日時／料金を表示
- クレジット決済に必要な項目の入力
- 決済の確定

## イベント概要

| No  | イベント名     | イベント分類 | 処理説明     |
| --- | -------------- | ------------ | ------------ |
| 1   | 初期表示       | 初期表示     |              |
| 2   | 日時指定に戻る | ボタン押下   | UIM003に遷移 |
| 2   | 決済する       | ボタン押下   |              |

## イベント詳細

### 1. 初期表示

起動パラメータ:

| Name       | Value                         | Memo |
| ---------- | ----------------------------- | ---- |
| trainer_id | {"trainer_id":"<trainer_id>"} |      |
| menu_id    | {"menu_id":"<menu_id>"}       |      |

利用API:

| ID     | URL                      | Parameter            |
| ------ | ------------------------ | -------------------- |
| APIxxx | トレーニングメニュー取得 | 初期パラメータを設定 |

### 2. 日時指定に戻る

[UIM03](../UIM03/index.md)に遷移

### 3. 決済

...
