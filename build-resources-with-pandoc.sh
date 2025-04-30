#!/bin/sh
set -e

ROOT_DIR=`pwd`
CSS_PATH="${ROOT_DIR}/documents/common/pandoc_styles/css/style.css"
STYLE_DOCX_PATH="${ROOT_DIR}/documents/common/pandoc_styles/スタイル.docx"
RESOURCES_DIR="${ROOT_DIR}/public/resources"

# バージョンチェック
cat /etc/alpine-release

apk update

# apkによるインストール
## chromium のインストール
apk add --update chromium

## nodejs のインストール
apk add --no-cache nodejs-current npm
npm install -g npm@9

# グローバルインストールされたnpmのパスを通す
NPM_GLOBAL_BIN=$(npm prefix -g)/bin
echo "NPM global bin path: ${NPM_GLOBAL_BIN}"
# 取得したディレクトリを PATH 環境変数の先頭に追加
export PATH="${NPM_GLOBAL_BIN}:${PATH}"
echo "Updated PATH: ${PATH}"
# 更新された npm の場所とバージョンを再確認
echo "Checking updated npm location and version..."
which npm
npm -v

# バージョンチェック
echo "Node version: $(node -v)"
echo "npm version: $(npm -v)"

## Playwright が Alpine で必要とする可能性のある依存関係を追加
echo "Installing potential Playwright dependencies for Alpine..."
apk add --no-cache \
    udev \
    ttf-freefont \
    fontconfig \
    dbus \
    freetype \
    harfbuzz \
    nss

## 日本語用フォントのインストール
apk add --no-cache curl fontconfig
curl -O https://moji.or.jp/wp-content/ipafont/IPAexfont/IPAexfont00301.zip
mkdir -p /usr/share/fonts/ipa
mkdir -p /temp
unzip IPAexfont00301.zip -d /temp
cp /temp/IPAexfont00301/*.ttf /usr/share/fonts/ipa/
rm IPAexfont00301.zip

# バージョンチェック
chromium --version

# mermaid-filterに必要な変数をセット
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD='true'
export MERMAID_FILTER_PUPPETEER_CONFIG="${ROOT_DIR}/.puppeteer.json"
export PUPPETEER_EXECUTABLE_PATH="/usr/bin/chromium"
# export MERMAID_FILTER_FORMAT="svg" # docxでの出力時にはsvgは使えません

# mermaid-filterのインストール
npm i -g mermaid-filter@1.4.7

# Web API
cd ${ROOT_DIR}/documents/forWebAPI

pandoc ./web_api_guidelines.md -s --self-contained --number-sections --toc -t html5 -c ${CSS_PATH} -o ${RESOURCES_DIR}/WebAPI設計ガイドライン.html
pandoc ./web_api_guidelines.md --toc --reference-doc=${STYLE_DOCX_PATH} -s -o ${RESOURCES_DIR}/WebAPI設計ガイドライン.docx

# PostgreSQL
cd ${ROOT_DIR}/documents/forDB

pandoc ./postgresql_guidelines.md -s --self-contained --number-sections --toc -t html5 -c ${CSS_PATH} -o ${RESOURCES_DIR}/PostgreSQL設計ガイドライン.html
pandoc ./postgresql_guidelines.md --toc --reference-doc=${STYLE_DOCX_PATH} -s -o ${RESOURCES_DIR}/PostgreSQL設計ガイドライン.docx

# Terraform
cd ${ROOT_DIR}/documents/forTerraform

pandoc ./terraform_guidelines.md -s --self-contained --number-sections --toc -t html5 -c ${CSS_PATH} -o ${RESOURCES_DIR}/Terraform設計ガイドライン.html
pandoc ./terraform_guidelines.md --toc --reference-doc=${STYLE_DOCX_PATH} -s -o ${RESOURCES_DIR}/Terraform設計ガイドライン.docx

# Markdown
cd ${ROOT_DIR}/documents/forMarkdown

pandoc ./markdown_design_document.md -s --self-contained --number-sections --toc -t html5 -c ${CSS_PATH} -o ${RESOURCES_DIR}/Markdown設計ドキュメント規約.html
pandoc ./markdown_design_document.md --toc --reference-doc=${STYLE_DOCX_PATH} -s -o ${RESOURCES_DIR}/Markdown設計ドキュメント規約.docx

# Slack
cd ${ROOT_DIR}/documents/forSlack

pandoc ./slack_usage_guidelines.md -s --self-contained --number-sections --toc -t html5 -c ${CSS_PATH} -o ${RESOURCES_DIR}/Slack利用ガイドライン.html
pandoc ./slack_usage_guidelines.md --toc --reference-doc=${STYLE_DOCX_PATH} -s -o ${RESOURCES_DIR}/Slack利用ガイドライン.docx

# コードレビュー
cd ${ROOT_DIR}/documents/forCodeReview

pandoc ./code_review.md -s --self-contained --number-sections --toc -t html5 -c ${CSS_PATH} -o ${RESOURCES_DIR}/コードレビューガイドライン.html
pandoc ./code_review.md --toc --reference-doc=${STYLE_DOCX_PATH} -s -o ${RESOURCES_DIR}/コードレビューガイドライン.docx

# Git
cd ${ROOT_DIR}/documents/forGitBranch

pandoc ./git_branch_standards.md -s --self-contained --number-sections --toc -t html5 -c ${CSS_PATH} -o ${RESOURCES_DIR}/Gitブランチフロー規約.html
pandoc ./git_branch_standards.md --toc --reference-doc=${STYLE_DOCX_PATH} -s -o ${RESOURCES_DIR}/Gitブランチフロー規約.docx
