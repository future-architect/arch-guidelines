import { fileURLToPath } from "url";
import { defineConfig as defineConfigBase } from "vitepress";
import { withMermaid } from "vitepress-plugin-mermaid";
import { Module } from "module";
import markdownItTaskLists from "markdown-it-task-lists";
import markdownItFootnote from "markdown-it-footnote";
import markdownItHeaderShift from "./lib/markdown-it-plugin-header-shift.mjs";
import * as plantumlLanguage from "./lib/plantuml.tmlanguage.mjs";
const __filename = fileURLToPath(import.meta.url);
const pkg = Module.createRequire(__filename)("../package.json");

const repoUrl = pkg.repository.url
  .replace(/\.git$/u, "")
  .replace(/^git\+/u, "");

/** @type {import("vitepress").DefaultTheme.Sidebar} */
const links = {
  "/documents/forWebFrontend/": [
    { text: "Introduction", link: "/documents/forWebFrontend/" },
    {
      text: "Webフロントエンド設計ガイドライン",
      link: "/documents/forWebFrontend/web_frontend_guidelines.html",
    },
  ],
  "/documents/forWebAPI/": [
    { text: "Introduction", link: "/documents/forWebAPI/" },
    {
      text: "Web API設計ガイドライン",
      link: "/documents/forWebAPI/web_api_guidelines.html",
    },
  ],
  "/documents/forBatch/": [
    { text: "Introduction", link: "/documents/forBatch/" },
    {
      text: "バッチ設計ガイドライン",
      link: "/documents/forBatch/batch_guidelines.html",
    },
  ],
  "/documents/forIF/": [
    { text: "Introduction", link: "/documents/forIF/" },
    {
      text: "I/F設計ガイドライン",
      link: "/documents/forIF/if_guidelines.html",
    },
  ],
  "/documents/forAsync/": [
    { text: "Introduction", link: "/documents/forAsync/" },
    {
      text: "非同期設計ガイドライン",
      link: "/documents/forAsync/async_guidelines.html",
    },
  ],
  "/documents/forMail/": [
    { text: "Introduction", link: "/documents/forMail/" },
    {
      text: "メール設計ガイドライン",
      link: "/documents/forMail/mail_guidelines.html",
    },
  ],
  "/documents/forLog/": [
    { text: "Introduction", link: "/documents/forLog/" },
    {
      text: "ログ設計ガイドライン",
      link: "/documents/forLog/log_guidelines.html",
    },
  ],
  "/documents/forDB/": [
    { text: "Introduction", link: "/documents/forDB/" },
    {
      text: "PostgreSQL設計ガイドライン",
      link: "/documents/forDB/postgresql_guidelines.html",
    },
    {
      text: "DynamoDB設計ガイドライン",
      link: "/documents/forDB/dynamodb_guidelines.html",
    },
  ],
  "/documents/forAWS/": [
    { text: "Introduction", link: "/documents/forAWS/" },
    {
      text: "AWS設計ガイドライン",
      link: "/documents/forAWS/aws_guidelines.html",
    },
  ],
  "/documents/forTerraform/": [
    { text: "Introduction", link: "/documents/forTerraform/" },
    {
      text: "Terraform設計ガイドライン",
      link: "/documents/forTerraform/terraform_guidelines.html",
    },
  ],
  "/documents/forDataManagement/": [
    { text: "Introduction", link: "/documents/forDataManagement/" },
    {
      text: "データマネジメント設計ガイドライン",
      link: "/documents/forDataManagement/datamanagement_guidelines.html",
    },
  ],
  "/documents/forGitBranch/": [
    { text: "Introduction", link: "/documents/forGitBranch/" },
    {
      text: "Gitブランチフロー規約",
      link: "/documents/forGitBranch/git_branch_standards.html",
    },
    {
      text: "VS Code Git操作",
      link: "/documents/forGitBranch/vscode_git_operation.html",
    },
  ],
  "/documents/forMarkdown/": [
    { text: "Introduction", link: "/documents/forMarkdown/" },
    {
      text: "Markdown設計ドキュメント規約",
      link: "/documents/forMarkdown/markdown_design_document.html",
    },
    {
      text: "サンプルプロジェクト",
      link: "/documents/forMarkdown/sample",
      items: [
        {
          text: "画面一覧",
          link: "/documents/forMarkdown/sample/ui",
          items: [
            { text: "UIS01", link: "/documents/forMarkdown/sample/ui/UIS01" },
            { text: "UIS02", link: "/documents/forMarkdown/sample/ui/UIS02" },
            { text: "UIS03", link: "/documents/forMarkdown/sample/ui/UIS03" },
            { text: "UIS04", link: "/documents/forMarkdown/sample/ui/UIS04" },
            { text: "UIM01", link: "/documents/forMarkdown/sample/ui/UIM01" },
            { text: "UIM02", link: "/documents/forMarkdown/sample/ui/UIM02" },
            { text: "UIM03", link: "/documents/forMarkdown/sample/ui/UIM03" },
            { text: "UIM04", link: "/documents/forMarkdown/sample/ui/UIM04" },
          ],
        },
      ],
    },
  ],
  "/documents/forSlack/": [
    { text: "Introduction", link: "/documents/forSlack/" },
    {
      text: "Slack利用ガイドライン",
      link: "/documents/forSlack/slack_usage_guidelines.html",
    },
  ],
  "/documents/forCodeReview/": [
    { text: "Introduction", link: "/documents/forCodeReview/" },
    {
      text: "コードレビューガイドライン",
      link: "/documents/forCodeReview/code_review.html",
    },
  ],
  "/documents/forSoftSkill/": [
    { text: "Introduction", link: "/documents/forSoftSkill/" },
    {
      text: "ソフトスキルガイドライン",
      link: "/documents/forSoftSkill/softskill_guidelines.html",
    },
  ],
};

/**
 * @typedef {import('vitepress').UserConfig<import('vitepress').DefaultTheme.Config>} VitepressConfig
 */
/**
 * @param {VitepressConfig} config config
 * @returns {VitepressConfig} config
 */
function defineConfig(config) {
  return withMermaid(defineConfigBase(config));
}

export default defineConfig({
  title: "フューチャー株式会社",
  description:
    "フューチャー株式会社の有志が作成する<br>良いアーキテクチャを実現するための設計ガイドライン",
  outDir: "docs",
  ignoreDeadLinks: "localhostLinks",
  markdown: {
    lineNumbers: true,
    config(md) {
      md.use(markdownItHeaderShift);
      md.use(markdownItTaskLists);
      md.use(markdownItFootnote);
    },
    languages: [plantumlLanguage],
  },
  locales: {
    root: {
      lang: "ja",
    },
  },
  head: [
    [
      "link",
      {
        rel: "icon",
        href: "/arch-guidelines/favicon.ico",
        sizes: "any",
      },
    ],
    [
      "link",
      {
        rel: "icon",
        href: `/arch-guidelines/images/logo-system.svg`,
        type: "image/svg+xml",
      },
    ],
    ["meta", { property: "og:type", content: "website" }],
    ["meta", { property: "og:locale", content: "ja_JP" }],
    [
      "meta",
      {
        property: "og:site_name",
        content: "アーキテクチャ設計ガイドライン | フューチャー株式会社",
      },
    ],
  ],
  transformHead({ pageData }) {
    const head = [];

    // タイトルの設定: Frontmatterにタイトルがあれば「記事タイトル | サイト名」、なければ「サイト名」
    const title = pageData.frontmatter.title
      ? `${pageData.frontmatter.title}`
      : "アーキテクチャ設計ガイドライン";

    head.push(["meta", { property: "og:title", content: title }]);

    // 説明文の設定: Frontmatterにdescriptionがあれば使用、なければデフォルトを使用
    const description =
      pageData.frontmatter.description ||
      "フューチャー株式会社の有志が作成する良いアーキテクチャを実現するための設計ガイドライン";

    head.push(["meta", { property: "og:description", content: description }]);
    head.push(["meta", { name: "description", content: description }]);

    return head;
  },
  srcExclude: ["./README.md"],
  base: "/arch-guidelines/",
  themeConfig: {
    siteTitle: "Future <wbr>Architecture Guidelines",
    logo: {
      light: "/images/logo.svg",
      dark: "/images/logo-dark.svg",
    },
    footer: {
      copyright: `Copyright ${new Date().getFullYear()} by Future Corporation`,
    },
    search: {
      provider: "local",
      options: {
        detailedView: true,
      },
    },
    editLink: {
      pattern: repoUrl + "/edit/main/:path",
    },
    outline: {
      level: "deep",
    },
    nav: [
      {
        text: "Guidelines",
        items: [
          {
            text: "アプリケーション",
            items: [
              {
                text: "Web フロントエンド",
                link: "/documents/forWebFrontend/web_frontend_guidelines.html",
              },
              {
                text: "Web API",
                link: "/documents/forWebAPI/web_api_guidelines.html",
              },
              {
                text: "非同期",
                link: "/documents/forAsync/async_guidelines.html",
              },
              {
                text: "バッチ",
                link: "/documents/forBatch/batch_guidelines.html",
              },
              {
                text: "I/F",
                link: "/documents/forIF/if_guidelines.html",
              },
              {
                text: "メール",
                link: "/documents/forMail/mail_guidelines.html",
              },
              {
                text: "ログ",
                link: "/documents/forLog/log_guidelines.html",
              },
            ],
          },
          {
            text: "DB",
            items: [
              {
                text: "PostgreSQL",
                link: "/documents/forDB/postgresql_guidelines.html",
              },
              {
                text: "DynamoDB",
                link: "/documents/forDB/dynamodb_guidelines.html",
              },
              {
                text: "データマネジメント",
                link: "/documents/forDataManagement/datamanagement_guidelines.html",
              },
            ],
          },
          {
            text: "インフラ",
            items: [
              {
                text: "AWS",
                link: "/documents/forAWS/aws_guidelines.html",
              },
              {
                text: "Terraform",
                link: "/documents/forTerraform/terraform_guidelines.html",
              },
            ],
          },
          {
            text: "開発生産性",
            items: [
              {
                text: "Gitブランチフロー",
                link: "/documents/forGitBranch/git_branch_standards.html",
              },
              {
                text: "Markdown設計ドキュメント",
                link: "/documents/forMarkdown/markdown_design_document.html",
              },
              {
                text: "コードレビュー",
                link: "/documents/forCodeReview/code_review.html",
              },
              {
                text: "Slack利用",
                link: "/documents/forSlack/slack_usage_guidelines.html",
              },
            ],
          },
          {
            text: "その他",
            items: [
              {
                text: "ソフトスキル",
                link: "/documents/forSoftSkill/softskill_standards.html",
              },
            ],
          },
        ],
      },
      {
        text: "About Us",
        items: [
          {
            text: "フューチャー株式会社",
            link: "https://www.future.co.jp/",
          },
          {
            text: "Blog",
            link: "https://future-architect.github.io/",
          },
          {
            text: "Qiita",
            link: "https://qiita.com/organizations/future",
          },
          {
            text: "X",
            link: "https://twitter.com/future_techblog",
          },
          {
            text: "Facebook",
            link: "https://www.facebook.com/future.saiyo/",
          },
          {
            text: "Email <techblog@future.co.jp>",
            link: "mailto:techblog@future.co.jp",
          },
        ],
      },
    ],

    sidebar: links,

    socialLinks: [
      {
        icon: "github",
        link: repoUrl,
      },
    ],
  },
});
