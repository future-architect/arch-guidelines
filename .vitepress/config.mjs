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
  "/documents/forDB/": [
    { text: "Introduction", link: "/documents/forDB/" },
    {
      text: "PostgreSQL設計ガイドライン",
      link: "/documents/forDB/terraform_guidelines.html",
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
  ],
  "/documents/forMarkdown/": [
    { text: "Introduction", link: "/documents/forMarkdown/" },
    {
      text: "Markdown設計ドキュメント規約",
      link: "/documents/forMarkdown/markdown_design_document.html",
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
  title: "Future Enterprise Arch Guidelines",
  description:
    "フューチャー株式会社が作成するエンタープライズ領域に特化したアーキテクチャガイドライン",
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
        href: `/arch-guidelines/images/logo-system.svg`,
        type: "image/svg+xml",
      },
    ],
  ],
  srcExclude: ["./README.md"],
  base: "/arch-guidelines/",
  themeConfig: {
    siteTitle: "Future Enterprise <wbr>Arch Guidelines",
    logo: {
      light: "/images/logo.svg",
      dark: "/images/logo-dark.svg",
    },
    footer: {
      copyright: `©2015 - ${new Date().getFullYear()} Future Enterprise Arch Guidelines - Future Corporation`,
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
            text: "Web Frontend",
            items: [
              {
                text: "Introduction",
                link: "/documents/forWebFrontend/",
              },
              {
                text: "Web フロントエンド設計ガイドライン",
                link: "/documents/forWebFrontend/web_frontend_guidelines.html",
              },
            ],
          },
          {
            text: "Web API",
            items: [
              {
                text: "Introduction",
                link: "/documents/forWebAPI/",
              },
              {
                text: "Web API設計ガイドライン",
                link: "/documents/forWebAPI/web_api_guidelines.html",
              },
            ],
          },
          {
            text: "Batch",
            items: [
              {
                text: "Introduction",
                link: "/documents/forBatch/",
              },
              {
                text: "バッチ設計ガイドライン",
                link: "/documents/forBatch/batch_guidelines.html",
              },
            ],
          },
          {
            text: "DB",
            items: [
              {
                text: "Introduction",
                link: "/documents/forDB/",
              },
              {
                text: "PostgreSQL設計ガイドライン",
                link: "/documents/forDB/postgresql_gbatch_guidelinesuidelines.html",
              },
            ],
          },
          {
            text: "Terraform",
            items: [
              {
                text: "Introduction",
                link: "/documents/forTerraform/",
              },
              {
                text: "Terraform設計ガイドライン",
                link: "/documents/forTerraform/terraform_guidelines.html",
              },
            ],
          },
          {
            text: "DataManagement",
            items: [
              {
                text: "Introduction",
                link: "/documents/forDataManagement/",
              },
              {
                text: "データマネジメント設計ガイドライン",
                link: "/documents/forDataManagement/datamanagement_guidelines.html",
              },
            ],
          },
          {
            text: "Git",
            items: [
              {
                text: "Introduction",
                link: "/documents/forGitBranch/",
              },
              {
                text: "Gitブランチフロー規約",
                link: "/documents/forGitBranch/git_branch_standards.html",
              },
            ],
          },
          {
            text: "Markdown",
            items: [
              {
                text: "Introduction",
                link: "/documents/forMarkdown/",
              },
              {
                text: "Markdown設計ドキュメント規約",
                link: "/documents/forMarkdown/markdown_design_document.html",
              },
            ],
          },
          {
            text: "レビュー",
            items: [
              {
                text: "Introduction",
                link: "/documents/forCodeReview/",
              },
              {
                text: "コードレビューガイドライン",
                link: "/documents/forCodeReview/code_review.html",
              },
            ],
          },
          {
            text: "Slack",
            items: [
              {
                text: "Introduction",
                link: "/documents/forSlack/",
              },
              {
                text: "Slack利用ガイドライン",
                link: "/documents/forSlack/slack_usage_guidelines.html",
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
            text: "Twitter",
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
