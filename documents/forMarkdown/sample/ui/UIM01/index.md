# [UIM01] ログイン

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://embed.figma.com/design/kLgdi4xdGRpQudMEoZYwvq/%E3%80%90FMP%E3%80%91Future-Muscle-Partner_%E7%94%BB%E9%9D%A2%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3?node-id=4-5&embed-host=share" allowfullscreen></iframe>

## 概要

機能目的:

- ログインや会員登録導線を提供する

機能概要:

- ログイン処理
- 会員登録への導線

## イベント概要

| No  | イベント名   | イベント分類 | 処理説明 |
| --- | ------------ | ------------ | -------- |
| 1   | 初期表示     | 初期表示     |          |
| 2   | ログインする | ボタン押下   |          |
| 3   | 会員登録     | ボタン押下   |          |

## イベント詳細

### 1. 初期表示

モーダルを起動。初期パラメータは無し。

### 2. ログインする

利用API:

| ID     | URL         | Parameter              |
| ------ | ----------- | ---------------------- |
| API001 | POST /login | 入力フォームの値を取得 |

画面表示制御:

- HTTPステータスが400系
  - 「IDまたはパスワードが異なります」を表示
- HTTPステータスが500系
  - メッセージID（MSG_BIZ_111）表示
- HTTPステータスが200
  - [UIS02](../UIS02/index.md)に遷移

### 3. 会員登録

...
