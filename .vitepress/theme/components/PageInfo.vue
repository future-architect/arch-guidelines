<template>
  <div class="page-info">
    <div
      class="fb-like"
      :data-href="href"
      data-layout="button_count"
      data-action="like"
      data-size="small"
      data-show-faces="true"
      data-share="true"
      style="height: 20px; line-height: 20px"
    />
    <a
      :href="hatena"
      class="hatena-bookmark-button"
      data-hatena-bookmark-layout="basic-label-counter"
      data-hatena-bookmark-lang="ja"
      title="このエントリーをはてなブックマークに追加"
    >
      <img
        src="https://b.st-hatena.com/images/entry-button/button-only@2x.png"
        alt="このエントリーをはてなブックマークに追加"
        width="20"
        height="20"
        style="border: none"
      />
    </a>
  </div>
</template>

<script>
import { addFacebook, addHatenaBookmark } from "./sns";

function debounce(fn, timeout) {
  let timeoutId;
  return () => {
    if (timeoutId != null) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(fn, timeout);
  };
}

const loadScript = debounce(function () {
  addFacebook();
  addHatenaBookmark();
}, 1000);

export default {
  name: "PageInfo",
  props: {
    href: {
      type: String,
      required: true,
    },
  },
  computed: {
    hatena() {
      return this.href.replace("https://", "https://b.hatena.ne.jp/entry/s/");
    },
  },
  mounted() {
    if (import.meta.env.SSR) return;
    loadScript();
  },
};
</script>

<style scoped>
.page-info {
  color-scheme: initial; /* darkにすると透過されないのでリセットする */
  display: inline-flex;
  align-items: flex-end;
}
.page-info ::v-deep(.hatena-bookmark-button-frame) {
  margin-left: 4px;
}
</style>
