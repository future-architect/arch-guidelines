# [UIS02] マイページ

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://embed.figma.com/design/kLgdi4xdGRpQudMEoZYwvq/%E3%80%90FMP%E3%80%91Future-Muscle-Partner_%E7%94%BB%E9%9D%A2%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3?node-id=4-2&embed-host=share" allowfullscreen></iframe>

## 概要

機能目的:

- トレーニーのマイページを表示し、受講予定・受講済みのトレーニング一覧を表示する

機能概要:

- 受講状況の表示
- パーソナルトレーナーの検索への導線

## イベント概要

| No  | イベント名       | イベント分類 | 処理説明                                                     |
| --- | ---------------- | ------------ | ------------------------------------------------------------ |
| 1   | 初期表示         | 初期表示     | 初期検索条件に従いAPIを実行し、履歴表示する                  |
| 2   | トレーナーを探す | ボタン押下   | パーソナルトレーナー検索モーダル起動                         |
| 3   | 受講完了確認     | ボタン押下   | 予約済みトレーニングを受講完了に切り替えるためのモーダル起動 |
| 4   | 受講完了         | ボタン押下   | 予約済みトレーニングを完了済みのトレーニングに更新           |

## イベント詳細

### 1. 初期表示

起動パラメータ:

| Name      | Value                   | Memo         |
| --------- | ----------------------- | ------------ |
| userState | {"user_id":"<user_id>"} | ログイン状態 |

初期表示イベント:

- マイページ表示

利用API:

| ID      | URL                       | Parameter                    |
| ------- | ------------------------- | ---------------------------- |
| API-005 | GET /profile/{trainee_id} | trainee_id=userState.user_id |

画面表示制御:

- HTTPステータスが500系
  - メッセージID（MSG_BIZ_111）表示
- HTTPステータスが400系
  - トップページにリダイレクト

利用API:

| ID     | URL                        | Parameter                    |
| ------ | -------------------------- | ---------------------------- |
| API013 | GET /bookings/{trainee_id} | trainee_id=userState.user_id |

画面表示制御:

- 起動条件
  - API016が有効な場合
- HTTPステータスが200以外
  - メッセージID（MSG_BIZ_111）表示

### 2. トレーナーを探す

[UIM002](../UIM02/index.md) を起動。

### 3. 受講完了確認

「`${トレーニングメニュー}` は完了しましたか？」ダイアログを表示する。

キャンセルの場合は閉じる。

### 4. 受講完了

「`${トレーニングメニュー}` は完了しましたか？」ダイアログがOKの場合。

利用API:

| ID     | URL                              | Parameter                    |
| ------ | -------------------------------- | ---------------------------- |
| API016 | PUT /booking/{booking_id}/status | 選択されたトレーニング予約ID |

画面表示制御:

- クリック可否判定
  - 予約済み＋現在時間<=受講時間になっている場合に、クリック可能とする
- HTTPステータスが200以外
  - メッセージID（MSG_BIZ_111）表示
- HTTPステータスが200
  - 次のAPIを呼び出し

利用API:

| ID      | URL                        | Parameter                    |
| ------- | -------------------------- | ---------------------------- |
| API-012 | GET /bookings/{trainee_id} | trainee_id=userState.user_id |

画面表示制御:

- 起動条件
  - API016が有効な場合
- HTTPステータスが200以外
  - メッセージID（MSG_BIZ_111）表示
