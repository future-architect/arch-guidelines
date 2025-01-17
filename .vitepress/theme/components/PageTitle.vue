<template>
  <div class="vitepress-page-title">
    <div class="share-buttons">
      <a
        href="https://twitter.com/share?ref_src=twsrc%5Etfw"
        class="twitter-share-button"
        :data-url="pageUrl"
        data-show-count="false"
      >
        Tweet
      </a>
      <div
        class="fb-like"
        :data-href="pageUrl"
        data-layout="button_count"
        data-action="like"
        data-size="small"
        data-show-faces="true"
        data-share="true"
      />
      <a
        :href="
          'http://b.hatena.ne.jp/entry/s/future-architect.github.io' +
          $page.path
        "
        class="hatena-bookmark-button"
        data-hatena-bookmark-layout="basic-label-counter"
        data-hatena-bookmark-lang="ja"
        title="このエントリーをはてなブックマークに追加"
      >
        <img
          src="https://b.st-hatena.com/images/v4/public/entry-button/button-only@2x.png"
          alt="このエントリーをはてなブックマークに追加"
          width="20"
          height="20"
          style="border: none"
        />
      </a>

      <component
        :is="GithubButton"
        href="https://github.com/future-architect/arch-guidelines"
        data-icon="octicon-star"
        data-show-count="true"
        aria-label="Star future-architect/arch-guidelines on GitHub"
      >
        Star
      </component>

      <a
        href="https://getpocket.com/save"
        class="pocket-btn"
        data-lang="en"
        :data-save-url="pageUrl"
        data-pocket-count="horizontal"
        data-pocket-align="left"
        >Pocket</a
      >
    </div>

    <h1 class="vitepress-page-title__title">
      {{ $page.title }}
    </h1>
    <div class="vitepress-page-title__author">
      {{ $page.frontmatter.author }}
    </div>
  </div>
</template>

<script>
import { useRoute } from "vitepress";
import { addTwitter, addFacebook, addHatenaBookmark, addPocket } from "./sns";
import { markRaw } from "vue";
/**
 * `markdown-it-plugin-header-shift`でheaderタグを1つづつずらす前提であるため、Markdownファイルにはタイトルがありません。
 * これを回避するためにMarkdownファイルの先頭に`<page-title/>`を記述させることでタイトルを表示させます。
 */
export default {
  name: "PageTitle",
  data: function () {
    return {
      GithubButton: "div",
    };
  },
  computed: {
    $page() {
      const route = useRoute();
      return {
        path: route.path,
        title: route.data.title,
        frontmatter: route.data.frontmatter,
      };
    },
    pageUrl() {
      return "https://future-architect.github.io" + this.$page.path;
    },
  },
  mounted() {
    if (import.meta.env.SSR) return;
    import("vue-github-button").then(({ default: GithubButton }) => {
      this.GithubButton = markRaw(GithubButton);
    });
    setTimeout(() => {
      addTwitter();
      addFacebook();
      addHatenaBookmark();
      addPocket();
    }, 10);
  },
};
</script>

<style scoped>
.share-buttons {
  color-scheme: initial; /* darkにすると透過されないのでリセットする */
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.vitepress-page-title ::v-deep(.share-buttons > *) {
  padding-left: 5px;
}

.vitepress-page-title__author {
  padding-bottom: 8px;
  margin-bottom: 18px;
  font-size: 12px;
  border: none;
  color: initial;
  text-align: right;
  page-break-after: always;

  font-weight: 600;
  line-height: 1.25;

  border-bottom: 1px solid #eaecef;
}

@media print {
  .share-buttons {
    display: none;
  }

  .vitepress-page-title__title {
    text-align: center;
    margin-top: 50%;
    page-break-before: auto;
  }
  .vitepress-page-title__author {
    page-break-after: always;
  }
}
</style>
