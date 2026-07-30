---
sidebarDepth: 4
title: Git環境設定ガイドライン
author: フューチャー株式会社
head:
  - - meta
    - name: keywords
      content: Git,GitHub,GitLab
---

<page-title/>

本ガイドラインは、[Gitブランチフローガイドライン](./git_branch_standards.md)を実効化するための、ローカルGit・リポジトリ・ホスティングサービス（GitHub／GitLab）の推奨設定をまとめる。

位置づけ・前提・免責事項は [Introduction](./index.md) を参照。

# Git config推奨設定

`git config` の推奨設定を紹介する。特にGitワークフローの設定が重要である。

```sh
# 基礎
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"

# プロキシ設定（存在する場合）
git config --global http.proxy http://id:password@proxy.example.co.jp:8000/
git config --global https.proxy http://id:password@proxy.example.co.jp:8000/

# プロキシが独自の証明書を持っている場合は、git config http.sslVerify false ではなく、証明書を設定する
git config --global http.sslCAInfo ~/custom_ca_sha2.cer

# Gitワークフロー
git config --global pull.rebase true
git config --global rerere.enabled true
git config --global fetch.prune true

# エイリアス（メンバーそれぞれで別のエイリアスを登録されると、チャットなどのトラブルシュート時に混乱をきすため、ベーシックなものはチームで統一して、認識齟齬を減らす目的で設定を推奨する）
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.ci commit
git config --global alias.br branch
```

::: tip git workflowの補足説明

- `pull.rebase`: pull時にリベースする
- `rerere.enabled`: コンフリクトの解決を記録しておき、再び同様のコンフリクトが発生した場合に自動適用する
- `fetch.prune`: リモートリポジトリで削除されたブランチを削除する
  :::

# クレデンシャル情報の混入防止

## Git-secrets

[git-secrets](https://github.com/awslabs/git-secrets)を用いることで、ユーザーパスワードや AWS アクセスキーなどの機密情報が含まれる可能性のあるコードなどをGit リポジトリに追加されないようにできる。

本ガイドラインの推奨と理由は以下。

- チームメンバー全員に `git-secrets` を導入する
  - Push Protection によってクレデンシャルのリモートへの Push は防げるが、ローカルにクレデンシャルを含むコミット履歴が残っていると復元される可能性がある。そこで、Git-secrets を用いてコミット段階でクレデンシャルを拒否する設定を行っておく

## Push Protection

Push Protectionを有効化することで、コードをプッシュする際にクレデンシャルが含まれていないかチェックする。
もしクレデンシャルが検知されると、プッシュが拒否されるようになる。
メンバー全員が `git-secrets` を設定していれば不要であるが、設定漏れなどでプッシュされてしまうことを防ぐために、本ガイドラインでは有効化しておくことを推奨する。

::: info 参考

- [GitLab Docs | Secret push protection](https://docs.gitlab.com/user/application_security/secret_detection/secret_push_protection/)
- [GitHub | プッシュ保護について](https://docs.github.com/ja/code-security/secret-scanning/introduction/about-push-protection)

:::

## Secret Scanning

Secret Scanningを利用することで、Git リポジトリにクレデンシャルが存在するとメールなどでアラートを送ってくれるようにできる。
Secret Scanningではコードだけでなく、IssueやPull Requestなどもスキャンできるため、本ガイドラインでは利用することを推奨する。

::: info 参考

- [GitHub | シークレットスキャンについて](https://docs.github.com/ja/code-security/secret-scanning/introduction/about-secret-scanning)
- [GitLab | Secret Detection](https://docs.gitlab.com/user/application_security/secret_detection/)

:::

# コミットフック

[git hooks](https://git-scm.com/book/ja/v2/Git-%E3%81%AE%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%9E%E3%82%A4%E3%82%BA-Git-%E3%83%95%E3%83%83%E3%82%AF) を用いて、コミットやプッシュ時に単体テスト実行などのカスタム処理を追加ができる。これを用いると、ローカルでの動作検証などを未実施な状態でレビュー依頼をしてしまうといった状況を未然に防ぎ、開発フローを強制的に適用ができる。

本ガイドラインの推奨と理由は以下。

- `git hooks` を用いたテスト実行は行わない
  - Gitのコマンドを実行するライフサイクルと、動作検証を行いたいライフサイクルは同じでないため、軽微な修正の度にテストが実行されると、作業効率が下がるため
  - CI側でテストが実行されるため、最悪CIで検知が可能
  - 開発者にとって作業効率を考えると、CIで検知ではなくローカルでテスト実行を通してからプッシュするため、CIが整備されている前提では `git hooks` で強制する必然性がないため

::: tip git hooksで何を行うべきか
テスト、コード生成、リンターなど、実行時間が長いものは含めるべきでない。

実行時間が短いフォーマットであれば、`git hooks` で実行させると便利なことが多く（CIで違反に気づいて対応する手戻りが減るためである）、必要に応じて導入しても良い。
:::

# .gitattributes

## eol

チーム開発において開発環境がWindows/Macなど複数存在することは少なくなく、また、Gitリポジトリ上の改行コードは統一した方が余計な差分が生じず扱いやすくなる。このときよく用いるのが、 `core.autocrlf` という設定である。

| 名称          | 設定値 | チェックアウト時の挙動 | コミット時の挙動     |
| ------------- | ------ | ---------------------- | -------------------- |
| core.autocrlf | true   | 改行コードをCRLFに変換 | 改行コードをLFに変換 |
|               | input  | 何もしない             | 改行コードをLFに変換 |
|               | false  | 何もしない             | 何もしない           |

特にWindowsでの開発者の作業ミスを防ぐため、 `git config --global core.autocrlf input` で設定するチームも多い。

しかし、上記の設定漏れや手順が増えてしまうため、本ガイドラインでは `.gitattributes` での対応を推奨する。

`.gitattributes` というファイルをGitリポジトリのルートにコミットしておけば、そのGitリポジトリを使う全員で改行コードの扱いをLFに統一できる。

```sh .gitattributes
* text=auto eol=lf
```

通常、改行コードやインデントの設定は[EditorConfig](https://editorconfig.org/)で行うことが多く、 `.gitattributes` の設定とは重複する。しかし、環境構築ミスなど何らかのトラブルで動作しなかった場合に改行コードミスで特にジュニアクラスのメンバーが困る状況もゼロとは言えないため、本ガイドラインでは `.gitattributes` も作成しておくことを推奨する。

::: warning 特定のファイルのみCRLFでコミットしたい
テスト目的であるファイルだけCRLFで読み込ませたいとする。さきほどの `.gitattributes` の設定ではチェックアウト時に強制的にLFに変換されてしまうため、CRLFのファイルのみ個別で改行コードを指定する必要がある。例えば、`testdata/eol`配下のCSVをCRLFで扱いたい場合は、以下となる。

```sh .gitattributes
* text=auto eol=lf

# 個別で指定
testdata/eol/*.csv text eol=crlf
```

前の行に書いた設定は、後ろの行に書いた設定によって上書きされるため、記載順は「全体に適用する原則」→「個別設定」となるように注意する。

この指定がちゃんと効いているか確認する場合は、 `git check-attr` コマンドを用いると良い。以下のように eolがcrlfで設定されたことが分かる。

```sh
$ git check-attr -a testdata/eol/input1.csv
testdata/eol/input1.csv: text: set
testdata/eol/input1.csv: eol: crlf
```

::: info 参考

- [行終端を処理するようGitを設定する - GitHub Docs](https://docs.github.com/ja/get-started/getting-started-with-git/configuring-git-to-handle-line-endings)
- [.gitattributesのeol=crlfは改行コードをCRLFに変換してチェックインするものではない - エンジニア的考察ブログ](https://chryfopp.hatenablog.com/entry/2013/04/13/113754)

:::

## linguist-generated

自動生成で変更が発生し、かつ大量の変更が頻繁に発生する場合には、レビュアが毎回レビューをすることは効率的でない。

`.gitattributes` で `linguist-generated=true` を設定することで、差分をデフォルトで表示させず、プルリクエストの可視性を向上させることができる。

```sh .gitattributes
# 自動生成されたHTMLファイルの差分を無視する
/path/to/generated/*.html linguist-generated=true
```

上記の設定で `/path/to/generated/main.html` をコミットすると、差分が以下のように非表示となる（Load diffをクリックすることで差分表示は可能）。

![プルリクエストのFile changedでmain.htmlの差分がLoad diffと表示](no_diff.png)

本ガイドラインの推奨は以下の通り。

- ツールなどによる生成ファイルをレビュー対象外とする場合は、`linguist-generated=true` を設定し、レビュアーの負荷を下げる
- レビュアーは差分が省略された場合は、レビュー対象外としてファイルの中身の確認は任意とする

::: tip 生成コードをレビュー対象としたい場合

GitHubでは、[言語毎に生成ファイルと判定する処理](https://github.com/github-linguist/linguist/blob/v9.0.0/lib/linguist/generated.rb)がある。例えツールで作成されたファイルであっても、レビュー確認を必須としたい場合にはクリックする手間が増える分、逆に非効率になる。

例えば、Javaなど複数の言語では3行目までに `Generated by the protocol buffer compiler.  DO NOT EDIT!` が含まれていると[Protocol Bufferの生成コードとみなされる](https://github.com/github-linguist/linguist/blob/63cfd70d54ee8f76c41a73fe56689ed8229c9622/lib/linguist/generated.rb#L348-L359)。

もし、明示的に差分を表示させたい場合、`linguist-generated=false` を設定する必要がある。

```sh .gitattributes
# 以下はコード生成されたファイルだが、レビュー対象としたいためlinguist-generated=falseを設定し、差分を表示させる
/path/to/generated/*.java linguist-generated=false
```

:::

::: info 参考

- [変更したファイルの GitHub での表示方法をカスタマイズする - GitHub Docs](https://docs.github.com/ja/repositories/working-with-files/managing-files/customizing-how-changed-files-appear-on-github)
- [GitHubでファイル差分が表示されない！？レビューを快適にするための差分の非表示ロジックを解説](https://zenn.dev/hacobell_dev/articles/show-diff-in-github)

:::

# .gitignore

Gitで管理したくないファイル名のルールを定義する`.gitignore`ファイルも入れる。ウェブフロントエンドであれば新規プロジェクトを作成すると大抵作成されるのでそれを登録すれば良いが、もしない場合、あるいは複数の言語を使っている場合などは[GitHubが提供するテンプレート](https://github.com/github/gitignore)を元に作成すると良い。GlobalフォルダにはWindows/macOSのOS固有設定や、エディタ設定などもある。

環境設定を`.env`で行うのが一般的になってきているが、`.env.local`、`.env.dev.local`といった`.local`がついたファイルはクレデンシャルなどの機微な情報を扱うファイルとして定着しているため、 `*.local`も追加すると良い。

# 個人用のファイルをGit管理対象外とする

`.gitignore` を用いると、チームでGit対象外とするファイルを一律で設定できる。

一方で、動作確認用のちょっとしたスクリプトなどで以下の要件が出てくることがある。

- 個人的にGitリポジトリ配下のフォルダに格納したいが、コミットしたくない（≒自分のローカルリポジトリのみ必要である）
- あくまで個人用途であるため `.gitignore` に追記したくない

上記の場合は、`.git/info/exclude` を利用することを推奨する。

::: info 参考
[個人的Gitおすすめtips 7選 #GitHub - Qiita](https://qiita.com/hichika/items/f3c980dd069df0f3a56e)
:::

# VS Code拡張

GUIでのGit操作にあたり、次の2つの拡張機能をインストールしておくと利便性が高い。業務上はほぼ必須と見て良い。

- [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)
  - Gitに関する様々な機能を提供する拡張機能
  - 詳細： [VSCodeでGitLensを使う - フューチャー技術ブログ](https://future-architect.github.io/articles/）20240415a/)
- [Git Graph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph)
  - コミットグラフを表示する拡張機能
  - GitLensにもコミットグラフはありますが、Pro（有料版）限定の提供のため、ここではこちらの拡張機能を使用する

# Pull Request / Merge Request テンプレート

GitHubやGitLabでは、プルリクエスト作成時のテンプレートを作ることができる。チームでプルリクエストに書いてほしいことを明示的にすることで、レビュー効率の向上や障害調査に役立てることができる。

GitHubでは `.github/PULL_REQUEST_TEMPLATE.md` に記載する（GitLabでは `.gitlab/merge_request_templates/{your_template}.md` を配置する）。

テンプレートの例を以下にあげる。

```md
## チケットURL

## 特に見てほしいレビューポイント

## 残課題（別チケットで対応予定の内容、別プルリクエストで対応予定の内容）

## 動作確認内容（画面キャプチャなど）

## セルフチェックリスト

- [ ] 開発規約(DEVELOPMENT.md) を確認した
- [ ] Files changed を開き、変更内容を確認した
- [ ] コードの変更に伴い、同期必要な設計ドキュメントを更新した
- [ ] 今回のPRでは未対応の残課題があればIssueに起票した
```

# Git、Git LFS、SVN の使い分け

設計ドキュメント（Excelなど）・画像・機械学習モデルなどのバイナリデータをGitで管理する場合、差分確認ができずマージが困難である点や、リポジトリ肥大化の課題がある。そのため、Git LFS、SVN、あるいはファイルサーバーなどの使い分けが求められる。このうち、SVNはコード（Git）との同期に難点がある。例えば、ソースコードのバージョン v1.5.0 には機械学習モデル v2.1 が必要といった紐づけが必要な場合、工夫が必要となる。この場合、Git LFSが優位である。しかし、Git LFSはSVNに比べるとロック取得の運用が難しい点と、Gitに不慣れな担当者（設計書レビュアーなど）にとっては学習コストが高い点がデメリットとなる。

| 特徴              | Git                            | Git LFS                            | SVN (Subversion)                            | Google Drive/ファイルサーバ |
| :---------------- | :----------------------------- | :--------------------------------- | :------------------------------------------ | :-------------------------- |
| 履歴の持ち方      | ✅️全履歴をローカルに複製       | ✅️実体はサーバー、ポインタのみ管理 | ✅️最新版のみ取得（履歴はサーバー）          | ⚠️履歴管理は限定的          |
| Gitと同期         | ✅️                             | ✅️ Gitのため                       | ⚠️ 運用設計が必要                           | ⚠️ 運用設計が必要           |
| 部分取得          | ⚠️苦手 (Sparse checkoutは複雑) | ✅️LFS対象のみ都度取得              | ✅️得意 (ディレクトリ単位でチェックアウト可) | ✅️                          |
| 排他制御 (ロック) | ❌️基本なし                     | ⚠️可能だが運用注意                 | ✅️得意 (Lockが直感的で容易)                 | ❌️基本なし                  |

推奨は以下の通り。

1. 数MB以上のバイナリファイルでかつ更新頻度も高いが、最新断面のみの保持で問題ない（厳密な紐づけは不要である）場合は、SVNを利用する
   - 過去の全履歴をローカルに持つ必要がないため、開発PCのストレージを圧迫しないため
   - ファイルロック機能で同時編集の事故を防げるため
   - 非エンジニア（PM/Manager）のレビュー参加も容易になるため
2. 数MB以上のバイナリファイルでかつ、コードとバイナリの同期を完全に取りたい場合は、Git LFSを採用する
   - 機械学習モデルなどが該当
   - 特定のコードバージョンとバイナリが密結合しており、完全に同期した状態を作るべきであるため
   - 導入時は `.gitattributes` で拡張子指定（例: `*.h5`, `*.onnx`）を行い、チーム全体でLFS管理を強制する設定を必ず指定する
3. 更新頻度が低いWebサイトのUI画像パーツなどは、Gitをそのまま用いる
   - ファイルサイズが小さく（数KB〜数MB）、更新も稀であれば、LFS等の仕組みを導入するコストの方が高いため
4. 更新頻度が高いイベント用バナー画像・販促素材などは、SVNか HeadlessCMSを利用する
   - Git管理するとリポジトリが肥大化するため。コードとの同期よりも、コンテンツとしての管理が主となるため、SVNや専用のCMSでの管理が適するため
5. バージョン管理が不要で、とりあえず共有すればよい一時的なファイルや、テストの画面キャプチャを含むエビデンス結果などは、Google Driveなどで管理する
   - リンクをREADMEに貼る運用を検討する

フローで示すと以下となる。

```mermaid
flowchart LR
    Start([管理対象ファイル]) --> CheckText{テキストであるか？}

    CheckText -- Yes --> Git>Git<br>通常のソースコード管理]
    CheckText -- No --> CheckSync{コードとの<br>厳密な同期が必要か？}

    CheckSync -- Yes --> GitLFS>Git LFS<br>MLモデルなど]
    CheckSync -- No --> CheckSize{サイズ小＆更新頻度低}

    CheckSize -- Yes --> GitBinary>Git<br>変更の少ないアイコンなど]
    CheckSize -- No --> CheckDoc{設計書か？}

    CheckDoc -- Yes --> SVN>SVN<br>Excel/PPT]
    CheckDoc -- No --> FileServer><b>Google Drive</b><br>共有のみが目的のファイル<br>テストエビデンスなど<br>]
```

::: tip Markdownベースの設計書
SVN環境を用意したくない、ライトに管理したい場合は、[Markdownベースの設計書](/documents/forMarkdown/markdown_design_document.html)で済ませるパターンも考えられる。
:::

# GitHub推奨設定

業務利用でのチーム開発を想定しており、リポジトリは以下の条件を満たす前提とする。

- プライベートリポジトリ
- Organization配下に作成
- Teamsプラン以上の有料契約（※プロテクトブランチの機能などを利用するために必要）

## General

| Category      | Item                                                             | Value        | Memo                                                                                       |
| ------------- | ---------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------ |
| General       | Require contributors to sign off on web-based commits            | チェックなし | 著作権・ライセンス承諾の場合に用いるが、業務アプリ開発では不要                             |
|               | Default branch                                                   | develop      |                                                                                            |
| Pull Requests | Allow merge commits                                              | ✅️           | main <- developなどのマージ時に必要                                                        |
|               | Allow squash merging                                             | ✅️           | develop <- feature はSquash mergeを推奨                                                    |
|               | Allow rebase merging                                             | -            | 利用しないため、チェックを外す                                                             |
|               | Allow suggest updating pull request branches                     | ✅️           | Pull Request作成後、ベースブランチが更新された場合、ソースブランチの更新を提案してくれる   |
|               | Automatically delete head branches                               | ✅️           | マージ後にfeature branchを削除するため有効にする                                           |
| Pushes        | Limit how many branches and tags can be updated in a single push | 5            | Git push origin –mirrorで誤ってリモートブランチを破壊しないようにする。推奨値の5を設定する |
| Security      | Secret scanning                                                  | ✅️           | コードやIssue、コメント等のクレデンシャル情報を検知し、通知を行う                          |
|               | Push Protection                                                  | ✅️           | プッシュ時にクレデンシャル情報が検知された場合、プッシュをブロックする                     |

## Access

| Category                | Item          | Value      | Memo  |
| ----------------------- | ------------- | ---------- | ----- |
| Collaborators and teams | Choose a role | 任意の権限 | ※後述 |

- 各ロールの権限については、公式ドキュメントを参照
- 通常、開発者には `Write` ロールを付与する
- 開発しない、例えばスキーマファイルの参照のみ必要であれば、`Read` 権限を、Issueの起票などのみ実施するマネージャーであれば `Triage` ロールを付与する
- `Maintain` 権限は、付与しない
- `Admin` 権限は、マネージャークラスに対して合計2~3名を付与し、属人化しないようにする
  - 1名でも、4名以上でもNGとする

## Code and automation

### Branches

Branch protection rules にdevelop, mainなど永続的なブランチに保護設定を追加する。

| Category                  | Item                                                             | Value | Memo                                                                                                 |
| ------------------------- | ---------------------------------------------------------------- | ----- | ---------------------------------------------------------------------------------------------------- |
| Protect matching branches | Require a pull request before merging                            | ✅️    | プルリクエストを必須とする                                                                           |
|                           | Require approvals                                                | ✅️    | レビューを必須とする                                                                                 |
|                           | Required number of approvals before merging                      | 1     | 最低1名以上の承認を必須とする                                                                        |
|                           | Dismiss stale pull request approvals when new commits are pushed | -     | レビュー承認後のPushで再承認を必要とするかだが、レビュー運用上に支障となることも多く、チェックを外す |
|                           | Require status checks to pass before merging                     | ✅️    | CIの成功を条件とする                                                                                 |
|                           | Require branches to be up to date before merging                 | 任意  | CIパイプラインのワークフロー名を指定                                                                 |
|                           | Require conversation resolution before merging                   | -     | レビューコメントがすべて解決していることを条件とする。チェックを外す                                 |
|                           | Require signed commits                                           | ✅️    | 署名付きコミットを必須化し、セキュアな設定にする                                                     |
|                           | Require linear history                                           | ✅️/-  | mainブランチの場合はOFFとするが、developの場合はSquash mergeを求めるため有効にする                   |
|                           | Do not allow bypassing the above settings                        | ✅️    | パイパスを許容しない                                                                                 |

`develop` ブランチに対し `require linear history` を選択することを推奨することで、`Create a merge commit` が選択できないようにする。

また、意図しない方法でのマージを避けるためにブランチごとにマージ戦略を設定しておき、想定外のマージ戦略が選択された時に警告色を表示するというサードパーティ製のChrome拡張[^1]も存在する。必要に応じて導入を検討する。

[^1]: [GitHubで誤ったマージ戦略のマージを防ぐChrome拡張機能の開発をした](https://zenn.dev/daku10/articles/github-merge-guardian)

### Tags

| Category | Item         | Value                | Memo                                                     |
| -------- | ------------ | -------------------- | -------------------------------------------------------- |
|          | Protect tags | v[0-9]+.[0-9]+.[0-9] | セマンティックバージョニングに則ったタグのみ、削除を防ぐ |

### GitHub Actions

| Category            | Item                                                                                                                                | Value | Memo |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----- | ---- |
| Actions permissions | Allow asset-taskforce, and select non-asset-taskforce, actions and reusable workflows > Allow actions created by GitHub             | ✅️    |      |
|                     | Allow asset-taskforce, and select non-asset-taskforce, actions and reusable workflows > Allow actions Marketplace verified creators | ✅️    |      |

### Code security and analysis

| Category   | Item                        | Value | Memo                                       |
| ---------- | --------------------------- | ----- | ------------------------------------------ |
| Dependabot | Dependabot alerts           | ✅️    | 依存パッケージのアップデートを検知するため |
|            | Dependabot security updates | ✅️    |                                            |
|            | Dependabot version updates  | ✅️    |                                            |

# GitLab推奨設定

- GitHubの `Automatically delete head branches`
  - マージリクエストから `Delete source branch` オプションを有効にすることが該当
  - プロジェクトの設定で `Enable "Delete source branch" option by default` を選択しておくとデフォルトで有効になる
